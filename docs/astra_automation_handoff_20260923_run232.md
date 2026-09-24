# Astra automation handoff — run 232

Problem 1 remains open.

## Entry state

Branch `research/astra-next` entered at run-231 commit `62a6e0a629608043d5773ff243275730c92c19ae`. No intervening work was present.

## New result

Run 232 proves a new all-depth derivative identity for the top-coordinate orbit parity. With

\[
p_R=\bigoplus_{t=0}^{O_R-1}x_R(t),
\]

and `R>=3`,

\[
\boxed{D_{e_{R-1}}p_R
=\bigoplus_{j=0}^{O_R/2-1}x_{R-2}(2j).}
\]

The proof uses run 228's even-time formula for `p_R` and the fact that flipping initial `x_{R-1}` keeps that coordinate complementary forever while all lower coordinates remain identical.

## Consequence for plateaus

Run 231 showed that a length-three constant-order plateau forces an appropriate `p_R` to vanish identically. Run 232 now shows that this automatically forces the descended square-map parity

\[
\bigoplus_{j=0}^{O_R/2-1}x_{R-2}(2j)=0
\]

for every state.

So the hoped-for descent mechanism exists for at least one additional level: consecutive non-doublings impose not only ordinary orbit parity cancellation but also an even-time cancellation one coordinate lower.

## Next target

Do not return to explicit expansion of `T^{2^k}`. Instead, try to continue this derivative hierarchy abstractly:

1. Differentiate the descended even-time observable in `e_{R-2}`.
2. Determine whether the result is a quarter-time parity of coordinate `R-3` (possibly with a correction term).
3. More generally, seek a theorem that successive derivatives produce `2^k`-spaced orbit sums.
4. If corrections appear, classify them and check whether plateau assumptions kill them.

A successful iteration would convert long constant-order plateaus into increasingly fine dyadic cancellation identities and could finally constrain plateau length or the growth of `m_R=v_2(O_R)`.

## New research file

`proofs/informal/problem1_run232_second_top_derivative_of_orbit_parity.md`
