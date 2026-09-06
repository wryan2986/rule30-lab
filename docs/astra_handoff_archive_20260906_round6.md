# Astra handoff: round 5 maintenance checkpoint, 2026-09-06

Problem1 remains OPEN. This is time-maintenance rollover, not goal achieved,
research blocked, or research exhaustion. Research continues on
`research/astra-next`. Round five began at21:20:55UTC; the final atomic audit
records the checkpoint time and elapsed seconds. Read ASTRA_GOAL.md first.
The incoming handoff is preserved byte for byte in
`docs/astra_handoff_archive_20260906_round5.md`.

## Current bottleneck and reading order

Prove activity growth for ONE FIXED ACTUAL period-two survivor, keeping its
FULL fringe coupling. New work has provided inequalities and a weaker
anchored target, but has NOT supplied that coupling mechanism.

Read the following notes in proofs/informal, in this order:

1. `problem1_activity_joint_window_target.md` (latest sufficient target).
2. `problem1_activity_temporal_gate_bridge.md` (exact boundary conversion).
3. `problem1_activity_transport_inequality.md` (general counting proof).
4. `problem1_activity_sparse_temporal_codes.md` (density necessity refuted).
5. `problem1_activity_staircase_bound.md` (explicit support bound).

All five all-depth units retain status `partial-proof` relative to the prize,
with independent review accepted in the stated scopes. Every actual-survivor
growth assertion remains `inconclusive`. No infinite conclusion is inferred
from the finite local checks.

## Latest target: anchored characteristic activity

Use

    T(x)=x XOR((x<<1) OR(x<<2)), pi(x)=x>>2, A=pi T,
    V_s(x)=sum_(t=0..s-1)bit_(2s)(T^t x), V_0=0,
    R(x)=sup_s V_s(x), E_K={x:R(x)<=K},
    P_n(t)=bit_(2n)(A^t x) OR bit_(2n+1)(A^t x),
    C_n(a,W)=sum_(t=a..a+W-1)P_n(t), J_n(x)=C_n(0,n).

Let H_odd(r)=sum_(j=0..r)1/(2j+1),
H_n=H_odd(floor((n-1)/2)),
g(K)=min{r:H_odd(r)>K}, h_V(K)=min{r:H_odd(r)>3K/2}.

The new sufficient target is simply sup_n J_n(x)=infinity for the SAME
actual x. No positive density is necessary for this implication. Exactly,

    R(x)<=K implies sup_n J_n(x)<=max(h_V(K),2g(K)).

Proof: z=A^h x=pi^h T^h x is finite, R(z)<=K and bitlen(z)<=4g+2.
For n>=2g+1 and t>=h, P_n(t)=0; smaller n have J_n<=n<=2g.
This imports the reviewed finite-entry theorem; it is NOT a new proof
of that theorem. Bounded J => bounded R is NOT asserted.

The stronger direct finite bound is, for ALL n>=1,a>=0,W>=1,

    sum_(s=a+2..a+W+n)V_s(x)
      >=sum_(r=0..floor((n-1)/2))ceil(C_n(a,W)/(2r+1))
      >=C_n(a,W)H_n.

The window has W+n-1 ages. Original transport was stated only for
a>=n-1; the latest note proves a>=0 by retaining each selected pair's
own valid interval. Never define w_j(s) at s<j. In particular,

    R_(2n)(x)>=J_n(x)H_n/(2n-1).

Jointly growing n,W can retain intermittent events lost in a fixed-n
density limit. No actual growing windows or unbounded J have been proved,
and no ray or prefix campaign is admitted by naming these observables.

## Staircase inequality and explicit bounded alternative

For finite x put n=max(ceil(bitlen(x)/2)-1,0),
u_i(t)=bit_i(A^t x), w_j(s)=u_(2j)(s-j). For s>=n,
V_s=sum_(j=1..n)w_j(s). The top pair2n,2n+1 stays nonzero.
A zero adjacent pair over L times forces the next higher pair zero over
L-1 times. Thus w_j,w_(j+1) cannot both vanish for n-j+1 consecutive
ages starting at S>=n+1. Disjoint pairs j=n,n-2,... give

    sum_(s=S..S+W-1)V_s(x)
      >=sum_(r=0..floor((n-1)/2))floor(W/(2r+1)),
    R(x)>=H_n, bitlen(x)<=4g(K)+2 if finite x in E_K.

This is growth with ORIGINAL support size, not age growth of a fixed
finite input. An explicit late-age witness interval is proved, not run.
For general x in E_K, the exact finite-entry decomposition gives
R(pi^h T^h x)<=K, hence

    bitlen(T^h x)<=B_explicit(K)=2h_V(K)+4g(K)+2.

This replaces the nonconstructive support bound and terminating cover
search with an explicit exponential bound. It still does NOT enumerate
E_K or decide equality of a candidate with the full actual survivor.

For arbitrary x, keep w_(n+1) rather than setting it zero. Each event P_n(t)
forces a staggered event in each chosen disjoint index pair over a time
interval of length1,3,5,...; a single occurrence accounts for at most that
many high events. This is the transport counting proof. The physical rays
are -2n-t,-2n-t-1; their backward cones avoid the attached right fringe.
The actual u/t branch is on a DIFFERENT line. Its bounded gaps alone
supply neither characteristic density nor anchored J growth.

## Temporal coding, its obstruction, and actual gate bridge

Theta(x)_t=A^t x mod4 is a computable triangular homeomorphism to the
four-symbol one-sided shift; Theta A=shift Theta. Spatial deletion becomes
Theta pi=Phi Theta, where

    g((a0,a1),(b0,b1))=(r,s),
    r=b0 XOR(a0 ORa1), s=b1 XOR(a1 ORr),
    (Phi b)_t=g(b_t,b_(t+1)).

x is rational iff Theta(x) is eventually periodic: A preserves a given
finite spatial-tail class; Phi preserves a given finite temporal-tail
class. This is not Delta and reopens no universal finite-state claim.

Density NECESSITY is `refuted` on general inputs. Temporal symbol1 exactly
at powers of two, symbol0 elsewhere, optionally after ANY fixed code
prefix, gives computable irrational x with R=infinity but EVERY

    d_n^*=limsup_(W->infinity) sup_(a>=n-1) C_n(a,W)/W=0.

Any W-window has <=1+floor(log2 W) sparse events plus the fixed prefix;
Phi^n uses n+1 consecutive symbols. Bounded R would trap the A orbit
in finite A-invariant E_K and force eventual code periodicity. These
counterexamples meet every finite cylinder/observed branch prefix but
are NOT proved infinite forced or full-fringe survivors. No numerical
run was performed for this counterexample. Sufficiency R>=d_n^*H_n
and finite-window transport survive; density is not an equivalence.

For a permitted step b=Theta x,c=Theta F(x),

    Phi c=shift^2 b, c0=3,
    c_(t+1)=h(c_t,b_(t+2)),
    h(a,(r,s))=(r XOR(a0 ORa1),s XOR(a1 ORr)).

The table rows a0..3 are [0,3,2,1],[1,2,3,0],[3,2,1,0],[3,2,1,0].
Gate x mod16=7(u)/11(t) is b0=3,b1=2/1. The scan bijects b_(>=2)
with c0=3 codes. F on the unrestricted TWO gate cylinders is TWO-to-one;
one needs b1 (the actual fringe-supplied branch) to recover x uniquely.
It supplies no new monotone group gauge or finite-state closure.

For m permitted steps and n>=m,

    P_n(F^m x,t)=P_(n-m)(x,t+2m).

Depth-zero boundary events are OUTSIDE the pullback formula. The draft's
substitution c0=3 => P0(x,2)=1 is `refuted`: x11 has A11=13,A^2(11)=12,
F11=51, so P0(F11,0)=1 while P0(11,2)=0. P1(F11,0)=0 correctly matches
the valid formula. This precise index error and a fiber ambiguity were
fixed, independently rechecked, and lead-audited before acceptance.

## Verification, records, and maintenance state

One Muse (`opencode-go/muse-spark-1.3-contributor`) supplied five scoped
reviews and a final read-only cross-file audit; it is CLOSED. No pending
worker, missing new-unit review, rate-limit retry or fallback remains.
Lead independently checked every contribution. Old all-memory/all-r
review limitations remain unchanged, as recorded in the incoming handoff.

Only new scientific computation:8 three-bit neighborhoods,16 four-bit
L=2 rectangles,64 six-bit L=3 rectangles. Packed-A and independent bit
arrays agree on all88 FULL local trajectories, premise counts1/1/1.
The independent implementation reran the SAME88 cases after correcting
unenforced CPU/wall caps and an omitted reference hash; its full prior
execution is retained. No old R controls were rerun. No frontier, return,
activity-level, period, ray, comparator, or first-witness census occurred.

Exact reviewed/current sources, reviews, source/admission snapshots,
full Git, timings, hashes and atomic provenance are in:

- results/problem1/20260906_activity_staircase_{primary,independent,verification}.json
- results/problem1/20260906_activity_sparse_temporal_codes_review.json
- results/problem1/20260906_round5_final_audit.json

Corresponding check/verify/archive/audit scripts are in
experiments/problem1_nonperiodicity. Scientific counts are finite-exhaustive
only in the declared local domains; proof scopes remain partial-proof.
The rejected initial boundary/defect route is preserved in
problem1_round5_muse_boundary_proposal.md. Its physical speed2 error was
corrected to speed1; the correct transported support bound was already
known. No universal fixed-width defect no-go was established.

Commits pushed this round include d87aabf (staircase/transport) and95db571
(temporal codes/sparse obstruction); later bridge/maintenance commits are
in Git history. Immutable reference SHA256 remains
358bdc07904e77080eb78b67bdd8da25822d6b51f1a91b58b5313dfe461c1d01.
Unrelated supervisor files, ASTRA_GOAL.md, worktrees and old untracked
results were preserved. Never edit the reference or force-push.

## Continue without repeating completed work

Attack an actual full-fringe mechanism for unbounded anchored J_n or the
original fixed-survivor record. The code bridge states the exact boundary
data available; it does not give the required deep-ray events. Neither
finite-cylinder matching, initial high ones, periodic high-front behavior,
nor growth across forced shifts settles that gap. No new experiment is
pre-admitted; state a concrete falsifiable mechanism and both outcomes
before any future run. Do not repeat the five round-five proofs/checks,
round-four finite-entry/isolation/effectivity/return tests, group gauges,
or earlier frozen searches. B_all and signed nonvanishing remain unproved.
Period1 is closed; least periods>=3 are unhandled. Pure alternating traces,
all eventual period-two traces and all finite seeds retain distinct
quantifiers. This is maintenance rollover, not research blockage.
