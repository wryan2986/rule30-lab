# Exact transport of the third return-shadow bit

Status: `partial-proof` / stopping-fence advance. Problem 1 remains OPEN.

## Setup

Continue the sufficiently late TWO-BIT nonresetting source `t` and put `q=t+2`. Run161 proves that the only remaining positive terminal hidden-slack case `g_(t+5)=1` has

    (d_2,d_3,d_4,d_5)=(0,0,2,3),
    (hat r_1,hat r_2,hat r_3)(q)=(1,0,0),
    (r_1,r_2,r_3)(q)=(1,0,1),
    m(q)=3.

The next requested check was to transport `hat r_3(q)` explicitly from the source-t global shadow driver.

Keep the SAME original global E-shadow. From `problem1_nonreset_return_birth_spacing.md`, at the TWO-BIT source `u=0`,

    shadow cells (-2,-1,0,1,2) at t = (0,0,0,0,1).

Write

    a = hat r_3(t),
    b = hat r_4(t),
    c = hat r_5(t).

No reinitialization of the shadow is made.

## Two-step Rule-30 transport

Use `F(l,x,r)=l XOR (x OR r)`.

At time `t+1`, the cells needed to compute position 3 at `q=t+2` are

    hat r_2(t+1) = 0 XOR (1 OR a) = 1,

    hat r_3(t+1) = 1 XOR (a OR b) = NOT(a OR b),

    hat r_4(t+1) = a XOR (b OR c).

Therefore

    hat r_3(q)
      = 1 XOR ( NOT(a OR b) OR (a XOR (b OR c)) ).

A four-case split on `(a,b)` (with `c` needed only when `(a,b)=(1,0)`) simplifies this exactly to

    boxed: hat r_3(q) = a * (b OR c).                (1)

This is the direct one-cell extension of the previously proved return pair

    (hat r_1(q),hat r_2(q))=(1,0)

for the two-bit source.

## Consequence for the last positive hidden-slack case

Run161 requires `hat r_3(q)=0`. By (1), the entire `g=1` branch therefore requires

    boxed: a * (b OR c) = 0.                        (2)

Equivalently,

    a=0  OR  (b,c)=(0,0).

Thus positive hidden slack is now translated completely back to a source-t condition on the original global shadow driver.

## Stopping fence

Equation (2) is NOT contradictory to the currently established nonreset-return identities. In particular, the older return theorem deliberately left `(a,b)` as unrestricted wider shadow-driver bits, and its all-depth conclusions for the two-bit source used `u=0`, which makes the forced later birth independent of `(a,b)` and of still wider cells. The new bit `c` likewise does not occur in those established gate/core identities.

Hence transporting one more shadow cell does not by itself exclude `g=1`. The exact remaining obstruction is now:

    g=1
      => source-t global-shadow driver satisfies a*(b OR c)=0,
         while the distinguished q-source first differs from that shadow at position 3.

Any contradiction must supply a genuinely new all-depth restriction on the source-t global E-shadow driver `(a,b,c,...)`, not another consequence of the already-used return pair or cyclic-core quotient.

This also identifies a clean witness-search target: search finite FULL actual rows together with their ORIGINAL E-shadow for a sufficiently late two-bit nonresetting source satisfying the distinguished passage and `a*(b OR c)=0`; do not restart the shadow locally at `t` or `q`.

Dependencies: `problem1_run161_g1_forces_unique_front_itinerary_and_shadow_bit.md`; `problem1_nonreset_return_birth_spacing.md`; `problem1_global_discrepancy_front.md`.
