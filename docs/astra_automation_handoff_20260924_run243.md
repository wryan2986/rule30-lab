# Astra automation handoff — run 243 — 2026-09-24

Problem 1 remains open.

## Entry state

The branch entered at run 242 commit `e702328b7555ca79dcc93851502d3145eed14e2e`; there was no intervening work.

Run 242 left one immediate blocker: its exact half-difference upper bound after a preceding doubling is sharp only if a state selecting the complementary branch at coordinate `r-1` can simultaneously maximize the complexity of coordinate `r-2`.

## New result

That compatibility is automatic after **two consecutive order doublings**.

Assume

`O_{r-3}=Q`, `O_{r-2}=2Q=P`, `O_{r-1}=2P=4Q`.

Take any state witnessing the second doubling.  Its lower prefix through `r-2` must have full period `P`; otherwise the binary skew extension at `r-1` could have period at most `P`, not `2P`.

Since the prefix through `r-3` has order `Q`, full period `P=2Q` at `r-2` forces the coordinate-`r-2` word to have complementary `Q`-halves.  Games–Chan therefore gives

`L(X_{r-2}^{[P]})=Q+1`,

which is exactly the maximal complexity at that doubling level.  Thus every witness for the second doubling is already a compatible lower maximizer.

If the next step is a plateau, `O_r=O_{r-1}=4Q`, run 242's half-difference identity and cyclic integration now give an exact formula with no computational witness needed:

`L_r(4Q)=2Q+(Q+1)+1=3Q+2`.

For `O_5=8, O_6=16, O_7=32, O_8=32`, this proves directly

`L_8(32)=26`.

Small exhaustive checks agree: at both observed consecutive-doubling runs (`2->4->8` and `8->16->32`), every second-doubling witness has the predicted maximal lower complexity.

## Files added

- `proofs/informal/problem1_run243_compatibility_after_two_consecutive_doublings.md`
- this handoff

## Next target

Do not revisit compatibility for two consecutive doublings; it is now proved.  Move to order-decision patterns containing an intervening plateau, especially `double / plateau / double`, or longer plateau runs.  Derive the corresponding dyadic half-difference/linear-complexity recursion and determine whether later doubling witnesses impose a similarly rigid complexity condition on lower coordinates.