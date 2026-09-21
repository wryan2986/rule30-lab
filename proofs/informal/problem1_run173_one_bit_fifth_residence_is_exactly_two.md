# Run 173: the one-bit fifth residence is exactly two

Status: `partial-proof`. Problem 1 remains OPEN.

## Setup

Continue from run 172. For every sufficiently late one-bit gate-u nonresetting source at even physical time `t`, the original-cut stopping times satisfy

    s_t = s_(t+1) = t+1,
    s_(t+2) = t+2,
    s_(t+3) = t+3,
    s_(t+4) = t+3,
    s_(t+5) in {t+4,t+5}.

Run 172 proved

    m(t+3)=2,
    J(t+3)=t+5,

and at physical time `t+3` position 2 differs between the actual row and the SAME original global E shadow:

    r_2(t+3)=0,
    h_2(t+3)=1.

Run 171 proved position 1 heals at this row, so

    r_1(t+3)=h_1(t+3).

The remaining question is whether `s_(t+5)=t+4` or `t+5`.

## The common position-1 value is zero

The classified cyclic return at `t+2` has actual gate t, hence

    (r_0,r_1,r_2,r_3)(t+2)=(1,1,0,1).

Therefore Rule 30 at position 1 gives

    r_1(t+3)
      = r_0(t+2) XOR (r_1(t+2) OR r_2(t+2))
      = 1 XOR (1 OR 0)
      = 0.

Since position 1 is healed there,

    h_1(t+3)=0

as well. Let the common position-0 value be `c`:

    r_0(t+3)=h_0(t+3)=c.

The equality at position 0 also follows from `m(t+3)=2`.

## One more step forces a discrepancy at position 1

Apply Rule 30 at position 1 on row `t+3`. Using the forced position-2 values from run 172,

    r_1(t+4)
      = c XOR (0 OR 0)
      = c,

while

    h_1(t+4)
      = c XOR (0 OR 1)
      = c XOR 1.

Thus position 1 is certainly a discrepancy at physical time `t+4`, independently of `c` and independently of every wider-right shadow bit.

We also know from run 172 that `s_(t+5)>t+3`, so at time `t+4` the first characteristic that can still be active is at least `t+5`. Hence the global-front identity gives

    m(t+4) >= 1.

The explicit discrepancy at position 1 makes this sharp:

    m(t+4)=1,
    J(t+4)=t+5.

By definition of `J`,

    s_(t+5)>t+4.

Run 172 already supplied the upper bound `s_(t+5)<=t+5` from the established zero physical delay at `t+5`. Integrality therefore forces

    s_(t+5)=t+5.

Since `s_(t+4)=t+3`,

    Delta_(t+4)=2.

So the sufficiently late one-bit gate-u nonresetting source has the exact original-cut prefix

    (Delta_t,...,Delta_(t+4))=(0,1,1,0,2).

## Significance and next target

The binary ambiguity left by run 172 is closed: characteristic `t+5` has residence length exactly two, not one. The result uses only the already classified actual return, the same original global shadow, and the global-front identity; no wider shadow driver enters.

The established one-bit delay profile also has `tau(Y_(t+6))=beta`, so the next useful step is to determine `s_(t+6)` (or its excess over `t+6`) from the global front during the second physical row of the `t+5` residence. This should reveal whether the one-bit passage has a fully rigid six-step cut itinerary or whether the final birth/reset parameter first appears there.

Dependencies: `problem1_run172_one_bit_front_is_exactly_two_at_tplus3.md`; `problem1_run171_one_bit_fourth_characteristic_is_skipped.md`; `problem1_nonresetting_core_returns.md`; `problem1_global_discrepancy_front.md`.
