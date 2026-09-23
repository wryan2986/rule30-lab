# Astra automation handoff — run 219

Problem 1 remains OPEN.

## New exact result

Inside a constant-period epoch P, align the eventual-cycle adjacent defect columns
\[
D_n=(d_n(k))_{k\bmod P}\in\{0,1\}^P.
\]
Using the run-215 recurrence
\[
d_n(k+1)=d_{n-2}(k)\oplus(d_{n-1}(k)\lor d_n(k)),
\]
and the reset uniqueness from the one-bit lift analysis, a period-preserving lift with a reset has a unique periodic defect column D_n once (D_{n-2},D_{n-1}) is fixed.

Hence, for fixed P, the aligned cycle geometry evolves by a deterministic partial finite-state map
\[
T_P:(D_{n-2},D_{n-1})\mapsto(D_{n-1},D_n)
\]
on at most 2^{2P} states.

Therefore, if a fixed finite origin ever had an infinite tail with constant eventual period P, its eventual-cycle defect columns would be eventually periodic in tower level n.

## Limitation

This does not yet make the preperiod increments eventually periodic. The mismatch at k=a_{n-1} depends on the actual transient entry bit, which is not encoded by the eventual-cycle pair alone. Do not claim a cumulative epoch bound from the finite-state cycle map.

## Strategic update

Run 218 proposed an epoch theorem. The cycle component of such a theorem is now finite-state. The next target is to augment T_P with the smallest stopping-curve / entry-phase state needed to decide whether the new defect is matched at k=a_{n-1}. If that augmented state is finite for fixed P, recurrent components can be classified by their mean residence increment; if it is not finite, identify exactly which transient ancestry escapes the finite-state reduction.

Detailed proof: `proofs/informal/problem1_run219_constant_period_cycle_column_finite_state.md`.
