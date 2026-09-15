# Two-step same-period repair trains are exact truncated Rule-30 fringe orbits

Status: exact reduction and finite period-dependent train bound. Problem 1 remains open.

## Setup

Fix `p>=1` and put `m=2p`. Let `z` be a finite `A^p`-fixed state with return fringe `R`:

\[
T^p(z)=2^m z+R,\qquad 0\le R<2^m.
\]

Suppose the next collision repairs after one row, so that

\[
z_+=T^2(z)
\]

is again `A^p`-fixed. Write its return fringe as `R_+`:

\[
T^p(z_+)=2^m z_+ +R_+.
\]

The previous runs classified when this repair occurs from bounded endpoint data. Here the goal is to identify the exact map `R -> R_+`.

## Triangularity modulo `2^m`

Rule 30 on integer bits has the local form

\[
(Tx)_i=x_i\oplus(x_{i-1}\lor x_{i-2}).
\]

Therefore every output bit below position `m` depends only on input bits below position `m`. Equivalently,

\[
T(X)\bmod 2^m=T(X\bmod 2^m)\bmod 2^m.
\]

Iterating,

\[
T^q(X)\bmod 2^m=T^q(X\bmod 2^m)\bmod 2^m
\]

for every `q>=0`.

## Exact two-step fringe transport

Since physical time commutes with itself,

\[
T^p(z_+)=T^p(T^2z)=T^2(T^pz)=T^2(2^m z+R).
\]

Reducing modulo `2^m` and using triangularity gives

\[
R_+=T^p(z_+)\bmod2^m
     =T^2(2^m z+R)\bmod2^m
     =T^2(R)\bmod2^m.
\]

Hence every successful same-period two-step repair obeys the exact fringe map

\[
\boxed{R_+=F_p(R):=T^2(R)\bmod2^{2p}.}
\]

No reconstruction of the often enormous fixed state is needed.

More generally, if an alternating same-period repair train contains fixed nodes

\[
z_j=T^{2j}(z_0),\qquad j=0,1,\ldots,N,
\]

with return fringes `R_j`, then

\[
\boxed{R_j=T^{2j}(R_0)\bmod2^{2p}.}
\]

Thus the entire repair train is a segment of one orbit of the finite permutation `T^2 mod 2^{2p}`, filtered by the exact repair endpoint conditions from the preceding notes.

## Injectivity and no repeated fringe in a finite physical repair train

Rule 30 modulo `2^m` is triangular with diagonal coefficient one, hence bijective; therefore `F_p=T^2 mod 2^m` is also a permutation.

Previous work proved that for fixed `p` a complete return fringe determines at most one finite `A^p`-fixed state. Consequently, if `R_i=R_j` for two fixed nodes in the same repair train, then `z_i=z_j`.

But every nonzero finite Rule-30 word gains two leading positions per physical step: the leading edge of `T(w)` is `11` beyond the old top bit. Hence

\[
\operatorname{bitlength}(T^q w)=\operatorname{bitlength}(w)+2q
\]

for nonzero finite `w`. In particular `T^{2(j-i)}z_i` cannot equal `z_i` when `j>i`.

Therefore a finite same-period repair train cannot revisit a return fringe.

## Explicit period-dependent bound for an alternating short-gap train

An alternating fixed/collision/fixed repair train requires every fixed node to have corridor `G in {0,1}`; otherwise its next collision is not the immediate next physical row.

For `m=2p`, the number of possible nonzero fringes with `G=0` is `2^{m-1}` and with `G=1` is `2^{m-2}`. Since no fringe can repeat, the number of fixed nodes in such an alternating same-period train is bounded by

\[
\boxed{N_{\rm fixed}\le 2^{m-1}+2^{m-2}=3\cdot2^{m-2}=3\cdot4^{p-1}.}
\]

This bound is intentionally crude, but it is the first unconditional bound depending only on the period after the small-universal-bound route was disproved by the period-8 13-node witness.

The exact endpoint repair classifiers should cut this finite set substantially; the important structural point is that the problem is now a finite permutation-orbit avoidance problem on the fringe alone.

## Consequence for the global bottleneck

A repaired long corridor can enter a substantial short-gap same-period repair train, as run 34 showed, but it cannot remain in that alternating train indefinitely for fixed `p`. Any hypothetical infinite survivor must eventually leave the train by failing a repair, developing a non-short corridor, or changing the effective period/phase mechanism.

This does not yet solve Problem 1: the bound grows exponentially with `p`, and the existing FULL/common-origin argument still has to control repeated transitions to larger periods/phases. But it removes the possibility of an infinite repair train at one fixed period and gives an exact finite-state object for sharper counting.

## Next target

Use the endpoint classifiers as a forbidden-set condition along the permutation

\[
F_p(R)=T^2(R)\bmod2^{2p}.
\]

Two concrete directions are now available:

1. compute maximal admissible repair-train lengths for modest `p` and look for a much smaller law (linear/polynomial in `p` rather than `4^p`);
2. characterize how leaving the admissible fringe set feeds the existing FULL/common-origin birth accounting, especially when the effective period increases.
