# Problem 1: exact transport for genuine high-bit projections

Status: `partial-proof`; exact for projections of one common-origin orbit, but not yet shown to apply to the forced states attached to doubling passages.

## Exact factor identity at arbitrary depth

For the accelerated Rule-30 map

    (A x)_i = x_(i+2) xor (x_(i+1) or x_i),

run 38 used the one-bit factor identity

    A(x) >> 1 = A(x >> 1).

Iterating the shift gives, for every integer k>=0,

    A(x) >> k = A(x >> k).                         (1)

Inducting on time then gives the stronger spacetime identity

    A^t(x) >> k = A^t(x >> k)                      (2)

for every t,k>=0. Equivalently, for every coordinate i,

    bit_i(A^t(x >> k)) = bit_(i+k)(A^t x).         (3)

Thus a temporal coordinate history of a *genuine projection* of the original realization is not merely approximately transported or event-counted: it occurs verbatim as a higher spatial column of that same original spacetime diagram, with no loss of time interval, parity, period, or two-time relations.

In particular, if a projected orbit y=x>>k contains a column b satisfying an antiperiodic relation

    b(t+q)=1 xor b(t)

on some time interval (or globally), then the corresponding column k+i of x satisfies exactly the same relation at the same times. Complete-period density and temporal-rank certificates are therefore preserved perfectly by projection.

## Consequence for the run-47 transport target

Run 47 asked for a theorem transporting complete antiperiodic doubling histories into one common-origin spacetime window. Equations (2)--(3) show that no new transport theorem is required for any doubling witness that can be identified as a coordinate of `A^tau(x) >> k` for the *same fixed original realization* x: its entire future history is already a literal column of the original orbit, shifted spatially by k and temporally by tau.

More generally,

    A^s(A^tau(x) >> k) = A^(s+tau)(x) >> k,         (4)

so a certificate on a projected state starting at passage time tau embeds verbatim in the original spacetime diagram starting at tau.

This reduces the global bridge to an identification question rather than a generic causal-transport question:

> For each genuine doubling passage supplied by the existing FULL/common-origin scan, is the finite periodic state whose new fiber is antiperiodic actually a high-bit projection of one common-origin state A^tau(x), or is it obtained by an additional low-bit forcing/reset operation?

If the former holds for infinitely many passages, the run-47 density witnesses already coexist as literal columns of the original spacetime diagram (though a further argument may still be needed to place enough of them inside one activity window). If the latter holds, (2)--(4) identify precisely where information is lost: the obstruction is the forcing/reset step, not evolution under A or spatial projection.

## Important limitation

The existing joint-window note explicitly warns not to replace the actual survivor by successive forced states, because the corrected gate bridge shifts ray depth downward and gives no depth-zero pullback. Therefore this note does NOT assert that the scan's forced periodic states are projections. That identification must be checked against the exact gate/source/return construction before using antiperiodic density on the original survivor.

## Dead end avoided

Do not seek a lossy event-by-event pullback for histories that are already genuine projections. Equation (3) gives exact history transport in that case. Future work should inspect the definition of the doubling-associated forced state and isolate its difference from `A^tau(x)>>k`; only that difference requires a new bridge.
