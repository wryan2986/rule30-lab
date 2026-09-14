# Astra automation handoff — run 13

Problem 1 remains **OPEN**.

This run starts from branch head `ed1b0fd6a21390eb7ebb1c0e542fe6b5b3695191` and adds `proofs/informal/problem1_period_doubling_forces_next_exit.md`.

## New theorem: a doubled-period zero lift forces the next zero lift to be nonperiodic

Let `z` be `A`-periodic of exact period `p`. Suppose its zero one-bit lift `2z` is periodic of exact period `2p`.

The previous lift-period classifier implies that along the `p`-cycle of `z`,

    b_s = bit_0(A^s(z)) = 0

for every `s`, and

    XOR_s c_s = 1,

where `c_s=bit_1(A^s(z))`.

Write

    A^s(2z)=2A^s(z)+a_s,

with `a_0=0`. Then

    a_(s+1)=a_s XOR c_s,

so `a_p=1`. Thus the `2p`-cycle of `2z` contains an eraser in its low-bit trace.

Now lift once more:

    4z = 2(2z)+d_0,
    d_0=0.

Because `bit_1(A^s(2z))=b_s=0`, the second lift bit satisfies

    d_(s+1)=a_s OR d_s.

Since some `a_s=1`, the unique recurrent initial second-lift bit is `d_0=1`. Therefore the actual zero lift `d_0=0`, namely `4z`, is nonperiodic.

Hence

    period(z)=p,
    period(2z)=2p

implies

    tau(4z)>0.

Moreover, if

    r=min{s>=0:a_s=1},

then

    tau(4z)=r+1,

and because `a_p=1`,

    2 <= tau(4z) <= p+1.

## Consequence: repeated period doubling inside one periodic zero-extension run is impossible

For a literal chain

    z_q=2^q u

periodic for `0<=q<Q`, the previous run proved

    p_(q+1) in {p_q,2p_q}.

The new theorem shows that if one doubling occurs at `q -> q+1`, then `z_(q+2)` is already nonperiodic. Thus:

- there is at most one doubling in the whole periodic prefix;
- if present, it is the final periodic transition `z_(Q-2)->z_(Q-1)`;
- all earlier periodic states have the starting period `p_0`.

Combining with the depth/period bound `q<2p_q` gives

    Q <= 2p_0+1.

If no doubling occurs, the slightly stronger bound is

    Q <= 2p_0.

The canonical example `u=25` is sharp:

    p_0=2,
    Q=5=2p_0+1,

with terminal doubling `200 -> 400` and forced nonperiodic next lift `800`, whose preperiod is `3=p_0+1`.

## Important correction to the previous preferred route

The run-12 handoff suggested that repeated period doublings might form an accumulating non-telescoping potential capable of storing inter-plateau debt. That mechanism is now ruled out inside a single periodic zero-extension prefix. A doubling does not allow the prefix to continue: it forces exit immediately on the next zero lift.

So the next useful target is not repeated doubling. Instead relate the **starting period `p_0` of the physical row** `u=T^H(v)` to later plateau heights/rises or to the next physical-row restart. Any inter-plateau compensation theorem must transport information across distinct physical rows/plateaus, not through multiple doublings within one plateau.

New proof commit before this handoff: `fb80b0c372930dbe19f3409adb8d76ed046d8de4`.
