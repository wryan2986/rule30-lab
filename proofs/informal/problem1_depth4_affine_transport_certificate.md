# Problem 1: all-period affine extension at depth four

Status: LEMMA WITH PROOF — INDEPENDENTLY CHECKED, computer-assisted.
Problem 1 remains **OPEN**.

## 1. Exact statement

Fix any even p>=2 and any realizable aligned depth-four normalized
portal orbit R. Require every earlier raw parent and the depth-four
raw parent to be nonzero, so its nonempty complete odd-label fiber C_R
has a unique depth-five extension E for every member. Then E is affine
over GF(2). Its affine rank is u_4-u_5, and u_5 is constant on C_R.

This extends the all-period shallow H_ext theorem from r<=3 to r=4 on
the same nonzero-parent domain. It does not assert invariant full Y,
invariant deeper blind set, existence past a zero parent, or the general
all-depth H_ext conjecture.

## 2. Certificate and exact graph

The product of two depth-five stacks sharing their depth-four state has
4096 states. Adding two driver parity bits and one temporal parity bit
gives the exact 32768-vertex graph in
`problem1_gate_miter_finite_reduction.md`. Labels are all four binary
pairs. An edge is retained precisely when the upper output states agree.
There are 67584 retained directed edges.

A bad edge has upper state blind, equal input labels, and unequal new
outgoing Y bits. The graph has 768 such edges. The supplied certificate
assigns an unsigned 16-bit integer rank rho to EVERY vertex, in order

    vertex=(sheet<<12)|product_state.

The product state uses eight low upper bits, the first new pair in bits
8–9 and the second new pair in bits10–11. The sheet uses driver-A,
driver-B,temporal bits in that order; each edge XORs a+2b+4 into it.
The certificate has 65536 bytes, encoded as base64 little-endian uint16.
Its SHA256 is

    3a9eb40a2b54e39ff79869888d1da5be5cfcb75368ad15db80d3619554a03263.

The required properties are:

    rho(target)>=rho(source) for EVERY retained edge;
    rho(target)>rho(source) for EVERY bad edge.             (1)

The independent verifier reconstructs the entire graph from raw
Rule-30 truth-table updates and checks (1), not merely certificate hashes
or the producer's component labels.

## 3. All-period consequence of the checked properties

Suppose two cyclic depth-five stacks share R and have the same driver
label at an upper blind phase but different outgoing new Y there. They
give a product cycle containing a bad edge. Any product cycle, whatever
its length and driver parities, accumulates some sheet increment h in
GF(2)^3. Repeating the same cycle from the translated sheet closes the
lifted walk because h+h=0.

Monotonicity in (1) forces the rank constant along that closed walk.
Strict increase on its bad edge is then an exact contradiction.
Thus no such two cyclic histories exist. In particular, for each upper
blind phase s, the new gate is the same for all drivers in C_R having
the same w_s. A function of one binary coordinate has the form

    d_s(w)=alpha_s+beta_s w_s.

The proved gate equivalence therefore makes E affine, at every even
presentation period p. Its complete output fibers give the claimed rank
formula. The finite graph is exact at this observer depth and covers
arbitrarily long closed walks; this argument uses no extrapolation from
a finite list of periods.

## 4. Reproduction and verification scope

Certificate producer:

    python3 experiments/problem1_nonperiodicity/check_depth4_gate_miter.py

Independent verifier:

    python3 experiments/problem1_nonperiodicity/verify_depth4_gate_rank_certificate.py

Producer record: `results/problem1/20261002_depth4_gate_miter.json`.
Verification record:
`results/problem1/20261002_depth4_gate_rank_certificate_verification.json`.

The producer uses the polynomial normalized recurrence and builds the
component condensation. The independent verifier uses the scalar raw
truth table [0,1,1,1,1,0,0,0] at neighborhood index 4h+2l+x, then
renormalizes two independently updated rows. It imports no producer
transition and needs no component algorithm. This difference of methods
checks the retained edges, parity sheets, bad-edge definition and rank
inequalities independently. The parent reviews both implementations and
the all-period reduction before accepting the theorem.

The admission fixes r=4, 60 seconds wall, 256 MiB resident memory and
256 KiB output. Records retain source/input hashes, full base commit,
hardware/software, timings and limitations. Draft witness-path errors in
the producer were corrected before accepting its final record; they were
not mathematical counterexamples. Its no-witness status alone would
have been insufficient without the independently checked certificate.

The final independent verification passed all 2048 raw two-row transition
controls, all 67584 retained-edge inequalities, and strict increase on
ALL 768 bad edges across all eight sheets. There are zero internal bad
edges and zero groups satisfying the conservative three-flag obstruction.
The parent inspected the raw truth-table construction, both product-copy
encodings, sheet arithmetic and every accepted predicate, then reran the
completed producer and independent verifier. The producer took about
3.3 seconds and the independent verifier about 0.1 seconds on the recorded
machine. These timings are execution metadata, not proof hypotheses.

Independent logical review of the general finite reduction is recorded in
`problem1_gate_miter_finite_reduction.md`. Proof of this specific theorem
uses the stronger strict-bad-edge property (1), so it needs no unverified
claim that the supplied groups are exact components.

Process correction: the graph worker tried an extra Luna app review task
despite its no-subdelegation assignment. The app rejected its arguments
before creating a task. Its initial report incorrectly described that as
failure to launch the worker itself; the parent obtained the exact error
and stopped that worker. No model fallback or Astra call was made. The
logical critic and independent certificate verifier used explicitly pinned
free Space Bunny routes. A draft verifier boundary/indexing error was
caught by its raw-rule controls and corrected before its accepted record.

## 5. Remaining obstruction

The smallest unresolved extension depth is now r=5.
A proof at every observer depth would still require transport through
zero returns and period doubling, with bounded reuse on the SAME original
finite support. This finite observer rank certificate supplies the
depth-four gate exclusion, not that physical-support resource.
