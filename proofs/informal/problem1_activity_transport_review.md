# Adversarial review: activity transport inequality (Secs 1-4)

Objective: FIND A FATAL FLAW, especially in (5). Result: none found;
every implication, index seam, and limit order re-derived by hand below.
Secs 1-4 stay `partial-proof` (lead-derived, independently re-derived
here). The file yields a SUFFICIENT condition only; no actual d_n
positivity is proved or claimed. Problem 1 remains open. No machine
check run: the admitted 8/16/64 cones cover only the local Boolean
seams and are imported, not re-executed. Lead's A-trace conjugacy
exploration of density strictness was not duplicated.

Source: proofs/informal/problem1_activity_transport_inequality.md,
SHA256 e71bf3f9aade2d2ae397c642f9dfb2d2297f3d63ee438904e4f92ec2380a42c9.

## 1. Independent derivation

Sec 1. Diagonal identity (1) re-derived for general 2-adic x via reviewed
A^r pi^j = pi^j A^r (no truncation; all s terms present). Implication (2)
verified: zero RHS makes u_{2j}(t+1) and u_{2j+2}(t) the exact LHS and
first RHS term of the cell equation at 2j, forcing the defining OR of
P_j(t) to zero. Both staggered ages satisfy age >= index. Implication (3)
verified: zero pair at t,t+1 gives u_{2j+2}(t) = 0 from the equation at
2j, then u_{2j+3}(t) = 0 from the equation at 2j+1: exactly the checked
rectangle shape. Iteration to (4) confirmed: (3) telescopes over
overlapping windows to OR_{k=0..n-j} P_j(t+k) with no multiplicities
(Boolean union, not a signed sum), then (2) per term gives ages
t+j+1..t+n+1. No flaw.

Sec 2. Event assignment checked: fixed occurrence (j', s) admits assigned
t only in [s-n-1, s-j-1], exactly L = n-j+1 integers, so each one absorbs
at most L events and the selected pair holds at least ceil(C_n/L) ones
over [a+j+1, a+W+n]. Pairs {n,n+1}, {n-2,n-1}, ... are disjoint with L
values 1,3,...,2r_max+1. Enlargement to the common [a+2, a+W+n] (W+n-1
ages) is termwise valid since j >= 1; the a >= n-1 premise gives minimum
age a+2 >= n+1, so every selected index through n+1 appears in (1) at
every common age. Summing selected pairs can only decrease V_s. The
retained w_{n+1} is load-bearing on infinite inputs; zeroing it would be
an error and the source explicitly forbids it. C_n = 0 and n = 1 edge
cases verified (n = 1 reduces exactly to summed (2)). No flaw.

Sec 3. Density order sup_a-then-limsup_W matches the proof steps:
R(W+n-1) >= C_n(a,W) H_n for all in-scope (a,W), sup in a, divide by W,
limsup with n FIXED (H_n constant in the limit). R = infinity case is
genuinely trivial in extended reals. (7) follows per-n from (6) with
H_n -> infinity; (8) implies (7); both are marked sufficient-only and
the converse is correctly disclaimed (only d_n^* <= K/H_n is necessary).
Witness form (9) verified: window inside 0..a+W+n, denominator equals the
age count. No flaw; no Banach-limit existence smuggled in.

Sec 4. Identity (10) exact via A^t = pi^t T^t (2t-bit drop). Physical
coordinates -2n-t, -2n-t-1 confirmed against the right-edge convention
(cell index t minus bit position). Radius-one backward cones end at -2n
and -2n-1 at time 0, strictly left of the cut: no contact with attached
right-fringe cells. The unresolved-coupling statement is honest:
bounded u/t gaps live on a different line, one fixed ray cannot feed
unbounded n, and the finite-support obstruction is declared surviving.
Controls: x = 1 vacuous as claimed. x = -1 rechecked by exact 2-adic
bits: -1 = ...111 gives T(-1) = 1 (XOR against ...1110) and A(-1) = 0,
so P_n is 1 only at t = 0 and d_n^* = 0 (for n = 1 the sup_a ratio 1/W
attained at a = 0 still vanishes in limsup). The control does exactly
the required work: initial high-pair activity without recurrence gives
no density. No flaw.

## 2. Falsification attempts (hand)

Tried collapsing the telescoping in (4) into multiplicities: fails, the
union is Boolean by construction. Tried breaking the L-count with
boundary t outside [a, a+W-1]: the preimage interval already intersects
it, only shrinking assignments. Tried n = 1 degenerate packing: single
pair, L = 1, common interval exactly W ages, consistent. Tried feeding
the -1 control into (7): d_n^* = 0 kills it as intended. No
counterexample found.

## 3. Dependencies and exact issues

1. Reviewed imports (fidelity confirmed, not re-proved): A-diagonal
   identity with pi-A commutation; 8/16/64 local Boolean seams for (2)
   and (3); T(-1) = 1, R(-1) = 1 rational controls.
2. No new machine check needed or run: the only Boolean content is the
   already-covered local seams; everything else is exact indexing and
   finite counting re-derived above.
3. Open, correctly marked `inconclusive`: deriving (7), (8), or any
   useful C_n lower bound from the FULL actual fringe coupling. The
   inequality is a sufficient condition awaiting its hypothesis; actual
   d_n positivity is NOT established.
4. Minor: Sec 4's "without replacing the supplied right fringe by an
   unconstrained driver" is interpretive framing around the exact cone
   computation, not a separately proved claim. Harmless.

## Verdict

No fatal flaw in Secs 1-4. The transport inequality survives as
`partial-proof`: a correct general-input counting criterion whose
characteristic-density hypothesis is unproved for the actual survivor.
It does not bound any fixed survivor's activity by itself.
