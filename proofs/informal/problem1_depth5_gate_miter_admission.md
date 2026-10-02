# Admission: depth-five product-rank screen

Status before execution: CONJECTURE; no depth-five result is claimed.

The proved all-period H_ext frontier is r=4. This experiment tests one
precise stronger sufficient condition at the first unresolved depth r=5:
the product graph below has no directed cycle containing a bad edge.
If true, an independently checked integer rank proves H_gate and affine
extension for every even presentation period on the nonzero-parent domain.
If false, the smallest recovered bad cycle identifies exactly where this
stronger mechanism stops; its odd-driver parity and all-parent domain must
be checked before making any claim about H_ext. The exact sheet/flag
reduction remains available in that case, with a separate admission.

This directly tests local label transport needed by the whole-tail route.
It does not prove transport through a zero return or bounded reuse against
the original finite support. No larger driver-period census or first-zero
traversal is admitted.

## Fixed graph and falsifiable statement

Use normalized Rule-30 states with boundary pairs (1,0),(0,1). The upper
state U has r=5 pairs (ten bits). Two added pairs V,Z each have two bits.
Encode the product as U + (V<<10) + (Z<<12), where each pair is X+2Y and
upper pair j occupies bits 2(j-1),2(j-1)+1. There are exactly 16384 states.

For each product state and each ordered binary label pair (a,b), update
(U,V) by T_a and (U,Z) by T_b. Retain the edge precisely when the upper
outputs agree. The upper state is blind precisely when all five upper
output Y coordinates are zero. A bad edge has blind U, equal labels a=b,
and unequal outgoing added Y coordinates.

**Candidate S5.** Every directed cycle in this complete product graph
contains zero bad edges. All initial states, both boundary cases, all four
label pairs and all cyclic lengths are included. There is no odd-parity
restriction in S5; it is deliberately stronger than H_ext on odd fibers.

An absence certificate is a uint16 rank for every product state, verified
nondecreasing on EVERY retained edge and strictly increasing on EVERY bad
edge. A topological rank of the strongly connected condensation suffices
if S5 is true. The independent verifier must derive all edges from a raw
Rule-30 truth table and import no producer transitions or SCC algorithm.

If S5 fails, recover an actual product cycle with labels and every phase
state. Record its length, both label parities, parent participation flags,
and first bad edge. Do not call it an H_ext counterexample unless it has
even length, both odd driver weights, every nonzero raw parent, and a
separately reconstructed four-word non-affinity witness. Do not perform
an unadmitted lifted-graph search merely because S5 fails.

## Controls, resources and reproducibility

Run locally, only r=5. Caps: 60 seconds wall per script, 256 MiB resident
memory, 256 KiB per result. There are at most 65536 candidate state/label
pairs before retaining edges; the rank has 32768 bytes before base64.
Stop on a cap or a first explicitly recovered bad cycle. Count the entire
graph to establish absence; arbitrary finite-period tests cannot do so.

Compare normalized local updates with an independent bit-array raw
Rule-30 transition on all 4096 depth-six states and both labels. Record
exact counts, ordered graph construction, cycle or rank bytes/hash,
full base commit, immutable-reference SHA256, all input/source hashes,
hardware/software facts, timings, exclusions and limitations. Write JSON
atomically. Do not edit the immutable reference or unrelated files.

Worker ownership is restricted to the named new r=5 producer/result paths;
the independent verifier owns separate new r=5 verifier/result paths.
No subdelegation, automatic fallback, cloud compute, first-witness scans,
or Astra call is authorized. Parent review supplies the proof and synthesis.
