# Astra automation handoff — run 57

Problem 1 remains open.

## Repository state

Run began at `b37be37747161efd94e328bf33171c9446de197a`; no intervening work was present after run 56.

## New result

Followed run 56's recommendation to attack the terminal zero basin directly. For any nonzero terminating temporal-word reconstruction

    q_(i+2) = S q_i xor (q_(i+1) OR q_i),

let `N` be the first index with `q_N=q_(N+1)=0`. Exact backward algebra forces

    q_(N-1)=1^p,
    q_(N-2)=1^p,
    q_(N-3)=0,
    q_(N-4)=alt_p     (when N>=4),

where `alt_p` is a cyclic alternating word. Thus every such trajectory has universal terminal suffix

    ..., alt_p, 0, 1^p, 1^p, 0, 0.

In particular, except for the short `p=1, N=3` base case, termination requires even temporal length. The known `p=8` trajectory matches this suffix exactly.

This is useful for the period-halving route because `alt_(2p)` has adjacent-pair XOR derivative `1^p`: reverse-basin classification can begin from a rigid tiny terminal set instead of arbitrary halved states.

## Research file

`proofs/informal/problem1_terminating_reconstruction_terminal_normal_form.md`

Research commit: `0cfa1637326e86a28e48b2a68e584ccd78458a45`

## Next target

Continue exact reverse predecessor analysis from the forced suffix, preferably in paired `(r,d)` coordinates. Test whether every reverse path that reaches a legal initial pair `(q_0,q_1)=(0,c)` necessarily puts `Delta_2(c)` in the lower-period terminating basin. This attacks the weak period-halving implication directly and avoids the semiconjugacy/local-gauge strategies already ruled out.