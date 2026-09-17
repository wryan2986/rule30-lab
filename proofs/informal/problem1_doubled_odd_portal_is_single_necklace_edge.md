# Problem 1: a doubled odd portal creates one new necklace edge, not two

## Context

Run 88 characterized the integrations of a doubled odd target. If `w` has odd XOR parity and exact rotational period `r`, then the two cyclic-derivative preimages of

\[
y=ww
\]

at ambient period `2r` are complementary exact-period-`2r` antiperiodic words `x, \bar x`, satisfying

\[
S^r x=\bar x.
\]

At the word level there are two singular integrations. This note observes that modulo rotation—the natural quotient for the zero-return graph—they are the same portal, and their zero-return endpoints are also the same necklace.

## Theorem

Let `w` have odd XOR parity and exact rotational period `r`, and let `x` be either solution of

\[
D(x)=ww.
\]

Then the two complementary integrations `x` and `\bar x` define the same length-`2r` necklace. Moreover their zero-return endpoints under `rho_{2r}` define the same necklace.

### Proof

Run 88 gives antiperiodicity:

\[
S^r x=\bar x.
\]

Therefore `x` and `\bar x` differ by a cyclic rotation and hence represent the same necklace:

\[
[x]=[\bar x].
\]

Run 82 proved rotation equivariance of the boundary-to-diagonal endpoint bijection:

\[
\rho_{2r}(S^k z)=S^k\rho_{2r}(z).
\]

Using `S^r x=\bar x`,

\[
\rho_{2r}(\bar x)
=\rho_{2r}(S^r x)
=S^r\rho_{2r}(x).
\]

Thus the two endpoint words are also rotations of one another:

\[
[\rho_{2r}(x)]=[\rho_{2r}(\bar x)].
\]

So the doubled odd target `ww` has exactly one new child edge in the zero-return graph modulo rotation, despite having two complementary integrations at the word level.

## Corollary: portal necklaces correspond to odd lower-period necklaces

The derivative map sends the antiperiodic portal necklace `[x]` to the repeated odd necklace `[ww]`. Conversely, run 88 shows every exact-period-`r` odd word `w` gives an antiperiodic exact-period-`2r` integration, unique up to complement; complement is half-rotation, so it is unique as a necklace.

Hence there is a natural bijection

\[
\boxed{\{\text{odd exact-period-}r\text{ necklaces}\}
\longleftrightarrow
\{\text{antiperiodic exact-period-}2r\text{ portal necklaces}\}.}
\]

In particular, within the actual root basin, every doubled odd leaf of the inherited period-`r` basin creates exactly one new full-period portal child necklace.

## Structural consequence

This removes an apparent binary branching at every dyadic portal. The two singular integrations are not two distinct branches after quotienting by rotation; they are two representatives of one antiperiodic necklace, and their deterministic connector endpoints are likewise one necklace.

Therefore any branching in the necklace-level root basin cannot be caused merely by the complementary pair born from a doubled odd leaf. If the lower-period root basin has a single odd leaf, doubling attaches exactly one new portal child there. Whether the new full-period sector later branches must be decided by later even targets, not by the portal birth itself.

This helps explain the path-shaped root basins observed through period 10 in run 86 and sharpens the period-32 problem: for each repeated odd period-16 leaf there is one, not two, full-period-32 portal necklace to follow.

## Remaining gap

This does not bound the number of full-period parent steps before a branch returns to a repeated odd lower-period target. It reduces the number of genuinely distinct portal starts and shows that complement symmetry has already been completely quotiented out at birth. The next useful target is to determine whether a full-period portal subtree can branch after this unique first child, or whether some additional property forces the dyadic root basin itself to remain a path.