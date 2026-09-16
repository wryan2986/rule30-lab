# Astra automation handoff — run 54

Problem 1 remains open. No intervening work was present after run 53 (`ea1dff89aeb3b3dbe1ec38f5d272172d1be4238e`).

New file: `proofs/informal/problem1_temporal_necklace_pair_derivative.md`.

Main new results:

- The raw decimation idea proposed by run 53 fails already for the known `p=8 -> p=4` necklaces: for every cyclic phase of the `p=8` representative, neither its even-index nor odd-index subsequence is a rotation of the `p=4` necklace. Do not pursue plain decimation.
- A different period-halving map survives all available nontrivial scales. After a suitable cyclic phase/pair boundary, pairwise adjacent XOR

      Delta_2(c)_j = c_(2j) xor c_(2j+1)

  maps the known `p=4` necklace to the `p=2` necklace and the known `p=8` necklace to the `p=4` necklace, up to rotation.
- This is structurally plausible because the exact reconstruction already produces the temporal derivative `q_3 = S c xor c`.

A naive exhaustive `p=16` trajectory classification was also attempted but is too expensive in the present implementation; the pair-state space is 32-bit and trajectories can already be long at `p=8`. No `p=16` claim should be inferred from that failed computation.

Next target: derive the evolution of adjacent-time-pair XORs under the exact column recursion and test whether terminating length-`2p` reconstruction implies terminating length-`p` reconstruction for one of the two pair boundaries. If XOR alone does not close, identify the smallest auxiliary pair variable needed for an exact semiconjugacy. A proof of this implication would give a credible induction route for the unique-necklace conjecture.