# Next candidate: finite levels of the activity record

Round-four disposition: the final-time zero-neighbor assertion below has
a hand counterexample, and a shorter window repairs it. The resulting
finite-level theorem, exact transitions and scoped independent review are
now in `problem1_activity_level_finiteness.md` and
`problem1_activity_finiteness_independent_review.md`. This draft is kept
as historical work in progress, not the current proof source.

Status: `inconclusive` as a proposed research route. The derivation below
is lead work in progress, not an externally verified theorem. It depends
on the temporal-activity finite-entry theorem, whose review disposition
must be read before using it. No experiment, graph construction, or
new numerical input is admitted by this draft.

The question is whether the new unbounded-memory observable nevertheless
has finite sublevel sets. A proof would justify a finite set for EACH
fixed activity bound, not one fixed state space for the whole problem.
A flaw in the isolation argument would close this particular compactness
route. The actual-survivor growth question would remain in either case.

## Candidate statement and compactness

Use V_s from `problem1_single_column_activity.md`, and define

    E_K={x in Z_2 : V_s(x)<=K for every s>=0},   K>=0.

Candidate: E_K is finite for every fixed integer K.

Each V_s depends on finitely many input digits, so E_K is a closed
subset of the compact binary product Z_2. The existing finite-entry
argument gives one common h=h_V(K) such that T^h(x) is nonnegative
finite for every x in E_K. This does not yet give a common spatial
support bound and does not, by itself, prove E_K finite.

The proposed additional step is to isolate each member of this compact
set, using the impossibility of hiding a first far-away one above a
fixed finite row without creating large temporal activity.

## Proposed isolation estimate

Fix a nonnegative integer y of bit length B (B=0 for y=0). Suppose
z!=y and a=v2(z-y)>=B, so their bits below a agree and z has a one
at a above y's zero tail. Put

    N=floor((a-B-1)/2).

When a is sufficiently large that N>=0, at times 0,...,N the cells
at a-1 and a-2 still equal zero: their lower input cone agrees with
the finite row y, whose bit length at time t is at most B+2t.
The cell at a stays one throughout these times. Bits above a do not
affect these assertions, by the causal direction of T.

If a is even, take s=a/2. Since N<=s-1, column a is sampled at
least N+1 times and V_s(z)>=N+1.

If a is odd, take s=(a+1)/2. The cell at a+1 toggles at every step
while cell a is one, because its update XORs the OR of cells a,a-1.
Among times 0,...,N it therefore has at least floor((N+1)/2) ones,
and V_s(z)>=floor((N+1)/2).

In both cases a>B+4L+5 suffices to contradict the assertion
V_s(z)<=L at every age. Constants here are deliberately nonsharp.
Before adopting the candidate, independently check these time endpoints,
the case B=0, odd a, and why no unobserved gate is needed: this estimate
is about arbitrary T inputs, not about executing forced branches.

## Proposed compactness conclusion

For every x and fixed h>=0, direct comparison of the time intervals
in the definition of V gives

    V_s(T^h(x)) <= V_s(x)+h.                             (1)

The newly included times are at most h, even when s<h. Consequently
T^h(E_K) has activity bounded by L=K+h.

Fix x in E_K and put y=T^h(x), which is finite by the finite-entry
theorem. The unit-triangular map T preserves the first differing bit
of two 2-adic inputs. Thus if another x' in E_K is sufficiently close
to x, the first difference of z=T^h(x') and y has the same arbitrarily
large position a. The isolation estimate contradicts their common
activity bound L unless x'=x. Each member of E_K would therefore
have an open binary cylinder meeting E_K only in that member.

Compactness supplies a finite subcover by these singleton-intersection
cylinders, proving the proposed finiteness. This is the step to review;
compact subsets of the ordinary integers need NOT in general be finite,
so substituting that false shortcut would invalidate the argument.

## Why this would not finish the forced-orbit argument

Two exact algebraic identities are useful consistency checks, but are
not a growth theorem. For s>=1, causality and pi A=A pi give

    V_s(Ax)=V_(s+1)(x)-bit_(2s+2)(x).                    (2)

Thus A would map E_K into itself. Also the three ordinary generators
G=T,U,P all satisfy pi G=A, so

    V_s(Gx)=V_s(x)-bit_(2s)(x)+bit_0(A^s(x)).            (3)

The equality is independent of the last generator. All projections
in the A-diagonal formula for V have exponent at least one.
In particular V ignores the lowest two input bits entirely. Directly,
the earliest input position affecting bit2s(T^t x) with t<s is at
least two. The hand base level is therefore E_0={0,1,2,3}: a one
at an even index>=2 pays at time zero; if the first high one is at
an odd index>=3, the next even column pays at time zero or one.

Equation (3) gives G(E_K) subset E_(K+1). Since an actual forced
step is F(x)=Q(Ax), these identities yield only

    F(E_K intersect permitted domain) subset E_(K+1).

The bound can grow at every forced step. Finiteness of each E_K
therefore does NOT imply that an infinite forced orbit has finitely
many states or an eventually periodic schedule. It supplies neither
a uniform graph for all K nor a decreasing potential on returns.
No graph or sublevel census is authorized without a further theorem
that addresses this growth of the allowed level.

Next session: independently verify or refute the isolation estimate and
the complete compactness deduction before treating this candidate as
established. Then decide whether its exact level transition can constrain
ACTUAL return histories. Merely enumerating larger K is not the next step.
