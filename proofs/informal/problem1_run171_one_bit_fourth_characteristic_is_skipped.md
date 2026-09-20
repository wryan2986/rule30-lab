# Run 171: the one-bit fourth original-cut characteristic is skipped

Status: `partial-proof`. Problem 1 remains OPEN.

## Setup

Continue from run 170. For every sufficiently late one-bit gate-u nonresetting source at even physical time `t`,

    s_t = s_(t+1) = t+1,
    s_(t+2) = t+2,
    s_(t+3) = t+3,

so the original-cut increments begin

    (Delta_t,Delta_(t+1),Delta_(t+2)) = (0,1,1).

Run 169 also proved that at physical time `t+2` the first actual/original-shadow discrepancy is at position 1:

    m(t+2)=1.

The remaining binary question from run 170 is

    s_(t+4) in {t+3,t+4},

or equivalently whether `Delta_(t+3)` is 0 or 1.

## Use the classified cyclic return

The all-depth nonresetting classification says that the next even row `t+2` is cyclic, has constant-one core low trace, and its actual gate is `t`. In the notation of that classification, gate `t` means `u=0`, while FULL fixes actual bits 0..3 as

    (r_0,r_1,r_2,r_3) = (1,1,u,1 XOR u).

Therefore at physical time `t+2`,

    (r_0,r_1,r_2,r_3)(t+2) = (1,1,0,1).

Run 169 wrote the common actual/shadow position 0 on row `t+1` as `c` and proved

    r_1(t+2)=c,
    h_1(t+2)=c XOR 1.

The classified return now fixes `c=1`, hence

    r_1(t+2)=1,
    h_1(t+2)=0.

At row `t+1`, source bits 1..3 gave

    r_2(t+1)=h_2(t+1)=0.

Let the common source bit 4 be `a=r_4(t)=h_4(t)`. Then one step from the source gives

    r_3(t+1)=h_3(t+1)
      = r_2(t) XOR (r_3(t) OR r_4(t))
      = 1 XOR (0 OR a)
      = 1 XOR a.

Consequently the next position-2 values are

    r_2(t+2)
      = r_1(t+1) XOR (r_2(t+1) OR r_3(t+1))
      = 0 XOR (0 OR (1 XOR a))
      = 1 XOR a,

whereas run 168 gives `h_1(t+1)=1`, so

    h_2(t+2)
      = h_1(t+1) XOR (h_2(t+1) OR h_3(t+1))
      = 1 XOR (0 OR (1 XOR a))
      = a.

But the classified actual cyclic return has `r_2(t+2)=0`. Hence `1 XOR a=0`, so

    a=1,

and therefore

    (r_1,r_2)(t+2)=(1,0),
    (h_1,h_2)(t+2)=(0,1).

Thus positions 1 and 2 are complementary in exactly the cross pattern needed below.

## One more Rule-30 step heals position 1

Because `m(t+2)=1`, actual and the SAME original global E shadow agree at position 0 on row `t+2`; write

    r_0(t+2)=h_0(t+2)=d.

At physical position 1 on the next row,

    r_1(t+3)
      = d XOR (1 OR 0)
      = d XOR 1,

while

    h_1(t+3)
      = d XOR (0 OR 1)
      = d XOR 1.

Therefore

    r_1(t+3)=h_1(t+3).

Run 170 gives `s_(t+3)=t+3`, so by definition of `J`,

    J(t+3)>=t+4,

and the global-front identity gives `m(t+3)>=1`. Since position 1 is now equal, the first discrepancy cannot be there. Therefore

    m(t+3)>=2,
    J(t+3)>=t+5.

By definition of `J(t+3)`, this implies in particular

    s_(t+4)<=t+3.

Monotonicity and `s_(t+3)=t+3` give the reverse inequality, hence

    s_(t+4)=t+3.

Thus

    Delta_(t+3)=0.

So every sufficiently late one-bit gate-u nonresetting source has the exact original-cut prefix

    (Delta_t,Delta_(t+1),Delta_(t+2),Delta_(t+3))=(0,1,1,0).

Equivalently, characteristic `t+4` is necessarily skipped.

## Significance and next target

This is stronger than merely resolving the binary branch left by run 170: at physical time `t+3` the global discrepancy front has retreated to at least position 2,

    m(t+3)>=2.

The result uses the classified cyclic return to fix the actual `(1,0)` pair at `t+2`; no assumption on the wider-right driver is needed after that classification.

The next useful target is `J(t+3)` itself. We now know `J(t+3)>=t+5`. The old zero-delay profile also gives `s_(t+5)<=t+5`. Determine whether position 2 at `t+3` is a discrepancy. If yes, then `m(t+3)=2`, `J(t+3)=t+5`, and the threshold bound may sharply constrain `s_(t+5)`. If position 2 also heals, the front skips at least one additional characteristic.

Dependencies: `problem1_run168_one_bit_shadow_forces_unit_second_residence.md`; `problem1_run169_one_bit_shadow_keeps_front_at_one_on_second_return.md`; `problem1_run170_one_bit_third_residence_is_exactly_one.md`; `problem1_nonresetting_core_returns.md`; `problem1_global_discrepancy_front.md`.
