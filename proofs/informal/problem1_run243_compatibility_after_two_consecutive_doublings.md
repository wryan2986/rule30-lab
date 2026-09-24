# Problem 1 — run 243: compatibility is automatic after two consecutive doublings

Problem 1 remains open.

Run 242 reduced the width-8 complexity calculation to a compatibility question.  The upper bound

\[
L(X_r)\le P+L(X_{r-2}^{[P]})+1
\]

on the complementary branch is exact only if a state selecting that branch can simultaneously maximize the length-`P` complexity of coordinate `r-2`.

For two consecutive order doublings, this compatibility is not an extra assumption: **every witness for the second doubling already maximizes the lower coordinate complexity.**

## Setup

Assume the global prefix orders satisfy

\[
O_{r-3}=Q,\qquad O_{r-2}=2Q=P,\qquad O_{r-1}=2P=4Q.
\]

All these orders are powers of two in the triangular Rule-30 system.

Choose any initial lower-prefix state through coordinate `r-2` for which adjoining coordinate `r-1` realizes the second doubling, i.e. the resulting prefix through `r-1` has orbit period `2P`.

Let `D` be the orbit period of its prefix through coordinate `r-2`.  Since coordinate `r-1` is a binary skew extension of that lower orbit, its period is at most `2D`.  The chosen state has period `2P`, so necessarily

\[
D=P.
\]

Thus a witness for the second doubling must already lie on a full-period `P` orbit one level below.

## Full period at level r-2 forces complementary Q-halves

Now inspect coordinate `r-2` on this same state.  Its lower prefix through `r-3` has orbit period `E\mid Q`.

The forcing of coordinate `r-2` is therefore `E`-periodic.  If `E<Q`, then because all periods are powers of two, `Q/E` is even.  Over a shift of length `Q`, the forcing parity is repeated an even number of times, so

\[
x_{r-2}(t+Q)=x_{r-2}(t).
\]

That would make the prefix through `r-2` have period at most `Q`, contradicting `D=P=2Q`.

Hence `E=Q`, and the parity over one `Q`-block must be `1`; otherwise the same contradiction occurs.  Therefore the length-`P=2Q` word

\[
B=X_{r-2}^{[P]}
\]

has complementary halves:

\[
\boxed{B=(C,\bar C).}
\]

Games–Chan immediately gives

\[
\boxed{L(B)=Q+1.}
\]

This is exactly the maximal complexity from the run-242 doubling theorem.  We have therefore proved the compatibility statement

\[
\boxed{
\text{second-doubling witness}\Longrightarrow
L(X_{r-2}^{[P]})=Q+1=L_{r-2}(P).
}
\]

No separate search for a compatible maximizer is needed.

## Consequence for a plateau after the two doublings

Assume in addition that the next extension does not double:

\[
O_r=O_{r-1}=2P.
\]

Use the same state witnessing the doubling at coordinate `r-1`.  Over the length-`2P` horizon, coordinate `r-1` has complementary `P`-halves, so run 242's exact OR half-difference identity applies:

\[
L(F_r)=P+L(\bar B).
\]

Here `L(B)=Q+1>1`, hence complementing does not change its complexity.  Cyclic integration on the plateau gives

\[
L(X_r)=L(F_r)+1=P+Q+2.
\]

Run 242 already supplies the matching upper bound for every state.  Therefore:

\[
\boxed{
O_{r-3}=Q,\ O_{r-2}=2Q,\ O_{r-1}=4Q,\ O_r=4Q
\Longrightarrow
L_r(4Q)=3Q+2.
}
\]

Equivalently, writing `P=2Q`,

\[
\boxed{L_r(2P)=P+P/2+2.}
\]

For the observed width-8 pattern

\[
O_5=8,\quad O_6=16,\quad O_7=32,\quad O_8=32,
\]

this gives directly

\[
L_8(32)=16+8+2=26,
\]

without importing an exhaustive witness from run 241.

## Computational sanity checks

Exhaustive enumeration of the small triangular system agrees with the stronger witness statement at both available consecutive-doubling patterns:

- for the `2 -> 4 -> 8` run, every state witnessing the second doubling has lower-coordinate complexity `3=2+1`;
- for the `8 -> 16 -> 32` run, every state witnessing the second doubling has lower-coordinate complexity `9=8+1`.

The proof above does not depend on those enumerations.

## What this resolves and what remains

The compatibility blocker stated at the end of run 242 is resolved for **two consecutive doublings**, which is exactly the configuration needed for the width-8 `26` calculation.

The next genuinely new case is not compatibility in that configuration.  It is to derive analogous exact complexity recurrences when the order-decision word contains a plateau between doublings (for example `double / plateau / double`) or longer plateau runs.  There a witness for a later doubling need not force the coordinate two levels below onto the simple complementary-half maximizer, so additional half-difference structure may be needed.