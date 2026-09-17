# Astra automation handoff — run 94 — 2026-09-17

## Starting state

No intervening repository work was present after run 93. Starting branch tip: `e0dafdf83800923c962c70332d2c7b41377aa24f`.

## New result

Added `proofs/informal/problem1_dyadic_primitive_parity_census.md`.

For dyadic `n=2^m`, every odd-weight length-`n` word is primitive: any proper rotational period `d<n` would make the word an even number `n/d` of repetitions and hence force even total weight. Therefore the exact number of odd primitive necklaces is

`N_odd(n)=2^(n-1)/n`.

Subtracting from the standard dyadic primitive-necklace count gives the exact even census

`N_even(n)=(2^(n-1)-2^(n/2))/n`.

Since every continuing vertex in a new full-period portal tree is even, while run 92 proved `O=E+1`, any such component satisfies

`E <= N_even(n)`,

`O <= N_even(n)+1`,

`V <= 2 N_even(n)+1`.

At `n=32`, this gives `E<=67,106,816`, `O<=67,106,817`, `V<=134,213,633`.

## Relevance to the actual bottleneck

This is a strict fixed-period improvement and shows that odd terminal leaves at dyadic lengths are automatically full-period; there is no proper-period odd terminal sector. It is still exponential and is not the finite-support birth budget demanded by `ASTRA_HANDOFF.md`.

The next useful theorem must connect original finite-support/fringe data to the even continuing vertices, odd terminal leaves, or the branch-prefix cylinders from run 93. Avoid further ambient necklace censuses unless they produce a support-dependent bound.

## Problem 1 status

OPEN.

Research commit: `5e882fac6b755917a6a3e433b8be838e191e2170`.
