# Projecting at the cut and pulling back

Status: both universal candidate gates are `refuted` by exact genuine-domain
counterexamples. Conditional inverse-branch facts below are `partial-proof`;
the 19-row replay is `finite-exhaustive`. Adjacent inclusion, B_all, signed
nonvanishing, and Problem 1 remain open.

## Strategy and admission

Direct rounded projection fails every positive-cut base prefix. The distinct
candidate from the handoff first moves the projection to the occurrence cut.
For a full-domain occurrence x in O_(a,k), k>=3, with base word w of length c,
put

```text
X=F^c(x),  R(X)=(X>>2) OR 3,
y=B_w(R(X)),
B_q(z)=4 P^(-1)(Q^(-1)(z))+3,  Q=T for t, U for u.
```

B_w means the inverse branches composed outer-to-inner in the order of w;
evaluation starts with the last letter of w. The inverses are the unique
2-adic inverses. Since R(X) is 3 modulo 4, the candidate follows w in Z_2.
Since the occurrence tail begins ut, its projected tail stops, so the
candidate's complete forced schedule is w if this construction is valid.
This terminal property is stronger than adjacent inclusion requires.

Candidate A: y is always a nonnegative finite integer on the full occurrence
domain. Candidate B: whenever y is a nonnegative finite integer, it lies in
O_(a,k-1). Together they would construct an adjacent shadow and, by the
separation lemma, exclude the boundary cuts. Neither is assumed true.

Route ranking (`heuristic`):

| Rank | Route | All-depth potential | Falsifiability / cost |
| --- | --- | --- | --- |
| 1 | Conjugated rounded projection at the base cut | Direct constructive adjacent inclusion if both gates hold | High / low on existing rows |
| 2 | Delete a generator from a representation while preserving the base word | Constructive shadow, but choice may require full representations | High on named witnesses / medium |
| 3 | Full endpoint correlation invariant across unequal returns | Could prove signed nonvanishing | Medium until specified / high |

Admitted check: only the 19 existing rows embedded in
`results/problem1/20260905_canonical_return_rows.json`, preserving their
complexity/phase/state/cut/gap order. Check all 19, recording the first
failure of each separate gate; duplicate cylinders may reuse computation.
Use the existing exact nonnegative partial inverses and recursive membership
oracle in
`experiments/problem1_nonperiodicity/analyze_period_two_phase_frontier_lift_recursion.py`.
Do not enumerate an entire frontier. For every successful candidate, replay
the full backward chain, the forward base prefix, the common-cylinder
congruence modulo 4^(c+1), and the predicted phase/complexity. Recover and
replay a generator witness if membership holds. Record every inverse failure
stage exactly, rather than labelling it a finite-precision uncertainty.

A failure refutes this particular universal construction or one of its gates,
not adjacent inclusion, belief nonemptiness, or Problem 1. Success in the
fixed rows gives only finite evidence and requires an all-depth mechanism;
it does not authorize a larger box. One local CPU, 120 seconds, 1 GiB;
atomic JSON with full commit, exact parameters, source and dependency hashes,
timings, hardware/software, limitations, and independently reviewable traces.

Before treating inverse rejection as decisive, independently check this
logical gate: if a final nonnegative y existed, its forward orbit and both
intermediate generator outputs would remain nonnegative. Therefore failure
of an exact nonnegative inverse at any backward stage rules out that y;
later inverse steps cannot restore a nonnegative final candidate. This does
not assert that the 2-adic candidate ceases to exist or classify its rationality.

Diagnostic admission after the primary result: independently replay the same
19 rows with a different exact inverse and direct three-generator predecessor
recursion. For the first nonnegative-inverse failure, seek an explicit signed
integer preimage and verify it by full forward arithmetic. For the first
membership failure, inspect only the candidate's high ancestors to locate
the earliest failed projection level, and determine that one four-digit
fiber. A smaller exact certificate improves the reviewability of the
negative result; lack of one leaves the independently checked membership
decision, without authorizing any larger frontier enumeration.

Further diagnostic admission: test only the three exact predecessors of the
first missing ancestor and their common projected ancestor `0x37a`, including
its four possible lift parents. A small rejection certificate would replace
reliance on a recursive membership oracle; failure to obtain one changes
only the certificate, not the admitted input box.

## 1. Exact conditional facts (`partial-proof`)

Use the established unit-triangular 2-adic bijections

```text
T(v)=v XOR ((v<<1) OR (v<<2)),
U(v)=T(v) XOR 1,
P(v)=T(v) XOR 1 XOR (2 if v is even else 0).
```

For an occurrence as above, let z_0=R(F^c(x)). The correct backward
recurrence, for j=0,...,c-1, is

```text
q=w[c-1-j],  Q=T if q=t, U if q=u,
a_j=Q^(-1)(z_j), b_j=P^(-1)(a_j),
z_(j+1)=4 b_j+3, y=z_c.                         (1)
```

The affine step is required in EVERY block. All inverse operations in (1)
exist uniquely in Z_2. Modulo 4, a 3-mod-4 output has T-preimage 1 and
U-preimage 2; P has residue map r -> 3-r. Thus B_t produces residue 11
modulo 16, B_u produces residue 7, and each is the correct inverse forced
branch. Consequently y follows w to z_0, even when y is outside N.

The occurrence tail starts ut, so the proved two-letter table gives
F^c(x)=7 modulo 64 and z_0=3 modulo 16. Hence z_0 stops, and y's exact
maximal schedule is w. Since x and y have the same inverse branch word,
and their cut states agree modulo 4, inverse isometry and multiplication
by 4 at each block give y=x modulo 4^(c+1).

**Exact nonnegativity gate.** If y belongs to N, its forward branch states
and all generator intermediates belong to N. They must equal the unique
backward values in (1). Therefore a failure of an exact nonnegative inverse
at ANY stage rules out y in N; further backward steps cannot repair it.
This distinguishes N from Z_2 minus N, not integers from nonintegers.

For a nonnegative output n>0, a positive T-preimage must have bit length
bitlen(n)-2. The triangular bit recurrence determines its only possible
low bits; full forward equality decides whether it exists. The exceptional
input zero is checked separately. U and P reduce to T by their exact low
bit corrections. Thus the implemented rejection is exact, not a truncation
heuristic.

**Conditional size.** If (1) succeeds in N, every a_j,b_j is positive:
Q(0) is 0 or 1, while Q(P(0)) is 13 or 12, none 3 modulo 4.
For positive v each generator increases bit length by two. Every complete
backward block therefore decreases it by two. If s=bitlen(x)>=5,
F^c(x) has length s+2c, R(F^c(x)) has length s+2c-2, and

```text
bitlen(y)=s-2.                                   (2)
```

This places y in the correct phase/size class, but proves no frontier
membership. These facts use the generator and inverse coding results in
`problem1_period_two_phase_frontier_lift_recursion.md` and
`problem1_period_two_schedule_coding.md`, and the ut table in
`problem1_rounded_projection_obstruction.md`.

## 2. Gate A fails: an exact negative integer (`refuted`)

The first counterexample in the admitted historical order is

```text
x=0x642fdfb in O_(u,14), c=1, w=t, gaps=(2,2,2).
Original generator witness from 0: uuuuputptuutuu.
Observed occurrence prefix: tututut; appended u is admissibility only.
X=F(x)=0x191cc387, Z=R(X)=0x64730e3.
```

Exact arithmetic gives

```text
T(0x1c10f9d)=Z,
P(-0xc0fd8e)=0x1c10f9d,
y=4*(-0xc0fd8e)+3=-0x303f635=-50591285.           (3)
```

The last two equalities use signed integers as 2-adic integers. They can
also be checked with finite arithmetic: for a>=0,
T(-1-a)=a XOR ((2a+1) AND (4a+3)). By inverse uniqueness, (3) is THE
candidate, not an alternative preimage. It is negative, takes exactly the
forced branch t to Z, and then stops. Gate A is therefore false on the
genuine occurrence domain.

## 3. Gate B fails independently (`refuted`)

The first nonnegative candidate outside the lower frontier is

```text
x=0xc85f8787 in O_(p,16), c=2, w=ut, gaps=(4,2,2).
Original generator witness from 0: putututpuuuuuptt.
X=F^2(x)=0xc85c546c7, Z=R(X)=0x3217151b3.
```

Evaluating the last inverse branch first gives the entirely positive chain

| Input | Q inverse | P inverse | B result |
| --- | --- | --- | --- |
| 0x3217151b3 | T inverse = 0xdeceae8d | 0x32395982 | 0xc8e5660b |
| 0xc8e5660b | U inverse = 0x379aa1f6 | 0xc855e91 | 0x32157a47 |

Thus y=0x32157a47 has bit length 30, agrees with x modulo 64, and
follows exactly ut before stopping. Nevertheless y is not in O_(p,15).
Here is a small rejection proof using only the established projection and
lift-fiber lemmas, plus exact arithmetic.

If y were in O_(p,15), then v=y>>14=0xc855 would belong to O_(p,8).
Its unique T,U,P predecessors are respectively 0x37ab,0x37ac,0x37aa.
All three project by >>4 to 0x37a. Any one in O_(p,7) would therefore
force 0x37a in O_(p,5).

Write 0x37a=4*222+2. The exact inverses of h=222 are
T^(-1)(h)=50 and U^(-1)(h)=P^(-1)(h)=41. The lift-fiber lemma gives
only these possible parents at level 4:

| Parent type | Parent | Contributed child digits if present |
| --- | --- | --- |
| 0 | 4*50=200 | {0,1,3} |
| 1 | 4*41+1=165 | {2,3} |
| 2 | 4*41+2=166 | {1,2,3} |
| 3 | 4*41+3=167 | {0,1} |

Parent 200 belongs to O_(p,4): the witness pupu gives 0 -> 3 -> 12 ->
55 -> 200. Each of 165,166,167 projects by >>4 to 10, whereas
O_(p,2)={12,13}. Projection therefore excludes all three. The fiber at
level 5 over 222 is exactly {0,1,3}, missing digit 2. Hence 0x37a is
absent, excluding all three predecessors of v and finally excluding y.
This is a finite exact certificate, with no enumerated frontier above level 2.

## 4. Bounded verification and independent review

Status: `finite-exhaustive` on exactly the 19 historical labels (17 distinct
state/base-prefix cases, 15 original states), preserving their original order.

| Test | Pass | Fail |
| --- | --- | --- |
| Original membership and full generator replay | 19 | 0 |
| Gate A: nonnegative candidate | 16 | 3 |
| Gate B, conditional on A | 14 | 2 |

All 14 cut-zero labels pass both gates (12 distinct lower states).
All five positive-cut labels fail one gate. This last sentence is finite
only; there is no theorem that every positive-cut candidate fails.
The other A failures are u/k15/0x1bd9c36b/cut2 and
u/k16/0x6f65c387/cut2. The other B failure is
u/k16/0x6f34fdfb/cut1, whose candidate is 0x1c1089cb.
Every nonnegative candidate passes the exact schedule, congruence, and
bit-length checks; every member has a replayed generator witness.

Default contributor Dewey used the existing exact partial inverse and
recursive lift-fiber membership implementation, with sweep entry points
disabled. The lead independently used cell-array forward T, P as the odd
section of T, signed inverses decoded from the entire finite output and
verified by full forward equality, and direct three-generator predecessor
recursion. All row decisions and first rejection stages agree. The lead
also verified every arithmetic identity and membership in the compact
certificate above. Neither implementation enumerated an entire frontier.

Muse Spark 1.3 Contributor (Singer) completed a tool-free independent
derivation and a separate hand review of the compact certificate. Its
initial recurrence summary omitted the affine step between inverse blocks;
the lead required and received a corrected derivation. The corrected review
distinguishes N from all integers, handles zero intermediates, and proves
exact stopping under ut. Muse independently checked the certificate's
arithmetic and its reliance on the existing projection/fiber lemmas. It
did not execute the finite checks. Earlier provider failures are not counted
as completed reviews.

Fresh reviewer Ramanujan independently accepted the full mathematical scope.
Its integration corrections are incorporated: counts keyed by the witness
state are not counts of distinct residue cylinders, and the original raw
primary input is preserved for portable replay of the independent source.

Atomic records contain exact parameters, full base Git commit, timings,
hardware/software, executed source, hashes, witnesses, and first-failure
diagnostics:

- `results/problem1/20260905_conjugated_projection_primary.json`
- `results/problem1/20260905_conjugated_projection_independent.json`

To replay, extract the independent record's `source_text` to a Python file
outside the repository and run it with Python 3 from the repository root
(or set `RULE30_REPLAY_ROOT`). It consumes the preserved
`original_record_utf8` inside the primary record and the committed canonical
rows, so the original temporary directory is not required. It atomically
regenerates both result files; timestamps, Git commit, and timings will
reflect the replay. The primary raw input's exact bytes and original hashes
are retained alongside the normalized fields.

## 5. Remaining bottleneck

The conjugated construction restores the required base schedule but fails
both nonnegative support and lower-frontier membership. Thus this particular
single-candidate shadow rule is closed. Neither counterexample refutes
existence of a different adjacent shadow, dominant nonemptiness, signed
nonvanishing, or B_all. General eventual periods >=3 remain unhandled.

Next candidate (`heuristic`, not tested here): delete a generator from an
ordinary representation and test the resulting lower state against the
base-cylinder congruence. First test the named failures above with exact
representation witnesses; do not infer universal failure from one chosen
representation. An all-depth selection rule, or a precise obstruction to
such a rule, would be needed before this could replace the failed map.

Subsequent checkpoint: `problem1_generator_deletion_test.md` gives an exact
all-representation deletion criterion. Both initial counterexamples above
have deletion shadows, but the already known deeper occurrence
u18/0x6473d46ab/cut4 refutes this construction even over all288 of its
representations. The earlier suggestion is therefore no longer untested
or a surviving universal candidate; adjacent inclusion remains open.
