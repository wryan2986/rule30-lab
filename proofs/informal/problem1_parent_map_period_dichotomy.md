# Problem 1: exact-period sectors of the zero-return parent map

## Context

Run 85 identified the zero-return parent map

\[
P_n = D\circ \rho_n^{-1},\qquad D(x)=Sx\oplus x,
\]

on nonzero zero targets. Run 82 established rotation equivariance, repetition naturality, and exact rotational-period preservation for \(\rho_n\).

This note records a useful consequence for the actual root basin which sharpens the period-16 / period-32 search.

## Lemma 1: cyclic derivative preserves exact rotational period except on the constant sector

Let \(x\in\{0,1\}^n\), and suppose \(D(x)=Sx\oplus x\neq 0\). Then

\[
\operatorname{per}(D(x))=\operatorname{per}(x),
\]

where \(\operatorname{per}\) denotes least positive rotational period.

### Proof

If \(S^k x=x\), then equivariance of \(D\) gives \(S^kD(x)=D(x)\), so every rotational symmetry of \(x\) is a symmetry of \(D(x)\).

Conversely, suppose \(S^kD(x)=D(x)\). Then

\[
D(S^k x\oplus x)=S^kD(x)\oplus D(x)=0.
\]

The kernel of the cyclic derivative consists exactly of the two constant words \(0^n,1^n\). Hence

\[
S^k x=x\quad\text{or}\quad S^k x=\bar x.
\]

The second alternative would imply \(S^{2k}x=x\). It can therefore occur only as a half-period complement symmetry. But if \(S^kD(x)=D(x)\) and \(S^kx=\bar x\), direct substitution gives the same derivative because \(D(\bar x)=D(x)\); this shows that the derivative can in fact lose a factor two in the antiperiodic case. Thus the stronger equality claimed above is false in general.

The correct statement is the dichotomy below.

## Corrected lemma: derivative period is either r or r/2

Let \(x\) have exact rotational period \(r\) and \(D(x)\neq0\). Then

\[
\operatorname{per}(D(x))\in\{r,r/2\}.
\]

The drop to \(r/2\) occurs exactly when

\[
S^{r/2}x=\bar x.
\]

### Proof

If \(D(x)\) has a shift symmetry \(k\), then the argument above gives \(S^kx=x\) or \(S^kx=\bar x\). In the first case \(r\mid k\). In the second, squaring gives \(r\mid2k\), while \(r\nmid k\); modulo the exact period this forces the nontrivial complement shift to be \(r/2\). Conversely, an antiperiodic half-shift clearly fixes \(D(x)\) because \(D(\bar x)=D(x)\).

## Consequence for P_n

Run 82 proved that \(\rho_n^{-1}\) preserves exact rotational period. Therefore for every nonzero target \(a\), writing \(x=\rho_n^{-1}(a)\),

\[
\operatorname{per}(P_n(a))\in
\{\operatorname{per}(a),\operatorname{per}(a)/2\}.
\]

A strict period drop occurs **exactly** when the boundary integration \(x\) is antiperiodic at half its exact period.

Thus ancestry under \(P_n\) can never increase exact rotational period. Along every root-basin path the period forms a nonincreasing chain, and every strict decrease is a factor of two.

For dyadic ambient periods this gives a canonical filtration

\[
2^m\to2^{m-1}\to\cdots\to2\to1.
\]

The genuinely new portal trees at period \(2^m\) are precisely the portions of the root basin that remain in exact period \(2^m\) until their first antiperiodic integration causes the drop to \(2^{m-1}\). After that drop, repetition naturality identifies the remainder of the ancestry with the inherited lower-period basin.

## Why this helps

This gives a rigorous version of the informal inherited/new-sector decomposition without requiring global enumeration of \(P_n\):

* proper-period ancestry cannot jump back into the full-period sector;
* every new full-period branch has a unique attachment point determined by its first period-halving edge;
* the period-halving condition is explicit on \(\rho_n^{-1}(a)\): half-rotation equals complement;
* repeated lower-period tails are exact, including connector lengths, by run 82.

For the period-32 obstruction, the useful target is therefore not a global invariant of \(P_{32}\), but a bound on how long a full-period ancestry chain can avoid the antiperiodic boundary condition

\[
S^{16}\rho_{32}^{-1}(a)=\overline{\rho_{32}^{-1}(a)}.
\]

That condition is exactly the event that the next parent drops into the inherited period-16 sector.

## Dead end corrected during this run

An initially tempting stronger claim, that \(D\) always preserves exact period, is false. The antiperiodic case is precisely the exception. This is not a nuisance: it identifies period-halving edges algebraically and explains the doubling portals.
