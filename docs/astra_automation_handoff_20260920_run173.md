# Astra automation handoff — run 173 — 2026-09-20

Problem 1 remains OPEN.

## New result

Continue from run 172. The sufficiently late one-bit gate-u nonresetting source had

    (Delta_t,...,Delta_(t+4))=(0,1,1,0,epsilon),
    epsilon in {1,2},

with

    m(t+3)=2,
    r_2(t+3)=0,
    h_2(t+3)=1

for the SAME original global E shadow.

The classified cyclic return at `t+2` has actual low cells

    (r_0,r_1,r_2,r_3)=(1,1,0,1).

Hence Rule 30 gives

    r_1(t+3)=1 XOR (1 OR 0)=0.

Run 171 already proved position 1 heals there, so `h_1(t+3)=0`. Since `m(t+3)=2`, position 0 also agrees; call its common value `c`.

One further Rule-30 step at position 1 gives

    r_1(t+4)=c XOR (0 OR 0)=c,
    h_1(t+4)=c XOR (0 OR 1)=c XOR 1.

Thus position 1 is forced to differ at `t+4`, independently of all wider-right shadow bits. Run 172 gives `s_(t+5)>t+3`, so the global front at `t+4` cannot lie left of position 1. Therefore

    m(t+4)=1,
    J(t+4)=t+5.

Hence `s_(t+5)>t+4`. Together with the previous upper bound `s_(t+5)<=t+5`,

    s_(t+5)=t+5,
    Delta_(t+4)=2.

The exact one-bit original-cut prefix is now

    (0,1,1,0,2).

Proof file: `proofs/informal/problem1_run173_one_bit_fifth_residence_is_exactly_two.md`.

## Next target

Determine `s_(t+6)` by following the SAME original global E shadow through the second row of the characteristic `t+5` residence. Combine this with the established terminal delay `tau(Y_(t+6))=beta`. The goal is to decide whether the six-step one-bit cut itinerary is fully rigid or whether the terminal birth/reset parameter first introduces genuine freedom there. Do not reinitialize a local cyclic shadow.
