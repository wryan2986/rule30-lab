# Astra automation handoff — 2026-09-23 run 225

Problem 1 remains open.

## Repository state entering this run

`research/astra-next` was at `d3ad9ceced0aa5f9f735ad3b38a2b18f7aa3b1c3` (run 224). No intervening work was present.

Run 224 proved that the near-edge automaton orders `O_R` are powers of two and satisfy `O_R | O_{R+1}`.

## New all-depth result

The one-coordinate triangular extension has skew-product form

\[
T_{R+1}(x,z)=(T_Rx,z\oplus f(x)).
\]

After `O_R` iterations the base returns, leaving only one possible fiber toggle. Squaring removes that toggle. Therefore

\[
\boxed{O_{R+1}\mid 2O_R}.
\]

Combined with run 224,

\[
\boxed{O_{R+1}\in\{O_R,2O_R\}}.
\]

Hence for `m_R=v_2(O_R)`,

\[
\boxed{m_{R+1}-m_R\in\{0,1\}}.
\]

There is also an exact doubling criterion. If

\[
g(x)=\bigoplus_{j=0}^{O_R-1}f(T_R^j x),
\]

then the extension doubles iff `g(x)=1` for at least one base state. Thus determining the entire order hierarchy reduces to an orbit-parity/cocycle problem.

Full proof: `proofs/informal/problem1_run225_edge_order_extension_bound.md`.

## Finite reconnaissance

Exhaustive enumeration extends the order table to `R=17`:

`1,2,2,4,8,8,16,32,32,64,64,64,128,256,256,512,512,1024`.

This table is finite evidence only.

## Consequence for Problem 1

For the stopping sample

\[
F_n=E_{\Delta_n}(a_{n-1}),
\]

each extra unit of transient depth can add at most one bit to the required time modulus. This is a genuine restriction on how fast transient phase complexity can grow, but it is not yet enough: `m_R` could still grow linearly.

## Next target

Analyze the cocycle parity `g` rather than the full automaton. Seek a structural criterion for forced non-doubling/doubling, long non-doubling blocks, or a useful upper bound on `m_R`. In parallel compare `m_{Delta_n}` with the 2-adic information in stopping times `a_{n-1}`. Do not infer a closed formula from the finite order table.
