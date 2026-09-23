# Astra automation handoff — 2026-09-23 run 227

Problem 1 remains open.

## Repository state entering this run

`research/astra-next` was at `47bb1b2a6d13b13ca287d34b70a5161b8a8e8401` (run 226). No intervening work was present.

Run 226 proposed studying `p_R(x)=XOR_{t=0}^{O_R-1} x_R(t)` jointly with the doubling cocycle `g_R`.

## New all-depth result

For every `R>=1`,

\[
\boxed{p_R(x\oplus e_R)=p_R(x).}
\]

The proof pairs trajectories differing only in the newest coordinate. Their lower coordinates remain identical and their top coordinates remain complementary. XORing that difference over `O_R` steps gives `O_R mod 2 = 0`, since run 224 proved `O_R` is an even power of two for `R>=1`.

Therefore `p_R` factors through projection to width `R-1`: it carries no dependence on the newest state bit.

Full proof: `proofs/informal/problem1_run227_top_coordinate_orbit_parity_descends.md`.

## Dead-end clarification

XORing the top-coordinate update over a full order yields `0=(q_R mod 2) g_{R-1}`. This is not a new restriction: for `q_R=1` it simply restates that the previous extension did not double; for `q_R=2` it is tautological. Do not spend another run treating this telescoping identity as independent leverage.

## Finite diagnostic

Small-width enumeration: `p_1,p_2` nonconstant; `p_3,p_4` identically zero; `p_5` nonconstant; `p_6,p_7` identically zero. Treat this only as finite evidence.

## Next target

Since `p_R` descends one width and run 226 showed the top-bit derivative of `g_R` also descends to lower orbit parity, derive the effect of flipping `e_{R-1}` (and then lower coordinates) on `p_R` and `g_R`. The useful goal is a finite recursive description of these Boolean observables under successive coordinate derivatives, not another raw order table. If that recursion closes, use it to prove structure in the doubling word and bound `m_R`.
