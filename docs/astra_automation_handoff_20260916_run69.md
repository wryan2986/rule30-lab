# Astra automation handoff — 2026-09-16 run 69

## What changed

Continued directly from run 68's p=16 branching counterexample and completed the proposed zero-column first-return graph enumeration.

Added:

- `proofs/informal/problem1_p16_zero_return_graph_complete.md`

Research commit: `655a2aa00a62ebd2f8bd27b9cbc0164c6e2656b7`.

## New result

The complete p=16 reverse basin, compressed to zero-column states `(0,w)` modulo cyclic rotation, is a finite DAG with:

- 36 zero-target necklaces total;
- 20 even-parity internal vertices;
- 16 odd-parity leaves;
- 39 nontrivial directed connector edges;
- no cycles.

Every odd leaf has exact rotational period 16, so all 16 are legal full-period odd-parity initial necklaces. Every reverse branch from the terminal pair ends at one of them. Therefore there are **exactly 16 rotation-inequivalent terminating period-16 initial necklaces**, not merely the two exhibited in run 68.

The note records canonical representatives and exact termination widths for all 16 leaves. The smallest-width representative is run 68's `c16_a = 0000010101000101` at width 87867. Run 68's `c16_b = 1001110010100010` is a rotation of canonical `0001010011100101` at width 229338.

The 20 internal even targets have primitive periods: 2 of period 1, and one each of periods 2, 4, and 8, plus 15 genuinely full-period-16 targets. Thus the inherited lower-period spine survives, but most p=16 internal structure is genuinely new.

## Evidence status

Exact finite computation only. Reverse connectors use the proved exact predecessor classification, so no brute-force search over 2^32 state pairs is required. The zero-return queue exhausts after 36 canonical vertices. All 16 leaves were independently forward-propagated to consecutive zero columns at the recorded widths.

## Best next target

Do not return to the disproved uniqueness conjecture. Define and compare the induced zero-return graphs `G_p` for p=1,2,4,8,16, including leaf counts and embedding relations. Look for a recurrence in the graph/leaf structure under p -> 2p. Only after that structural comparison should p=32 be attempted, preferably directly at the zero-return graph level rather than by enumerating initial words.