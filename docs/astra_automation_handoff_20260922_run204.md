# Astra automation handoff — 2026-09-22 run 204

Problem 1 remains OPEN.

## New result

Continue only the corrected run-193--204 chain.

Run 203's renormalization identities remain valid, but its description of

    T(q)=q XOR ((q<<1) OR (q<<2))

as linear was incorrect. `T` is nonlinear because bitwise OR contributes a quadratic Boolean term. Do not use linear superposition for `T`.

The exact bit recurrence is

    (Tq)_i = q_i XOR (q_(i-1) OR q_(i-2)).

This is triangular and gives an exact inverse recursion from low bits upward:

    q_i = (Tq)_i XOR (q_(i-1) OR q_(i-2)).

Therefore `T` is injective on finite integers. Also, for every nonzero finite `q`,

    h(Tq)=h(q)+2,

so

    h(T^m x)=h(x)+2m.

Thus `T^m x` never enters a bounded finite state space; a periodicity/dimension-counting proof of the run-203 target cannot work. The needed theorem must genuinely control the `A`-preperiod of a state whose width grows by exactly two bits per `T` step:

    tau(T^m x) <= b+m,
    tau(2T^m x) <= b+m+1

eventually (or exploit the weaker renewal condition including strict increase).

Next target: combine the triangular bit recurrence for `T` with the existing `A` erasing-history/cycle-completion identities. Look specifically for a statement that one `A` step can eliminate, in the preperiod sense, the two new high bits introduced by one `T` step. Do not assume this from width alone, and do not return to shift-tower sampling or local driver-bit propagation.

Proof note: `proofs/informal/problem1_run204_T_is_nonlinear_triangular_injective.md`.
