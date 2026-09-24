# Problem 1 — run 245: the available double / plateau / double evidence is confounded by a preceding doubling

Problem 1 remains open.

Run 244 derived a correct exact decision functional for a local `double / plateau / double` pattern, but its computational interpretation needs tightening. The two available examples do **not** test the proposed new principle that the final doubling selects the high-complexity plateau branch. In both examples there is an additional doubling immediately before the displayed pattern, so run 243 already forces the compatibility needed for the high-complexity plateau.

## Setup and the run-244 identity

Assume

\[
O_{r-3}=Q,\qquad O_{r-2}=2Q,\qquad O_{r-1}=2Q.
\]

On a state realizing the first displayed doubling, write

\[
X_{r-2}=(C,\bar C),\qquad X_{r-3}=(B,B),\qquad
Y=X_{r-1}=(Y_0,Y_1),\qquad D=Y_0\oplus Y_1.
\]

Run 244 correctly proves

\[
\Delta D=\bar B
\]

and, for the next forcing `H=f_r`,

\[
\operatorname{parity}(H)
=\operatorname{parity}(Y_0)\oplus\langle D,C\rangle.
\]

Thus the final doubling is decided by that functional.

## Why the two available examples do not isolate a new selection law

The examples cited in run 244 are

\[
4\to8\to8\to16
\]

and

\[
16\to32\to32\to64.
\]

But in the actual global order sequence they occur inside

\[
2\to4\to8\to8\to16
\]

and

\[
8\to16\to32\to32\to64.
\]

Therefore the first displayed doubling in each run-244 example is itself the **second of two consecutive doublings**.

Run 243 already proves that a witness of the second consecutive doubling automatically realizes maximal lower-coordinate linear complexity. Combining that with run 242's plateau half-block formula forces the high-complexity plateau branch before the final-doubling functional is even inspected.

Concretely, if

\[
O_{r-4}=Q/2,\quad O_{r-3}=Q,\quad O_{r-2}=2Q,
\]

then a state witnessing the doubling to `2Q` has the required maximal complexity at coordinate `r-3`. If the next order is a plateau `O_{r-1}=2Q`, run 242 gives the maximal plateau complexity

\[
L(X_{r-1})=Q+L(\bar B)+1,
\]

with the lower term already maximal by run 243. Hence the high-complexity plateau property is a consequence of the preceding `double / double`, not evidence that the *following* doubling functional selects it.

For the observed cases this recovers the known values:

- `2 -> 4 -> 8 -> 8`: the period-8 plateau top word is forced onto the maximal class `L=8` for states realizing the relevant consecutive-doubling chain;
- `8 -> 16 -> 32 -> 32`: the period-32 plateau top word is forced onto the maximal class `L=26` for states realizing that chain.

The subsequent doublings to 16 and 64 are compatible with those classes, but do not establish a converse selection theorem.

## Computational sanity check

A direct exhaustive check of the `2 -> 4 -> 8 -> 8` chain confirms the point: after requiring the actual prefix periods corresponding to the chain, every relevant period-8 plateau word already has cyclic linear complexity 8. There is no low-complexity branch left for the final-doubling functional to reject.

This also explains an apparent discrepancy one can obtain by enumerating merely period-8 top-coordinate words without conditioning on the full preceding prefix-period chain: lower-complexity period-8 words exist, but they are not witnesses of the same consecutive-doubling history.

## Consequence for the research target

The run-244 Boolean functional remains useful and proved. What is **not** currently supported is the stronger empirical claim

> final doubling after a plateau selects the high-complexity plateau branch.

The existing examples cannot distinguish that statement from the already-proved run-243 compatibility theorem.

A genuine test requires a `double / plateau / double` occurrence in which the first displayed doubling is **not** itself preceded by a doubling, or a symbolic argument that does not assume the preceding `double / double` history. Until such a case is found, the correct blocker is:

\[
\boxed{\text{classify the run-244 functional without importing run-243 compatibility from an earlier doubling.}}
\]

This correction narrows the next computation: search longer order prefixes for the first `D/P/D` pattern whose initial `D` is preceded by `P` (or otherwise not by `D`), then test whether the decision functional still correlates with maximal plateau complexity. If no such order pattern occurs, that absence itself may be a stronger structural target than the proposed selection law.
