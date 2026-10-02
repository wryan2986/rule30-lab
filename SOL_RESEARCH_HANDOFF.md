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
