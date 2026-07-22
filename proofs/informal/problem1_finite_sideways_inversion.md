# Finite sideways inversion for Rule 30

Status: informal rigorous finite lemma; not a proof of Problem 1

## Definitions

Let

\[
f(a,b,c)=a\oplus(b\lor c)
\]

be the Rule 30 local map. Fix a nonnegative horizon \(H\). A center trace is
the \(H+1\)-tuple

\[
C=(c_0,c_1,\ldots,c_H).
\]

Fix the initial right half to zero: \(x_j(0)=0\) for \(1\le j\le H\).
Only these cells can affect the center by time \(H\), so cells farther right
can also be fixed to zero without changing this finite question.

## Lemma 1: local left inversion

For bits \(a,b,c,n\), if

\[
n=f(a,b,c)=a\oplus(b\lor c),
\]

then

\[
a=n\oplus(b\lor c).
\]

Proof: xor both sides with \(b\lor c\) and use
\(q\oplus q=0\) and \(a\oplus0=a\). Thus, for fixed center and right bits,
the Rule 30 map is bijective in the left bit. ∎

## Lemma 2: the finite right triangle is unique

Given \(C\) and the zero initial right half, every cell \(x_j(t)\) with
\(j\ge1\) and \(j+t\le H+1\) that is needed by the reconstruction is uniquely
determined.

Proof: at time zero the relevant right cells are fixed to zero. Proceed by
induction on time. Every cell in the next row is the value of the deterministic
local map applied to three values in the preceding row; at \(j=1\), the left
input is the supplied boundary value \(c_t\). ∎

## Lemma 3: finite sideways reconstruction is unique

Given \(C\) and its unique right triangle, the inverse equation

\[
x_{j-1}(t)=x_j(t+1)\oplus\bigl(x_j(t)\lor x_{j+1}(t)\bigr)
\]

uniquely constructs the next column to the left wherever all three values on
the right-hand side are defined. Repeating this operation constructs columns
\(-1,-2,\ldots,-H\), with successively shorter time domains. In particular,
it uniquely determines

\[
L_H(C)=\bigl(x_{-1}(0),x_{-2}(0),\ldots,x_{-H}(0)\bigr).
\]

Proof: Lemma 1 gives one and only one bit at each position of the next column.
After one step the new column has times \(0,\ldots,H-1\); after depth \(d\)
it has times \(0,\ldots,H-d\). Induction on \(d\) gives the claim through
depth \(H\). ∎

## Lemma 4: finite forward/reconstruction round trip

Take any bit \(c_0\) and any initial-left word

\[
L=(\ell_1,\ldots,\ell_H).
\]

Evolve Rule 30 forward for \(H\) steps from the finite initial data

\[
x_0(0)=c_0,\qquad x_{-d}(0)=\ell_d\ (1\le d\le H),
\qquad x_j(0)=0\ (j>0),
\]

with arbitrary cells outside the finite center causal cone. Let \(C\) be the
resulting center trace. Then

\[
L_H(C)=L.
\]

Conversely, if a trace \(C\) is reconstructed to \(L_H(C)\), forward evolution
from those reconstructed finite initial data reproduces \(C\) through time
\(H\).

Proof: the actual forward spacetime diagram satisfies every inverse equation,
so uniqueness in Lemma 3 forces reconstruction to recover its initial-left
bits. Conversely, the reconstructed triangle satisfies the Rule 30 local
equation by Lemma 1. Determinism of the forward rule and induction on time make
that locally consistent triangle identical to forward evolution throughout
the finite causal cone. ∎

## Corollary: zero-left finite compatibility

If \(L_H(C)\) is all zero, then exactly one of the following holds:

1. \(c_0=0\), in which case \(C\) is the all-zero trace through time \(H\);
2. \(c_0=1\), in which case \(C\) is the true single-cell Rule 30 center trace
   through time \(H\).

Proof: when the reconstructed left word and the fixed initial right word are
both zero, the finite center causal cone has either the all-zero initial data
or the single-cell initial data, according to \(c_0\). Lemma 4 and forward
determinism determine the trace. ∎

This corollary is useful for auditing finite searches: a purported surviving
trace with \(c_0=1\) must match the trusted center vector bit-for-bit through
the same horizon. It also explains why the constant-zero trace is a genuine
finite reconstruction survivor but is incompatible with the required seed.

## Fixed-width periodic driver lemma

Fix a period word of length \(p\ge1\) and truncate the right half to sites
\(1,\ldots,W\), permanently fixing site \(W+1\) to zero. Include the phase of
the periodic boundary in the state. The resulting driven system has exactly

\[
p2^W
\]

possible states and one successor per state. Therefore every orbit in this
explicitly truncated model is eventually periodic, with preperiod plus period
at most \(p2^W\).

This is a finite pigeonhole argument, not a statement about the original
semi-infinite right half for unbounded time. To safely contain the finite
right causal cone through horizon \(H\), one may take \(W=H\), giving the bound
\(p2^H\). The bound therefore grows exponentially with reconstruction depth.
No uniform finite transducer follows from this construction.

## Why this does not prove eventual nonperiodicity

The computation can establish statements of the form:

> For every description with \(m\le M\) and \(p\le P\), a nonzero
> reconstructed initial-left bit occurs at some depth at most \(H\).

Problem 1 requires exclusion of

\[
\exists m\ge0\ \exists p\ge1\ \forall t\ge m: c_{t+p}=c_t,
\]

where neither \(m\), \(p\), nor a necessary witness depth has a prior bound.
No finite triple \((M,P,H)\) covers those quantifiers. A complete sideways
proof would need an argument applying to every eventual-period description,
such as a depth-independent invariant or a proved finite-state quotient whose
state bound does not grow with depth. Neither is established here.
