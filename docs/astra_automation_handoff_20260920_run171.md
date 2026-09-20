# Astra automation handoff — run 171 — 2026-09-20

Problem 1 remains OPEN.

## New result

For every sufficiently late one-bit gate-u nonresetting source at even time `t`, runs 167--170 gave

    s_t=s_(t+1)=t+1,
    s_(t+2)=t+2,
    s_(t+3)=t+3,

and run 169 gave `m(t+2)=1`.

The older all-depth nonresetting classification says the next even row `t+2` is cyclic with actual gate `t`. FULL therefore fixes

    (r_0,r_1,r_2,r_3)(t+2)=(1,1,0,1).

Combining this with the run-168/169 shadow propagation fixes the original-shadow pair at positions 1,2 on that row to

    actual: (1,0),
    shadow: (0,1).

Because `m(t+2)=1`, position 0 agrees. One Rule-30 step then makes position 1 agree on row `t+3`:

    r_1(t+3)=h_1(t+3).

But `s_(t+3)=t+3` implies `m(t+3)>=1`. Since position 1 is equal, actually

    m(t+3)>=2,
    J(t+3)>=t+5.

Hence `s_(t+4)<=t+3`; monotonicity with `s_(t+3)=t+3` forces

    s_(t+4)=t+3,
    Delta_(t+3)=0.

Therefore the one-bit original-cut itinerary now begins exactly

    (Delta_t,Delta_(t+1),Delta_(t+2),Delta_(t+3))=(0,1,1,0).

Characteristic `t+4` is necessarily skipped.

Proof file: `proofs/informal/problem1_run171_one_bit_fourth_characteristic_is_skipped.md`.

## Next target

Determine whether position 2 at physical time `t+3` is an actual/original-shadow discrepancy. We know `m(t+3)>=2`. If position 2 differs, then `m(t+3)=2` and `J(t+3)=t+5`; combine that with the old zero-delay bound at `t+5` to constrain or fix `s_(t+5)`. If position 2 also agrees, the global front skips at least one more characteristic. Keep using the SAME original global E shadow, not a reinitialized local cyclic shadow.
