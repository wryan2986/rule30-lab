# Sol research handoff — 2026-10-02

Problem 1 remains **OPEN**. This is the current compact handoff for this
goal. Historical ASTRA-named files are research material; they do not
authorize use of Astra.

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
fixed aligned odd-label fiber, is a precise sufficient target. It is
proved only at r<=3. The smallest unresolved extension depth is r=4.

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

Even a proof of general H_Y would only settle layer transport inside one
fixed-period connector. Cross-return transport and bounded reuse against
the SAME ORIGINAL support remain the global obstruction. Do not claim a
Prize Problem solution from these local transfer lemmas.
