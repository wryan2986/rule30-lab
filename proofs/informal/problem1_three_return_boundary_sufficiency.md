# Boundary sufficiency and the temporal-transient bridge

Status: `partial-proof` for the unconditional frontier-membership lemma and
the conditional implications below, independently checked by Muse. The
boundary bound itself remains `inconclusive`. No exclusion of eventual
alternation or solution of Problem 1 is claimed without that hypothesis.

## Candidate statements and admission

Let `sigma(x)` be the forced ordinary zero schedule from the renewal note,
and call a schedule admissible if it avoids `uu`, `ttttt`, and `ututtu`.

Candidate implication A: under (B_all), every three-return occurrence on every
phase frontier at ANY cut c>=0 obeys `c+1<=k-2`, so no phase-frontier state has an
infinite admissible forced schedule. Indeed, such a schedule would have
three-return occurrences at unbounded cuts. A proposed finite consequence
is that no admissible forced prefix from complexity k has length k+18.
Neither statement asserts that the boundary bound has been proved.

Candidate implication B: if an odd positive finite seed integer S has an
eventually alternating diagonal trace, then some ordinary phase-frontier
state has an infinite admissible forced schedule. A direct physical
construction, intended to handle arbitrary finite temporal transients, is:

1. Write `R_t=T^t(S)` and choose an alternating 1-phase time n beyond both
   the temporal transient and `bitlen(S)`.
2. The current center-and-left integer is `X=R_n>>n`. Since S occupies the
   low n bits, `X=(T^n)|_S(0)`. Closure of forward sections on `{T,P,U}`
   places this nonzero integer in an ordinary phase frontier after removing
   initial generators T that fix zero.
3. Alternation forces `X=3 mod4`. Direct Rule 30 evolution of this half-row
   gives `X1=P(X>>1)=2P(X>>2)` after one step and
   `X2=T(X1>>1) xor b=Q(P(X>>2))` after the second, where
   `b=not(right_neighbor_1 or right_neighbor_2)` at the even phase.
4. This is the normalized forced recurrence, with the physical fringe
   supplying an admissible infinite driver by the existing local-language
   theorem.

Independent verification is asked to attack the half-row boundary bit, word
order, section indices, initial T removal, time alignment, and the distinction
between temporal preperiod and an emitted spatial zero suffix. A failure
would locate a missing bridge premise; a valid derivation would show that
the boundary bound is a standalone sufficient route to exclude eventual
alternation, including temporal transients in the original zero-right-half
seed class. It would not handle eventual periods of least period >=3.

Only hand derivation, independently written small section/half-row checks,
and finite word-language checks are admitted here; no frontier census or
search-cap increase. Every nontrivial verification writes atomic provenance.

## 1. Unconditional membership of an evolved half-row (`partial-proof`)

Use uppercase `T,P,U` for the forward maps and lowercase `t,p,u` for their
inverses. In arithmetic frontier analyzers the uppercase forward maps are
also printed as lowercase generator labels; this notation difference does
not change the functions. Explicitly,

```text
T(x)=x xor ((x<<1) or (x<<2)),
U(x)=T(x) xor 1,
P(x)=T(x) xor 1 xor (2 if x is even else 0).
```

Their root actions and sections are

```text
T=(T,P),  P=(U,P) swap,  U=(T,P) swap.
T(0)=0, P(0)=3, U(0)=1.
```

The frontier generator agrees with this P: expanding T at the odd input
gives `P(r)=(T(1+2r)-1)/2=T(r) xor 1 xor (2 if r is even else 0)`.

Here a section at an n-bit input word r satisfies

```text
F(r+2^n z) = (F(r) mod2^n) + 2^n F|_r(z).
```

**Lemma.** For every positive integer S, put `s=bitlen(S)`. For every
integer `n>=s`,

```text
X_n=T^n(S)>>n belongs to O_(a,k),
k=ceil((s+n)/2),
a=p if s+n is even, and a=u if s+n is odd.
```

Proof. Since `S<2^n`, the section formula gives
`X_n=(T^n)|_S(0)`, with S read as an n-bit word. By section composition and
closure of `{T,P,U}` under sections, `(T^n)|_S` is a composition of n
forward generators. Explicitly, with `FG=F composed with G`, the chain rule
is `(FG)|_r=F|_(G(r) mod2^n) composed with G|_r`. Put
`r_j=T^j(S) mod2^n`; then
`(T^n)|_S=T|_(r_(n-1)) composed with ... composed with T|_(r_0)`.
Evaluate on zero starting with the rightmost factor, at r_0.
Remove any initial T applications, which fix zero. The result is nonzero:
the degree law gives `bitlen(T^n(S))=s+2n`, hence `bitlen(X_n)=s+n`.
Thus the first remaining generator is P or U, giving seed 3 or 1.
Every subsequent generator adds two to the bit length. This is precisely
membership in one phase frontier, whose bit-length law determines the
displayed phase and complexity. This proves the lemma at every n, with no
alternation assumption. The hypothesis `n>=s` is essential to the zero input
in the section formula.

At times `n,n+2,n+4,...`, phase a consequently stays constant and frontier
complexity increases by one per block. No claim of surjectivity onto these
frontiers is made: these are necessary membership conditions on actual rows.

## 2. Direct physical realization of the forced recurrence (`partial-proof`)

Encode an initial finite configuration with rightmost one at cell 0 by
`S=sum_(i>=0) x_(-i)(0) 2^i`, so S is odd and positive. The moving-edge
encoding of Rule 30 gives

```text
R_t=T^t(S),
x_j(t)=bit_(t-j)(R_t) whenever t-j>=0,
c_t=bit_t(R_t).
```

In particular `X_t=R_t>>t` encodes the current center and all cells to its
left. This relation follows directly from Rule 30: the new packed bit at
position r is the old bit r XOR the OR of old bits r-1 and r-2.

Suppose the center is 1 at time t and 0 at time t+1. Its left neighbor must
then be 1 because `0=x_(-1)(t) xor (1 or x_1(t))`. Hence `X_t=4z+3`.
The first updated center-and-left half-row is

```text
X^(1)=(X_t>>1) xor (X_t or (X_t<<1))
     =T(X_t)>>1=P(X_t>>1)=P(2z+1)=2P(z).
```

For positions strictly left of center this is the ordinary Rule 30 formula.
At the center, its value 1 masks the unspecified right neighbor, which
justifies the same formula at the boundary bit. The identities with P also
follow from the forward section table, giving a second algebraic derivation.

At odd time t+1 the center is zero and the right neighbor is

```text
b=1 xor (x_1(t) or x_2(t)).
```

The second half-row therefore satisfies

```text
X_(t+2)=T(X^(1)>>1) xor b
       =Q(P(z)),
Q=U if b=1, and Q=T if b=0.
```

The only boundary correction is bit b at the center; all other bits follow
the same packed rule. Here evenness is essential: `X^(1)=2P(z)` implies
`T(X^(1))>>1=T(X^(1)>>1)`. This proves the normalized recurrence directly in
physical spacetime, without identifying an arbitrary dual boundary point
with a finite seed.

If the center continues alternating forever from time t, every even-phase
half-row is `3 mod4`. The exact continuation table is

```text
X mod16 = 7: unique continuing branch U;
X mod16 = 11: unique continuing branch T;
X mod16 = 3 or 15: neither branch continues with next X=3 mod4.
```

For clarity, a return to center value 1 after two steps is not automatic:
it requires `bit_2(X)=b`. The following center value 0 also requires
`bit_3(X)=1-b`. Together these conditions give precisely 7 or 11 above.

Thus permanent alternation makes the physical sequence an infinite orbit of
the exact forced map `X -> Q(P(X>>2))`, with forced schedule `sigma(X)`.
Its driver is the physical fringe indicator `b`. By the all-fringe-state
local-language theorem in `problem1_period_two_fringe_language.md`, it avoids
`uu`, `ttttt`, and `ututtu`. That theorem restarts at any even-phase row and
does not require a zero fringe there.
Each forbidden finite window lies entirely in the alternating tail; its
finite dependency cone starts at that row with an arbitrary fringe state.

## 3. The temporal-transient bridge (`partial-proof`)

**Theorem.** If some odd positive finite S has eventually alternating
diagonal trace, then an ordinary phase-frontier state has an infinite
admissible forced schedule.

Proof. Choose a time n beyond `bitlen(S)` and beyond the temporal transient,
with center value 1. Such times exist arbitrarily late in an alternating
tail. Section 1 places `X_n` in a definite `O_(a,k)`. Section 2 gives its
infinite admissible forced schedule. Both constructions use the original
right-zero initial seed S; no time-shifted seed with a different right half
is substituted. This discharges the temporal-transient bridge for this seed
class.

The theorem has a one-way conclusion. It does not say that every ordinary
frontier state, or every admissible forced schedule, is physically realizable
by such a seed. In particular the universal frontier domain can contain
obstructions irrelevant to a more narrowly coupled physical-row invariant.

## 4. The boundary bound alone suffices (`partial-proof`, conditional)

Use the full occurrence domain of Section 2 of
`problem1_period_two_three_return_adjacent_shadows.md`: a cut is ANY integer
`c>=0`, with `|w|=c`, `sigma(x)` beginning `w E(g)`, and `w E(g) u`
admissible. There is NO restriction `L=c+1<k` in this definition.

Assume the following unproved hypothesis, for both phases and every `k>=2`:

```text
Every full-domain three-return occurrence x in O_(a,k), at ANY cut c>=0,
with the established final-u admissibility, satisfies c+1<=k-2.   (B_all)
```

This is the all-cuts boundary obligation identified in
`problem1_signed_mass_scope_audit.md`, not merely the restricted signed-mass
conjecture's domain `L<k`. A bound only for `L<k` does not justify the late-cut
argument below: it leaves cuts with `L>=k` untreated. Neither the restricted
signed conjecture nor finite absence proves (B_all).

Suppose `sigma(x)` were infinite and admissible for some `x in O_(a,k)`.
It cannot have a terminal t-run because `ttttt` is forbidden. Its u positions
are therefore unbounded, and consecutive u gaps lie in `{2,3,4,5}`.
Choose a u position `c>=k-2` and its next three return gaps g. The actual
fourth u exists, so the prefix through it is an admissible `w E(g) u`.
This is a full-domain occurrence with `c+1>=k-1`, contradicting (B_all).
For the singleton levels k=1, states 3 and 1 have no continuing forced
branch directly from the modulo-16 rule. Thus no frontier state at any
complexity has an infinite admissible forced schedule.

Combining with Section 3 proves the conditional implication

```text
(B_all) => no odd positive finite S has an eventually alternating diagonal.
```

This bypasses signed-mass nonvanishing, the existence of a dominant shadow,
and the phase-minimizer penalty telescope. Full adjacent inclusion still
implies (B_all) conditional on the existing separation lemma (`partial-proof`,
using the phase-frontier projection theorem); it is a stronger sufficient
route. More generally any proved finite upper bound on admissible occurrence
cuts for each fixed frontier complexity would give the same termination
conclusion. No such all-depth bound is supplied here.

## 5. A finite-length consequence, not a proved bound on Rule 30

Under hypothesis (B_all), for `k>=2`, an admissible prefix of `sigma(x)`
cannot have length `k+18`. Indeed, its positions k-2 through k+2 contain a u
at some c, since five t's are forbidden. Three further u's occur at gaps at
most five, with the fourth at position at most `c+15<=k+17`. The length-k+18
prefix therefore contains an admissible `w E(g) u` with c>=k-2, again
contradicting (B_all). Thus `k+17` is a sufficient conditional upper bound on
admissible prefix length; it is not asserted as sharp.

The word `ttttu` repeated four times shows the worst placement of four
observed u's in a 20-letter window. This does not establish a sharp threshold
for the original occurrence convention, whose final u need only be admissible,
not observed.

## Scientific boundary and verification

Unconditional all-depth progress is the actual-half-row frontier-membership
lemma, its exact phase/complexity formula, the direct physical two-step
identity, and the implication from an eventually alternating finite-seed
trace to an infinite admissible frontier schedule. Muse independently derived
and checked these statements, with small finite membership and cell-array
tests recorded separately. The general proofs above do not follow by
extrapolating those tests.

Atomic finite verification records in `results/problem1/` are
`20260905_boundary_frontier_membership.json` (508 rows: S=1..127 and
n=bitlen(S)..bitlen(S)+3), `20260905_boundary_half_row_identity.json`
(512 half-row/right-pair cases, including 128 with centers 1010), and
`20260905_boundary_word_length.json` (admissible words of lengths 20,21,23).
Each embeds its executed source and records parameters and provenance.

Hypothesis (B_all) is still unproved. Its sufficiency and the k+17 prefix bound
are conditional only. No conclusion about eventual alternation is established
without it. Eventual periods of least period >=3 are outside this argument,
so even a completed proof of (B_all) would not solve Prize Problem 1.
