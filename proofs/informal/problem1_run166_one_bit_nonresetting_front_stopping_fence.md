# Run 166 — one-bit nonresetting source: local core data do not determine the next original-cut front

Status: stopping-fence / reduction. Problem 1 remains OPEN.

## Setup

Continue from run165. Let `t` be a sufficiently late even ONE-BIT gate-u nonresetting source. The established classification in `problem1_nonresetting_core_returns.md` and `problem1_full_driver_exit_phase.md` gives

- actual source delay `tau(Y_t)=1`;
- `x=Y_t`, `z=cyc(x)`, with `x=z XOR 1=z+1` and `A x=A z`;
- actual low bits `r_0..r_3=(1,1,1,0)`;
- the SAME original global E-shadow has center 0 and selected right pair `(hat r_1,hat r_2)=(1,1)`;
- bits >=2 agree between actual and shadow at the source.

Thus at the source the actual and original shadow differ at position 0, while their entire nonnegative right cuts become identical after one A update:

    A x = A z.

This equality is exact and uses the full right cut, not merely the displayed low cells.

## Consequence for the proposed run165 route

The two-bit argument succeeded because its already-derived original-cut itinerary supplied several successive exact values of the GLOBAL first-discrepancy position `m(u)=J(u)-u`; those values could then be checked against local Rule-30 evolution of the same original E-shadow.

For the one-bit source, the existing classification supplies only the cyclicization delay `tau(Y_t)=1`. It does NOT supply the next original-cut residence time `s_j`, hence does not determine `J(t+1)` or `m(t+1)` after the exact healing `A x=A z` of the right cut.

In particular, it is invalid to identify

    tau(Y_t)=1

with a one-step residence of the global original-cut discrepancy front. `tau` measures delay to the cyclic core; `m` is determined by the original finite-support E-shadow / characteristic stopping times. Run165's collision cannot therefore be transplanted by simply replacing the two-bit source delay 2 by the one-bit source delay 1.

## Exact bottleneck

At time `t+1`, the source's complete right cut has healed against its cyclic core. Any later discrepancy entering the right cut is therefore controlled by the ORIGINAL-CUT ancestry from the left / the next characteristic stopping time, information absent from the one-bit core-return theorem.

So the next useful theorem must be one of:

1. an original-cut stopping-time identity for a late one-bit gate-u nonresetting source, giving at least `J(t+1)` (preferably a short residence itinerary); or
2. a direct relation between the healed equality `A x=A z` and the global stopping sequence `s_j` strong enough to bound or fix `m(t+1)`.

Without such a bridge, further evolution of the local `(x,z)` pair is tautological: once `A x=A z`, their future A-images remain equal and cannot reveal where the next GLOBAL discrepancy enters.

## Dead end recorded

Do not infer an original-cut itinerary from `tau=1`, and do not continue a local right-tail simulation after `A x=A z` expecting it to reconstruct the global front. The missing datum is the next original characteristic whose stopping time exceeds the physical time, not another local driver bit.

This is a genuine distinction from the eliminated two-bit case and narrows the next search to existing stopping-time / finite-entry lemmas rather than core-only calculations.
