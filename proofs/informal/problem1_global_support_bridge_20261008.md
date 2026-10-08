# Problem 1: complete-half gates and the original-support seam

Status: `partial-proof` for the exact reductions and one-passage support
certificate below; `inconclusive` for termination and the excess target.
Dependencies: `problem1_period_two_phase_maps_20261008.md`,
`problem1_shift_tail_excess_reduction.md`, and
`problem1_normalized_excess_germ_is_physical_orbit_invariant.md`.
No finite census is used as evidence for an infinite assertion here.

## 1. Keep one original finite row

Fix a nonzero finite physical row `r`, and a nonnegative original right
support bound `b`. Set

    v = L_b(r) = sum_(i<=b) r_i(0) 2^(b-i) > 0.

This is one fixed seed. Extending the original cut gives
`L_(b+n)(r)=2^n v`. Let `Y_t=sum_(j>=0) r_(-j)(t) 2^j` be the
actual center-and-left half at physical time `t`. The exact front identity is

    tau(Y_(b+n)) = max(tau(2^n v) - (b+n), 0).       (1)

Consequently the strong original-support target

    limsup_(n->infinity) [tau(2^n v)-n] = infinity    (2)

would exclude every eventual bounded delay strip for this same row.
Mere divergence of `tau(2^n v)` does not give (2). A later physical
restart must retain the exact descendant of `r`; the restart covariance
in the dependency above only reindexes its normalized excess germ.
It does not produce a new consumable support resource.

## 2. The complete-half period-two reduction

Suppose the future center alternates after time `t_0`, chosen with center
one. Use the actual complete halves of `U^t_0(r)`:

    L_0 = sum_(j>=0) r_(-j)(t_0) 2^j,
    R_0 = sum_(j>=1) r_j(t_0) 2^(j-1).

Both are finite. Here `R_m` denotes a right half, not the original bound
`b`, and `U` in `U^t_0(r)` denotes physical Rule 30 evolution.
The phase-map dependency proves, with

    A(z) = (z>>2) XOR ((z>>1) OR z),
    Psi(L) = 4 A^2(L)+3,
    D(R) = (R<<1) XOR (R OR (R>>1)),
    F(R) = D(D(R) XOR 1),
    q(R) = 1 iff R=0 mod4,

that the center alternates forever exactly when every iterate
`(L_m,R_m)=(Psi^m(L_0),F^m(R_0))` passes

    L_m=7 mod16 if q(R_m)=1; otherwise L_m=11 mod16. (3)

Under (3), these iterates are the actual full physical halves at
`t_0+2m`. Thus no independent fringe schedule has been substituted.
Excluding infinite survivors for *all* finite pairs is sufficient for
the original finite-support class and is exactly period-two exclusion
for arbitrary finite configurations. It is not an all-period theorem.

## 3. What the finite inverse certifies

The phase-map note gives an exact inverse test for one passage.
From a proposed successor `R_next`, recover
`R=J^(-2)(R_next>>2)`, where

    J(z) = z XOR ((z>>1) OR (z>>2)),

and check `F(R)=R_next`. This determines `q` and the low-four-bit
seed `7` or `11` for the left inverse. For
`z=(L_next-3)/4`, the 16-state recursion for `A^2(L)=z` reads
`bitlen(z)` output bits; a finite predecessor exists precisely when its
terminal four-bit state is `0000`. Positive finite `A^2` inputs preserve
bit length, and the zero state stays zero on the remaining zero output.
Hence this checks the ordinary-zero boundary, not merely a 2-adic inverse.

For comparison with the older inverse-section notation, define

    T(z) = z XOR ((z<<1) OR (z<<2)),
    U_1(z) = T(z) XOR 1,
    P(z) = T(z) XOR 1 XOR (2 if z is even else 0),

and let `t,u,p` be their 2-adic inverses. Writing an admissible
`L=4w+3`, the two-step fringe identity is
`L_next=U_1(P(w))` if `q=1`, and `L_next=T(P(w))` if `q=0`.
Indeed `A(4w+3)=P(w)`; at the intermediate center-zero phase,
the next left half is `T(P(w)) XOR q` under the compatibility gate.
Thus the unique branch-selected 2-adic predecessor is

    L = 4 p(u(L_next))+3  if q=1,
    L = 4 p(t(L_next))+3  if q=0.                  (4)

The inner inverse is applied first. Formula (4) and the four-bit recursion
describe the same unique inverse branch. Ordinary finiteness of (4) is
an additional condition; the terminal-zero test supplies exactly that
condition. No assertion about a nine-state composite automaton is needed.

## 4. The remaining original-support obligation

The support test is automatic on every finite admissible forward passage:
its actual finite predecessor already witnesses success. Repeating that
test along an assumed infinite forward survivor therefore supplies no
contradiction and no bound on the number of passages. Both autonomous
halves gain two bits per passage, so their relative bit lengths are
constant; support width alone supplies no decreasing quantity either.

The precise missing period-two statement is that every fixed finite pair
eventually fails (3). The stronger target (2) also requires control of
all other eventual periods and of unbounded original-cut delays.
A local affine transport theorem or a finite inverse certificate governs
a specified connector or inverse passage. Neither bounds the length of
the full spatial basin, nor couples successive returns to a resource
bounded by the support of the one original row in (1).
The complete-half formulation retains that coupling as an exact orbit
condition; proving its termination remains open. The new one-passage
certificate does not remove this infinite quantifier.
