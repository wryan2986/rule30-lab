# Problem 1 run 219 — constant-period cycle columns form a finite-state level automaton

Problem 1 remains open.

## Setup

Let
\[
q_n=2^n x,\qquad a_n=\tau(q_n),\qquad P_n=\pi(q_n).
\]
Write the adjacent-level defect by
\[
A^k(q_n)=2A^k(q_{n-1})+d_n(k),\qquad d_n(k)\in\{0,1\}.
\]
Runs 207 and 215 established the exact defect update and, for n sufficiently above the base boundary,
\[
d_n(k+1)=d_{n-2}(k)\oplus(d_{n-1}(k)\lor d_n(k)).
\]

Consider a maximal interval of tower levels on which the eventual period is a fixed value P. For every level n in the interior of that interval, restrict d_n(k) to the eventual P-cycle and record one full period as a cyclic binary word
\[
D_n=(d_n(0),\ldots,d_n(P-1))\in\{0,1\}^P,
\]
with all columns aligned to the same time phase via the exact projection tower.

## Exact finite-state result

For fixed P, the next cycle column D_n is uniquely determined by the ordered pair (D_{n-2},D_{n-1}) whenever the lift preserves period P and the lower cycle contains a reset.

Reason: at each phase k mod P, the recurrence is
\[
d_n(k+1)=d_{n-2}(k)\oplus(d_{n-1}(k)\lor d_n(k)).
\]
Thus, for fixed forcing words U=D_{n-2}, V=D_{n-1}, one traversal of the P phases defines a one-bit monodromy map F_{U,V}:{0,1}\to{0,1}. In a period-preserving lift whose lower cycle contains a reset, the one-bit automaton has a reset, so the periodic defect phase is unique. Choosing that unique fixed phase and iterating the recurrence around the cycle uniquely produces D_n.

Consequently there is a deterministic partial map
\[
\boxed{T_P:(D_{n-2},D_{n-1})\mapsto(D_{n-1},D_n)}
\]
on at most 2^{2P} ordered pairs of P-bit words.

Therefore:

**Finite-state epoch theorem.** If a fixed finite origin x has an infinite tail of tower levels with constant eventual period P, then the aligned eventual-cycle defect columns are eventually periodic in the level direction n, with preperiod plus period bounded crudely by 2^{2P} states.

More generally, every finite constant-P epoch is a finite orbit segment of this same deterministic state graph, except at its boundary where a period change occurs.

## Why this is useful

Run 218 showed that each positive preperiod increment inside a constant-P epoch is at most P, but that did not control cumulative reuse. The present result says that the *eventual-cycle geometry* being reused is not arbitrary across levels: for fixed P it evolves in a finite deterministic state space.

This sharply reduces the proposed epoch theorem. Any proof that an infinite constant-P tail is impossible, or harmless for residence surplus, can in principle be reduced to excluding recurrent states/cycles of T_P that are compatible with the stopping-time entry phases of one common finite origin.

## Important limitation

This does **not** yet bound the cumulative preperiod gain. The increment a_n-a_{n-1} depends on whether the actual defect at cycle entry matches the unique periodic defect phase. The eventual-cycle pair (D_{n-2},D_{n-1}) does not by itself encode that transient entry bit. Therefore it would be invalid to conclude that the increment sequence is eventually periodic merely from the finite-state theorem above.

The missing variable is the stopping-curve / entry-phase state. A useful next step is to augment T_P with the minimum transient information needed to decide the mismatch at k=a_{n-1}, and determine whether that augmented state is still finite for fixed P.

## Diagnostic note

For x=1, run 218 already gives very long constant-period epochs (P=8 from levels 29 through 399, and P=16 from 400 through at least 1000), so any hoped-for small bound on epoch length is false. The finite-state reduction is preferable to trying to bound epoch length directly.
