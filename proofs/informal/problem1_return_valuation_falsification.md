# Valuation falsification on genuine return ancestors

Status: `refuted` for both the occurrence-only and ancestor valuation
conjectures, by independently verified finite counterexamples. Signed
nonvanishing, adjacent inclusion, B_all, and Problem 1 remain `inconclusive`.

## Bottleneck and route selection

The previous count-transfer pass proved an exact update for even and odd
endpoint totals but refuted its unrestricted preservation of
`v2(N)!=v2(2O)`. That generic failure does not settle the proposed invariant
on ancestors of admissible three-return cylinders. Before a long proof
attempt, this stronger finite consequence needs a test on a domain larger
than the 25 old ancestors plus two selected nodes, without enlarging the
repository's historically studied phase-u gap-222 box.

Ranked routes (`heuristic` judgments, not mathematical conclusions):

| Rank | Route | Plausibility / all-depth potential | Falsifiability / testability | Cost |
| --- | --- | --- | --- | --- |
| 1 | Valuation invariant on genuine return ancestors | Medium / high if return-conditioned preservation can be proved | High / high | Low falsification cost, high proof cost |
| 2 | Bound all admissible occurrence cuts at each complexity | Medium / high for eventual alternation | High for a proposed bound / medium | High structural cost |
| 3 | Joint-fiber invariant indexed by return context | Medium / high | Medium until a concrete partition is specified / medium | High |

Route 1 is selected for falsification first. The old signed-belief derivative
archive already covers gap 222 through complexity 18 (and beyond), but retains
only aggregate statistics rather than per-cylinder N,O pairs. It therefore
cannot certify the new valuation observable without replaying this fixed box.

## Admission, fixed before execution

Use phase u only, complexity at most 18, gap triple (2,2,2), and every cut c.
An occurrence requires the forced schedule to begin `w ututut`, |w|=c,
with `w utututu` avoiding `uu`, `ttttt`, and `ututtu`. The last u is an
admissibility test, not an additional required observed branch.

For each occurrence at cylinder depth L=c+1<k, include every positive-depth
stripped ancestor `(u,k-j,L-j,x>>(2j))`, 0<=j<L. Deduplicate these nodes.
Test in ascending complexity, depth, and state order. For a distinct-endpoint
belief count E even-defect and O odd-defect endpoints, set N=E+O, and test
`v2(N)!=v2(2O)` with v2(0)=infinity. In particular N=0 fails; it cannot be
discarded as a successful case or omitted from the search.

Stop at the first failing node or exhaustion of this fixed box. A failure
refutes the ancestor valuation conjecture only after its ancestry and exact
endpoint counts have been independently verified. A passing finite box would
support only attempting a structural proof; it authorizes no cap increase.
Neither outcome proves or refutes signed nonvanishing without examining the
actual signed mass S=E-O at the witness.

Track schedule-cap hits (cap 64) and excluded depths L>=k explicitly. They
are unresolved boundary cases, not successful valuation checks. The broader
all-cuts obligation B_all remains separate from this restricted test.

Use one local CPU, 120 seconds, 1 GiB, primary and Boolean generator checks,
direct and recursive concrete beliefs, arithmetic gate self-checks, and an
atomic result with full commit, source hashes, parameters, software/hardware,
timings, and limitations. If a counterexample appears, record its complete
defect histogram, an originating admissible occurrence, and a generator
witness. The test is a new observable on an old bounded domain; it is not a
larger signed-nonvanishing census or a first-prefix-witness search.

## Follow-up admission: separate the two original conjectures

The first reported failure is a stripped ancestor with low digit 2, so it
is not itself a three-return occurrence. The original valuation note stated
both an occurrence-only conjecture and the stronger ancestor conjecture
needed for a simple digit-by-digit induction. They must not be conflated.

On the SAME 26 phase-u gap-222 occurrences found in this fixed box, test the
occurrence-only gate separately, in complexity/depth/state/cut order, stopping
at the first failure or exhaustion. This adds no frontier levels or gap
triples. A failure refutes the weaker original conjecture too; success leaves
it open while the proposed ancestor induction is obstructed. Record that
result independently with the same exact provenance and resource limits.

Also replay the three nodes on the named failure-to-occurrence ancestry,
to see whether the failed gate recovers at either subsequent required lift.
This is three named evaluations, not a further search.

## Actual occurrence counterexample (`refuted`)

The weaker occurrence-only conjecture already fails at

```text
phase u, k=17, x=0x190b9fdfb, cut c=1, depth L=2, gaps=(2,2,2).
generator witness: uuptutuuuuutuputp
forced schedule: tututut
base w: t
observed wE: tututut
admissibility word wEu: tutututu
```

The witness begins with phase seed u=1 and has 17 letters; its remaining
letters are forward generators in the arithmetic convention. Independent
Boolean-generator replay gives x exactly. The forced schedule contains the
entire required wE. The appended final u is NOT observed, but wEu avoids
all three forbidden words. This meets the original occurrence definition;
requiring that final u to be observed would silently change the conjecture.

There are exactly 946 distinct dominant endpoints, with defect histogram

```text
cost 0: 525; cost 1: 421; no other costs.
E=525, O=421, N=946, S=104.
```

Consequently

```text
N=2*473, 2O=2*421, S=8*13,
v2(N)=v2(2O)=1, while v2(S)=3.
```

This contradicts the occurrence-only valuation inequality and its equivalent
form `v2(S)<=v2(N)`. Both odd parts E and O are odd and E+O is 2 modulo 4,
which also violates the normalized criterion. The actual signed mass is
nonzero; this is not a cancellation or an adjacent-shadow counterexample.
Its cut also satisfies the proposed boundary bound by a wide margin.

## Ancestor counterexample (`refuted`)

The stronger ancestor conjecture fails already at the node

```text
phase u, k=16, x=0x6473d46a, depth L=3.
```

It comes from the known genuine occurrence

```text
phase u, k=18, z=0x6473d46ab, depth 5, cut 4, gaps=(2,2,2),
forced/admissibility word ttttutututu,
generator witness uutuuttuupupuuupup.
```

Indeed `z>>4=x`, and both complexity and depth decrease by two. The
ancestor's complete defect histogram is `{0:46, 1:36, 2:6}`, giving

```text
E=52, O=36, N=88, S=16,
v2(N)=v2(2O)=3, v2(S)=4.
```

Equivalently E=4*13 and O=4*9 have equal valuation, with odd parts summing
to 22, which is 2 modulo 4. This node is not itself a three-return occurrence:
its low digit is 2. Its verified ancestry, rather than a generic mask path,
puts it in the exact domain of the stronger conjecture.

## Failure can recover along the required ancestry

The actual two lifts from this ancestor are:

| Node (phase u) | Depth | E | O | N | S | v2(N), v2(2O) |
| --- | --- | --- | --- | --- | --- | --- |
| k16, `0x6473d46a` | 3 | 52 | 36 | 88 | 16 | 3,3: fails |
| k17, `0x191cf51aa` | 4 | 25 | 10 | 35 | 15 | 0,2: passes |
| k18, `0x6473d46ab` | 5 | 11 | 9 | 20 | 2 | 2,1: passes |

The first lift adjoins digit 2 with current mask 1111. Only the parent's
full-fiber endpoints survive, with their defect parity unchanged. Its full
slice has E=25,O=10, explaining the middle row by the all-depth count-transfer
formula. The second lift adjoins digit 3 with current mask 1011. Thus even
on a genuine ancestor chain, success at the final occurrence does not imply
success at all ancestors. This recovery does not rescue the occurrence-only
conjecture, which has the separate actual counterexample above.

## Finite verification and provenance

The fixed phase-u gap-222 box through k=18 has 26 occurrences and 43 distinct
positive-depth ancestors, with zero schedule truncations and zero excluded
depths. The ancestor test stopped at node 22; the other 21 ancestor nodes
were not tested by that search. The separate occurrence-only test stopped
at occurrence 13; its remaining 13 occurrences were not tested by that
search. All tested direct and recursive beliefs agree. Minimality means
only first in these specified finite orders, not smallest among both phases
or all admissible gap triples.

This does not contradict the earlier 19-row/25-ancestor finite result. Those
ancestors were generated only from originating occurrences through k=16.
The failing k=16 ancestor here originates at k=18, outside that old source
set. Checking two selected k=18 nodes earlier did not check their full
ancestry. The actual failing occurrence has k=17.

Muse implemented the bounded searches and independently replayed the
ancestor with the pre-existing oracle. Lead review checked the code,
replayed the actual occurrence and all three chain nodes using the old
independent oracle, and compared packed versus Boolean frontiers through
k=18. The independent actual-occurrence record retains all 946 endpoint
costs, the histogram, the generator witness, and the unobserved-final-u
check. Two Muse workers encountered provider rate limits during the final
follow-up; the lead completed those checks locally. No fresh Muse review of
that final follow-up is claimed.

Atomic records in `results/problem1/`:

- `20260905_return_ancestor_valuation.json`: bounded ancestor search;
- `20260905_return_ancestor_valuation_independent.json`: Muse's old-oracle
  replay of the named ancestor and its originating occurrence;
- `20260905_return_occurrence_valuation.json`: separate occurrence-only
  search and the three-node chain, with executed source embedded;
- `20260905_return_occurrence_valuation_independent.json`: lead replay using
  the pre-existing independent oracle, with executed source embedded.

All include exact parameters, full commit, timing, software/hardware, hashes,
and finite scope. The runnable ancestor analyzer is
`scripts/check_return_ancestor_valuation.py`.

## Consequence for the research strategy

Retire `v2(N)!=v2(2O)` as an all-depth certificate on this pathway: both of
its stated domains now have counterexamples. The elementary valuation law
remains valid, and all earlier finite records keep their stated meanings.
No relaxed valuation bound is proposed merely to fit these new witnesses.

The original task is still to exclude S=0 (or prove dominant nonemptiness
by another method) on genuine return occurrences, together with all excluded
boundary depths if using adjacent inclusion. Alternatively, the all-cuts
bound B_all is a standalone sufficient route for eventual alternation.
The next proof mechanism must retain full return constraints and concrete
endpoint correlations, or work directly on those occurrence cuts. Merely
omitting a future word from a local update formula does NOT show that return
words cannot constrain its realized inputs. No such impossibility claim is
made. General periods of least period >=3 remain unresolved.
