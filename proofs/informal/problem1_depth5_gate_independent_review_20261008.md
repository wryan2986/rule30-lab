# Independent review of the depth-five gate screen

Status: **FINITE-EXHAUSTIVE** for the corrected product graph at observer depth
`r=5`. Problem 1 remains **OPEN**.

## Independent reconstruction

I reconstructed the normalized transition without importing either the
producer's `T`/`local_step` routine or an SCC/rank routine. The implementation
uses the explicit Rule 30 lookup table for
`F(a,b,c)=a XOR (b OR c)`. For each local state, it forms the two fixed-boundary
raw rows, applies `F` to the first row and to the XOR companion row, sets
`Y=raw_a XOR raw_b`, then normalizes `Xnew=raw_a XOR (label AND Y)`. The
extra pair is decoded from product bits 10–11 or 12–13, copied into pair 5
of the depth-six input, and evaluated as a genuine depth-six transition.
This places the added pair where the transition reads it.

The product domain is all `2^14 = 16,384` tuples
`U | (V << 10) | (Z << 12)`. For blind `U`, the graph allows all four
label pairs `(a,b)`; otherwise it allows only equal labels. An edge is retained
only when the two next upper states agree in their lower ten bits. A bad edge
has blind `U`, equal labels, and unequal `Y` bits in the two added output
pairs.

## Cycle check and result

The verifier generated the complete graph and found 33,152 retained directed
edges, 160 bad edges, and 12 blind upper states. For each bad edge `s -> t`, it
ran a separate breadth-first search from `t` to test whether `s` is reachable.
That is the exact directed-cycle criterion for the edge. All 160 searches
finished; none returned to its source. Thus no bad edge lies on any directed
cycle in this finite graph. The recorded run took 0.50 seconds on Python
3.12.14, Linux x86-64, and peaked at 14.1 MiB resident memory. The verifier
enforces 60-second CPU/wall and 256 MiB address-space limits with resource
limits and an alarm.

This independently corroborates the corrected depth-five graph counts and the
stronger unlifted cycle-exclusion conclusion. It does not check the producer's
rank bytes or SCC partition: direct reachability was used instead. I reviewed
the supplied finite-reduction argument and its projection lemma. The lemma's
rank projection is valid under its stated premise (a lifted rank nondecreasing
on every edge and strictly increasing on every bad edge on all sheets), while
the present check establishes the base product graph property directly. The
all-period deduction remains conditional on the supplied finite-reduction
theorem and its nonzero-parent and complete odd-fiber hypotheses.

## Scope and provenance

This is an exhaustive finite computation at `r=5`, not a proof about all
depths or Problem 1. It establishes neither transport over zero returns nor
bounded reuse on original finite support. Exact input domains, software and
hardware facts, timing, full commit, and result are recorded in
`results/problem1/20261008_depth5_gate_independent.json`.

- Base and observed full commit: `ddc53f28dbe30a98764f3dec8a7725ec5be1dbe8`
- Verifier SHA-256: `e0a186e503f991c978631e50d9d367d17cc310c401ece95d4ce2917ffbfbe6f3`
- Result SHA-256: `b94b835f79652521e278f2034219195791eb6f62bbc57d7d1b4291af4823790d`
- Corrected producer note SHA-256: `a6d84dcdc76b5d14629026d8d58fbd7cf0f2900d7e703c4c08de2381604e4cfb`
- Supplied checker SHA-256: `69d3f20bc1b7eb95df38270506483e1ac201a5339ec7edd487c557684e0d093a`

The JSON result is written by a same-directory temporary file, flushed, and
atomically renamed into place.
