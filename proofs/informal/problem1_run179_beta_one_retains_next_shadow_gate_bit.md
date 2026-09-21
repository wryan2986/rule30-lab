# Run 179: beta=1 retains an independent next-shadow gate bit

Status: `partial-proof` / obstruction refinement. No new experiment. Problem 1 remains OPEN.

## Setup

Continue from runs 175--178. Let t be a sufficiently late one-bit gate-u nonresetting source in the eventual K=3 regime. The established passage has a cyclic gate-u row at t+4 and terminal Boolean birth beta at t+6. In the branch beta=1, the row Y_(t+6) has delay one, actual gate t, and a resetting core.

Run 178 isolated the missing transition as resetting -> nonresetting while positive delay may persist. The purpose here is to identify the first extra piece of the original global shadow that survives beta=1 and therefore must be retained in any such transport argument.

## Exact refinement at the cyclic source t+4

Write the SAME global E-shadow right cells at the cyclic row t+4 as

    (a,b,c,d)=(hat r_1,hat r_2,hat r_3,hat r_4)(t+4).

Because the actual gate there is u, its actual zero-pair flag is

    u_(t+4)=1.

The cyclic-source birth law gives

    beta = u_(t+4) XOR hat u_(t+4)
         = 1 XOR hat u_(t+4).

Hence beta=1 says only

    hat u_(t+4)=0,

or equivalently

    (a,b) != (0,0).                                  (1)

The already-proved exact two-step forward transport of the SAME shadow flag gives

    hat u_(t+6)=a*b*(c OR d).                         (2)

Therefore beta=1 does not collapse the next shadow gate flag. Define

    gamma := hat u_(t+6)=a*b*(c OR d).

Under (1), gamma remains a genuine additional Boolean datum of the complete original shadow driver. Algebraically, both values survive the beta=1 condition: for example (a,b,c,d)=(1,0,0,0) gives gamma=0, whereas (1,1,1,0) gives gamma=1. These assignments are only witnesses to non-implication of the Boolean formulas; they are NOT asserted to be realizable FULL/E-shadow states.

Thus the implication

    beta=1 => a determined shadow gate state at t+6

is unavailable. Any proof that treats the beta=1 resetting endpoint as a closed scalar state loses information already visible one step beyond beta.

## Relation to the resetting endpoint

The actual gate at t+6 is t, so its actual zero-pair flag is 0. Consequently gamma records whether the global shadow's right-pair gate flag agrees with that actual t gate at the resetting delayed endpoint:

    gamma=0: actual and shadow zero-pair flags agree at t+6;
    gamma=1: they disagree at t+6.

The cyclic-source birth law cannot simply be reapplied at t+6, because Y_(t+6) is noncyclic when beta=1. Equation (2), however, is legitimate: it was propagated forward from the cyclic source t+4 using its justified shadow center inputs. This distinction is essential.

So the run-178 target sharpens from an unspecified "complete resetting witness/driver" to at least the pair

    (resetting endpoint, gamma),

with gamma inherited from the original shadow cells c,d at the preceding cyclic source. A scalar state consisting only of tau, g, beta, actual gate, and resetting/nonresetting type is not closed even for the first post-passage shadow gate observable.

## What this does and does not prove

This does not show that both gamma values occur on an infinite FULL survivor, nor does it determine whether gamma controls the eventual resetting -> nonresetting conversion. It does prove that beta=1 alone cannot do so via the known gate-flag transport: the next shadow flag still depends on wider original-shadow data.

A productive next step is to propagate gamma together with the resetting core through the first admissible recombination time (the existing spacing theorem excludes a new nonresetting source through t+7). The target should be an all-depth relation constraining gamma at a possible source t+8, not another scalar delay ledger.

## Dependencies

* `problem1_shadow_gate_birth_phase.md`, especially equations (3) and (9).
* `problem1_nonreset_return_birth_spacing.md`, Sections 2--4.
* `problem1_run175_zero_birth_terminal_residence_is_one.md`.
* `problem1_run178_recombination_not_charged_by_delay_switches.md`.
