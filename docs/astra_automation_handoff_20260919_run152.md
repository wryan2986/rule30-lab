# Astra automation handoff — 2026-09-19 run152

Problem 1 remains OPEN.

## New result

Run152 attacked the hidden-slack target in `ASTRA_AUTOMATION_HANDOFF.md` rather than extending the local `011` recurrence tests.

For original-cut delays `s_j`, put `e_j=s_j-j`, so `tau(Y_j)=max(e_j,0)`. Since `s_j` is nondecreasing,

    e_(j+1) >= e_j-1.

Hence if a positive physical delay `d` at row `a` reaches physical delay zero exactly `d` rows later, then the zero endpoint is forced to lie exactly on threshold:

    e_(a+d)=0.

Indeed `e_a=d`, while the excess can fall by at most one per row. Equality forces the entire descent `e_(a+k)=d-k`.

Applied to the pushed two-bit nonreset profile

    2,1,0,0,0,0,1,

this upgrades the first three values from truncated physical delays to exact original-cut excesses:

    e_t=2, e_(t+1)=1, e_(t+2)=0.

So the first zero row has no hidden slack. Later zero rows satisfy

    g_(t+3)<=1, g_(t+4)<=2, g_(t+5)<=3,

where `g=-e`. For the immediate resetting one-bit passage, the possible `1,0,1` profile likewise forces its middle zero to have exact `e=0`; the `1,1,1` profile has no truncation.

Full note: `proofs/informal/problem1_run152_hidden_slack_boundary_pinning.md`.

## Interpretation

Hidden negative slack is not present at the first zero reached by deterministic descent from a positive-delay source. It can arise only during additional consecutive zero rows. Thus the all-depth target can be narrowed to the interior zero plateau of the two-bit passage, especially rows `t+3,t+4,t+5`.

## Next target

Use complete cyclic/gate/global-shadow information to determine whether any of the interior zero rows `t+3,t+4,t+5` must also satisfy `e=0`, or otherwise improve the generic bounds `g<=1,2,3`. A repeatable bound on zero-plateau slack could connect forced K=3 episodes to the global original-cut residence ledger. Do not return to local `011` recurrence alone.
