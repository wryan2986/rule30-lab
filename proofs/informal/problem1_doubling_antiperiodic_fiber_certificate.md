# Problem 1: antiperiodic fiber certificate at every genuine period doubling

## Context

Runs 42--44 isolated the missing global step: a FULL common-origin finite-entry realization already has infinitely many actual period doublings, but distinct late scalar boundary hits do not pull backward monotonically to distinct anchored hits. This note records a stronger exact certificate attached to a genuine doubling. It is not yet the needed accumulation theorem, but it preserves temporal phase information that the scalar hit indicator loses.

## Setup

Use the one-bit factorization

\[
x(t)=2u(t)+b(t),\qquad A(x)\gg1=A(u).
\]

Assume the parent orbit \(u(t)\) has exact period \(p\), and the lifted orbit \(x(t)\) has exact period \(2p\). Let \(F:\{0,1\}\to\{0,1\}\) be the return map on the omitted low bit after one complete parent period.

## Lemma: a doubling fiber is exactly antiperiodic

Because the lifted orbit has period \(2p\), the fiber return map cannot fix the fiber state reached by the orbit after one parent period. A self-map of a two-point set whose relevant orbit has length two must exchange the two points. Hence

\[
F(0)=1,\qquad F(1)=0.
\]

Therefore along the actual doubled child orbit,

\[
\boxed{b(t+p)=1\oplus b(t)\quad\text{for every }t.}
\]

So a genuine period doubling is witnessed not merely by a local nonzero boundary bit but by a full temporal column with half-period complement symmetry.

Conversely, if a lift over a period-\(p\) parent satisfies \(b(t+p)=1\oplus b(t)\), then it cannot have period \(p\), while projection shows its period divides \(2p\); therefore its exact period is \(2p\). Thus the antiperiodicity condition is an exact certificate for the doubling branch.

## Immediate consequences

1. Every length-\(2p\) temporal block of the new fiber contains exactly \(p\) ones and \(p\) zeros.
2. The second half of the fiber history is determined by the first half, but is disjoint from it pointwise.
3. For \(p>1\), the XOR parity of the full doubled fiber column is even. Therefore plain column parity cannot itself count successive doublings.
4. The useful information is the *half-period complement relation*, not scalar occupancy or total parity.

## Nested doubling tower

Suppose a chain of projections/lifts contains genuine doublings

\[
p,2p,4p,\ldots,2^r p.
\]

At the coordinate introduced at the \(j\)-th doubling, its temporal column on the corresponding child cycle satisfies

\[
\boxed{b_j(t+2^{j-1}p)=1\oplus b_j(t).}
\]

Thus successive doublings create a hierarchy of distinct complement scales. This is stronger than merely saying that periods double: each doubling leaves a phase-sensitive spacetime witness at its own coordinate/scale.

## Why this does not yet close Problem 1

The certificate lives on the periodic forced state used at that passage. Existing common-origin work must still show that certificates from many different doubling passages can be represented simultaneously in one spacetime window of the original realization. Without that common-origin transport, the hierarchy can move outward to new coordinates as bitlength grows and need not violate a fixed anchored activity bound.

Also, run 44's counterexample to backward monotonicity remains decisive: antiperiodicity cannot be replaced by selecting one of its \(1\)-bits and pulling that scalar event backward.

## Refined next target

Instead of seeking an injection from doubling passages to scalar boundary hits, seek a transport statement preserving the two-time relation

\[
(b(t),b(t+p))\in\{(0,1),(1,0)\}.
\]

A sufficient global bridge would pull \(r\) distinct doubling passages into one common-origin joint window while retaining \(r\) distinct complement scales. Such a theorem could potentially force window complexity/activity to grow with \(r\), unlike the scalar-hit formulation of run 43.

## Status

New exact local certificate proved. No contradiction with finite entry yet. The main blocker is now simultaneous common-origin transport of multiple antiperiodic certificates.