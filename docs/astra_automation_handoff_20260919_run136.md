# Astra automation handoff — 2026-09-19 — run 136

Problem 1 remains OPEN.

Starting branch tip was `b280cd49511ed3a135c49ae17f6f795541c2094c`; no intervening work was present after run135.

## New stopping fence: FULL center trace alone has unlimited finite realizability

Run135 identified the desired missing theorem as finite-range plus bounded reuse for the distinguished source-relative `011` events. This run proves that no such finite obstruction can come from FULL's center trace alone.

Rule 30 is left-permutive:

    f(l,c,r) = l XOR (c OR r).

For any finite desired center word `c_0,...,c_T`, after fixing the nonnegative initial side, choose initial cells `-1,-2,...,-T` successively. At stage `t`, the new extreme-left bit `-t` is outside all earlier center cones and enters the time-`t` center through a chain of left arguments. Left-permutivity makes the time-`t` center bijective in that bit. Thus exactly one choice realizes the next desired center symbol without changing the previous prefix.

Consequently every finite binary center word, in particular arbitrarily long prefixes of FULL's alternating `1010...` center trace, is realized by some finite-support initial row. A small exact sanity enumeration through time 8 agreed with the induction.

This is a stopping fence, not a solution: it does not realize an infinite FULL survivor and does not preserve the complete cyclic-source/right-fringe constraints.

## Next target

Any bounded-reuse/birth-budget theorem must explicitly consume the complete cyclic-source/fringe hypotheses; center alternation plus generic ancestry is insufficient at every finite depth. The next useful question is whether the complete source/gate/right-fringe constraints fix the successive extreme-left bits used by the left-permutive construction, or whether enough freedom remains to realize arbitrarily many distinguished `011` source events. Avoid another center-only ancestry argument.

New note: `proofs/informal/problem1_arbitrary_finite_center_trace_by_left_permutivity.md`.
Research commit: `447a79d5c92a9e3ac402e232e6a275739a6a10b9`.
