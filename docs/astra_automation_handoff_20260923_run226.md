# Astra automation handoff — 2026-09-23 run 226

Problem 1 remains open.

## Repository state entering this run

`research/astra-next` was at `7b285c5994bf1f08e3335c59dfe80dee047ce71b` (run 225). No intervening work was present.

Run 225 proved `O_{R+1}/O_R` is always 1 or 2 and reduced doubling to the orbit parity of the extension cocycle `f_R=x_R OR x_{R-1}`.

## New all-depth identity

For

\[
g_R(x)=\bigoplus_{t=0}^{O_R-1}(x_R(t)\lor x_{R-1}(t)),
\]

let `e_R` flip only the newest coordinate. The paired trajectories stay complementary in coordinate `R` and identical below. Hence, for `R>=1`,

\[
\boxed{g_R(x)\oplus g_R(x\oplus e_R)=\bigoplus_{t=0}^{O_R-1}x_{R-1}(t).}
\]

Writing `q_R=O_R/O_{R-1}` gives the important consequence

\[
\boxed{q_R=2 \implies g_R(x)=g_R(x\oplus e_R)\ \forall x.}
\]

So immediately after an order doubling, the next doubling cocycle is completely insensitive to the newest coordinate. If `q_R=1`, its top-coordinate sensitivity is exactly a lower-width orbit parity.

Full proof: `proofs/informal/problem1_run226_cocycle_top_flip_identity.md`.

## Consequence

The width-by-width doubling tests are not independent. Their top-coordinate dependence recursively descends to lower orbit parity, and a preceding doubling annihilates that dependence. This is structural progress toward a recursion for the doubling word, but does not yet imply sublinear growth of `m_R` because dependence through lower coordinates remains possible.

## Next target

Define `p_R(x)=XOR_{t=0}^{O_R-1} x_R(t)` and derive a recursion coupling `(g_R,p_R)`, especially under projection and top-bit flip. Try to turn the doubling/non-doubling sequence into a provable finite-state or substitution process. Do not infer a closed formula solely from the finite order table.