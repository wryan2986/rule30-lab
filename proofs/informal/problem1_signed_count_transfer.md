# Exact parity-count transfer and the valuation induction obligation

Status: `partial-proof` for the all-depth count identities below.
Subsequent update: the valuation invariant on genuine occurrences and
ancestors is `refuted`; see `problem1_return_valuation_falsification.md`.
The identities and universal nonclosure counterexamples here remain valid.

## Admission and scope

The valuation note proposes `v2(N)!=v2(2O)`, where N counts distinct endpoints
and O counts endpoints with odd defect. Its success on the 25 existing
ancestors and two named nodes is finite evidence. This pass asks whether
the inequality is preserved by an ordinary one-digit lift without additional
return-context hypotheses.

Muse will search the already verified universal cylinder box: parent
complexity `3<=h<=9`, both phases, `1<=D<=h-2`, q in the parent frontier,
and each digit d whose current child exists. Order by h, phase p then u,
D, q, d; stop at the first passing parent and failing NONEMPTY child.
Compare direct and recursive beliefs and verify the displayed count identity.
Use a local CPU, 120 seconds, 1 GiB, and atomic source-embedded provenance.
No larger census and no inference that a generic cylinder is an admissible
three-return ancestor are allowed.

A failure refutes the unrestricted induction premise; it does not refute the
restricted conjecture. No failure in this box would justify only further
structural analysis, not a search-cap increase.

## Exact one-lift formula (`partial-proof`)

Use the parent and child definitions from the joint-transfer note:

```text
parent P=(a,h,D,q), child C=(a,h+1,D+1,4q+d),
h>=3, 1<=D<=h-2, q in O_(a,h), 4q+d in O_(a,h+1).
```

Put `m=M_(a,h)(q)`, which contains d and hence is nonempty. For each outgoing
shadow mask n in `(0000,0011,1011,1100,1111)`, let E_n and O_n count the
parent's distinct even- and odd-defect endpoints with that outgoing mask.
Let `A_m={n : m subset n}`; the full mask 1111 belongs to A_m.

Then the exact child totals are

```text
E(C)=E_1111 + sum_(n in A_m, n!=1111) O_n,
O(C)=O_1111 + sum_(n in A_m, n!=1111) E_n,
N(C)=sum_(n in A_m) (E_n+O_n).
```

Proof. A parent endpoint survives exactly when its outgoing mask contains m.
Since d belongs to m, the child endpoint `4p+d` then exists automatically.
This assignment is injective and accounts for every dominant child shadow.
A full fiber contributes zero new defect and preserves parity; a proper
surviving fiber contributes one and swaps parity. Counting these two cases
gives the formulas. No sign cancellation or endpoint multiplicity is hidden.

In particular the ten parent parity counts and m DO determine the next E,O
totals, independently of which d in m is used. They do not thereby determine
the child's ten outgoing counts, which require joint endpoint correlations.
Thus this formula is a scalar count update, not a closed vector recurrence.

If `H_n(z)=sum z^cost(p)` over the parent endpoints in mask n, the same
argument yields the generating-polynomial identity

```text
H_C(z)=H_1111(z) + z sum_(n in A_m, n!=1111) H_n(z).
```

Evaluating at 1 and -1 gives N(C) and S(C). Equivalently,

```text
S(C)=(E_1111-O_1111)
     - sum_(n in A_m, n!=1111) (E_n-O_n).
```

This recovers the signed-slice hyperplane exactly. The valuation proposal
requires an arithmetic restriction on these selected subtotals; the parent
inequality alone supplies no such restriction by this derivation.

## Unrestricted valuation preservation is refuted

Status: `refuted` for the universal one-lift assertion. The first failure in
the specified finite order has phase p, parent h=5, D=1, q=`0x321`, digit
0, current outgoing mask m=`0011`, and child `0xc84` at k=6, L=2.

The entire concrete endpoint tables are:

| Cylinder | Endpoint | Defect cost | Outgoing mask |
| --- | --- | --- | --- |
| Parent | `0xc9` | 0 | 1011 |
| Parent | `0xdd` | 0 | 1111 |
| Child | `0x324` | 1 | 1011 |
| Child | `0x374` | 0 | 0000 |

The parent has E=2, O=0, N=2: `v2(N)=1 != infinity=v2(2O)`.
Both endpoints survive m=0011. The proper-mask endpoint gains one defect;
the full-mask endpoint gains none. The child therefore has E=1, O=1, N=2,
S=0, with `v2(N)=v2(2O)=1`. Its outgoing empty mask does not remove an
endpoint already present; that mask concerns a possible later lift.

Thus a parent satisfying the valuation gate can lift to a nonempty child
that cancels exactly. O=0 is allowed by the stated convention and does not
make the parent inequality vacuous. No admissible-ancestor status is claimed
for these cylinders. In particular the child's low digit is not 3.

The stopped search checked 101 ordinary transitions and 202 direct/recursive
belief comparisons with exact agreement, plus the seven elementary arithmetic
checks described in the embedded source. This is smallest only in the
specified ordinary-transition order. It does not locate a counterexample on
the restricted admissible three-return domain.

Lead review caught and rejected an earlier false positive: the worker had
passed E in place of N=E+O to the valuation function. Its purported E=2,O=1
child actually satisfies the gate. The corrected run, arithmetic self-checks,
and independently reviewed endpoint tables supply the present result. The
rejected output is not evidence for any mathematical claim.

## Ten parity counts do not close (`partial-proof`)

Adding unsigned counts to the five signed slices does not repair universal
vector closure. The exact concrete tables already proved in
`problem1_signed_slice_joint_transfer.md` give the following collision;
Muse independently rechecked the endpoint costs and outgoing masks.

All vectors below use mask order `(0000,0011,1011,1100,1111)`:

| Quantity | First transition | Second transition |
| --- | --- | --- |
| Parent (phase p, h=6, D=1) | `0xc82` | `0xc88` |
| Parent E vector | (2,0,0,0,1) | (2,0,0,0,1) |
| Parent O vector | (0,0,0,0,0) | (0,0,0,0,0) |
| Adjoined digit / current mask | 0 / 1011 | 0 / 1011 |
| Child (phase p, k=7, L=2) | `0x3208` | `0x3220` |
| Child E vector | (0,0,1,0,0) | (0,0,0,0,1) |
| Child O vector | (0,0,0,0,0) | (0,0,0,0,0) |

Each parent has three even-defect endpoints. Its sole full-fiber endpoint
survives the lift with cost zero. The first surviving child's outgoing mask
is 1011; the second's is 1111. Thus identical phase, complexity, depth,
digit, current mask, and ten parity counts give different child ten-count
vectors. No universal deterministic update on this information can exist.
The proof uses concrete endpoint tables, not a dimension-count heuristic.

The scalar total update survives: both children have E=1, O=0. On a second
common digit-zero lift with common current mask 1011, their totals become
(E,O)=(0,1) and (1,0), respectively. Consequently the original ten counts
do not determine two-lift E,O totals even when both digits and current masks
are specified. The joint correlations still matter.

These are generic ordinary cylinders; neither parent is asserted to belong
to the admissible three-return ancestor domain. A restricted closure theorem
or a multivalued update with additional arithmetic constraints is not refuted.

## Remaining quantifier

Even a universal counterexample leaves the actual three-return ancestor
conjecture open. Its proof would need a property retained along the genuine
ancestry, including how outgoing parity subtotals are regrouped after each
lift. The additional all-cuts boundary obligation B_all remains separate.

The final source-embedded atomic record is
`results/problem1/20260905_signed_count_transfer.json`. It records the
corrected search, exact counterexample tables, and the two ten-count
collision cases, with full provenance. The lead additionally replays the
named beliefs using the pre-existing independent signed-mass oracle before
integration; exact agreement is recorded in
`results/problem1/20260905_signed_count_transfer_independent.json`.
Final independent adversarial review accepted the count identities and
the stated scope of the two universal obstructions. This pass did not
refute the restricted three-return valuation conjecture; the subsequent
return-domain replay cited above does, with nonzero signed masses.

The old complexity-28 signed-mass archive contains summary counts and a
minimum witness, not the per-cylinder (N,O) pairs. Those summaries cannot
test this stronger valuation conjecture. No new census was launched to
fill that gap.
