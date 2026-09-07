# Transport of cycle-entry delays into spatial disagreements

Status: `partial-proof` for the exact identities below. Review and lead
disposition are recorded in problem1_round9_fresh_review.md and the handoff.
The bounded-delay and FULL/finite-entry exclusions are `inconclusive`.
Problem 1 remains OPEN. No numerical experiment is used in this note.

## 0. Admission and route selection

Round eight closed a period-dependent local lag bound at its precise
finite-entry/three-diagonal scope. It left open whether uniformly bounded
least preperiods along ONE infinite permitted orbit force bounded periods.
The routes considered here are:

1. Transport temporal delays along that same orbit to an exact spatial
   quantity. This has the lowest proof cost and keeps the infinite future.
2. Strengthen the local family to initially finite inputs. A separate
   sidecar treats this; no varying family answers route 1.
3. Prove a universal settling-speed estimate for the original I_0 fringe.
   The available inverse-scan onset bound depends on its entire periodic
   drive. No improved speed is assumed, and no lag census is admitted.

For route 1, an exact equivalence would locate precisely the spatial
disagreements that a bounded-lag argument must exclude. A failure would
identify a lost phase or an invalid temporal/spatial transfer. The result
is a threshold identity, not an exclusion of its bounded alternative.

Import A, pi, Theta, Phi and the permitted map F from the reviewed
temporal-code bridge and full-fringe notes. Write N for nonnegative finite
integers. Let ONE orbit X_m=F^m(x), m>=0, have every step permitted, so

    X_(m+1)=4 A^2 X_m+3,
    pi^n X_(m+n)=A^(2n) X_m, m,n>=0.                (1)

Assume every X_m is eventually A-periodic. Finite entry of x suffices:
the projection identity and commutation of pi with A preserve finite
entry under F, and finite A states have finite orbits. For FULL with
a fixed finite initial right fringe, (1) applies to its actual even rows.
No independently chosen or reset fringe is used.

## 1. The phase-correct cycle representative (`partial-proof`)

For an eventually A-periodic y, let tau(y) be its LEAST A-preperiod and
p(y) its LEAST eventual A-period. Define

    cyc(y)=A^k y for any k>=tau(y) with p(y) dividing k. (2)

All such k give the same state. This is the cycle representative whose
pure temporal code agrees with Theta(y) from time tau(y), at the SAME
temporal phase. In particular A^tau(y) cyc(y)=A^tau(y)y. It is not the
arbitrary first cycle state A^tau(y)y, whose code can have a different
phase. Full-code injectivity gives

    cyc(y)=y iff y is A-periodic,
    cyc(A^r y)=A^r cyc(y),
    cyc(pi^n y)=pi^n cyc(y), r,n>=0.                    (3)

For the last identity, choose a multiple of p(y) beyond both onsets;
the period of pi^n y divides p(y), and pi commutes with A. The same
choice proves the time identity, or use equality of the periodic code
completions after shifting. Also

    tau(A^r y)=max(tau(y)-r,0).                     (4)

The reverse inequality in (4) matters: if A^r y enters earlier, y was
already on its eventual cycle at that earlier total time, contradicting
the least onset. Periodic states have tau=0 throughout.

If y has finite entry, cyc(y) is finite. If y itself is finite and positive,
cyc(y) has exactly the same bit length, since A preserves finite positive
bit length. For a nonfinite finite-entry y, finiteness of cyc(y) does NOT
make y finite.

## 2. An exact threshold transport (`partial-proof`)

Define the spatial cycle-entry depth

    kappa(y)=min{n>=0:pi^n y is A-periodic},          (5)

with value infinity if this set is empty. By (3),

    kappa(y)<=n iff pi^n y=pi^n cyc(y).               (6)

The set in (5) is upward closed: spatial deletion preserves A-periodicity.
Thus kappa measures the number of low spatial pairs that must be removed
to make the actual row coincide with its phase-correct cycle representative.
For finite-entry y, kappa(y)<infinity iff y is initially finite: cyc(y) is
finite, and a finite number of differing low bits cannot change that.
This equivalence is about ONE y, not uniform boundedness along an orbit.

Put tau_m=tau(X_m), kappa_m=kappa(X_m). For EVERY m,n>=0, (1) and (4)
give the exact identity

    tau(pi^n X_(m+n))=max(tau_m-2n,0),
    kappa_(m+n)>n iff tau_m>2n.                     (7)

Infinity on the left is allowed; every tau_m is finite under the premise.
Equivalently, when m>=n,

    kappa_m<=n iff tau_(m-n)<=2n.                   (8)

For all sufficiently large m (2m>=tau_0), kappa_m<=m, and therefore

    kappa_m=min{0<=n<=m:tau_(m-n)<=2n}.              (9)

This uses the same original orbit index throughout. A high delay is not
transported into a disagreement of the original x: it appears in a LATER
row X_(m+n). At n=0, (7) is simply the correct equivalence between
nonperiodicity of X_m and positive kappa_m.

A second derivation uses the complete temporal codes C_m=Theta(X_m).
The iterated bridge gives Phi^n C_(m+n)=shift^(2n) C_m. The left side
is purely periodic iff kappa_(m+n)<=n; the right side is purely periodic
iff tau_m<=2n. This verifies the same thresholds without making any
assumption about the boundary symbol of the periodic completion.

## 3. Uniform bounds are equivalent, with exact constants (`partial-proof`)

If tau_m<=K for all m>=M, set N=ceil(K/2). Then

    kappa_j<=N for every j>=M+N.                    (10)

Conversely, if kappa_j<=N for every j>=M, then

    tau_m<=2N for every m>=max(0,M-N).              (11)

Both implications follow directly from (7); (11) applies it at j=m+N.
Consequently the sequence of least temporal preperiods is eventually
bounded iff the sequence of spatial cycle-entry depths is eventually
bounded. Since each tau_m is finite, its unboundedness requires late m;
the corresponding statement for kappa is its late behavior, since
nonfinite early rows can have kappa=infinity before physical finite entry.

More exactly, for each fixed N the sets of witnesses satisfy

    {j>=N:kappa_j>N} = N + {m>=0:tau_m>2N}.          (12)

Hence infinitely many occurrences above threshold 2N in temporal delay
are equivalent to infinitely many occurrences above spatial threshold N,
with only the displayed index translation. No frequency, growth rate,
or boundedness conclusion is manufactured by this identity.

## 4. The same finite-width disagreement strip (`partial-proof`)

Write Z_m=cyc(X_m). Taking cycle representatives of (1) yields

    pi Z_(m+1)=A^2 Z_m,
    Z_(m+1)=4 A^2 Z_m+a_m, a_m=Z_(m+1) mod4.        (13)

Here a_m is the cycle representative's low pair, NOT an initial-right-
fringe symbol and NOT a freely chosen u/t branch. It need not be 3.
The original actual X_(m+1) still has low pair 3. Under (10), X_j and
Z_j coincide in EVERY bit of index >=2N, simultaneously for all late j.
This is a fixed spatial strip at the center of the actual even rows.

For finite X_j, one may write |X_j-Z_j|<=4^N-1, but the equality of
the high parts in (6) is the exact assertion; an integer-distance bound
alone would not imply it because of carries. The periods p(X_j)=p(Z_j)
can remain unbounded as far as (10)-(13) establish. The strip still
receives the evolving higher bits of Z_j; its finite width does not
supply an autonomous finite-state system or periodicity in j.

## 5. The highest disagreement has an exact reset rule (`partial-proof`)

Suppose X_m and Z_m differ in finitely many bits, and let d>=0 be the
HIGHEST differing bit. All higher bits agree, as do their higher bits
after every A step: A at position i reads only positions i,i+1,i+2.
At the current highest disagreement the local rule gives

    bit_d(A X_m) XOR bit_d(A Z_m)
       = 1 XOR bit_(d+1)(Z_m).                     (14)

Indeed the common input at d+2 cancels, while OR with the common bit
at d+1 either erases the difference (if that bit is 1) or preserves it.
Once erased at d it cannot be recreated there from lower differences.
Consequently it survives TWO A steps exactly when

    bit_(d+1)(Z_m)=bit_(d+1)(A Z_m)=0.              (15)

Equation (13) and the actual F rule give the integer XOR identity

    X_(m+1) XOR Z_(m+1)
       =4 (A^2 X_m XOR A^2 Z_m)+(3 XOR a_m).        (16)

The two terms have disjoint bit positions, so ordinary addition in (16)
is harmless. Thus the highest disagreement at the next row is exactly
d+2 if and only if (15) holds. If (15) fails, every next disagreement
has index <=d+1 (or there is none). New disagreements in the low pair
must be retained; erasing the old disagreement need not make X_(m+1)
periodic. When there is no current disagreement, only that new low pair
can differ. The fixed55 cycle-mate example already demonstrates such a
new defect and is not rerun here.

For initially finite X_m, kappa_m=0 if there is no disagreement, and
kappa_m=floor(d/2)+1 otherwise. The bit rule (15) is more precise than
a rule on pair depth alone: a decrease of d by one can leave its pair
index unchanged. A proof cannot replace this distinction by automatic
pair synchronization. In particular d=0 always erases at the first A
step under FULL, because the common bit at 1 equals the actual 1.
This does not exclude later births or higher disagreements.

## 6. Remaining obligation and stopping fence (`inconclusive`)

To prove unbounded lag heights along a FULL finite-entry candidate, it
would suffice and be necessary to show that no fixed spatial deletion
depth makes all its late actual even rows A-periodic. This is stronger
than the already proved infinitely many kappa_m>0 at doubling sources.
The proof-critical missing step is exclusion of EVERY finite width,
using the original FULL future, not merely a varying family or a local
pair mismatch. Even such an exclusion would establish unbounded delays,
not yet the original bounded-activity contradiction: (7) moves to later
rows, and (9) allows kappa_m to grow below m for a finite-entry input.

No fixed-width graph, period list, lag sweep, or longer actual prefix
is run or authorized by this note. Round-eight local controls and the
fixed55 counterexample retain their exact scopes. The present result
does not prove uniformly bounded delays force bounded periods, does not
prove unbounded delays under FULL, and does not prove Problem 1.

Dependencies: problem1_activity_temporal_gate_bridge.md Sections 1-3;
problem1_activity_sparse_temporal_codes.md Sections 1-2;
problem1_full_fringe_temporal_diagonal.md Sections 2-4;
problem1_inverse_scan_reset_language.md Section 3;
problem1_anchored_activity_finite_entry.md Section 3.
