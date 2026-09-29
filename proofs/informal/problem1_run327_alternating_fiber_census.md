# Problem 1 run 327: alternating-fiber reset census and boundary sensitivity

Status: exact exploratory computation; Problem 1 remains OPEN.

Continue the run-326 alternating-fiber route with center trace `1010...` and distinguished prefix

    R0,R1,R2 = 1,1,0.

Left permutivity uniquely determines each successive left bit `L_n`.

## Longer reset witness

A finite eventually-zero right half already permits at least 18 consecutive forced zeros. One witness is

    (R0,...,R16) = (1,1,0,1,1,0,0,1,1,0,0,1,1,0,0,1,0),
    R_j = 0 for j >= 17.

Exact triangular inversion gives

    L166 = L167 = ... = L183 = 0,
    L184 = 1.

Thus the unrestricted alternating fiber does not support any small universal bounded-gap latch. This strengthens the seven-zero witness in run 326.

## New boundary-sensitivity check

To test whether the long reset is monotone under extending a structured right prefix, use the infinite formal pattern

    R = 110 1100 1100 1100 ...

and, for each width `w`, truncate after `R_w` and set all later right cells to zero. Exact inversion through depth 220 gives the following maximum zero-run lengths:

    w=10: 7
    w=11..14: 6
    w=15..18: 18   (the run is L166..L183)
    w=19..25: 5

So the 18-zero reset persists under several one-bit extensions but disappears when the next `1` of the `1100` pattern is admitted at width 19. In particular, reset length is not monotone in right-support width even inside this simple periodic-prefix family.

This rules out another tempting shortcut: one cannot prove the finite-right-half case by showing that extending a right prefix monotonically preserves or lengthens a reset/nonreset property. The far-right boundary can destroy a long reset abruptly.

## Stopping fence

Further unrestricted alternating-fiber census work is unlikely to resolve Problem 1. The exact identity from run 326,

    L11 = R3,

should instead be transported through the actual FULL/cyclic-source return map. The repository handoff says the complete phase/fringe constraints were developed in recovered worktree drafts (`problem1_three_bit_complete_core_system.md`, `problem1_complete_core_phase_transport.md`, `problem1_fixed_fringe_phase_collapse.md`) that are not present on this pushed branch. Those constraints are needed to distinguish admissible source returns from the unrestricted fibers above.

Reproducibility: for each depth n, set the new initial cell at position -n to 0 and 1, evolve Rule 30 for n steps, and choose the unique value producing the required center bit of the alternating trace. Left permutivity guarantees exactly one choice. All cells to the right of the declared finite width are fixed to zero.
