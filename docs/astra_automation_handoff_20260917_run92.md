# Astra automation handoff — run 92 — 2026-09-17

## Starting state

No intervening repository work was present after run 91. Starting branch tip: `07dafe1445c005019ec979f4daefa9ffe26bd29d`.

## New result

Added `proofs/informal/problem1_portal_tree_leaf_balance.md`.

Runs 90-91 imply that every genuinely new fixed-period portal component, modulo rotation, is a finite full binary tree: even-parity exact-period vertices have exactly two children, odd-parity vertices are terminal, parents are unique, and fixed-period branches cannot cycle.

Let `E` be its number of even-parity vertices and `O` its number of odd-parity vertices. Counting tree edges in two ways gives the exact identity

`O = E + 1`.

Hence `V=2E+1=2O-1`; every portal component has odd size. The primitive-necklace state bound sharpens to `E <= floor((N_prim(n)-1)/2)` and `O <= floor((N_prim(n)+1)/2)`, though this remains exponential.

## Relevance to the actual bottleneck

The useful reduction is that a finite-support resource bound only needs to control terminal odd leaves. If odd leaves inject into at most `B` resources determined by the original finite support, then automatically `O<=B`, `E<=B-1`, and the whole new full-period component has `V<=2B-1`. Thus a future birth-budget proof need not count internal portal births independently.

This is still not the missing finite-support bridge. `ASTRA_HANDOFF.md` remains authoritative: FULL must contradict finite entry for one actual survivor with its complete original fringe.

## Problem 1 status

OPEN.

## Next target

Seek an injection/charging rule from terminal odd portal leaves to finite data of the original survivor (initial support positions, fringe phases, or bounded-use entry resources). The exact leaf balance means such a leaf bound is sufficient to control the whole portal component. Do not return to fixed-period finiteness or unrestricted primitive-necklace enumeration.

Research commit: `182808079c1a042cd13387ad4503e4cc36607a0d`.
