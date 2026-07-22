# Excluding eventual center period one

Status: rigorous partial theorem, conditional on Kopra's published width-two
nonperiodicity theorem. This excludes eventual period one for the center of
every allowed finite seed; it does not exclude periods two or greater and does
not solve Problem 1.

## External theorem used

Kopra's Corollary 3.7 states that if a binary elementary cellular automaton is
left permutive and left spreading and the initial configuration belongs to
\(\mathcal L_0(\Sigma_2)\), then every adjacent width-two trace is not
eventually periodic.

Rule 30 is left permutive because

\[
f(a,b,c)=a\mathbin\oplus(b\lor c)
\]

is bijective in \(a\). It is left spreading in Kopra's convention because
\(f(0,0,1)=1\). Every nonzero finite-support configuration belongs to
\(\mathcal L_0(\Sigma_2)\). Therefore the theorem applies to every adjacent
pair for the single-cell seed and, more generally, for every finite seed in
the whole-tail reformulation.

The source and convention audit is in `docs/theory_literature_review.md`.

## Eventually one

Suppose that \(x_0(t)=1\) for every \(t\geq T\). At the center,

\[
1=x_0(t+1)
=x_{-1}(t)\mathbin\oplus\bigl(x_0(t)\lor x_1(t)\bigr)
=x_{-1}(t)\mathbin\oplus1.
\]

Hence \(x_{-1}(t)=0\) for all \(t\geq T\). The adjacent trace on
\([-1,0]\) is eventually the constant pair \((0,1)\), contradicting the
width-two theorem.

## Eventually zero

Suppose instead that \(x_0(t)=0\) for every \(t\geq T\). Apply Rule 30 at
the cell immediately to the right:

\[
x_1(t+1)
=x_0(t)\mathbin\oplus\bigl(x_1(t)\lor x_2(t)\bigr)
=x_1(t)\lor x_2(t)
\qquad(t\geq T).
\]

Thus the binary sequence \(x_1(t)\) is nondecreasing from time \(T\): once
it becomes one it remains one. It is therefore eventually constant. More
explicitly, either it never becomes one and stays zero, or it has a first one
and stays one thereafter.

The adjacent trace on \([0,1]\) is consequently eventually either \((0,0)\)
or \((0,1)\). Both are eventually periodic, again contradicting the
width-two theorem.

## Theorem

> For Rule 30 started from any nonzero finite-support configuration, no fixed
> temporal column can be eventually constant.

The proof above was written for position zero. Translating the coordinate
names gives the same argument at any fixed position, while Kopra's theorem
covers every adjacent interval.

In particular, the center sequence of the single-cell seed cannot have
eventual period one. In the stronger whole-tail formulation, no positive odd
finite right-edge seed can have an eventually constant growing diagonal.

## Scope

This deduction does not generalize automatically to a period-\(p\) center
with \(p\geq2\). For a zero center tail the right-neighbor update becomes a
monotone OR recurrence; a nonconstant periodic center reintroduces the XOR
term and destroys that monotonicity. A new invariant or phase argument is
still required for every period above one.
