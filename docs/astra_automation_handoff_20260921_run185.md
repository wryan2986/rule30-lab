# Astra automation handoff — run 185 — 2026-09-21

Problem 1 remains OPEN.

No intervening work was present after run 184 when this run began.

## New exact conditional result

Continue the `beta=1` branch. Run 181 gives at `t+7`, with `x=r_0(t+6)` and `y=1 XOR x`,

    actual (r_0,r_1,r_2)=(y,y,0).

Run 184 gives

    m(t+8)=0,
    J(t+8)=t+8,
    s_(t+8)>=t+9,
    tau(Y_(t+8))>=1,
    s_(t+7)=t+7.

Put `p=r_3(t+7)` and

    alpha := y XOR p.

Direct Rule 30 gives the actual right pair at `t+8`:

    (r_1,r_2)(t+8)=(0,alpha).

So the actual gate-u indicator at `t+8` is exactly `alpha`.

If `N_(t+8)` holds, the pushed nonresetting-core theorem says its source delay is `d=2-u`. Hence

    tau(Y_(t+8))=2-alpha,
    s_(t+8)=t+10-alpha,
    Delta_(t+7)=3-alpha.

Thus a hypothetical first-allowed nonresetting recurrence has only two exact possibilities:

    alpha=1: one-bit gate-u source, tau=1, Delta_(t+7)=2;
    alpha=0: two-bit gate-t source, tau=2, Delta_(t+7)=3.

There is no remaining scalar-delay freedom inside the candidate nonresetting branch. One actual complete-driver bit `p=r_3(t+7)` relative to `x` selects gate, source width, delay and residence endpoint.

## Fence

This does NOT prove `N_(t+8)` and does not classify the resetting alternative. Do not apply cyclic-source birth laws here without an independent cyclicity result.

## Next target

Express `alpha=(1 XOR x) XOR r_3(t+7)` from the complete resetting endpoint at `t+6`, or determine whether the resetting/nonresetting classification at `t+8` is selected by this same bit. A separate useful exclusion would be any all-depth argument forcing `Delta_(t+7)>=4`, because the candidate N branch permits only 2 or 3.

New proof file:
`proofs/informal/problem1_run185_tplus8_nonreset_candidate_has_exact_delay.md`
