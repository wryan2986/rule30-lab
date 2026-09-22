# Problem 1 run 202 — finite fringe reduces the global tail to one shift-tower delay sequence

Status: `partial-proof`. Problem 1 remains OPEN.

Continue only the corrected run-193--201 chain. Run 201 shows that the newly exposed complete-driver bits are exactly residence erasers, so further local propagation does not create a new finite resource. The useful consequence of retaining the COMPLETE ORIGINAL FINITE RIGHT FRINGE is instead an exact scalar reduction of every sufficiently far-right residence to one zero-extension tower.

## 1. Exact tail reduction

Let `b` be the rightmost occupied site of the fixed original finite row and put

    x = L_b > 0.

For every `n>=0`, the original cut ending at `b+n` merely appends `n` zero bits, hence

    L_(b+n) = 2^n x.

With the global-front notation `s_j=tau(L_j)`, this gives the exact identity

    s_(b+n) = tau(2^n x).                                      (1)

Thus after the original fringe ends, the complete threshold sequence is not an arbitrary family of cuts. It is the single scalar shift-tower delay sequence

    a_n := tau(2^n x).

The older zero-extension theorem proves `a_n -> infinity`, but supplies no rate relative to physical depth.

## 2. Residence lengths are first differences of the shift-tower delay

The established global residence law says characteristic `j` is occupied on

    [s_(j-1), s_j) intersect Z.

Therefore for every `n>=1`, the complete residence length of characteristic `b+n` is exactly

    ell_n = a_n - a_(n-1) >= 0.                               (2)

Clock-doubling labels are precisely among the zero-length residences already identified by the global-front theorem; no new local driver is needed to describe them.

More importantly, the renewal portion after the front has crossed the physical center is, from the established formula

    R_t = max(s_(t+1)-max(s_t,t+1),0).

Taking `t=b+n-1` gives the exact finite-fringe tail formula

    R_(b+n-1)
      = max(a_n - max(a_(n-1), b+n), 0).                       (3)

Hence a positive late renewal is equivalent to

    a_n > max(a_(n-1), b+n).                                  (4)

This is stronger than merely saying `a_n` increases: the new threshold must both exceed the previous delay and lie strictly beyond the physical diagonal.

## 3. What FULL must force in this language

The imported FULL/renewal argument requires infinitely many positive late renewals. Because only finitely many indices lie inside the original fringe, (3) implies the following necessary condition for any alleged FULL finite seed:

    tau(2^n x) > max(tau(2^(n-1) x), b+n)

for infinitely many `n`. Equivalently, infinitely many strict increases of the zero-extension delay must occur while the new delay is already strictly above the physical diagonal `b+n`.

This isolates the missing global statement as a one-integer asymptotic problem. The previously proved theorem

    tau(2^n x) -> infinity

is insufficient: an unbounded nondecreasing integer sequence may remain below the diagonal forever, and even strict increases need not create positive `R` unless they occur above it.

Conversely, proving for every finite `x>0` that

    tau(2^n x) <= b+n

for all sufficiently large `n`, or more generally that (4) occurs only finitely often, would directly contradict FULL for the original finite seed. No ancestry injection or nonnegative path factorization would then be needed.

## 4. Why this is not the invalid driver-bit charge

Equation (1) uses only the fixed original finite fringe: beyond `b`, every cut is literally a zero extension of the same integer `x`. It does not map spacetime erasers injectively to original 1-bits, does not count active GF(2) paths, and does not treat complete-driver selector bits as independent resources.

Run 201's negative result therefore remains intact. The new reduction changes the target: instead of seeking bounded reuse of individual erasers, seek a diagonal-growth theorem for the single sequence `tau(2^n x)`.

The old `problem1_highest_wait_nonforcing.md` already proves `tau(2^n x)->infinity` and explicitly warns that it does NOT prove `tau(2^n x)>n` infinitely often. Equation (3) shows that this previously fenced-off rate question is exactly the global quantity needed once the fixed finite fringe and residence identity are combined. Sampling shift towers is still not evidence; the next useful work must be an all-depth upper/rate argument or a rigorous counterfamily to such an argument.

## 5. New target

For fixed finite `x>0`, study

    e_n := tau(2^n x) - n.

Equation (4) becomes

    e_n > b

and `a_n>a_(n-1)` at infinitely many late indices under FULL. A sufficient contradiction would be `limsup e_n < infinity` with a bound compatible with the fixed fringe, but the exact needed claim is only finiteness of indices satisfying (4).

No claim of that rate bound is made here. The contribution of this run is the exact reduction (1)--(4), which removes the need to invent a new ancestry charge and identifies the remaining finite-fringe obstruction as the diagonal growth of one zero-extension delay tower.

Dependencies: `problem1_global_discrepancy_front.md` Sections 1--4; `problem1_highest_wait_nonforcing.md` Sections 1--5; `problem1_run201_driver_bits_are_residence_erasers.md`.