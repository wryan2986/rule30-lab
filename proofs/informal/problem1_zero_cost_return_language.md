# Zero-cost return histories and a finite residue graph

Status: `partial-proof` for the exact all-length language reduction and
history-image scope lemmas; `finite-exhaustive` for the graph certificates;
`refuted` for universal strict descent of W* and its representation minimum.
Base checkpoint: `5d30b069a70145da53b81ec3a958e95d500cc9d4`.
Problem 1 and the whole-tail occurrence bounds remain open.

## Strategy and admission

The synchronization theorem gives an exact growing history, but no return
exclusion or universally decreasing potential. The surviving candidate is

    W*(w)=count_(old prefix0 mod16,T)(w)
          +count_(old prefix1 mod16,U)(w),

excluding the fixed phase root. It decreases2->0 on two named genuine
blocks, a finite observation only. Because W*>=0 on every ordinary
history, one genuine block with W*(initial)=0 would already refute strict
descent, regardless of its final value.

Ranked routes (`heuristic`):

1. Exact zero-cost language reachability for the fixed motif ututut.
   High falsifiability, low cost, and an all-length structural reduction.
   It either supplies a counterexample or proves no zero-cost input has
   that block. It is not a frontier census.
2. A weighted finite-word automaton for the complete block change.
   Potentially tests all input-history lengths, but the required residue
   precision and terminal contribution must first be proved. Higher cost;
   unnecessary if route1 refutes the current candidate.
3. Descent restricted to the synchronized induced family near critical
   cuts. Directly relevant, but its length/elapsed-time constraint has
   not been reduced to a finite graph. A cut0 counterexample alone does
   not refute that restricted claim.

Choose route1. The arbitrary integer903 has the six observed branches
ututut, although it is NOT an ordinary-frontier state. Test the proposed
exact branch cylinder x=903 mod2^14. Construct the graph on residues
modulo16384 with generator edges T,U,P, deleting precisely the two edge
types counted by W*. Start separately from root3 (phase p) and root1
(phase u), and seek residue903. Breadth-first search gives a shortest
zero-cost history for each phase; if no path exists, exhaust the finite
graph and retain its closure certificate.

For each reached witness, reconstruct the actual positive integer from
its ordinary generator word, verify membership by that word, execute
exactly six forced branches, and retain initial/final histories and all48
edge counts. Verify the appended admissibility-test u without counting
it as an observed seventh branch. A zero-cost initial word refutes the
universal candidate; an unreachable target would prove positive initial
cost for every occurrence of this motif. Neither outcome establishes a
whole-tail theorem. No other motifs, larger frontier boxes or LP runs are
admitted. Independent verification uses a reverse graph distance map, not
the same forward search. Each local run has120seconds and1GiB, atomic
JSON, full Git, exact sources/input hashes and runtime provenance.

## Exact branch-cylinder lemma (`partial-proof`)

Use T,U,P,F and the gate from the established notes. The generators
preserve congruence modulo every power of2. Within a permitted branch,
F=Q(P(x>>2)), so congruence precision decreases by exactly two bits.
Every defined forced output is3 modulo4.

Let a be a verified finite integer with a prescribed r-step branch word
sigma, r>=1. For every nonnegative integer x,

    x has those r observed branches
       iff x=a modulo 2^(2r+2).                      (1)

For sufficiency, equal low2r+2 bits supply the same first mod16 gate.
After one step the outputs agree modulo2^(2r), enough to continue the
induction through all r gates. For necessity, use the established exact
common-branch valuation law: two different inputs sharing the r branches
have outputs3 modulo4 after r steps, so their initial difference is
divisible by2^(2r+2). Same-branch injectivity prevents different inputs
from becoming equal during this argument. Identical inputs are immediate. This argument
does not require a seventh branch or an infinite continuation.

For sigma=ututut, r=6 and a=903, the modulus is16384. The use of903
as a residue representative makes no claim of ordinary membership.

## Exact language reduction (`partial-proof`)

Let an additive history potential have fixed nonnegative edge weights
indexed by (old prefix modulo2^b,input generator). For a fixed verified
branch word as above, put m=max(b,2r+2). Use residues q modulo2^m with
edges

    q --g--> G_g(q) modulo2^m.

Retain only zero-weight edges. A path starts at the phase root and is
accepted when its terminal residue agrees with a modulo2^(2r+2).

These accepted paths are exactly the ordinary
histories of zero initial potential whose endpoints have branch word
sigma, at EVERY finite history length. Proof: by induction each graph
path is the residue projection of the concrete generator word from its
root. Conversely every ordinary word projects to that unique path.
Nonnegative weights make total weight0 equivalent to using only
zero-weight edges. Equation (1) is exactly the endpoint acceptance test.

This quotient is exact for the fixed finite block and a concrete word
path. It is not a finite-state quotient for arbitrary future trajectories,
and it does not splice paths from different endpoints in a signed belief.
No generator-word count is substituted for a distinct-endpoint mass.

If an accepted zero-cost path exists, W(final)>=0=W(initial), so strict
descent on all such blocks is impossible. If none exists, every history
admitting sigma has positive initial cost; for integer weights it is at
least1. That finite-graph closure would prove an all-length statement
through this exact reduction, not by extrapolating a census.

## Counterexamples and finite minimality

Claim status: `finite-exhaustive`. Forward breadth-first search and an
independent reverse-distance computation agree on these witnesses:

| Phase,k | Word FROM ZERO, including phase root | Initial integer | W* before/after six branches |
| --- | --- | --- | --- |
| p,12 | putptttttptu | 0xc84387 | 0->1 |
| u,15 | utututupupuuttt | 0x191cc387 | 0->0 |

Each actual integer is reconstructed from its word, lies in the stated
ordinary frontier, and has the six required observed branches
ututut in this check. The string utututu is admissible; its final u is
not executed. Thus universal strict block descent of W* is `refuted` in
each phase. The p witness also refutes universal nonincrease of W* on
these arbitrary initial histories. No conclusion about every block of a
particular physical orbit follows.

The shortest nonroot zero-cost words have lengths11 in p and14 in u,
with lexicographic tie order t,u,p. This is minimum length only within
the corresponding phase's ZERO-W* language and this fixed branch motif.
It is not a minimum among all descent counterexamples or integer values.

The forward runs retain3,011 and9,720 discovered states, checking23,407
traversed edges independently with cells. They stop on first target
discovery. The reverse implementation constructs all16,384 states and
47,104 permitted edges, and records a distance to903 for every state.
For each edge q->q', the certificate satisfies d(q)<=1+d(q'); every
nonterminal state has an edge attaining d(q)-1. Only903 has distance0.
These inequalities prove the distances exactly: they lower-bound every
accepted path length and exhibit a path attaining each bound. In
particular the two root distances certify the stated minimum lengths.
All graph edges are ordinary-generator extensions, not forced-time
steps; coaccessibility is not a nontermination claim.

## Minimizing over representations does not repair strict descent

Claim status: `partial-proof` (exact counterexample implication). For
x in O_(a,k), define

    V_a(x)=min W*(w), over all ordinary representations of x.

The set is nonempty and finite, containing at most3^(k-1) nonroot words;
V_a(x)>=0. Each displayed zero word proves V_a(x)=0 without enumerating
the other representations. The six-step endpoint is ordinary by the
prescribed history update, so V_a(F^6(x))>=0. Strict decrease is therefore
impossible. For the u witness the displayed final word also has cost0,
so V_u is exactly0->0. For p the final minimum is bounded between0 and1;
no exact value beyond those bounds is asserted.

Moreover the u integer is already a known forced successor:

    F(0x642fdfb)=0x191cc387.

The previous u14 certificate induces a representation of this successor
with W*=2; the new u15 word represents the SAME integer with W*=0.
Thus merely restricting input ENDPOINTS to once-forced-reachable ones
does not rescue V. This excludes minimization over all representations
and selectors attaining that minimum, not arbitrary canonical selectors
or minimization over a smaller prescribed family.

## Why the new zero words are not prescribed descendants

Claim status: `partial-proof` (all-depth history-image constraints).
For any nonempty phase-u history v, H(v) begins with P: its first
original prefix is one of7,6,6, so S maps its residue to P in every case.
The new u witness begins with T AFTER its root, so it cannot be H(v)+Q
from a preceding history.

In phase p, if H(v) begins with U, the original first prefix must be13:
the possible prefixes are13,12,12. If v has another letter, its next
prefix is51 or50, so the second H letter is necessarily P. The new p
witness begins with UT after its root, violating this condition.
Both witness words have at least three nonroot letters, so their first
two positions precede the final appended Q in any putative predecessor.
This removes the short-word exception where the second letter might
itself be the append.

Consequently neither ZERO WORD can be the output of one prescribed
forced-history update. Nor can it be a prescribed descendant at any
positive forced time, since the last update would again have that form.
The u ENDPOINT is nevertheless once-forced reachable, as shown above.
This distinction is essential: these witnesses do not refute W* restricted
to actual prescribed histories or the near-boundary synchronized family.
The minimum V fails because it includes representations outside that
family. Synchronization does not authorize later reselection from all
representations of the endpoint.

## Independent verification and remaining obligation

Muse Spark 1.3 Contributor independently checked the valuation argument,
the14-bit/six-observed-branch distinction and the representation-minimum
scope. An initial objection treating the appended u as a seventh gate
was withdrawn after redoing the terminal-mod4 argument. The lead retained
the unobserved-letter quantifier throughout. Fresh adversarial review
accepted the language reduction, image constraints and counterexample
scopes. It caught a verification check using the old modulo4 table for
W*: the corrected verifier independently replays that history, compares
all48 modulo16 counts and confirms the claimed value2. The complete
certificate verification passes after this correction. Final read-only
review accepted the corrected count reconstruction, refreshed hashes and
all five checkpoint files without remaining corrections.

The two implementations agree on both shortest words, all14 witness
states,12 forced transitions and all14 full edge-count tables. The lead
also verifies the complete reverse-distance inequalities on47,104 edges,
the forward discovery/edge transcripts, the image-prefix base cases and
the old/new u-endpoint linkage. Source, input, original payload/raw and
reference hashes are checked after JSON round trips.

Records in `results/problem1/`:

- `20260905_zero_cost_return_primary.json`: completed forward searches,
  parent/distance/edge transcripts, actual witnesses, original source and
  all runtime/input/source/payload provenance.
- `20260905_zero_cost_return_independent.json`: cell/odd-section reverse
  graph, complete distance map and independent full-word replays.
- `20260905_zero_cost_return_verification.json`: complete certificate
  comparison and the representation/image scope checks. Independent and
  verification sources support RULE30_REPLAY_ROOT and RULE30_REPLAY_OUTPUT.

Runs stayed local within120seconds and1GiB. The immutable reference is
unchanged. No frontier set, new motif or linear program was generated.
The graph's finite size follows from the fixed block precision; it is
not a complexity cutoff on ordinary histories.

Next target (`inconclusive`): refine the zero-cost language to histories
of the form H(v)+Q with an ACTUAL preceding forced gate, then require
the following six branches. Derive the sufficient residue precision and
the output-edge cost before running that graph. This tests the surviving
prescribed-history hypothesis directly; another arbitrary zero-cost
history would not do so. Even success there would not yet exclude the
near-boundary return layers. B_all, signed nonvanishing, and the original
whole-tail question remain open.
