# Astra handoff: supervisor round 304 maintenance checkpoint, 2026-09-07

Problem 1 remains OPEN. Continue on `research/astra-next`. This is a routine
research maintenance checkpoint, NOT goal achieved, research blocked, or
research exhaustion. Read ASTRA_GOAL.md first; do not repeat settled work.
Round304 base: `c6873e33ee8b657fdc7c647aa050e02cf7b064e5`.
Incoming round303 handoff is preserved byte for byte in
`docs/astra_handoff_archive_20260907_round304.md`; the older round-ten handoff
is in `docs/astra_handoff_archive_20260907_round303.md`.

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
