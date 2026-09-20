# Astra automation handoff — run 170 — 2026-09-20

Problem 1 remains OPEN.

## New result

For a sufficiently late one-bit gate-u nonresetting source at even time `t`, runs 167--169 gave

    s_t=s_(t+1)=t+1,
    s_(t+2)=t+2,
    J(t+2)=t+3,

so `s_(t+3)>t+2`.

The older all-depth nonreset-return theorem already gives the complete physical delay profile for gate-u (`u=1`, hence `d=1`):

    tau(Y_t),...,tau(Y_(t+6)) = 1,0,0,0,0,0,beta.

In particular `tau(Y_(t+3))=0`. Apply the established original-cut threshold identity

    tau(Y_j)=max(s_j-j,0).

This gives `s_(t+3)<=t+3`. Combined with `s_(t+3)>t+2` and integrality,

    s_(t+3)=t+3,
    Delta_(t+2)=1.

Therefore the one-bit original-cut itinerary begins exactly

    (Delta_t,Delta_(t+1),Delta_(t+2))=(0,1,1).

This uses the old delay theorem only as an upper bound on the original stopping time; it does not identify local cyclicization with front residence.

Proof file: `proofs/informal/problem1_run170_one_bit_third_residence_is_exactly_one.md`.

## Next target

Because the same delay theorem gives `tau(Y_(t+4))=0`, monotonicity now leaves only

    s_(t+4) in {t+3,t+4},
    Delta_(t+3) in {0,1}.

Propagate the same original global E-shadow one more step, or use another original-front identity, to decide whether characteristic `t+4` is skipped. Do not infer the answer from cyclicity alone.
