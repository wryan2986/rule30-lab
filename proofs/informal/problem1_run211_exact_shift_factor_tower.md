# Problem 1 run 211 — exact shift-factor tower

Problem 1 remains OPEN.

Run 207's adjacent-level identity extends to a useful common-origin statement that is stronger than treating the reset gaps at different tower levels independently.

Use

    A(q) = (q>>2) XOR ((q>>1) OR q).

For every finite nonnegative integer y, write y=2q+d with d in {0,1}. The run-207 calculation gives

    A(y) = 2 A(q) XOR d'

for some d' in {0,1}. Therefore

    floor(A(y)/2) = A(floor(y/2)).                 (1)

So deletion of the least-significant bit is an exact factor map of the A dynamics, not merely an identity valid when the input is even.

Iterating (1) in time gives, for every k>=0,

    floor(A^k(y)/2) = A^k(floor(y/2)).             (2)

Iterating the spatial projection n times gives

    floor(A^k(y)/2^n) = A^k(floor(y/2^n)).         (3)

In particular, for one fixed finite origin x and its zero-extension tower q_n=2^n x,

    floor(A^k(q_n)/2^n) = A^k(x)                  (4)

for every n,k>=0. More generally, for 0<=m<=n,

    floor(A^k(q_n)/2^(n-m)) = A^k(q_m).           (5)

Thus all levels of the shift tower form an exact inverse system under least-significant-bit deletion. At every time k, the entire discrepancy between level n and the n-bit lift of the base orbit is confined to the n newly appended low bits:

    A^k(2^n x) = 2^n A^k(x) + c_{n,k},
    0 <= c_{n,k} < 2^n.                            (6)

(The `+` is ordinary integer addition; the high and low bit blocks are disjoint.)

## Consequences for preperiods

If A^k(q_n) is periodic from time t, then every projection q_m with m<n is periodic from time t by (5). Hence

    tau(q_0) <= tau(q_1) <= ... <= tau(q_n),

recovering run 209 monotonicity simultaneously for the whole tower.

More importantly for run 210, the reset-gap variables rho_n are not dynamics of unrelated eventual cycles. The eventual cycle at level n-1 projects, at the same time phase, onto the eventual cycles of every lower level once those lower levels have entered their cycles. The one-bit defect automaton of run 207 is exactly the fiber extension from one member of this inverse system to the next.

Consequently any future bounded-reuse argument should be formulated on the nested low-bit fiber c_{n,k}, not by charging rho_n to independent cycle words. Equation (5) is the exact common-origin compatibility that was missing from the run-210 formulation.

## A precise synchronization interpretation

Let a_n=tau(q_n). Since a_n is nondecreasing, at time a_n every lower level q_m (m<=n) is already on its eventual cycle. Equation (5) says the level-n cycle state at that time projects to the simultaneous phase of every lower cycle. Therefore a positive increment a_n-a_(n-1)=rho_n is exactly the extra synchronization time needed by the newest one-bit fiber after the entire (n-1)-level factor has already become periodic. No higher-level transient can be attributed to renewed transient behavior in any older high-bit factor.

This does not by itself bound the sum of the rho_n: an n-bit triangular fiber can in principle keep introducing new synchronization delays. But it rules out arguments that treat a long rho_n as fresh behavior of the full ancestry. The only genuinely new state at tower step n is one additional low fiber bit, driven by the already-periodic lower factor.

## Remaining obstruction

The needed theorem is now a synchronization bound for this nested triangular fiber system. One must show (or refute) that, for a tower generated from one fixed finite x, the successive one-bit synchronization delays rho_n cannot keep producing the late-renewal condition

    a_(n-1) + rho_n > b+n

infinitely often. Equation (5) supplies exact cross-level compatibility, but no such bound has yet been proved.
