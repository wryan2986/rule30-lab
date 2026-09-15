# Exact finite cycle period by bitlength through period 8

Status: exact finite-extension computation; structural computational result. Problem 1 remains open.

## Motivation

Run 36 observed that all finite periodic points found through `Fix(A^8)` have power-of-two exact period. Re-examining the same exact finite-extension census by **bitlength**, rather than only by period, reveals substantially more structure.

Recall

\[
A(x)=T(x)\gg2,\qquad T(x)=x\oplus((x\ll1)\lor(x\ll2)).
\]

For every nonzero finite word, `A` preserves bitlength, so each bitlength is an invariant finite dynamical system.

## Exact census

Using the exact extension graph already used in `scripts/check_repair_train_maxima.py`, every finite state in `Fix(A^p)` was reconstructed for `p=1,2,4,8`, its exact period computed, and the states grouped by bitlength.

The result is:

| bitlength `n` | exact period | periodic states at each `n` |
|---:|---:|---:|
| 1..3 | 1 | 1 |
| 4..8 | 2 | 2 |
| 9..29 | 4 | 4 |
| 30..400 | 8 | 8 |

There are **no gaps and no multiplicities beyond one cycle** in these ranges. Equivalently, for every bitlength `n<=400`, the finite periodic points of `A` at that bitlength form exactly one cycle, whose period is

\[
1,2,4,8
\]

on the four consecutive intervals above.

This exactly explains the run-36 state counts:

- period 1: `3 = 3*1` states, one fixed point at each length 1..3;
- exact period 2: `10 = 5*2` states, one 2-cycle at each length 4..8;
- exact period 4: `84 = 21*4` states, one 4-cycle at each length 9..29;
- exact period 8: `2968 = 371*8` states, one 8-cycle at each length 30..400.

Thus the previously mysterious counts `3,10,84,2968` are not arbitrary: each is `period * number of consecutive bitlengths carrying that period`.

## Why this is stronger than the period-spectrum observation

The run-36 power-of-two observation could in principle have arisen from many unrelated cycles. Instead, through bitlength 400 the data say something much more rigid:

> At each invariant bitlength there is exactly one finite periodic orbit, and its period is a power of two.

A theorem of this form would imply the power-of-two-period conjecture immediately. It also converts period changes into a question about the threshold lengths at which the unique cycle doubles its period.

The observed threshold starts are

\[
1,4,9,30,401.
\]

The next threshold `401` is exact in the following sense: period 8 occurs at every length 30 through 400, while no period <=8 periodic point exists at length 401. This does **not** prove that length 401 has period 16, because `Fix(A^16)` has not been enumerated.

## Independent small-state sanity check

Direct forward dynamics on all words of small fixed bitlength agrees with the extension census: each tested bitlength has one eventual cycle, with periods 1 on lengths 1..3, 2 on 4..8, and 4 beginning at 9. This check is not needed for exactness of the extension census, but supports the interpretation that the reconstructed periodic orbit is the unique attractor cycle at each length.

## New target

The proof target should be strengthened from merely

> every finite periodic point has power-of-two period

to

> for each bitlength `n`, `A` has exactly one periodic orbit on the `n`-bit words, and that orbit has power-of-two period.

A promising route is to prove coalescence/contraction for two `n`-bit words under `A` in a one-sided disagreement metric. Since the top bit is fixed and the local rule is

\[
(Ax)_i=x_{i+2}\oplus(x_{i+1}\lor x_i),
\]

a comparison from the leading edge may show that all `n`-bit states eventually synchronize up to phase on a unique cycle. If uniqueness can be proved first, the remaining task is to explain why that cycle length is a power of two.

The threshold sequence `1,4,9,30,401` should also be compared against any existing leading-edge/finite-entry recurrences in the repository before attempting a p=16 brute-force computation.