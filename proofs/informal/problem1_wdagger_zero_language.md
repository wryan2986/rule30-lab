# Testing the separating potential on its zero-cost language

Status: `refuted` for universal strict Wdagger descent; `finite-exhaustive`
for the fixed graph certificates; `partial-proof` for separation of the
four closed constraints at every coefficient size. Problem1 remains open.
Base checkpoint: `b0f81633845b86599560b640bb6f88e72f77b4bf`.

## Admission and exact reduction

The six-block separator Wdagger=N_(0,t)+N_(1,t)+N_(1,u)+2N_(6,t)
is nonnegative on every ordinary history, but its strict descent has only
been checked on six fixed blocks. The next falsifiable claim is universal
strict decrease over a genuine three-return block with prescribed histories.

Use ONLY the previously studied motif ututut. Its six actual branches
correspond exactly to residue903 modulo16384; the following admissibility
u is unobserved. Apply the already proved exact zero-cost-language theorem
at this same16384-state graph size, with the new zero-cost edge set:

- disallow T at old residue0,1,6 modulo16;
- disallow U at old residue1 modulo16;
- allow every P edge and all other T/U edges.

The weight2 on edge(6,t) has no effect on which paths cost zero. The graph
has16384 vertices and45056 allowed labelled edges. Start separately at the
phase roots3 and1. Breadth-first search supplies a shortest zero-cost word
to903 if reachable; otherwise its full reachable closure excludes every
zero-cost ordinary history of that phase at every history length.

A zero-cost ordinary witness would refute universal strict descent of
Wdagger because its final cost is nonnegative. Absence would establish
positive initial cost on this motif only, not descent. Either outcome
changes the potential argument. This is a new weight support on the fixed
existing graph, not a larger frontier or repetition of the W* calculation.

Limits: one local CPU,120 CPU seconds,180 wall seconds,1GiB address space;
no width, motif, frontier or coefficient-cap increase. Store exact graph
distance/parent certificates, recovered ordinary words and endpoints,
all six actual gates and prescribed updates, and full48-component cost
tables. Verify small Boolean/packed controls before the graph and require
independent certificate replay before adopting a claim. Atomic JSON must
include exact parameters, full Git, source/input hashes, timing and
hardware/software facts. Do not scope-edit a raw record after hashing it.

## Recovered completed results

These records were already present, untracked, at continuation start. The
graph search was not repeated. The stored independent cell implementation
was replayed to verify the full graph certificates and the witnesses.

Status: `refuted` on these ordinary histories, with cut0 and gaps222:

| Phase | Initial k | Word FROM ZERO (root included) | Endpoint | Wdagger before, after six prescribed steps |
| --- | --- | --- | --- | --- |
| p | 14 | ptuuupttuttttp | 0xde68387 | 0,0 |
| u | 18 | upuuutututttututup | 0x642e4c387 | 0,1 |

Both endpoints have the six actual branches ututut, with admissibility word
utututu; the last u is unobserved. Both violate universal strict decrease,
and the u example also violates nonincrease. All six updates use the
prescribed scanner histories, without choosing new representations.
Their terminal residues modulo16 change respectively7->3 and7->7.
These cut0 examples do not refute a positive prescribed-age restriction
or the near-boundary restriction relating cut to ORIGINAL complexity.

Status: `finite-exhaustive`. Each root reaches all16384 vertices of the
45056-edge zero-cost graph. The shortest accepted nonroot word lengths
are13 in phase p and17 in phase u. Minimality is only within this exact
zero-cost language, not among all counterexamples to descent. Stored
forward parent/distance certificates satisfy every edge inequality, and
the independent reverse distances give the same root distances. The
all-length interpretation follows from the exact language theorem; no
finite frontier is extrapolated to an all-depth assertion.

## Why the four closed constraints still cannot obstruct the class

Status: `partial-proof`. For an edge-count difference D=N_final-N_initial,
using outgoing-minus-incoming divergence, a block starting at residue7
and ending at e has div(D)=delta_7-delta_e. All the eight stored blocks
start at7. In a nonnegative combination of their differences, divergence
at any e!=7 is minus the sum of coefficients of blocks ending there.
Consequently a circulation combination must assign coefficient0 to every
block ending away from7. This excludes the four open blocks algebraically,
not by selecting favorable examples. This assertion concerns these
ututut blocks, not every possible three-return motif.

The four remaining closed blocks are the previous u14, u18 and u15
blocks and the new u18 zero-cost block. The nonnegative weight vector

    V=N_(3,t)+N_(3,u)              (old prefix residues modulo16)

has dot products(-1,-1,-1,-4) with their differences. Therefore no nonzero
nonnegative REAL combination of these four differences is componentwise
nonnegative: pairing such a combination with V gives a strict negative
number. Together with the divergence argument, this excludes a nonnegative
circulation combination of ANY of these eight differences at ANY coefficient
size. It does not show that V decreases on the four open blocks or on all
ordinary return blocks, and does not refute the sixteen-state potential
class. Phase-dependent weights are not mixed by this argument; the four
closed examples all have phase u.

The stored624-tuple search (coefficients0..4, excluding0) is superseded
by this exact separator. No coefficient-cap increase is justified.

## Verification and provenance limits

Records: `results/problem1/20260906_wdagger_zero_` followed by
`{primary,independent,verification}.json`. The primary preserves original search and
closed-constraint JSON/source bytes and the original admission-note snapshot.
The independent source is portable via RULE30_REPLAY_ROOT and
RULE30_REPLAY_OUTPUT. The continuation replay agrees on the complete
summaries and certificate rows, both graph distance systems, all14 states,
all12 prescribed updates, all four48-component count tables, the four
closed divergences, and all four separator dots. It regenerates the fixed
graph by cell arithmetic to CHECK its certificates, not a new frontier.
No new word or motif search was performed by the continuation.

The raw primary small controls compare T with Boolean arithmetic; its U
check is definitional and its P mismatch branch is a no-op. Those controls
alone would be inadequate. The independent full-edge and witness replay
uses a separate Boolean formula for all three generators, including P,
and supplies the missing check. Original computational runtimes (about
0.193s and0.015s) remain separate from packaging time. Raw timestamps
and fields labelled preregistered are preserved as recorded; packaging
does not establish independent evidence of preregistration chronology.
Source hashes are source hashes, not hashes of their containing JSON.
The source reference was not modified.

Two fresh Muse audit attempts returned provider HTTP429, so the lead
performed certificate replay locally rather than substituting another model.
The lead also derived all12 prescribed histories independently using the
original-prefix and birth-position formulas. The compact verification record
stores this audit and its exact input hashes. The older independent cell
record and the current replay are distinct from a successful fresh Muse
review; no successful fresh Muse review is claimed.

## Next discriminating question

Universal Wdagger descent is closed. The sixteen-state bounded-below
additive class is still open, but increasing coefficients on these eight
vectors cannot refute it. A new test must address a structural constraint
on the class, or explicitly retain prescribed age versus initial length.
Merely fitting another potential to a finite witness list is not a descent
proof. Actual return exclusion, B_all and Problem1 remain open.
