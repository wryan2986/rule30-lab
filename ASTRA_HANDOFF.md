# Astra handoff: round 5 in-progress checkpoint, 2026-09-06

Problem 1 remains OPEN. Research continues on `research/astra-next`.
Round five began at21:20:55UTC and is still in progress. This is a logical
unit checkpoint, not goal achieved or research blocked. The complete
incoming round-four handoff is preserved byte for byte in
`docs/astra_handoff_archive_20260906_round5.md`. Read ASTRA_GOAL.md first.

## Current bottleneck

Prove unbounded activity R_N for ONE FIXED ACTUAL period-two survivor,
retaining its full fringe coupling. Use

    T(x)=x XOR((x<<1) OR(x<<2)), pi(x)=x>>2, A=pi T,
    V_s(x)=sum_(t=0..s-1)bit_(2s)(T^t x), V_0=0,
    R(x)=sup_s V_s(x), E_K={x:R(x)<=K}.

No actual-survivor growth or mortal-rational exclusion is proved. Growth
across successive forced states is insufficient; their R can grow even
from a finite initial state. Period1 is excluded; period2 and least
periods>=3 remain open, with pure/eventual-trace quantifiers distinct.

## New round-five results, accepted in scope

Read `proofs/informal/problem1_activity_staircase_bound.md` and then
`proofs/informal/problem1_activity_transport_inequality.md`.
All all-depth results retain status `partial-proof` relative to the prize.

For finite x put n=max(ceil(bitlen(x)/2)-1,0),

    u_i(t)=bit_i(A^t x), w_j(s)=u_(2j)(s-j),
    V_s(x)=sum_(j=1..n)w_j(s), s>=n.

The top pair 2n,2n+1 stays nonzero. A zero adjacent pair over L times
forces the next higher pair zero over L-1 times. The staggered terms
w_j,w_(j+1) cannot both vanish through n-j+1 consecutive ages starting
at S>=n+1. Packing disjoint pairs j=n,n-2,... proves, every W>=1,

    sum_(s=S..S+W-1)V_s(x)
      >=sum_(r=0..floor((n-1)/2))floor(W/(2r+1)).

Thus R(x)>=H_odd(floor((n-1)/2)), where
H_odd(r)=sum_(j=0..r)1/(2j+1). Let g(K)=min{r:H_odd(r)>K}.
Finite x in E_K has bitlen(x)<=4g(K)+2. An explicit short late-age
witness interval for larger support is also proved; no sampling run
was added. This is growth with ORIGINAL support size, not age growth
for the same finite x.

The reviewed finite-entry theorem gives h=h_V(K), the first r with
H_odd(r)>3K/2. For x in E_K let y=T^h x finite and z=pi^h y.
The exact nonnegative early-term decomposition gives R(z)<=K, so

    bitlen(T^h x)<=B_explicit(K)=2h_V(K)+4g(K)+2.

This replaces the previous nonconstructive support bound/terminating
cover search by an explicit exponential bound. It does not enumerate
E_K or decide equality of any candidate with the actual survivor.

The transport inequality works for ANY x in Z_2, without finite support:

    P_n(t)=bit_(2n)(A^t x) OR bit_(2n+1)(A^t x),
    C_n(a,W)=sum_(t=a..a+W-1)P_n(t),
    H_n=H_odd(floor((n-1)/2)).

For n>=1,a>=n-1,W>=1,

    sum_(s=a+2..a+W+n)V_s(x)
      >=sum_(r=0..floor((n-1)/2))ceil(C_n(a,W)/(2r+1))
      >=C_n(a,W)H_n.

The age window has W+n-1 values. On infinite inputs retain the
w_(n+1) term; setting it zero is invalid. Define

    d_n^*=limsup_(W->infinity) sup_(a>=n-1) C_n(a,W)/W.

Then R(x)>=d_n^* H_n. Uniformly positive d_n^* along unbounded n is a
SUFFICIENT growth condition, not an established actual-survivor fact.
P_n is a pair of physical characteristic rays -2n-t,-2n-t-1. Their
backward cones avoid the attached right fringe, so the sampled values
are from the same actual original spacetime. The actual u/t branch
lies on a different line: its bounded gaps do not supply this density.

## Verification and execution scope

One Muse (`opencode-go/muse-spark-1.3-contributor`) remains ACTIVE for
round five. It independently reviewed staircase Sections1-5 and
transport Sections1-4. Lead independently checked zero-window seams,
disjoint packing, event assignment, limit order and physical cones.

Local finite verification ONLY:8 three-bit neighborhoods,16 four-bit
L=2 rectangles,64 six-bit L=3 rectangles. Independent packed-A and
bit-array methods agree on all88 complete trajectories, premise counts
1/1/1. No old R numerical controls were rerun. No E_K enumeration,
return, fringe, ray, period, or first-witness census was added.

Files: `check_activity_staircase_{primary,independent}.py` and
`verify_activity_staircase.py` under experiments/problem1_nonperiodicity;
three corresponding `results/problem1/20260906_activity_staircase_*.json`
records. The verification record archives exact reviewed/current sources,
reviews, full Git, timings, source/admission hashes and lead disposition.
The independent run corrected declared-but-unenforced CPU/wall caps and
an omitted reference hash; SAME88-case payload unchanged, full prior
execution retained in the corrected record. The reviewer documents scope.

Immutable reference SHA256 remains
358bdc07904e77080eb78b67bdd8da25822d6b51f1a91b58b5313dfe461c1d01.
Pre-existing supervisor files, ASTRA_GOAL.md, worktrees and unrelated
untracked results are preserved. Never force-push or edit the reference.

## Sparse temporal codes: accepted second unit

Read `problem1_activity_sparse_temporal_codes.md` and its full review.
Status `partial-proof`: Theta(x)_t=A^t x mod4 is a computable triangular
homeomorphism conjugating A to the four-symbol one-sided shift. Spatial
pair deletion pi becomes Phi on adjacent temporal symbols:

    g((a0,a1),(b0,b1))=(r,s),
    r=b0 XOR(a0 ORa1), s=b1 XOR(a1 ORr),
    (Phi b)_t=g(b_t,b_(t+1)), Theta pi=Phi Theta.

Given rational x, its A orbit lies in a fixed finite spatial-tail class;
conversely an eventually periodic temporal code remains in a fixed finite
class under Phi. Thus x is rational iff Theta(x) is eventually periodic.

NECESSITY of positive characteristic density is now `refuted` on general
inputs. Set temporal code symbol1 at powers of two and symbol0 elsewhere,
optionally after ANY prescribed finite code prefix. Its inverse x is
computable irrational, EVERY d_n^*=0, but R(x)=infinity. Any W-time window
has <=1+floor(log2 W) sparse events plus the fixed prefix; Phi^n uses only
n+1 consecutive temporal symbols. Bounded R would make the A orbit lie
in finite A-invariant E_K and hence make the code eventually periodic.
These counterexamples meet every finite binary cylinder, including any
finite observed survivor prefix, but are NOT proved infinite forced or
full-fringe survivors. No numerical experiment was run for this unit.

The transport inequality remains valid. Fixed-n density limits can miss
intermittent events relevant when n and W grow together. Do not mistake
its sufficient condition for an equivalence or reopen a ray-density census.
Exact proof/review snapshots, dependencies, lead disposition and archive
builder are in `results/problem1/20260906_activity_sparse_temporal_codes_review.json`
and `archive_activity_temporal_codes.py` in the experiment directory.

The first unit is committed/pushed as d87aabf. This second unit is being
checkpointed next. Muse is deriving the exact forced-step bridge in the
new temporal-code coordinates; that bridge is NOT yet accepted. It adds
no new monotone invariant or permission to repeat the old group gauges.

## In progress / next logical unit

A separate nearest-column temporal-defect route supplied only the known
boundary equations. The initial Muse proposal mixed physical speed1
with right-edge speed2 and was rejected; no numerical campaign followed.
Its temporary sidecar is not a new no-go theorem or admitted experiment.

After the sparse-code review, prioritize simultaneous n,W finite-window
transport or a new full-fringe lower bound, preserving the same fixed
survivor. Do not substitute initial nonzero pairs for recurrent activity.
Do not repeat round-four finite-entry/isolation, return nonincrease
counterexample, rational profile proofs or numerical checks. All old
all-memory/all-r review limits, B_all and signed nonvanishing gaps remain
as recorded in the incoming archived handoff.
