# Finite support escapes moving-fringe recurrence only at unbounded depth

Status: `proved`. Structural bridge/stopping-fence result; not a proof of Problem 1.

## Statement

Let a nonzero finite Rule-30 row at time 0 have leftmost and rightmost 1s at `L` and `R`. Use the moving-right-edge coordinates

    a_j(t) = x_{R+t-j}(t),   j >= 0.

Let

    D(t) = max { j : a_j(t)=1 }.

Then for every `t>=0`,

    D(t) = (R-L) + 2t.                              (1)

Moreover, if `M=D(t)`, then the two newly exposed deepest coordinates at the next step satisfy

    a_{M+1}(t+1)=a_{M+2}(t+1)=1.                    (2)

Thus an actual finite-support moving-fringe orbit never returns globally, even though every fixed finite prefix has the previously proved pro-2 recurrence. All failure of global return can be pushed beyond every fixed observation depth.

## Proof

The moving-fringe update already established in the preceding notes is

    a_j(t+1) = a_j(t) XOR (a_{j-1}(t) OR a_{j-2}(t)),

with negative-index coordinates zero.

Suppose `M=D(t)`. Finite support gives `a_j(t)=0` for `j>M` and `a_M(t)=1`. Hence

    a_{M+2}(t+1)
      = 0 XOR (a_{M+1}(t) OR a_M(t))
      = 1,

and

    a_{M+1}(t+1)
      = 0 XOR (a_M(t) OR a_{M-1}(t))
      = 1.

For `j>M+2`, all three inputs `a_j,a_{j-1},a_{j-2}` vanish, so the output is zero. Therefore

    D(t+1)=D(t)+2.

Since `D(0)=R-L`, induction gives (1), and the displayed calculation gives (2).

Equivalently in laboratory coordinates, the leftmost 1 moves from `L-t` to `L-t-1` at every step (Rule 30 sends neighborhood `001` to 1), while the maximal right ray is `R+t`; their separation therefore grows by exactly two per step.

## Relation to the pro-2 recurrence no-go

The recent no-go theorem says that no **continuous** real-valued function of the instantaneous infinite moving fringe can be a globally nonincreasing consumable resource. The present result identifies exactly how finite-support physical rows evade literal recurrence: `D` is an unbounded-depth observable and is discontinuous in the product topology. A sequence of finite-support fringes may agree on arbitrarily long prefixes while having support endpoints arbitrarily far away.

So the pro-2 recurrence is not a claim that the complete finite-support configuration eventually repeats. It says only that every bounded-depth observation returns along synchronized dyadic times. The information certifying nonreturn is forced outward to ever larger moving-coordinate depth.

There is also an exact anchored quantity

    D(t)-2t = R-L,                                   (3)

which remembers the original support width. This is a genuine finite-support invariant, but it is conserved rather than consumed. Therefore it cannot by itself bound the number of regenerative births required by FULL.

## Consequence for the birth-budget program

This gives a sharper admission test for a proposed survivor-specific resource. If it is supposed to evade the continuous-fringe no-go by using finite support, it must genuinely exploit information at depths growing with time (or equivalent left-boundary/core/history information). Merely taking a very large but fixed right-fringe window still falls under the pro-2 stopping fence.

Conversely, `D(t)` shows that discontinuous/unbounded-depth information is available, but the obvious such quantity has deterministic drift `+2` independent of births. To obtain a finite birth budget one needs a second quantity coupling a birth/source event to this escaping depth, original left-boundary data, or core/global-shadow history. Counting support width alone supplies no depletion.

A useful next target is therefore a source-indexed depth/characteristic invariant: determine whether each forced cyclic birth can be charged to a strictly ordered characteristic reaching the expanding left boundary, rather than to a fixed moving-right-fringe prefix. Any such charge must prove bounded reuse; locality alone does not do so.

Problem 1 remains OPEN.
