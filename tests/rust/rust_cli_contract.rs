use std::fs;
use std::fs::OpenOptions;
use std::path::PathBuf;
use std::process::{Command, Output, Stdio};

const SHARED_SHA256: &str = "61de1c97dc3f80cb24d3a02207920bd442d6f530304497eee70189a039a47860";
const EMPTY_SHA256: &str = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855";

fn binary() -> &'static str {
    env!("CARGO_BIN_EXE_rule30-rust")
}

fn shared_vector() -> Vec<u8> {
    let path = PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .join("../../../tests/reference_vectors/center_c00000000_c00009999.u8");
    let bits = fs::read(&path)
        .unwrap_or_else(|error| panic!("failed to read {}: {error}", path.display()));
    assert_eq!(bits.len(), 10_000);
    bits
}

fn run(arguments: &[&str]) -> Output {
    Command::new(binary())
        .args(arguments)
        .output()
        .unwrap_or_else(|error| panic!("failed to execute rule30-rust: {error}"))
}

fn assert_success(output: &Output) {
    assert!(
        output.status.success(),
        "status={:?}, stderr={}",
        output.status.code(),
        String::from_utf8_lossy(&output.stderr)
    );
    assert!(output.stderr.is_empty());
}

#[test]
fn raw_contract_covers_zero_one_and_word_boundaries() {
    let expected = shared_vector();
    for count in [0, 1, 64, 65, 127, 128, 129] {
        for backend in ["coordinate", "packed"] {
            let count_text = count.to_string();
            let output = run(&[
                "generate",
                "--count",
                &count_text,
                "--backend",
                backend,
                "--format",
                "raw",
            ]);
            assert_success(&output);
            assert_eq!(
                output.stdout,
                expected[..count],
                "backend={backend}, count={count}"
            );
            assert!(output.stdout.iter().all(|&bit| bit <= 1));
        }
    }
}

#[test]
fn both_raw_backends_match_the_shared_ten_thousand_vector() {
    let expected = shared_vector();
    for backend in ["coordinate", "packed"] {
        let output = run(&[
            "generate",
            "--count",
            "10000",
            "--backend",
            backend,
            "--format",
            "raw",
        ]);
        assert_success(&output);
        assert_eq!(output.stdout, expected, "backend={backend}");
    }
}

#[test]
fn json_contract_reports_counts_backend_and_sha256() {
    for backend in ["coordinate", "packed"] {
        let output = run(&[
            "generate",
            "--count",
            "10000",
            "--backend",
            backend,
            "--format",
            "json",
        ]);
        assert_success(&output);
        let expected = format!(
            concat!(
                "{{\"backend\":\"{}\",",
                "\"bit_order\":\"c_0_to_c_n_minus_1\",",
                "\"count\":10000,\"discrepancy\":64,\"ones\":5032,",
                "\"sha256_u8\":\"{}\",\"zeros\":4968}}\n"
            ),
            backend, SHARED_SHA256
        );
        assert_eq!(output.stdout, expected.as_bytes());
    }
}

#[test]
fn empty_json_contract_has_exact_empty_digest() {
    let output = run(&[
        "generate",
        "--count",
        "0",
        "--backend",
        "packed",
        "--format",
        "json",
    ]);
    assert_success(&output);
    let expected = format!(
        concat!(
            "{{\"backend\":\"packed\",",
            "\"bit_order\":\"c_0_to_c_n_minus_1\",",
            "\"count\":0,\"discrepancy\":0,\"ones\":0,",
            "\"sha256_u8\":\"{}\",\"zeros\":0}}\n"
        ),
        EMPTY_SHA256
    );
    assert_eq!(output.stdout, expected.as_bytes());
}

#[test]
fn invalid_missing_duplicate_and_huge_arguments_are_rejected() {
    let cases: &[(&[&str], &str)] = &[
        (
            &[
                "generate",
                "--count",
                "-1",
                "--backend",
                "packed",
                "--format",
                "raw",
            ],
            "nonnegative decimal integer",
        ),
        (
            &[
                "generate",
                "--count",
                "9999999999999999999999999999999999999999",
                "--backend",
                "packed",
                "--format",
                "raw",
            ],
            "--count is too large",
        ),
        (
            &[
                "generate",
                "--count",
                "250001",
                "--backend",
                "coordinate",
                "--format",
                "json",
            ],
            "coordinate backend safety limit 250000",
        ),
        (
            &[
                "generate",
                "--count",
                "1",
                "--count",
                "1",
                "--backend",
                "packed",
                "--format",
                "raw",
            ],
            "--count may only be specified once",
        ),
        (
            &["generate", "--count", "1", "--format", "raw"],
            "--backend is required",
        ),
        (
            &[
                "generate",
                "--count",
                "1",
                "--backend",
                "unknown",
                "--format",
                "raw",
            ],
            "--backend must be coordinate or packed",
        ),
    ];

    for &(arguments, expected_error) in cases {
        let output = run(arguments);
        assert_eq!(output.status.code(), Some(2), "arguments={arguments:?}");
        assert!(output.stdout.is_empty());
        let stderr = String::from_utf8_lossy(&output.stderr);
        assert!(
            stderr.contains(expected_error),
            "arguments={arguments:?}, stderr={stderr}"
        );
    }
}

#[cfg(unix)]
#[test]
fn raw_write_errors_are_reported() {
    let full = match OpenOptions::new().write(true).open("/dev/full") {
        Ok(file) => file,
        Err(error) if error.kind() == std::io::ErrorKind::NotFound => return,
        Err(error) => panic!("failed to open /dev/full: {error}"),
    };
    let output = Command::new(binary())
        .args([
            "generate",
            "--count",
            "1",
            "--backend",
            "packed",
            "--format",
            "raw",
        ])
        .stdout(Stdio::from(full))
        .output()
        .expect("failed to execute rule30-rust");
    assert_eq!(output.status.code(), Some(1));
    let stderr = String::from_utf8_lossy(&output.stderr);
    assert!(
        stderr.contains("failed to write raw output")
            || stderr.contains("failed to flush raw output"),
        "stderr={stderr}"
    );
}

#[cfg(unix)]
#[test]
fn broken_pipe_is_reported_without_a_panic() {
    let mut child = Command::new(binary())
        .args([
            "generate",
            "--count",
            "65536",
            "--backend",
            "packed",
            "--format",
            "raw",
        ])
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .spawn()
        .expect("failed to execute rule30-rust");
    drop(child.stdout.take());
    let output = child.wait_with_output().expect("failed to wait for CLI");
    assert_eq!(output.status.code(), Some(1));
    let stderr = String::from_utf8_lossy(&output.stderr);
    assert!(
        stderr.contains("failed to write raw output"),
        "stderr={stderr}"
    );
    assert!(!stderr.contains("panicked"), "stderr={stderr}");
}
