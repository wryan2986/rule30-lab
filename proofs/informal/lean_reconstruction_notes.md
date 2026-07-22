# Lean reconstruction notes

Status: rigorous proof within Lean's kernel, for the finite and local statements
listed below. No global Rule 30 nonperiodicity theorem is imported or claimed.

## Synchronized definitions

All definitions are in `proofs/lean/Rule30.lean`, namespace `Rule30`.

- `localUpdate left center right = left.xor (center || right)` is the Rule 30
  local map used by the computational implementations.
- `sidewaysStep center next right = next.xor (center || right)` is its
  left-permutive inverse.
- `Column = Nat → Bool` and `Spacetime = Int → Nat → Bool`.
- `LeftwardStrip = Nat → Nat → Bool` uses a reconstruction-oriented
  spatial index: strip index `0` is the supplied right column, index `1` is
  the center column, and increasing indices move leftward.
- `EvolvesByRule30 x` states the Rule 30 local equation at every integer
  position and natural-numbered time.
- `EvolvesLeftwardByRule30 x` states the identical local map in strip
  coordinates: at offset `d`, the right, current, and left columns have
  indices `d`, `d + 1`, and `d + 2`, respectively.
- `sidewaysColumn current right` applies `sidewaysStep` pointwise, using
  `current (time + 1)` as the supplied next value.
- `reconstructionPair center right depth` recursively stores the adjacent
  pair `(right, current)` after `depth` leftward reconstruction steps.
- `reconstructLeft center right depth` projects the reconstructed current
  column.

## Checked theorem statements

The original local theorems remain synchronized with the Boolean definition:

- `localUpdate_111` through `localUpdate_000`: all eight truth-table rows.
- `leftPermutiveInversion`: the original left value equals the sideways
  inverse of a genuine update.
- `sidewaysStep_recovers_left`: a sideways step recovers the genuine left
  input.
- `localUpdate_sidewaysStep`: applying Rule 30 to a reconstructed left input
  recovers the supplied next value.
- `true_center_true_next_forces_left_false`: if a local update has center
  `true` and next value `true`, then the left input is `false`.

The new column and finite-region theorems are:

- `sidewaysColumn_of_evolution`: for any genuine Rule 30 spacetime, one
  sideways column step from positions `j` and `j + 1` exactly recovers
  position `j - 1`.
- `reconstructionPair_bounded_correct`: suppose supplied center and right
  columns agree with strip indices `1` and `0` of a genuine right-to-left
  Rule 30 strip through a finite `horizon`. At any natural `time` and
  reconstruction `depth` with `time + depth ≤ horizon`, the reconstructed
  current column equals strip index `depth + 1`, and its stored right neighbor
  equals strip index `depth`.
- `reconstructLeft_bounded_correct`: the current-column projection of that
  bounded triangular-region theorem.
- `consecutive_true_values_force_adjacent_left_false`: if a genuine column is
  `true` at times `t` and `t + 1`, its adjacent-left cell at time `t` is
  `false`.
- `true_closed_interval_forces_left_false_on_halfOpen_interval`: if a genuine
  column is `true` throughout the closed natural-number interval
  `[start, start + length]`, then the adjacent-left column is `false`
  throughout `[start, start + length)`.
- `true_tail_forces_adjacent_left_false_tail`: if a genuine column is `true`
  at every time from `start` onward, its adjacent-left column is `false` at
  every time from that same `start` onward. The theorem is purely local and
  does not import the separate width-two nonperiodicity result needed for a
  contradiction.
- `false_left_true_center_stays_true_locally`: with a `false` left input, a
  `true` center remains `true` independently of the right input.
- `false_left_tail_true_right_persists`: for explicitly adjacent positions, if
  the left column is `false` from `start` onward and the right column is `true`
  at a later time, that right column remains `true` at every subsequent
  offset. This is the stable local core of the eventual-zero-center argument.

The interval endpoints are intentional: each forced-left conclusion at time
`t` requires both center values at `t` and `t + 1`.

## Verification

From `proofs/lean`:

```bash
env \
  ELAN_HOME=/home/wryan/rule30-lab/.toolchains/elan \
  PATH=/home/wryan/rule30-lab/.toolchains/elan/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin \
  lake build
```

This was checked with Lean 4.30.0. The source contains no `sorry`,
user-declared axioms, or unsound placeholders. Lean's `#print axioms` reports
that each of the eight tail/reconstruction theorems listed above depends on no
axioms.

## Scope and limitations

- These results prove local identities and finite reconstruction correctness;
  they do not prove that the center column is nonperiodic.
- The bounded reconstruction theorem assumes supplied boundary columns agree
  with an already genuine right-to-left Rule 30 strip through the stated
  horizon. It is a correctness theorem, not by itself a compatibility or
  existence theorem for arbitrary proposed traces.
- The theorem models columns as total functions and expresses finiteness by a
  horizon bound. It does not define a serialized finite-vector format or prove
  correspondence to the Python, C++, Rust, or CUDA memory layouts.
- The finite true-interval theorem does not import the literature theorem
  about width-two traces and does not derive an infinite-tail or global
  nonperiodicity conclusion.
- The infinite-tail implication likewise does not prove that the hypothesized
  true tail is impossible without the separately cited width-two theorem.
- The formal false-tail result proves persistence after a right-neighbor one;
  the classical dichotomy “a one occurs or the column stays zero” and Kopra's
  external width-two theorem remain in the synchronized informal proof.
