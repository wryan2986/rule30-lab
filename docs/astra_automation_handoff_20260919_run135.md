# Astra automation handoff — 2026-09-19 — run 135

Problem 1 remains OPEN.

Starting branch tip was `7e36a3a201205bbb9faf6af1f26f109de2f796e9`; no intervening work was present after run134.

## New stopping fence

Run134 suggested reconnecting distinguished source-relative `011` events state-dependently to the finite initial 1-support. Such reconnection always exists, but this by itself is vacuous as a finite budget.

Rule 30's output-1 neighborhoods are exactly

    001, 010, 011, 100.

Each contains at least one 1-parent. Hence every later 1-cell admits a backward path consisting entirely of 1-cells and ending at an initial 1-site. At `011`, sensitivity fails, but ordinary 1-ancestry does not: one may choose either 1-parent.

The obstruction is reuse. For the single-seed initial condition there is only one initial 1-site, so every later 1-cell—and therefore every generic `011` event—must ultimately charge to that same initial 1. Earlier branch computation found thousands of `011` events by time 199. Thus finite range of an ancestry label does not imply a finite event count.

Together with run134 there is now a clean two-sided fence:

- unconditional sensitive routing: strict/nonreused labels, but in an infinite zero tail;
- ordinary 1-ancestry routing: labels in the finite initial 1-support, but potentially unbounded reuse.

## Next target

Do not spend a run merely constructing a route from distinguished `011` events to initial 1-sites; that is automatic. The missing theorem must combine finite range with bounded reuse. A concrete target is: under FULL plus the cyclic-source constraints, prove that each initial 1-site can terminate only finitely (ideally uniformly boundedly) many distinguished source-relative `011` ancestry routes, or identify a different bounded object with the same property.

New note: `proofs/informal/problem1_initial_one_ancestry_exists_but_has_unbounded_generic_reuse.md`.
