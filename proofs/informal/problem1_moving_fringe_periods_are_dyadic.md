# Problem 1: every fixed moving-right-fringe period is dyadic

## Status

Rigorous structural refinement of the fixed-width moving-fringe no-go result. This does **not** solve Problem 1.

## Setup

Let `R` be the right endpoint of the original finite row and

    a_j(t) = (T^t r)_{R+t-j},  j >= 0.

As established in the preceding note, Rule 30 gives

    a_j(t+1) = a_j(t) XOR (a_{j-1}(t) OR a_{j-2}(t)),

where `a_-1=a_-2=0`. Hence for every fixed `J`, the prefix

    A_J(t)=(a_0(t),...,a_J(t))

is updated autonomously by a triangular Boolean permutation

    y_j = x_j XOR f_j(x_0,...,x_{j-1}).

## Lemma: triangular XOR permutations form a finite 2-group

For `n=J+1`, let `G_n` be the set of all maps of `{0,1}^n` of the form

    y_j = x_j XOR f_j(x_0,...,x_{j-1}),   0 <= j < n,

with arbitrary Boolean functions `f_j` of the preceding coordinates (and `f_0` constant).

These maps are closed under composition and inverse: successive recovery of `x_0,x_1,...` preserves the same triangular form. Thus `G_n` is a finite group.

For coordinate `j`, there are `2^(2^j)` choices of `f_j`. Therefore

    |G_n| = product_{j=0}^{n-1} 2^(2^j)
          = 2^(2^n-1).

So `G_n` is a finite 2-group. By Lagrange, every element of `G_n` has order a power of two.

## Consequence for Rule 30

The fixed-prefix Rule-30 update `F_J` belongs to `G_{J+1}`. Therefore

    ord(F_J) = 2^m

for some `m`, and every orbit period of `A_J(t)` divides `2^m`. In particular:

> **Every fixed-width moving-right-fringe prefix has a period that is a power of two.**

This strengthens the preceding result from merely `purely periodic` to `purely dyadically periodic`.

The compatible prefixes also imply that every individual moving-edge coordinate `a_j(t)` is periodic with 2-power period. Thus the infinite moving fringe carries a nested family of finite dyadic clocks. Any recurrence obstruction that only observes finitely many moving-edge bits will necessarily recur at a dyadic time separation.

## Why this matters for the remaining bottleneck

The previous note ruled out an acyclic finite-state budget based on a fixed instantaneous moving-edge prefix. The present lemma gives more structure to what replaces acyclicity: finite-width fringe information is not arbitrary recurrent state; its recurrence is constrained to powers of two.

This suggests a sharper target for an anchored FULL/non-reuse theorem. A genuinely new obstruction could come from a phase requirement incompatible with repeated dyadic returns. Conversely, any proposed finite-width invariant that merely distinguishes ordinary phases is still doomed: after a sufficiently large power-of-two time shift, every fixed observed moving-edge prefix returns exactly.

Therefore a successful finite-support budget must either

1. use information at unbounded fringe depth, so no single finite dyadic return synchronizes all required data; or
2. couple the dyadic fringe clock to a non-dyadic/core/source-indexed quantity and prove an incompatibility.

This is a useful refinement of the stopping fence: finite moving-fringe state is not just recurrent; it is a finite 2-group action.

## Computational sanity check

Direct enumeration of the actual Rule-30 prefix map for widths `n=1,...,12` produced only periods in `{1,2,4,...}`. The observed maximum periods were

    n:       1  2  3  4  5  6   7   8   9   10  11  12
    max:     1  2  2  4  8  8  16  32  32  64  64  64

This computation is only a check; the 2-group argument proves the dyadic-period statement for all finite widths.

## Open point

Problem 1 remains OPEN. The next useful question is whether the known FULL/nonreset source passages impose an anchored phase condition whose recurrence time has an odd component, or otherwise cannot synchronize with these nested dyadic moving-fringe returns.
