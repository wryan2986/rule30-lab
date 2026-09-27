# Problem 1 run 300: adjacent coboundary is phase-covariant

## Status

Problem 1 remains open. This continues run 299 on the restricted branch
[
x_0=1,qquad x_1=x_2=:p_t.
]

Run 299 found at phase zero, by exact exhaustive Boolean evaluation, that for the corrected moving-window summand
[
B_t=c_tg_t+eta_tu_t,
]
and
[
D_t:=B_t+B_{t+4}+B_{t+8}+B_{t+12},
]
one has
[
D_1+D_0=1+x_5(0)(1+p_0).
]

This run tests whether that collapse is an accident of the phase-zero normalization of the global scalar (a), or a transported identity of the orbit.

## Exact all-phase computation

Keep the run-262 scalar
[
a=igoplus_{s<32}P_s(1+x_8(s))
]
fixed from the original phase-zero state, and define
[
alpha_t=a+igoplus_{j<t}(1+x_8(j)).
]
Thus no reinitialization or recomputation of (a) is performed when (t) changes.

For each of all (2^7=128) initial states
[
(p,x_3,x_4,x_5,x_6,x_7,x_8),
]
I propagated the exact triangular Rule-30 recurrence, formed the moving windows
[
c_t=igoplus_{j=t}^{t+15}x_8(j),
]
the exact (d_t=x_8(t+16)+x_8(t)), then the corrected (B_t) and (D_t).

For every state and every phase (0le t<16), the identity holds:
[
oxed{D_{t+1}+D_t=1+x_5(t)(1+p_t).}
]

This is 2048 exact state/phase checks. In particular the run-299 cancellation is phase-covariant with the *same fixed global scalar (a)*; it is not a phase-zero artifact.

## Low-coordinate 8-step compatibility

The right-hand side itself has zero XOR over any eight consecutive phases:
[
oxed{igoplus_{j=0}^{7}left[1+x_5(t+j)(1+p_{t+j})ight]=0.}
]

There is a short low-coordinate explanation. Since
[
p_{t+1}=p_t+1,
]
the factor (1+p_{t+j}) selects one parity class of the eight phases. Exact lower recurrence gives
[
oxed{x_5(t)+x_5(t+2)+x_5(t+4)+x_5(t+6)=p_t,}
]
and, after shifting once,
[
oxed{x_5(t+1)+x_5(t+3)+x_5(t+5)+x_5(t+7)=1+p_t.}
]
Hence if (p_t=0), the selected even-phase XOR is zero; if (p_t=1), the selected odd-phase XOR is zero. The eight constant 1 terms also cancel.

Consequently the adjacent coboundary identity is compatible with
[
oxed{D_{t+8}=D_t.}
]
Computationally this 8-periodicity also holds on all 128 restricted states and all tested phases.

The two selector formulas above are stronger refinements of run 265's total parity
[
igoplus_{j=0}^{7}x_5(t+j)=1.
]

## Why this helps

The analytic target can now be treated as a genuine local cocycle law, not as a one-off equality at (t=0). This allows phase shifting freely while retaining the original (a).

A proof should therefore target
[
Delta D_t:=D_{t+1}+D_t
]
directly and may use the 8-periodic phase structure. There is no need to prove a closed form for either (D_0) or (D_1), whose common high-coordinate ANF is large.

The low-coordinate forcing term is itself an 8-periodic zero-sum cocycle. Thus any analytic derivation may equivalently seek an 8-periodic primitive (F_t) satisfying
[
F_{t+1}+F_t=1+x_5(t)(1+p_t),
]
and prove that (D_t+F_t) is phase-invariant. The remaining challenge is to identify that invariant structurally from the corrected quarter-pair algebra without expanding the common high-coordinate part.

## Blocker

This is still a finite Boolean certificate for the full (D)-identity, although it is materially stronger than run 299 because it establishes phase covariance and exposes the low-coordinate 8-step compatibility.

Next: derive (Delta D_t) from the repaired quarter-pair formula using the cocycles
[
c_{t+1}+c_t=d_t,quad c_{t+8}+c_t=x_3(t),
]
[
d_{t+1}+d_t=1+x_6(t),quad d_{t+8}+d_t=p_t,
]
and the 8-shift (e,f) recurrences. Do not expand (D_t)'s common high-coordinate ANF.
