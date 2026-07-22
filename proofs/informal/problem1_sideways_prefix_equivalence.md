# Sideways reconstruction equals first-prefix disagreement

Status: informal rigorous finite lemma; not a proof of Problem 1

Fix a horizon \(H\), an initial center bit \(a\), and zero initial cells at
every positive coordinate. Let \(R^a_0,\ldots,R^a_H\) be the center trace
obtained when every negative initial cell is also zero. Thus \(R^0\) is the
all-zero trace and \(R^1\) is the single-cell Rule 30 center trace.

For any proposed trace \(C=(c_0,\ldots,c_H)\) with \(c_0=a\), finite
left-permutive reconstruction returns the unique initial-left word

\[
L_H(C)=(\ell_1,\ldots,\ell_H),
\qquad \ell_d=x_{-d}(0).
\]

## Theorem

The first reconstructed one and the first center-trace disagreement occur at
the same index:

\[
\min\{d\in\{1,\ldots,H\}:\ell_d=1\}
=
\min\{t\in\{1,\ldots,H\}:c_t\ne R^a_t\}.
\]

If either set is empty, both are empty.

## Proof

Finite sideways inversion gives a genuine Rule 30 triangle whose initial
negative cells are the reconstructed bits \(\ell_d\), whose initial positive
cells are zero, and whose center trace is \(C\). Compare this triangle with
the reference evolution defining \(R^a\).

Suppose first that \(d\) is the least index with \(\ell_d=1\). For every
time \(t<d\), the center's backward light cone reaches only initial sites
\(-t,\ldots,t\). The two initial configurations agree throughout that cone:
the reconstructed cells \(\ell_1,\ldots,\ell_t\) are zero, as are all cells
of the reference configuration. Determinism therefore gives \(c_t=R^a_t\).

At time \(d\), compare the rightmost edge of the influence cone from site
\(-d\). At time zero the two configurations differ at \(-d\), while every
site to its right agrees. Inductively, if the rightmost disagreement is at
site \(-d+k\) at time \(k\), then the center and right inputs used to update
site \(-d+k+1\) agree in the two evolutions, while the left inputs differ.
Rule 30 is permutive in that left input:

\[
f(0,b,c)\ne f(1,b,c)
\quad\text{for every }b,c\in\{0,1\}.
\]

Hence the rightmost disagreement advances one site at every step. At time
\(d\) it reaches site zero, so \(c_d\ne R^a_d\). The first disagreement is
therefore exactly \(d\).

If no reconstructed bit through depth \(H\) is one, both initial
configurations agree throughout the complete backward light cone of the
center through time \(H\), so their center traces agree throughout the
horizon. Conversely, if a first reconstructed one exists, the preceding
argument produces a disagreement at that same index. This proves the empty
case as well. ∎

## Consequences for the periodic-trace searches

For the required seed \(a=1\), a candidate's first nonzero reconstructed-left
depth is exactly its first mismatch from the trusted Rule 30 center prefix.
Accordingly:

- finite sideways reconstruction gives a valid, local incompatibility
  certificate;
- the finite exclusion histogram contains the same mathematical information
  as a direct prefix-comparison histogram;
- running the triangular reconstruction does not provide independent evidence
  for eventual nonperiodicity; and
- proving that every eventually periodic proposal reconstructs at least one
  nonzero left cell is equivalent to proving that no eventually periodic
  proposal equals the true center sequence.

The stronger proposed route—showing that every eventually periodic proposal
reconstructs a left tail with *infinitely many* nonzero cells—does not collapse
to this finite lemma and remains open. No finite first-witness search addresses
that stronger tail statement.
