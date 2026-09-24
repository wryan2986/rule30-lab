# Astra automation handoff — run 238 — 2026-09-24

Problem 1 remains open.

## Entry state

Branch `research/astra-next` entered at run-237 tip `dbd85866fc28d67d72a8b489110db8d0a965b8fb`. No intervening branch work was present.

Run 237 proved the exact Pascal-mask periodic folding threshold `P_*(k)=2^{ceil(log2(N-k))}` and proposed the separation conjecture that `O_{r-1}>=P_*(k)` should force some state with nonzero pairing `S_{A^k1_N}[f_r]`.

## New result

Added `proofs/informal/problem1_run238_separation_conjecture_counterexamples.md`.

The separation conjecture is false.

For `k=0`, `N=O_{r-1}`, the recurrence gives

\[
S_{1_N}[f_r]\equiv0 \iff O_r=O_{r-1}.
\]

But `P_*(0)=N=O_{r-1}`, so every non-doubling step is a counterexample. The first interior example is `O_4=O_5=8`, hence `(r,N,k)=(5,8,0)` has threshold met exactly but the forcing pairing vanishes identically.

Exhaustive enumeration of the triangular map through width 9 reproduced

`O_0,...,O_9 = 1,2,2,4,8,8,16,32,32,64`

and found a genuinely nonzero-k counterexample:

\[
(r,N,k,P_*)=(8,32,1,32),
\]

with `O_7=32` but `S_{A1_32}[f_8] identically 0` over all lower-prefix initial states. Larger-N lifted variants also occur and are recorded in the proof note.

Thus run 237's folding threshold is necessary but not sufficient. There are genuine Rule-30-specific **excess annihilations** after automatic periodic cancellation has been factored out.

## Next target

Do not try to prove the run-237 separation conjecture.

Classify excess annihilation

\[
E(r,N,k): P_*(k)<=O_{r-1} \text{ and } S_{A^k1_N}[f_r]\equiv0,
\]

preferably with `N=O_{r-1}` or after reducing to the minimal effective period so lifted duplicates are removed.

First priority: derive an exact interpretation of `k=1`. Determine whether the `(r,N)=(8,32)` cancellation follows from a known orbit-parity/plateau identity (runs 231–235) or is a new independent condition. Then census minimal excess-annihilation triples at larger feasible widths.
