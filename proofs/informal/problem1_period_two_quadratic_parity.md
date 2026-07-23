# Quadratic parity no-go for the period-two coupled strip

Status: exact coefficient no-go theorem over `GF(2)`. It closes one nonlinear
finite-memory class. It does not exclude period two and does not solve Rule 30
center nonperiodicity.

## 1. Motivation

The coupled-strip theorem gives the exact word update

\[
J^+=q\,p\,\tau_{11}(J),
\]

where `q` is supplied by the exact moving fringe, `tau_11` is the complete
four-state whole-word scan, and the terminal scan state

\[
e(J)\in\{00,01,10,11\}
\]

is the next reconstructed spatial pair. Rational additive functionals through
nearest-neighbor range cannot distinguish `e=00` from a nonzero pair.

The next natural nonlinear class is parity-based. Such quantities can contain
products of global factor-count parities and therefore are not rational
additive cocycles.

## 2. Factor-parity coordinates

For `r>=1`, let `P_r` be the set of words over `{t,p,u}` of lengths one through
`r`. For an inverse word `J`, define

\[
N_w(J)=\#\{\text{occurrences of }w\text{ in }J\}\pmod2,
\qquad w\in P_r.
\]

Write `N_r(J)` for the complete vector of these parities. We allow an arbitrary
polynomial

\[
Q:\mathbb F_2^{|P_r|}\to\mathbb F_2
\]

of algebraic degree at most two. Because `x^2=x` over `GF(2)`, its coefficient
basis consists of all linear monomials `N_w` and all square-free products
`N_w N_v` with `w!=v`.

For ranges one, two, and three the numbers of coordinates and monomials are:

| range `r` | factor parities | degree-1/2 monomials |
|---:|---:|---:|
| 1 | 3 | 6 |
| 2 | 12 | 78 |
| 3 | 39 | 780 |

## 3. The proposed cocycle

Fix either boundary branch `q=t` or `q=u`. The strongest one-step identity of
this form is

\[
Q(N_r(qp\tau_{11}(J)))+Q(N_r(J))=V(e(J))+C, \tag{1}
\]

for every inverse word `J`, where `V` is an arbitrary function on the four
terminal states and `C` is an arbitrary scalar.

Allowing `C` to be arbitrary is important. If a proposed invariant also has an
arbitrary potential `P(A)` on the exact current fringe state, then at a fixed
fringe state `A` the term

\[
P(F(A))+P(A)+K
\]

is just one scalar `C`. Therefore a no-go theorem for (1), separately for each
fixed branch, automatically covers arbitrary exact-fringe-state potentials.

## 4. Exact finite coefficient systems

Equation (1) is linear in the unknown coefficients of `Q`, `V`, and `C`, even
though `Q` is nonlinear in the word statistics. Evaluate it on all words up to
the lengths shown below and perform exact bitset Gaussian elimination over
`GF(2)`.

| range | maximum word length | variables | rank | nullity |
|---:|---:|---:|---:|---:|
| 1 | 5 | 11 | 9 | 2 |
| 2 | 6 | 83 | 68 | 15 |
| 3 | 7 | 785 | 581 | 204 |

For both `q=t` and `q=u`, appending any one of the three coefficient rows

\[
V_{00}+V_{11},\qquad V_{01}+V_{11},\qquad V_{10}+V_{11}
\]

does not increase the rank. Hence all three rows already belong to the exact
row space, and every solution of (1) satisfies

\[
\boxed{V_{00}=V_{01}=V_{10}=V_{11}.} \tag{2}
\]

A combined system with separate constants `C_t,C_u` gives the same conclusion.
For range three it has 786 variables, 6,422 distinct equations, rank 582, and
nullity 204.

## 5. Why the finite elimination is an all-word theorem

The calculation is not using finite absence as evidence for an infinite
statement. Assume an identity of form (1) holds for every word. It must then
hold on the finite subset of words used above. Exact elimination of that finite
subsystem logically forces (2). Therefore every all-word identity in the
stated coefficient class has constant terminal potential.

No converse classification of all `Q` coefficients is required for this
conclusion. The potentially large nullspaces contain parity identities and
functionals that do not distinguish terminal states.

## 6. Conclusion and boundary

> **Quadratic parity no-go.** For factor ranges `r=1,2,3`, no polynomial of
> algebraic degree at most two in the parities of all factors of length at most
> `r` can participate in an all-word one-step cocycle whose boundary term
> distinguishes terminal state `00` from any nonzero terminal state. This
> remains true with an arbitrary potential on the exact current fringe state.

This closes a genuinely nonlinear finite-memory class beyond rational additive
statistics. It does not cover:

- algebraic degree three or greater;
- factor range four or greater;
- observables depending on the order of factors beyond their global counts;
- memory growing with the strip width;
- archimedean or other non-finite-field quantities.

The next admitted target is therefore not another small additive weight table.
It is either a higher-order nonlinear observable that uses factor arrangement,
or a growing-memory quantity defined directly on the moving-cut row.
