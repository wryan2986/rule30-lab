# Astra automation handoff — 2026-09-15 run 49

## New result

Audited run 48's exact projection-history identity against the reset/forced scan construction.

The identity

\[
A^t(x)\gg k=A^t(x\gg k)
\]

really does transport complete coordinate histories with zero loss when the state at a doubling passage is a genuine projection of the original realization.

However, the periodic comparison states in the reset-bit scan are produced using a reset/boundary prescription. They therefore cannot automatically be identified with `A^tau(x) >> k`. The projection identity does not commute away that forcing operation.

The resulting bridge is a finite-speed/cone-width problem. A sufficient condition for transferring a doubling certificate of parent period `p` back to the original realization is that the doubling-fiber coordinate remain outside the causal influence of the reset support for at least `2p` steps. Then the forced and unforced coordinate histories agree throughout one complete doubled cycle, so

\[
b(t+p)=1\oplus b(t)
\]

holds for a literal column of the original spacetime diagram.

This also identifies a precise failure mode: agreement at the doubling source time is insufficient if the reset boundary can enter the fiber's causal cone before `2p` steps elapse.

## File added

- `proofs/informal/problem1_projection_vs_forced_state_audit.md`

## Next target

Extract from the exact reset/gate/source definitions:

1. the spatial coordinate of the fiber bit responsible for each genuine doubling;
2. the support/location of the imposed reset modification;
3. their separation as a function of the parent period `p` and scan depth;
4. whether that separation dominates the `2p`-step causal width for infinitely many late doubling passages.

If yes, the antiperiodic half-density certificates become genuine columns of the original common-origin realization and can feed the run-47 activity budget. If no, record the resulting inequality as a concrete obstruction and return to structured gate/source transport.

Problem 1 remains open.
