# Astra handoff: supervisor round305 in-progress checkpoint, 2026-09-07

Problem1 remains OPEN. Continue on `research/astra-next`. Round305 base:
`dc4ffc5ed8981dcb7f36509ade43d1277e9c83bd`.
Incoming round304 handoff is preserved byte for byte in
`docs/astra_handoff_archive_20260907_round305.md`.
This is a maintenance checkpoint, not goal achieved or research blocked.

## Round305: full driver plus phase map still loses transient memory

New scoped `refuted` update in
`proofs/informal/problem1_full_driver_phase_memory_obstruction.md`:
let F_y(a)=bit0(cyc(2y+a)) and
S(y)=(cyc(y),tau(y),F_y(0),F_y(1)). There is NO general function
F_(2y+a)=H(S(y),a), even when only the next zero branch is requested.
This retains the ENTIRE cyclic driver and exact least onset, and is
therefore different from the earlier finite-observation no-go.

Hand pair110/112: both map to100, with core111, delay1, period2 and
F_y=(0,0). Attach the SAME zero: children220/224 have common core222,
but delays3/1 and phase maps respectively0 and (a XOR1).
Thus cyc440=444 but cyc448=445. These are phases of the SAME period4
cycle, not a new cycle fork. Both zero branches differ. The witness
refutes a general summary; it is NOT an infinite FULL counterexample
or a refutation of an independently proved FULL-only summary.

Fixed checker `experiments/problem1_nonperiodicity/check_round305_phase_transport.py`
and atomic record `results/problem1/20260907_round305_phase_transport.json`:
14 hand edges,14 closed certificates,four full phase maps and8 phase
comparisons. Packed/cell and product/scalar implementations agree;
10s/128MiB caps passed. Lead disposition is
`proofs/informal/problem1_round305_review.md` Section2.

Muse incoming-review thread01a07b36-d832-7f00-8d9d-b5d874a5cb16 failed
before review text with MissingSessionID (missing x-opencode-session)
and is CLOSED. Not429; no fallback, native substitution or config change.
Fresh external review remains missing. Next: retain the whole transient
in a proposed crossing transport, or justify an extra FULL-only constraint;
do not refit this failed general summary with more local observations.

## Round305: sharp full-width delay bound refuted

The distinct structural proposal tau(y)<=bitlen(y)-1 for all finite y>0
is `refuted` by144: its width is8 and its exact delay is8, with orbit
144,252,193,209,205,220,201,223,200,222,200. Core200, period2.
The frozen admission is `proofs/informal/problem1_width_delay_bound_test.md`;
outcome is `proofs/informal/problem1_width_delay_bound_obstruction.md`.
Had the bound held, the original-cut bridge would give tau(Y_t)<=L-1 for
one fixed finite row of original left extent L. It fails even at time4
of seed9 with the SAME zero right half: Y_4=205 has delay4 while L-1=3.
Seed9 is not FULL. No eventual bound or width-plus-constant bound is refuted.

Checker `experiments/problem1_nonperiodicity/check_round305_width_delay.py`
and atomic record `results/problem1/20260907_round305_width_delay.json`:
independent packed/cell orbits agree on1..144; stopped at first violation,
before its predeclared4095 cap. No fitted intercept or larger range.
Do not sample shifted144 or9 to estimate a rate. A general unbounded-excess
family is unproved; this sharp bound's falsification is complete.

## Round305: one global front orders the injections (`partial-proof`)

Read `proofs/informal/problem1_global_discrepancy_front.md`. For original
cuts L_j and s_j=tau(L_j), define J(u)=min{j:s_j>u}. Its existence uses
finite original support and the IMPORTED unbounded zero-extension delays.
The WHOLE actual/shadow leftmost discrepancy is m(u)=J(u)-u, including
when it lies right of the center. J(u)=j exactly on [s_(j-1),s_j).
The shared left neighbor is0 until the residence's final time, when its1
erases the front. The next front needs the remaining entire discrepancy tail.

Physical R_t counts EXACTLY the portion of residence j=t+1 after center
crossing: I_t=[max(s_t,t+1),s_(t+1)), length R_t. For R_t>0 the old residual
at u=t+1+T_t is the GLOBAL leftmost discrepancy m=-T_t. Distinct injections
have disjoint residence subintervals and ordered erasers. This is not
uniqueness or bounded reuse of original discrepancy ancestors.

Every clock-doubling target j has s_j=s_(j-1), so J NEVER visits that
characteristic at any time. The converse is not claimed and no jump bound
follows. Counting residences recovers the old renewal, not a finite budget.

The exact full-driver cocycle in characteristic coordinates is
Delta_j(u+1)=Delta_(j-2)+(1 XOR h_j)Delta_(j-1)
                          +(1 XOR v_(j-1))Delta_j,
where v and h are the complete actual/shadow rows. Its finite-cone solution
is a PARITY of weighted paths from original discrepancies. The fixed112
control has two active paths to the time-one center which cancel. Another
valid OR factorization changes individual paths while preserving their XOR.
Do not turn reachability into a positive count or assume coefficients remain
fixed when the underlying actual/shadow pair changes.

Fresh front-review Muse thread01a07b59-b4da-70d2-8671-c445e57100a3 also
failed before text with MissingSessionID and is CLOSED. Lead audit only:
`proofs/informal/problem1_round305_review.md` Section4. No external review.

## Preserved round304 frontier (still authoritative except for that update)

## Exact bottleneck and next attack

FULL must contradict finite entry for ONE fixed actual survivor with its
COMPLETE original finite right fringe. The renewal forces infinitely many
delay injections and clock doublings, but no finite upper budget for those
injections has been proved. An eventual K=1 bound is still only a CONDITIONAL
hypothesis; bounded lag-one episodes do not exclude infinitely many births.

Round304 supplies a whole-spacetime representation of all cycle defects.
It shows that finite actual support does NOT give a finite stock of initial
cycle discrepancies: there are infinitely many on the auxiliary right half,
and they remain infinite after every finite physical rebase. The unresolved
question is which of them reach the center under FULL, with what phase
selection and reuse. Do not silently replace the actual zero fringe by the
auxiliary fringe, or assert that the auxiliary center is FULL.

Rankings are `heuristic`:

1. Retain the entire original zero-extension history and its uniquely selected
   global shadow. Use the exact transient phase data below to constrain the
   FULL crossing history. A new update or invariant must retain its complete
   driver; no autonomous update of the two phase bits is proved.
2. Construct a genuinely global charge of resets to a finite anchored target
   set after ONE justified even physical rebase, with bounded reuse. Its
   displacement must grow with physical time; direct ray reindexing fails.
3. Use the same full shadow to close a conditional bounded-strip episode.
   The existing K=1 gate/lag rules do not determine its next birth.

No more source words, fork positions, cycle trees, birth prefixes, or local
neighborhoods should be enumerated merely to illustrate these results.

## New global cycle shadow (`partial-proof`)

Read `proofs/informal/problem1_global_cycle_shadow.md`, especially Sections
1-6. The separate disposition file is explicitly a LEAD audit:
`proofs/informal/problem1_round304_review.md`, Section 5.

For a row r that is zero sufficiently far LEFT, every cut

    L_j(r)=sum_(i<=j) r_i 2^(j-i)

is finite, even with an infinite right half. Let U be physical Rule30,
sigma(y)=y>>1, and C_j=cyc(L_j(r)), with PHASE-CORRECT cyc. Then

    sigma L_(j+1)=L_j,   L_j(Ur)=A L_(j+1)(r),
    sigma C_(j+1)=C_j.

These compatible cuts define one unique whole row E(r), and

    E(E(r))=E(r),   E(Ur)=U(E(r)).

Thus if hat r evolves from E(r), its center-and-left row at EVERY physical
time t is exactly cyc(Y_t). The auxiliary boundary bits in the old defect
recurrence belong to this one actual Rule30 spacetime; they are not free.
E(r) itself is a DIFFERENT initial row, not the original prescribed fringe.

With S the shift RIGHT and B=SU, L_j(B^n r)=A^n L_j(r), so

    E(r)=lim_k S^(2^k) U^(2^k) r

on fixed windows. Each fixed cut has a dyadic eventual clock. There is no
uniform onset or period. The original center moves to position2^k under
this shift and escapes every fixed window: FULL cannot be transferred to
a fixed center of E(r) by taking this limit.

For nonzero FINITE r, with L_0(r)>0, the C_j have widths L+j and unbounded
least periods. At every one-bit doubling index j, the next cyclic lift's
low trace v visits1 and its following lift satisfies w'=v OR w. Cyclicity
forces w=1 at every A-time, so

    E(r)_(j+2)=1 at EVERY doubling index j.

There are infinitely many such positions beyond any finite actual fringe.
Hence d_i(0)=r_i XOR E(r)_i has infinitely many right-hand1s. By commutation,
the global discrepancy set is infinite to the right at EVERY finite time.
This asserts no individual discrepancy's immortality or positive density.
At a cyclic center-and-left row all discrepancies at positions<=0 vanish,
but infinitely many still remain to the right.

For R_t>0, T=max(tau_t-1,0), the residual wrong bit is a genuine discrepancy

    d_(-T)(t+1+T)=1.

It has some initial discrepancy ancestor k in [-t-1-2T,t+1]. This is NOT
an original nonzero-cell or anchored-P charge. If Y_0 is cyclic, all such
ancestors are positive. No uniqueness or bounded reuse is proved.

Exact old55 control: initial cuts55,110,220 have cyc55,111,222. Initial
shadow discrepancy is1 at position1, zero at2 and every position<=0.
The actual rows at physical times1,2 are100,223; shadow rows100,222.
Thus R_1=1 has only the OLD position1 as an initial discrepancy ancestor
in its cone, although the newly included initial position2 agrees.

## Exact transient phase selection (`partial-proof`; fixed controls checked)

The recursion cyc(2y+a)=cyc(2cyc(y)+a) is REFUTED even for a=0:
y=7 gives cyc14=13, whereas cyc12=12. The original transient matters.

For finite y, z=cyc(y), assume the low A-trace of z is identically zero.
Choose ANY T>=tau(y), and for s<T put
u_s=bit0(A^s y), v_s=bit1(A^s y), w_s=bit1(A^s z). With XOR sums,

    eta = product_(s<T)(1 XOR u_s),
    theta = XOR_(s<T)[(v_s XOR u_s) product_(s<k<T)(1 XOR u_k)]
              XOR XOR_(s<T)w_s,
    cyc(2y+a)=2z+(eta*a XOR theta).

Extra valid horizon steps cancel. If an actual transient low1 occurs,
eta=0 and only its last reset and following suffix survive in theta.
If none occurs, eta=1 and theta=XOR_(s<T)(v_s XOR w_s). At a cyclic
source T=0, eta=1,theta=0. For a cyclic driver with a low1, the unique
resetting lift instead fixes the phase from z alone.

Hand controls: y7,z6 gives (eta,theta)=(0,1). The hand preimage166->222
->200->222 has cyc166=200 and low trace zero at EVERY time, but
(eta,theta)=(1,1). It gives cyc332=401 and cyc333=400, checked against
400->444->401->445->400. Thus no low reset does not imply no phase change.
These two bits suffice for ONE extension with its whole cyclic driver;
they are NOT a proved finite-state description of successive extensions.

Fixed checker `experiments/problem1_nonperiodicity/check_round304_phase_memory.py`
and atomic record `results/problem1/20260907_round304_phase_memory.json`:
12 cases (y7/166, a0/1, T1/2/5), product formula versus independent
cell/scalar-OR recurrence;15 hand edges and8 closed cycle certificates.
All passed, with 10s/128MiB caps. Status is `finite-exhaustive` ONLY for
those controls, not machine verification of the all-depth shadow theorem.

## Anchored charging geometry (`partial-proof`)

`proofs/informal/problem1_reset_anchoring_geometry.md` locates the erasing
1 of an injection R_t>0. With lambda=tau_(t+1)=T+R_t, it is

    r_(-lambda)(t+lambda)=1.

Its characteristic coordinate i+u is t. Original anchored samples are
(-2n-s-epsilon,s), n>=1,0<=s<n,epsilon=0/1, with i+u<=-2. The SHARP
L1 distance to that entire sampling domain is

    t + ceil(2(lambda+1)/3) >= t+2.

No direct same-cell charge is possible. A bounded physical neighborhood
cannot furnish targets for arbitrarily late resets. This does NOT refute
all FULL-only local-charge lemmas: the hypothetical domain may be empty.
Global, distance-growing transport remains unexcluded and unconstructed.

Also Q is a supremum per ray, not a total count: A(-1)=0 gives Q(-1)=1
but sum_n J_n(-1)=infinity. A single fixed physical rebase repairs capacity:
for Q(Y_0)<=K, h=h_J(K), H=2ceil(h/2), the ACTUAL x=Y_H is finite and

    Q(x)<=K'=K+h+H/2,   sum_n J_n(x)<=K'(K'+1)/2.

H is even, and its ENTIRE actual finite right fringe must be retained.
A bounded-multiplicity assignment of all later resets to these finite
active pair samples would contradict the renewal. Neither such an
assignment nor its multiplicity bound is proved. Counting ancestors in the
infinite right shadow from the preceding sections does not supply it.

## Finite phase fork (`refuted` rigidity; one `finite-exhaustive` certificate)

`proofs/informal/problem1_finite_cycle_phase_fork.md` tests the false claim
that a positive finite cyclic zero-low-bit driver must have odd high-bit
weight. The single word from Rowland's primary-source Section5 is

    b=0000220002020022, least period16, six 2s,
    Phi^26604 b=0, every earlier iterate nonzero.

Its inverse y is FINITE with width53208. Both2y and2y+1 have least period16
but lie on DISTINCT cycles, with low traces0000010000110001 and its
complement. A phase joining them would project to a return of y and hence
fix the starting lift. Finite support does not select a universal cycle
or charge every retained phase choice to a doubling. Under the SAME
complete right fringe, their physical leftmost difference stays at -t.
This is between TWO orbits, not internal cycle delay on one FULL survivor.

Checker `experiments/problem1_nonperiodicity/check_round304_phase_fork.py`;
atomic record `results/problem1/20260907_round304_phase_fork.json` gives
full source hex, both deletion-trajectory hashes, all provenance, and
851328 independent packed/cell bit comparisons. Runtime1.665s, peak
RSS29286400 bytes;60s/128MiB caps passed. No minimal fork depth or larger
word/period/fork supply was searched. Do not pursue the published later
fork positions or repeat this failed rigidity hypothesis.

## Preserved incoming results and stopping fences

The incoming archives retain exact proofs and valuations; do not redo them.
Round303: both delay-birth fibers are dense/nowhere continuous on general
cyclic permitted rows, even at identical exact dyadic clocks and with an
arbitrary finite FULL shadow using the SAME complete fringe. The sources
vary with the observation; they are not finite-support or infinite-FULL
countermodels. Finite cyclic birth density remains unproved.

Round10: tau_(t+1)=max(tau_t-1,0)+R_t; every FULL doubling has R_t=0 and
consumes one delay. Telescoping requires infinitely many injections as clocks
grow. The shift family2^n*7 refutes bounding whole delay by the current
highest erasing wait; it gives no physical lag-growth rate. Under an eventual
physical K=1 bound, lag-one even episodes have at most5 rows and doubling
episodes have2..5; their next birth is not determined by gate/lag alone.
These are conditional restrictions, not an exclusion of finite-entry FULL.

## Verification, ownership and external review

All new proof units have a lead adversarial disposition in
`proofs/informal/problem1_round304_review.md`. No `rigorous-proof` status
is assigned. Current source hashes and canonical payload hashes of both
atomic results were independently audited after the checks.

Muse incoming-review thread01a07af9-afb9-7e03-833c-cbe7da1826b8 and fresh
global-shadow-review thread01a07b25-f1d7-73b0-ae99-72d5bfd89552 both failed
before review text with MissingSessionID (missing x-opencode-session).
Both are CLOSED. Neither was429; no rate-limit fallback was triggered.
MiMo was not advertised. No native or other provider reviewer was substituted
and no provider configuration changed. External review remains missing for
the incoming round10/303 notes AND the new round304 units.

Round304 owns only its three proof notes, lead review, two fixed checkers
and atomic records, incoming handoff archive, and this handoff. Unrelated
supervisor files, worktrees and old untracked results are untouched. The
immutable reference SHA256 remains
358bdc07904e77080eb78b67bdd8da25822d6b51f1a91b58b5313dfe461c1d01.
Continue locally; no force-push, history rewrite, main merge, reference edit,
cloud workload or hardware-control changes.
