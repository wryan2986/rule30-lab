# Joint constraints on sixteen-state history potentials

Status: `partial-proof` for exact feasibility and all-coefficient separation
on the fixed six constraints; `finite-exhaustive` for their replay. Universal
descent remains `inconclusive`. Problem1 remains open.
Base checkpoint: `e6ae2ddf1303180c7c873a08c6c1e104f67dabd6`.

## Admission and route

The four-state additive potential class is already refuted, and particular
sixteen-state counts W_0t and W* have verified counterexamples. Those facts
do not refute the entire class of fixed edge weights indexed by old prefix
residue modulo16 and input generator. Testing whether the already certified
blocks admit ANY such weights is a distinct question from repeating those
individual potential tests.

Use only the six existing rooted histories: u14/0x642fdfb at cut1,
u18/0x6473d46ab at cut4, p12/0xc84387 and u15/0x191cc387 at cut0,
p19/0x32173ffdfb and u16/0x6f34fdfb at cut1, all with gaps222.
Their words are supplied by the history-potential, zero-cost-language and
prescribed-cost notes. Apply the actual prescribed scanner updates; do not
reselect a representation. Verify the entire observed prefix and the
unobserved final-u admissibility convention.

First seek a nonzero nonnegative integer combination of the six48-component
edge-count differences that is componentwise nonnegative and has zero graph
divergence. The declared coefficient box is0..4 in each of six coordinates,
excluding the zero tuple:15624 combinations. A certificate would rule out
the fixed shared sixteen-state potential class by cycle pumping. Finite
absence would leave the class open and would not justify enlarging the box.
No new starting words, endpoints, occurrence census, frontier or solver
installation is admitted. Local CPU120seconds, wall180seconds and1GiB;
atomic standard-protocol records with full sources and provenance.

After bounded absence, admit an exact separator check on the SAME six
vectors. The lead's proposed nonnegative weight vector is

    Wdagger=N_(0,t)+N_(1,t)+N_(1,u)+2N_(6,t),          (1)

with residues modulo16 and the fixed root excluded. If its dot product
with each change vector is negative, then no nonzero nonnegative REAL
combination of those six changes can be componentwise nonnegative. This
would be an all-coefficient statement about the fixed six vectors, not a
universal descent theorem. It also supplies a concrete next potential to
falsify. This additional check needs no coefficient-box increase.

## Combination and separation lemmas

Status: `partial-proof`.

Let omega be fixed real edge weights on the16-state ordinary residue graph,
with one lower bound on path weights over all histories from either root.
Every reachable directed cycle must have nonnegative omega weight, since
otherwise it could be repeated to violate the lower bound.

If Delta_i is the prescribed edge-count change of a genuine block and a
nonzero coefficient vector alpha_i>=0 makes D=sum alpha_i Delta_i a
nonnegative circulation, then omega·D>=0 by cycle decomposition. Strict
descent on every selected block would imply omega·D<0, a contradiction.
Rational coefficients can be cleared to an integer circulation. For real
coefficients the finite nonnegative circulation decomposes into cycles
with nonnegative real weights. Blocks of different phases can be combined
only when omega is shared; this does not refute independently phase-indexed
weights.

Conversely, if some w>=0 has w·Delta_i<0 for every i, then D cannot be
componentwise nonnegative for ANY nonzero alpha>=0, with or without the
circulation requirement: w·D is strictly negative. Such a w is an exact
feasibility certificate for the listed finite descent constraints. Its
nonnegativity supplies a uniform lower bound0 on every ordinary history,
but its descent is still only verified on the selected blocks.

## Exact separator for the six constraints

The weight vector in (1) gives the following changes under the actual
prescribed six-step block:

| Input, original cut | Wdagger change | Terminal residue change modulo16 |
| --- | --- | --- |
| u14,1 | -2 | 7 to7 |
| u18,4 | -2 | 7 to7 |
| p12,0 | -2 | 7 to15 |
| u15,0 | -1 | 7 to7 |
| p19,1 | -1 | 7 to11 |
| u16,1 | -1 | 7 to15 |

These exact six dot products prove there is NO nonzero nonnegative real
combination of these differences that is componentwise nonnegative, even
if the divergence requirement is dropped. Thus increasing coefficient
sizes cannot turn these same six inputs into a circulation obstruction.
This is an all-coefficient conclusion about six FIXED vectors. It does not
establish decrease on any other block.

The original bounded cube had15624 nonzero tuples, all failing the desired
circulation test; its raw parameter15625 counts the zero tuple too. The
all-u subcube had624 nonzero tuples, not625. The exact separator supersedes
both bounded absences, so neither cube needs enlargement or repeated
enumeration. Nonzero-divergence rows cannot automatically be treated as
cycles: the p12, p19 and u16 terminal residues differ from their starts.

## Independent verification and next gate

Muse computed the original six prescribed history pairs and a separate
separator replay. The lead independently used cell-array generators and
the odd-section formula for P. All49 listed states,43 prescribed updates,
the two complete48-component count tables per block, all six difference
vectors and their divergences agree. The exact separator gives changes
(-2,-2,-2,-1,-1,-1). No coefficient enumeration is repeated by the lead;
the separating weight vector is a stronger certificate.

The records are `results/problem1/20260906_sixteen_potential_` followed by
`{primary,independent}.json`. The primary preserves both received raw records
and sources. The raw `self_sha256` fields hash executed source, not their
JSON bodies; its post-run all-u scope refinement has a separate verified
hash. Packaging and computational timings are distinguished. The independent
embedded `source_text` runs from the repository root, with optional
RULE30_REPLAY_ROOT and RULE30_REPLAY_OUTPUT, and needs no original temporary
paths. Full Git, exact parameters, hardware/software and atomic hashes are
retained.
Final four-file review accepted the combination/separation arguments and
all finite scopes; its isolated replay matched every summary and row field,
with current Git provenance distinguished from the original base commit.

The next discriminating hypothesis is universal descent of this SPECIFIC
new Wdagger. A zero-cost ordinary history with a genuine ututut occurrence
would refute it immediately, since its final cost is nonnegative. The
existing fixed16384-state zero-cost language construction can decide that
question without increasing the graph size or an ordinary frontier. No such
new-weight graph run is part of this record. Absence of a zero-cost word
would prove only positive initial cost on that motif, not strict descent.
Do not infer a theorem from fitting these six witnesses, and do not enlarge
the old coefficient box: this explicit separator already settles it.
