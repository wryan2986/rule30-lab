# Problem 1: portal-tree axioms alone cannot yield an original-support birth bound

## Purpose

Runs 85--94 extracted a useful abstract structure for a genuinely new exact-period dyadic portal component: unique parent/no mergers, a single portal entry, exact-period preservation until the portal boundary, binary branching at every even full-period vertex, odd full-period terminal leaves, finiteness at each fixed period, leaf balance `O=E+1`, Kraft conservation, and the exact ambient parity census.

This note records a limitation of that package. Those facts, by themselves, cannot imply the support-dependent birth bound required by `ASTRA_HANDOFF.md`. A new ingredient coupling a portal branch to the actual finite survivor/fringe is logically necessary.

## Abstract countermodels of arbitrarily large depth

Let `n=2^m`. The exact primitive-necklace parity census from run 94 is

`N_odd(n)=2^(n-1)/n`,

`N_even(n)=(2^(n-1)-2^(n/2))/n`.

Consider only the structural axioms established for a new full-period portal component. A complete rooted binary tree of depth `d` has

- `E=2^d-1` even internal vertices,
- `O=2^d` odd terminal leaves,
- `O=E+1`,
- Kraft sum `O*2^(-d)=1`,
- unique parents and no mergers.

Thus whenever

`2^d-1 <= N_even(n)`

and

`2^d <= N_odd(n)`,

we may injectively label the internal vertices by distinct even primitive necklaces and the leaves by distinct odd primitive necklaces. The resulting labelled abstract tree satisfies every counting, parity, tree, and Kraft constraint proved in runs 90--94. (This is a logical countermodel to deduction from those constraints; it is not claimed to be the actual Rule-30 parent map.)

For every `m>=3`, take `n=2^m` and `d=m`. Then

`2^d = 2^m = n`,

whereas

`N_odd(n)=2^(n-1)/n`

and

`N_even(n)=(2^(n-1)-2^(n/2))/n`.

Both counts exceed `n` for all sufficiently small cases directly checked below and then overwhelmingly thereafter. In fact for `n>=8`,

`N_odd(n)>=2^(7)/8=16>=8`,

and `N_even(8)=14>=7`; both functions then grow much faster than `n`. Therefore the run-90--94 axioms admit abstract portal trees of depth at least

`d=m=log2(n)`

for arbitrarily large dyadic periods.

A much stronger depth is compatible with the same census. The maximum complete-tree depth allowed by ambient counts is

`d_max(n)=min(floor(log2(N_even(n)+1)), floor(log2 N_odd(n)))`,

which is asymptotic to

`n-log2(n)-1`.

For example, at `n=32`, `N_even=67,106,816` and `N_odd=67,108,864`, so a complete binary tree of depth 25 already satisfies all of the abstract constraints (`E=33,554,431`, `O=33,554,432`).

## Consequence for the current proof strategy

No argument using only the following data can produce a bound controlled by the original finite support width `L`:

1. fixed-period finiteness;
2. unique parent/no merger;
3. even vertices branch twice and odd vertices terminate;
4. `O=E+1`;
5. Kraft conservation;
6. primitive/even/odd necklace counts;
7. period nonincrease and period-halving at doubled odd targets.

These statements contain no coupling to `L`, and they have models with unbounded branch depth as `n` grows. Further refinements that only count ambient necklaces, parity classes, or abstract binary-tree shapes cannot close the authoritative birth-budget gap.

This does **not** show that actual Rule-30 portal trees attain those depths. It shows only that the already-proved abstract portal package cannot rule them out.

## What new information would suffice

A useful next lemma must break this countermodel by importing survivor-specific data. Examples include:

- a map from each branch prefix to a distinct finite center/fringe prefix of the actual survivor;
- a bound on how many portal branch decisions one original support position can witness;
- a monotone quantity attached jointly to `(portal state, actual fringe phase)` rather than to the portal necklace alone;
- a weighted charging rule assigning disjoint terminal cylinders to finitely many original-support resources.

This aligns with the older `ASTRA_HANDOFF.md` bottleneck: FULL for one actual survivor with its complete original finite right fringe must be contradicted using a finite-support resource. The portal theory is useful only once coupled back to that survivor-specific information.

## Status

Problem 1 remains open. This note is a strategy no-go/result: it rules out treating further ambient portal-tree counting as a route to the required support-dependent bound unless a new fringe/support coupling is added.
