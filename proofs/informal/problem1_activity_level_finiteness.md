# Finite levels of the single-column activity record

Status: `partial-proof` for the all-depth results in this note. These are
support criteria and limitations of a proposed growth argument, not a proof
of period-two exclusion or Problem 1. The independent review and its precise
scope are recorded in `problem1_activity_finiteness_independent_review.md`.
Base checkpoint: `726e75881b9388aa56fc106b199558c5d3f96bee`.

## Route and verification scope

The round-three draft proposed finiteness of each activity sublevel set.
Ranked next routes (`heuristic`): (1) verify this compactness argument and
its exact transition laws; (2) use a valid level transition to constrain
actual return histories; (3) seek an ordered-history growth mechanism if
level transitions alone give no control. The first route has an all-depth
statement and a small falsifiable seam, so it comes first. No new census,
graph construction, comparator, or numerical experiment is admitted here.

The original draft's final-time zero-neighbor assertion is `refuted` by
the hand case below. Shortening its time window repairs the proof. The
draft is retained as historical work in progress; this note supersedes it.
The uniform finite-entry dependency has received a fresh complete scoped
Muse derivation in round four, checked by the lead. Its source hashes and
the corrected independent finiteness review are retained separately.

## 1. Definitions and the finite-entry dependency (`partial-proof`)

On the 2-adic integers use

    T(x)=x XOR ((x<<1) OR (x<<2)),
    pi(x)=x>>2,   A(x)=pi(T(x)),
    V_0(x)=0,
    V_s(x)=sum_(t=0..s-1) bit_(2s)(T^t(x)),  s>=1,
    R(x)=sup_(s>=0) V_s(x) in N union {infinity},
    E_K={x:R(x)<=K},  K a nonnegative integer.

The single-column note proves that R(x) is finite exactly when T^h(x)
is a nonnegative integer for some h. More precisely, for

    h=h_V(K)=min{h>=0:sum_(r=0..h) 1/(2r+1)>3K/2},

every x in E_K satisfies T^h(x) in N. Here and below N includes zero.
The proof controls activity in bi-infinite even spatial limits, makes
their last active time spatially constant, and uses the odd harmonic
bound to extinguish ALL such limits at the SAME h. Infinitely many
output ones would supply a nonzero output spatial limit, a contradiction.
It does not assert extinction of the original one-sided columns.

For all s,h>=0, comparison of the sampled time intervals gives

    V_s(T^h(x)) <= V_s(x)+h.                            (1)

There are at most h newly included times; when s<h there are at most
s<=h. Thus T^h(E_K) lies in E_(K+h). The finite-entry theorem alone
does not bound the bit length of T^h(x) uniformly over x in E_K.

## 2. An isolated finite row (`partial-proof`; corrected seam)

Let y be a nonnegative integer of bit length B, with B=0 for y=0.
Suppose z!=y and a=v2(z-y)>=B. The first differing bit is at a;
z has bit a equal to one, and all bits below a agree with y. Set

    N=floor((a-B-2)/2),

and assume N>=0. Causality makes the bits below a of T^t(z) agree
with T^t(y) at every time. Finite propagation gives bitlen(T^t(y))
<=B+2t. For 0<=t<=N we have B+2t<=a-2, so both cells a-2 and
a-1 are zero. Cell a stays one throughout times 0,...,N+1; cell
a+1 toggles at each step up to time N+1.

For even a set s=a/2. Since N<=s-1, its sampled column gives

    V_s(z)>=N+1.

For odd a set s=(a+1)/2. Again N<=s-1, and the toggling column gives

    V_s(z)>=floor((N+1)/2).

Both arguments concern arbitrary 2-adic inputs and arbitrary higher
bits. No observed or unobserved forced branch is used. They include
y=0; the conservative bound remains valid even though that row never
propagates. In particular, for every integer L>=0,

    a>=B+4L+4  implies  R(z)>L.                         (2)

Indeed then N>=2L+1, so even the odd case contributes at least L+1.

The old assertion with N_old=floor((a-B-1)/2) that BOTH lower
neighbors stay zero through N_old is `refuted`: y=1, z=17 give
B=1, a=4, N_old=1, but

    T(17)=17 XOR (34 OR 68)=119,

whose bit a-2=2 is one. The corrected N is zero in this hand case.
This flaw concerned the asserted time endpoint; it was not a
counterexample to sublevel finiteness. The shorter window proves (2).

## 3. Compactness proves finite levels (`partial-proof`)

**Theorem.** E_K is finite for every fixed nonnegative integer K.

Each V_s depends on finitely many digits, so E_K is closed in the
compact binary product Z_2. Let h=h_V(K), L=K+h. Fix x in E_K and
write y=T^h(x), a finite row of bit length B. T is unit-triangular:
its output bit i is input bit i XOR a function of strictly lower
bits. It therefore preserves the position of the first difference,
as does every iterate T^h.

If x' in E_K agrees with x modulo 2^(B+4L+4) and x'!=x, then
z=T^h(x') differs from y first at some a>=B+4L+4. Equation (1)
gives R(z)<=L, while (2) gives R(z)>L. Thus the cylinder

    x + 2^(B+4L+4) Z_2

meets E_K only at x. These cylinders, one for each x in E_K, cover
E_K. A finite subcover exists by compactness, and each member contains
only one point of E_K. Hence E_K is finite.

It follows that a uniform finite output support bound DOES exist for
each fixed K: take the maximum of bitlen(T^h(x)) over this finite
set. This argument supplies no explicit formula for that maximum.
Compact subsets of ordinary integers need not be finite; the isolation
step above, not mere finite entry, is essential.

## 4. Exact level transitions (`partial-proof`)

The established identities pi A=A pi and A^t=pi^t T^t give

    V_s(x)=sum_(t=0..s-1) bit_0(A^t(pi^(s-t)(x))).

For s>=1, applying this to Ax and shifting the summation index proves

    V_s(Ax)=V_(s+1)(x)-bit_(2s+2)(x).                  (3)

Do not justify (3) by commuting pi with T, or A with T. These
one-sided maps do NOT commute: pi(T(1))=1 while T(pi(1))=0;
A(T(1))=6 while T(A(1))=7. In (3) only pi A=A pi is needed.
The independent review's first attempted commuting-T derivation was
rejected and replaced by the displayed A-diagonal argument.

Every ordinary generator G in {T,U,P} satisfies pi G=A. Since all
projection exponents s-t in the sum are at least one, applying G
changes the time-index interval from 0,...,s-1 to 1,...,s. Hence

    V_s(Gx)=V_s(x)-bit_(2s)(x)+bit_0(A^s(x)).          (4)

In particular

    A(E_K) subset E_K,       G(E_K) subset E_(K+1).

Deleting one low pair also preserves the level. The same diagonal
sum, this time removing its final term, gives for s>=1

    V_s(pi x)=V_(s+1)(x)-bit_2(A^s(x)),                (4a)
    pi(E_K) subset E_K.

On its permitted domain the actual step is F(x)=Q(Ax), Q=T or U,
so the conclusion is only

    F(E_K intersect domain(F)) subset E_(K+1).          (5)

The increase by one in (5) is sharp even on an ordinary permitted
input; replacing E_(K+1) by E_K there is `refuted`. A hand certificate
is x=27, which has ordinary history P,U from root 1 (P(1)=6,
U(6)=27), and its permitted t step is F(27)=T(A(27))=T(25)=111.
The exact A cycles are 25<->27 and 100<->111. For the first cycle,
both initial bits at position 2 vanish, both bits at position 4 are
one, and both states have all bits at positions>=6 zero. Equation
(3) therefore gives V_1=0 and V_s=1 for every s>=2 on both states.
For the second cycle, both bits at positions 2 and 6 are one, both
bits at position 4 vanish, and positions>=8 vanish. Equation (3)
gives V_1=V_2=1 and V_s=2 for every s>=3. Thus

    R(27)=1,       R(F(27))=R(111)=2.

The successor 111 is 15 modulo16 and has no further permitted step.
This refutes only the universal one-step nonincrease claim; it is
not a counterexample on the infinite-survivor domain, nor a new
return or frontier census. The finite arithmetic and all-age cycles
above are hand-derived, not extrapolations of a sampled age range.

The base level is E_0={0,1,2,3}. These four inputs have V_s=0 by
finite propagation. Any even input bit at index>=2 gives V_s>=1 at
time zero for its own age. If all such even bits vanish but an odd
bit at index>=3 is one, the next even column becomes one after one
update and its sampled age is at least two. Thus it also violates E_0.
This covers arbitrary infinite high tails, not just finite inputs.

## 5. A precise limitation for forced trajectories (`partial-proof`)

Finiteness of each E_K supplies no finite state space for an orbit
whose allowed K increases at every step. In fact it yields a useful
warning with an exact quantifier. Suppose x has an infinite forced
orbit x_r=F^r(x), and R(x)<infinity. The finite-entry equivalence in
the single-column/temporal-deficit notes implies that x_r is finite
for all sufficiently large r. Its permitted residue is 7 or 11
modulo16, and every further forced step increases bit length by two.
Thus the states eventually have distinct, unbounded bit lengths.

For each fixed K the set E_K is finite. The orbit can therefore visit
E_K only finitely often after its finite entry. Consequently

    R(x_r) tends to infinity as r tends to infinity,    (6)

even though the initial record R(x) is finite. At the same time (5)
gives R(x_r)<=R(x)+r. Both conclusions are conditional on the assumed
infinite forced orbit; its existence from a finite input is NOT asserted.

Thus growth of the activity bound ACROSS successive forced states
would not exclude a finite initial survivor. The required theorem is
unbounded V_s for ONE fixed actual survivor as its age s grows. That
remains open, as do the full-fringe growth mechanism, B_all, and least
temporal periods at least three. No graph or sublevel census follows
from this result.
