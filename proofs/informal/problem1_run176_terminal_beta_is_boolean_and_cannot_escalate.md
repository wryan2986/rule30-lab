# Run 176: terminal beta is Boolean; positive-charge escalation is impossible

Status: `partial-proof / correction`. Problem 1 remains OPEN.

## Correction to runs 174–175

For a sufficiently late one-bit gate-u nonresetting source, runs 173–175 established the exact original-cut itinerary

    (Delta_t,...,Delta_(t+5))=(0,1,1,0,2,1+beta)

and hence six-step signed ledger charge

    beta-1.

Runs 174–175 discussed cases `beta>=2` as though the terminal parameter could be an arbitrary nonnegative delay. That is not compatible with the imported nonreset-return theorem.

In `problem1_nonreset_return_birth_spacing.md`, beta is explicitly the cyclic-source **birth indicator**

    beta = 1 XOR eta,

where eta is a Boolean shadow flag. Therefore

    beta in {0,1}.

The same theorem gives the terminal physical-delay profile

    tau(Y_(t+6))=beta.

Thus the complete one-bit itinerary has only two possibilities:

    beta=0: (0,1,1,0,2,1),
    beta=1: (0,1,1,0,2,2).

The corresponding signed charges are exactly

    -1 and 0.

In particular a one-bit nonresetting passage can NEVER have positive six-step signed residence charge. The proposed continuation target "force beta>=2" is impossible and must not be pursued.

## Consequence for the global strategy

This strengthens the existing telescope fence rather than weakening it. The two-bit nonresetting source was already excluded in the later source analysis, and the surviving one-bit source has a complete local passage whose signed charge is always nonpositive. Therefore no contradiction can come from proving that terminal births become numerically large: the terminal birth variable is one bit.

The remaining all-depth routes are the ones already identified in `ASTRA_AUTOMATION_HANDOFF.md`:

1. control hidden slack `g_j=j-s_j` at zero-delay rows;
2. prove a non-telescoping global charge with bounded reuse; or
3. use complete-core/global-shadow transport across successive separated episodes to rule out an infinite sequence of the two Boolean passage types.

The third route must concern the *pattern* of beta values and intervening resetting/cyclic episodes, not beta magnitude.

## Audit note

This correction does not invalidate the algebraic result of run 175. Its proof of the beta=0 terminal residence remains useful and, together with the beta=1 threshold case, yields the exact two itineraries above. Only the statements allowing `beta>1` and suggesting positive charge for `beta>=2` are removed from the research direction.

Dependencies: `problem1_run175_zero_birth_terminal_residence_is_one.md`; `problem1_nonreset_return_birth_spacing.md`; `problem1_physical_episode_ledger_telescope.md`.
