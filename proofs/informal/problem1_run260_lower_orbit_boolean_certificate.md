# Problem 1 run 260 — exact lower-orbit Boolean certificate

## Status

Problem 1 remains open. This run continues the run-257/259 reduction of the triple-64 parity transport step.

For the closed lower orbit through coordinate 8, write

[
g_s=x_8(s)lor x_7(s),qquad
P_s=igoplus_{j<s}g_j,qquad
b=igoplus_{s<32}g_s.
]

Run 259 reduced the dynamically realized coordinate-10 skew to

[
a=igoplus_{s<32}P_s(1oplus x_8(s)),
]

using the exact identity (igoplus_{s<32}x_8(s)=0).

Let

[
A_s=igoplus_{j<s}(1oplus x_8(j)),
]

and define the run-257 lower-orbit target

[
W=
igoplus_{substack{0le s<30\smod4in{0,1}}}
(1oplus aoplus A_s)g_s.
]

The desired statement is (b=1Rightarrow W=1).

## New exact finite certificate

I enumerated all (2^9=512) initial prefixes ((x_0,ldots,x_8)), evolved the triangular Rule-30 recurrence for 32 steps, and independently converted the truth tables for (b) and (W) to algebraic normal form.

All 512 lower prefixes close after 32 steps. There are exactly 64 states with (b=1), and every one has (W=1).

More strongly, the Boolean function

[
R=b(1oplus W)
]

has identically zero ANF: its Möbius transform contains no monomials. Thus

[
oxed{b(1oplus W)equiv0}
]

as a Boolean polynomial in the nine initial lower-prefix bits. This is an exact complete-state certificate, not a sample.

The forcing skew itself has a notably small ANF:

[
oxed{
b=x_0igl(
1oplus x_1oplus x_2oplus x_1x_2x_3
oplus x_1x_2x_4oplus x_1x_2x_3x_4
oplus x_5oplus x_1x_5oplus x_2x_5
igr).
}
]

In particular the (b=1) branch forces (x_0=1), and (b) is independent of the initial (x_6,x_7,x_8) bits despite being defined from the 32-step (x_8lor x_7) forcing sequence.

## Interpretation

This closes the remaining run-257 parity implication at the finite Boolean-algebra level. Combined with runs 255–259, it supplies a complete finite certificate for the observed (E_{11}(64)=0) transport on the (b=1) branch.

It is not yet the desired structural proof: the certificate depends on exhaustive/symbolic reduction over the nine-bit lower prefix. The striking next target is the compact nine-term formula for (b). Derive that formula analytically from shorter-prefix recurrences, then reduce (W) modulo the relation (b=1) without enumerating all 512 states. The independence of (b) from (x_6,x_7,x_8) is likely the useful cancellation to exploit.

## Dead end avoided

Do not assume (W=b) globally. The census is:
- (b=1,W=1): 64 states;
- (b=0,W=0): 384 states;
- (b=0,W=1): 64 states.

Only the implication (b=1Rightarrow W=1) is universal.
