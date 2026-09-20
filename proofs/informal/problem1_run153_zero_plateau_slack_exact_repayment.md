# Zero-plateau hidden slack is exactly repaid by the forced-birth cut jump

Status: `partial-proof`. Problem 1 remains open.

## Setup

Use the original-cut delays

    s_j = tau(L_j(r(0))),
    e_j = s_j-j,
    tau(Y_j)=max(e_j,0).

For the established TWO-BIT nonreset passage at time `t`,

    tau(Y_t),...,tau(Y_(t+6)) = 2,1,0,0,0,0,1.

Run152 proved the first zero is exactly on threshold:

    e_t=2, e_(t+1)=1, e_(t+2)=0.

The positive endpoint is also untruncated, so

    e_(t+6)=1.

Hence

    s_(t+2)=t+2,
    s_(t+6)=t+7.                                  (1)

Put the four original-cut increments across the zero plateau and forced birth

    d_k = s_(t+k+1)-s_(t+k),   k=2,3,4,5.

Monotonicity of the cut delays gives `d_k>=0`. Equation (1) gives the exact total

    d_2+d_3+d_4+d_5 = 5.                          (2)

## Exact plateau constraints

For `m=1,2,3`,

    e_(t+2+m) = (d_2+...+d_(m+1))-m.

The physical delays at `t+3,t+4,t+5` are all zero, so

    d_2 <= 1,
    d_2+d_3 <= 2,
    d_2+d_3+d_4 <= 3.                             (3)

These are equivalent to the run152 slack bounds, but now expressed directly in the original residence increments.

Define the terminal hidden slack

    g = g_(t+5) = -e_(t+5)
      = 3-(d_2+d_3+d_4),

so `0<=g<=3`. Combining with (2) yields the exact repayment identity

    d_5 = g+2.                                    (4)

Thus the forced birth at `t+6` cannot merely coexist with arbitrary hidden slack accumulated on the zero plateau. Whatever terminal slack remains is repaid immediately in the original-cut coordinate by a larger jump: the final cut increment is exactly `2+g`, hence lies in `{2,3,4,5}`.

Equivalently,

    g_(t+5)=d_5-2.                                (5)

This is stronger bookkeeping than the physical injection `beta=1`, which sees only the truncated delays and therefore does not distinguish these four possibilities.

## Sharpness of the scalar information

The scalar delay profile and monotonicity alone do **not** improve `0<=g<=3`. Each value is arithmetically realizable by nonnegative cut increments satisfying all zero-row inequalities. For example choose

    (d_2,d_3,d_4,d_5) = (0,0,3-g,g+2),

for `g=0,1,2,3`; condition (3) holds and the sum is five. These are only ledger-compatible increment patterns, not claims that all four occur on a FULL Rule-30 orbit.

Therefore any exclusion of positive hidden slack must use additional complete-core/global-shadow structure. It cannot follow from the known physical delay profile, endpoint positivity, and monotonicity of `s_j` alone.

## Interpretation

Run152 localized hidden slack to the interior zero plateau. The present identity shows exactly where that slack goes: it is converted into extra original-characteristic skipping at the terminal forced birth. In particular, a theorem bounding the final original-cut jump `d_5` would be equivalent on this passage to a theorem bounding the terminal hidden slack.

This reframes the next structural target. Instead of trying to infer `e=0` directly at `t+3,t+4,t+5`, inspect the complete cyclic/gate/global-shadow data at the forced birth for an upper bound on

    s_(t+6)-s_(t+5).

Showing that jump is always `2` would force `g_(t+5)=0`; showing it is at most `C` would give `g_(t+5)<=C-2`. Conversely, if the complete-driver data allow jumps 3,4,5, the hidden-slack route needs a different global charge.

Dependencies: `problem1_run152_hidden_slack_boundary_pinning.md`; `problem1_nonreset_return_birth_spacing.md`; `problem1_physical_episode_ledger_telescope.md`; `problem1_global_discrepancy_front.md`.
