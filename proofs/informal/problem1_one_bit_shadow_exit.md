# The exact shadow bit deciding a one-bit-strip exit

Status: `partial-proof` for the conditional whole-spacetime statements;
`finite-exhaustive` only for the32 local algebra controls. External review
is missing. No infinite FULL orbit or eventual K=1 exclusion is established.
Problem1 remains OPEN.

## 0. Admission

The earlier one-bit episode theorem proves a return at a lag-one u gate
ASSUMING that the future stays in the one-bit strip. The global shadow and
new gate criterion allow the alternative to be located before that future
assumption is imposed. Determine which exact shadow datum decides whether
the step returns or exits the strip. Either outcome sharpens the missing
constraint; no source, driver or longer episode is searched.

Keep ONE actual FULL spacetime and its original complete finite fringe,
together with the uniquely selected global shadow. At an even time t assume

    d_i(t)=0 for all i<=-1, d_0(t)=ell in {0,1}.     (1)

Do not assume (1) at later times. Write u=1[(r_1(t),r_2(t))=00],
h=hat r_1(t), and hat u=1[(hat r_1(t),hat r_2(t))=00]. The actual gate
is u when u=1 and t when u=0. The complete two-step alternatives are

| initial ell | actual gate | shadow condition | d_0(t+1) | d_-1(t+2) | d_0(t+2) |
| --- | --- | --- | --- | --- | --- |
| 0 | either | any | 0 | 0 | u XOR hat u |
| 1 | t | any h | 1 XOR h | 0 | 1 |
| 1 | u | h=1 | 0 | 0 | 0 |
| 1 | u | h=0 | 1 | 1 | 0 |

Every position<=-2 agrees at t+2. Thus the last row is an EXIT: the center
has resynchronized, but the left neighbor now differs. It is not a return
to a cyclic row. The penultimate row IS a return, and the lag-one t row
stays a one-bit disagreement without a future strip assumption.

## 1. Direct derivation (`partial-proof`)

At the source the common left neighbor is1. It masks the center discrepancy
in the update at position-1. Thus all positions<=-1 agree at t+1. The
actual odd center is0, while its shadow value is

    1 XOR ((1 XOR ell) OR h).

Consequently epsilon=d_0(t+1) is0 if ell=0 and1 XOR h if ell=1.
At the odd row FULL and the actual right pair give

    r_1(t+1)=u, r_-1(t+1)=1 XOR u.                 (2)

The left neighbor still agrees, so its next discrepancy is exactly

    d_-1(t+2)=u*epsilon.                            (3)

At the center, subtracting the two physical update rules gives

    d_0(t+2)=u XOR (epsilon OR hat r_1(t+1)),
    hat r_1(t+1)=(1 XOR ell) XOR
                     (hat r_1(t) OR hat r_2(t)).   (4)

For ell=0, (4) is u XOR hat u, the cyclic-source birth law. For ell=1,
if h=0 then epsilon=1 and (4) is1 XOR u; if h=1 then epsilon=0 but
hat r_1(t+1)=1, again giving1 XOR u. Equations(3)-(4) give the table.
Positions<=-2 only read the already agreeing negative half at the odd row.

There is also an exact least-delay obstruction in the exit case. At time
t+1 only the center differs, and its common left neighbor is0 by(2).
One A step therefore preserves that lowest discrepancy, by the imported
highest-disagreement rule. Since the shadow cut is the phase-correct cycle
representative,

    ell=1, u=1, h=0 => tau(Y_(t+1))>=2.            (5)

The finite least delay exists on the fixed finite actual orbit. Equation(5)
does not assign a specific later delay or a growth rate.

## 2. Relation to the conditional episode result

Under an EVENTUAL all-physical bound tau(Y_s)<=1, the imported threshold
transport also gives agreement of all negative positions sufficiently late.
Equation(5) therefore excludes h=0 at every sufficiently late lag-one u
source. The required condition is precisely

    ell=1 and u=1 => hat r_1(t)=1.                  (6)

Then the table recovers the earlier lag-one t persistence and u return by
a separate physical-cell derivation. It also identifies the missing exit
branch when the future K=1 premise is withheld.

More generally, as long as the negative halves currently agree, the ONLY
possible failure of that agreement on the next physical step is the bit at
-1. Under FULL it is automatically shielded at even times; at odd times
the exact condition for continuing agreement is

    r_1(s)*d_0(s)=0, s odd.                         (7)

For the given two ACTUAL spacetimes, initial agreement plus (7) at every
later odd time is necessary and sufficient for preserving the one-bit
strip, by induction on physical time. It is not a way to choose a new
left neighbor or force a replacement center trace on the shadow.

These formulas retain the entire actual/shadow evolution. They are not an
autonomous update of (ell,u,h): the next h depends on the wider shadow
fringe and, after a birth, its own center values. Nor is this a sufficiency
theorem constructing a finite initial left half from freely chosen right
half trajectories. The actual FULL and global E premises remain required.

## 3. Fixed verification and limits

`experiments/problem1_nonperiodicity/check_round305_shadow_exit.py` checks
all32 combinations of ell in{0,1} and the two actual/shadow right pairs.
It chooses the common left cells at-1,-2,-3 to be1,u,1 XOR u, respectively;
these are enough to give the actual centers1,0,1,0 locally. Direct whole-row
Boolean-cell evolution is compared with the independently evaluated table
for both center differences and the left-neighbor difference. All further
left output differences are also checked to be zero as asserted.

These32 cone assignments are ONLY a Boolean-identity test. The second row
in such a test is not asserted to be the global cycle shadow of the first,
and neither is asserted to have an infinite FULL continuation. Thus the
test supplies no new sources or counterexamples on the admissible domain.
The exact delay implication(5) is a mathematical deduction using E, not
an empirically inferred delay of the arbitrary local test rows.

Admission fixed before execution: a disagreement invalidates this local
table; agreement verifies only those32 cases. Caps: one local CPU,
10 seconds,128MiB, three physical steps,128KiB output. The atomic record is
`results/problem1/20260907_round305_shadow_exit.json`.

The next K=1 question is whether the full original finite boundary can
sustain(6) at every late lag-one u source while continuing to create the
required cyclic-source gate disagreements. Neither impossibility nor
existence is proved. Do not enumerate more local h patterns or episodes
to substitute for that all-time, one-orbit constraint.
