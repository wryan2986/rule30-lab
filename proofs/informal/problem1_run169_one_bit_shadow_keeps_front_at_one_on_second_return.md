# Run 169: the one-bit global shadow keeps the front at position one on the second return

Status: `partial-proof`. Problem 1 remains OPEN.

## Setup

Continue from run 168. For every sufficiently late one-bit gate-u nonresetting source at even physical time `t`,

    s_t = s_(t+1) = t+1,
    s_(t+2) = t+2,

and therefore

    J(t+1)=t+2,
    m(t+1)=1.

At the source, the classified actual and SAME original global E-shadow cells are

    actual (r_0,r_1,r_2,r_3)(t) = (1,1,1,0),
    shadow (h_0,h_1,h_2,h_3)(t) = (0,1,1,0).

Run 168 used one Rule-30 step to show `r_1(t+1)=0`, `h_1(t+1)=1`.

## The discrepancy remains at physical position 1 one step later

Because `m(t+1)=1`, actual and original shadow agree at physical position 0 on row `t+1`. Denote their common value by `c`:

    r_0(t+1)=h_0(t+1)=c.

The source cells also determine position 2 after one step, independently of every wider-right driver bit:

    r_2(t+1)
      = r_1(t) XOR (r_2(t) OR r_3(t))
      = 1 XOR (1 OR 0)
      = 0,

and the shadow has the same source bits 1..3, so

    h_2(t+1)=0.

Thus on row `t+1` the triples entering physical position 1 on the next step are

    actual: (c,0,0),
    shadow: (c,1,0).

Rule 30 therefore gives

    r_1(t+2) = c XOR (0 OR 0) = c,
    h_1(t+2) = c XOR (1 OR 0) = c XOR 1.

So actual and the SAME original global E shadow necessarily differ at physical position 1 on row `t+2`.

On the other hand, run 168 gives `s_(t+2)=t+2`. By definition of

    J(u)=min{j : s_j>u},

we have `J(t+2)>=t+3`, hence the global-front identity gives

    m(t+2)=J(t+2)-(t+2)>=1.

Since position 1 is already a discrepancy, this lower bound is sharp:

    m(t+2)=1,
    J(t+2)=t+3.

Therefore

    min{j : s_j>t+2}=t+3.

Equivalently, characteristic `t+3` is the next original-cut characteristic whose stopping time lies strictly beyond physical time `t+2`; no later characteristic can jump ahead of it in the global-front ordering.

## What this does and does not determine

This does **not** yet determine `s_(t+3)` itself. The identity `J(t+2)=t+3` only gives

    s_(t+3)>t+2,

so integrality yields `s_(t+3)>=t+3`. It does not imply `s_(t+3)=t+3`; the residence of characteristic `t+3` may be longer. Thus the next increment

    Delta_(t+2)=s_(t+3)-s_(t+2)

is now known to be positive, but its exact value still needs an upper/phase constraint.

The useful new rigid prefix is therefore

    (Delta_t, Delta_(t+1), Delta_(t+2)) = (0,1, positive),

with exact front positions

    m(t+1)=m(t+2)=1.

No wider-right shadow driver appears in this conclusion.

## Next target

Bound or determine `s_(t+3)` using the classified cyclic return at `t+2`, the eventual delay bound, and the original-cut threshold identity. A direct local-shadow calculation can identify the next front characteristic, as above, but cannot by itself determine how long characteristic `t+3` remains active. Avoid replacing this residence question with the local cyclicization delay.

Dependencies: `problem1_run168_one_bit_shadow_forces_unit_second_residence.md`; `problem1_nonresetting_core_returns.md`; `problem1_global_discrepancy_front.md`.
