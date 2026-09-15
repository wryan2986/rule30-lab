# Astra automation handoff — run 53

Problem 1 remains open. This run continued the run-52 one-word reconstruction route.

New file: `proofs/informal/problem1_terminating_temporal_word_necklace_experiment.md`.

Main new result: exhaustive word-level computation for dyadic periods `p=1,2,4,8` shows that the odd-parity words whose exact column reconstruction terminates are, at every tested period, exactly one cyclic rotation orbit. Counts are `1,2,4,8`; representatives can be taken as `1`, `01`, `0111`, `00001101`. Termination columns are respectively `3,8,29,400`.

This motivates the unique-necklace conjecture: for every dyadic `p`, exactly one temporal necklace reconstructs a finite doubling-eligible parent. If proved, local doubling parents are extremely rigid rather than plentiful.

Also derived the exact parity recurrence

    P(q_(i+2)) = P(q_(i+1)) xor P(q_i AND q_(i+1)),

which immediately gives `P(q_2)=1`, `P(q_3)=0` from odd `c`.

Next target: classify `p=16` with memoized functional-graph/basin computation rather than naive per-word simulation, and search for an inductive decimation/predecessor theorem from a terminating length-`2p` word to the unique terminating length-`p` necklace. Do not return to forced-fiber transport; runs 50–52 already reduced the useful certificate to this protected temporal-word problem.
