# Problem 1: cyclic blind-visit spacing and a period-controlled charge

Status: LEMMA WITH PROOF — INDEPENDENTLY CHECKED at the exact quotient
scope below. Repository status: `partial-proof` relative to Prize Problem 1,
which remains OPEN. Finite checks have their own `finite-exhaustive` record.

## 1. Scope and admission

The latest pushed frontier at `7ee66c81e974106f6bd0d04607e24e2110e045ce`
proposes bounding `sum_r u_r`, where `u_r=max(k_r-1,0)` and `k_r` counts
blind phases in the normalized portal observer. Raw blind stacks can be
arbitrarily deep. This note adds the temporal cyclicity hypothesis rather
than assuming finite root-basin ancestry.

A counterexample to the propagation or cyclic spacing statement kills this
route. A proof supplies an all-period bound on the existing charge and moves
the obstruction to its transport across portal restarts/period doublings.
Neither outcome licenses larger connector enumeration.

## 2. Definitions and exact quantifiers

Fix integers `p>=1`, `r>=1`. At time `s`, let

    R_s=((X_1(s),Y_1(s)),...,(X_r(s),Y_r(s)))

be a binary stack. The two boundary pairs are fixed at every time:

    (X_-1,Y_-1)=(1,0), (X_0,Y_0)=(0,1).

For a binary label `w_s`, compute simultaneously from the OLD input pairs:

    F_j = X_(j-2) XOR (X_(j-1) OR X_j),
    D_j = Y_(j-2) XOR Y_(j-1) XOR Y_j
          XOR X_(j-1)Y_j XOR Y_(j-1)X_j XOR Y_(j-1)Y_j,
    (X_j(s+1),Y_j(s+1))=(F_j XOR w_s D_j,D_j).       (1)

This is exactly `T_w=G^w Phi_0` in
`problem1_portal_multilift_phase_quotient.md`, with dynamic layers indexed
from one. Boundaries are reinserted at each update, not evolved by (1).

A state is blind if `T_0(R)=T_1(R)`. Equivalently, all its OUTPUT
differences `D_1,...,D_r` vanish. Blindness is not the assertion that all
its input differences vanish.

For the cyclic results assume `R_(s+p)=R_s` and `w_(s+p)=w_s` for all
integer `s`. The specified `p` need not be the least period. Let `B_r`
be the set of blind phases in `{0,...,p-1}` and `k_r=|B_r|`.
No oddness, dyadic period, finite integer, or finite-support hypothesis is
required for the propagation and spacing results.

## 3. Zero-cone lemma

Suppose at time `s_0` that `Y_j(s_0)=0` for every `1<=j<=r`.
Then for EVERY choice of the initial `X` coordinates and subsequent labels,
and every integer `0<=t<=floor(r/2)`,

    Y_(2t)(s_0+t)=1,
    Y_j(s_0+t)=0 for 2t<j<=r.                       (2)

At `t=0`, the first equality is the fixed boundary value `Y_0=1`.

Proof. Induct on `t`. Given the statement at `t`, evaluate (1)
at `j=2t+2` whenever this index is at most `r`. Its previous-layer
differences are `(Y_(j-2),Y_(j-1),Y_j)=(1,0,0)`, so `D_j=1` regardless
of the `X` coordinates. At every `j>2t+2`, all three previous-layer
differences are zero, so `D_j=0`. The half-swap label changes `X` only.
This proves the induction, including the endpoint `2t=r`.
There is no assertion about the other layers `1<=j<2t`.

## 4. Blind-spacing theorem

For every depth `r>=1`, two consecutive transitions cannot both be blind.
Indeed, at the first dynamic layer (1) reduces identically to

    D_1=1 XOR X_1,
    X_1(s+1)=(1 XOR w_s)(1 XOR X_1(s)).             (3)

A blind input has `X_1(s)=1`, hence `X_1(s+1)=0` and the next output has
`D_1=1`.

If phase `s` is blind, its successor has zero differences through layer
`r`. Apply (2) at `s_0=s+1`. For each
`1<=t<=floor(r/2)`, the state at `s+1+t` has `Y_(2t)=1`. Thus the
transition at `s+t` cannot be blind.

Define

    g_r=max(2,floor(r/2)+1).

Combining these facts excludes blind transitions at every forward distance
`1,...,g_r-1` after a blind transition. This statement is local in time and
does not assume a cycle.

On a `p`-cycle, consecutive blind visits, INCLUDING the last-to-first
wraparound gap, must therefore be at least `g_r` apart. For one blind
visit the gap back to itself is `p`; when `g_r>p`, even that visit is
impossible. Consequently

    k_r <= floor(p/g_r).                           (4)

In particular `k_r=0` at every depth `r>=2p`.

The separation constant is optimal at depths one and two. The odd driver
`01` gives the two-cycles

    r=1: (0,0) --0--> (1,1) --1--> (0,0),
    r=2: (0,0,1,0) --0--> (1,1,1,1) --1--> (0,0,1,0).

In each cycle the second state is blind and the first is not. Thus each
has one blind phase per two steps. No optimality claim is made for `r>=3`.

## 5. Driver uniqueness and charge corollaries

For a realizable aligned state orbit, nonblind transitions force their
labels and blind transitions each allow one independent label bit. If the
realizing driver is known to have odd parity, the exact ambiguity dimension
is `u_r=max(k_r-1,0)`. The number of odd labelings, when `k_r>=1`, is
`2^u_r`, not `u_r`. This uses aligned period-`p` labelings with no finite-basin
restriction, as in
`problem1_blind_visit_rank_and_finite_basin_collapse.md`; restricting to
terminating leaves or exact least-period words can remove realizations.

Without ANY parity assumption, (4) already implies that the unlabeled
`p`-cyclic depth-`2p` orbit determines every driver label uniquely.

For even `p>=2`, (4) implies `k_r<=1`, and hence `u_r=0`, whenever `r>=p`.
For odd `p>=3`, the same holds whenever `r>=p-1`. For `p=1`, (3) gives
`k_r=0` already at every `r>=1`. These are sufficient bounds, not claims
of optimal depths. Odd parity uniquely reconstructs the labels when one
blind phase remains. Equality of unlabeled orbits up to rotation therefore
determines the odd driver up to that same rotation at these depths.

Let any collection have a `p`-cyclic orbit at each depth `1,...,h`, where
`h>=1` is finite. The following bound is depthwise; compatibility between
the different orbits is not needed. In particular, every compatible portal
tower of length `h` has charge obeying

    sum_(r=1..h) u_r <= U(p),
    U(1)=0,
    U(p)=2 sum_(q=1..p) floor(p/q)-4p+floor(p/2)+1
         for p>=2.                                (5)

The same bound applies if such a tower extends to every depth, since (4)
makes all summands vanish from depth `2p` onward.

To compute (5), depth one contributes at most
`max(floor(p/2)-1,0)`. For each integer `q>=2`, the two depths
`r=2q-2,2q-1` contribute at most
`2 max(floor(p/q)-1,0)`. Terms with `q>p` vanish. For `p>=2`, summing
gives (5); the case `p=1` is handled separately by (3). Since the divisor sum
is at most `p H_p`, this is `O(p log p)`.

The theorem does not assume every odd driver extends to every depth. A
finite portal may end at a zero track where the next same-period child is
impossible. The finite-length formulation covers that case.

## 6. Relationship to the remaining prize obstruction

This bound holds even WITHOUT finite root-basin ancestry.
Thus finiteness of the blind-rank charge for one fixed temporal period is
not itself a discriminator for finite support. A period-controlled bound
also does not bound total charge over infinitely many different portal
restarts or over unbounded dyadic periods.

The original global question is still whether FULL is incompatible with
one complete finite original fringe. The alternative sufficient scalar
target remains unbounded positive excess

    limsup_n [tau(2^n v)-n]=infinity, v>0 finite.

No positive contribution to that excess, no bounded reuse of original
support, no portal endpoint parity readout, and no K=3 exclusion at all
periods follows from (2)-(5) alone.

## 7. Verification and reproduction

The main agent wrote the induction, checked the precise time offsets and
cyclic wraparound, and reconstructed it a second time from the two original
Rule-30 rows. A separate Space Bunny reviewer re-derived the recurrence and
reviewed Sections 3–5. Its first report contained count/dimension confusion
and an incorrect shallow-density assertion; both were independently refuted
and the reviewer withdrew them. The accepted disposition, scope limits,
failed unrepaired `p=1` closed form, and provider failures are recorded in
`problem1_cyclic_blind_cone_review.md`. Reviewer agreement is not the proof.

Run from the repository root:

    python3 experiments/problem1_nonperiodicity/check_cyclic_blind_cone_independent.py

The primary verifier applies Rule 30 separately to the two original rows,
instead of using the polynomial `D_j` identity. It checks:

* all 10,920 raw transition/label cases through depth six against the existing
  pair implementation, with projectivity and blind nesting;
* all 5,850 zero-difference histories through depth eight, including all
  initial `X` values and all relevant future labels (27,250 observations);
* all 45,080 driver/initial-state pairs for `1<=p<=3`, `1<=r<=2p`, retaining
  61 cyclic pairs and 48 distinct aligned state orbits;
* cyclic gap/count bounds, ambiguity-cube cardinalities, the two sharpness
  controls, one explicit period-12 count/dimension review control, and the
  charge-sum arithmetic for `1<=p<=256`.

The atomic result is
`results/problem1/20261002_cyclic_blind_cone_independent.json`, with exact
parameters, full base Git commit, source hashes, payload hash, software,
hardware, timing, and limitations. These are finite checks. The all-depth
claims follow from the proofs in Sections 3–5, not from enumeration.

The original prize concerns the center column of the single-cell evolution;
see [the official problem statement](https://rule30prize.org/) and
`docs/problem_statements.md`. The observer theorem has a strictly narrower
scope and leaves that prize question unresolved.
