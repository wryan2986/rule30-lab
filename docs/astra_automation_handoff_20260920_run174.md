# Astra automation handoff — run 174

Problem 1 remains OPEN.

Run 173 fixed the one-bit gate-u nonresetting original-cut prefix to

    (Delta_t,...,Delta_(t+4))=(0,1,1,0,2),

with `s_(t+5)=t+5`.

Run 174 isolates the terminal freedom using the threshold identity and the established delay profile `(1,0,0,0,0,0,beta)`:

- if `beta>0`, then `s_(t+6)=t+6+beta` and `Delta_(t+5)=1+beta`;
- if `beta=0`, then `s_(t+6) in {t+5,t+6}` and `Delta_(t+5) in {0,1}`.

Thus every nonterminal residence is rigid. The only remaining ambiguity is the zero-beta terminal case.

Important stopping fence: do not simply propagate the local cyclic core as though it were the same original global E-shadow. At row `t+4`, run 173 fixes a discrepancy at position 1 but the position-2 original-shadow driver needed for the next Rule-30 update is not fixed by the currently classified low-cell data. A bridge from the terminal birth/reset parameter `beta` to that wider original-shadow driver is needed.

Next target: determine whether `beta=0` forces `s_(t+6)=t+5` or `t+6`. Search existing birth/reset and global-front notes first for a relation fixing the terminal original-shadow position-2 driver; only then do further local propagation.

New proof note: `proofs/informal/problem1_run174_terminal_one_bit_cut_dichotomy.md`.
