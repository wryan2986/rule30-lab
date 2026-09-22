# Astra automation handoff — run 212

Problem 1 remains OPEN.

## New result

Run 211's abstract n-bit fiber now has an exact recurrence.  Write

    y = 2^n r + c,  0 <= c < 2^n,

and let u=bit_0(r), v=bit_1(r).  For n>=2,

    s1 = (c>>1) | (u<<(n-1)),
    s2 = (c>>2) | (u<<(n-2)) | (v<<(n-1)),
    Phi_n(r,c) = s2 XOR (s1 OR c).

Then exactly

    A(2^n r+c) = 2^n A(r) + Phi_n(r,c).

In bits,

    c'_i = c_(i+2) XOR (c_(i+1) OR c_i),  0<=i<=n-3,
    c'_(n-2) = u XOR (c_(n-1) OR c_(n-2)),
    c'_(n-1) = v XOR (u OR c_(n-1)).

Thus the common base orbit drives only the top two fiber bits.  For the tower 2^n x the fiber starts at zero and is a triangular finite-speed transducer driven by the low-two-bit word of A^k(x).

Full proof: `proofs/informal/problem1_run212_exact_nbit_fiber_recurrence.md`.

## Strategic consequence

Boundary information propagates downward at at most two bit positions per A-step.  A top-boundary disturbance cannot affect bit i before ceil((n-1-i)/2) steps.  Therefore a uniform O(1) synchronization theorem does not follow from projection compatibility and should not be pursued naively.

Next target: once A^k(x) reaches its eventual period, compose Phi_n over one base period and study the resulting n-bit return map from the zero fiber.  Seek a genuine erasing/contraction or amortized transient theorem for that return map strong enough to exclude infinitely many above-diagonal renewals.  The exact recurrence should be used rather than treating rho_n as independent reset gaps.
