# Run 174: terminal one-bit cut dichotomy

Status: `partial-proof` / stopping fence. Problem 1 remains OPEN.

## Setup

Continue from run 173. For every sufficiently late one-bit gate-u nonresetting source at even physical time `t`, the established original-cut stopping times are

    s_t = s_(t+1) = t+1,
    s_(t+2) = t+2,
    s_(t+3) = t+3,
    s_(t+4) = t+3,
    s_(t+5) = t+5.

Equivalently the exact cut-increment prefix is

    (Delta_t,...,Delta_(t+4)) = (0,1,1,0,2).

The all-depth nonreset-return theorem gives the physical-delay profile

    (tau(Y_t),...,tau(Y_(t+6))) = (1,0,0,0,0,0,beta),

where the terminal parameter `beta` is the remaining birth/reset freedom.

## What the threshold identity determines at t+6

Use the established threshold identity

    tau(Y_j) = max(s_j-j,0).

At `j=t+6` this gives a sharp dichotomy.

If `beta>0`, then the maximum is positive and hence

    s_(t+6) = t+6+beta.

Since `s_(t+5)=t+5`, the terminal cut increment is then

    Delta_(t+5) = 1+beta.

If `beta=0`, thresholding only gives

    s_(t+6) <= t+6.

Monotonicity of the stopping times and `s_(t+5)=t+5` give

    s_(t+6) in {t+5,t+6},

so

    Delta_(t+5) in {0,1}.

Therefore the full six-step original-cut itinerary is already rigid except for exactly the same terminal freedom carried by the birth/reset parameter:

    beta>0  =>  (Delta_t,...,Delta_(t+5))=(0,1,1,0,2,1+beta),

while

    beta=0  =>  (Delta_t,...,Delta_(t+5))=(0,1,1,0,2,epsilon),
                 epsilon in {0,1}.

No additional nonterminal cut freedom remains.

## Why the next shadow step alone is insufficient

Run 173 proves `m(t+4)=1`, so the same original global E-shadow differs at position 1 on row `t+4`. But `s_(t+5)=t+5` means characteristic `t+5` expires exactly at the next physical row. To determine `s_(t+6)` from row `t+5`, one must know whether the first surviving discrepancy there is attached to characteristic `t+6` or lies farther right. The run-173 data fix the discrepancy at position 1 on row `t+4`, but do not fix the needed position-2 shadow driver on that row. Rule 30 propagation of the position-1 discrepancy to row `t+5` therefore cannot be completed from the currently classified low cells alone.

This is the precise stopping fence: another local step is useful only if an existing theorem fixes the wider original-shadow driver at the terminal birth, or if a new argument relates that driver to `beta`. Treating the cyclic return's local core as that original shadow would repeat the invalid identification fenced off in run 166.

## Next target

The useful next target is not another unconstrained low-cell propagation. Prove a bridge between the terminal birth/reset parameter `beta` and the original global-shadow driver at position 2 on row `t+4` (equivalently the first surviving discrepancy on row `t+5`). In particular, the only unresolved zero-birth question is whether

    beta=0 => s_(t+6)=t+5

or

    beta=0 => s_(t+6)=t+6.

Resolving that binary case completes the six-step original-cut itinerary.

Dependencies: `problem1_run173_one_bit_fifth_residence_is_exactly_two.md`; `problem1_global_discrepancy_front.md`; the established all-depth nonreset-return/birth theorem; `problem1_run166_one_bit_nonresetting_front_stopping_fence.md`.
