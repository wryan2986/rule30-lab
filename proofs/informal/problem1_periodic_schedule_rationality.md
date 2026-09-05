# Periodic auxiliary schedules and rational spatial survivors

Status: `partial-proof` for the spatial recurrence and rationality theorem.
The bit-length-only boundary strengthening is `refuted` by a finite exact
counterexample outside the ordinary frontiers. Named finite checks are
reported separately below.
This concerns auxiliary zero-branch schedules, not a periodicity assertion
about the actual moving fringe. Problem 1 and B_all remain open.

## Strategy and admission

The previous Walsh checkpoint refuted one-character defect signs but did
not supply a correlation constraint on the zero-frequency coefficient.
The separate boundary obligation has a sharper concrete arithmetic test:
does a late three-return occurrence force x >= 4^(c+2) for every positive
integer, or is ordinary-frontier membership essential?

Ranked routes (`heuristic`):

| Rank | Route | All-depth potential | Falsifiability / cost |
| --- | --- | --- | --- |
| 1 | Finite spatial recurrence for periodic auxiliary survivors | Exact rationality theorem and structured boundary comparators | High / bounded cycle certificates |
| 2 | Return-conditioned joint Walsh correlation constraint | Direct nonvanishing if a suitable constraint exists; none currently specified | Undetermined / high |
| 3 | Frontier-specific exclusion at the five critical cuts | Direct B_all proof | High for a concrete candidate / high |

Candidate: every eventually periodic auxiliary schedule has a rational
2-adic survivor. For a pure schedule of period p, its p cyclic phase states
obey a deterministic spatial recurrence on four p-bit vectors after the
low boundary. There are at most 2^(4p) states. A repeated sufficient state
would certify eventual spatial periodicity, not merely suggest it from a
repeated output prefix. Inverse generators should preserve rational 2-adics
and extend the result to eventually periodic schedules.

Before attempting a long proof, Muse is asked for a tool-free independent
derivation or counterexample, including the precise boundary and memory size.
The bounded implementation checks only the constant t/u controls and the
two named words `ututtt` and `ttututt`. The former is the smallest unequal
gap (2,4) comparator outside the existing equal-gap prefix certificate;
the latter is the already documented seven-block comparator. Their infinite
repetitions are auxiliary admissible words, not the actual fringe schedule.

One local CPU, 120 seconds, 1 GiB, at most 2^20 spatial states per named word.
Stop on a repeated sufficient state or the cap. Retain complete cycle data,
exact rational phase values, and recurrence verification. Check finite
truncations only within one completed spatial preperiod and period for
canonical three-return occurrences at c >= ceil(bitlen(x)/2)-2. Any reported
counterexample needs an exact independent forced orbit and admissibility
certificate. Absence is only on these truncations, not all truncations or
all schedules. No larger word family, period, frontier, or integer box is
authorized by either outcome.

A boundary counterexample would refute the bit-length-only strengthening
and isolate the need for frontier information; it would not refute B_all
without separate frontier membership. No counterexample would leave that
strengthening open. Independently of this finite outcome, a proved spatial
recurrence would give an exact rationality classification in one direction.
Atomic JSON records must retain executed source, base Git, inputs, hardware,
software, timings, hashes and limitations. Contributors own only /tmp paths;
the lead reviews and integrates completed records.

## 1. Cyclic phases and the exact spatial recurrence (`partial-proof`)

Use the forward maps T, U, P and the inverse branches B_q from
`problem1_period_two_schedule_coding.md`. Let q be a nonempty word of
length p, repeated infinitely. Its phase-j survivor is X_j, with j modulo p.
Existence and uniqueness follow from the established contraction theorem.
The exact equations are

```text
X_j = 3 mod 4,
X_(j+1) = Q_j(P((X_j-3)/4)).                       (1)
```

Write x_(j,n) for bit n of X_j and V_n=(x_(j,n))_j for the p-bit vector.
Let R shift phase indices, (Rv)_j=v_(j+1 mod p), and let delta_j=1 when
q_j=u, 0 when q_j=t. All vector Boolean operations below are coordinatewise;
complements are within p bits.

For a binary input z with output w=P(z), the exact boundary rules are

```text
w_0=z_0 XOR 1,       w_1=z_1 XOR 1,
w_n=z_n XOR (z_(n-1) OR z_(n-2)) for n>=2.         (2)
```

The second identity uses P's parity correction: z_0 XOR [z_0=0]=1.
Q_j is T followed by a possible toggle of output bit zero. Substitution in
(1) at output bits n=0,1,2,3 gives

```text
V_0=V_1=1,  V_2=delta,  V_3=1 XOR delta,
V_4=R delta,           V_5=1 XOR delta.           (3)
```

For clarity, the n=2 equation reduces to x_(j+1,2)=x_(j,4), because
x_(j,2) and x_(j,3) are complementary. The n=3 correction is
x_(j,2) XOR x_(j,4); since x_(j+1,3)=1 XOR x_(j+1,2), it gives
x_(j,5)=1 XOR x_(j,2). Thus (3) includes all exceptional low-bit equations.

For n>=4, every P-output bit used in Q's neighborhood has index at least
two, so both operations use their homogeneous Rule 30 formulas. Define

```text
H(a,b,c,d) = (a OR b)
             XOR ((a XOR (b OR c)) OR (b XOR (c OR d))).
```

Expanding (1) twice yields

```text
x_(j+1,n) = x_(j,n+2)
             XOR H(x_(j,n+1),x_(j,n),x_(j,n-1),x_(j,n-2)).
```

Consequently the upward spatial recurrence is exactly

```text
V_(n+2) = R V_n XOR H(V_(n+1),V_n,V_(n-1),V_(n-2)), n>=4. (4)
```

It is triangular in spatial position, even though the phases are cyclic:
R V_n is already known when V_(n+2) is generated. The state consists of
four previous vectors, not five; the fifth vector is the newly computed
output. Starting with (3), the recurrence constructs a solution of every
bit equation in (1). Alternatively the unique contraction solution must
obey these seeds and this recurrence, identifying the two constructions.
Neither argument treats agreement of a finite prefix as equality in Z_2.

## 2. Rationality and a cycle certificate (`partial-proof`)

**Theorem.** For every word q of length p>=1, the survivor of q repeated
infinitely is a rational 2-adic integer. More precisely the deterministic
state sequence

```text
H_n = (V_(n-2),V_(n-1),V_n,V_(n+1)), n>=4,
```

has a transient mu>=0 and a cycle lambda>=1 with

```text
mu+lambda <= 2^(4p).
```

Proof. There are at most 2^(4p) four-vector states. The update (4) is
deterministic and independent of spatial position after the boundary.
The first repeated state therefore determines an exact cycle. If the
equal states occur at update times mu and mu+lambda, equality of all
subsequent states follows by induction. Their earliest components show
that V_n is lambda-periodic for all n>=a=mu+2.

For phase j let A_j be its low a-bit prefix and C_j its next lambda-bit
block, both interpreted least significant bit first. The entire phase
state is therefore exactly

```text
X_j = A_j + 2^a C_j / (1-2^lambda).               (5)
```

The geometric series converges 2-adically and its denominator is odd.
This proves rationality. It is an upper bound on a sufficient state space;
the reported vector cycle need not give each phase's least spatial period.

A complete computational certificate can consist of the boundary seeds,
the transient and cycle vector lists, every local recurrence check, and
the equality of the closing four-vector state. A repeated output block
without this sufficient-state equality would not be such a certificate.

## 3. Eventually periodic auxiliary schedules (`partial-proof`)

Each inverse generator preserves rational 2-adic integers. To prove this
directly, write b for an input bitstream and a for the recovered preimage.
For T inverse, with negative-index a bits set to zero,

```text
a_n = b_n XOR (a_(n-1) OR a_(n-2)), n>=0.
```

For U inverse first toggle b_0, then use the T inverse recurrence. For
P inverse the initial conditions are a_0=b_0 XOR 1 and a_1=b_1 XOR 1,
followed by the same recurrence for n>=2.

A rational 2-adic input has eventually periodic bits. After both its transient
and the exceptional initial bits (at n>=max(N,2) for input onset N),
the input phase modulo its period lambda and the two previous output bits
form a finite state with at most 4lambda possibilities. A repeated state
forces eventual periodicity of the output bits, hence a rational output.
The equivalence between rationality and eventual bit periodicity follows
directly from the geometric-series formula in one direction and the finite
remainder recurrence for division by an odd denominator in the other.

Now let a schedule have a finite prefix followed by an infinite periodic
tail. Section 2 makes the tail survivor rational. Each inverse branch
B_q(y)=4 P^(-1)(Q^(-1)(y))+3 preserves rationality by the preceding
recurrences. Applying the finitely many prefix branches proves:

> Every eventually periodic auxiliary branch schedule has a rational
> 2-adic survivor.

Together with the existing degree-growth theorem, these survivors have
infinitely many nonzero bits; they are not nonnegative ordinary integers.
No converse classification of rational survivors is asserted. In particular
this does not prove that the actual auxiliary schedule is periodic or that
its survivor is rational, nor does it settle the whole-tail question.

## 4. A spatial zero-gap bound (`partial-proof`)

There is a second all-depth constraint, from the existing repetition theorem
rather than the finite cycle checks. For a purely p-periodic auxiliary
schedule, consecutive nonzero base-four digits of its survivor are at
distance at most 2p. Thus every intervening run of zero digits has length
at most 2p-1. No minimality of the period p is required.

Proof. Let d_b and d_a be consecutive nonzero base-four digits, a>b>=1.
Truncate the survivor above d_b, obtaining the positive integer x of
complexity k=ceil(bitlen(x)/2)=b+1. Since the intervening digits vanish,
x agrees with the survivor modulo 4^a. Branch choice uses two low base-four
digits, and each common forced step loses one digit of agreement. Hence x
follows the first a-1 branches of the periodic schedule, ending in 3 mod 4.

The exact periodic-prefix theorem in
`problem1_finite_schedule_repetition_bound.md`, Section 2, applies to every
positive finite integer of complexity k>=2, without frontier membership.
It gives a-1<=k+2p-2=b+2p-1, hence a-b<=2p. For b=0, the low seeds (3)
give d_0=3 and d_1 in {1,2}, so the first distance is one. There are
infinitely many nonzero digits by the established noninteger-survivor
theorem, so no final infinite zero run is omitted.

This controls the spacing of spatial nonzeros for auxiliary periodic
schedules. It neither proves B_all nor transfers a periodicity premise to
the actual moving fringe. The same bound with just the eventual period p
is not asserted across an arbitrary schedule preperiod.

## 5. Named cycle certificates and a boundary counterexample

The enumeration and replay counts in this section are `finite-exhaustive`
on their stated finite domains. Turning a closed cycle into an exact
rational expansion uses the proved recurrence in Sections 1–2.

Both implementations found the following sufficient-state cycles:

| Auxiliary word | Phase count p | Transient mu | Vector period lambda | Spatial onset |
| --- | --- | --- | --- | --- |
| t | 1 | 0 | 2 | 2 |
| u | 1 | 0 | 2 | 2 |
| ututtt | 6 | 0 | 138 | 2 |
| ttututt | 7 | 0 | 728 | 2 |

All vector lists and all 15 rational phase values agree exactly. The constant
controls give 1/3 and 5/3. The zero transients in this table are not asserted
for arbitrary words. Neither are these necessarily least periods of each
individual phase. The primary also checked the cyclic aligned base-four
zero runs: their maximum over phases is three for each nonconstant word.

The primary truncation search uses X_j modulo 2^N, increasing N and then
phase j, deduplicating integers within each word. Its upper cutoff is the
spatial onset plus one vector period. Inputs below four are skipped.
The two controls each test one integer. All 420 distinct `ututtt` truncations
in this scope pass the proposed boundary bound. The `ttututt` scan stops
at its first failure, after 1,677 distinct truncations, at N=456, phase j=5.
No later truncations in that scan were tested. These counts and first-witness
minimality concern the specified primary search only, not all integers.

The counterexample (`refuted` bit-length-only strengthening) is

```text
x = 0xd29f48fac73f656a906a603e118f11364babc77266b9f6e5713415e4eb4dfbface6176141a66eb51ed9f6afbdba3ab3fb17fe13f3088c146ab
bitlen(x)=456, k=ceil(bitlen(x)/2)=228.
```

Its complete forced word is exactly

```text
(ttttutu)^32 ttt ututut, length 233,
```

after which the state has residue 15 modulo 16 and stops. The displayed
power denotes concatenation, not an arithmetic operation. At cut c=227
the final `ututut` is a three-return occurrence with gaps (2,2,2).
Appending one unobserved u makes the complete admissibility word. It has
neither uu nor five consecutive t's; its successive u gaps are 2 and 5
in the repeated part, followed by 4,2,2,2 at the end, never the forbidden
successive gaps (2,3). Thus it also avoids ututtu.

The claimed bit-length-only bound requires c<=k-3=225. Here c=227,
equivalently L=c+1=k=228, so the candidate fails. In arithmetic form,
the requirement x>=4^(c+2)=2^458 fails since x<2^456.

The input is exactly the 456-bit truncation of phase five of the rational
`ttututt` comparator. Its difference from that rational has 2-adic valuation
456. Its first 227 branches agree with the periodic comparator, and branch
227 is the first disagreement. The final occurrence therefore does not
have a wholly periodic prefix; the previously proved periodic-prefix
boundary subclass is unaffected.

### Compact exclusion from the ordinary frontiers

Admission after finding the named counterexample: inspect only its projected
leading prefixes through complexity four. This distinguishes an actual B_all
violation from failure of its bit-length-only strengthening. It is not a
new frontier census or a test of other integers.

The ordinary phase bit lengths are 2k for p and 2k-1 for u. Thus only
p at complexity 228 could contain this 456-bit integer. The exact small
frontiers, derived by applying T, U, P to each member, are

```text
O_(p,1) = {3}
O_(p,2) = {12,13}
O_(p,3) = {50,51,52,53,55}
O_(p,4) = {200,201,202,203,204,205,207,220,221,222,223}.
```

Its projected prefixes at levels one through four are 3,13,52,210. The
last is x>>448=0xd2. It is absent from O_(p,4). Iterating the established
projection inclusion O_(p,h)>>2 subset O_(p,h-1) would place 210 in that
frontier if x belonged to O_(p,228). Hence x is in neither phase frontier.
The first three leading-prefix membership tests do pass; the fourth fails.

This is not a counterexample to B_all. It proves that a valid all-depth
boundary argument needs information beyond bit length alone. The compact
projection rejection identifies such information for this particular input;
it does not prove that one fixed leading width suffices universally.

## 6. Independent checks, reproducibility, and remaining obligation

Muse Spark 1.3 Contributor independently derived the homogeneous recurrence,
all six boundary vectors, the finite-state rationality argument and its
eventually periodic extension without tools. It also checked the zero-gap
corollary and hand-derived the four small frontiers in the nonmembership
certificate. It did not execute the truncation search.

Dewey implemented the primary local computation. Every generated vector
transition was compared with a per-phase lookup obtained directly from
packed QP, and the exceptional seeds were solved from the packed triangular
equations. The lead independently used vector windows and cell-array phase
equations. For onset a and period lambda, the equation residual is periodic
for n>=max(4,a+2); checking the earlier boundary and one full period therefore
checks all indices of the rational phase equations. The independent check
uses 6,6,852,5124 individual phase-bit comparisons for the four words.

The selected finite counterexample was independently replayed with cell-array
T and the odd-section identity P(v)=T(2v+1)>>1. All 233 transitions and every
orbit state agree. The independent third-u prefix criterion finds u positions
227,229,231 after the critical threshold 226 and confirms the following t.
The complete primary negative truncation search was not independently rerun;
the positive counterexample, its occurrence, and its frontier exclusion were.
The verification record also archives Dewey's separate forward check through
p level four; its complete levels agree with the cell-array/odd-section
replay, and its original input is recoverable from the embedded primary
contributor payload.

Fresh reviewer Ramanujan approved Sections 1–4 and the all-index justification
of the cycle certificate, including the exact offsets and the distinction
between sufficient and least spatial periods. The note incorporates its
clarification about starting inverse finite-state reasoning after both the
input transient and the exceptional initial bits.
The same reviewer subsequently approved the completed boundary certificate,
its exclusion from B_all's domain, and the full provenance integration,
including the archived prefix check and portable verification paths. No
remaining mathematical or provenance correction was requested.

Atomic standard-protocol records are

- `results/problem1/20260905_periodic_rational_primary.json`
- `results/problem1/20260905_periodic_rational_independent.json`
- `results/problem1/20260905_periodic_rational_verification.json`

They retain exact inputs, executed source, base Git, hashes, timings,
hardware/software and limitations. The primary embeds its original contributor
payload and complete raw mathematical data. Documentation hashes in that
payload describe run-time snapshots of evolving notes; they are not claims
that those notes remain byte-identical after integration. Its actual
computational inputs are the literal words, maps, bounds and search order.

Independent sources can be extracted to a file outside the repository and
run from the checkout root or with RULE30_REPLAY_ROOT set. RULE30_REPLAY_OUTPUT
selects an output file. The verification source reads only the two committed
cycle records and writes its own record atomically. The original primary
source retains its recorded checkout path and writes beside the extracted
source. No temporary raw-data file is needed to inspect or independently
verify the committed certificates. Replay changes timestamps and timings.

The all-depth rationality and gap theorems use structural arguments; the
finite cycles certify only the named comparators. Bit-length-only boundary
exclusion is now refuted, so enlarging its integer box is not a next step.
The strongest boundary target remains B_all with actual ordinary-frontier
membership at the five critical cuts. A useful next hypothesis must couple
that membership to the forced schedule, beyond the four leading digits
which reject only this counterexample. Joint signed nonvanishing and eventual
center periods of least period at least three also remain open.
