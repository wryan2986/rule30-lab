# Astra automation handoff — run 12

Problem 1 remains **OPEN**.

This run starts from branch head `6b787c35e53b18876cb7d6cd4b393d21c5d60270` and adds `proofs/informal/problem1_period_growth_on_periodic_zero_extension_runs.md`.

## New exact structure: cycle period is a monotone power-of-two potential on a periodic zero-extension run

Let `z` be `A`-periodic with exact period `p`, and let `w=2z+a_0` be a periodic one-bit lift. Using the already-proved lift recurrence

    a_(s+1)=c_s XOR (b_s OR a_s),

consider the return map on the lift bit after one base period. Because the fiber has two states and projection has exact period `p`, every periodic lift has exact period

    p  or  2p.

More precisely:

- if the base low trace has an eraser (`b_s=1` somewhere in one period), the recurrent periodic lift has exact period `p`;
- if the base low trace is identically zero, the period is `p` or `2p` according to the parity XOR of the `c_s` trace.

Therefore along a literal periodic zero-extension chain

    z_q=2^q u,

its exact periods satisfy

    p_(q+1) in {p_q,2p_q}.

They never decrease during the periodic prefix.

## New depth/period obstruction

If nonzero `2^q u` is `A`-periodic with exact period `p`, then necessarily

    q < 2p.

Proof: if `q>=2p`, the exact shift/Rule-30 identity gives

    A^p(2^q u)=2^(q-2p)T^p(u).

Periodicity would imply

    T^p(u)=2^(2p)u,

but `T` preserves the 2-adic valuation of every nonzero state, while the right side raises it by `2p`.

Hence deep periodic skip runs force cycle-period doublings. Writing

    p_q=p_0*2^(D_q),

the periodicity condition gives

    q < 2 p_0 2^(D_q).

So successive negative plateau segments are not memoryless scalar events: sustaining a deep periodic prefix requires persistent period growth.

## Exit period also bounds exit preperiod

If `Q` is the first nonperiodic extension and `z_(Q-1)` has exact period `p`, then the terminal parent must contain an eraser (otherwise both lifts would be periodic). The lift classifier therefore gives

    1 <= tau(z_Q) <= p.

Combined with the run-10 causal estimate,

    tau(z_Q) >= ceil((Q+1)/2),

we get

    p >= ceil((Q+1)/2).

Thus a long deficit exits from a periodic core whose cycle period has already reached at least half the periodic-prefix depth.

## Canonical v=1 example

For the run-11 chain

    25,50,100,200,400,

the exact periods are

    2,2,2,2,4.

The doubling at `400` is forced by the new depth/period obstruction: at depth `q=4`, period `2` would require the impossible strict inequality `4<4`.

So the previous sharp negative plateau `Q=5,d=3` is now understood to carry an irreversible period-doubling event before its exit.

## Preferred next target

Try to turn this period potential into a true inter-plateau compensation mechanism.

Specifically, track both tower preperiod and the exact period of the stripped periodic core. Seek one of:

1. a theorem that a period doubling accumulated during a negative plateau forces additional preperiod surplus at a later plateau/rise; or
2. a common-origin/FULL bound on how many period doublings can occur while `h_n-n` remains bounded above.

Do not revert to scalar `(Q_H,d_H)` analysis alone; run 11 disproved local full repayment, while this run shows the missing memory is at least partly encoded in cycle-period growth.

New proof commit before this handoff: `22ec060d3d9099a3ab53b7f9bc46c2f264373dc0`.
