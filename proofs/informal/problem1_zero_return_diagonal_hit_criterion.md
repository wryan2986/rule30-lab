# Problem 1: zero return is exactly a diagonal hit of the inverse pair map

## Context

Run 76 rewrote the unique inverse step for a nonzero column `a` as the exact predecessor equation

`b = S y xor (a or y)`, with pair update `(a,b) -> (y,a)`.

The current computational blocker is that the first tested `p=32` portal has not returned to a zero column after more than 10,000,000 exact inverse steps. This note isolates the zero-return event itself inside the pair dynamics.

## Theorem: zero predecessor iff the current adjacent columns are equal

For any cyclic words `a,b` of the same period, a solution `y=0` of

`b = S y xor (a or y)`

exists iff

\[
\boxed{b=a.}
\]

Proof: substituting `y=0` gives immediately

`b = 0 xor (a or 0) = a`.

Conversely, if `b=a`, then `y=0` satisfies the predecessor equation. If `a != 0`, the previously proved predecessor-uniqueness theorem says this is the unique predecessor.

Therefore, along every nonsingular reverse connector, the next zero column occurs exactly when the current ordered pair first reaches the diagonal

\[
\Delta=\{(a,a):a\ne0\}.
\]

Equivalently, if `T(a,b)=(P(a,b),a)` denotes the unique inverse pair map for `a != 0`, then a zero-to-zero first-return connector can be found by iterating `T` only until the first diagonal hit. There is no need to construct the following predecessor to test whether it is zero.

## Local structure at a diagonal hit

If the connector reaches `(a,a)` with `a != 0`, uniqueness gives

\[
T(a,a)=(0,a).
\]

The following inverse step is precisely the singular zero-column integration step: its first column is zero, so the equation for the next predecessor has the familiar two complementary solutions when the target has even parity.

Thus every zero-return graph vertex can be viewed equivalently as a diagonal-hit label `a`, and all branching happens one step after the diagonal hit. This separates a connector into:

1. deterministic motion in the off-diagonal state space `(a,b)` with `a != 0` and `a != b`;
2. a first hit `(a,a)`;
3. the forced zero predecessor `(0,a)`;
4. the singular integration that determines whether the zero-return vertex is unary (phase collapse) or binary (genuine branching).

This is exactly compatible with the primitive-block parity branching criterion proved earlier.

## Companion extremal identity

There is a similarly simple identity for the all-one predecessor. Substituting `y=1^p` gives

`b = 1 xor 1 = 0`,

so, whenever `a != 0`, predecessor uniqueness implies

\[
\boxed{b=0 \iff y=1^p.}
\]

Hence the coordinate hyperplane `b=0` maps in one inverse step to `(1^p,a)`. This may be useful when studying the inherited lower-period spine, where all-one zero targets occur naturally.

## Computational consequence

For the `p=32` portal search, the stopping predicate should be checked as `a == b` at the start of each unique inverse iteration. This saves the final segmented-prefix predecessor computation at every return and, more importantly, recasts the >10^7 connector problem as a **first return to the diagonal under a deterministic map on ordered word pairs**.

That reformulation may be more amenable to cycle/return-time techniques than asking directly when a generated predecessor word becomes zero. It does not by itself shorten the known >10^7 connector, so it is a structural reduction rather than a claimed asymptotic acceleration.

## Next target

Study the off-diagonal map `T` relative to the diagonal: seek either (i) a quotient/statistic whose first diagonal return can be predicted without visiting every pair, or (ii) a multi-step broadword transducer that advances `T^k` while certifying that no intermediate diagonal hit occurred.
