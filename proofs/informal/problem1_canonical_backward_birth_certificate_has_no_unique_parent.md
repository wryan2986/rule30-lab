# Canonical backward certificates for forced births: local uniqueness fails

Status: `structural-no-go`. Problem 1 remains OPEN.

## 1. Target

Run118 left the concrete target of tracing the forced beta=1 birth from the established two-bit nonreset passage backward toward time zero, hoping successive births might admit strictly ordered ancestral intercepts with bounded reuse.

Before attempting a global ordering, one needs a canonical local predecessor rule for a Rule-30 output 1. This note checks that admission condition exactly.

## 2. Rule-30 predecessor ambiguity

Write the local rule as

    f(l,c,r) = l XOR (c OR r).

For an output cell equal to 1, its predecessor triples are exactly

    001, 010, 011, 100.

Thus a 1 has no intrinsically distinguished parent. In particular:

* in 001 the only predecessor 1 is the right parent;
* in 010 the only predecessor 1 is the center parent;
* in 100 the only predecessor 1 is the left parent;
* in 011 there are two predecessor 1s, center and right.

Consequently no direction (left, center, or right) is guaranteed even to contain a 1 whenever the child is 1.

The same obstruction remains if one defines a certificate by Boolean sensitivity rather than by ancestry of 1s. The left input is always sensitive because f is XOR in l. The center and right inputs are sensitive conditionally. Choosing the always-sensitive left input gives a formally canonical dependency path, but after t backward steps it simply reaches the deterministic light-cone boundary x-t. It therefore cannot distinguish births at a common moving offset except by their spacetime coordinates; it does not certify consumption of distinct original support cells.

## 3. Consequence for the run118 characteristic proposal

The proposed map

    forced birth -> canonical backward 1-ancestor -> time-zero intercept

is not available from the Rule-30 local rule alone. Any useful certificate must carry additional phase/context selecting among the predecessor alternatives, or use a larger object than a single ancestral path (for example a minimal dependency set, a source-labelled path, or crossing data relative to the complete core/global shadow).

This is not yet a proof that all characteristic charging schemes fail. It rules out the simplest one-parent ancestry budget before spending effort on a false uniqueness premise.

## 4. Sharper next target

The established two-bit nonreset passage gives more information than the fact that the eventual birth cell equals 1: beta=1 is forced because the relevant return zero-pair flag vanishes, independently of the wider shadow. The next useful certificate should therefore be attached to that *forcing event*, not to an arbitrary physical 1-cell.

A concrete next test is to expand the exact dependency cone of the zero-pair flag responsible for beta at t+6 back through the known centers 0,0,1 and right pair 10. Determine whether the forcing reduces to a boundary/intercept condition on a bounded set of time-t shadow cells. If it does, then ask whether repeated forced births require strictly ordered such forcing sets. If the forcing set can be reused unchanged, record that as the next no-go.

Dependencies: `problem1_nonreset_return_birth_spacing.md`; `problem1_left_edge_prefix_cycles_are_dyadic.md`; `problem1_finite_support_escapes_fringe_recurrence_at_depth.md`.
