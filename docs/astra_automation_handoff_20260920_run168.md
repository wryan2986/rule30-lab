# Astra automation handoff — run 168 — 2026-09-20

Problem 1 remains OPEN.

## New result

For every sufficiently late one-bit gate-u nonresetting source at even time `t`, run 167 gave

    s_t=s_(t+1)=t+1,
    s_(t+2) in {t+1,t+2}.

Run 168 resolves the remaining branch. The classified source cells are

    actual bits0..3 = (1,1,1,0),
    original-shadow bits0..3 = (0,1,1,0).

One Rule-30 step at physical position 1 gives

    r_1(t+1)=0,
    hat r_1(t+1)=1.

Thus the original global discrepancy front is at position 1 on row `t+1`. Since run 167 already forced `m(t+1)>=1`, this gives

    m(t+1)=1,
    J(t+1)=t+2,
    s_(t+2)=t+2.

Therefore the exact first two original-cut increments are

    (Delta_t,Delta_(t+1))=(0,1).

Interpretation: characteristic `t+1` is skipped, characteristic `t+2` has residence exactly one.

Proof file: `proofs/informal/problem1_run168_one_bit_shadow_forces_unit_second_residence.md`.

## Next target

Determine `s_(t+3)` / `Delta_(t+2)` by combining the fixed `(0,1)` prefix with the classified cyclic return at `t+2` and the SAME original global E shadow. Avoid identifying local cyclicization delays with global-front residence. If the next front position depends on wider shadow cells, isolate that dependence exactly rather than enumerating unrelated local cores.
