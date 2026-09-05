# Dependency audit: three-return inclusion to Problem 1 (final)

Status: read-only audit plus three tiny replays (sections 7-9). Derivations
marked `partial-proof` were independently derived by Muse Spark 1.3 Contributor
and reviewed by the lead; all other statuses quote cited sections. Nothing
here is `rigorous-proof`. Problem 1 is open.

Lead clarification after adversarial review: the boundary hypothesis in this
audit is `B_all` from `problem1_three_return_boundary_sufficiency.md`, over
ALL cuts c>=0 in the original adjacent-inclusion domain. Restricting it to
the signed conjecture's `L=c+1<k` domain would invalidate the late-cut argument.

## 1. Claimed chain under audit

Handoff pathway: eventual period two implies three consecutive returns carry
positive phase penalty, via adjacent inclusion, via nonempty belief, via
signed-mass nonvanishing, via slice induction. The prize needs eventual
periodicity of any period excluded for the single seed.

## 2. Valid implications with exact sources

E1 (`problem1_period_two_three_return_adjacent_shadows.md`, section 3). For all
a, k >= 2: a three-return zero-penalty plateau from base prefix w with kappa(w)
= k implies T(a,k) NOT SUBSET P(a,k-1). Inclusion therefore implies every three
consecutive returns carry positive penalty. That note records inclusion as
strictly stronger than necessary.

E2 (`partial-proof`, derived here). Nonnegative consecutive penalties d_j along
any return sequence: if every three consecutive contain a positive one, disjoint
three-windows give kappa(L_J) >= kappa(L_J0) + floor((J-J0)/3). The cited
two-return criterion instead needs no two consecutive zeros; three-return
positivity does not supply that antecedent (the k=25 state has two consecutive
zeros with Delta = 0). Divergence goes through the three-window form.

E3 (`partial-proof`, per `problem1_period_two_witness_complexity.md`, sections
1-3). Bounded kappa in L iff one finite word kills the full future boundary
(nested finite-set intersection, exact); that note identifies this with an
ordinary finite phase-a zero survivor via its dual-cut and fixed-phase theorems.
The survivor-to-killing-word correspondence is quoted, not re-verified, so the
divergence-to-no-survivor step stays conditional on it. The kappa line (E2-E3)
is bypassed, not refuted, by the seam bridge below.

E4 (exact one-way, scope audit and belief-derivative note). Nonzero signed mass
implies nonempty belief; converse false. Nonvanishing plus the boundary bound
gives inclusion; the boundary bound is open.

E5 (exact, `problem1_whole_tail_equivalence.md`). The uniform statement over all
odd positive S (no eventually periodic diagonal, any period, transient allowed)
implies the single-seed prize.

## 3. Transient handling via the general prefix (no invented gaps)

The time-shift lemma (pure-for-all-finite-seeds implies eventual) is correct but
bypassed: the prefix route keeps the ORIGINAL right-zero seed throughout, so no
seed-class shift occurs. Verified generalities: dual-cut Theorems 1-2 quantify
over arbitrary past G and future q (sections 2-5), so schedule-universal claims
cover the tail schedule; fringe exclusions hold for EVERY fringe state A under
pure center by complete exhaustion, restartable each block (fringe-language
sections 1-5), hence from the seam on; sections section-3 recurrence sends any
finite temporal prefix to finite H. Distinct: (a) finite past WORD strip is not
(b) temporal preperiod; the same recurrence gives finiteness in both.

H membership, correct direction (`partial-proof` here). Lowercase t,p,u are
inverse maps, so finite H gives H^{-1}(0) through FORWARD T/P/U on 0:
automatically ordinary nonnegative. Stripping leading t (T fixes 0), the first
non-t letter gives P(0) = 3 or U(0) = 1, landing H^{-1}(0) in O(a,k) by
construction. All-t H cannot emit 00 (trivial root fixes low bit 1).

Unconditional sharpening (`partial-proof` by hand, corroborated `finite-
exhaustive` on 508 rows in results/problem1/20260905_boundary_frontier_membership.json). For ANY positive S with
s = bitlen(S) and n >= s, X = T^n(S)>>n has bitlen s+n by the degree law and
lies in O(a,k) with a = p iff s+n even, k = ceil((s+n)/2) -- no alternation
needed for membership. The n >= s requirement is load-bearing (initial input
high part 0); nothing is claimed for n < s. Per block (two steps) k rises by 1
at constant phase.

## 4. Seam verification: semirows, branch ID, and non-stopping

All identities below were derived by hand (`partial-proof`) and cross-checked
against an independent cell array (complete 512-case box, results/problem1/20260905_boundary_half_row_identity.json, `finite-exhaustive`). With center 1 at even time n and X the
center-plus-left integer: first semirow X1 = (X>>1) XOR (X OR (X<<1)) = P(X>>1)
(bit 0 uses center 1 masking the unknown right neighbor); with X = 4z+3 and
P(2z+1) = 2P(z), X1 = 2P(z), center 0. With b = odd-time right neighbor =
NOT(old pair OR), second semirow X2 = T(X1>>1) XOR b = Q(P(z)), Q = U iff b = 1
else T. Hence X_{m+1} = Q_m P(X_m>>2), exactly the renewal normalized recurrence,
with taken branch = fringe branch (Q = U iff even pair 00) for ANY finite
prefix. Fringe all-A admissibility therefore attaches to the tail with no
pure-initial-zero assumption.

Non-stopping (`partial-proof` by hand, corroborated by zero stops among 128
1010-center cases in the 512-box). Exact bit conditions, no free step: from X = 4z+3 and X2 = T(P(z)) XOR b,
bit0(X2) = 1 XOR bit2(X) XOR b, so c_{n+2} = 1 imposes bit2(X) = b (e.g. X = 3
with right pair 00 gives b = 1 and c_2 = 0). Given c_{n+2} = 1, c_{n+3} =
(bit3 XOR b) XOR 1, so c_{n+3} = 0 imposes bit3(X) = 1-b. Together X lies in
{7,11} mod 16 with taken = forced branch. Under persistent alternation every
even time meets both conditions, giving infinite admissible sigma; stop class
forces a break by step 3 (minimal exhibit X = 3 with right pair (1,0) runs
c = 1,0,1,1). Taken-vs-forced is therefore no gap.

Seam-time branch identification verified: q(W) = u iff schedule head is T iff
top section bits are 00 iff the physical even-time pair is 00 (edge frame), for
arbitrary prefix; even alignment costs at most one shift and tail phase selects
the block framing, both checked in the box setup (n >= 2). No pending item
remains on the seam; conditional premises are exactly the boundary bound (open),
the bypassed E3 correspondence, and F2 periods >= 3.

## 5. Handoff wording jump (recalibrated, standing results kept)

As logic, `penalties -> inclusion` asserts the converse of E1 and is unproved;
only inclusion-implies-penalties holds. As obligation ordering it is defensible
but incomplete: it omits E2 (three-window form), the E3 correspondence condition,
the seam bridge with its explicit premises, and F2 below. E1-E5 stand within
their stated classes. F2 (periods >= 3): all return objects are period-two-
specific; no note supplies any route there, so a completed period-two path still
leaves the any-period quantifier undischarged.

## 6. Dependency graph

```text
SliceInduction --open--> Nonvanishing --E4--> NonemptyBelief
  --def--> Inclusion[open; boundary open] --E1--> ThreeReturnPenalties.
Boundary bound --Lemma A--> NoInfiniteAdmissibleSigma(x), x in O(a,k).
EventualAlternation(original S) --seam(X in O, sigma infinite admissible)-->
  contradiction with Lemma A. Hence: universal bound ALONE excludes eventual
  alternation for all odd positive S, transients included, no time-shift.
Kappa line E2-E3 bypassed (alternative, needs correspondence).
Periods >= 3: no route. UniformAnyPeriod --E5--> SingleSeed.
```

## 7. Separate task: independent orthant-vector replay (pass)

Admission: recompute the one named belief and fiber grouping with the
pre-existing independent oracle only, never the new lead script; a mismatch
would be reported as a correction. Caps: k <= 14 frontiers, one belief, one
witness, 120 s, 1 GiB, /tmp only. Provenance: results/problem1/20260905_signed_slice_orthants_independent.json,
self-contained, `finite-exhaustive`. Expected values compared against the lead
orthants record.

Result: pass. Word uuuuputptutpuu replays to 0x642fdfb (k=14); strip suffix 3
gives 0x190bf7e; schedule tutututu with gap-222 window at cut 1 and clean
final-u word verified. Belief (u,13,L1) identical by direct and recursive
implementations: 357 endpoints, bins (101,41),(0,0),(72,0),(0,9),(84,50),
vector (60,0,72,-9,34), mass 157. Exact counterexample to the sign-coherent
cone-union proposal only; belief nonempty and mass nonzero, so nonvanishing
is untouched.

## 8. Separate task: boundary standalone lemma (pass, sharpness restated)

Admission: verify that the boundary bound alone kills infinite admissible forced
schedules, checking off-by-ones and admissibility; a failure would be reported
as a correction. No frontier census; tiny word enumeration only. Provenance:
results/problem1/20260905_boundary_word_length.json, `finite-exhaustive` over enumerated lengths.

Lemma A valid (`partial-proof`, hand derivation checked here). Under c+1 <= k-2
for every occurrence, an infinite schedule avoiding uu, ttttt, ututtu has
unbounded u-positions with gaps 2..5; any u-position c >= k-2 with its next
three actual gaps and real fourth u forms wE(g)u with |w| = c, an occurrence
violating the bound. Uses none of inclusion, nonvanishing, kappa, separation;
conversely inclusion plus separation gives the bound.

Finite consequence (off-by-ones checked): no admissible forced prefix reaches
length k+18, since positions k-2..k+2 contain a u at c and c+B+1 <= k+18; prefix
global admissibility is required and assumed. Sharpness is claimed ONLY for the
four-observed-u structure (worst need exactly k+18, e.g. ttttuttttuttttuttttu
at k = 2): an occurrence needs merely an admissible appended final u, so k+18
as occurrence threshold is sufficient, sharpness not claimed there.


## 9. Final adversarial review of the explicit all-cuts hypothesis

Status: independent proof review by a second Muse contributor, reviewed and
integrated by the lead. The reviewer initially read the boundary hypothesis
as restricted to L<k and objected to extracting occurrences at later cuts.
That objection correctly identifies a failure of the restricted argument.
The final proof now defines B_all explicitly over every c>=0. The reviewer
checked the original adjacent-shadow language definition and the scope audit:
both require treatment of all cuts, including L>=k. Under that hypothesis,
the late-cut contradiction and conditional k+17 prefix bound are valid.

The final review also accepted the displayed section chain rule and action
order, the forward P formula, the shifted half-row identity and its evenness
step, and application of each forbidden finite window within the alternating
tail. These close the exposition concerns for the unconditional membership
and temporal-transient bridge. The proof does not establish B_all, does not
infer it from the restricted signed conjecture, and does not address least
periods >=3. The implication from full inclusion to B_all retains the cited
separation lemma's partial-proof and projection-theorem premises.
