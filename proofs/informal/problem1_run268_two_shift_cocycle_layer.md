# Problem 1 run 268: exact two-shift cocycle layer

## Status

Problem 1 remains open. This continues run 267. The branch entered at `53b9598e56ec34476e5d4def5f33fd180dab63b2`; no intervening pushed work was present.

Work on the restricted branch
[
x_0=1,qquad x_1=x_2=:p.
]

Runs 263--267 exposed complement/fixed-point structure at shifts 16, 8, and 4. The same hierarchy continues one level lower.

## Exact two-shift structure

For every phase (t),
[
oxed{x_j(t+2)=x_j(t)quad(0le jle2),}
]
and
[
oxed{x_3(t+2)=x_3(t)oplus1.}
]

This follows directly from two applications of the triangular Rule-30 recurrence; it was also exhaustively checked on all 128 restricted initial states.

Thus the observed hierarchy is now
[
2: x_3mapsto x_3oplus1,qquad
4: x_4mapsto x_4oplus1,qquad
8: x_6mapsto x_6oplus1,qquad
16: x_7mapsto x_7oplus1.
]

## Coordinate-4 two-shift skew

Define
[
k_t=x_4(t+2)oplus x_4(t).
]
Comparing the coordinate-4 update at (t) and (t+2), using (x_2(t+2)=x_2(t)) and (x_3(t+2)=x_3(t)oplus1), gives
[
oxed{k_{t+1}=k_toplus1oplus x_2(t).}
]
At phase zero this skew is especially small:
[
oxed{k_0=1oplus poplus x_3.}
]
Since (x_4(t+4)=x_4(t)oplus1), one also has (k_{t+2}oplus k_t=1).

## Coordinate-5 two-shift skew

Define
[
ell_t=x_5(t+2)oplus x_5(t).
]
The same OR-difference identity used in the higher-shift arguments gives
[
oxed{ell_{t+1}=ell_toplus1oplus x_4(t)oplus k_t x_3(t).}
]
At phase zero,
[
oxed{ell_0=poplus px_3oplus px_4
      =p(1oplus x_3oplus x_4).}
]

The run-266 four-shift skew (h_t=x_5(t+4)oplus x_5(t)) is therefore
[
h_t=ell_toplusell_{t+2},
]
so its previously observed collapse (h_0=p(1oplus x_3)) is the next telescoped level of this two-step cocycle.

## Verification

All displayed shift and cocycle identities were independently checked for all (2^7=128) assignments of ((p,x_3,ldots,x_8)) and phases through a full 16-step lower period. The ANF supports at phase zero are exactly
[
k_0:{1,p,x_3},qquad
ell_0:{p,px_3,px_4}.
]

## Consequence / next target

The residual from run 267,
[
(poplus x_4)(1oplus x_5),
]
should now be paired at separation two before any coordinate-7 or coordinate-8 expansion. The new (k_t,ell_t) recurrences give exact two-step differences of both (x_4) and (x_5), so this boundary factor can be transported using only low-coordinate cocycles.

This is preferable to expanding the remaining quarter-pair boundary terms: the period-doubling hierarchy now reaches shift two and supplies a candidate telescoping mechanism for the last (x_4,x_5) dependence.
