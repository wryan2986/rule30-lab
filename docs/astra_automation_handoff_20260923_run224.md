# Astra automation handoff — 2026-09-23 run 224

Problem 1 remains open.

## Repository state entering this run

`research/astra-next` was at `53afd72ea75b6900ec37e9e23c02959e35424dbf` (run 223). No intervening work was present.

Run 223 proved that the fixed-depth near-edge vectors

\[
(E_0,\dots,E_R),\qquad E_r(k)=d_{2k-r}(k),
\]

evolve by an invertible triangular Boolean map and that the stopping frontier is

\[
F_n=E_{\Delta_n}(a_{n-1}),
\qquad
\Delta_n=2a_{n-1}-(n+1).
\]

## New all-depth result

Every width-\(R\) near-edge automaton belongs to the finite group of triangular Boolean permutations

\[
y_r=x_r\oplus f_r(x_0,\dots,x_{r-1}).
\]

That group has power-of-two cardinality. Hence it is a finite 2-group, so the order of every edge automaton and every state-orbit period is a power of two.

Writing

\[
O_R=\operatorname{ord}(T_R),
\]

projection from width \(R+1\) to width \(R\) commutes with the dynamics, giving the exact divisibility hierarchy

\[
\boxed{O_R\mid O_{R+1}}.
\]

Thus the finite edge bands form a nested **2-adic period hierarchy**, not merely arbitrary periodic systems.

Full proof: `proofs/informal/problem1_run224_edge_automata_2group_period_hierarchy.md`.

## Exhaustive finite reconnaissance

Enumeration of all states through width 16 gave automaton orders

`1, 2, 2, 4, 8, 8, 16, 32, 32, 64, 64, 64, 128, 256, 256, 512`.

The power-of-two property is proved for all widths; this exact order sequence and any prospective closed formula remain computational evidence only.

## Sharpened obstruction

Since

\[
F_n=E_{\Delta_n}(a_{n-1}),
\]

the unresolved transient state can now be viewed as a moving sample from a nested 2-adic tower. For fixed depth \(R\), its time phase depends only on time modulo the power-of-two order \(O_R\). The unresolved question is therefore whether the common-origin stopping relation constrains

\[
a_{n-1}\pmod{O_{\Delta_n}}
\]

as \(\Delta_n\) grows.

## Next target

Study the order exponent

\[
m_R=v_2(O_R)
\]

and seek structural upper/lower recurrences under one-coordinate extension. In parallel, reproduce the `x=1` long constant-period epoch while recording `a`, `Delta`, `F`, and, where feasible, `a mod O_Delta`. A restricted stopping-phase pattern would be genuinely new information; arbitrary-looking residues would be evidence against this route but not a proof.

Do not infer a closed formula for `O_R` from the width-16 table without proof.
