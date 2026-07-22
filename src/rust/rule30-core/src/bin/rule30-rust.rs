//! Production command-line interface for the verified Rust Rule 30 engines.

#![forbid(unsafe_code)]

use std::env;
use std::ffi::OsString;
use std::io::{self, Write};
use std::process::ExitCode;

use rule30_core::{CenterEngine, CoordinateEngine, PackedEngine};

const OUTPUT_CHUNK_BYTES: usize = 64 * 1024;
const MAX_COORDINATE_COUNT: usize = 250_000;
const MAX_PACKED_COUNT: usize = 10_000_000;

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
enum Backend {
    Coordinate,
    Packed,
}

impl Backend {
    const fn name(self) -> &'static str {
        match self {
            Self::Coordinate => "coordinate",
            Self::Packed => "packed",
        }
    }

    const fn maximum_count(self) -> usize {
        match self {
            Self::Coordinate => MAX_COORDINATE_COUNT,
            Self::Packed => MAX_PACKED_COUNT,
        }
    }
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
enum OutputFormat {
    Raw,
    Json,
}

impl OutputFormat {
    const fn name(self) -> &'static str {
        match self {
            Self::Raw => "raw",
            Self::Json => "json",
        }
    }
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
struct Settings {
    count: usize,
    backend: Backend,
    format: OutputFormat,
}

enum ParseResult {
    Run(Settings),
    Help,
}

#[derive(Clone, Debug, Eq, PartialEq)]
struct GenerationSummary {
    count: usize,
    ones: usize,
    zeros: usize,
    discrepancy: i128,
    sha256_u8: String,
}

fn usage(program: &str, mut output: impl Write) -> io::Result<()> {
    writeln!(
        output,
        concat!(
            "Usage:\n",
            "  {} generate --count N --backend coordinate|packed ",
            "--format raw|json\n\n",
            "Raw output is exactly N numeric bytes (0 or 1), ordered ",
            "c_0 through c_(N-1).\n",
            "JSON output is a streaming summary and does not include the bit prefix.\n",
            "Safety limits: coordinate <= {}; packed <= {}.\n",
            "For benchmarks, use the separately verified rule30-rust-bench binary."
        ),
        program, MAX_COORDINATE_COUNT, MAX_PACKED_COUNT
    )
}

fn required_value(arguments: &[String], index: &mut usize, option: &str) -> Result<String, String> {
    *index += 1;
    arguments
        .get(*index)
        .cloned()
        .ok_or_else(|| format!("{option} requires a value"))
}

fn parse_count(text: &str) -> Result<usize, String> {
    if text.is_empty() || !text.bytes().all(|byte| byte.is_ascii_digit()) {
        return Err("--count requires a nonnegative decimal integer".to_owned());
    }

    let value = text
        .parse::<u128>()
        .map_err(|_| "--count is too large".to_owned())?;
    usize::try_from(value).map_err(|_| "--count is too large for this platform".to_owned())
}

fn parse_backend(text: &str) -> Result<Backend, String> {
    match text {
        "coordinate" => Ok(Backend::Coordinate),
        "packed" => Ok(Backend::Packed),
        _ => Err("--backend must be coordinate or packed".to_owned()),
    }
}

fn parse_format(text: &str) -> Result<OutputFormat, String> {
    match text {
        "raw" => Ok(OutputFormat::Raw),
        "json" => Ok(OutputFormat::Json),
        _ => Err("--format must be raw or json".to_owned()),
    }
}

fn parse_arguments(arguments: &[String]) -> Result<ParseResult, String> {
    let Some(command) = arguments.first() else {
        return Err("the generate command is required".to_owned());
    };
    if command == "--help" || command == "-h" {
        return Ok(ParseResult::Help);
    }
    if command != "generate" {
        return Err(format!("unknown command {command:?}; expected generate"));
    }

    let mut count = None;
    let mut backend = None;
    let mut format = None;
    let mut index = 1;
    while index < arguments.len() {
        match arguments[index].as_str() {
            "--help" | "-h" => return Ok(ParseResult::Help),
            "--count" => {
                if count.is_some() {
                    return Err("--count may only be specified once".to_owned());
                }
                let value = required_value(arguments, &mut index, "--count")?;
                count = Some(parse_count(&value)?);
            }
            "--backend" => {
                if backend.is_some() {
                    return Err("--backend may only be specified once".to_owned());
                }
                let value = required_value(arguments, &mut index, "--backend")?;
                backend = Some(parse_backend(&value)?);
            }
            "--format" => {
                if format.is_some() {
                    return Err("--format may only be specified once".to_owned());
                }
                let value = required_value(arguments, &mut index, "--format")?;
                format = Some(parse_format(&value)?);
            }
            unknown => return Err(format!("unknown option {unknown:?}")),
        }
        index += 1;
    }

    let count = count.ok_or_else(|| "--count is required".to_owned())?;
    let backend = backend.ok_or_else(|| "--backend is required".to_owned())?;
    let format = format.ok_or_else(|| "--format is required".to_owned())?;
    let maximum = backend.maximum_count();
    if count > maximum {
        return Err(format!(
            "--count {count} exceeds the {} backend safety limit {maximum}",
            backend.name()
        ));
    }

    Ok(ParseResult::Run(Settings {
        count,
        backend,
        format,
    }))
}

fn utf8_arguments(arguments: impl Iterator<Item = OsString>) -> Result<Vec<String>, String> {
    arguments
        .map(|argument| {
            argument
                .into_string()
                .map_err(|_| "command-line arguments must be valid UTF-8".to_owned())
        })
        .collect()
}

fn absorb_chunk(
    chunk: &[u8],
    format: OutputFormat,
    output: &mut impl Write,
    digest: &mut Sha256,
) -> Result<(), String> {
    digest.update(chunk);
    if format == OutputFormat::Raw {
        output
            .write_all(chunk)
            .map_err(|error| format!("failed to write raw output: {error}"))?;
    }
    Ok(())
}

fn generate<E: CenterEngine>(
    mut engine: E,
    settings: Settings,
    output: &mut impl Write,
) -> Result<GenerationSummary, String> {
    let mut digest = Sha256::new();
    let mut chunk = Vec::with_capacity(OUTPUT_CHUNK_BYTES);
    let mut ones = 0_usize;

    for emitted in 0..settings.count {
        let bit = engine.center_bit();
        if bit > 1 {
            return Err(format!(
                "{} backend emitted non-binary value {bit} at index {emitted}",
                settings.backend.name()
            ));
        }
        chunk.push(bit);
        ones += usize::from(bit);

        if chunk.len() == OUTPUT_CHUNK_BYTES {
            absorb_chunk(&chunk, settings.format, output, &mut digest)?;
            chunk.clear();
        }
        if emitted + 1 < settings.count {
            engine.advance();
        }
    }

    if !chunk.is_empty() {
        absorb_chunk(&chunk, settings.format, output, &mut digest)?;
    }

    let zeros = settings.count - ones;
    Ok(GenerationSummary {
        count: settings.count,
        ones,
        zeros,
        discrepancy: 2 * (ones as i128) - (settings.count as i128),
        sha256_u8: hex_digest(digest.finalize()),
    })
}

fn write_json_summary(
    summary: &GenerationSummary,
    backend: Backend,
    mut output: impl Write,
) -> Result<(), String> {
    writeln!(
        output,
        concat!(
            "{{\"backend\":\"{}\",",
            "\"bit_order\":\"c_0_to_c_n_minus_1\",",
            "\"count\":{},\"discrepancy\":{},\"ones\":{},",
            "\"sha256_u8\":\"{}\",\"zeros\":{}}}"
        ),
        backend.name(),
        summary.count,
        summary.discrepancy,
        summary.ones,
        summary.sha256_u8,
        summary.zeros
    )
    .map_err(|error| format!("failed to write JSON output: {error}"))
}

fn execute(settings: Settings) -> Result<(), String> {
    let stdout = io::stdout();
    let mut output = stdout.lock();
    let summary = match settings.backend {
        Backend::Coordinate => generate(CoordinateEngine::new(), settings, &mut output)?,
        Backend::Packed => generate(PackedEngine::new(), settings, &mut output)?,
    };

    if settings.format == OutputFormat::Json {
        write_json_summary(&summary, settings.backend, &mut output)?;
    }
    output
        .flush()
        .map_err(|error| format!("failed to flush {} output: {error}", settings.format.name()))
}

fn main() -> ExitCode {
    let mut raw_arguments = env::args_os();
    let program = raw_arguments
        .next()
        .unwrap_or_else(|| OsString::from("rule30-rust"))
        .to_string_lossy()
        .into_owned();
    let arguments = match utf8_arguments(raw_arguments) {
        Ok(arguments) => arguments,
        Err(error) => {
            eprintln!("error: {error}");
            return ExitCode::from(2);
        }
    };

    match parse_arguments(&arguments) {
        Ok(ParseResult::Help) => {
            if let Err(error) = usage(&program, io::stdout().lock()) {
                eprintln!("error: failed to write help output: {error}");
                ExitCode::FAILURE
            } else {
                ExitCode::SUCCESS
            }
        }
        Ok(ParseResult::Run(settings)) => match execute(settings) {
            Ok(()) => ExitCode::SUCCESS,
            Err(error) => {
                eprintln!("error: {error}");
                ExitCode::FAILURE
            }
        },
        Err(error) => {
            eprintln!("error: {error}");
            if let Err(write_error) = usage(&program, io::stderr().lock()) {
                eprintln!("error: failed to write usage: {write_error}");
            }
            ExitCode::from(2)
        }
    }
}

#[derive(Clone)]
struct Sha256 {
    state: [u32; 8],
    block: [u8; 64],
    block_length: usize,
    total_bytes: u64,
}

impl Sha256 {
    const fn new() -> Self {
        Self {
            state: [
                0x6a09_e667,
                0xbb67_ae85,
                0x3c6e_f372,
                0xa54f_f53a,
                0x510e_527f,
                0x9b05_688c,
                0x1f83_d9ab,
                0x5be0_cd19,
            ],
            block: [0; 64],
            block_length: 0,
            total_bytes: 0,
        }
    }

    fn update(&mut self, input: &[u8]) {
        self.total_bytes = self
            .total_bytes
            .checked_add(input.len() as u64)
            .expect("SHA-256 input length overflow");

        let mut offset = 0;
        while offset < input.len() {
            let available = 64 - self.block_length;
            let take = available.min(input.len() - offset);
            self.block[self.block_length..self.block_length + take]
                .copy_from_slice(&input[offset..offset + take]);
            self.block_length += take;
            offset += take;

            if self.block_length == 64 {
                let block = self.block;
                compress_sha256(&mut self.state, &block);
                self.block_length = 0;
            }
        }
    }

    fn finalize(mut self) -> [u8; 32] {
        let bit_length = self
            .total_bytes
            .checked_mul(8)
            .expect("SHA-256 bit length overflow");
        self.block[self.block_length] = 0x80;
        self.block_length += 1;

        if self.block_length > 56 {
            self.block[self.block_length..].fill(0);
            let block = self.block;
            compress_sha256(&mut self.state, &block);
            self.block = [0; 64];
            self.block_length = 0;
        }

        self.block[self.block_length..56].fill(0);
        self.block[56..].copy_from_slice(&bit_length.to_be_bytes());
        let block = self.block;
        compress_sha256(&mut self.state, &block);

        let mut output = [0_u8; 32];
        for (chunk, word) in output.chunks_exact_mut(4).zip(self.state) {
            chunk.copy_from_slice(&word.to_be_bytes());
        }
        output
    }
}

fn compress_sha256(state: &mut [u32; 8], block: &[u8; 64]) {
    const ROUND_CONSTANTS: [u32; 64] = [
        0x428a_2f98,
        0x7137_4491,
        0xb5c0_fbcf,
        0xe9b5_dba5,
        0x3956_c25b,
        0x59f1_11f1,
        0x923f_82a4,
        0xab1c_5ed5,
        0xd807_aa98,
        0x1283_5b01,
        0x2431_85be,
        0x550c_7dc3,
        0x72be_5d74,
        0x80de_b1fe,
        0x9bdc_06a7,
        0xc19b_f174,
        0xe49b_69c1,
        0xefbe_4786,
        0x0fc1_9dc6,
        0x240c_a1cc,
        0x2de9_2c6f,
        0x4a74_84aa,
        0x5cb0_a9dc,
        0x76f9_88da,
        0x983e_5152,
        0xa831_c66d,
        0xb003_27c8,
        0xbf59_7fc7,
        0xc6e0_0bf3,
        0xd5a7_9147,
        0x06ca_6351,
        0x1429_2967,
        0x27b7_0a85,
        0x2e1b_2138,
        0x4d2c_6dfc,
        0x5338_0d13,
        0x650a_7354,
        0x766a_0abb,
        0x81c2_c92e,
        0x9272_2c85,
        0xa2bf_e8a1,
        0xa81a_664b,
        0xc24b_8b70,
        0xc76c_51a3,
        0xd192_e819,
        0xd699_0624,
        0xf40e_3585,
        0x106a_a070,
        0x19a4_c116,
        0x1e37_6c08,
        0x2748_774c,
        0x34b0_bcb5,
        0x391c_0cb3,
        0x4ed8_aa4a,
        0x5b9c_ca4f,
        0x682e_6ff3,
        0x748f_82ee,
        0x78a5_636f,
        0x84c8_7814,
        0x8cc7_0208,
        0x90be_fffa,
        0xa450_6ceb,
        0xbef9_a3f7,
        0xc671_78f2,
    ];

    let mut schedule = [0_u32; 64];
    for (index, chunk) in block.chunks_exact(4).enumerate() {
        schedule[index] = u32::from_be_bytes(
            chunk
                .try_into()
                .expect("a four-byte SHA-256 schedule chunk"),
        );
    }
    for index in 16..64 {
        let sigma_zero = schedule[index - 15].rotate_right(7)
            ^ schedule[index - 15].rotate_right(18)
            ^ (schedule[index - 15] >> 3);
        let sigma_one = schedule[index - 2].rotate_right(17)
            ^ schedule[index - 2].rotate_right(19)
            ^ (schedule[index - 2] >> 10);
        schedule[index] = schedule[index - 16]
            .wrapping_add(sigma_zero)
            .wrapping_add(schedule[index - 7])
            .wrapping_add(sigma_one);
    }

    let [mut a, mut b, mut c, mut d, mut e, mut f, mut g, mut h] = *state;
    for index in 0..64 {
        let choice = (e & f) ^ ((!e) & g);
        let majority = (a & b) ^ (a & c) ^ (b & c);
        let big_sigma_zero = a.rotate_right(2) ^ a.rotate_right(13) ^ a.rotate_right(22);
        let big_sigma_one = e.rotate_right(6) ^ e.rotate_right(11) ^ e.rotate_right(25);
        let temporary_one = h
            .wrapping_add(big_sigma_one)
            .wrapping_add(choice)
            .wrapping_add(ROUND_CONSTANTS[index])
            .wrapping_add(schedule[index]);
        let temporary_two = big_sigma_zero.wrapping_add(majority);

        h = g;
        g = f;
        f = e;
        e = d.wrapping_add(temporary_one);
        d = c;
        c = b;
        b = a;
        a = temporary_one.wrapping_add(temporary_two);
    }

    state[0] = state[0].wrapping_add(a);
    state[1] = state[1].wrapping_add(b);
    state[2] = state[2].wrapping_add(c);
    state[3] = state[3].wrapping_add(d);
    state[4] = state[4].wrapping_add(e);
    state[5] = state[5].wrapping_add(f);
    state[6] = state[6].wrapping_add(g);
    state[7] = state[7].wrapping_add(h);
}

fn hex_digest(bytes: [u8; 32]) -> String {
    const HEX: &[u8; 16] = b"0123456789abcdef";
    let mut output = String::with_capacity(64);
    for byte in bytes {
        output.push(char::from(HEX[usize::from(byte >> 4)]));
        output.push(char::from(HEX[usize::from(byte & 0x0f)]));
    }
    output
}

#[cfg(test)]
mod tests {
    use super::{Sha256, hex_digest};

    #[test]
    fn sha256_matches_standard_empty_and_abc_vectors() {
        let empty = Sha256::new();
        assert_eq!(
            hex_digest(empty.finalize()),
            "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        );

        let mut abc = Sha256::new();
        abc.update(b"a");
        abc.update(b"bc");
        assert_eq!(
            hex_digest(abc.finalize()),
            "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
        );
    }

    #[test]
    fn sha256_matches_the_million_a_multiblock_vector() {
        let mut digest = Sha256::new();
        let chunk = [b'a'; 1_000];
        for _ in 0..1_000 {
            digest.update(&chunk);
        }
        assert_eq!(
            hex_digest(digest.finalize()),
            "cdc76e5c9914fb9281a1c7e284d73e67f1809a48a497200e046d39ccc7112cd0"
        );
    }
}
