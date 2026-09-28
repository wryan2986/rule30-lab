# Problem 1 run 326: alternating fiber depth-11 collapse

Status: exact exploratory calculation; Problem 1 remains OPEN.

Continue the Condrey alternating-fiber route with center trace 1010... and the
distinguished prefix R0,R1,R2=1,1,0. Left permutivity gives a unique L_n at
each depth.

The existing notes give L1,...,L5=1,0,1,0,1 and formulas through L9. Exact
truth-table inversion through the full depth-11 light cone gives the new
identity

    L11 = R3.

All dependence on R4,...,R10 cancels. The preceding bit is

    L10 = 1 + R3 + R6 + R3 R6 + R4 R6 + R3 R4 R6
          + R5 R6 + R3 R5 R6 + R4 R5 R6 + R3 R4 R5 R6

over GF(2). The simplification is isolated: the direct ANF for L12 has 106
monomials in R3,...,R11.

A generic short-gap latch is false. For the finite right half

    R0,R1,R2,R3 = 1,1,0,1,  and Rj=0 for j>=4,

the exact alternating completion has

    L54=L55=...=L60=0.

The row later returns to 1, so this is not a finite-support counterexample,
but it rules out any generic claim that every block of at most seven new left
bits contains a 1. It also corrects the earlier short-horizon observation
that only tiny terminal zero runs appeared.

Interpretation: L11=R3 is a useful low-memory return, but the unrestricted
alternating fiber is too flexible for a simple Condrey-style monotone latch.
The next test should impose the repository's FULL/cyclic-source return
constraints: express R3 at distinguished returns, then ask whether the
depth-11 identity recurs under the admitted source return map. If an
admissible return cycle resets it indefinitely, stop this route.

Reproducibility: recursively choose L_n so that the time-n center equals the
target alternating bit; left permutivity makes this choice unique. The
symbolic formulas were obtained by complete Boolean truth tables and the
GF(2) Moebius transform to ANF.
