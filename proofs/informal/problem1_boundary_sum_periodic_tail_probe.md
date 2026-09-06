# Periodic spatial tails as a test of the boundary-sum bound

Status: `partial-proof` for the exact rational cycle and all-age cost law;
`finite-exhaustive` for the declared graph comparison. The general
subunit bound remains `inconclusive`. Problem 1 remains open.

## Admission (before execution)

The current route seeks an upper bound
`Psi_s <= alpha*s+C`, with `alpha<1`, on actual admissible forced
schedules. Such a bound, if valid on ordinary endpoints at all ages,
would contradict their exact padding lower bound under infinite survival.
Before trying to prove the stronger SCHEDULE-ONLY assertion, test whether
spatially periodic infinite tails already refute it. These are not finite
seeds and are never asserted to be ordinary endpoints.

Ranked routes (`heuristic`): (1) exact periodic-tail countermodels, because
their boundary growth rate is a finite-cycle calculation at ALL ages;
(2) a direct inequality retaining the original length and ordinary
membership; (3) a nonlinear observable on ordered histories. The first is
a bounded falsification test, not a new return or first-witness census.

For each spatial period p=1,...,12, represent the pure periodic 2-adic
integer by its low p bits a, namely a/(1-2^p). Its A evolution is the
cyclic p-cell map `(x>>2) XOR ((x>>1) OR x)`, with circular shifts.
The periodic tail of F is R=rotate_left_2 composed with A^2. An edge
between two periodic states is an EXACT forced edge when both states
have a gate (low four bits 7 or 11): F has output low two bits 11,
and agrees with R in every higher bit. Verify this algebra separately.

Enumerate only this finite functional graph and its cycles. Retain a
cycle only if its cyclic branch word avoids uu, ttttt, and ututtu.
For each retained cycle and each spatial alignment, compute the exact
periodic mean of the existing summand
`J(y)=I(A(y))+I(y>>2)`, where I tests low six bits 0 or 5.
The cycle and alignment give an exact arithmetic progression of ages,
so a mean at least 1 refutes every uniform subunit slope, without a
finite-to-infinite extrapolation. If no such cycle exists, close this
specific countermodel class through period 12; do not increase the cap
or claim the desired inequality. This separates a schedule-only route
from a route that must retain ordinary membership and age versus length.

Compare independent packed circular arithmetic and cell-array rules on
every admitted state. Hand controls at p=4 are A(7)=2, A(11)=1,
R(7)=14 and R(11)=7; the latter single edge does not form a survivor
cycle. Resource cap: one local CPU, 120 seconds, 1 GiB; no backends,
frontiers, coefficient searches or larger schedule atlas. Atomic records
must include the full Git commit, exact parameters, source hashes,
hardware/software, timings, limitations and exact cycle certificates.

The only infinite implications admitted here are proofs from the exact
cyclic model. Neither finite passage nor periodic spatial support settles
the whole-tail question for eventually-zero initial support.

## 1. Exact periodic-tail model (`partial-proof`)

Let `[a]_p=a/(1-2^p)` in the 2-adic integers, with `0<=a<2^p`.
Its digits repeat the low-to-high p-bit word a. Write `rot_j` for a
circular right shift by j bits. Then

    pi([a]_p)=[rot_2(a)]_p,
    A([a]_p)=[a_p(a)]_p,
    a_p(a)=rot_2(a) XOR (rot_1(a) OR a).

These follow bit by bit from
`A(x)=(x>>2) XOR ((x>>1) OR x)`. Define
`R_p=rot_(-2) composed with a_p^2`. The bits at positions >=2 of
`T(A([a]_p))` agree with `[R_p(a)]_p`; only the bottom two positions
can differ because T uses zero inputs below position zero, whereas a
circular computation uses the periodic continuation.

If a has gate u or t, the ACTUAL output `F([a]_p)=Q(A([a]_p))`
has low two bits 11. Thus whenever both a and R_p(a) have a gate,

    F([a]_p)=[R_p(a)]_p.                              (1)

Conversely, an F cycle of pure p-periodic tails must give a cycle
of this graph: equality in bits >=2 identifies the periodic word,
including its bottom two bits. This proves completeness at each fixed
p, independently of the enumeration. No assertion of completeness
over ultimately periodic tails with a spatial transient is made.

## 2. An explicit rational closed survivor (`partial-proof`)

For p=7 the hand table is

| a | a_7(a) | a_7^2(a) | R_7(a) | branch |
| --- | --- | --- | --- | --- |
| 7 | 38 | 126 | 123 | u |
| 123 | 1 | 97 | 7 | t |

Both outputs have the required low pair 11. Equation (1) therefore gives
the exact 2-adic identities

    X=-7/127  --u-->  Y=-123/127  --t-->  X.           (2)

This is a rational infinite-support cycle. It is not an ordinary
nonnegative integer orbit and not a finite-seed realization. By the
existing survivor uniqueness theorem, X is precisely the survivor of
`(ut)^infinity`; Y is the survivor of `(tu)^infinity`.

The repeating digits also give directly

    X = 903 mod 16384,
    X = 50055 mod 65536.                              (3)

For example the first three 7-bit copies are
`7+7*128+7*128^2`; its residues give (3).
For EVERY requested b>=4 take the residue
`a=(-7)*127^(-1) mod 2^(b+12)`. It has the six gates ututut,
and `F^6(a)=a mod 2^b` by the two-bit precision loss per forced step.
All-width ordinary controllability supplies a finite ordinary endpoint
in that residue class in either phase. This is an explicit alternative
to the abstract survivor/four-class-table closure used by
`problem1_all_residue_memory_rigidity.md`; it asserts neither one
ordinary word for all b nor a bound on its length.

## 3. Exact boundary growth on this cycle (`partial-proof`)

Extend the existing finite boundary expression to 2-adic endpoints:

    Psi_s(x)=sum_(t=0..s-2) J(pi^(s-t-2)(F^t(x))),
    J(y)=I(A(y))+I(pi(y)),
    I(z)=1 if z=0 or5 mod64, otherwise0.               (4)

Every expression uses finitely many bits at each fixed s. The
nonnegative-integer boundary identity therefore extends to these
endpoints by choosing sufficiently precise nonnegative representatives
with the same observed gates. There is no ordinary history attached
to X or Y, so (4) is not an assertion of their finite word costs.

Every rotation of the periodic word 7 has I=0: its three consecutive
ones and four consecutive zeros allow neither six zeros nor 000101.
Every rotation of 38 has I=0, since it has no run of three zeros.
Every rotation of 123 has I=0, since it has only one zero per period.
The word `a_7(123)=1` has I=1 for exactly one of its seven rotations:
its unique one must be outside the six tested positions. Hence J=0
at every rotation of X, and J=1 at exactly one rotation of Y.

For fixed s the summand sequence in t in (4) is 14-periodic.
At odd t on the X-started cycle (even t on the Y-started cycle),
the rotation advances through all seven possibilities over 14 steps,
because 4 is invertible modulo 7. Its total per 14 steps is exactly 1.
More explicitly, for X it pays precisely when

    t odd,  t = s-6 mod7,  0<=t<=s-2;                (5)

for Y replace odd by even. Consequently, for either Z=X or Z=Y,

    Psi_(s+14)(Z)=Psi_s(Z)+1       for EVERY s>=1,
    0 <= Psi_s(Z) <= ceil((s-1)/14).                 (6)

The slope 1/14 follows from this exact identity, not from fitting
computed ages. This admissible schedule therefore does not refute a
uniform subunit slope. The result controls only these two periodic
schedules; it gives no estimate for schedules with even one interruption.

## 4. Finite verification and next obligation

Status: `finite-exhaustive`. Packed circular arithmetic and a separate
cell-array rule agree on A, R and J for all 8,190 states at periods
1,...,12. Different functional-graph algorithms agree on every cycle.
There is exactly one cycle in this box, the two states at p=7 above;
its cyclic word ut avoids all three forbidden factors. The seven
alignment totals are all 1 over joint period 14. No larger spatial
period, ordinary frontier, return census or first-witness box was run.

Records:
`results/problem1/20260906_boundary_periodic_tails_primary.json` and
`results/problem1/20260906_boundary_periodic_tails_independent.json`.
The executable is
`experiments/problem1_nonperiodicity/check_boundary_sum_periodic_tails.py`.
Both records retain the pre-execution admission text and executed
source, hashes, base Git, exact parameters, local machine facts and
timings, and were written atomically. An initial independent small-period
indexing error was corrected before the accepted matching run; no failed
comparison is presented as validation. Both computations are lead-local.

Fresh Muse adversarial review accepted the exact model, rational cycle,
all-age cost law and finite scope. The review and reviewed source snapshot
are archived in `results/problem1/20260906_boundary_survivor_muse_review.json`.

The existing `problem1_periodic_schedule_rationality.md` already proves
rationality for every eventually periodic auxiliary schedule. That theorem
is reused, not rediscovered here. The explicit ut cycle and its boundary
functional are the new specialization.

The bounded countermodel class is now closed through its admitted cap.
Do not enlarge it. The rational cycle improves the separate all-memory
closure dependency and supplies an exact cost control. The main research
obligation remains an inequality on general ACTUAL return histories
retaining original length and all gates, or an observable using ordered
history information beyond fixed additive residue weights.
