# Full ordinary membership at the existing decoder base

Status: `finite-exhaustive` for the fixed membership decisions; `refuted`
for the empty-base hypothesis and the inclusive-base backward claim below.
The all-depth induction remains `inconclusive`. Problem1 remains open.
Base checkpoint: `e6ae2ddf1303180c7c873a08c6c1e104f67dabd6`.

## Question and admitted computation

The composed-inverse checkpoint refutes backward closure from a short valid
future, but not the restriction to sufficiently deep ordinary endpoints with
long observed words. The earlier decoder experiment tested153 leading-core
candidates (120 p,k19 and33 u,k18), each with11 observed admissible branches.
It did not decide their full ordinary membership. This is a missing finite
base decision, not an invitation to enlarge the candidate set.

Ranked routes (`heuristic`): decide that existing base exactly; seek a
membership-preserving reduction for the all-depth long-word family; or
return to an inequality for the established boundary sum. The latter two
still require a structural lemma, not a larger census.

Hypothesis for this run: none of the153 existing decoded candidates is
ordinary in its specified phase and original complexity. A positive word
would refute this stronger base exclusion and force the proposed induction
to retain the actual-return condition. A complete negative certificate would
establish a finite base case only. It would not establish the induction,
B_all, eventual-alternation exclusion or Problem1.

Read only the153 candidate integers already stored in
`results/problem1/20260905_decoder_inverse_primary.json`, under the embedded
decoder run. Decide membership by the exact signed-generator predecessor
recursion with phase-root and bit-length gates. Each positive verdict needs
an explicit ordinary word; each negative verdict needs a complete dependency
DAG or a previously proved, correctly aged leading-head rejection. No
positive inverse or compatible leading block counts as membership.

Limits: one local process, CPU120seconds, wall180seconds,1GiB address space,
100000 memo nodes. At a cap, record unresolved candidates as inconclusive
without extending it. There is no new decoder, frontier, root BFS, suffix
word generation, branch atlas or return census. Hand controls are the two
level-two frontiers and the established signed inverse examples. The run
must write atomic JSON with exact inputs and parameters, full Git,
source/input hashes, timings and hardware/software facts. Independent
verification checks every retained edge and every candidate verdict using
a different arithmetic implementation.

## What a base result can imply

For p,k>=19, the existing core decoder uniquely determines a candidate from
r=k-8 observed branches; for u,k>=18, it does so from r=k-7 branches.
At the two base levels r=11 in both phases. If all accepted candidates are
rejected by full membership, no ordinary endpoint at either base level has
an admissible11-branch prefix. The decoder already certifies that the other
branch words have no head-compatible candidate, so this finite implication
is complete at those two levels.

This exclusion, if proved, would be stronger than absence of a genuine
three-return occurrence in the corresponding raw-empty layers. It still
does not say anything about k19 in u, k20 in p, or any later level without
an additional argument.

A possible all-depth induction would need to turn any later ordinary
long-word counterexample into an earlier one, retaining full ordinary
membership and the required actual gates. The inverse sign criterion alone
cannot do this. Neither the current nonordinary decoder counterexample nor
the ordinary short-future counterexample resolves this restricted step.

## The base has three ordinary endpoints

Exactly three of the153 candidates are ordinary. The following words INCLUDE
the phase root, unlike the primary raw word fields, which omit it.

| Phase,k | Endpoint | Rooted ordinary word | Complete admissible forced word |
| --- | --- | --- | --- |
| u,18 | 0x6473d46ab | uutuuttuupupuuupup | ttttutututu |
| u,18 | 0x6473d46c7 | uutuuttuupuputuuut | utttutututu |
| p,19 | 0x37b38b3bc7 | pupututuuuptutttpup | uttuttuttutu |

The primary's indices are12,115,127 in the original candidate order. The
last word has12 actual branches, although the decoder used only its first11.
Each complete word ends because the next gate is undefined. These are actual
ordinary endpoints with long words, not leading-core-only candidates.
The first endpoint and its ordinary membership were already known from the
deeper return/deletion examples. The new result is the complete membership
classification of the existing153-row decoder set, not discovery of that
old witness.

This refutes the stronger empty-base hypothesis. Genuine canonical return
cuts are respectively {4}, {0,4}, and {0,3}. The stored decoder field
`occurrences=[]` was restricted to its declared near-boundary layer; it
does not mean these endpoints have no occurrences at any cut.
All listed cuts lie below the tested raw-empty thresholds11 in u and13
in p. No boundary bound or signed-nonvanishing conjecture is refuted here.

## Follow-up admission after the nonempty base

The primary reports three ordinary candidates. For ONLY these three, decide
full ordinary membership of their six forced predecessors, all of which
were already computed and stored in the previous decoder-inverse record.
Retain the admissible-prepend filter on the entire observed word, and replay
their already recorded complete trajectories. This adds no candidate integer
or decoder word. A failed admissible ordinary predecessor would refute the
long-word backward claim at that base level, but not an induction restricted
strictly above the base or to near-boundary return cuts. A successful
predecessor needs an explicit root-reaching word. The same exact recursion,
independent verification and resource/provenance rules apply.

## Long-word backward closure already fails at the base

All six stored forced predecessors are positive but nonordinary:

| Original endpoint | Prior t predecessor | Prior u predecessor | Admissible prepend |
| --- | --- | --- | --- |
| 0x6473d46ab | 6723009195 | 6723009223 | u only |
| 0x6473d46c7 | 6723009275 | 6722787223 | t only |
| 0x37b38b3bc7 | 59712243451 | 59703716759 | t only |

The u targets must belong to O_(u,17), and the p targets to O_(p,18), to
provide an ordinary predecessor. Exact recursion rejects every one. The
two inverse branches are exhaustive by the established triangular bijection;
there is no third forced predecessor to search for. Their signs and values
were already stored in the earlier inverse record; this follow-up adds
full ordinary membership, not a larger inverse search.

Consequently the claim that every ordinary endpoint at or above the decoder
base with r>=k-8 in p or r>=k-7 in u has an admissible ordinary forced
predecessor is `refuted`, even when a genuine three-return occurrence is
also required. Each example is at the BASE itself. This is not a
counterexample to closure restricted STRICTLY ABOVE the base, or to closure
conditioned on a near-boundary actual-return cut. A proposed descent of a
boundary counterexample must preserve that stronger cut condition, not only
long-word ordinary membership.

## Verification and provenance

The primary uses the exact base-four lift recursion without head pruning,
visiting6485 memo nodes and7711 retained parent attempts across the153
independent input oracles. The150 negative certificates contain6252 nodes
and7454 edges. The independent verifier checks every such node and every
eligible lift edge, including completeness and phase-root rejection.
Positive certificates are checked by full ordinary word replay.

The independent membership engine instead solves the forward generator
equations bit by bit for their signed inverses, then tries all three direct
generator parents. It agrees on all153 verdicts and all six predecessor
rejections. Its combined graph has11499 nodes, including small controls
and the added predecessor queries. No frontier, decoder or word census is
constructed in either implementation. The existing complete trajectories
of the three members are replayed with every actual gate checked.
The separate independent lift calculation for the six stored predecessors
has48 nodes and47 edges; the arithmetic verifier checks every one, as
well as all three genuine cut sets and admissible-prepend lists.

The raw primary omits its run-start timestamp. The wrapper supplies its own
packaging timestamp and separately labels the original file modification
time; neither is claimed to recover an unrecorded start time. The primary's
clean Git-status field excludes untracked files; the pre-existing untracked
files were present and preserved. Original sources, numerical results and
hashes are retained without post-hash editing.

Records are `results/problem1/20260906_decoder_full_membership_` followed by
`{primary,independent}.json`. Extract the independent `source_text` and run
from the repository root to replay; RULE30_REPLAY_ROOT and
RULE30_REPLAY_OUTPUT override the input root and output location. The source
needs only committed inputs, not the original temporary paths. Timings,
full Git, software/hardware facts and atomic-write provenance are recorded.
Final four-file review accepted the mathematical scopes and provenance;
its isolated replay matched all verdicts, ordinary rows and the full direct
membership DAG. Different valid rooted words in the two engines were
separately replayed rather than mistaken for a discrepancy.

The remaining long-word route must use a reduction strictly above a
nonempty base AND retain the actual boundary-return condition, or abandon
backward induction for a direct exclusion. The three base words are finite
exceptions to stronger proposed exclusions, not evidence of infinite
survival. No larger decoder scan is justified by this result. B_all,
return-conditioned signed nonvanishing and Problem1 remain open.
