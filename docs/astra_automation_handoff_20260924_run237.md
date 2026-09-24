# Astra automation handoff — run 237 — 2026-09-24

Problem 1 remains open.

## Entry state

Branch `research/astra-next` entered at run-236 tip `7e19c8bc0820b5908d2f16eb9134be542398225d`. No intervening branch work was present.

Run 236 proved that a three-level plateau `O_{s-1}=O_s=O_{s+1}=N` implies `s<=2N-3`, using the terminal even Pascal mask `A^{N-2}1_N=(1,1,0,...)`. It proposed classifying earlier masks.

## New result

Added:

- `proofs/informal/problem1_run237_pascal_mask_period_folding.md`

For `N=2^M`, `w=A^k1_N`, and power-of-two `P|N`, let `F_Pw` be XOR folding of the length-`N` mask modulo `P`. The exact smallest period detected by `w` is

\[
P_*(k)=2^{\lceil\log_2(N-k)\rceil}.
\]

Precisely,

\[
F_P(A^k1_N)=0 \iff P<P_*(k)
\]

for power-of-two divisors `P` of `N` (within `0<=k<=N-2`). Proof uses Lucas' theorem: after fixing a residue modulo `P=2^p`, the parity of admissible high-bit assignments is odd iff all high bits of `k` are 1, equivalently `k>=N-P`.

Since `f_r(t)=x_{r-1}(t) OR x_{r-2}(t)` has period dividing `O_{r-1}`, this gives the automatic-annihilation criterion

\[
O_{r-1}<P_*(k) \Longrightarrow S_{A^k1_N}[f_r]\equiv0.
\]

Thus earlier Pascal masks cannot be expected to contradict identities before the lower-prefix order reaches their folding threshold. In particular every `k<N/2` has threshold `N`.

Direct folding checks for `N=8,16,32` agree. Exhaustive state enumeration for feasible widths at `N=4,8,16` also found that the first non-identically-zero forcing pairing occurs exactly when `O_{r-1}` reaches `P_*(k)`. That equality is currently computational evidence, not an all-depth theorem.

## Next target

Prove or refute the separation conjecture:

> If `O_{r-1}>=P_*(k)`, then there exists an initial state with `S_{A^k1_N}[f_r]=1`.

If true, Pascal-mask annihilation is classified exactly by the prefix order. Combining this with run 235's descent should convert a three-level plateau into explicit inequalities among earlier `O_j`, rather than merely the coarse positional bound from run 236.

If false, record the smallest counterexample: it would expose a genuinely nonlinear cancellation not explained by periodic folding and would become the next structural target.

Do not spend another run deriving individual Pascal masks; run 234 already gives them in closed form. Do not interpret vanishing below `P_*(k)` as Rule-30-specific cancellation; run 237 shows it is automatic for every periodic sequence of that order.
