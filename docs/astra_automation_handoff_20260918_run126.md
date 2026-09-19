# Astra automation handoff — run 126

Problem 1 remains OPEN.

Starting branch tip: `817f1fc1d643342087bc5be7a83552fecdaabc97` (`research/astra-next`). No intervening work was found after run125.

## New result

Run125 proposed an episode-dependent selector on the finite original support. The weakest geometric implementation of that idea is now ruled out.

For finite original support `S subset [L,R]`, the time-zero backward cone of any fixed bounded source-relative event window `J=[a,b]` at time `t` is `[a-t,b+t]`. Hence once

` t >= max(a-L, R-b, 0) `,

that cone contains all of `[L,R]`, so in particular

`S intersect [a-t,b+t] = S`.

Therefore every selector/observable depending only on *which original support sites lie in the ordinary backward cone* is eventually constant. Cardinality, extremal reachable support index, and the complete ordered reachable-support set cannot advance across infinitely many late births.

This is distinct from the earlier ancestry stopping fence: it shows that even set-valued causal reachability into the finite original support loses all episode discrimination at late times because the cone saturates the support.

Recorded in `proofs/informal/problem1_support_cone_selector_eventually_saturates.md`, commit `267503e991f677652562cb91b297c3cb272a8076`.

## Next target

If the finite-support selector route is continued, the selector must encode routed provenance inside the cone, not mere reachability. A concrete admissible form is a canonical crossing of a moving spacetime cut, with a theorem that its original-support label strictly advances or has uniformly bounded reuse across resetting and nonresetting passages. Do not spend another run on selectors defined only by backward-cone intersection with the initial support; this note rules them out eventually.
