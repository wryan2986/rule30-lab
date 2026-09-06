# A mortal periodic tail need not have a pair active at every age

Status: `partial-proof` / `refuted` by the hand certificate below, with
independent derivation and complete packed/cell-array agreement accepted
after lead audit. Review: `problem1_anchored_activity_vertical_spine_review.md`;
the round-six audit retains original admissions and execution histories.
Problem 1 remains open. No general linear-bound
impossibility or actual-survivor counterexample is claimed.

## Admission and precise route

The new anchored finite-entry proof counts activity in different spatial
intervals at different ages. A tempting strengthening would align those
witnesses in one fixed pair: whenever a bi-infinite A spacetime has final
nonzero row at time M, some even-aligned pair is nonzero at EVERY time
0,...,M. Under a per-pair budget K this would give M+1<=K, replacing the
harmonic extinction estimate by h<=K. This would substantially strengthen
the bounded-activity alternative available to a full-fringe argument.

The three temporal words below were derived by hand from the inverse scan,
without any search. Their proposed cycle would refute this alignment claim
and the coefficient-one extinction bound. If a local identity fails, the
claimed counterexample must be withdrawn; no search expansion follows.
The ONLY admitted computational verification is these three six-symbol
words and the corresponding single six-cell spatial period for six updates,
using packed arithmetic and an independent cell-array rule. No period,
frontier, ray, mortality-level, or prefix census is admitted. Local one CPU,
120 seconds, 1 GiB, with exact sources, full Git, hashes, hardware/software,
timing and an atomic record. Agreement certifies only this fixed witness.

## 1. Three temporal words (`partial-proof`, exact hand calculation)

Extend each displayed temporal word by zero forever:

    v_0=(2,3,2,1,0,3),
    v_1=(0,1,2,3,1,3),
    v_2=(3,1,0,2,2,3).

Use the established deletion rule (Phi v)_t=g(v_t,v_(t+1)), with

    g((a0,a1),(b0,b1))=(r,s),
    r=b0 XOR(a0 OR a1), s=b1 XOR(a1 OR r).

The exact identities are

    Phi v_0=v_1, Phi v_1=v_2, Phi v_2=v_0.            (1)

For example the six component evaluations in the first identity are

    g(2,3)=0, g(3,2)=1, g(2,1)=2,
    g(1,0)=3, g(0,3)=1, g(3,0)=3.

The terminal zero extensions stay zero since g(0,0)=0. Each word has
exactly FIVE nonzero times, but misses a different time: respectively
4,0,2. They all have final symbol 3 at time 5.

## 2. The full bi-infinite spacetime (`partial-proof`)

Repeat the initial spatial PAIRS (2,0,3) across all integer pair indices.
The corresponding six-bit spatial word has packed value 50, with low-to-high
bits (0,1,0,0,1,1). Reading the three words in (1) as columns gives
the complete periodic A evolution below. Each integer encodes six cells;
the rule is cyclic on that period, not a finite row with zero boundaries.

| time | three spatial pair symbols | six-bit word |
| --- | --- | --- |
| 0 | 2,0,3 | 50 |
| 1 | 3,1,1 | 23 |
| 2 | 2,2,0 | 10 |
| 3 | 1,3,2 | 45 |
| 4 | 0,1,2 | 36 |
| 5 | 3,3,3 | 63 |
| 6 and later | 0,0,0 | 0 |

Equation (1) is precisely the local compatibility needed for these temporal
columns to obey A at every cell and time; it was obtained by solving those
same two local equations. Equivalently verify each row by

    u_i(t+1)=u_(i+2)(t) XOR(u_(i+1)(t) OR u_i(t)),
    indices modulo 6.

The spatial period lifts the six-cell verification to ALL integer spatial
indices. The final zero row is fixed, so the displayed finite temporal
certificate covers ALL later times. No extrapolation from a sampled tail
is used.

## 3. Exact scope of the obstruction (`refuted`)

Every even-aligned pair has five nonzero times, but none is active at all
six times before extinction. Thus the proposed vertical alignment claim is
false, and the implication "per-pair activity <=K => extinction by time K"
is false at K=5: this row is still all ones at time 5 and dies at time 6.

This also gives an exact one-sided rational example. Put

    x=50/(1-64)=-50/63 in Z_2.

Its pairs repeat (2,0,3) starting at index zero. Because A only uses bits at
the current or higher indices, the same cyclic rows describe its entire
one-sided A orbit. Every row before time 6 has a nonzero periodic tail;
A^6 x=0. Therefore the first finite-entry time for A (and for T, using
A^h=pi^h T^h) is exactly 6.

For every n>=6 the anchored horizon includes all six potentially nonzero
times, so J_n(x)=5. For smaller n, J_n<=n<=5. Hence Q(x)=5 exactly.
This refutes even the anchored variant "Q(x)<=K => A^K(x) finite".

The harmonic theorem is unaffected: H_6=49/20<=5. This ONE counterexample
does not refute an extinction bound cK for some larger constant c, establish
superlinear optimal growth, or classify other mortality heights. Its low
pair is 2, so it is not even a permitted actual survivor. It supplies no
counterexample to full-fringe growth. The retained conclusion is only that
the different-time witnesses cannot universally be aligned in one pair.
