# Astra automation handoff — run 178 — 2026-09-21

Problem 1 remains OPEN.

## New result

The run-177 terminal slack/reset dichotomy does not yield a new delay-switch cost common to both beta branches.

For a late one-bit gate-u nonresetting source at t:

    beta=0 -> endpoint t+6 is cyclic, tau=0, g=0;
    beta=1 -> endpoint t+6 has tau=1, g=-1, but its core is resetting.

At paired even times I_m=1[tau(Y_(2m))>0]. Every later nonresetting source has I=1 and returns to I=0.

* beta=0: reaching a later nonresetting source indeed requires a 0->1 switch, but this is exactly an ordinary birth already counted by the existing B_m ledger.
* beta=1: endpoint and later nonresetting source both have I=1, so no intervening 0->1 switch is forced. The missing transition is resetting -> nonresetting **while positive delay may persist**.

Therefore tau/b/s/g/I accounting cannot by itself charge every recombination after a one-bit passage. Treating beta=1 as requiring a fresh birth would be an unsupported inference.

Full note: `proofs/informal/problem1_run178_recombination_not_charged_by_delay_switches.md`.

## Next target

Track the complete resetting witness/periodic driver from a beta=1 terminal row. Seek an all-depth law showing whether resetting -> nonresetting conversion at positive delay must pass through cyclicity, a new birth, or consume some separately bounded original-shadow resource. Do not extend the scalar delay-switch ledger unless such a law is proved.
