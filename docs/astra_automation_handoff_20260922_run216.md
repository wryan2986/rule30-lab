# Astra automation handoff — run 216

Problem 1 remains OPEN.

## Repository state entering run

No intervening work after run 215; branch tip was `6ec9611f017eaf2bc858e190ff1792d432ac2e6f`.

## New exact result

Run 215 gives

    d_j(k+1)=d_{j-2}(k) XOR (d_{j-1}(k) OR d_j(k)).

The reset driver for the level-j lift is exactly

    bit_0(y_{j-1}(k))=d_{j-1}(k).

Applying the recurrence to that driver, whenever `d_{j-1}(k)=0`,

    d_{j-1}(k+1)=d_{j-3}(k) XOR d_{j-2}(k).

Hence a reset-free zero run in layer `j-1` continues exactly while the adjacent lower layers `d_{j-3}` and `d_{j-2}` agree, and it terminates exactly at their first disagreement (up to the one-step reset-transition indexing convention).

Thus every large positive preperiod increment/reset gap at level j forces a long synchronization interval

    d_{j-3}=d_{j-2}

starting at the relevant lower-level cycle-entry window. The gain endpoint is their first disagreement.

Full note:

`proofs/informal/problem1_run216_reset_gap_equals_lower_defect_agreement.md`

## Why this matters

This is the first direct local cross-level constraint on the reset gaps themselves. Run 210 represented gains as low-bit zero runs; run 216 eliminates that proxy and identifies a long gain with a long agreement run of two lower defect layers.

It does not yet bound those agreement runs or prove non-reuse.

## Next target

Analyze

    g_j(k)=d_{j-2}(k) XOR d_{j-3}(k).

Derive an exact recurrence or causal ancestry law for `g_j`, specifically along the stopping-time windows beginning at `a_{j-1}`. The desired theorem is that repeated long zero runs of `g_j` across increasing j require fresh/non-reusable boundary ancestry, or otherwise have an amortized bound. Do not assume adjacent-layer agreement is automatically short.