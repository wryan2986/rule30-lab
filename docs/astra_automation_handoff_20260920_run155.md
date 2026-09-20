# Astra automation handoff — 2026-09-20 run155

Problem 1 remains OPEN.

## New result

Run154 reduced terminal hidden slack to `g_(t+5) in {0,1,2}` and left `g=2` as the next target. The complete global-front residence trace for `g=2`, based at the distinguished cyclic source `q=t+2` with motif

    (r_-5,...,r_2)(q)=10101110,

is

    r_2(q+1)=0,
    r_1(q+2)=0,
    r_0(q+3)=0,
    r_-1(q+4)=1 (final eraser).

Writing `a=r_3(q)`, exact Rule30 evolution gives

    r_2(q+1)=NOT a,
    r_1(q+2)=NOT a,
    r_0(q+3)=0,
    r_-1(q+4)=1.

Thus the ENTIRE `g=2` residence certificate collapses to the single condition `a=1`. It is independent of `b=r_4(q)` and all farther right fringe bits. For `g=1`, the residence likewise forces only `a=1`; for `g=0`, its local residence conditions are automatic.

So the local residence geometry yields only

    g>=1 => a=1,

and cannot distinguish `g=1` from `g=2`. Do not infer the converse: `a=1` does not determine the original-cut jump.

## Stopping fence

Do not continue extending the same residence-zero calculation for `g=2`. There are no additional cells in that residence: every required cell is already accounted for and compatible. Run154's contradiction worked only because `g=3` reaches the extra source cell `(3,q)`.

## Next target

To exclude `g=2`, seek an independent condition linking the complete original-cut/global-shadow state to `a=1`, or prove a stronger cut-jump restriction not expressible solely by the local residence trace. The cyclic/gate structure is the most plausible source. A useful negative result would also be to construct a fully admissible finite-support witness satisfying the complete cyclic/gate hypotheses with `g=2`; that would close this hidden-slack route rather than merely the local residence subroute.

New proof: `proofs/informal/problem1_run155_g2_residence_trace_collapses_to_single_driver_bit.md`.
