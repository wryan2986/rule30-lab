# Problem 1 run 224 — near-edge automata form a 2-group period hierarchy

## Status

Problem 1 remains open. This note continues run 223's exact near-edge automaton analysis.

## Setup

Run 223 defined

\[
E_r(k)=d_{2k-r}(k)
\]

and proved that every fixed-width vector \((E_0,\dots,E_R)\) evolves autonomously by

\[
E'_0=E_0,
\qquad
E'_1=E_1\oplus E_0,
\]

and, for \(r\ge2\),

\[
E'_r=E_r\oplus(E_{r-1}\lor E_{r-2}).
\]

Call the width-\(R\) map \(T_R\).

Run 223 proved directly that \(T_R\) is invertible. Here we strengthen that observation into an exact period theorem and a nested divisibility hierarchy.

## Theorem 1: every finite-width edge orbit has power-of-two period

For every \(R\ge0\), the permutation \(T_R\) has order a power of two. Consequently every orbit of every width-\(R\) near-edge state has period a power of two.

### Proof

Consider the set \(G_R\) of triangular Boolean permutations of \(\{0,1\}^{R+1}\) of the form

\[
y_0=x_0\oplus c_0,
\]

and, for \(1\le r\le R\),

\[
y_r=x_r\oplus f_r(x_0,\dots,x_{r-1}),
\]

where \(c_0\in\{0,1\}\) and each \(f_r\) is an arbitrary Boolean function of the preceding coordinates.

These maps form a finite group under composition: triangularity is preserved by composition, and the coordinates can be inverted successively from low to high, giving an inverse of the same triangular form.

The number of choices is

\[
|G_R|=2\prod_{r=1}^{R}2^{2^r},
\]

which is a power of two. Hence \(G_R\) is a finite 2-group. By Lagrange's theorem, every element of \(G_R\) has order a power of two.

The run-223 map \(T_R\) belongs to \(G_R\): its zeroth coordinate is fixed, and every higher coordinate is the old coordinate XOR a Boolean function of lower coordinates only. Therefore

\[
\operatorname{ord}(T_R)=2^{m_R}
\]

for some integer \(m_R\ge0\). Every state-orbit period divides this order, so every orbit period is itself a power of two. QED.

### Slightly smaller group

Our actual maps fix coordinate zero rather than translating it, so they lie in the index-two subgroup with \(c_0=0\). The 2-group conclusion is unchanged.

## Theorem 2: the automaton orders form a divisibility tower

Let

\[
O_R=\operatorname{ord}(T_R).
\]

Then

\[
\boxed{O_R\mid O_{R+1}.}
\]

Since both are powers of two, the exponent \(m_R\) in \(O_R=2^{m_R}\) is nondecreasing with depth.

### Proof

Projection onto the first \(R+1\) coordinates commutes with the dynamics:

\[
\pi_R\circ T_{R+1}=T_R\circ\pi_R,
\]

because the update of coordinate \(r\) depends only on coordinates at indices at most \(r\).

If \(T_{R+1}^{O_{R+1}}\) is the identity, projecting gives

\[
T_R^{O_{R+1}}=\mathrm{id}.
\]

Therefore the order \(O_R\) divides \(O_{R+1}\). QED.

## Corollary: all fixed-depth diagonal periods are 2-adic

For every fixed depth \(r\), the scalar sequence

\[
k\mapsto E_r(k)
\]

is periodic after that diagonal has been born, and its period is a power of two. More generally, every finite collection \((E_0,\dots,E_R)\) has a joint power-of-two period dividing \(O_R\).

Thus the transient cone is not merely a nested family of arbitrary finite periodic systems: it is a nested **2-adic period hierarchy**.

## Exact relevance to the stopping frontier

Run 223 rewrote the unresolved look-ahead bit as

\[
F_n=E_{\Delta_n}(a_{n-1}),
\qquad
\Delta_n=2a_{n-1}-(n+1),
\]

when \(\Delta_n\ge0\), and proved

\[
\Delta_{n+1}-\Delta_n=2\delta_n-1.
\]

The present theorem says that, conditional on a fixed sampled depth \(R\), the time dependence of the sampled edge state is controlled entirely by time modulo a power of two. Therefore the moving-frontier obstruction can be reformulated as interaction between two quantities:

1. the growing depth \(\Delta_n\), which selects a deeper member of the nested 2-group tower;
2. the stopping time \(a_{n-1}\), whose residue modulo the corresponding power-of-two order selects the phase.

This is stronger than run 223's generic finite-periodicity statement because no odd period factors can occur in any finite edge band.

## Computational reconnaissance

An exhaustive enumeration of all states for widths \(w=R+1\le16\) gives the following permutation orders:

| width \(w\) | order of \(T_{w-1}\) |
|---:|---:|
| 1 | 1 |
| 2 | 2 |
| 3 | 2 |
| 4 | 4 |
| 5 | 8 |
| 6 | 8 |
| 7 | 16 |
| 8 | 32 |
| 9 | 32 |
| 10 | 64 |
| 11 | 64 |
| 12 | 64 |
| 13 | 128 |
| 14 | 256 |
| 15 | 256 |
| 16 | 512 |

For every tested width, all observed cycle lengths were powers of two, as now proved abstractly. The exact order sequence above is computational evidence only; no closed formula for \(O_R\) is claimed.

## What this does and does not solve

This result gives the precise algebraic structure suggested at the end of run 223: finite near-edge automata form a nested power-of-two period hierarchy.

It does **not** bound \(\Delta_n\), and therefore does not yet reduce the stopping sequence to one fixed finite automaton. As \(\Delta_n\) grows, the required modulus \(O_{\Delta_n}\) may also grow. The remaining issue is whether the common-origin stopping relation constrains

\[
a_{n-1}\pmod{O_{\Delta_n}}
\]

strongly enough to control

\[
F_n=E_{\Delta_n}(a_{n-1}).
\]

## Next target

The most concrete continuation is to derive structural bounds or a recurrence for the order exponent

\[
m_R=v_2(O_R),
\]

and then combine that with

\[
\Delta_n=2a_{n-1}-(n+1).
\]

In parallel, reproduce the `x=1` tower diagnostics with \((a_{n-1},\Delta_n,F_n)\) and record the residue

\[
a_{n-1}\bmod O_{\Delta_n}
\]

whenever \(O_{\Delta_n}\) is computationally accessible. The aim is to determine whether the stopping curve follows a restricted 2-adic phase class rather than an arbitrary phase of the deeper edge automata.
