# Problem 1 run 207 — exact adjacent-tower defect automaton

Problem 1 remains OPEN.

## Setup

Use the reviewed map

    A(q) = (q>>2) XOR ((q>>1) OR q).

Run 206 proved

    A(2q) = 2 A(q) XOR epsilon(q),
    epsilon(q) = q_0 XOR q_1.

The useful strengthening is that the discrepancy between the entire adjacent shift-tower trajectories never spreads beyond bit 0.

Let

    r_k = A^k(q),
    s_k = A^k(2q).

Then for every k >= 0 there is a single bit d_k in {0,1} such that

    s_k = 2 r_k XOR d_k.

Initially d_0=0. Moreover d_k obeys the exact driven recurrence

    d_{k+1} = (r_{k,0} XOR r_{k,1}) XOR (d_k AND (NOT r_{k,0})).

Equivalently, by the two low bits of r_k,

    (r0,r1)=00: d' = d
    (r0,r1)=01: d' = 1 XOR d
    (r0,r1)=10: d' = 1
    (r0,r1)=11: d' = 0.

## Proof

Assume s_k=2r_k XOR d_k. The two inputs 2r_k and 2r_k XOR d_k differ, if at all, only in input bit 0. Under A, input bit 0 can affect only output bit 0, because

    (A u)_i = u_{i+2} XOR (u_{i+1} OR u_i).

Toggling u_0 changes (Au)_0 iff u_1=0. For u=2r_k, u_1=r_{k,0}. Hence

    A(2r_k XOR d_k)
      = A(2r_k) XOR [d_k AND (NOT r_{k,0})].

Using run 206,

    A(2r_k)=2A(r_k) XOR (r_{k,0} XOR r_{k,1}),

so

    s_{k+1}=2r_{k+1} XOR d_{k+1}

with the claimed recurrence. Induction proves the identity for all k.

## Consequences

1. Run 206's 'first defect' is not the end of exact control. At every depth, adjacent shift-tower levels differ from exact doubling by at most the single least-significant bit.

2. The post-defect dynamics is a one-bit automaton driven only by the low two-bit trace of the lower tower orbit. There is no uncontrolled nonlinear spatial spread between A^k(q) and A^k(2q).

3. Once r_k enters its eventual cycle, the driver word (r0,r1) is periodic. The remaining question for tau(2q) versus tau(q) is therefore a finite-state synchronization/phase question for this one-bit driven automaton over the complete low-two-bit cycle word.

4. The recurrence also explains exact resynchronization events. A driver symbol 11 forces d'=0 regardless of the incoming defect; a symbol 10 forces d'=1; 00 preserves d; 01 toggles it.

This is materially stronger than merely locating the first epsilon=1 event. It suggests that the true increment criterion for a_n=tau(2^n x) should be formulated in terms of the complete low-two-bit code of the eventual A-cycle at level n-1 and the phase of d when that cycle is entered.

## What is not proved

This note does not yet give an iff criterion for tau(2q)>tau(q), because the pair (r_k,d_k) can enter its eventual periodic orbit at a phase different from the first periodic time of r_k. In particular, knowing only the first defect time is insufficient.

The next step should classify the one-bit automaton over one period of the eventual low-two-bit driver word. Because each symbol acts on d by one of {identity, toggle, constant-0, constant-1}, the period map is itself one of these four maps. This should give an exact bound/criterion for the extra transient of 2q after q reaches its cycle, and can then be applied to the renewal condition a_n>max(a_{n-1},b+n).
