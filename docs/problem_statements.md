# Rule 30 problem statements

## Coordinate and initial-condition convention

For bits `x_j(t) in {0,1}`, this repository defines Rule 30 by

```text
x_j(t+1) = x_{j-1}(t) XOR (x_j(t) OR x_{j+1}(t)).
```

The initial row is the single-black-cell seed:

```text
x_0(0) = 1,
x_j(0) = 0 for every j != 0.
```

The center sequence is `c_t = x_0(t)`, beginning with `c_0 = 1`. Every file
must state whether a requested length `N` means `c_0,...,c_(N-1)` (the standard
prefix convention) or an evolution horizon through time `N` (which has `N+1`
bits).

## Problem 1: eventual periodicity

Determine whether the center sequence is eventually periodic. Formally, does
there exist a preperiod `m >= 0` and period `p >= 1` such that

```text
c_(t+p) = c_t for every t >= m?
```

The expected conjecture is **no**. Finite period exclusions do not prove this
universal statement.

Status at repository initialization: `inconclusive`.

## Problem 2: limiting balance

Determine whether

```text
lim_(N -> infinity) (1/N) sum_(t=0)^(N-1) c_t = 1/2.
```

Define

```text
D(N) = sum_(t=0)^(N-1) (2 c_t - 1).
```

The required result is equivalent to `D(N) = o(N)`. Finite agreement with a
fair-coin heuristic is descriptive evidence only.

Status at repository initialization: `inconclusive`.

## Problem 3: exact computational complexity

This repository does not silently identify natural-language and symbolic
formulations. It tracks at least these distinct statements:

1. No exact algorithm computes `c_n` in `o(n)` time.
2. Every exact algorithm computing `c_n` requires `Omega(n)` time.
3. No exact algorithm computes `c_n` in `O(n)` time, if a published symbolic
   formula literally uses that quantifier/complexity combination.

Statements 1 and 2 require a carefully fixed model before their relationship
can be assessed; statement 3 is prima facie different because direct evolution
provides a linear-number-of-time-steps procedure under common conventions.

Every Problem 3 record must state:

- deterministic or randomized machine model;
- binary, unary, or word-sized representation of `n`;
- whether only `c_n` or the prefix through `c_n` is output;
- exactness and output convention;
- uniform versus nonuniform algorithms;
- permitted preprocessing and advice;
- bit, word, circuit-depth, or other time measure;
- word size and arithmetic cost;
- memory model and space allowance.

Failure to discover an algorithm is not a lower bound. Distinct finite
2-kernel prefixes do not establish nonautomaticity.

Status at repository initialization: `inconclusive`.
