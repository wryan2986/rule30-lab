# Resetting cannot be global information consumption

Status: structural stopping fence. Problem 1 remains OPEN.

## Context

Run123 isolated the missing birth-budget lemma: a finite label/resource tied to the original ACTUAL finite row must have bounded reuse across resetting and nonresetting passages. One tempting interpretation is that the forced resetting source after a two-bit nonreset return might literally erase some portion of the original-row information. This note rules out that interpretation at the level of the complete finite configuration.

## Proposition: Rule 30 is injective on finite-support configurations

Write the local rule as

    f(l,c,r) = l XOR (c OR r).

Let x and x' be two finite-support configurations with the same Rule-30 image y. Choose J to the right of both supports, so x_j=x'_j=0 for all j>=J. Descend from right to left. If x_i=x'_i and x_(i+1)=x'_(i+1), equality of the output cells at i gives

    x_(i-1) XOR (x_i OR x_(i+1))
      = x'_(i-1) XOR (x'_i OR x'_(i+1)),

hence x_(i-1)=x'_(i-1). Starting from the common zero right tail and inducting leftward proves x=x'. Therefore the global Rule-30 map is injective on finite-support rows.

Equivalently, for a row known to lie in the image of a finite-support row, its predecessor is uniquely reconstructed from the zero right tail by

    x_(i-1) = y_i XOR (x_i OR x_(i+1)).

Iteration shows that every later finite-support row uniquely determines the complete original finite row.

## Consequence for the current birth-budget route

The word "resetting" in the source/core decomposition cannot mean that the physical Rule-30 evolution has destroyed or consumed original-row information. In particular, the forced resetting one-bit source at t+6 in `problem1_nonreset_return_birth_spacing.md` occurs inside a globally injective evolution: the entire row at t+6 still determines the entire row at t and, ultimately, the initial finite row.

Thus a successful finite birth budget cannot be justified by literal information erasure at reset episodes. Any finite label that becomes unavailable after a reset must be a deliberately coarse-grained, episode-specific resource with a proved one-way transition law, even though the underlying information remains recoverable from the complete row.

This does not rule out such a coarse monotone resource. Injective systems can have monotone observables on nonrecurrent orbits. It only closes the stronger but unjustified shortcut

    resetting source => loss of original finite-row information => finite number of resets/births.

## Sharpened next target

Search for an order/filtration on recoverable original-row information rather than information loss: e.g. a source-relative boundary, intercept, or nested subset of the finite original support whose index moves monotonically across the exact resetting/nonresetting passages. The transition must be proved from the passage identities; global injectivity means it cannot rely on the discarded information actually disappearing.
