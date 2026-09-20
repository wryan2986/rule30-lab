# Run 172: the one-bit global front is exactly two at t+3

Status: `partial-proof`. Problem 1 remains OPEN.

## Setup

Continue from run 171. For every sufficiently late one-bit gate-u nonresetting source at even physical time `t`, we have

    s_t = s_(t+1) = t+1,
    s_(t+2) = t+2,
    s_(t+3) = t+3,
    s_(t+4) = t+3,

and at physical time `t+2` the SAME original global E shadow satisfies

    (r_1,r_2)(t+2) = (1,0),
    (h_1,h_2)(t+2) = (0,1).

The classified cyclic return at `t+2` has actual gate `t`, so FULL also fixes

    r_3(t+2)=1.

Run 171 proved that position 1 heals one step later and therefore

    m(t+3) >= 2.

The remaining question is whether position 2 at `t+3` differs.

## Position 2 differs independently of the wider shadow

Apply Rule 30 at physical position 2. For the actual row,

    r_2(t+3)
      = r_1(t+2) XOR (r_2(t+2) OR r_3(t+2))
      = 1 XOR (0 OR 1)
      = 0.

For the original shadow, write the unrestricted next shadow bit as

    b = h_3(t+2).

Then

    h_2(t+3)
      = h_1(t+2) XOR (h_2(t+2) OR h_3(t+2))
      = 0 XOR (1 OR b)
      = 1.

Thus, for every possible wider-right shadow driver,

    r_2(t+3)=0,
    h_2(t+3)=1.

So position 2 is certainly a discrepancy. Combined with run 171's `m(t+3)>=2`, this is sharp:

    m(t+3)=2.

By the global-front identity,

    J(t+3)=t+5.

Hence characteristic `t+5` is exactly the first original-cut characteristic whose stopping time lies strictly after physical time `t+3`.

## Consequence for the next stopping time

By definition of `J`,

    s_(t+5) > t+3.

The established one-bit nonresetting delay profile has

    tau(Y_(t+5))=0.

Using the original-cut threshold identity

    tau(Y_j)=max(s_j-j,0),

we obtain

    s_(t+5) <= t+5.

Therefore

    s_(t+5) in {t+4,t+5}.

Since run 171 gave `s_(t+4)=t+3`, the next original-cut increment is reduced to

    Delta_(t+4) in {1,2}.

So the one-bit original-cut itinerary now begins

    (Delta_t,...,Delta_(t+4)) = (0,1,1,0, epsilon),

with

    epsilon in {1,2}.

## Significance and next target

The front location at `t+3` is now exact and is independent of all wider shadow bits:

    m(t+3)=2,
    J(t+3)=t+5.

This rules out any additional skipped characteristic at that physical row: `t+4` is skipped, but `t+5` is definitely the next visited characteristic.

The remaining ambiguity is its residence length, equivalently whether `s_(t+5)=t+4` or `t+5`. The next useful step is to evolve the actual/original-shadow pair one more physical step and test the first discrepancy at `t+4`; together with the threshold bound above this should distinguish `Delta_(t+4)=1` from `2` if the low shadow cells remain rigid enough.

Dependencies: `problem1_run171_one_bit_fourth_characteristic_is_skipped.md`; `problem1_nonresetting_core_returns.md`; `problem1_global_discrepancy_front.md`.
