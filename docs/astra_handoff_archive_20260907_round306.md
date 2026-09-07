# Astra handoff: supervisor round305 maintenance checkpoint, 2026-09-07

Problem1 remains OPEN. Continue on `research/astra-next`. This is a routine
maintenance checkpoint, NOT goal achieved, research blocked, or exhaustion.
Read ASTRA_GOAL.md first; do not repeat settled work. Round305 base was
`dc4ffc5ed8981dcb7f36509ade43d1277e9c83bd`. The incoming round304 handoff is
preserved byte for byte in `docs/astra_handoff_archive_20260907_round305.md`.
That archive links the earlier round303/round-ten handoffs.

## Current bottleneck and next attack

FULL must contradict finite entry for ONE actual survivor with its COMPLETE
original finite right fringe. The renewal forces infinitely many delay
injections and clock doublings, but no finite budget has been proved.
An eventual all-physical K=1 bound is still CONDITIONAL, not established.

Round305 identifies the precise shadow data at cyclic returns and at possible
one-bit-strip exits. Ranked next routes (`heuristic`):

1. Retain the whole original actual/shadow pair. At each cyclic even return,
   study the actual/shadow gate disagreement below; at a lag-one u source,
   study the shadow first right bit deciding return versus strip exit.
   A surviving K=1 orbit must sustain BOTH the required births and the
   no-exit constraint forever. Use the actual eventually-zero INITIAL right
   fringe and the uniquely selected shadow, not freely chosen phase flags.
2. Without assuming K=1 or cyclic returns, use the global front residence
   identity to constrain all injections. A charge into the finite anchored
   set after ONE justified even physical rebase still needs distance-growing
   transport and bounded reuse. Path existence or path parity is not a
   nonnegative budget.

No autonomous update of the new shadow flag is proved. No more source words,
clock trees, shifted-source rate samples, local neighborhoods, front samples,
or longer gate prefixes should be enumerated merely to illustrate these facts.

## New exact birth observable (`partial-proof`)

Read `proofs/informal/problem1_shadow_gate_birth_phase.md`.
On the ONE fixed actual FULL orbit, let t be even and Y_t cyclic. Put

    u_t = indicator[(r_1(t),r_2(t))=00],
    hat u_t = indicator[(hat r_1(t),hat r_2(t))=00].

Here hat r is the global E shadow, not a replacement actual fringe.
Then

    tau(Y_(t+1))=0,
    chi_t=tau(Y_(t+2))=u_t XOR hat u_t in {0,1}.

Thus R_t=0 and R_(t+1)=chi_t. Direct physical updates and the full periodic
scan give separate derivations. No eventual strip bound is needed for this
one CYCLIC-source transition.

The missing phase bit has an exact full-driver description. For the PURE
code b=Theta(Y_t), with b_0=3 and b_1 in{1,2}, extend its period to negative
A-times and set ell=max{s<0:b_s in{1,2}}. Then

    hat u_t = XOR_(s=ell+1..-1) indicator[b_s=3].

This is parity since the last1/2 in the periodic past. Its lookback may
depend on the whole period; negative phases are not actual prehistory.
The zero-indicator quotient of H_0,H_1,H_2,H_3 is respectively identity,
constant0,constant0,flip. This explains the old suffix13/11 controls without
repeating their construction or evading the finite-observation no-go.

At a cyclic source the shadow centers used for the next two updates are1,0,
so, writing its right cells as a,b,c,d,

    hat u_(t+2)=a*b*(c OR d).

The same formula holds for the actual fringe under FULL. The wider driver
remains present. If this step creates a birth, do NOT reuse1,0 as the next
shadow center inputs: the shadow's own boundary must be retained.

## Exact one-bit-strip exit (`partial-proof`)

Read `proofs/informal/problem1_one_bit_shadow_exit.md`.
At an even FULL time, assume only CURRENT agreement at every position<=-1,
with center discrepancy ell in{0,1}. Let u be the actual u-gate indicator,
h=hat r_1(t), and hat u the shadow right-pair zero flag. Do NOT assume the
future strip persists. The exact two-step alternatives are:

| source | next odd center discrepancy | next even left discrepancy | next even center discrepancy |
| --- | --- | --- | --- |
| ell=0 | 0 | 0 | u XOR hat u |
| ell=1, gate t | 1 XOR h | 0 | 1 |
| ell=1, gate u, h=1 | 0 | 0 | 0 |
| ell=1, gate u, h=0 | 1 | 1 | 0 |

All positions<=-2 still agree at the next even time. In the last row the
CENTER agrees but position-1 differs: this is an EXIT, not a cycle return.
At the intervening odd row the center defect has common left neighbor0,
so it survives one A step and the least delay there is at least2.

Consequently eventual all-physical K=1 requires h=1 at every sufficiently
late lag-one u source. This recovers the old conditional t persistence/u
return law and identifies the exact excluded branch. For the given two U
spacetimes, continuing negative-half agreement is equivalent, by induction,
to r_1(s)*d_0(s)=0 at every later ODD time (even times are shielded).
It is not a freely forced half-line construction or a finite-state closure.

## One global front orders all injections (`partial-proof`)

Read `proofs/informal/problem1_global_discrepancy_front.md`.
For ORIGINAL cuts L_j and s_j=tau(L_j), define J(u)=min{j:s_j>u}.
Imported unbounded zero-extension delays make J finite at every u and
unbounded over time. The WHOLE leftmost discrepancy is m(u)=J(u)-u,
including when it lies right of the center. Its exact residence is

    J(u)=j iff s_(j-1)<=u<s_j.

The shared left neighbor is0 until the last residence time, when its1
erases the front. The next front still requires the whole discrepancy tail.
Physical R_t counts exactly the part AFTER reaching the center:

    I_t=[max(s_t,t+1),s_(t+1)), length R_t.

For R_t>0, the old residual at u=t+1+T_t is the GLOBAL leftmost discrepancy,
m=-T_t. Different injections have disjoint I_t and ordered erasers. This
orders events, not original ancestors or their reuse. Clock-doubling targets
j have s_j=s_(j-1), so J NEVER visits them. The converse is not asserted.
Counting these residences recovers the old renewal, not a finite budget.

In characteristic coordinates v_j(u)=r_(j-u)(u), h_j(u)=hat r_(j-u)(u),
Delta=v XOR h, the exact full-driver recurrence is

    Delta_j(u+1)=Delta_(j-2)+(1 XOR h_j)*Delta_(j-1)
                              +(1 XOR v_(j-1))*Delta_j,

with XOR sums. Its finite-cone solution is weighted path PARITY. The fixed112
control has two active paths to the time-one center which cancel. Swapping
actual/shadow in the OR factorization changes individual paths while keeping
the XOR. Do not use reachability as a positive birth count or freeze the
coefficients while changing the underlying spacetimes.

## Two scoped routes closed in round305

`proofs/informal/problem1_full_driver_phase_memory_obstruction.md`:
let F_y(a)=bit0(cyc(2y+a)) and S(y)=(cyc(y),tau(y),F_y(0),F_y(1)). The
GENERAL update F_(2y+a)=H(S(y),a) is `refuted`, even on the next zero branch.
Rows110/112 have the SAME complete core111, delay1, period2 and F=(0,0).
Attach the SAME zero: children220/224 have core222 but phase maps0 and
(a XOR1), respectively. Thus cyc440=444 but cyc448=445. They are phases
of one period4 cycle, not a new cycle fork. The witness is not FULL and
does not refute a separately justified FULL-only summary.

`proofs/informal/problem1_width_delay_bound_obstruction.md`:
the sharp universal proposal tau(y)<=bitlen(y)-1 is `refuted` by144:

    144,252,193,209,205,220,201,223,200,222,200.

Width8, exact delay8, core200, period2. The original-cut bridge would have
turned that proposal into tau(Y_t)<=L-1 for a finite row of original left
extent L. It fails at time4 of seed9 with the SAME zero right half:
Y_4=205 has delay4 while L-1=3. Seed9 is not FULL. An EVENTUAL bound or a
width-plus-constant bound is NOT refuted. No intercept was fitted and no
unbounded-excess family was proved. The frozen pre-run admission is
`problem1_width_delay_bound_test.md`; its pending status is historical.

## Preserved round304 facts and fences

The full incoming archive remains authoritative for details. In particular:

* E glues cyc(L_j) into ONE whole row, E(E(r))=E(r), E(Ur)=U(E(r)).
  Its infinite initial right discrepancy supply remains infinite at every
  finite physical rebase. The original zero fringe is not the shadow fringe.
* E is a dyadic B=SU limit on fixed windows. The actual center moves out of
  those windows; FULL cannot be passed to a fixed shadow center by that limit.
* The round304 one-extension transient formula retains the full transient.
  The new round305 summary counterexample closes its proposed recursion
  from only complete core, exact delay, and one-bit phase map.
* The finite width53208 even-parity fork is settled. Do not enumerate later
  fork positions, source words, or cycle trees.
* The reset eraser (-lambda,t+lambda) is at sharp L1 distance
  t+ceil(2(lambda+1)/3) from the entire original anchored sampling domain.
  A single justified even rebase makes total anchored capacity finite, but
  the charge of resets to it and bounded reuse remain unproved.
* Round303's finite-observation birth no-go retains its exact general cyclic
  domain and finite-FULL-shadow fence. No infinite FULL countermodel exists
  in those notes. Round-ten renewal, clock consumption, and conditional
  lag-one episodes of at most5 even rows remain unchanged.

## Verification, provenance and review

Lead dispositions: `proofs/informal/problem1_round305_review.md` Sections2-6.
No new `rigorous-proof` status is assigned. Four atomic result/checker pairs
use the prefix `20260907_round305_` / `check_round305_`:

* phase_transport:14 hand edges,14 closed certificates,four full phase maps,
  eight product/scalar phase checks;10s/128MiB caps passed.
* width_delay: independent complete packed/cell orbits on1..144; STOPPED at
  first violation before the4095 cap;30s/128MiB passed. No larger input.
* shadow_gate:32 Boolean identity cases,two fixed three-step physical
  controls27/55 with their specified complete fringes,eight closed cycles;
  10s/128MiB passed. No infinite FULL claim for either control.
* shadow_exit:32 LOCAL algebra assignments;10s/128MiB passed. Their second
  row is NOT claimed to be E of the first. They check the table, not global
  shadow membership, infinite FULL, or the all-depth least-delay deduction.

All four current source-hash manifests and canonical payload hashes were
independently audited. No additional numerical experiment was needed for
the front's all-depth counting and path identities.

Muse incoming-review thread01a07b36-d832-7f00-8d9d-b5d874a5cb16 and fresh
front-review thread01a07b59-b4da-70d2-8671-c445e57100a3 both failed before
review text with MissingSessionID (missing x-opencode-session); both CLOSED.
Neither was429. MiMo was not advertised; no native/other provider was
substituted and no provider settings changed. External review remains
missing for the incoming notes AND all new round305 units.

Round305 owns only its proof/review/admission notes, four fixed checkers and
atomic records, incoming handoff archive, and this handoff. Unrelated
supervisor files, worktrees and old untracked results are untouched.
The immutable reference SHA256 remains
358bdc07904e77080eb78b67bdd8da25822d6b51f1a91b58b5313dfe461c1d01.
Continue locally; no force-push, history rewrite, main merge, reference edit,
cloud workload or hardware-control changes.
