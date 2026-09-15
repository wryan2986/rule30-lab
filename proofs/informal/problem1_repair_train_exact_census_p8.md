# Exact same-period repair-train census through period 8

Status: exact finite computation; new lower bound and empirical scaling clue. Problem 1 remains open.

## Purpose

Run 35 reduced every alternating same-period repair train at fixed period `p` to a nonrepeating segment of the fringe permutation

\[
F_p(R)=T^2(R)\pmod{2^{2p}}.
\]

It gave the crude unconditional bound `N_fixed <= 3*4^(p-1)` and proposed computing exact maxima for modest periods. This note carries out that census using the finite-extension graph for `A^p(x)=x`, so only fringes that extend to genuine finite fixed words are counted.

The reproducer is `scripts/check_repair_train_maxima.py`.

## Definition measured

For every finite exact-period-`p` state `z`, measure the maximal initial sequence

\[
z,\ T^2z,\ T^4z,\ldots,T^{2(N-1)}z
\]

such that every displayed node is `A^p`-fixed and each intervening odd physical row is not `A^p`-fixed. Thus `N` is the number of fixed nodes in the alternating fixed/collision/fixed repair train starting at `z`.

The finite-extension graph is exact: a `2p`-bit low state is retained iff it has an upward extension terminating at zero and satisfying every local `A^p(x)=x` constraint. The unique extension is then reconstructed and checked directly.

## Exact maxima

The census gives:

| p | number of exact-p finite fixed states | maximum alternating train |
|---|---:|---:|
| 1 | 3 | 1 |
| 2 | 10 | 1 |
| 3 | 0 | 0 |
| 4 | 84 | 3 |
| 5 | 0 | 0 |
| 6 | 0 | 0 |
| 7 | 0 | 0 |
| 8 | 2968 | 15 |

For the nontrivial power-of-two periods this is

\[
M_2=1,\qquad M_4=3,\qquad M_8=15.
\]

These three values fit the striking law

\[
\boxed{M_p=2^{p/2}-1\quad(p=2,4,8),}
\]

but this is only an empirical conjecture at present. In particular, the census does **not** justify extrapolating it to `p=16`.

The period-8 result improves run 34's 13-node witness: the true exact maximum at `p=8` is at least and in fact exactly 15 among all finite `A^8`-fixed states.

## Two exact period-8 maximizers

There are exactly two starting states attaining 15 fixed nodes.

One is

\[
z=36088633440115177043812706397341401,
\]

with fringe/gap sequence

```
(22681,1), (21521,1), (21897,1), (21825,1), (21849,1),
(21841,1), (21833,1), (21761,1), (21785,1), (21649,1),
(20489,1), (20673,1), (23769,1), (31185,1), (45769,0).
```

The other is

\[
z=16255307958207225759917725669098125,
\]

with

```
(36621,0), (22493,1), (22765,1), (21885,1), (21901,1),
(21853,1), (21869,1), (22013,1), (22029,1), (22237,1),
(24557,1), (24701,1), (26253,1), (20061,1), (7277,3).
```

The first maximizer is especially suggestive: fourteen successive repaired fixed nodes have corridor `G=1`, followed by one `G=0` node. Thus long trains are not being sustained by repeated excursions to larger corridors; the short-gap `G=1` dynamics alone can support essentially the whole train.

## Additional exact period-spectrum observation

The same extension census gives the following period spectra among nonzero finite `A^p`-fixed states:

- `p=1`: exact period 1 only (3 states);
- `p=2`: periods 1 and 2 (3 and 10 states);
- `p=3`: period 1 only;
- `p=4`: periods 1,2,4 (3,10,84 states);
- `p=5`: period 1 only;
- `p=6`: periods 1,2 only;
- `p=7`: period 1 only;
- `p=8`: periods 1,2,4,8 (3,10,84,2968 states).

So through `p=8`, every observed nontrivial finite cycle period is a power of two. This is potentially more important globally than the train-length fit, but it is recorded only as a computational observation here. A theorem that all finite `A`-cycle periods are powers of two would sharply constrain the period-change escape mechanism left open by the FULL/common-origin argument.

## Interpretation

The crude `3*4^(p-1)` run-35 bound is very far from sharp at `p=8` (`15` versus `49152`). However, the exact maxima `1,3,15` do **not** currently support a polynomial-in-`p` conjecture; the simplest fit is exponential in `p/2`. Therefore the proposed route of obtaining a small polynomial same-period residence bound has no evidence yet.

The stronger new clue is the period spectrum. If the power-of-two phenomenon can be proved structurally, then a survivor changing exact period cannot wander through arbitrary periods: nontrivial period increases would have to move among powers of two. That is a concrete possible bridge from the local repair theory to global period-growth accounting.

## Next targets

1. Prove or disprove that every finite periodic point of `A` has exact period a power of two. The exact spectra above make this a sharper target than merely extending the repair census.
2. Analyze the `G=1` restriction of `F_p`; the 15-node maximizer shows it is the main source of long repair trains at `p=8`.
3. If feasible, build a more memory-efficient finite-extension/transfer computation for `p=16` to test both `M_16=255` and the power-of-two period hypothesis without allocating the naive `2^(32)` state graph.
