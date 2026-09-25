# Problem 1 run 263 — exact 16-step half-period skew structure

Problem 1 remains open. This continues run 262.

Run 262 reduced the remaining computational ingredient, under

[
x_0=1,qquad x_1=x_2,
]

to the exact identity

[
W=1oplus x_5(1oplus x_1).
]

This run finds a structural half-period reduction behind that 32-step identity.

## Exact 16-step lower-coordinate identities

Use the triangular Rule-30 recurrence

[
x_0'=x_0,qquad x_1'=x_1oplus x_0,qquad
x_j'=x_joplus(x_{j-1}lor x_{j-2})quad(jge2).
]

On the restricted Boolean cube (x_0=1, x_1=x_2), exact Boolean propagation for 16 steps gives

[
oxed{x_j(t+16)=x_j(t)quad(0le jle6)}
]

and

[
oxed{x_7(t+16)=x_7(t)oplus1}.
]

These are identities on all (2^7=128) restricted initial states, not sampled observations. They require no (b=1) assumption.

## Coordinate-8 skew recursion

Define

[
d_t=x_8(t+16)oplus x_8(t).
]

Comparing the coordinate-8 update at times (t) and (t+16), using the 16-periodicity of (x_6) and complementing of (x_7), gives

[
oxed{d_{t+1}=d_toplus1oplus x_6(t)}.
]

Thus the entire second half of the coordinate-8 orbit is determined by the first half plus one scalar skew bit.

For the forcing sequence

[
g_t=x_8(t)lor x_7(t),
]

Boolean expansion gives

[
oxed{
g_{t+16}oplus g_t
=
1oplus x_8(t)oplus d_t x_7(t).
}
]

Indeed, with (v=x_8(t),z=x_7(t),d=d_t),

[
(voplus d)lor(zoplus1)oplus(vlor z)
=1oplus voplus dz.
]

## Consequence for the run-262 target

The selector in (W) is

[
smod4in{0,1},qquad 0le s<30,
]

so it pairs exactly as (t) and (t+16) for

[
tin{0,1,4,5,8,9,12,13}.
]

Hence the remaining 32-step cancellation can be rewritten wholly as a 16-step problem. If

[
A_s=igoplus_{j<s}(1oplus x_8(j)),qquad
alpha_s=aoplus A_s,
]

and

[
c=igoplus_{j<16}x_8(j),
]

then (alpha_{t+16}=alpha_toplus c). Pairing
(F_s=(1oplusalpha_s)g_s) gives the exact identity

[
F_toplus F_{t+16}
=
c,g_t
oplus
(1oplusalpha_toplus c)
igl(1oplus x_8(t)oplus d_t x_7(t)igr).
]

Therefore

[
oxed{
W=
igoplus_{tin{0,1,4,5,8,9,12,13}}
left[
c,g_toplus
(1oplusalpha_toplus c)
(1oplus x_8(t)oplus d_t x_7(t))
ight].
}
]

This is an exact half-period reduction. The second 16-step orbit has disappeared; only the first-half lower orbit, (c), and the scalar process (d_t) remain.

## Current blocker / next target

The remaining analytic task is to telescope the eight displayed terms using

[
d_{t+1}oplus d_t=1oplus x_6(t)
]

and the 16-periodic lower orbit through coordinate 6, to obtain

[
W=1oplus x_5(1oplus x_1).
]

The useful new point is that this is now a 16-step identity rather than a generic 32-step Boolean cancellation. A next run should search for a two- or four-step primitive for the (d_t x_7(t)) contribution before expanding the full ANF.
