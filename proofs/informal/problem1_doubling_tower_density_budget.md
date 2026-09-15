# Problem 1: doubling towers carry linear temporal density

Status: `partial-proof` for the finite-cycle statement below; global transport to one actual survivor remains `inconclusive`.

## Setup

Use the genuine one-bit doubling certificate from runs 45--46. If a parent finite cycle has exact period `p` and its one-bit lift has exact period `2p`, the introduced fiber bit `b` satisfies

    b(t+p) = 1 xor b(t)

for every phase `t`. Hence `b` has exactly `p` ones and `p` zeros in each full `2p` period.

For a nested tower of `r` genuine doublings

    p, 2p, 4p, ..., 2^r p,

let `b_j` be the coordinate introduced at the `j`th doubling. Run 46 proved `per(b_j)=2^j p` and linear independence of the resulting temporal columns.

## Stronger density consequence

View every `b_j` on the final common temporal period

    L = 2^r p.

Its antiperiodic block of length `2^j p` repeats exactly `2^(r-j)` times in this common period. Every block has half of its entries equal to one. Therefore

    sum_(t=0..L-1) b_j(t) = L/2

for every `j=1,...,r`. Summing over the introduced coordinates gives

    sum_(t=0..L-1) sum_(j=1..r) b_j(t) = r L / 2.       (1)

Equivalently, the average Hamming occupancy of just these `r` coordinates is exactly

    (1/L) sum_t sum_j b_j(t) = r/2.                    (2)

Thus a common spacetime object containing `r` complete doubling-fiber histories already has a linear activity budget. Temporal rank is a useful non-reuse certificate, but once complete histories coexist, rank-to-occupancy conversion is unnecessary: antiperiodicity itself gives density `1/2` in each witness column.

A weaker finite-window version is immediate. In any interval of `W` consecutive times, an antiperiodic periodic column of period `2q` has at least

    floor(W/(2q)) q

ones, because each complete `2q` block contributes exactly `q`. Hence several witnesses can still give a quantitative occupancy lower bound if a transport theorem preserves sufficiently many complete periods of each history.

## Audit against the existing joint-window machinery

The reviewed joint-window theorem (`problem1_activity_joint_window_target.md`) transports/counts scalar boundary-pair occurrences

    P_n(t) = bit_(2n)(A^t x) OR bit_(2n+1)(A^t x)

through the quantities `C_n(a,W)` and `J_n=C_n(0,n)`. Its proof is an event-assignment/counting inequality. It does not state that a whole temporal coordinate history of a later forced finite state is reproduced in the original common-origin realization, nor that a two-time relation such as

    b(t+q)=1 xor b(t)

is preserved under the gate/source pullback. The adversarial review explicitly leaves the actual-survivor mechanism open and warns that the corrected gate bridge shifts ray depth downward and gives no depth-zero pullback.

Therefore (1)--(2) cannot currently be inserted into the joint-window inequality. This is the precise missing bridge.

## Consequence for the research route

The highest-value transport target can now be stronger and simpler than a generic rank-preservation theorem:

> Given `r` genuine doubling passages on one FULL common-origin realization, transport complete periods (or a uniformly positive fraction of complete periods) of the associated antiperiodic fiber histories into one spacetime window of the original realization, with their coordinate contributions remaining distinguishable.

If such a theorem preserves `r` complete histories over a common interval, (2) gives average occupancy `r/2` before any harmonic amplification. If it preserves `m_j` complete periods of witness `j`, the finite-window bound above gives an explicit additive lower bound.

This would be enough to contradict bounded activity as `r -> infinity`, provided the transported coordinate occupancies are legitimate summands of the existing `V_s` activity or can be charged to them with bounded multiplicity.

## Dead end to avoid

Do not spend another run trying to prove a separate abstract inequality `rank r => large occupancy` for arbitrary binary temporal matrices. Such an inequality is too weak in general and is unnecessary for these witnesses. Their antiperiodicity already supplies exact half-density. The unresolved issue is common-origin transport of the histories, not conversion of rank to mass.
