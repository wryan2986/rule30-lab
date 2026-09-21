# Run 177: the one-bit passage has an exact slack/reset dichotomy

Status: `partial-proof / synthesis`. Problem 1 remains OPEN.

## Setup

Take a sufficiently late surviving one-bit gate-u nonresetting source at even physical time `t`. Runs 167--176 establish the exact original-cut increment itinerary

    (Delta_t,...,Delta_(t+5)) = (0,1,1,0,2,1+beta),

where `beta in {0,1}` is the Boolean terminal cyclic-source birth indicator from `problem1_nonreset_return_birth_spacing.md`.

Define the original-cut slack

    g_j = j - s_j.

The threshold identity is

    tau(Y_j) = max(s_j-j,0) = max(-g_j,0).

At the one-bit source `tau(Y_t)=1`, hence `s_t=t+1` and

    g_t = -1.

## Exact slack path

Summing the proved increments gives

    s_t     = t+1,
    s_(t+1) = t+1,
    s_(t+2) = t+2,
    s_(t+3) = t+3,
    s_(t+4) = t+3,
    s_(t+5) = t+5,
    s_(t+6) = t+6+beta.

Therefore the slack path is exactly

    (g_t,...,g_(t+6)) = (-1,0,0,0,1,0,-beta).

So the six-step signed residence charge `beta-1` found earlier is not merely telescoping in the abstract: on this passage it is exactly

    beta-1 = g_t - g_(t+6).

This explains why the local charge cannot accumulate independently across repeated passages.

## Terminal dichotomy

The imported complete-core theorem supplies more structure than the slack value alone. At `t+6` the actual gate is `t` in both beta cases. Moreover:

* `beta=0`: `tau(Y_(t+6))=0`, and the terminal row is cyclic. The lag has been extinguished: `g_(t+6)=0`.
* `beta=1`: `tau(Y_(t+6))=1`, and the terminal one-bit t-source is resetting because its complete code at A-time 1 equals the actual gate symbol 1. The lag survives: `g_(t+6)=-1`, but the nonresetting-core condition has been destroyed.

Thus every sufficiently late surviving one-bit NONRESETTING passage exits through exactly one of two mutually exclusive repairs:

    beta=0: erase the lag and return cyclic;
    beta=1: preserve lag one but reset the core.

In particular the passage cannot exit at `t+6` with both lag one and a nonresetting core. This is a stronger structural reading of the already proved >=8 source spacing: the obstruction to an immediate new nonresetting source is not just a gate-prefix accident. The terminal Boolean chooses which of the two ingredients needed for the source is lost.

## What this does and does not prove

This is not yet a global contradiction. A later evolution can in principle recreate the missing ingredient: after beta=0 a new lag may be born, and after beta=1 the core may later become nonresetting again. The existing >=8 spacing theorem only excludes source times through `t+7`.

The useful next target is therefore narrower than tracking beta alone: prove a lower bound or monotone cost for RECOMBINING the two ingredients after either terminal repair. In the beta=0 branch, track the first later creation of negative slack from `g=0`. In the beta=1 branch, track the first later loss of the resetting witness while `g=-1` (or show the lag must first heal). A bounded-reuse charge attached to those recombination events would avoid counting the local `beta-1` telescope twice.

Dependencies: `problem1_run175_zero_birth_terminal_residence_is_one.md`; `problem1_run176_terminal_beta_is_boolean_and_cannot_escalate.md`; `problem1_nonreset_return_birth_spacing.md`; `problem1_physical_episode_ledger_telescope.md`.
