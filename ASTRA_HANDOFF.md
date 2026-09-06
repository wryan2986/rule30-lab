# Astra handoff: round 6 maintenance checkpoint, 2026-09-06

Problem 1 remains OPEN. This is time-maintenance rollover, not goal achieved,
research blocked, or research exhaustion. Round six began at 22:26:45 UTC;
the final atomic audit records the checkpoint time and elapsed seconds.
Research continues on `research/astra-next`. Read ASTRA_GOAL.md first.
The incoming round-five handoff is preserved byte for byte in
`docs/astra_handoff_archive_20260906_round6.md`.

## Current bottleneck and reading order

Prove that the FULL-FRINGE inverse-scan diagonal is incompatible with finite
entry for ONE FIXED ACTUAL survivor. Round six has now stated both sides
in the same temporal coordinates; incompatibility remains unproved.

Read these notes in proofs/informal:

1. `problem1_full_fringe_temporal_diagonal.md` (exact full-fringe premise).
2. `problem1_anchored_activity_finite_entry.md` (new equivalence and bounds).
3. `problem1_finite_entry_period_tower.md` (mortal spatial tail restriction).
4. `problem1_anchored_activity_vertical_spine_obstruction.md` (failed shortcut).
5. Corresponding review files (all accepted in their stated scopes).

The round-five gate bridge, joint-window target, transport, sparse-code,
and staircase results remain established and need not be repeated.
Their compact formulas and references are in the incoming handoff archive.
All new all-depth results retain `partial-proof` relative to the prize;
actual-survivor growth remains `inconclusive`.

## Exact full-fringe diagonal, not just permitted gates

Let b=Theta(x), Theta(x)_t=A^t(x) mod4, Phi Theta=Theta pi, and define

    (I_a b)_0=a,
    (I_a b)_(t+1)=h((I_a b)_t,b_t),
    h((a0,a1),(r,s))=(r XOR(a0 ORa1),s XOR(a1 ORr)).

Then Theta(4x+a)=I_a Theta(x) and Phi I_a=id. The symbol a is an
INITIAL spatial pair, not a u/t branch. For the attached initial right
half use the facing-inward symbols a_j=r_(2j)(0)+2r_(2j-1)(0). Put

    B_m=I_(a_m)...I_(a_1)b,
    C_m=shift^(2m) B_m, D_m=(B_m)_(2m).

C_m is exactly Theta of the ACTUAL center-and-left row at time 2m.
The initial cut at physical 2m contains every relevant backward cone.
The center is 1010... at ALL times iff D_m=3 at EVERY m>=0.
For the original zero right half this becomes

    (I_0^m b)_(2m)=3 for all m>=0.                    (FULL)

For each fixed initial right half, b -> (D_m)_m is a triangular
homeomorphism: D_m is a permutation of b_m when the earlier symbols
are fixed. This proves exact realization, NOT growth. Hand checks only:
zero-right D0,D1,D2 force b0,b1,b2=3,2,2; no longer prefix was generated.

Phi C_(m+1)=shift^2 C_m always. Under FULL, C_(m+1)=I_3 shift^2 C_m,
which recovers the old gate bridge but by itself loses the full initial
right boundary. At any actual even row, b1=2 iff its right pair is00
(u); otherwise b1=1 (t). The known constant-u survivor5/3 has b2=1
and D2=2 under zero initial right fringe, so infinite gate permission
still does not give FULL. This is a coordinate check of an old countermodel.

DO NOT replace shift^(2m) I_0^m by (shift^2 I_0)^m: that resets the
right fringe after every block. Eventual period two must first be rebased
at an actual phase-one row beyond its transient, retaining the resulting
a_j (eventually zero under finite support, generally not all zero).
Uniform exclusion for all finite fringes would be a sufficient stronger
statement, not an asserted equivalence of all those quantifiers.

## Anchored activity is now an EQUIVALENT target

Use T(x)=x XOR((x<<1) OR(x<<2)), pi=x>>2, A=pi T, and the existing
P_n(x,t)=OR of bits2n,2n+1 of A^t x, J_n=sum_(t=0..n-1)P_n(x,t).
Write Q(x)=sup_n J_n(x); Q here is a record, NOT the old forward generator.
Let H_m=sum_(r=1..m)1/r and h_J(K)=min{h>=0:H_(h+1)>K}.

The new theorem proves, for arbitrary 2-adic x,

    Q(x)<=K => A^h x and T^h x are finite, h=h_J(K),
    Q(x)<infinity iff R(x)<infinity iff finite entry under T or A.

The unasserted converse from round five is now proved. The new proof
uses the bi-infinite A rule: adjacent temporal pair codes satisfy
b_(j+1)=Phi b_j; g(a,0)=3 for a!=0 preserves the last nonzero time.
If each pair has <=K active times, all share last time M and final row1.
Every r+1-pair input interval for that row contains a one at time M-r,
so H_(M+1)<=K. Even spatial limits of bounded J inherit this total
budget, and ALL vanish at the SAME h_J(K); compactness gives finite entry.

For finite z, EXACTLY Q(z)=N(z)=max(ceil(bitlen(z)/2)-1,0), because
the top pair stays active forever under A. Also Q(A^h x)<=Q(x)+h.
Consequently Q(x)<=K gives

    bitlen(A^h x)<=2(K+h+1),
    bitlen(T^h x)<=2K+4h+2,
    {x:Q(x)<=K} subset {T^(-h)y:0<=y<2^(2K+4h+2)}.

These are explicit finite rational supersets, NOT an executed enumeration
or a decision that a candidate equals the actual survivor. Q levels are
NOT A-invariant: x=-3*4^(n+1), n>=2, gives Q(x)=n-1 and Q(Ax)=n.
Never import A-invariance from the older R levels.

The remaining exact question on the SAME b is FULL =>

    sup_n sum_(t=0..n-1)1[(Phi^n b)_t!=0]=infinity.

No periodicity, density, finite list, branch-frequency or cone argument
has established this implication. No census is admitted by naming it.

## The bounded alternative has restricted spatial tail periods

New `partial-proof`: every NONZERO bi-infinite A row with first extinction
height e is periodic: e=1 gives the all-one row; e>=2 gives least BINARY
spatial period p=3*2^k, 0<=k<=e-2. No initial periodicity is assumed.
Inverse states s_i=v_i+2v_(i+1) obey f0=[0,2,3,3], f1=[2,0,1,1].
A periodic output gives a four-state return map. At a zero output phase,
f0 followed by either next map has rank<=2. Hence a nonconstant periodic
output of least period p has preimages of least period p or2p, at most
TWO preimages as actual bi-infinite rows. Constant1 instead has the three
rotations of001 as preimages; constant0 has only constant0/1.

With phases counted separately, S1=1,S2=3, S_e<=2S_(e-1), e>=3;
therefore #{v:A^h v=0}<=3*2^(h-1)-1 for h>=1. This is a proved finite
bound, NOT an enumerated mortality tree. For finite-entry x with entry h,
its least eventual spatial period is1 or3*2^k, with common tail period
P_0=P_1=1 and P_h=3*2^(h-2) for h>=2. Its reduced denominator divides
2^P_h-1. Q<=K supplies h=h_J(K). These restrictions retain EVERY finite
integer in the period1 case; they do not settle the main obstruction.

The finite-A TEMPORAL dyadic clock is an OLD IMPORT from
`problem1_frontier_head_dynamics.md` Section2. A duplicate draft derivation
was replaced by that citation, not claimed as new; no old cycle check ran.

## A precise failed vertical-alignment shortcut

Status `refuted`: bounded pair activity K does NOT imply extinction by K,
nor does a final all-one row supply one pair active at EVERY earlier age.
The exact period-six row50 has A rows50,23,10,45,36,63,0 and temporal
pair words (2,3,2,1,0,3), (0,1,2,3,1,3), (3,1,0,2,2,3), then zero.
Each pair has five active times and misses a different time. Thus x=-50/63
has Q(x)=5 but first finite entry6. The spatial-period/zero-row argument
supplies the infinite scope; the computation checks the fixed certificate.
This refutes only coefficient ONE, not every cK bound or harmonic optimality.
It is not a permitted survivor and gives no actual-growth counterexample.

## Review corrections and verification state

One Muse worker (`opencode-go/muse-spark-1.3-contributor`, thread
01a078d5-58aa-7ee3-9c1d-15b1bbaa1eed) supplied the four scoped reviews;
the lead independently audited and accepted them. Its first anchored
review falsely extended AFTER deleting low bits, pinning an artificial
boundary at zero. The actual proof extends the original row FIRST and
then translates: v_i^(l)=bar{x}_(i+2n_l) for ALL integer i. Every fixed
negative offset eventually reads genuine input bits. The reviewer
withdrew its counterexample and re-derived the full original theorem.
Exact rejected and corrected versions are retained in the audit.

The sidecar cone memo is corrected EXPOSITION, not a new no-go. Actual
branch points are (-2,2m),(-3,2m), not merely columns>=-1; the only even
branch points in the n>=1 ray cones are the m=0 pair in n=1. Odd-time
(-3,1) is an explicit exception to the formerly overbroad claim.
Causality alone does NOT refute a constraint from global center consistency.
The valid forced-to-original anchored budget is n>t+3m; no multiplicity
mechanism follows. See `problem1_round6_muse_characteristic_coupling.md`.

Only new scientific computation: the SINGLE six-cell input50 for six updates
(all seven complete rows), plus18 declared g seams. Packed cyclic A and
independent physical Rule30 arrays agree on the complete payload and hash.
The independent implementation ran this SAME case three times: initial,
then two repairs of required provenance/caps. All executions are retained.
There was no input, period, height, frontier, ray or prefix extension.
The final replay wrapper changes only authenticated archival loading and
error handling; its successful scientific code matches the executed version.
A metadata-only replay with /tmp disabled verifies the already-written
record without recomputing a trajectory; both source versions are archived.
No provider429 or fallback occurred. No mainproblem proof candidate is claimed.

Exact reviewed/current sources, initial failed review, dependencies,
full Git, timings, hashes and atomic provenance are in
`results/problem1/20260906_round6_audit.json`; builder
`experiments/problem1_nonperiodicity/audit_astra_round6.py`.
Scientific records are `results/problem1/20260906_anchored_spine_`
`{primary,independent}.json`; matching check scripts are in the experiment
directory. Checkpoint94f28fc contains the first two accepted units;
later logical/maintenance commits are in Git history.
Immutable reference SHA256 remains
358bdc07904e77080eb78b67bdd8da25822d6b51f1a91b58b5313dfe461c1d01.
Unrelated supervisor files, ASTRA_GOAL.md, worktrees and old untracked results
remain untouched. Never force-push or edit the immutable reference.

## Continue without repeating completed work

Attack an actual incompatibility between the fixed-boundary inverse-scan
diagonal and finite entry. The two sides are now exact; more observables,
finite ray samples, larger prefix boxes, or a finite-level list would not
supply the missing mechanism. State both outcomes of any concrete new
experiment before running it. Do not repeat the old R-return nonincrease,
finite-entry/isolation/effectivity, staircase, density, gate or group-gauge
work. B_all and signed nonvanishing remain open. Period1 is closed;
least periods>=3 are unhandled. Pure traces, arbitrary eventual traces,
and arbitrary finite seeds/fringes retain distinct quantifiers.
