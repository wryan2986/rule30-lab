# Problem 1: a period-doubling zero lift forces the next zero lift to exit

## Status

Problem 1 remains open. This note strengthens the period-growth invariant from the previous run and closes the proposed route based on repeated period doublings inside one periodic zero-extension run.

## Setup

Let `z` be nonzero and periodic under `A` with exact period `p`. Write

    z_s = A^s(z),
    b_s = bit_0(z_s),
    c_s = bit_1(z_s).

For a one-bit lift `w=2z+a_0`, write

    A^s(w) = 2 z_s + a_s.

The established lift recurrence is

    a_(s+1) = c_s XOR (b_s OR a_s).

Suppose specifically that the zero lift `2z` is periodic with exact period `2p`, i.e. this lift doubles the base period.

By the previous period classifier, period doubling is possible only if

    b_s = 0   for every 0<=s<p,

and

    C := XOR_(s=0..p-1) c_s = 1.

For the zero lift, `a_0=0`, so while `b_s=0` we have

    a_(s+1)=a_s XOR c_s.

Hence

    a_p = C = 1,

and in particular the `2p`-cycle of `2z` contains a state with low bit one.

## Theorem: if 2z doubles the period, then 4z is nonperiodic

Now view

    4z = 2(2z)+d_0

as the zero one-bit lift of the periodic base `2z`, with `d_0=0`.

Along the orbit of `2z`, we have

    A^s(2z)=2z_s+a_s.

Therefore

    bit_0(A^s(2z)) = a_s,
    bit_1(A^s(2z)) = b_s = 0.

Apply the one-bit lift recurrence again to the second lift bit `d_s`:

    d_(s+1) = 0 XOR (a_s OR d_s)
            = a_s OR d_s.

Because `a_p=1`, this recurrence has an eraser during one period of the base `2z`. Its unique recurrent initial bit is `d_0=1`: once `d_s` becomes one it remains one forever around the cycle.

But `4z` has `d_0=0`. Hence it is the nonrecurrent lift and is not periodic under `A`.

Thus

    z periodic of period p,
    2z periodic of period 2p

implies

    4z is nonperiodic.

This is exact; no FULL hypothesis is needed.

## Exact preperiod of 4z

Let

    r = min{s>=0 : a_s=1}.

Since `a_0=0` and `a_p=1`,

    1 <= r <= p.

The second lift recurrence `d_(s+1)=a_s OR d_s` started from `d_0=0` first joins the recurrent lift immediately after the first `a_s=1`. Therefore

    tau(4z)=r+1,

so

    2 <= tau(4z) <= p+1.

In terms of the first-layer trace,

    a_s = XOR_(j=0..s-1) c_j,

so `r` is the first time the prefix XOR of the bit-1 trace of the original `p`-cycle becomes one.

## Corollary: at most one doubling occurs in a periodic zero-extension prefix, and it is terminal

Consider a literal zero-extension chain

    z_q = 2^q u

that is periodic for `0<=q<Q`, with `z_Q` the first nonperiodic extension. Let `p_q` be the exact period of `z_q`.

The previous run proved

    p_(q+1) in {p_q,2p_q}

while both states are periodic.

The theorem above shows that if

    p_(q+1)=2p_q,

then `z_(q+2)` is necessarily nonperiodic. Therefore:

- there can be at most one period doubling in the whole periodic prefix;
- if a doubling occurs, it must be the final periodic transition `z_(Q-2) -> z_(Q-1)`;
- all earlier periodic states have the same exact period `p_0`.

So the previous suggestion that a deep periodic prefix might be sustained by repeated doublings was too permissive. Repeated doubling is impossible.

## Consequence for periodic-prefix length

Use the existing depth/period obstruction

    q < 2 p_q

for every periodic `z_q`.

If no doubling occurs, then `p_q=p_0` throughout `0<=q<Q`, so at the terminal periodic state

    Q-1 < 2p_0,

hence

    Q <= 2p_0.

If a doubling occurs, it can only occur at `Q-2 -> Q-1`. Therefore `z_(Q-2)` still has period `p_0`, and

    Q-2 < 2p_0,

hence

    Q <= 2p_0+1.

Thus every periodic literal zero-extension prefix satisfies the universal bound

    Q <= 2p_0+1,

where `p_0` is the exact period of the starting periodic state `u`.

The canonical run-11 example is sharp:

    u=25,
    p_0=2,
    Q=5=2p_0+1.

Its terminal transition `200 -> 400` doubles period `2 -> 4`, and the theorem forces the next extension `800` to be nonperiodic. The exact exit preperiod is `3=p_0+1`, again attaining the upper bound above for the doubling case.

## Research consequence

This is useful progress but also closes the previous preferred inter-plateau mechanism. Cycle period is not an indefinitely accumulating potential inside a negative plateau: a doubling immediately forces exit on the next zero lift.

The remaining inter-plateau question must therefore use the starting period `p_0` of the physical row `u=T^H(v)`, or another quantity transported between distinct plateaus. A productive next target is to relate `p_0` for one post-threshold plateau to the next plateau's height/increment under physical evolution, rather than expecting repeated doublings within one plateau to store arbitrary debt.
