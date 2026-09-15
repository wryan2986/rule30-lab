# Astra automation handoff — 2026-09-15 run 47

Problem 1 remains open.

## Repository state

No intervening work was present after run 46 (`58a6764c1757e9b5afc6524ff774ae1c90d6ba55`).

## New progress

Added `proofs/informal/problem1_doubling_tower_density_budget.md`.

Run 46's temporal-rank invariant can be strengthened to an exact density statement. For a genuine doubling fiber,

    b(t+p)=1 xor b(t),

so the new coordinate has exactly half ones over every full period. For a tower of `r` genuine doublings, place all introduced columns on the final common period `L=2^r p`. Every witness contributes exactly `L/2` ones, hence

    sum_t sum_(j=1..r) b_j(t) = rL/2.

Thus their average Hamming occupancy is exactly `r/2`. If complete histories can be transported into one common spacetime object, no separate rank-to-activity theorem is needed: antiperiodicity already gives linear density in the number of doublings.

A finite-window form was also recorded: a period-`2q` antiperiodic column contributes at least `floor(W/(2q))*q` ones to any `W` consecutive times.

## Audit of existing joint-window machinery

The reviewed joint-window result transports/counts scalar boundary-pair events through `C_n(a,W)` / `J_n`; it does not preserve complete temporal coordinate histories or the two-time complement relation. Its own adversarial review leaves the actual-survivor mechanism open and notes the corrected gate bridge has a downward depth shift/no depth-zero pullback.

Therefore the exact blocker is now common-origin transport of antiperiodic histories, not rank-to-mass conversion.

## Highest-value next step

Inspect the exact gate/source/return bridge and common-origin scan formulas for whether a genuine doubling's fiber history can be represented directly as a sequence of original-realization boundary/gate bits over one parent period. Seek a bounded-multiplicity charging map from those `p` forced complement events to legitimate `V_s` summands in the original realization. If this cannot hold, construct the smallest explicit local obstruction and record it.
