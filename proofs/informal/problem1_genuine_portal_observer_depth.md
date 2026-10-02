# Problem 1: genuine p32 portal observer depth

Status: exact finite-domain observer census on the sixteen genuine period-32
portal roots. This is not an all-scale theorem. Problem 1 remains OPEN.

## 1. Question

The all-depth finite-stack phase quotient gives an exact normalized state orbit
for any finite number r of post-normalization dynamic layers. Run 20 found a
genuine collision: portals 5 and 6 have the same complete unlabeled quotient
orbit through the fifth connector lift but opposite p32 root parity.

This note asks a narrower finite question:

> On the actual set of sixteen p16 leaf portals, what is the smallest stack
> depth at which the unlabeled quotient orbit ceases to mix odd and even p32
> root outcomes?

Here r=1 is the third connector lift after the universal two-lift
normalization, so r=3 reaches the fifth connector lift and r=4 reaches the
sixth.

## 2. Exact census

For each of the sixteen known p16 leaf representatives, reconstruct the
antiperiodic doubled portal, generate the first r dynamic lifts exactly, apply
the phase normalization from run 20 at every temporal phase, and canonicalize
the resulting cyclic sequence of 2r-bit quotient states by rotation.

The exact counts are:

| dynamic layers r | connector lift reached | distinct unlabeled root orbits | mixed endpoint-parity classes |
|---:|---:|---:|---:|
| 1 | 3 | 15 | 1 |
| 2 | 4 | 15 | 1 |
| 3 | 5 | 15 | 1 |
| 4 | 6 | 16 | 0 |
| 5 | 7 | 16 | 0 |
| 6 | 8 | 16 | 0 |
| 7 | 9 | 16 | 0 |
| 8 | 10 | 16 | 0 |

At r=1,2,3 the one mixed class is exactly

    portal 5: odd singleton
    portal 6: even branching.

No other genuine roots collide even at r=1.

At r=4 the sixth connector lift separates portals 5 and 6, and in fact all
sixteen genuine roots have distinct unlabeled quotient orbits. They remain
distinct through r=8.

Thus, on this finite genuine p32 domain,

    boxed:
    the sixth-lift unlabeled quotient orbit determines the root identity and
    therefore its first-return parity.

The statement is finite-domain only. Run 20 already gives arbitrary odd
drivers with equal unlabeled quotient orbits at every r=4,...,8, so this
injectivity cannot be extrapolated to all periods or all odd drivers.

## 3. No affine state-visit parity readout

The r=4 quotient orbits collectively visit 29 distinct 8-bit states.

For each root, form the GF(2) feature vector consisting of

- a constant bit, and
- the parity of the number of visits to each of those 29 states.

Exact Gaussian elimination on the sixteen genuine roots is inconsistent with
their odd/even endpoint labels. Therefore

    no affine GF(2) combination of sixth-lift state-visit parities
    decides the p32 root endpoint parity.

So the sixth layer contains enough information to distinguish the sixteen
roots, but the distinction is not captured by the simplest phase-invariant
linear counting observable.

This is a scoped no-go, not a claim against nonlinear or labeled observers.

## 4. Interpretation

The finite p32 root set has a very sharp observer boundary:

- through lift 5, exactly one proof-relevant bit is hidden, witnessed by
  portals 5/6;
- lift 6 transports that hidden bit and separates the final collision;
- no additional separation is needed for the other fourteen roots.

This supports the run-20 blind-label mechanism directly on the complete
genuine-root census. It also shows why merely increasing state depth is not
yet a proof: arbitrary-driver observer collisions persist beyond this point,
and even on the genuine roots the parity is not a linear state-visit count.

The next structural target remains a recursive law for which blind labels must
be transported as r grows, ideally tied to a finite-support resource rather
than to an ever-growing raw stack.

Reproducer:

    experiments/problem1_nonperiodicity/analyze_genuine_portal_observer_depth.py

Atomic record:

    results/problem1/20261002_genuine_portal_observer_depth.json

Dependencies:

    problem1_portal_multilift_phase_quotient.md
    problem1_period32_complete_portal_root_census.md
