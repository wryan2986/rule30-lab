# Astra automation handoff — run 59

Problem 1 remains open.

This run continued the reverse-basin program from run 58. No intervening repository work was present before the run.

New result: after the first reverse branch at `q_(N-9)`, each branch enters a rigid period-four subsystem. The immediate predecessor is uniquely `1^p`; subsequent predecessor equations remain period-four for many layers.

Exact exhaustive predecessor enumeration at temporal length `p=8` shows that each first-branch choice has a unique reverse predecessor for 20 further equations. The second branch occurs on the 21st equation and again consists of exactly two complementary solutions. For one phase the pair is `01101001` / `10010110`; for the complementary phase it is `01011010` / `10100101`.

See `proofs/informal/problem1_reverse_basin_second_branch_experiment.md`.

Next target: derive the rigid period-four reverse subsystem symbolically and isolate the next noninvertible predecessor equation. Test whether it is another cyclic derivative equation imposing the next dyadic divisibility condition (`8 | p`). Avoid treating the p=8 experiment itself as proof.
