//! Independent, safe Rust implementations of Rule 30.
//!
//! Both engines emit exactly `count` center bits, beginning with `c_0`.
//! [`CoordinateEngine`] keeps an explicit cell for every coordinate in the
//! active row. [`PackedEngine`] stores the same row in packed `u64` words and
//! advances it with carry-aware shifts.

#![forbid(unsafe_code)]

use std::error::Error;
use std::fmt;

/// The Rule 30 local map, with arguments ordered from left to right.
#[must_use]
pub const fn local_update(left: u8, center: u8, right: u8) -> u8 {
    left ^ (center | right)
}

/// Common interface used by center-column generators.
pub trait CenterEngine {
    /// The time index of the currently represented row.
    fn generation(&self) -> usize;

    /// Return the center bit of the currently represented row.
    fn center_bit(&self) -> u8;

    /// Advance by one Rule 30 time step.
    fn advance(&mut self);
}

/// A direct implementation with one byte per active coordinate.
///
/// The row is stored from the leftmost active coordinate to the rightmost.
/// This deliberately favors transparency and independence over speed.
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct CoordinateEngine {
    generation: usize,
    row: Vec<u8>,
    scratch: Vec<u8>,
}

impl CoordinateEngine {
    /// Construct the single-black-cell initial state.
    #[must_use]
    pub fn new() -> Self {
        Self {
            generation: 0,
            row: vec![1],
            scratch: Vec::new(),
        }
    }

    /// Return the complete active row, ordered from left to right.
    #[must_use]
    pub fn row_left_to_right(&self) -> &[u8] {
        &self.row
    }
}

impl Default for CoordinateEngine {
    fn default() -> Self {
        Self::new()
    }
}

impl CenterEngine for CoordinateEngine {
    fn generation(&self) -> usize {
        self.generation
    }

    fn center_bit(&self) -> u8 {
        self.row[self.generation]
    }

    fn advance(&mut self) {
        let old_len = self.row.len();
        let new_len = old_len
            .checked_add(2)
            .expect("Rule 30 coordinate row length overflow");

        self.scratch.clear();
        self.scratch.resize(new_len, 0);

        // New index i represents the coordinate whose old-row index is i-1.
        // Thus its left, center, and right inputs have old indices i-2, i-1,
        // and i, respectively. Out-of-range cells are the quiescent zero tail.
        for i in 0..new_len {
            let left = i
                .checked_sub(2)
                .and_then(|index| self.row.get(index))
                .copied()
                .unwrap_or(0);
            let center = i
                .checked_sub(1)
                .and_then(|index| self.row.get(index))
                .copied()
                .unwrap_or(0);
            let right = self.row.get(i).copied().unwrap_or(0);
            self.scratch[i] = local_update(left, center, right);
        }

        std::mem::swap(&mut self.row, &mut self.scratch);
        self.generation = self
            .generation
            .checked_add(1)
            .expect("Rule 30 generation counter overflow");
    }
}

/// A packed-`u64` Rule 30 engine.
///
/// Packed bit zero is the rightmost active cell. At generation `t`, the center
/// is packed bit `t`, and the active row occupies exactly `2*t + 1` bits. The
/// update is the arbitrary-width identity
///
/// `next = row XOR ((row << 1) OR (row << 2))`.
///
/// Shifts are performed word by word; carries from the preceding word are
/// handled explicitly and unused bits in the final word are always cleared.
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct PackedEngine {
    generation: usize,
    active_bits: usize,
    words: Vec<u64>,
    scratch: Vec<u64>,
}

impl PackedEngine {
    /// Construct the single-black-cell initial state.
    #[must_use]
    pub fn new() -> Self {
        Self {
            generation: 0,
            active_bits: 1,
            words: vec![1],
            scratch: Vec::new(),
        }
    }

    /// Number of meaningful bits in the packed row.
    #[must_use]
    pub const fn active_bits(&self) -> usize {
        self.active_bits
    }

    /// Read-only access to the packed words, least-significant word first.
    #[must_use]
    pub fn packed_words(&self) -> &[u64] {
        &self.words
    }

    /// Materialize the active row from its leftmost cell to its rightmost.
    #[must_use]
    pub fn row_left_to_right(&self) -> Vec<u8> {
        (0..self.active_bits)
            .rev()
            .map(|index| self.packed_bit(index))
            .collect()
    }

    fn packed_bit(&self, index: usize) -> u8 {
        let word = self.words[index / 64];
        ((word >> (index % 64)) & 1) as u8
    }

    fn final_word_mask(active_bits: usize) -> u64 {
        let remainder = active_bits % 64;
        if remainder == 0 {
            u64::MAX
        } else {
            u64::MAX >> (64 - remainder)
        }
    }
}

impl Default for PackedEngine {
    fn default() -> Self {
        Self::new()
    }
}

impl CenterEngine for PackedEngine {
    fn generation(&self) -> usize {
        self.generation
    }

    fn center_bit(&self) -> u8 {
        self.packed_bit(self.generation)
    }

    fn advance(&mut self) {
        let new_active_bits = self
            .active_bits
            .checked_add(2)
            .expect("Rule 30 packed row length overflow");
        let new_word_count = new_active_bits
            .checked_add(63)
            .expect("Rule 30 packed word-count overflow")
            / 64;

        self.scratch.clear();
        self.scratch.resize(new_word_count, 0);

        for word_index in 0..new_word_count {
            let current = self.words.get(word_index).copied().unwrap_or(0);
            let previous = word_index
                .checked_sub(1)
                .and_then(|index| self.words.get(index))
                .copied()
                .unwrap_or(0);

            let shifted_one = (current << 1) | (previous >> 63);
            let shifted_two = (current << 2) | (previous >> 62);
            self.scratch[word_index] = current ^ (shifted_one | shifted_two);
        }

        let final_index = new_word_count - 1;
        self.scratch[final_index] &= Self::final_word_mask(new_active_bits);

        std::mem::swap(&mut self.words, &mut self.scratch);
        self.active_bits = new_active_bits;
        self.generation = self
            .generation
            .checked_add(1)
            .expect("Rule 30 generation counter overflow");
    }
}

/// Prefix statistics captured after exactly `n` emitted center bits.
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct CheckpointStats {
    pub n: usize,
    pub ones: usize,
    pub zeros: usize,
    pub discrepancy: i128,
}

/// Statistics from a complete streaming generation call.
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct StreamReport {
    pub count: usize,
    pub ones: usize,
    pub zeros: usize,
    pub discrepancy: i128,
    pub checkpoints: Vec<CheckpointStats>,
}

/// Error returned when a requested checkpoint is outside the generated prefix.
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct CheckpointOutOfRange {
    pub checkpoint: usize,
    pub count: usize,
}

impl fmt::Display for CheckpointOutOfRange {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(
            formatter,
            "checkpoint {} exceeds generated center-bit count {}",
            self.checkpoint, self.count
        )
    }
}

impl Error for CheckpointOutOfRange {}

fn checkpoint_stats(n: usize, ones: usize) -> CheckpointStats {
    CheckpointStats {
        n,
        ones,
        zeros: n - ones,
        discrepancy: 2 * (ones as i128) - (n as i128),
    }
}

/// Stream exactly `count` center bits through `emit` and return statistics.
///
/// Checkpoints are prefix lengths. They may be unsorted or repeated; returned
/// checkpoints are sorted and deduplicated. Checkpoint zero is supported.
/// A checkpoint greater than `count` is rejected rather than silently omitted.
pub fn stream_center_bits<E, F>(
    mut engine: E,
    count: usize,
    checkpoints: &[usize],
    mut emit: F,
) -> Result<StreamReport, CheckpointOutOfRange>
where
    E: CenterEngine,
    F: FnMut(u8),
{
    if let Some(&checkpoint) = checkpoints.iter().find(|&&value| value > count) {
        return Err(CheckpointOutOfRange { checkpoint, count });
    }

    let mut requested = checkpoints.to_vec();
    requested.sort_unstable();
    requested.dedup();

    let mut reports = Vec::with_capacity(requested.len());
    let mut checkpoint_index = 0;
    let mut ones = 0;

    if requested.first() == Some(&0) {
        reports.push(checkpoint_stats(0, 0));
        checkpoint_index = 1;
    }

    for emitted in 1..=count {
        let bit = engine.center_bit();
        debug_assert!(bit <= 1);
        emit(bit);
        ones += usize::from(bit);

        if checkpoint_index < requested.len() && requested[checkpoint_index] == emitted {
            reports.push(checkpoint_stats(emitted, ones));
            checkpoint_index += 1;
        }

        if emitted < count {
            engine.advance();
        }
    }

    Ok(StreamReport {
        count,
        ones,
        zeros: count - ones,
        discrepancy: 2 * (ones as i128) - (count as i128),
        checkpoints: reports,
    })
}

/// Generate exactly `count` center bits with the coordinate implementation.
#[must_use]
pub fn center_bits_reference(count: usize) -> Vec<u8> {
    let mut bits = Vec::with_capacity(count);
    stream_center_bits(CoordinateEngine::new(), count, &[], |bit| bits.push(bit))
        .expect("an empty checkpoint list is always valid");
    bits
}

/// Generate exactly `count` center bits with the packed-`u64` implementation.
#[must_use]
pub fn center_bits_packed(count: usize) -> Vec<u8> {
    let mut bits = Vec::with_capacity(count);
    stream_center_bits(PackedEngine::new(), count, &[], |bit| bits.push(bit))
        .expect("an empty checkpoint list is always valid");
    bits
}

#[cfg(test)]
mod tests {
    use super::{
        CenterEngine, CoordinateEngine, PackedEngine, center_bits_packed, center_bits_reference,
        local_update, stream_center_bits,
    };

    const HAND_ROWS: &[&[u8]] = &[&[1], &[1, 1, 1], &[1, 1, 0, 0, 1], &[1, 1, 0, 1, 1, 1, 1]];

    #[test]
    fn local_rule_matches_rule_30_truth_table() {
        let expected = [0, 1, 1, 1, 1, 0, 0, 0];
        for neighborhood in 0_u8..8 {
            let left = (neighborhood >> 2) & 1;
            let center = (neighborhood >> 1) & 1;
            let right = neighborhood & 1;
            assert_eq!(
                local_update(left, center, right),
                expected[usize::from(neighborhood)]
            );
        }
    }

    #[test]
    fn coordinate_engine_matches_hand_rows() {
        let mut engine = CoordinateEngine::new();
        for (generation, expected) in HAND_ROWS.iter().enumerate() {
            assert_eq!(engine.generation(), generation);
            assert_eq!(engine.row_left_to_right(), *expected);
            assert_eq!(engine.center_bit(), expected[generation]);
            if generation + 1 < HAND_ROWS.len() {
                engine.advance();
            }
        }
    }

    #[test]
    fn packed_engine_matches_hand_rows() {
        let mut engine = PackedEngine::new();
        for (generation, expected) in HAND_ROWS.iter().enumerate() {
            assert_eq!(engine.generation(), generation);
            assert_eq!(engine.active_bits(), 2 * generation + 1);
            assert_eq!(engine.row_left_to_right(), *expected);
            assert_eq!(engine.center_bit(), expected[generation]);
            if generation + 1 < HAND_ROWS.len() {
                engine.advance();
            }
        }
    }

    #[test]
    fn complete_rows_match_across_multiple_words() {
        let mut coordinate = CoordinateEngine::new();
        let mut packed = PackedEngine::new();
        for generation in 0..=130 {
            assert_eq!(
                packed.row_left_to_right(),
                coordinate.row_left_to_right(),
                "generation={generation}"
            );
            if generation < 130 {
                coordinate.advance();
                packed.advance();
            }
        }
    }

    #[test]
    fn packed_final_word_is_masked_across_boundaries() {
        let mut engine = PackedEngine::new();
        for generation in 0..=130 {
            let active_bits = 2 * generation + 1;
            assert_eq!(engine.active_bits(), active_bits);
            assert_eq!(engine.packed_words().len(), active_bits.div_ceil(64));

            let remainder = active_bits % 64;
            if remainder != 0 {
                let unused_mask = u64::MAX << remainder;
                assert_eq!(
                    engine.packed_words().last().copied().unwrap() & unused_mask,
                    0
                );
            }
            if generation < 130 {
                engine.advance();
            }
        }
    }

    #[test]
    fn exact_output_counts_and_word_boundaries_match() {
        for count in [0, 1, 2, 3, 63, 64, 65, 66, 127, 128, 129] {
            let reference = center_bits_reference(count);
            let packed = center_bits_packed(count);
            assert_eq!(reference.len(), count);
            assert_eq!(packed.len(), count);
            assert_eq!(packed, reference, "count={count}");
        }
    }

    #[test]
    fn streaming_statistics_are_deterministic_and_exact() {
        let mut emitted = Vec::new();
        let report =
            stream_center_bits(PackedEngine::new(), 129, &[129, 0, 65, 64, 65, 1], |bit| {
                emitted.push(bit)
            })
            .unwrap();

        assert_eq!(emitted, center_bits_reference(129));
        assert_eq!(report.count, 129);
        assert_eq!(report.ones + report.zeros, 129);
        assert_eq!(report.discrepancy, 2 * report.ones as i128 - 129);
        assert_eq!(
            report
                .checkpoints
                .iter()
                .map(|checkpoint| checkpoint.n)
                .collect::<Vec<_>>(),
            [0, 1, 64, 65, 129]
        );
        for checkpoint in report.checkpoints {
            let ones = emitted[..checkpoint.n]
                .iter()
                .map(|&bit| usize::from(bit))
                .sum::<usize>();
            assert_eq!(checkpoint.ones, ones);
            assert_eq!(checkpoint.zeros, checkpoint.n - ones);
            assert_eq!(
                checkpoint.discrepancy,
                2 * ones as i128 - checkpoint.n as i128
            );
        }
    }

    #[test]
    fn invalid_checkpoint_is_rejected_before_emission() {
        let mut calls = 0;
        let error = stream_center_bits(PackedEngine::new(), 64, &[65], |_| calls += 1).unwrap_err();
        assert_eq!(calls, 0);
        assert_eq!(error.checkpoint, 65);
        assert_eq!(error.count, 64);
    }

    #[test]
    fn zero_bits_do_not_advance_or_emit() {
        let mut calls = 0;
        let report = stream_center_bits(CoordinateEngine::new(), 0, &[0], |_| calls += 1).unwrap();
        assert_eq!(calls, 0);
        assert_eq!(report.count, 0);
        assert_eq!(report.ones, 0);
        assert_eq!(report.zeros, 0);
        assert_eq!(report.discrepancy, 0);
        assert_eq!(report.checkpoints[0].n, 0);
    }
}
