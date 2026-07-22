use std::env;
use std::hint::black_box;
use std::process::ExitCode;
use std::time::{Duration, Instant};

use rule30_core::{CenterEngine, CoordinateEngine, PackedEngine, stream_center_bits};

const FNV_OFFSET: u64 = 0xcbf2_9ce4_8422_2325;
const FNV_PRIME: u64 = 0x0000_0100_0000_01b3;

#[derive(Clone, Debug)]
struct Settings {
    bits: usize,
    repetitions: usize,
}

fn usage(program: &str) {
    eprintln!("usage: {program} [--bits N] [--repetitions N]");
}

fn parse_positive(name: &str, value: Option<String>) -> Result<usize, String> {
    let text = value.ok_or_else(|| format!("missing value for {name}"))?;
    let parsed = text
        .parse::<usize>()
        .map_err(|error| format!("invalid value for {name}: {error}"))?;
    if parsed == 0 {
        return Err(format!("{name} must be positive"));
    }
    Ok(parsed)
}

fn settings() -> Result<Settings, String> {
    let mut result = Settings {
        bits: 5_000,
        repetitions: 3,
    };
    let mut arguments = env::args().skip(1);
    while let Some(argument) = arguments.next() {
        match argument.as_str() {
            "--bits" => result.bits = parse_positive("--bits", arguments.next())?,
            "--repetitions" => {
                result.repetitions = parse_positive("--repetitions", arguments.next())?;
            }
            _ => return Err(format!("unknown argument: {argument}")),
        }
    }
    Ok(result)
}

fn generate_once<E>(bits: usize) -> (usize, i128, u64)
where
    E: CenterEngine + Default,
{
    let mut digest = FNV_OFFSET;
    let report = stream_center_bits(E::default(), bits, &[bits], |bit| {
        digest ^= u64::from(bit);
        digest = digest.wrapping_mul(FNV_PRIME);
    })
    .expect("the final checkpoint equals the requested output size");
    black_box((report.ones, report.discrepancy, digest))
}

fn duration_seconds(duration: Duration) -> f64 {
    duration.as_secs_f64()
}

fn benchmark<E>(engine: &str, settings: &Settings)
where
    E: CenterEngine + Default,
{
    let warmup = generate_once::<E>(settings.bits);
    black_box(warmup);

    let mut samples = Vec::with_capacity(settings.repetitions);
    let mut verified_result = None;
    for _ in 0..settings.repetitions {
        let start = Instant::now();
        let result = generate_once::<E>(settings.bits);
        samples.push(start.elapsed());
        if let Some(previous) = verified_result {
            assert_eq!(result, previous, "nondeterministic benchmark result");
        } else {
            verified_result = Some(result);
        }
    }

    samples.sort_unstable();
    let seconds = samples
        .iter()
        .copied()
        .map(duration_seconds)
        .collect::<Vec<_>>();
    let minimum = seconds[0];
    let maximum = seconds[seconds.len() - 1];
    let median = if seconds.len() % 2 == 0 {
        (seconds[seconds.len() / 2 - 1] + seconds[seconds.len() / 2]) / 2.0
    } else {
        seconds[seconds.len() / 2]
    };
    let mean = seconds.iter().sum::<f64>() / seconds.len() as f64;
    let variance = seconds
        .iter()
        .map(|sample| (sample - mean).powi(2))
        .sum::<f64>()
        / seconds.len() as f64;
    let (ones, discrepancy, digest) = verified_result.expect("at least one repetition");
    let samples_json = seconds
        .iter()
        .map(|sample| format!("{sample:.9}"))
        .collect::<Vec<_>>()
        .join(",");

    println!(
        concat!(
            "{{\"engine\":\"{}\",",
            "\"operation\":\"generate_center_stream_with_statistics\",",
            "\"bits\":{},\"stores_output\":false,\"warmups\":1,",
            "\"repetitions\":{},\"samples_seconds\":[{}],",
            "\"minimum_seconds\":{:.9},\"median_seconds\":{:.9},",
            "\"maximum_seconds\":{:.9},\"mean_seconds\":{:.9},",
            "\"stddev_seconds\":{:.9},\"ones\":{},",
            "\"discrepancy\":{},\"fnv1a64\":\"{:016x}\"}}"
        ),
        engine,
        settings.bits,
        settings.repetitions,
        samples_json,
        minimum,
        median,
        maximum,
        mean,
        variance.sqrt(),
        ones,
        discrepancy,
        digest
    );
}

fn main() -> ExitCode {
    let program = env::args()
        .next()
        .unwrap_or_else(|| "rule30-rust-bench".to_owned());
    let settings = match settings() {
        Ok(value) => value,
        Err(error) => {
            eprintln!("error: {error}");
            usage(&program);
            return ExitCode::from(2);
        }
    };

    benchmark::<CoordinateEngine>("coordinate-reference", &settings);
    benchmark::<PackedEngine>("packed-u64", &settings);
    ExitCode::SUCCESS
}
