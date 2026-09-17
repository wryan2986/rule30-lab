# Problem 1: period-halving edges are exactly repetitions of odd-parity blocks

## Context

Run 87 proved that for the cyclic derivative

\[
D(x)=Sx\oplus x,
\]

an exact-period-\(2r\) word can drop to period \(r\) under \(D\) exactly when it is antiperiodic:

\[
S^r x=\bar x.
\]

This note identifies the image of that antiperiodic sector exactly. The result removes \(\rho_n\) from the *target-side* test for a period-halving edge.

## Theorem: derivative of an antiperiodic word is a repeated odd block

Let \(x\) have exact rotational period \(2r\) and satisfy

\[
S^r x=\bar x.
\]

Then

\[
D(x)=ww
\]

for a length-\(r\) word \(w\) of **odd XOR parity**. Moreover \(w\) has exact rotational period \(r\).

### Proof

Because \(D\) commutes with rotation and complement does not change the derivative,

\[
S^rD(x)=D(S^rx)=D(\bar x)=D(x).
\]

Hence \(D(x)=ww\) for some length-\(r\) block \(w\).

Write indices cyclically along the first half. Then

\[
w_i=x_{i+1}\oplus x_i,\qquad 0\le i<r.
\]

Taking XOR over one block telescopes:

\[
\bigoplus_{i=0}^{r-1}w_i=x_r\oplus x_0.
\]

Antiperiodicity gives \(x_r=\bar x_0\), so the right-hand side is 1. Thus \(w\) has odd XOR parity.

Finally, run 87's period dichotomy says that an exact-period-\(2r\) antiperiodic word has derivative of exact period \(r\), so the block \(w\) itself has exact period \(r\).

## Converse

Let \(w\) be a length-\(r\) word of odd XOR parity, and consider the repeated length-\(2r\) word

\[
y=ww.
\]

Since \(y\) has even total parity, the cyclic derivative equation

\[
D(x)=y
\]

has exactly the two complementary solutions \(x,\bar x\).

For either solution, integrating over the first \(r\) derivative bits gives

\[
x_r\oplus x_0=\bigoplus_{i=0}^{r-1}w_i=1.
\]

Therefore

\[
S^r x=\bar x.
\]

So every derivative preimage of \(ww\) is antiperiodic. If \(w\) has exact period \(r\), then \(x\) has exact period \(2r\): a smaller rotational period for \(x\) would force a smaller rotational period for \(D(x)=ww\), except for the already-accounted factor-two derivative drop, which would make the derivative period smaller than \(r\).

Thus, for exact-period blocks,

\[
\boxed{\;x\text{ exact period }2r\text{ and antiperiodic}\;\Longleftrightarrow\;D(x)=ww\text{ with }w\text{ exact period }r\text{ and odd parity}.\;}
\]

## Corollary for the zero-return parent map

Recall

\[
P_{2r}(a)=D(\rho_{2r}^{-1}(a)).
\]

If \(a\) has exact period \(2r\), then its parent has exact period \(r\) **if and only if**

\[
\boxed{P_{2r}(a)=ww}
\]

for an exact-period-\(r\), odd-parity block \(w\).

Equivalently, every period-halving edge from the new \(2r\)-sector lands directly on a repeated odd-parity target from the lower period.

This is stronger than the run-87 formulation in one practical sense: after an edge has been computed, recognizing that it is the attachment edge requires only inspecting the parent target. One does not need to reconstruct \(\rho_{2r}^{-1}(a)\) and test its half-rotation/complement symmetry.

## Dyadic interpretation

At ambient period \(2r\), the inherited copy of a lower-period target is \(ww\). The theorem says that only **odd-parity** lower-period blocks can be entry points from a genuinely new exact-period-\(2r\) branch.

This matches the earlier observation that odd-parity zero targets are terminal with respect to singular integration at their own period: an odd \(w\) has no cyclic derivative preimage at period \(r\), but after doubling to \(ww\) it acquires exactly two preimages, and those preimages are necessarily new exact-period-\(2r\) antiperiodic words.

So dyadic doubling has an exact algebraic mechanism:

1. an odd-parity terminal target \(w\) at period \(r\) has no integration at period \(r\);
2. its repetition \(ww\) has even parity at period \(2r\);
3. the two integrations of \(ww\) are complementary, antiperiodic, exact-period-\(2r\) words;
4. these are precisely the boundary words that can generate the new portal branches attached at \(ww\).

This identifies period-halving attachment points with repeated lower-period terminal candidates and explains why the new sector is born specifically at doubled odd leaves.

## Consequence for the period-32 target

For a full-period-32 ancestry branch, the first drop into period 16 must land on

\[
ww
\]

where \(w\) is an exact-period-16 odd-parity target. Thus the attachment set is not the whole inherited period-16 sector: it is the repeated image of its odd-parity targets (and, within the root basin, its odd leaves).

The remaining hard question is quantitative: bound the number of full-period-32 parent steps before such a repeated odd block is reached. But the terminal condition is now expressed entirely on the target side and is exactly characterized.
