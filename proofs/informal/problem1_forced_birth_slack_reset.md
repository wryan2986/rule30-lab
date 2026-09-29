# Problem 1: forced two-bit birth resets hidden slack only to depth one

Status: exact local consequence / route clarification; Problem 1 remains OPEN.

This note combines the pushed two-bit nonreset return profile in `problem1_nonreset_return_birth_spacing.md` with the signed hidden-slack coordinate from `problem1_hidden_slack_tail_identity.md`. It shows that the forced terminal birth really does repay all hidden zero-delay slack accumulated inside that passage, but its overshoot is exactly one. Thus repeating this local birth mechanism alone cannot produce the unbounded negative slack required by the shift-tail excess theorem.

## Setup

For original-cut thresholds `s_j=tau(L_j(r))`, define the signed slack

    g_j = j-s_j.

The global-front identity is

    tau(Y_j)=max(s_j-j,0)=max(-g_j,0).

Hence a positive physical delay `d` means `g_j=-d`, while a zero-delay row means `g_j>=0`.

The pushed two-bit nonreset source profile has, at times `t,...,t+6`,

    tau(Y_t),...,tau(Y_(t+6)) = 2,1,0,0,0,0,1.

The last `1` is the forced `beta=1` birth.

## Exact threshold consequences

At the first two positive-delay rows,

    s_t=t+2,
    s_(t+1)=t+2.

At `t+2` the physical delay is zero, so `s_(t+2)<=t+2`. Monotonicity of the original-cut thresholds gives

    s_(t+2)>=s_(t+1)=t+2,

therefore

    s_(t+2)=t+2,
    g_(t+2)=0.                                      (1)

At each of `t+3,t+4,t+5` the physical delay remains zero. Thus `g_j>=0`; in particular, writing

    q = g_(t+5) >= 0,

we have

    s_(t+5)=t+5-q.                                  (2)

Because `s_j` is nondecreasing and `s_(t+2)=t+2`, necessarily `0<=q<=3`.

The forced birth gives physical delay one at `t+6`, hence

    s_(t+6)=t+7,
    g_(t+6)=-1.                                     (3)

Combining (2)-(3), the final threshold increment is exactly

    Delta_(t+5)=s_(t+6)-s_(t+5)=2+q.                (4)

In the signed-slack increment law `g_(j+1)-g_j=1-Delta_j`, equation (4) says

    g_(t+6)-g_(t+5)=-(q+1).

So the terminal forced birth repays all `q` units of hidden slack and then overshoots by exactly one unit:

    q  -->  -1.                                     (5)

This conclusion is independent of how the intermediate zero-delay thresholds were distributed inside the passage.

## Consequence

The two-bit forced birth is a genuine slack-repayment event, but it is a **fixed-depth reset**, not an accumulating one. Every such completed passage ends at the same signed level `g=-1` (physical delay one), regardless of the hidden slack present immediately before the birth.

Therefore an argument that only proves infinitely many repetitions of this local two-bit birth profile cannot establish

    liminf g_j = -infinity,

or equivalently

    limsup e_v(n)=+infinity.

To obtain the required unbounded overshoot, one must force either:

1. source/birth passages whose terminal physical delay itself grows without bound; or
2. a genuinely global interaction across passages that preserves some charge not erased by the reset (5).

The already proved spacing of nonreset sources does not supply either statement by itself.

## Relation to the earlier telescope

The result is consistent with `problem1_physical_episode_ledger_telescope.md`: local births cannot simply be summed as independent positive residence gain. Here the same obstruction is visible directly in the hidden-slack coordinate. The forced birth consumes whatever bounded slack `q` accumulated in this six-step profile but always returns to `g=-1`; its local history is forgotten at the endpoint.

This is a stopping fence against the tempting refinement "prove every forced birth repays slack, then iterate." Repayment is true for this exact passage, but the overshoot is uniformly one. Any successful all-depth argument must make the endpoint depth grow or retain additional complete-core/fringe information across these resets.
