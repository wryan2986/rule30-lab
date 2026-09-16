# Astra automation handoff — run 58

Problem 1 remains open.

This run continued the reverse zero-basin calculation from run 57. No intervening repository work was present at the start of the run (tip `429a3b6da558e429f352742627a77e9eb9fd1673`).

New exact result: if `A=alt_p` and `N` is the first zero-pair index, then four additional predecessors behind the run-57 suffix are forced:

    q_(N-8),...,q_(N+1)
      = 0, A, A, 1, A, 0, 1, 1, 0, 0.

The next predecessor is the first genuine reverse branch. It satisfies

    A = S q_(N-9) xor q_(N-9).

Hence, when `N>=9`, solvability forces `p` divisible by 4. There are exactly two solutions, complementary/rotational phases of the period-four pattern `0011...`.

This also yields a useful scale-compatibility observation: under adjacent-pair XOR derivative `Delta_2`, that period-four reverse branch maps to the alternating word at half temporal length, i.e. precisely the universal alternating predecessor in the lower-period terminal basin. This is an exact reverse-basin compatibility, not a forward semiconjugacy.

The `p=2` terminating trajectory is not contradicted: it terminates at `N=8`, so `q_(N-9)` does not exist.

Research note: `proofs/informal/problem1_terminal_normal_form_extended_backward.md`.

Next target: compute/classify predecessors of the two period-four `q_(N-9)` branches and test whether their `Delta_2` images coincide with the predecessor set of the lower-period alternating state. Persistence of this relation through reverse layers would give a basin-level period-halving induction.
