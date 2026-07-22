use std::fs;
use std::path::PathBuf;

use rule30_core::{
    CenterEngine, CoordinateEngine, PackedEngine, center_bits_packed, center_bits_reference,
    stream_center_bits,
};

fn shared_vector_path() -> PathBuf {
    PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .join("../../../tests/reference_vectors/center_c00000000_c00009999.u8")
}

fn shared_vector() -> Vec<u8> {
    let path = shared_vector_path();
    let bits = fs::read(&path)
        .unwrap_or_else(|error| panic!("failed to read shared vector {}: {error}", path.display()));
    assert_eq!(bits.len(), 10_000);
    assert!(bits.iter().all(|&bit| bit <= 1));
    bits
}

fn shared_rows_path() -> PathBuf {
    PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .join("../../../tests/reference_vectors/rows_t0000_t0255.txt")
}

#[test]
fn both_engines_match_all_ten_thousand_shared_bits() {
    let expected = shared_vector();
    assert_eq!(center_bits_reference(expected.len()), expected);
    assert_eq!(center_bits_packed(expected.len()), expected);
}

#[test]
fn both_engines_match_all_two_hundred_fifty_six_shared_rows() {
    let path = shared_rows_path();
    let text = fs::read_to_string(&path)
        .unwrap_or_else(|error| panic!("failed to read shared rows {}: {error}", path.display()));
    let mut coordinate = CoordinateEngine::new();
    let mut packed = PackedEngine::new();

    for (generation, line) in text.lines().enumerate() {
        let (label, row_text) = line
            .split_once('\t')
            .unwrap_or_else(|| panic!("malformed shared row at generation {generation}"));
        assert_eq!(label, format!("{generation:04}"));
        let expected = row_text
            .bytes()
            .map(|value| match value {
                b'0' => 0,
                b'1' => 1,
                _ => panic!("non-binary shared row at generation {generation}"),
            })
            .collect::<Vec<_>>();
        assert_eq!(
            coordinate.row_left_to_right(),
            expected,
            "coordinate t={generation}"
        );
        assert_eq!(
            packed.row_left_to_right(),
            expected,
            "packed t={generation}"
        );
        if generation < 255 {
            coordinate.advance();
            packed.advance();
        }
    }
    assert_eq!(text.lines().count(), 256);
}

#[test]
fn boundary_sized_outputs_match_shared_prefixes() {
    let expected = shared_vector();
    for count in [0, 1, 64, 65, 127, 128, 129] {
        assert_eq!(center_bits_reference(count), expected[..count]);
        assert_eq!(center_bits_packed(count), expected[..count]);
    }
}

#[test]
fn streaming_engines_match_vectors_and_checkpoint_counts() {
    let expected = shared_vector();
    let checkpoints = [0, 1, 64, 65, 127, 128, 129, 1_000, 10_000];

    for (name, output, report) in [
        {
            let mut output = Vec::with_capacity(expected.len());
            let report = stream_center_bits(
                CoordinateEngine::new(),
                expected.len(),
                &checkpoints,
                |bit| output.push(bit),
            )
            .unwrap();
            ("coordinate", output, report)
        },
        {
            let mut output = Vec::with_capacity(expected.len());
            let report =
                stream_center_bits(PackedEngine::new(), expected.len(), &checkpoints, |bit| {
                    output.push(bit)
                })
                .unwrap();
            ("packed", output, report)
        },
    ] {
        assert_eq!(output, expected, "engine={name}");
        assert_eq!(report.count, expected.len(), "engine={name}");
        assert_eq!(
            report.ones,
            expected.iter().map(|&bit| usize::from(bit)).sum()
        );
        assert_eq!(report.zeros, expected.len() - report.ones);

        for checkpoint in report.checkpoints {
            let ones = expected[..checkpoint.n]
                .iter()
                .map(|&bit| usize::from(bit))
                .sum::<usize>();
            assert_eq!(checkpoint.ones, ones, "engine={name}, n={}", checkpoint.n);
            assert_eq!(checkpoint.zeros, checkpoint.n - ones);
            assert_eq!(
                checkpoint.discrepancy,
                2 * ones as i128 - checkpoint.n as i128
            );
        }
    }
}
