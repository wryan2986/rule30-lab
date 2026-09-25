# Problem 1 run 267: selected nonlinear residual collapses

## Status

Problem 1 remains open. This continues run 265. The branch entered at `f63174a7ecccc34ba01eb474dba9cebedf24c708`; no intervening pushed research was present.

Work throughout on the restricted branch
[
x_0=1,qquad x_1=x_2=:p.
]

Run 265 defined the 8-shift skew
[
e_t=x_7(t+8)oplus x_7(t)
]
and proved
[
e_{t+1}=e_toplus1oplus x_5(t).
]

For the 4-shift of coordinate 6 put
[
q_t=x_6(t+4)oplus x_6(t).
]
Exact lower-orbit propagation gives (x_6(t+8)=x_6(t)oplus1), hence
[
q_{t+4}=q_toplus1.
]

## New collapse

The nonlinear obstruction singled out in run 265 does not need a generic primitive. For the four phases selected by the quarter-pair functional,
[
S:=e_0q_0oplus e_1q_1oplus e_4q_4oplus e_5q_5,
]
exact Boolean simplification gives
[
oxed{S=poplus x_4oplus px_5oplus x_4x_5
=(poplus x_4)(1oplus x_5).}
]

All dependence on (x_3,x_6,x_7,x_8) cancels.

The cancellation is already visible after pairing phases four apart:
[
e_0q_0oplus e_4q_4
=x_3oplus x_6oplus px_4oplus px_5
 oplus x_3x_5oplus px_3x_4,
]
[
e_1q_1oplus e_5q_5
=poplus x_3oplus x_4oplus x_6oplus px_4
 oplus x_3x_5oplus x_4x_5oplus px_3x_4.
]
Their common six-term core cancels, leaving the boxed degree-2 boundary factor.

## Compact algebra behind the pairing

Let
[
r_t=e_{t+4}oplus e_t.
]
Since (q_{t+4}=q_toplus1),
[
e_tq_toplus e_{t+4}q_{t+4}
=e_toplus r_tq_toplus r_t.
]
For the two needed phases,
[
r_0=1oplus x_4oplus px_3,qquad
r_1=1oplus poplus x_4,
]
and
[
e_0oplus e_1=1oplus x_5.
]
A direct four-step calculation gives
[
q_0=poplus x_3oplus x_4oplus x_5oplus px_3oplus px_5,
]
while (q_1) follows from the one-step 4-shift cocycle. Substitution reduces to
[
S=(poplus x_4)(1oplus x_5).
]
This is a much smaller analytic target than expanding either 8-shift skew.

## Verification

Independently evaluated the triangular Rule-30 recurrence on all (2^7=128) assignments of the free variables (p,x_3,ldots,x_8). The truth table of (S) has Möbius/ANF support exactly
[
{p,x_4,px_5,x_4x_5}.
]

## Next target

Insert the factored residual into the run-264/265 quarter-pair expression before expanding any coordinate-8 skew. The remaining boundary terms should be combined with
[
(poplus x_4)(1oplus x_5)
]
and tested for direct cancellation to the run-262 target
[
W=1oplus x_5(1oplus p).
]

Do not search for a primitive for generic (e_tq_t); the selected four-phase sum is substantially simpler than its summands.
