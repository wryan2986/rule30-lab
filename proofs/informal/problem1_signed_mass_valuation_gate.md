# A 2-adic valuation gate for the signed certificate

Status: `finite-exhaustive` for the fixed records and ancestor checks below;
`inconclusive` for the all-depth arithmetic conjecture. The sufficient
valuation implication is `partial-proof` (elementary integer arithmetic).

For a distinct-endpoint belief write `E` and `O` for the numbers of even- and
odd-defect endpoints, `N=E+O`, and `S=E-O=N-2O`. A possible arithmetic
certificate of nonvanishing is `v_2(N) != v_2(2O)`, using `v_2(0)=infinity`.
For positive `N` this inequality implies `S!=0` by the elementary valuation
law for a difference of terms with unequal valuations.

Candidate (`inconclusive`): that inequality holds on every admissible
three-return occurrence. It differs from the sign/coherence hypotheses:
it allows both signs and mixed slice components, using integer divisibility
instead of a real region. It remains stronger than nonvanishing.

Admission: compare the 19 existing full-domain per-occurrence rows through
complexity 16 from the primary and independent atomic records, including
phase, complexity, state, cut, depth, gaps, signed mass, and belief size.
Exact row agreement is required before interpreting this derived observable.
Compute `E,O` from the primary defect histogram and independently from the
other record's `(N,S)`, requiring identical integers.

If the two valuations coincide on any row, the unequal-valuation certificate
is refuted there, even if the signed mass is nonzero. If they never coincide,
only a structural arithmetic argument is justified; no larger census.
This reads fixed records and does not rerun a frontier search. Save normalized
rows, source hashes, full Git commit, software/hardware, and timings atomically.
One local CPU, at most 19 rows, 30 seconds, 1 GiB. Any mismatch of the source
rows suspends the arithmetic conclusion pending correction.

## Exact sufficient implication (`partial-proof`)

Assume `N>0`. If `v_2(N) != v_2(2O)`, factor the lower power of two from
`N-2O`. The remaining difference is odd because exactly one term is odd,
including the case O=0. Consequently

```text
v_2(S)=min(v_2(N),v_2(2O)) <= v_2(N), and S!=0.
```

Conversely, for positive N and nonzero S, if `v_2(N)=v_2(2O)`, the normalized
terms are both odd, so their difference has higher valuation:
`v_2(S)>v_2(N)`. Thus the candidate can equivalently be expressed as the
inequality `v_2(S)<=v_2(N)` when the values are nonzero. This is stronger than
nonvanishing, and it explicitly fails at a cancellation E=O>0.

A useful reformulation isolates the nontrivial parity case. If E and O are
both positive with different valuations, `v_2(E-O)=v_2(E+O)` automatically.
If `v_2(E)=v_2(O)=j`, write `E=2^j e`, `O=2^j o` with e,o odd. Then the
candidate holds exactly when `e+o=0 mod4` (equivalently `e-o=2 mod4`).
Indeed one of e+o and e-o is 2 modulo 4 and the other is divisible by 4.
This presents a concrete arithmetic condition an all-depth proof would need
to explain, rather than a real hyperplane-avoidance condition.

## Fixed-record result (`finite-exhaustive`, not an invariant)

All 19 primary and independent occurrence rows agree on their full keys,
signed masses, belief sizes, and same-cylinder counts. Even/odd counts from
the primary defect histograms match `(N+S)/2,(N-S)/2` from the independent
record. Every row satisfies the unequal-valuation condition.

The atomic record `results/problem1/20260905_signed_mass_valuation_gate.json`
contains all normalized rows, exact input hashes, full source commit, complete
replay source, and run provenance. The original two input records were
pre-existing untracked files; they were read and preserved. Embedded normalized
rows allow the arithmetic to be replayed independently of those files.

## Independent ancestor check (`finite-exhaustive`)

An induction on stripped digits may need the property on ancestors, not only
on actual occurrences. Muse tested that stronger finite consequence on
exactly the 25 ancestors of the same 19 occurrences, in complexity/phase/
depth/state order, followed by the two already-verified named nodes:

| Node | N | E | O | S | v2(N) | v2(2O) |
| --- | --- | --- | --- | --- | --- | --- |
| u, k=18, `0x642e4d2f1`, L=3 | 405 | 161 | 244 | -83 | 0 | 3 |
| u, k=18, `0x6473d46ab`, L=5 | 20 | 11 | 9 | 2 | 2 | 1 |

All 27 nodes satisfy the inequality, with direct/recursive endpoint-belief
agreement on every node. This uses the existing complexity-16 domain and two
named complexity-18 evaluations; no larger nonvanishing census was run.
The record `results/problem1/20260905_signed_ancestor_valuation.json` embeds
the complete executed source and exact node rows, with full provenance.

## Unresolved proof obligation

The current conjecture is that the unequal-valuation condition holds on every
admissible three-return ancestor at every complexity. No induction proving
this condition has been found. In particular, its preservation does not
follow from the scalar lift or the joint-fiber identity. A successful proof
must control how exact even/odd endpoint counts split and recombine under
the forced schedule, and must also prevent the empty-belief case N=0.

The subsequent `problem1_signed_count_transfer.md` proves the exact parity
count update and refutes unrestricted one-lift preservation: parent p/k5/
`0x321`, D1 has (E,O)=(2,0), but its digit-zero child p/k6/`0xc84`, L2 has
(E,O)=(1,1). Retaining all ten outgoing parity counts also fails to close
the universal vector update. These generic counterexamples do not refute
the conjecture on admissible three-return ancestors.

The next step is a structural analysis of that integer-count transfer or a
precisely motivated counterexample test. Merely increasing the census cap
after finite success is not authorized by this result. The original
nonvanishing conjecture, the boundary bound, and Problem 1 remain open.
