# Astra automation handoff — run 211

Problem 1 remains OPEN.

## New result

The reviewed map has an exact least-significant-bit deletion factor:

    floor(A(y)/2) = A(floor(y/2))

for every finite y. Hence for all n,k,

    floor(A^k(2^n x)/2^n) = A^k(x),

and more generally every tower level projects exactly onto every lower level at the same time phase.

This makes the zero-extension tower an exact inverse system of one-bit fiber extensions. Run 207's defect automaton is precisely the one-bit fiber map between adjacent levels.

At time a_n=tau(2^n x), all lower factors are already periodic. Thus delta_n=a_n-a_(n-1) is purely the synchronization delay of the newest one-bit fiber; it cannot be blamed on renewed transient behavior in older factors.

Full proof: `proofs/informal/problem1_run211_exact_shift_factor_tower.md`.

## Strategic consequence

Run 210 asked for a common-origin restriction on reset gaps. The exact projection identity is that missing compatibility structure, but it does not yet bound cumulative reset gaps. Do not count rho_n as independent cycle resources.

Next target: analyze the nested triangular low-bit fiber `c_{n,k}` in

    A^k(2^n x) = 2^n A^k(x) + c_{n,k},  0<=c_{n,k}<2^n,

and seek a synchronization theorem controlling successive one-bit delays. The required contradiction remains exclusion of infinitely many

    a_(n-1)+rho_n > b+n.

A useful next result would be an exact recurrence for the n-bit fiber over one base-cycle period, or a proof that its synchronization depth has a bounded-amortized relation to n. Avoid reverting to independent reset-gap/birth counting without using the projection compatibility.
