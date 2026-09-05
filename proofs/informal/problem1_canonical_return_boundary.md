# Canonical return triples and a finite critical boundary window

Status: `partial-proof`, exact all-depth word-language reductions with
independent adversarial proof review. Finite verification is separately
labelled below. Neither B_all nor signed nonvanishing has been proved.

## Strategy and admission

The valuation route is closed by counterexamples. The remaining boundary
obligation quantifies over all occurrence cuts, including L>=k. This pass
asks whether that unbounded cut quantifier and the 56 triple labels can be
reduced exactly before attempting a structural frontier argument.

Route ranking (`heuristic`):

| Rank | Route | Plausibility / all-depth potential | Falsifiability / testability | Cost |
| --- | --- | --- | --- | --- |
| 1 | Canonicalize the invisible final return and localize boundary cuts | High for an exact reduction / reduces an all-depth obligation | High / high | Low |
| 2 | Prove exclusion on the resulting critical frontier cylinders | Unknown / high for eventual alternation | High for an explicit invariant / medium | High |
| 3 | Control signed joint fibers across complete returns | Unknown / high | Medium until a structural invariant is specified | High |

Candidate A: because the final u need only be admissible, any occurrence with
g=(r0,r1,r2) also occurs at the SAME state and cut with (r0,r1,2). This reduces
the relevant triples from 56 to the 15 choices with r2=2 and (r0,r1)!=(2,3).
The underlying belief and its signed mass depend on state and cut, not g.

Candidate B: any occurrence at cut c>=b can be replaced by an occurrence at
c0 in {b,...,b+4}, with canonical last gap 2, requiring at most b+16 observed
branches. With b=k-2, the full boundary condition is equivalent to excluding
these five offsets using only the first k+14 branches. This argument must
cover finite, infinite, or eventually inadmissible forced schedules.

Candidate C: every admissible observed word of length b+16 contains such an
occurrence at cut >=b. Thus B_all would imply that no frontier state at
complexity k has an admissible forced prefix of length k+14. This is a
conditional consequence, not an established termination bound for Rule 30.

Admitted checks: independent word-language enumeration on fixed short words,
with final u treated as unobserved; hand boundary words; and canonical-label
comparison on the already existing 19 full-domain rows through complexity 16.
No frontier census, cap increase, or first-prefix-witness search. Both outcomes
change the proof architecture: a counterexample corrects the quantifiers or
indexing; a surviving derivation reduces the all-depth proof to explicit
families. Every nontrivial run records its exact finite set and atomic
provenance. One local CPU, 120 seconds, 1 GiB per check.

## Exact definitions

Let Sigma be any finite or infinite word over {t,u}. It need not be globally
admissible. A word is admissible if it avoids uu, ttttt, and ututtu. An
occurrence at cut c has Sigma beginning wE(g), |w|=c, where

```text
E(g)=u t^(r0-1) u t^(r1-1) u t^(r2-1),  ri in {2,3,4,5},
```

and wE(g)u is admissible. The appended u need not occur in Sigma. This is
the exact original adjacent-shadow occurrence convention, with no L<k
restriction. The low-cylinder depth is L=c+1.

## 1. Canonical third gap (`partial-proof`)

**Lemma.** Fix any Sigma, cut c, and triple g witnessing an occurrence.
There is an occurrence at the same cut in the same Sigma with
`g'=(r0,r1,2)`.

Proof. Let p be the position of the third u in the observed wE(g). Since
r2>=2, the t at p+1 is also observed. Retain just the prefix through that t,
and append u at p+2. The retained prefix is admissible because it is a prefix
of wE(g)u. Any newly created forbidden word must end at the appended u.
It cannot be uu because the preceding symbol is t. It cannot be ttttt,
which ends in t. It cannot be ututtu: the last two u's in that forbidden
word have distance 3, whereas the new last two u's have distance 2. Thus
the appended word is admissible. Its observed portion is precisely wE(g').
No symbol already required to occur in Sigma was changed. This proves the lemma.

Of the 16 pairs (r0,r1) in {2,3,4,5}^2, exactly (2,3) creates ututtu between
the first three u's. Fixing r2=2 introduces no further forbidden pair. Thus
there are 15 canonical triples. The converse inclusion is immediate because
these 15 are among the original 56. For every Sigma, their sets of occurrence
CUTS are identical. This is not equality of the sets of labeled triples.

For the phase-frontier language, write T^can_(a,k) using just those 15 triples.
Then, at every phase and complexity,

```text
T^can_(a,k) = T_(a,k).
```

For each witnessing x the base prefix w and depth L=c+1 are unchanged.
Therefore the set of base cylinders, its ancestor closure, its dominant
beliefs, and its signed masses are unchanged by this canonicalization.
Any assertion depending only on these objects can use the 15 triples.
The actual moving fringe still has its original return gaps: this lemma
shortens an admissibility label, not an observed physical return time.
The argument uses exactly the three stated forbidden factors. Adding a
stronger admissibility test would require checking canonicalization again.

## 2. Exact prefix criterion (`partial-proof`)

Let A be the longest admissible prefix of Sigma, possibly infinite. Fix
an integer b>=0. Let p be the position of the third u in A at or after b,
if it exists. Then

```text
An occurrence exists at some cut c>=b
iff p exists and p+1 < length(A).
```

Proof of the forward direction. In an occurrence at c>=b, three actual u's
and the t following the third are observed in an admissible prefix of Sigma.
Consequently they belong to A. Its earliest three u's at or after b appear
no later than those three occurrence u's. The t after the earliest third u
is still inside that observed prefix, so p+1<length(A).

For the reverse direction, let c0 be the first u at or after b in A. Its next
two u's give the first two gaps, which lie in {2,3,4,5} because A avoids uu
and ttttt. The following observed symbol is t because A avoids uu. Append u
after this t; the argument of Section 1 proves admissibility. This is an
occurrence at c0 with last gap 2. Only A is used: Sigma may have a forbidden
factor later or may terminate. Global admissibility is not assumed.

## 3. Critical-cut localization (`partial-proof`)

**Theorem.** For every Sigma and b>=0, an occurrence at any cut c>=b exists
if and only if a canonical occurrence exists with

```text
b <= c0 <= b+4,
observed prefix length <= b+16.
```

Proof. The reverse direction is immediate. For the forward direction, use
Section 2 and select the first three u's in A at or after b. The first lies
at c0<=b+4: otherwise five t's would occur inside A before it. The next two
gaps are at most 5, so the third u is at position at most b+14. The canonical
observed word ends with its following t, hence has length at most b+16.
Section 2 ensures this t is observed even if the original final u was not.
This proves the assertion, without assuming that Sigma halts.

Equivalently, the truth of "there is an occurrence at some cut >=b" is
completely determined by the first b+16 symbols of Sigma (or the whole word
if shorter). Once b+16 symbols have been observed, later continuations cannot
change a negative verdict, because any later violation would already have a
localized witness in that prefix. A word ending before the horizon is
evaluated as terminated; extending that shorter word is a different input
and may create an occurrence.

## 4. Application to B_all

For x in O_(a,k), k>=2, let Sigma=sigma(x) and put b=k-2. The full boundary
condition at this x is equivalent to absence of the canonical occurrences at

```text
c=k-2+j,  j in {0,1,2,3,4},
g=(r0,r1,2),  (r0,r1) in {2,3,4,5}^2 except (2,3).
```

Only the first k+14 actual forced branches are needed. If the schedule stops
earlier, its whole finite word suffices. Reaching this horizon is not a
truncation that leaves this PARTICULAR boundary predicate unresolved.

There are five possible depths,

```text
L=c+1 in {k-1,k,k+1,k+2,k+3}.
```

The first lies in the old restricted signed domain L<k; the remaining four
are excluded from it. Together these five moving boundary depths suffice for
the full all-cuts obligation. No larger depths can introduce a new violation
without producing one in this window. All offsets refer to the STARTING
complexity k of x, not the changing complexity after forced iterations.

Thus B_all is exactly a family of exclusions indexed by phase, k, the five
cut offsets, and the 15 canonical triples. The universal quantifier over k
is still open. This is a finite-horizon predicate for each finite input, not
a finite verification of all k and not a proof of B_all.

Changing only the last gap preserves a signed certificate. Moving the cut
does NOT preserve its depth or signed mass. The localization theorem therefore
does not reduce signed-cancellation tests to these five cuts. It reduces
boundary-occurrence existence, which is the separate obstruction to inclusion.

## 5. Sharper conditional prefix bound

**Lemma.** Every admissible word of length b+16 has an occurrence at a cut
>=b. Indeed its first u at or after b lies by b+4, its second by b+9, and
its third by b+14. The following symbol exists and is t, so Section 2 applies.

Consequently, under B_all, no phase-frontier state at complexity k>=2 has an
admissible forced prefix of length k+14. Its maximum such prefix length is
at most k+13. This sharpens the earlier sufficient k+17 upper bound, which
remains valid but was not asserted sharp. It bounds admissible prefixes;
it does not assert termination of a schedule that later becomes inadmissible.

For abstract admissible words, the constant 16 is necessary: at b=0,
`ttttu` repeated three times has length 15 and no occurrence, since its
third u has no observed following t. Appending one t creates the canonical
occurrence at cut 4 with gaps (5,5,2). Each of the five offsets is necessary
in the abstract word class: for j=0,...,4, the admissible word
`t^j u t^4 u t^4 u t` has exactly three u's and its only possible cut is j.
No sharpness assertion is made for phase frontiers at k=2 or any other k.

Combined with the existing physical-row bridge, B_all would still exclude
all eventually alternating traces from odd positive finite seeds. This
conditional implication does not address eventual periods of least period >=3.

## Verification and limitations

The fixed-record check maps all 19 old full-domain labels through k=16 to
17 canonical representatives, preserving every base cylinder, signed mass,
endpoint count, and defect histogram. The two changed labels are (2,4,3)
to (2,4,2) at p/k15/0x37b38787/cut0, and (2,2,4) to (2,2,2) at
u/k15/0x1bd90387/cut0. Historical occurrence-label counts are not errors;
the theorem identifies their redundancy for cylinder-based assertions.
The atomic record is `results/problem1/20260905_canonical_return_rows.json`,
which embeds the 19 source rows and the executed comparison source.

The separate literal-motif versus prefix-position check exhausts all 25,208
admissible words of lengths 0 through 22 and all 8,191 binary words of lengths
0 through 12, with thresholds b=0,...,6: 233,793 threshold checks, with no
discrepancy. It tests equality of canonical and original cut sets, the prefix
criterion, five-cut localization, and the b+16 observation horizon. Hand
cases cover the invisible final u, a terminal third u, and all five offsets.
These are `finite-exhaustive` statements on the declared word sets only.
The lead executed this comparison after taking over the unfinished Muse
enumeration; it is not a completed Muse experiment. Source, exact counts,
resource limits, timings, and hashes are embedded in the atomic record
`results/problem1/20260905_canonical_return_words.json`.

The general proofs above use the forbidden-word definitions and exact
prefix inclusions. They do not extrapolate from the rows or word checks.
Independent adversarial review by Dewey (agent
`01a0721c-027e-71e0-8cbc-b86d859d4b64`, default reviewer) accepted the proofs
in Sections 1–5 under the original source Section 2 occurrence convention.
The reviewer independently flagged the shorter-word extension caveat now
explicit in Section 3: `ututu` has no occurrence, but `ututut` does. The
lead had made the same qualification before receiving the review. This
correction concerns wording, not the theorem for a fixed finite or infinite
Sigma. No claim of stability before the full horizon is intended.

Two Muse Spark 1.3 Contributor review attempts terminated with provider
HTTP 429. They supplied no completed independent check for this result.
The fallback reviewer performed a proof review, not a computational run.
Its scope covered the word lemmas and their algebraic B_all substitution;
external signed-belief definitions and the physical bridge were outside
that review. The lead checked the former in
`problem1_period_two_three_return_signed_mass.md`; the latter remains the
separately established dependency in
`problem1_three_return_boundary_sufficiency.md`. Both reductions preserve
these proof boundaries and leave B_all itself open.
