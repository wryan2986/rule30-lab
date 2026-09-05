# Testing additive history potentials at a three-return block

Status: `partial-proof` for the pumping/circulation argument; `refuted`
for the universal four-state additive descent class specified below;
`finite-exhaustive` for the fixed history and scope checks. Independently
derived and adversarially reviewed.
Base checkpoint: `fb39f7bb01374b69c4a42b47799784658eb72d07`.
Problem 1 and all-occurrence boundary bounds remain open.

## Bottleneck and route selection

The latest dominant-empty boundary theorem requires L<=k-4 for a
nonempty dominant certificate when k>=6; it does not exclude any genuine
return occurrence. The underlying whole-tail route needs a finite bound
on admissible occurrence cuts for every initial ordinary frontier state.
A lower-bounded potential decreasing by a uniform positive amount across
successive nonoverlapping three-return blocks would supply such a bound.
No such potential is currently established.

Ranked candidates (`heuristic`):

1. Additive potentials on the exact history scanner, with decrease over
   whole three-return blocks. Direct all-depth potential if successful;
   plausibility uncertain, falsifiability high and initial cost low.
2. Additive potentials with more scanner memory or return-state memory.
   Same potential relevance, but a larger class and higher certificate
   cost; specify the state graph before any additional test.
3. A reset-propagation or cycle-uniqueness argument for A. Its connection
   to the growing forced history is weaker: finite-width head membership
   propagates automatically. Moreover the simplest reset premise already
   fails: A(6)=6 has low bit identically zero. Its next-bit lift flips,
   rather than splitting; this does not refute cycle uniqueness itself.

Choose route 1 and falsify before attempting a long proof. An initial
single-step argument used the wrong history for7: T(1)=7 but U(1)=6.
The actual phase-u history update at7->27 is t->pu, with count difference
(-1,+1,+1) in (t,u,p). Thus this example does NOT refute decreasing
nonnegative letter potentials. The independent cell replay caught the
mistake; the proposed single-step obstruction is withdrawn. The whole
block test below has its own independently verified input history.

Initial proposed input x=903=0x387, cut0, gaps222 was selected from the
finite-integer repetition note. That note did NOT assert its ordinary
membership. The membership gate rejects it: its projected head225 is
absent from O_(p,4), so it cannot be in O_(p,5). Thus treating it as an
ordinary occurrence was a scope error, corrected before any proof claim.
It is retained only as a membership-rejection certificate, not as a
counterexample on the genuine occurrence domain.

Replacement admitted test: the already certified phase-u,k14 endpoint
x=0x642fdfb, cut1, prefix t, gaps222. Its known FROM-ZERO word is
uuuuputptuutuu; the first u supplies root1 and the other13 letters form
the ordinary history. Verify this word, apply one forced t to reach the
cut, then the six observed branches ututut. Compare the histories at
times1 and7, retaining each intermediate word and endpoint. Also retain
the hand check7->27. Compare letter counts and the twelve counts
of (old prefix residue modulo4, input generator). Check whether any count
difference is componentwise nonnegative. A positive witness refutes the
corresponding universal strictly decreasing additive certificate; absence
would leave that class unresolved on these constraints, not prove it.
No enumeration of alternate representations is yet admitted. No additional
occurrence census, new endpoints as starting cases, or
longer schedule horizon is admitted. Local CPU,120seconds,1GiB, atomic
records with exact source, input hashes, full Git and runtime provenance.

After both implementations confirmed the four-state circulation, admit one
scope check on the SAME two words: lift edge labels to old prefix residue
modulo16, the exact scanner's stopping-gate state. If their count difference
is still nonnegative, the same proof extends to that richer additive class.
If an edge count decreases, counting that edge alone is a nonnegative
potential that decreases on this pair; this prevents extrapolating the
four-state obstruction to the sixteen-state class. It would not establish
a universal potential. No new histories or forced steps are admitted.

## Exact history dynamics

Use the generators, roots and scanner theorem from
`problem1_frontier_head_dynamics.md`. A history is ANY finite word over
{t,u,p} applied to root3 (phase p) or root1 (phase u). Every such word
represents an ordinary frontier endpoint. Distinct histories need not
represent distinct endpoints.

Let H be the scanner for A, retaining the root:

| Old prefix residue | Next residues for t,u,p | Emitted letters for t,u,p |
| --- | --- | --- |
| 0 | 0,1,3 | t,u,p |
| 1 | 3,2,2 | p,p,p |
| 2 | 2,3,1 | p,p,u |
| 3 | 1,0,0 | u,t,t |

For endpoint x with x mod16=7, append u to H(w); with residue11 append t.
Otherwise no forced step is defined. The resulting history represents
F(x)=4A^2(x)+3. The old prefix residues used by H are those obtained while
reading the old word, not the emitted word. History length increases by
one at each forced step. This is not a finite endpoint quotient.

## Obstruction for a bounded-below edge potential

Claim status: `partial-proof` (all-depth, no finite extrapolation).
Assign a fixed real number omega(r,g) to every directed edge
of the four-state input-residue graph above. Let

    W(w)=sum omega(r,g) along the history path from its phase root.

Require one lower bound for W over ALL finite ordinary histories from
that root, not merely over the finite test domain. Weights need not be
nonnegative. Every directed cycle reachable from the root must then
have nonnegative total weight: a negative one could be repeated
arbitrarily often after a path reaching it, contradicting the lower bound.
All four residues are reachable from either root.

Suppose two histories from the same root have the same terminal residue,
and their edge-count difference N_final-N_initial is componentwise
nonnegative. The difference has zero net divergence at every vertex,
since the two path divergences agree. It is therefore a nonnegative
integer circulation, decomposable into directed cycles. Summing the
nonnegative weights of these cycles gives

    W(final)-W(initial)>=0.

Thus a single genuine block whose prescribed history update has such a
count difference rules out strict block decrease for EVERY potential in
this class, provided the claimed decrease quantifies over all initial
representations. Adding a potential of the terminal residue does not
change this obstruction because those residues agree.

This argument does not rule out a chosen representation with a different
update, finer state memory, a nonlinear function, or a criterion allowing
some blocks to increase and proving a net decrease over longer groups.
An existence-of-shadow statement also does not require any such potential.

## Concrete circulation certificate

Status: `finite-exhaustive` for the named certificate; `refuted` for
universal strict block descent in the stated class. Two implementations
verify the known input history,
the observed seven-branch word tututut, and these two histories from root1:

    time1: pptpttpuppuppt
    time7: ppttpupttpupppptuppt.

The exact orbit certificate is:

| Time | Endpoint | Observed next branch |
| --- | --- | --- |
| 0 | 0x642fdfb | t |
| 1 | 0x191cc387 | u |
| 2 | 0x642e3dfb | t |
| 3 | 0x191cf5387 | u |
| 4 | 0x642e4d1fb | t |
| 5 | 0x191cf07287 | u |
| 6 | 0x642e5db8bb | t |
| 7 | 0x191cf1bfd37 | not executed in this check |

The comparison is across the actual occurrence at cut1, with motif ututut.
The appended admissibility-test u is not an observed eighth branch.
The change in letter counts (t,u,p) is (2,1,3). The change in residue-edge
counts is one on each of

    (0,t), (0,p), (1,p), (2,u), (3,t), (3,p),

and zero on the other six edges. Both paths end at residue3. The added
circulation decomposes into these three directed cycles:

    0 --t--> 0;
    0 --p--> 3 --p--> 0;
    1 --p--> 2 --u--> 3 --t--> 1.

The certificate's exact consequence is

    W(time7)-W(time1)
      = omega(0,t)
        + [omega(0,p)+omega(3,p)]
        + [omega(1,p)+omega(2,u)+omega(3,t)] >=0.

Each bracket is a reachable cycle weight and hence nonnegative under the
all-history lower-bound premise. This refutes universal strict decrease
over each genuine admissible three-return block for that potential class.
It also rules out any representation-independent endpoint potential
expressible by this additive formula. It does not rule out a selected
history with a different update or state-dependent extra memory. The
witness is phase u. It excludes a simultaneous both-phase descent theorem,
but is not a counterexample to a phase-p-only claim. Requiring a uniform
positive drop on every block is stronger than strict decrease, so that
version is refuted as well.

## Exact limit of the four-state obstruction

Claim status: `finite-exhaustive` for these two words; `refuted` for the
claim that THIS nonnegative circulation lifts to the sixteen-state graph.
Both paths end at residue7 modulo16, but their refined edge-count
difference has three negative entries:

| Old prefix residue modulo16 / letter | Initial count | Final count |
| --- | --- | --- |
| 0,t | 2 | 0 |
| 3,u | 1 | 0 |
| 15,p | 1 | 0 |

All 48 refined counts agree between independent implementations, and
coarsening residues modulo4 recovers exactly the previous 12-edge vectors.
In particular W(w)=the number of T edges entered at residue0 modulo16
has lower bound0 on every history and decreases by2 on this pair. Thus
the fixed pair cannot rule out the sixteen-state additive class. This is
one decreasing instance, not a universally valid potential, an all-depth
descent theorem, or evidence for a boundary bound.

## Verification and remaining work

The primary packed/scanner implementation and independent cell/odd-section
implementation agree on all eight genuine states, seven prescribed
updates, all eight 12-edge count tables, and the three-cycle decomposition.
The same pair's 48 refined counts and the three negative refined entries
also agree. The independent scope audit checks all 33 final-generator
rejections for903 and the corrected t->pu single-step control.
No alternate representations or new occurrence census were run.

Muse Spark 1.3 Contributor independently derived the cycle-pumping argument
and reviewed the word-count and refinement scopes. The lead checked the
actual endpoint arithmetic separately rather than adopting hand inputs
without verification. Fresh adversarial review accepted the all-history
lower-bound premise, circulation proof and representation scope. Its
correction to the list of surviving approaches is incorporated below.
The final read-only integration review independently compared all shared
finite fields and validated all three original source/raw/payload chains,
selected-input links, aggregate timing, verification-file hashes and the
immutable-reference hash. It approved the final scope with no remaining
correction and repeated no scientific run.

Atomic records in `results/problem1/`:

- `20260905_history_potential_primary.json` retains all three original
  worker records (genuine word,903 rejection,16-state refinement), exact
  sources, raw traces and runtime/input/source/payload provenance.
- `20260905_history_potential_independent.json` contains the standalone
  cell/odd-section replay and complete count tables.
- `20260905_history_potential_verification.json` compares those records,
  the count/cycle certificates, and the full original hash chain. Its
  source uses committed inputs only. Independent and verification replay
  support RULE30_REPLAY_ROOT and RULE30_REPLAY_OUTPUT.

The primary aggregate runtime is the sum of its three original run
timings, not a claim about contiguous elapsed time. Original primary
sources retain their historical temporary paths; their intermediate
records and raw data are embedded, while the shared frontier input remains
in its committed file under the recorded hash. The verification source
has no such temporary dependency. Runs stayed local and below120seconds
and1GiB; the immutable reference hash is unchanged.

This fixed occurrence does not claim global minimality and does not prove
a boundary bound. Any surviving approach must change at least one
premise: the additive four-state formula, the all-history lower-bound
domain, the universal representation/prescribed-update requirement, or
strict decrease on every block. Changing the twelve weights alone cannot
escape the obstruction.

Next targeted question (`inconclusive`): can the sixteen-state additive
class satisfy descent constraints simultaneously on already certified
return blocks? The present decreasing refined edge count supplies a
concrete candidate to falsify on another named block, before any search
over a larger input set. If testing the full class, require an exact
potential or a rational cycle/inequality obstruction; numerical LP
feasibility alone is not a proof. B_all, dominant nonemptiness, signed
nonvanishing and the original whole-tail target remain open.
