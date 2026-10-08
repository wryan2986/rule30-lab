# Sol research handoff — 2026-10-08

Problem 1 remains **OPEN**. This is the current compact handoff for this
goal. Historical ASTRA-named files are research material; they do not
authorize use of Astra.

## Current checkpoint — 2026-10-08

This section supersedes the historical statements below that call depth four
or five the first unresolved affine-extension depth. This session recovered
the latest remote `research/sol-blind-frontier` at
`ddc53f28dbe30a98764f3dec8a7725ec5be1dbe8`, including its corrected depth-five
product encoding. The corrected graph is independently verified again:
16,384 states, 33,152 retained edges, 160 bad edges, and no bad edge on a
directed cycle. The new verifier uses literal raw Rule 30 transitions and
per-edge return reachability, with no imported producer transition, SCC, or
rank routine.

The principal new results are stronger explanations, rather than a
larger observer census:

1. **Exact all-width common-output language.** A blind transition has a
   16-context raw preimage automaton, 11 reachable deterministic subsets,
   and an eight-state quotient. Its infinite common rows are
   `01(111)^omega`, or `01(111)^k 0 v` with
   `v in {0,110,111}^omega`. The proof is a local path correspondence at
   arbitrary width, not an extrapolation from the depth-eight controls.
   A complete eventually-zero common row has exactly one ordered raw
   preimage pair; one row is eventually zero and the other eventually one.
   Read `proofs/informal/problem1_blind_image_language_20261008.md` and its
   independent review.

2. **Short proofs of S4 and S5.** Every cyclic blind source at depth at
   least three has low-three-pair encoding 35 or 51. Its common blind
   output at depth five begins `01011` or `01111`; in particular, common
   output bits four and five equal one. At observer depth four or five,
   the next, necessarily common-label edge therefore resets every added
   child-copy difference. Following this reset around any product cycle
   excludes every bad gate edge. No driver parity or nonzero-parent
   hypothesis is needed for S4/S5 themselves. This supplies a short local
   proof in place of dependence on the large product-graph calculation.
   Read `proofs/informal/problem1_shallow_cyclic_reset_review_20261008.md`
   and `proofs/informal/problem1_all_depth_gate_candidate.md`.

3. **The unqualified temporal reset bridge is false.** A genuine transient
   blind source at depth five has the exact path
   `255 -> 4 -> 90 -> 162 -> 194 -> 995 -> 340`. Start two equal children
   at zero, use labels `(0,1)` on the first blind edge, then common labels
   `11100`. The final equal-label blind edge has unequal outgoing child
   Y bits. The raw last-parent no-reset products are `(1,0)`. The upper
   source cannot return to itself, so this is not a cyclic S5
   counterexample. Recurrence cannot be discarded in an all-depth proof.

4. **Exact period-two complete-half formulation and inverse support test.**
   At a center-one phase, encode the center and left half by `L`, and
   the complete right half by `R`. Write
   `Psi(L)=4 A^2(L)+3`, `D(R)=(R<<1) XOR (R OR (R>>1))`, and
   `F(R)=D(D(R) XOR 1)`. An alternating center is equivalent to the
   gate `L=7 mod16` when `R=0 mod4`, and `L=11 mod16` otherwise,
   at EVERY independent iterate `(Psi^m(L),F^m(R))`. This is a
   biconditional for arbitrary finite halves and allows a finite temporal
   rebase. Both bit lengths grow by exactly two, so their difference is
   neutral. The actual finite collision `Psi(171)=Psi(199)=811` has
   opposite gate branches; the left successor alone cannot select the
   correct predecessor. The complete right successor selects its unique
   finite predecessor and hence the left gate branch. A 16-state local
   inverse then has an exact terminal-zero test for whether that left
   predecessor is finite. This test is for one passage, not a finite-state
   model of the entire diagonal map or a proof of orbit termination.
   Read `proofs/informal/problem1_period_two_phase_maps_20261008.md`
   and its independent review. Literal full-row controls cover all 4,096
   specified half pairs; inverse controls cover both gate branches for
   every target below 4,096. The algebra supplies the unbounded claims.

All-depth cyclic gate transport remains open from depth six. Restricting
the exact regular-language search to the necessary cyclic shallow prefix
did not produce an inductive invariant: the exact automata reached the
stated state cap, and a widened counterexample was spurious. Increasing
the observer bound or accepting a widened witness is not a proof.

The global target remains the SAME ORIGINAL finite-support condition.
Even an all-depth affine extension theorem inside one fixed-period
connector would not prove the needed unbounded excursions

    limsup_n [tau(2^n v)-n] = infinity,  v>0 finite.

The fixed-period blind ambiguity already vanishes by depth `p` on the
even-period odd-driver domain. Connector lifetimes can be much greater
than that; no bound on those lifetimes or on reuse across zero returns
follows from the new shallow reset proof. Problem 1 remains **OPEN**.

For the precise relation between the complete-half gate, the inverse support
test, and this original-cut excess target, read
`proofs/informal/problem1_global_support_bridge_20261008.md`. A finite
inverse test is automatic on an actual finite admissible forward passage;
its repeated success is not a termination proof or a bounded support budget.

Reproduction of the completed independent checks:

    python3 experiments/problem1_nonperiodicity/analyze_blind_image_language_20261008.py
    python3 experiments/problem1_nonperiodicity/verify_blind_image_language_20261008.py
    python3 experiments/problem1_nonperiodicity/verify_depth5_gate_independent_20261008.py
    python3 experiments/problem1_nonperiodicity/analyze_gate_difference_reachability_20261008.py
    python3 experiments/problem1_nonperiodicity/verify_period_two_phase_maps_20261008.py

The corresponding `results/problem1/20261008_*.json` files separate finite
computation from mathematical implications and record exact domains,
resource limits, source and payload hashes, full base commit, software,
hardware, and timings. The original reference remains unchanged.

## Historical checkpoint — 2026-10-02

## Model routing

The user prohibits Astra for EVERY subagent, verification, fallback, and
final check. Use explicitly pinned free/cheap routes; if a route cannot
guarantee exclusion of Astra, do not delegate. Difficult issues return to
the Sol parent. The parent is configured as `gpt-6.1-sol`, effort `max`.
Space Bunny is available through `opencode-go/space-bunny-free`. Direct and
OpenCode Go DeepSeek attempts both failed with insufficient funds in this
session; these failures are not research results.
Explicitly pinned `gpt-6-luna`, effort `low`, also works for bounded
verification and independent logical review. Never use an unpinned
default or automatic escalation path.

## Repository recovery

The existing `/home/ryan/rule30-lab` checkout was at `2fee2dc` on
`research/astra-next`, with recovered untracked round308–312 drafts. Fetch
revealed it was 581 commits behind the remote. Those drafts and all other
local changes were preserved.

Current work is in an isolated worktree on `research/sol-blind-frontier`,
based on remote `7ee66c81e974106f6bd0d04607e24e2110e045ce`. Read
`ASTRA_AUTOMATION_HANDOFF.md`, particularly sections 20–24, for that newer
frontier. `ASTRA_HANDOFF.md` is an older incomplete checkpoint and is not
the latest frontier by itself. Do not redo the old p32 connector census.

The immutable reference still has SHA256
`358bdc07904e77080eb78b67bdd8da25822d6b51f1a91b58b5313dfe461c1d01`.

## Strongest recovered frontier

The normalized multilift portal system is exact at every finite depth.
Its transition is `T_w=G^w Phi_0`, with boundary pairs `(1,0),(0,1)`.
An aligned unlabeled orbit with `k_r` blind phases permits `2^k_r`
aligned labelings; known odd parity leaves affine dimension
`u_r=max(k_r-1,0)`. Blind phase sets are nested with depth.

The full p16 terminating leaf set and a certified subset of p32 leaves
show earlier ambiguity collapse than the ambient odd language, but these
finite facts alone do not provide an original-support charge. Raw blind
stacks of arbitrary depth exist. Finite A-cycle connectors do return to a
zero low plane; their enormous return lengths need no further blind scan.

The original all-period obstruction is still FULL versus one actual finite
original fringe. A sufficient scalar target for excluding every eventual
finite physical strip is

    limsup_n [tau(2^n v)-n]=infinity for every finite v>0.

Neither `tau(2^n v)->infinity` nor separated forced births proves this.
The residence ledger telescopes; the prior forced-birth budget is fenced off.
Period-8/16 K=3 exit exclusions do not establish all dyadic periods.

## New result: LEMMA WITH PROOF — INDEPENDENTLY CHECKED

Read `proofs/informal/problem1_cyclic_blind_cone_bound.md` and its review.

For ANY `p`-cyclic depth-`r` quotient orbit, with arbitrary binary driver
and the stated boundaries, blind visits have cyclic gaps at least

    g_r=max(2,floor(r/2)+1).

Therefore, all depths and all presentation periods satisfy

    k_r<=floor(p/g_r).

Consequences:

* depth `2p` is blind-free and its unlabeled orbit determines all labels,
  without parity conditioning;
* for even `p`, depth `p` already uniquely determines a known odd driver;
  for odd `p>=3`, depth `p-1` suffices;
* every finite or existing infinite fixed-`p` tower has

      sum_r u_r<=U(p)=O(p log p),
      U(1)=0,
      U(p)=2 sum_(q=1..p)floor(p/q)-4p+floor(p/2)+1, p>=2.

Proof mechanism: a blind transition produces zero difference coordinates.
From such a row, the rightmost forced discrepancy advances two dynamic
layers per time step. Cyclicity bounds return of blindness. The first
layer separately excludes consecutive blind visits. No finite ancestry
is required. The bound is sharp at depths one and two.

Verification: separate free-model symbolic review, parent re-derivation,
and independent two-row finite implementation. Exact finite checks include
10,920 transition comparisons, 5,850 zero-cone histories through depth eight,
45,080 driver/state pairs for p<=3 at depths r<=2p, and the named controls.
Finite evidence has its own status and is not promoted into the proof.

Reproduce:

    python3 experiments/problem1_nonperiodicity/check_cyclic_blind_cone_independent.py

The atomic JSON contains exact domains, source/payload hashes, full base
commit, resource caps, hardware/software, and timings.

## Sharper obstruction and next admissible question

The proposed fixed-period blind-rank charge is now universally finite,
even on the abstract driver domain. Thus finiteness of `sum_r u_r` for
one portal cannot distinguish finite root ancestry. It is also completely
accumulated by depth p-1 for even p, since u_r=0 from depth p onward;
it supplies no new positive ambiguity loss on the remaining long connector.

A viable charge must therefore have an exact transport law across a zero
return / portal restart or period doubling, together with bounded reuse
against the SAME ORIGINAL support. Neither is established. A precise next
question is whether there is an ancestry-compatible transport of individual
blind-phase labels through a return, with a proved nonnegative loss that
cannot be regenerated freely at the next portal. State that map and its
domain before launching a computation. Without such a map, do not expand
the p32 census or polish a fixed-period budget as a Prize Problem proof.

Failed closed forms and rejected reviewer claims are retained in
`proofs/informal/problem1_cyclic_blind_cone_review.md`. Commit this logical
unit without claiming a full Rule-30 solution.

## Second unit: FAILED — unweighted portal-charge nonincrease

Read `problem1_blind_charge_portal_transport_counterexample.md`.
For the complete eight odd singleton p32 root certificates, the COMPLETE
single-connector charge kappa increases from parent to returned leaf in
every case. Smallest tested portal index 2 has

    w=0101101101111011, kappa(w)=11,
    z=00001000111100010010101100101111, kappa(z)=26.

The raw returned phase has the same value. These are exact full charges,
because the cone theorem proves u_r=0 beyond the checked p-1 depths.
Actual first zero return is at 1,555,560,444 in the imported connector
certificate; a blind-free observer at depth six is NOT that zero return.

Free worker and independent Luna review agree on the eight numerical
pairs; the parent checked the code, corrected mistakes, and verified
deep transitions, blind predicates, and raw/canonical phase equivalence.
The input endpoints were imported and hashed, not traversed again.

Reproducer:

    python3 experiments/problem1_nonperiodicity/check_blind_charge_portal_transport.py

Thus even singleton period doubling regenerates the proposed unweighted
charge. The same witness has 26>2*11, so dividing the charge by its period
does not repair nonincrease. Do not use either as an ancestry potential, and do not
repeat nearby scalar monotonicity fits without a concrete transport law
that accounts for this regeneration. The unresolved requirement is still
an original-support resource with bounded reuse across these changes.

## Third unit: exact layer transfer and shallow label transport

Read:

* `proofs/informal/problem1_portal_layer_monodromy.md`;
* `proofs/informal/problem1_shallow_blind_label_affinity.md`;
* `proofs/informal/problem1_portal_label_transport_review.md`.

Status: **LEMMA WITH PROOF — INDEPENDENTLY CHECKED** at the scopes below.

For a fixed odd driver of ANY presentation period p>=1 and arbitrary
p-periodic upper pair histories, the added layer has an affine p-step
state return `V->A V+b`, with exactly four possible matrices:

    A=[[d1,d1],[d0+d1,d1]], d0,d1 in {0,1}.

Here d_i says that the corresponding raw parent half has no reset.
A nonzero parent gives `d0*d1=0`, `A^2=0`, and a unique cyclic added
pair `V*=(I+A)b`. Every seed synchronizes after at most two aligned
p-step returns. A zero parent gives `A=G`; there are no cyclic extensions
if `b_Y=1`, and exactly two if `b_Y=0`. Explicitly `b_Y=XOR_s K_s`, the
parity of the HIGHER raw track. This formula is affine in the added
state for a fixed driver; it is not a driver-affinity theorem.

For every EVEN p>=2 and odd driver, on a fixed aligned depth-r upper
orbit, extension to depth r+1 is affine in its complete odd-label cube
at r=1,2,3. At r=1 it is constant. At r=2 hidden labels affect only
the next new X bit; at r=3 only the following two new X bits. Explicit
five-state upper resets erase these effects before another free label
can interact. The newest Y history and the deeper blind set are fixed
on each such fiber. The exact extension rank is `u_r-u_(r+1)`.

There is also an ALL-DEPTH CONDITIONAL reduction: if newest Y is fixed
on any one upper fiber with nonzero parent, the full extension is affine,
the deeper blind set is fixed, and the same rank formula follows. A
parent phase with M=1 anchors X; if M is always zero, a phase with L=1
provides an affine reset. Thus **H_Y**, invariant newest Y on every
fixed aligned odd-label fiber, was a precise sufficient target. It is
proved at r<=3, but its universal version was refuted in the fourth unit
below. The conditional lemma remains valid. The smallest unresolved
extension depth is r=4.

Reproduce:

    python3 experiments/problem1_nonperiodicity/check_portal_layer_monodromy.py
    python3 experiments/problem1_nonperiodicity/check_blind_fiber_endpoint_affinity.py

The first record checks 25,104 return matrices and 100,416 seed returns
using an independent raw-half recurrence. The second supplies
**FINITE EVIDENCE ONLY** for H_ext and H_Y at p=2,4,6,8,10,12,14,
r=1..6: 42 scopes, 65,532 driver/scope instances, 42,196 complete
eligible fibers, no exclusions or counterexamples. Independent p8
controls cover all 128 odd drivers through depth seven. Endpoint
affineness survives only the separate p8,r1 classifier check; no new
long first-return traversal was performed.
At r=4,5,6 those tested cubes have dimension at most one, so H_ext is
automatic there. Invariant Y remains a nontrivial finite test. To attack
H_ext itself beyond the proof requires a fiber of dimension at least two.

Exact output records are in `results/problem1/20261002_portal_layer_monodromy.json`
and `results/problem1/20261002_blind_fiber_endpoint_affinity.json`.
The companion review retains rejected critic claims and corrected draft
checker bugs. Read those dispositions before reusing old implementations.

The historical finite-speed margin idea in
`problem1_projection_vs_forced_state_audit.md` is superseded by
`problem1_forced_doubling_fiber_cone_audit.md`: low changes never affect
higher indices under A, while the actual doubling fiber is at the changed
boundary. This is an existing correction, not a new support bridge.

Even a proof of general affine extension would only settle layer transport
inside one fixed-period connector. Cross-return transport and bounded reuse
against the SAME ORIGINAL support remain the global obstruction. Do not
claim a Prize Problem solution from these local transfer lemmas.

## Fourth unit: false full-Y bridge and an exact gate repair

Read `proofs/informal/problem1_hidden_label_reset_counterexample.md` and
`proofs/informal/problem1_blind_output_gate_criterion.md`.

Status: **FAILED — COUNTEREXAMPLE FOUND** for the active-label reset
criterion H_reset and general H_Y. The ordered bounded search first
fails at p10,r6,w55,s4: an active child X impulse reaches a parent Y=1
after four phases with no earlier (1,0) reset. Its odd fiber is a
singleton, so that witness alone does not settle H_Y.

Repeat that aligned upper orbit THREE times. At p30,r6 its blind phases
are {4,14,24}, giving an exact four-member odd cube. Words 57711655 and
40950823 share the whole upper orbit but differ in newest Y at phases
19 and 29. Both have weight thirteen and least period thirty. Thus H_Y
is false even with full-period witness drivers. Independent scalar child
and original two-row temporal reconstruction passed for all four words.
This is four targeted inputs, not a period-thirty census.

The full four-output XOR is zero, so H_ext holds on that entire square.
Each old blind phase has outgoing new Y=1 for every input. Thus the
weaker **H_B**, constant gate only at old blind phases, survives here;
rank is two and the new blind set is empty. General H_B is unproved.

New status: **LEMMA WITH PROOF — INDEPENDENTLY CHECKED**, at EVERY depth:
on a complete odd upper fiber with nonzero parent, extension is affine
IFF each old blind phase's outgoing new difference has the form

    d_s(w)=alpha_s+beta_s w_s.

It may depend on its own label, but not other labels once its own is
fixed. Sufficiency uses one fixed odd base driver's invertible monodromy
and affine forcing. Necessity uses the second finite difference of the
product w_s*d_s. H_B is beta=0; H_Y is an unnecessarily stronger
all-phase condition. Any affine extension also has constant u_(r+1)
and exact rank u_r-u_(r+1), even if its deeper blind set varies.

Reproduce the stopped reset search plus exact four-input repair test:

    python3 experiments/problem1_nonperiodicity/check_hidden_label_reset_criterion.py

The `--targeted-only` option replays the four inputs without modifying
the full-run record. Atomic record:
`results/problem1/20261002_hidden_label_reset_criterion.json`.

The subsequent fifth unit settles its first unproved depth r=4 by an
exact graph reduction and independently checked certificate. General
H_gate/H_ext at r>=5 is now the local target; false H_Y is closed.

## Fifth unit: all-period depth-four affine transport, computer-assisted

Read `proofs/informal/problem1_depth4_affine_transport_certificate.md`
and `proofs/informal/problem1_gate_miter_finite_reduction.md`.

Status: **LEMMA WITH PROOF — INDEPENDENTLY CHECKED**, computer-assisted.
For EVERY even p>=2 and every complete aligned depth-four odd-label
fiber with all raw parents nonzero, extension to depth five is affine.
Its rank is u_4-u_5 and u_5 is constant. This extends H_ext from r<=3
to r=4. It does not extend full-Y invariance or fixed-blind-set claims.

The proof uses the exact product of two depth-five stacks with a shared
depth-four state: 4096 product states and eight parity sheets, 32768
lifted vertices. A bad edge has upper state blind, equal input labels
and unequal outgoing new Y. An independently checked topological rank
is nondecreasing on all 67584 retained edges and STRICTLY increasing
on all 768 bad edges. Any product cycle lifts to a closed walk by
repeating it twice; strict increase would be impossible. This proves
the gate condition at ALL periods, not a finite-period extrapolation.

The rank certificate has 65536 bytes, SHA256
`3a9eb40a2b54e39ff79869888d1da5be5cfcb75368ad15db80d3619554a03263`.
The independent verifier derives every edge from a raw Rule-30 truth
table, importing no producer transition or component algorithm. It
checks 2048 full transition controls, the complete edge set and all bad
edges. Parent code/logic review and final reruns passed. The producer's
record retains its finite-graph status; the proof supplies the all-period
consequence at this fixed observer depth.

Reproduce:

    python3 experiments/problem1_nonperiodicity/check_depth4_gate_miter.py
    python3 experiments/problem1_nonperiodicity/verify_depth4_gate_rank_certificate.py

Atomic records:
`results/problem1/20261002_depth4_gate_miter.json` and
`results/problem1/20261002_depth4_gate_rank_certificate_verification.json`.
All runs remain local and within 60 seconds, 256 MiB and 256 KiB output.
The immutable reference hash is unchanged.

The first unresolved extension depth is now r=5. Section 6 of the finite
reduction gives a cheap stronger screen: a rank strict on every bad
edge across all sheets projects to the product graph by taking the
maximum over sheets. A direct r=5 product graph would therefore have
only 16384 states. If a bad product cycle exists, its parities and
nonzero-parent domain must still be checked by the full miter; it is
not automatically an odd-fiber counterexample. A new admission is
required before executing that next depth.

The unchanged global obstruction is transport across a zero return or
period doubling with bounded reuse on the SAME ORIGINAL finite support.
No fixed observer theorem alone proves the whole-tail target or Problem 1.
