# The 2-adic Rule 30 diagonal map

Status: complete informal proof of the stated diagonal-map lemmas and exact
countermodel. These are partial results and a proof-strategy barrier, not a
proof of Rule 30 center nonperiodicity. They have not yet been formalized in
Lean.

## 1. Setup

In right-edge coordinates, Rule 30 acts on a binary state by

\[
T(S)=S\mathbin{\mathtt{xor}}
\bigl((S\ll1)\mathbin{\mathtt{or}}(S\ll2)\bigr).
\]

This formula makes sense both for nonnegative integers and for the 2-adic
integers \(\mathbb Z_2\), interpreted digit by digit. If

\[
S=\sum_{k\geq0}a_k2^k,
\]

then, with \(a_{-1}=a_{-2}=0\),

\[
a_k(T(S))=a_k(S)\mathbin\oplus
\bigl(a_{k-1}(S)\lor a_{k-2}(S)\bigr).
\]

In particular, output digits through position \(m-1\) depend only on input
digits through position \(m-1\). Thus \(T\) respects congruence modulo
\(2^m\) and is a well-defined continuous map on \(\mathbb Z_2\).

Define the growing-diagonal map \(\Delta:\mathbb Z_2\to\mathbb Z_2\) by

\[
\operatorname{bit}_t(\Delta(S))
=\operatorname{bit}_t(T^t(S)).
\]

For a finite-support state whose rightmost one is at the moving-frame origin,
these output digits are exactly its fixed-spatial-coordinate temporal trace.

## 2. Unit triangularity

### Lemma

For every \(t\geq0\), there is a Boolean function \(g_t\) of the lower input
digits such that

\[
\operatorname{bit}_t(\Delta(S))
=a_t\mathbin\oplus g_t(a_0,\ldots,a_{t-1}).
\]

### Proof

For any coordinate \(k\), one application of \(T\) leaves \(a_k\) present
with coefficient one and toggles it by a function of coordinates below
\(k\). The evolution of those lower coordinates is independent of \(a_k\)
and of all higher coordinates. Induction on the number of iterations therefore
gives

\[
\operatorname{bit}_k(T^r(S))
=a_k\mathbin\oplus G_{k,r}(a_0,\ldots,a_{k-1})
\]

for every \(r\). Set \(k=r=t\). ∎

For \(m\geq1\), let \(\Delta_m\) be the induced map modulo \(2^m\). The lemma
shows that \(\Delta_m\) is a unit triangular Boolean map: output digit zero
uniquely determines input digit zero, then output digit one uniquely determines
input digit one, and so on. Consequently every \(\Delta_m\) is a permutation
of \(\mathbb Z/2^m\mathbb Z\).

The permutations are compatible under reduction modulo lower powers of two.
Recursively solving the input digits therefore gives a unique 2-adic preimage
for every 2-adic output. Hence:

> **Theorem 1.** The growing-diagonal map \(\Delta\) is a bijection of
> \(\mathbb Z_2\).

There is a stronger metric statement. If \(S\) and \(R\) first differ at
digit \(n\), their outputs agree below digit \(n\), while the unit triangular
formula makes output digit \(n\) differ. Therefore

\[
v_2(\Delta(S)-\Delta(R))=v_2(S-R).
\]

> **Theorem 2.** \(\Delta\) is an isometry of \(\mathbb Z_2\).

This is the infinite version of the previously proved finite
sideways-prefix equivalence: the first changed initial-left bit and the first
changed temporal bit have the same index.

## 3. Eventual periodicity becomes rationality

A binary digit sequence is eventually periodic if and only if the 2-adic
integer represented by those digits is rational.

In one direction, a preperiod of length \(q\) followed by a period-\(p\) word
is a finite binary polynomial plus

\[
2^q\frac{W}{1-2^p},
\]

which is rational and lies in \(\mathbb Z_2\). Conversely, for a rational
2-adic integer \(a/b\) with odd \(b\), binary long division has only finitely
many possible remainders modulo \(b\), so its digits eventually repeat.

Combining this fact with the right-edge equivalence gives exact restatements:

- the original single-cell Problem 1 asks whether
  \(\Delta(1)\notin\mathbb Q\);
- the stronger whole-tail conjecture asks whether

  \[
  \Delta(\{1,3,5,\ldots\})\cap\mathbb Q=\varnothing;
  \]

- equivalently, for every odd rational \(C\in\mathbb Z_2\), the unique lift
  \(\Delta^{-1}(C)\) must have infinitely many nonzero binary digits.

Here positive odd integers are exactly the right-edge states with finite
spatial support, while rational 2-adic outputs are exactly eventually
periodic temporal traces.

The last formulation is a sharper target than finite trace rejection. Given
an eventually periodic \(C\), the compatible residues

\[
S_m=\Delta_m^{-1}(C\bmod 2^m)
\]

form the successive binary prefixes of one unique 2-adic state. The required
claim is that these prefixes never stabilize to a nonnegative integer.

## 4. An exact periodic countermodel without finite spatial support

Define

\[
A=-\frac13=1+2^2+2^4+\cdots
\]

and

\[
B=\frac13=1+2^1+2^3+2^5+\cdots.
\]

For \(A\), the shifted supports of \(A\ll1\) and \(A\ll2\) together occupy
every digit position at least one. XOR with \(A\) leaves digit zero and every
positive odd digit set, so

\[
T(A)=B.
\]

The same support calculation for \(B\) gives

\[
T(B)=A.
\]

Thus \(A,B\) form an exact 2-cycle. At even time \(t\), state \(A\) has digit
\(t\) equal to one; at odd time \(t\), state \(B\) has digit \(t\) equal to
one. It follows that

\[
\Delta(A)=1+2+2^2+\cdots=-1.
\]

Starting instead from \(B\), digit zero is one, every later even-time sample
uses a positive even digit of \(B\), and every odd-time sample uses an odd
digit of \(A\). All samples after time zero are zero, so

\[
\Delta(B)=1.
\]

> **Theorem 3.** An exactly periodic Rule 30 right-edge orbit can have an
> exactly periodic growing diagonal. Fixed-coordinate power-of-two periods do
> not contradict temporal periodicity of the growing diagonal.

This is not a counterexample to the whole-tail conjecture: \(A\) has infinitely
many nonzero spatial digits and is not a nonnegative integer.

## 5. The finite-horizon compactness trap

Let

\[
A_m=A\bmod 2^m.
\]

Each \(A_m\) is a finite positive odd integer. Unit triangularity gives

\[
\Delta_m(A_m)=-1\bmod 2^m.
\]

Therefore the finite seed \(A_{H+1}\) has an all-one center trace through
time \(H\). The survivor changes as \(H\) increases and converges 2-adically
to the infinite-support state \(A\).

Consequently, either of the following inferences would be invalid:

1. a compatible finite seed at every horizon implies one fixed compatible
   finite seed for all time;
2. temporal periodicity plus periodicity of every fixed moving-frame
   coordinate forces a contradiction.

The explicit \(-1/3\) state satisfies the finite conditions at every depth and
the compatible limit exists, but the limit loses finite spatial support.

## 6. Research consequence

The unresolved property is now isolated precisely:

> Show that the inverse 2-adic lift of every odd eventually periodic trace has
> infinitely many one bits, or find an odd periodic trace whose lift is a
> nonnegative integer.

A successful proof must detect eventual-zero spatial support. Arguments using
only finite quotient bijectivity, fixed-coordinate periods, or existence of
arbitrarily deep compatible prefixes cannot do this. Promising continuations
must derive a recurrence or invariant for the lift bits driven by a periodic
output, then distinguish eventual-zero lifts from the explicit rational
infinite-support cycles above.

## 7. Executable checks

The supporting finite analyzer is
`experiments/problem1_nonperiodicity/analyze_two_adic_diagonal.py`. It compares
two independent evaluators, exhausts every finite quotient in its stated
range, checks the inverse in both directions, and verifies the \(A,B\) cycle.
Those checks are finite-exhaustive regression evidence. The all-width claims
in this note rest on the proofs above, not on extrapolation from the checks.
