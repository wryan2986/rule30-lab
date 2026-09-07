# Admission: a width bound on the complete transient

Status: `inconclusive` pending the fixed falsification test below.
Problem1 remains OPEN. No all-depth width bound is assumed.

## 0. Why this is a different route

The round305 full-driver phase-map counterexample blocks a specific history
compression. It does not rule out a direct bound on the complete transient.
The earlier highest-wait note refutes controlling total delay by its FIRST
erasing wait; it does not establish or refute a bound by full spatial width.

Test the precise proposed all-depth statement

    tau(y) <= bitlen(y)-1 for EVERY finite y>0.      (W)

This has a concrete consequence on the current bottleneck. For one original
finite row, keep its ENTIRE finite right fringe. If its leftmost1 is at-L+1,
then for t beyond its right support, the initial cut L_t has width L+t and
the actual center-and-left row is Y_t=A^t L_t. Thus(W) would imply

    tau(Y_t)=max(tau(L_t)-t,0)<=L-1.                (1)

This would establish an eventual uniform delay bound for each fixed finite
row (with the displayed dependence on its original left extent). It would
not itself exclude every finite-width strip or solve Problem1.
Here L>=1 presumes the chosen center is at or right of the initial left edge;
one fixed rebase, if needed, retains the full actual fringe.

Rankings are `heuristic`: this scalar FULL-independent bound is cheap to
falsify and stronger than needed; if false, do not fit a larger intercept
or collect a growth profile. Instead inspect whether the exact obstruction
admits an all-depth unbounded-excess family. The original shift-tower
sampling prohibition remains in force: no sequence tau(2^n*x) is sampled
to estimate its growth rate.

## 1. Hand controls and finite test scope

The complete width-at-most-three hand graph is

    0->0, 1->1, 2->3, 3->3,
    4->7, 5->6, 6->6, 7->6.

The bound holds for these seven positive inputs, with equality for2 and4.
The least delay of0 is0 and it is excluded from(W).

The admitted finite falsification test examines positive integers in
increasing order, stopping at the FIRST violation or at4095 (width12).
It compares two simple implementations: packed shifts/XOR/OR and explicit
Boolean cells, with separate finite-orbit detection. Every observed edge
must agree; the bound uses LEAST preperiod, not time of an arbitrary repeat
or first occurrence of the phase-correct representative.

A counterexample must include its entire closed transient-and-cycle
certificate, exact delay, width and core. Agreement through4095 would be
`finite-exhaustive` only on that finite set and leave(W) unproved. Either
outcome changes whether this proposed all-depth bound remains a possible
route to(1). It is not a center-prefix, phase-source or period census.

Resource caps: one local CPU worker,30 seconds,128MiB,4096 updates per
individual orbit,256KiB final output. Every result is written atomically
with the protocol's parameters, full Git, software/hardware, timing and
hash fields. Stop on a mismatch, cap breach or first violation. No larger
bound or refitted constant is authorized by this test.
