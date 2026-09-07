# Each clock doubling starts at a late diagonal under FULL

Status: `partial-proof`, independently re-derived and accepted after lead
audit. Review: `problem1_scan_doubling_cycle_lag_review.md`. The
FULL/finite-entry incompatibility is `inconclusive`; Problem 1 remains
open. No numerical experiment, period list, or diagonal census is used.

## 0. The concrete next question

The reset-language note proves that a FULL finite-entry candidate cannot
eventually put all of its diagonal samples on A-cycles. Test whether the
exact clock-doubling alternatives identify where this obstruction occurs,
instead of leaving a qualitative compactness argument. The positive
outcome would charge each necessary doubling to a specific late diagonal;
a failure would expose a missing phase or multiplicity condition. This
is an exact comparison of the same two round-six conditions, not a new
activity observable or permission to sample more prefixes.

Import Theta, pi, A, T, I_a and the full boundary from the reviewed notes.
Let a_j=0 for j>J, x!=0, W_0=x, W_m=4W_(m-1)+a_m, and

    B_m=Theta(W_m), D_m=(B_m)_(2m).

Assume finite entry A^h x finite. Write p_m for the LEAST eventual
temporal period of B_m and tau_m=tau_A(W_m). The prior note proves
tau_m is finite. Its homeomorphism argument also identifies tau_m
with the least temporal preperiod of B_m: B_m is periodic from T
exactly when Theta(A^T W_m) is purely periodic, which is equivalent
to A^T W_m being on an A-cycle.

## 1. Clock growth for every fixed nonzero finite-entry input (`partial-proof`)

Without any FULL premise, the fixed nonzero finite-entry x and the finite
right fringe imply

    p_m tends to infinity as m tends to infinity.    (1)

Here is a direct proof which includes the case A^h x=0. Put y=W_J.
The common-entry argument pi^J A^h W_J=A^h x makes A^h y finite,
and therefore Y=T^h y finite. Also y!=0 because pi^J y=x!=0. The
unit-triangular injectivity of T and T(0)=0 give Y!=0, so Y is a
positive finite integer. For m>=J+h, the actual finite fringe gives

    W_m=4^(m-J)y,
    A^h W_m=4^(m-J-h)Y,                             (2)
    L_m:=bitlen(A^h W_m)=2(m-J-h)+bitlen(Y).

To check (2), T commutes with multiplication by 4^k by its XOR/OR
formula, and A^h=pi^h T^h. The condition m-J>=h permits deleting h
zero low pairs. This is NOT a commutation claim for pi with T.

Every eventual A-cycle of W_m has finite width L_m, since A preserves
positive finite bit length after time h. Its least cycle period equals
p_m by Theta conjugacy and injectivity. Finite A-cycle states with a
given available temporal period p inject into the 4^p purely p-periodic
codes. Taking the finite union over p=1,...,P, only finitely many
finite A-cycle states have period at most a fixed P, and their widths
have a finite maximum. Since L_m
tends to infinity, p_m eventually exceeds every fixed P, proving (1).

There is also an explicit width/period bound, without a cycle catalogue:

    ceil(L_m/2) <= 4^(p_m)-1.                        (3)

For any positive finite A-cycle state z of width L, let c=Theta(z)
and N=ceil(L/2). The codes Phi^n c=Theta(pi^n z) are nonzero for
0<=n<N and zero for n=N. They are ALL distinct before zero. If
Phi^i c=Phi^j c with 0<=i<j<N, apply Phi^(N-j) to get
Phi^(N-j+i)c=0 at a depth strictly below N, a contradiction. Each
code has available period p because Phi commutes with temporal shift.
There are exactly 4^p-1 nonzero purely p-periodic words. Hence
N<=4^p-1, proving (3). This count is combinatorial, not executed.

## 2. A distinct late diagonal for every doubling (`partial-proof`)

Now assume FULL: D_m=3 for EVERY m>=0. Let

    E={m>=0:p_(m+1)=2p_m},
    d_N=|E intersect {0,...,N-1}|,
    LATE_N={j in {0,...,N}:tau_j>2j}.

The exact reset theorem gives p_N=p_0*2^(d_N), and (1) makes E infinite.
FULL supplies BOTH original gate symbols at every even row:

    (B_m)_(2m)=3, (B_m)_(2m+1) in {1,2}.            (4a)

The second identity is the already reviewed actual-gate calculation in
the full-fringe note, Section 4. It uses the actual next alternating
block and its actual right pair, not only D_m=3 in isolation.
There is one further exact consequence of the next gate. From
C_(m+1)=I_3 shift^2 C_m,
(C_(m+1))_1=H_((C_m)_2)(3). By (1) in the reset note, this lies in
{1,2} exactly when (C_m)_2 lies in {1,2}. Hence FULL also gives

    (B_m)_(2m+2) in {1,2}.                          (4b)

For each m in E, classify its input periodic alphabet:

- If the periodic tail of B_m is contained in {0,2}, then D_m=3
  is outside that alphabet. Hence tau_m>2m.
- If that periodic tail is contained in {0,3}, the gate symbol
  (B_m)_(2m+1) in {1,2} is outside its periodic alphabet. Hence
  tau_m>2m+1; using (4b) sharpens this to tau_m>2m+2. In addition
  the eventual symbols of B_(m+1) lie in
  {0,1}, so D_(m+1)=3 implies tau_(m+1)>2m+2 as well.

These are the ONLY doubling alternatives; in each the relevant symbol
count over a least period is odd. Thus EVERY doubling index m itself
is late, with lag at least THREE in the {0,3} case.
Distinct indices already give distinct witnesses; no multiplicity is
assumed or lost. For every N>=0,

    |LATE_N intersect {0,...,N-1}| >= d_N
                                  = log_2(p_N/p_0). (4)

Every counted depth concerns the SAME original code and fixed right
boundary. This proves the infinite late-cycle-entry conclusion again,
and locates the required events at the actual clock-doubling sources.
The earlier two-choice source/successor argument is sharpened by retaining
the next gate symbol in (4a). It is not a comparison with a worst-case
upper bound for a transient.

For a zero initial right half tau_m=tau_A(4^m x). With a finite
fringe use the same W_m throughout. No phase or spatial-pair symbol
is selected anew to arrange the desired witnesses.

## 3. A permitted step from a cycle has at most one transient (`partial-proof`)

For an A-periodic state x in the permitted domain, let b=Theta(x),
of least period p. The gate gives b_0=3, b_1 in {1,2}, hence p>=2.
The new code is c=I_3 shift^2 b. Its period-p drive has final two
symbols b_0=3 and b_1. Let R be the return map on scan states over
that period. Its last two factors are H_(b_1) H_3, so

    R({0,1,2,3}) subset {2,3}, R(2)=R(3).           (5)

The first inclusion follows from H_3's image {0,1}, which H_1 and
H_2 both map onto {2,3}. The equality follows because EVERY H_i
identifies 2 and 3, already at the first applied letter. This also
handles p=2, where there are no intervening factors.

Write z=R(2)=R(3), in {2,3}. Then R(z)=z. The unique purely
p-periodic driven response starts at z. The actual starting state 3
equals z or is its partner 2/3, and the first H_i identifies that
pair. Therefore c is periodic from time 0 if z=3, and has LEAST
preperiod exactly 1 if z=2. Its least eventual period is exactly p,
using Phi c=shift^2 b and the period-p response. Consequently

    p(Fx)=p(x),  tau_A(Fx) in {0,1} for tau_A(x)=0.  (6)

The claim of LEAST preperiod one cannot conceal a longer pure period:
at every positive multiple of p the state is z. If c were purely
periodic with ANY period q, a common multiple of p and q would force
its initial state 3 to equal z=2, a contradiction.

More concretely, exactly ONE of

    4 A^2 x+2,  4 A^2 x+3                          (7)

is A-periodic, and the other has least A-preperiod one. Their scans
start in states 2 and 3 under the same drive, so (5) proves this
directly via Theta. For a finite positive x this changes just the low
bit of the prospective forced state; no high-bit comparison is hidden.
The fixed55 example realizes the transient alternative, with
F55=223 and its periodic partner222.

This is a local restriction, not invariance of the periodic core. It
does NOT bound the transient after a step from a nonperiodic state.

## 4. Exact scope and unresolved step (`inconclusive`)

The number of required late depths is unbounded. Neither (3) nor (4)
proves the VALUES tau_j-2j are unbounded or their density is positive.
They may, as far as this argument shows, be one at arbitrarily sparse
depths. Nor do these late events give positive anchored activity in the
original x: W_j has an increasing attached spatial prefix, while the
anchored Q(x) budget stays on the one original input. No such transfer
or contradiction is asserted.

The same mechanism also holds for an infinite permitted F orbit with
finite entry. After its finite entry its positive widths grow by two;
the eventual code periods tend to infinity by the same finite-code
count. Apply the reset alternatives to C_(m+1)=I_3 shift^2 C_m.
Each doubling forces C_m to have positive preperiod, and the {0,3}
case forces its preperiod to exceed two by the next permitted gate.
Precisely, on this larger class
write p_m for the least eventual period of C_m; then

    #{0<=m<N:tau_A(F^m x)>0} >= log_2(p_N/p_0).

This uses positive preperiod at the current row, whereas (4) uses the
original W_m clock and its threshold 2m. The mechanism distinguishes
neither actual fringes nor particular permitted gate orbits.

A potentially sufficient next target is to forbid these specific
type-{0,2}/{0,3} transient passages for the fixed FULL realization,
or to show that only finitely many of the required passages can occur.
The fixed55 certificate already blocks a naive immediate-cycle-entry
induction; it supplies no asymptotic counterexample. No additional
period, lag, width, ray, candidate or prefix census is admitted here.
