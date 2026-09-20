# Astra automation handoff — run 169 — 2026-09-20

Problem 1 remains OPEN.

## New result

Continue from run 168 for a sufficiently late one-bit gate-u nonresetting source at even time `t`:

    s_t=s_(t+1)=t+1,
    s_(t+2)=t+2,
    m(t+1)=1.

At the source the classified actual/global-shadow cells are

    actual bits0..3 = (1,1,1,0),
    original-shadow bits0..3 = (0,1,1,0).

Run 168 gives row `t+1` position-1 bits `0` actual versus `1` shadow. Since `m(t+1)=1`, position 0 agrees; call its common value `c`. The shared source bits1..3 force position 2 on row `t+1` to be 0 in both rows. Therefore the next Rule-30 update at position 1 is

    actual r_1(t+2)=c,
    shadow h_1(t+2)=c XOR 1.

Thus position 1 is again a discrepancy at time `t+2`, independent of all wider-right driver bits. Since `s_(t+2)=t+2`, the global-front theorem gives `m(t+2)>=1`; hence

    m(t+2)=1,
    J(t+2)=t+3.

So characteristic `t+3` is exactly the next characteristic with stopping time beyond physical time `t+2`.

Important fence: this proves only `s_(t+3)>t+2` (hence `Delta_(t+2)>0`), not `s_(t+3)=t+3`. The remaining problem is the residence length of characteristic `t+3`, not which characteristic comes next.

Proof file: `proofs/informal/problem1_run169_one_bit_shadow_keeps_front_at_one_on_second_return.md`.

## Next target

Use the classified cyclic return at `t+2`, the eventual delay bound, and the threshold/original-cut machinery to bound or determine `s_(t+3)`. Do not identify local cyclicization delay with global-front residence.
