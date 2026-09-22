# Problem 1 run 212 — exact n-bit fiber recurrence

Problem 1 remains open.

## Setup

Use the reviewed finite-state scan map

    A(q) = (q >> 2) XOR ((q >> 1) OR q).

Run 211 proved the exact factor identity

    floor(A(y)/2^n) = A(floor(y/2^n)).

Write a state uniquely as

    y = 2^n r + c,   0 <= c < 2^n,

where `r` is the base state and `c` is the n-bit fiber.  Let

    u = bit_0(r),   v = bit_1(r),   M = 2^n-1.

For n >= 2 define

    s1 = (c >> 1) | (u << (n-1)),
    s2 = (c >> 2) | (u << (n-2)) | (v << (n-1)).

Then direct substitution into A gives the exact skew-product recurrence

    A(2^n r+c) = 2^n A(r) + Phi_n(r,c),

with

    Phi_n(r,c) = s2 XOR (s1 OR c).

(The right side is automatically in [0,2^n); equivalently mask by M.)

Thus the n-bit fiber is driven by only the two least-significant bits of the base orbit.

## Bit form

Writing c_i for bit i of c, the update is

    c'_i = c_{i+2} XOR (c_{i+1} OR c_i),        0 <= i <= n-3,
    c'_{n-2} = u XOR (c_{n-1} OR c_{n-2}),
    c'_{n-1} = v XOR (u OR c_{n-1}).

So the base orbit enters the fiber only through its top two bits; the interior update is exactly the same local Boolean rule at every n.

For the zero-extension tower y=2^n x, the initial fiber is c_0=0 and the driver is the low-two-bit word of A^k(x).  Hence

    A^k(2^n x) = 2^n A^k(x) + c_{n,k}

where c_{n,0}=0 and

    c_{n,k+1}=Phi_n(A^k(x),c_{n,k}).

This is an explicit recurrence for the object isolated abstractly in run 211.

## Exact finite-speed / dependency cone

The bit recurrence gives a useful causal statement.  After one step, output bit i depends only on old fiber bits i,i+1,i+2 (except at the top boundary, where the two driver bits enter).  Inductively, after k steps, bit i depends only on initial fiber bits

    i, i+1, ..., min(n-1,i+2k)

and on those base-driver symbols whose boundary influence can reach that cone.

In particular, a disturbance introduced at the top boundary cannot affect fiber bit i before at least

    ceil((n-1-i)/2)

steps.  The n-bit extension is therefore not a collection of independent reset gaps: it is one triangular, finite-speed transducer fed from the common base orbit.

## Consequence for the research direction

This explains why synchronization delays naturally grow with extension depth and why a naive bounded-delay theorem is implausible.  More importantly, it gives a concrete finite object for the required amortized theorem: once the base orbit is periodic, compose the maps Phi_n over one base period.  The remaining question is the transient/synchronization behavior of the zero fiber under that periodically driven n-bit return map.

A contradiction to FULL would require a theorem strong enough to exclude infinitely many above-diagonal renewals, not merely a pointwise finite-speed estimate.  The present recurrence does not supply that contraction theorem.

## Checked dead end / warning

The projection compatibility by itself does not imply that the n-bit fiber synchronizes in O(1) time.  Boundary information can require order n steps just to reach the low end of the fiber.  Future work should therefore analyze the period return map (or find a monotone/erasing quantity for it), rather than try to prove a uniform synchronization bound from the factor map alone.
