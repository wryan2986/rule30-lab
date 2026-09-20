# Run 167: a one-bit gate-u nonresetting source forces the next original-cut characteristic to be skipped

Status: `partial-proof`. Problem 1 remains OPEN.

## Setup

Keep the original finite actual row and its original-cut stopping times

    s_j = tau(L_j(r(0))).

The established global-front theorem gives

    tau(Y_j) = max(s_j-j,0),

and spatial deletion gives monotonicity

    s_(j+1) >= s_j.

At a sufficiently late one-bit gate-u nonresetting source at even physical time `t`, the established nonreset-return classification gives the delay profile

    tau(Y_t)=1,
    tau(Y_(t+1))=0,
    tau(Y_(t+2))=0.

Run 166 correctly warned that the source cyclicization identity `A x=A z` does not by itself determine the next global-front residence. The following deduction instead uses only the original-cut threshold identity and monotonicity.

## Exact stopping-time consequence

Because `tau(Y_t)=1>0`, the max in the threshold identity is inactive, hence

    s_t-t=1,

so

    s_t=t+1.                                      (1)

At the next index, `tau(Y_(t+1))=0`, so

    s_(t+1) <= t+1.                               (2)

But original-cut stopping times are nondecreasing, therefore

    s_(t+1) >= s_t=t+1.                           (3)

Combining (2) and (3) gives the exact identity

    s_(t+1)=s_t=t+1.                              (4)

Thus the original-cut residence increment is

    Delta_t=s_(t+1)-s_t=0.                        (5)

By the global-front residence theorem, characteristic `t+1` has residence interval

    [s_t,s_(t+1)) = [t+1,t+1),

which is empty. Therefore:

> Every sufficiently late one-bit gate-u nonresetting source forces the immediately following original-cut characteristic `t+1` to be skipped by the global discrepancy front.

Equivalently, at physical time `t+1`,

    J(t+1) >= t+2,
    m(t+1)=J(t+1)-(t+1) >= 1.                     (6)

This is an original-cut statement, not an inference from the local cyclicization delay. It supplies the first exact entry of the missing one-bit residence itinerary.

## What is and is not determined

The same argument does not fix `s_(t+2)`. From `tau(Y_(t+2))=0` we have only

    t+1=s_(t+1) <= s_(t+2) <= t+2.

Hence

    s_(t+2) in {t+1,t+2},

so the next increment is restricted to

    Delta_(t+1) in {0,1}.                         (7)

Accordingly, at `t+1` the front either skips characteristic `t+2` as well (`s_(t+2)=t+1`) or visits it for exactly one step (`s_(t+2)=t+2`). Existing delay data alone do not distinguish these cases.

This is the precise next branch to test against the complete original global shadow. It is stronger than the run-166 stopping fence: the first post-source residence is now known exactly, and the second has only two possibilities.

## Dependencies and fence

Dependencies: `problem1_global_discrepancy_front.md` Sections 1-2 for `s_j` monotonicity, the threshold identity and residence intervals; `problem1_nonreset_return_birth_spacing.md` Sections 1-2 for the one-bit gate-u delay profile.

Do not identify `tau(Y_t)=1` with a residence length. Equation (5) follows only after combining the physical-delay threshold identity with monotonicity of the original-cut stopping times. No claim is made that all later zero-delay rows have zero hidden slack.
