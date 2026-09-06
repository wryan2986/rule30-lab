# Temporal-code bridge for one forced step

Status: `partial-proof`, corrected derivation independently rechecked
and accepted by the lead in scope. Problem 1 remains open. No experiment
run, admitted, or proposed. This file is a coordinate bridge between
the temporal code scan and one forced step; it is NOT a new monotone
invariant and NOT permission to rerun D4/group-count experiments.

Review: `problem1_activity_temporal_gate_bridge_review.md`. The exact
reviewed source, corrected-error disposition and current source are in
`results/problem1/20260906_round5_final_audit.json`. The lead independently
checked the gate fibers, full scan and boundary counterexample.

## 1. Setup and imports

Write b = Theta(x), c = Theta(F(x)) with Theta(y)_t = A^t(y) mod 4.
Import pi F = A^2 on the permitted domain, the conjugacy
Theta(Ay) = shift(Theta(y)), the deletion rule Theta(pi y) =
Phi(Theta(y)) with g(a,b) = (beta_0 XOR (alpha_0 OR alpha_1),
beta_1 XOR (alpha_1 OR r)), and the exact ray identity
P_n(y,t) = 1[(Phi^n Theta(y))_t != 0]. One forced step means the low
pair of Fx is 3 with the actual gate below. The full-fringe recurrence
import supplies the actual branch letter q; nothing here replaces it
by an arbitrary gate.

## 2. Forced-step code equations (`partial-proof`)

Theta(pi Fx) = Phi(c) by deletion, while pi Fx = A^2 x gives
Theta(A^2 x) = shift^2(b) by conjugacy. Hence on the permitted domain

  Phi(c) = shift^2(b),   c_0 = 3.

Write a = c_t = (a0, a1) and target (r,s) = b_{t+2}. From
g(a, c_{t+1}) = (r,s), inversion of the two defining equations gives
the forward scan

  c_{t+1} = h(c_t, b_{t+2}),
  h(a,(r,s)) = (r XOR (a0 OR a1), s XOR (a1 OR r)).

For fixed a, h(a, .) is a permutation of the four symbols (recover r
first, then s). The scan therefore gives a unique c with c_0 = 3 from
each tail b_{>=2} -- BUT F on the unrestricted 2-adic gate-cylinder union is
2-to-1, because c fixes b_{>=2} and not b_1. The exact bijection is
between tail b_{>=2} and c with c_0 = 3; x-recovery must additionally
supply b_0 = 3 and b_1 = 1 or 2, with the actual branch known from the
full fringe (not freely chosen). Each fixed-gate branch is then
bijective. The scan is not a finite-state closure: c_{t+1} reads the
unbounded input stream b_{t+2}. Hand-verified table (rows a = 0..3,
columns b = 0..3):

  [0,3,2,1], [1,2,3,0], [3,2,1,0], [3,2,1,0].

Gate check by the temporal (not spatial) reading b_1 = A(x) mod 4:
x low 4 = 7 gives bit_0(Ax) = 1 XOR 1 = 0, bit_1(Ax) = 0 XOR 1 = 1,
so b_1 = 2 for u; x low 4 = 11 gives bit_0(Ax) = 0 XOR 1 = 1,
bit_1(Ax) = 1 XOR 1 = 0, so b_1 = 1 for t. Both have b_0 = 3.

## 3. Ray-count shift (`partial-proof`)

Phi is a sliding-block code, hence commutes with shift (verified
index by index: both orders give g(b_{t+k}, b_{t+k+1})). P_0 uses the
SAME pair-OR formula extended to n = 0: P_0(y,s) := u_0(s) OR u_1(s),
which coincides with 1[Theta(y)_s != 0] since the raw symbol is that
low pair. For n >= 1:

  P_n(Fx,t) = 1[(Phi^n c)_t != 0]
            = 1[(shift^2 Phi^{n-1} b)_t != 0]
            = P_{n-1}(x,t+2).

Iterating m steps, assuming every one of those steps is permitted,
for n >= m:

  P_n(F^m x,t) = P_{n-m}(x,t+2m).

Each forced step trades one ray-depth unit for two time units. The
chain bottoms out: pulling a new-state depth-n event back to the old
state lowers depth by 1, and n = 0 cannot be pulled back. In
particular c_0 = 3 is P_0(Fx,0) = 1 with n = 0, OUTSIDE the shift's
n >= 1 domain, and it does NOT map to P_0(x,2). Exact hand
counterexample on the permitted (t-gate) domain, x = 11: A(11) =
2 XOR (5 OR 11) = 2 XOR 15 = 13, A^2(11) = A(13) = 3 XOR (6 OR 13) =
3 XOR 15 = 12, and the forced step F(11) = 51 satisfies pi(51) = 12 =
A^2(11) with low pair 3. Then c_0 = 51 mod 4 = 3, yet P_0(x,2) reads
bits 0,1 of 12 = 0. The invalid boundary substitution is refuted (no
machine run). The valid shift still holds at n = 1: P_1(F(11),0)
reads bits 2,3 of 51 = 0, correctly equal to P_0(x,2) = 0. The shift
manufactures no deep original ray from a shallow event, and the
n >= m budget makes the depth cost explicit.

## 4. Novelty fence and joint-window target

Against the group-cocycle no-go: this scan is a change of coordinates
for one forced step; each fixed scan state h is a permutation of the
input symbol, and no monotone quantity has been proved, so it reopens
no counting experiment. Against the coupled additive no-go: no
additive word functional is asserted.

Joint-window target (unproved, no census admitted): if for some
epsilon > 0, unboundedly many n, and windows a >= n-1, W >= n with
C_n(a,W) >= epsilon W, then (5) gives sum V >= epsilon W H_n over at
most 2W ages, so R >= epsilon H_n / 2 -> infinity. No actual such
windows are proved; no window census is admitted to look for them.
The full-fringe coupling that could supply them remains inconclusive.
