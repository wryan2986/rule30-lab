# Depth-five product-rank screen, corrected and certified

Status: **COMPUTATIONALLY VERIFIED — INDEPENDENTLY CHECKED** at observer depth r=5.
Problem 1 remains **OPEN**.

## What was wrong with the first depth-five run

Both uncommitted depth-five scripts decoded the third pair `Z` from bits 12-13
of the product state, but then fed it to `local_step(..., depth=6)`, which reads
only bits 0..11. `Z` was therefore invisible: copy B was evaluated as if `Z`
were `(0,0)`. 14336 of 32768 copy-B outputs change under the correction.

The consequence was not a small perturbation. The buggy run reported 4 bad
edges inside cyclic strongly connected components and the record was set to
`COUNTEREXAMPLE_CANDIDATE`, so candidate **S5 was recorded as refuted**. A
witness-extraction probe built on that graph produced a 10-step cycle for word
`0110011100` whose projected upper states were

    995, 995, 340, 26, 499, 708, 474, 162, 194, 995

with a duplicated entry, while `local_step(995,0,5) = 340`. That cycle was
never a valid trajectory; it was an artifact of the mis-encoded graph.

The corrected convention matches the independently certified depth-four checker
`check_depth4_gate_miter.py`: the added pair occupies the pair at bits 2r..2r+1
and `local_step` is called at depth r+1. Product packing is unchanged
(`U | (V<<2r) | (Z<<(2r+2))`); only the decode re-encodes `Z` into pair r.

## Candidate S5

Every directed cycle of the complete depth-five product graph contains no bad
edge. This is strictly stronger than affine extension, since it imposes no
odd-parity and no nonzero-parent restriction on product cycles.

**S5 holds at r=5.**

## Certificate

- product states: 16384
- retained edges: 33152
- bad edges: 160
- blind upper states: 12
- strongly connected components: 16165, largest 197
- bad edges inside any cyclic SCC: **0**
- rank: uint16 per state, 32768 bytes
- rank SHA256: `aeec97837a2d02f2f595698b3e644871d64a29cf9203291e05d325a462ec6645`
- nondecreasing violations on every retained edge: 0
- bad edges not strictly increasing: 0

The rank is a topological rank of the strongly connected condensation. It is
nondecreasing on every edge and strictly increasing on every bad edge, so no
bad edge can lie on a directed cycle.

## Independent check

A separately written verifier re-derived the graph and re-checked the
certificate. It obtained 33152 edges, 160 bad edges, 12 blind upper states, 0
bad edges on a directed cycle by brute-force reachability rather than by any
SCC algorithm, and the decoded rank hash `aeec978...6645` matched. Because the
producer author twice shipped wrong strongly connected components, the
brute-force reachability test is the authoritative check and the SCC counts are
reported only as supporting data.

Two independent facts were also confirmed exactly:

- `T(u,0,r) == T(u,1,r)` if and only if all r upper `Y` coordinates are zero.
- label-blind upper-state counts are 2, 2, 4, 8, 12, 20, 36, 60 for r = 1..8.

## Depth sweep

Brute-force reachability on the corrected graph gives zero bad edges on a cycle
for every depth tested:

| r | states | edges | bad | bad on a cycle |
|---|--------|-------|-----|----------------|
| 1 | 64 | 192 | 16 | 2 |
| 2 | 256 | 576 | 32 | 0 |
| 3 | 1024 | 2176 | 64 | 0 |
| 4 | 4096 | 8448 | 96 | 0 |
| 5 | 16384 | 33152 | 160 | 0 |
| 6 | 65536 | 131712 | 288 | 0 |
| 7 | 262144 | 525440 | 480 | 0 |
| 8 | 1048576 | 2099072 | 800 | 0 |

At r=1 the statement genuinely fails, with 2 bad edges on a cycle, so this is
not a vacuous pattern. r=1 is already covered by the proved shallow theorem.
The sweep r=2..8 is **COMPUTATIONALLY VERIFIED TO DEPTH 8** by brute-force
reachability, and carries no rank certificate of its own; only r=5 does.

## What this does and does not establish

By the projection lemma in `problem1_gate_miter_finite_reduction.md` Section 6,
a rank on the unlifted product graph that is nondecreasing on every edge and
strictly increasing on every bad edge implies absence of bad product cycles.
Combined with the gate equivalence theorem this yields affine extension at
observer depth r=5 for every even presentation period, on the complete
odd-label fiber with all raw parents nonzero.

It does not establish affine extension at observer depths r >= 9 by any proved
mechanism, nor transport across a zero return or a period doubling, nor any
bounded-reuse charge on the original finite support. The global obstruction
stated in the handoff is unchanged: local affine label transport does not
yet imply transport across a zero return, and no bounded-reuse charge exists
on the same original finite support.
