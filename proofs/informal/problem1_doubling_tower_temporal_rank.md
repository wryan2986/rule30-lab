# Problem 1: temporal-rank structure of a genuine doubling tower

Status: new structural lemma; Problem 1 remains open.

## Context

Run 45 proved that a genuine lift from exact period `p` to exact period `2p` carries an omitted-bit column `b` satisfying

\[
b(t+p)=1\oplus b(t).
\]

The global obstruction is still simultaneous common-origin transport. This note asks what *would* be gained if several such doubling certificates are simultaneously represented in one descendant periodic spacetime window.

## Lemma 1: the new fiber column has exact period `2p`

Assume the parent has exact period `p`, where (by the finite-cycle theorem) `p` is a power of two, and the child genuinely doubles to exact period `2p`. The fiber column `b(t)` is generated over a period-`p` parent, so its period divides `2p`. Antiperiodicity gives

\[
b(t+p)=1\oplus b(t),
\]

so its period does not divide `p`. Since every divisor of `2p` is a power of two and every proper divisor of `2p` divides `p`, the only possibility is

\[
\boxed{\operatorname{per}(b)=2p.}
\]

Thus a genuine doubling creates a *single coordinate column* whose temporal period already realizes the entire new doubled period.

## Lemma 2: successive doubling columns are linearly independent over F2

Consider a nested tower of genuine doublings with exact periods

\[
p,2p,4p,\ldots,2^r p,
\]

and let `b_j` be the coordinate introduced by the `j`-th doubling. Regard all columns as periodic functions on the final period `2^r p`, repeating earlier columns as necessary.

By Lemma 1,

\[
\operatorname{per}(b_j)=2^j p.
\]

Every F2-linear combination of `b_1,...,b_{j-1}` has period dividing `2^{j-1}p`, because each summand does. But `b_j` does not have period dividing `2^{j-1}p`. Hence

\[
b_j\notin \operatorname{span}_{\mathbf F_2}\{b_1,\ldots,b_{j-1}\}.
\]

Induction gives

\[
\boxed{\dim_{\mathbf F_2}\operatorname{span}\{b_1,\ldots,b_r\}=r.}
\]

The same argument survives addition of any collection of older columns whose temporal periods divide the parent period: the newest doubling column cannot lie in their span.

## Consequence: the useful accumulation target is temporal rank, not occupancy

Runs 43--45 showed why scalar boundary-hit counts and full-cycle parity lose too much information. The present lemma identifies a quantity that *does* accumulate exactly one unit per genuine doubling, provided the corresponding coordinate histories coexist in one spacetime object:

\[
\boxed{\text{temporal column rank over }\mathbf F_2.}
\]

A chain of `r` doublings forces rank at least `r` among the introduced coordinate histories. This is stronger than merely retaining `r` nonzero events and is immune to cancellation of ordinary XOR parity.

## Important limitation

This is not yet a contradiction with finite entry. A finite state of sufficiently large width can contain arbitrarily many linearly independent temporal columns, and the existing bounded-activity theorem is phrased in terms of boundary occupancy/joint-window counts rather than F2 rank.

Therefore the missing bridge can now be stated more sharply:

> Show that bounded activity / finite entry imposes a uniform bound on the temporal F2-rank of the family of coordinate histories that can be transported into one common-origin joint window.

Alternatively, prove that the existing joint-window transport mechanism preserves enough of the coordinate histories from `r` distinct doubling passages that their rank-`r` property survives in one window; then derive an activity lower bound from rank.

## Why this is preferable to the scalar pullback target

A scalar event can be created locally under `A`, so backward event injection fails. Rank is tied to *whole temporal histories* and the strict period filtration

\[
p<2p<\cdots<2^r p.
\]

Any transport preserving these histories cannot identify the newest doubling witness with combinations of older ones, because that would lower its temporal period. Thus non-reuse is automatic once faithful simultaneous transport is established.

## Status / next target

New exact lemmas proved:

1. the fiber introduced by a genuine `p -> 2p` doubling has exact temporal period `2p`;
2. the fibers introduced by an `r`-step doubling tower have F2 temporal rank exactly `r`.

Problem 1 remains open. The next useful audit is whether the existing common-origin joint-window/transport lemmas preserve complete coordinate histories (or restrictions long enough to preserve rank), and whether their bounded-activity side yields any uniform rank bound. If neither is available, that absence is the precise blocker rather than lack of a non-reuse invariant.