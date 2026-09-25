# Problem 1 run 270: analytic even/odd selector split

## Status

Problem 1 remains open. This continues runs 267--269 on the restricted branch
[
x_0=1,qquad x_1=x_2=:p.
]

Define the run-267 boundary residual at arbitrary phase
[
R_t=(p_toplus x_4(t))(1oplus x_5(t)),
qquad p_t=x_1(t)=x_2(t).
]

## New two-step selector law

Put
[
E_t:=R_toplus R_{t+2}.
]
Writing at phase (t)
[
p=x_1=x_2,quad a=x_3,quad b=x_4,quad c=x_5,
]
exact Boolean simplification gives
[
E=1oplus aoplus paoplus pboplus coplus pcoplus ac.
]

Transport four steps using the already proved lower map
[
p_{t+4}=p_t,quad a_{t+4}=a_t,quad
b_{t+4}=b_toplus1,quad
c_{t+4}=c_toplus p_t(1oplus a_t).
]
The (b)-complement changes (E) by (p).  The change caused by (c) is
[
p(1oplus a)(1oplus poplus a)=0,
]
so
[
oxed{E_{t+4}=E_toplus p_t}.
]
Hence
[
oxed{R_toplus R_{t+2}oplus R_{t+4}oplus R_{t+6}=p_t}.
]
Since (p_{t+1}=p_toplus1), shifting by one gives
[
oxed{R_{t+1}oplus R_{t+3}oplus R_{t+5}oplus R_{t+7}=1oplus p_t}.
]
XORing the two identities recovers the already observed full-period parity
[
igoplus_{j=0}^{7}R_{t+j}=1.
]

## Verification

Independent direct Rule-30 propagation over all 16 low-coordinate initial states
((p,x_3,x_4,x_5)) verifies the even selector equals (p) and the odd selector equals (1oplus p).

## Consequence

The target coefficient (1oplus p) in
[
W=1oplus x_5(1oplus p)
]
is itself the odd-phase parity of the residual (R).  Together with the previous selector
[
R_toplus R_{t+1}oplus R_{t+4}oplus R_{t+5}=x_3(t),
]
the remaining quarter-pair boundary terms should be reconstructed as combinations of these selector masks before any high-coordinate ANF expansion.

The current blocker is bookkeeping: recover the non-(e_tq_t) terms of the quarter-pair functional in selector-preserving form and test whether their sum cancels the (x_3) contribution and leaves the target boundary (1oplus x_5(1oplus p)).
