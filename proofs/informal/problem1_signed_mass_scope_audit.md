# Signed-mass scope audit and adjacent-level separation

Status: `partial-proof` for the separation argument below, pending fresh
independent review. The three-return signed-nonvanishing conjecture and
Problem 1 remain `inconclusive`.

Later addition (2026-09-05):
`problem1_cyclic_seed_boundary.md` proves stronger empty layers for
DOMINANT beliefs: both phases L=k-2,k>=3; phase p L=k-3,k>=5; phase u
L=k-3,k>=6, and larger depths by monotonicity. This does not improve the
raw adjacent-level separation theorem below or prove any occurrence bound.
In particular B_all retains its original meaning L=c+1<=k-2. A dominant
or signed certificate would additionally require L<=k-4 for k>=6.

## Source boundary and admission

This pass starts at `b54f067210d5d8eeb1af3247c858c97af456497c`.
`docs/research_status.md` and `docs/adversarial_review.md` are historical
summaries; recent Git history and the phase-frontier proof notes describe the
current boundary. The signed-belief derivative census concerns phase `u` and
return triple `(2,2,2)`. The adjacent-shadow sufficient condition quantifies
over both phases and all admissible three-return triples.

The new falsification question is whether the same signed certificate works
on that enlarged return domain, without increasing the old complexity cap.
For `a in {p,u}`, `k>=2`, `x in O_(a,k)`, a cut `c>=0`, and a gap triple
`g in {2,3,4,5}^3`, require that the exact forced zero schedule of `x` begins
`w E(g)`, where `|w|=c` and

    E(g)=u t^(g_0-1) u t^(g_1-1) u t^(g_2-1).

Require that `w E(g) u` avoids `uu`, `ttttt`, and `ututtu`. The appended `u`
is an admissibility test, not an additional observed branch. At depth
`L=c+1<k`, form the concrete dominant adjacent-shadow belief. Each DISTINCT
endpoint contributes `(-1)^d`, with `d` the number of its nonfull fibers over
all `L` common low digits. Generator representations are not counted.

Conjecture (`inconclusive`): this signed sum never vanishes on the stated
domain. Its implication to nonemptiness is sufficient, not necessary.

Outcome gate, fixed before the new run:

- A cancellation refutes this unified certificate. It does not refute concrete
  nonemptiness, the adjacent-shadow inclusion, or center nonperiodicity.
- Absence through the finite cap supports only the tested instances. The next
  step would be an all-depth counting argument, not a larger census.

The cap is complexity 16, both phases, schedule cap 64, ordered by complexity,
phase (`p` first), integer state, cut, and lexicographic triple; stop at the
first cancellation or exhaustion. One local CPU process per independent run,
120 seconds and 1 GiB address space. The independent run verifies the new
observable, not an extension of the scientific search bounds. Truncation and
excluded depths must be reported rather than silently counted as successes.
The pre-existing untracked three-return proposal is preserved, not adopted as
an established result.

## All-depth separation lemma

Claim status: `partial-proof`. Assume the phase-frontier definitions and
projection theorem in `problem1_period_two_phase_frontier_projection.md`.
For every phase `a`, every `k>=2`, and every

    x in O_(a,k), y in O_(a,k-1),

one has

    x != y (mod 4^(k-1)).

Proof. Suppose the residues were equal. Their digit at position `k-2`,
counting the low digit as position zero, would be equal. Repeated projection
gives

    x >> (2(k-2)) in O_(a,2),
    y >> (2(k-2)) in O_(a,1).

The exact base cases are

    O_(p,1)={3}, O_(p,2)={12,13};
    O_(u,1)={1}, O_(u,2)={6,7}.

For phase `p`, the current digit is in `{0,1}` whereas the shadow digit is
`3`. For phase `u`, the current digit is in `{2,3}` whereas the shadow digit
is `1`. Both contradict equality. This proves the lemma for every `k`,
including `k=2`. Equality modulo a larger power implies equality modulo
`4^(k-1)`, so no adjacent shadow exists at any depth `L>=k-1` either.

The two base cases were recalculated directly with the Boolean generators;
the calculation is only a check of the displayed base cases. The all-depth
conclusion comes from the projection theorem and the argument above.

## Consequence for the proof architecture

Claim status: `partial-proof` (conditional implication).
Any three-return occurrence with `c+1>=k-1` would refute the adjacent-shadow
inclusion itself, not merely its dominant or signed strengthening. Therefore
an all-depth proof via that inclusion must establish a depth bound
`c+1<=k-2` for every occurrence, or otherwise rule out all boundary cases.
A finite census having no such cases does not establish this bound.

The proposed signed domain `L<k` still includes `L=k-1`; the separation
lemma shows that any occurrence there has empty belief and zero signed mass.
Occurrences with `L>=k` are outside that proposed domain but remain relevant
to the original inclusion. Thus even a proof of the restricted signed
conjecture would require a separate treatment of the excluded depths before
proving the full three-return statement.

There is a corresponding helper-API boundary: the existing weighted direct
mask routine rejects fiber levels below one, while the recursive formula
syntactically permits a level-zero fiber. At the singleton boundary the
ordinary five-mask theorem is not the appropriate alphabet. However, the
separation lemma shows that for valid frontier inputs the same-residue filter
has already removed every candidate before such a shadow fiber is inspected.
This is not a demonstrated disagreement between the existing valid-input
belief routines. A new check may either enumerate that empty residue set or
return the empty belief using the lemma, with explicit boundary tests. No
historical analyzer needs modification on this account.

## What the local derivative does and does not give

Claim status: `partial-proof` (elementary identities).
Writing `epsilon_m(n)` for the signed containment factor, the identity

    P(-1) = sum_y product_j epsilon_(m_j)(n_j(y))

is exactly the definition of the signed concrete belief mass. The missing-
sibling formulas re-express its local factors; they do not make the signed
sum invariant or prove it nonzero. A sign-reversing involution would still
need an unpaired endpoint on the admissible domain. Negative mass is not a
counterexample; zero mass with a nonempty belief is.

Do not return to the already-refuted mask-only or fixed modular endpoint
quotients without a new realization-consistency theorem. Do not infer
nonemptiness from an abstract path formed by splicing different endpoints.
Even a completed adjacent-shadow theorem would need the existing reduction
and its actual-orbit hypotheses checked before claiming anything about the
whole-tail conjecture, especially eventual temporal transients.

## Execution and fresh review

Pending independently verified worker artifacts. No infinite nonperiodicity
claim is made. Finite evidence is not an infinite proof.
