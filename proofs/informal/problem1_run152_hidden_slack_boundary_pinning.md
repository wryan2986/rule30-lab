# Hidden slack is pinned at the first zero of the forced nonreset passage

Status: `partial-proof`. Problem 1 remains open.

## Setup

For the fixed original finite row write

    s_j = tau(L_j(r(0))),
    e_j = s_j-j,
    tau(Y_j)=max(e_j,0).

Since `s_(j+1)>=s_j`,

    e_(j+1)-e_j = (s_(j+1)-s_j)-1 >= -1.          (1)

Thus the hidden excess can decrease by at most one per spatial step. At a zero-delay row define hidden slack `g_j=-e_j>=0`.

## Boundary-pinning lemma

If `tau(Y_a)=d>0` and `tau(Y_(a+d))=0`, then

    e_a=d,
    e_(a+d) <= 0.

Iterating (1) gives

    e_(a+d) >= e_a-d = 0,

hence necessarily

    e_(a+d)=0,
    g_(a+d)=0.                                     (2)

Moreover equality across the whole d-step drop forces every increment of `s` on that interval to vanish, so

    e_(a+k)=d-k,  0<=k<=d.                         (3)

This is an exact original-cut statement; no Rule-30 local calculation beyond the already established threshold identity and monotonicity of `s_j` is needed.

## Application to the pushed two-bit nonreset profile

The established profile is

    tau(Y_t),...,tau(Y_(t+6)) = 2,1,0,0,0,0,1.

Applying the lemma with `a=t,d=2` gives the stronger untruncated information

    e_t=2,
    e_(t+1)=1,
    e_(t+2)=0.                                     (4)

Therefore the first zero-delay row of the passage has **no hidden negative slack at all**. The truncation in `tau(Y_(t+2))=0` loses no information there.

For later zero rows monotonicity alone gives

    e_(t+k) >= 2-k,

so

    0 <= g_(t+k) <= k-2,   k=2,3,4,5.              (5)

In particular the only possible hidden slack before the forced birth is bounded locally by

    g_(t+3)<=1,
    g_(t+4)<=2,
    g_(t+5)<=3.                                    (6)

The endpoint `e_(t+6)=1` is again exact because its physical delay is positive.

## Resetting one-bit passage

The pushed resetting one-bit `t` passage has delay triple either

    1,1,1

or

    1,0,1.

In the second case, applying the lemma with `d=1` pins the middle zero row exactly:

    e_(t+7)=0.                                     (7)

Thus that zero also carries no hidden slack. In the `1,1,1` case there is no truncation anywhere.

## Interpretation

The hidden-slack target from `ASTRA_AUTOMATION_HANDOFF.md` is narrower than it first appears on the forced K=3 passages. Slack cannot already be negative at the first zero reached by the deterministic descent from a positive source; it is created only by remaining at physical delay zero for additional spatial steps. In the complete two-bit nonreset + immediate resetting passage, every zero that occurs immediately after a positive delay is pinned to the threshold `e=0`.

This does not yet bound slack globally: consecutive zero rows can accumulate it, and a later large residence can repay it in one step. The next useful question is whether the complete cyclic/gate constraints restrict the consecutive-zero portion `t+2,...,t+5`, especially whether they force any of `e_(t+3),e_(t+4),e_(t+5)` to remain at zero. Such a theorem would control information that the physical-delay profile currently hides.

Dependencies: `problem1_global_discrepancy_front.md`; `problem1_physical_episode_ledger_telescope.md`; `problem1_nonreset_return_birth_spacing.md`; `problem1_exit_wait_front_residence.md`.
