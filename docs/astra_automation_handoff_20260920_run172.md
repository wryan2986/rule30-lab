# Astra automation handoff — run 172 — 2026-09-20

Problem 1 remains OPEN.

## New result

Continue from run 171. At physical time `t+2`, the sufficiently late one-bit gate-u nonresetting source has

    actual (r_1,r_2,r_3) = (1,0,1),
    original shadow (h_1,h_2) = (0,1).

Run 171 proved that position 1 heals on row `t+3`, hence `m(t+3)>=2`.

Position 2 on that row is nevertheless forced to differ. Rule 30 gives

    r_2(t+3) = 1 XOR (0 OR 1) = 0,

while, for arbitrary `b=h_3(t+2)`,

    h_2(t+3) = 0 XOR (1 OR b) = 1.

Therefore

    m(t+3)=2,
    J(t+3)=t+5.

Thus `t+5` is exactly the next characteristic visited by the original-cut global discrepancy front after the skipped characteristic `t+4`.

The old one-bit delay profile gives `tau(Y_(t+5))=0`, hence the threshold identity gives `s_(t+5)<=t+5`. Since `J(t+3)=t+5`, also `s_(t+5)>t+3`. Therefore

    s_(t+5) in {t+4,t+5},
    Delta_(t+4) in {1,2}.

The one-bit original-cut itinerary now begins

    (0,1,1,0,epsilon),  epsilon in {1,2}.

Proof file: `proofs/informal/problem1_run172_one_bit_front_is_exactly_two_at_tplus3.md`.

## Next target

Distinguish `s_(t+5)=t+4` from `s_(t+5)=t+5`, equivalently `Delta_(t+4)=1` from `2`. Evolve the SAME original global E shadow to physical row `t+4` and locate its first discrepancy there. Do not reinitialize a local cyclic shadow.
