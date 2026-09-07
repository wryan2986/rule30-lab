# Finite support does not select a unique recurrent phase

Status: `partial-proof` for the structural statements; `finite-exhaustive`
for the one exact certificate; `refuted` for the odd-parity rigidity in
Section 0. No FULL survivor is asserted; Problem 1 remains OPEN. Fresh
external review has not been obtained in round 304.

## 0. Admission and relation to the bottleneck

Round 303 rules out a finite-observation birth predicate on general cyclic
rows, but leaves spatial nilpotence load-bearing. Before using nilpotence
to select a unique cyclic history, test this precise proposed rigidity:

> Every nonzero finite A-periodic row whose low temporal bit is identically
> zero has odd high-bit weight over its least period.

If true, a nonresetting one-bit lift of a positive finite cycle would always
double its clock; the two lift bits would belong to that same doubled cycle.
If false, finite support permits a phase choice that survives forever without
a doubling or delay injection. A proof that charges retained phase choices
to doublings would need an extra hypothesis involving the actual boundary.
This is a test of phase rigidity, not a new supply of delay-birth examples.

Rankings are `heuristic`: (1) test this finite-support rigidity first, because
it is structural and cheaply falsifiable; (2) track the entire compatible
cycle-extension history with the original zero boundary, a surviving but
more costly route; (3) pull physical resets back to anchored activity with
valid depth/time indices and bounded multiplicity, still unproved. These
are not substitutes for the complete FULL premise.

The one admitted input is suggested by Eric Rowland, *Local Nested Structure
in Rule 30*, author PDF, Section 5, printed page 17:
[source](https://ericrowland.github.io/papers/Local_nested_structure_in_rule_30.pdf).
The displayed binary temporal word is `0000110001010011`. The paper discusses
an even-parity fork; we do not import its numerical minimality assertion or
assume its proposed phases are realized by finite rows. Instead verify the
four-symbol word `0000220002020022` independently under Phi and A.

The local checker has one word, at most 100000 deletion steps, one CPU,
60 seconds, and 128 MiB. It stops on zero or the cap. Reaching zero supplies
an exact finite-support certificate and refutes the stated rigidity. Failure
to reach zero within the cap is only `inconclusive` and triggers no larger
bound or word search. Two independently represented deletion recurrences,
hand transitions, packed A and explicit cell A must agree. No source word,
period, initial seed or FULL prefix is enumerated.

## 1. The complete one-bit fiber over a finite cycle (`partial-proof`)

Use A(y)=(y>>2) XOR ((y>>1) OR y), sigma(y)=y>>1, Theta, Phi and
phase-correct cyc from the existing physical-time and temporal-code notes.
Let y be a positive finite A-periodic row of least period p. Suppose

    Theta(y)_t=2u_t,  u_(t+p)=u_t,  u_t in {0,1}.

For e in {0,1}, put z_e=2y+e and
v^e_t=bit_0(A^t z_e). The one-bit scan equation reduces to

    v^e_(t+1)=v^e_t XOR u_t,   v^e_0=e.             (1)

Thus both lifts are finite and cyclic. With epsilon=XOR_(t=0..p-1)u_t,

    A^p z_e = z_(e XOR epsilon).                    (2)

If epsilon=1, both lifts lie on ONE cycle of least period 2p. If epsilon=0,
they lie on TWO DISTINCT cycles, each of least period p. For the last
assertion, any phase shift carrying z_0 to z_1 would project to a return
of y. Its shift is therefore a multiple of p, but (2) fixes z_0 at every
such shift. This is impossible. Projection also proves the least periods;
the available p or 2p periods give the reverse divisibilities.

In the even case the two complete traces v^0 and v^1 are complements at
every time. The full upper row y is identical, and the least clocks are
identical. Neither lift has a transient. The difference is a persistent
phase bit, not an inherited defect or a delay injection. This classification
uses the existing scan law; its new use is the finite-support test below.

## 2. Fixed word and hand checks

The chosen word is b=2u with

    u=0000110001010011,   b=0000220002020022.

It has six 1s (even). Its least period is 16: u_1=0 and u_9=1 rule out
period 8, hence every proper divisor of 16. Direct hand deletion gives

    0000220002020022
    0002130023230213
    0022230201032223
    0211032333111103.

These use g's hand table, with rows and columns in order 0,1,2,3:

    [0,3,2,1], [3,0,1,2], [3,2,1,0], [3,2,1,0].

For any verified vanishing depth N, recover an explicit integer by

    y = sum_(n=0..N-1) (Phi^n b)_0 * 4^n.           (3)

The deletion conjugacy proves Theta(y)=b when Phi^N b=0: the original
Theta-inverse has precisely these digits and zero spatial tail. The
checker must additionally verify A^16 y=y and its exact 16-symbol trace
using independent cell updates. Repetition of a bounded temporal sample
alone would not suffice.

Equation (1) gives, independently of the deletion computation,

    v^0=0000010000110001,  v^1=1111101111001110.

These words have weights 4 and 12 and cannot be temporal rotations of
each other. This provides a second, trace-level separation of the cycles
if the finite-support certificate succeeds.

## 3. Exact certificate (`finite-exhaustive` / scoped `refuted`)

`experiments/problem1_nonperiodicity/check_round304_phase_fork.py` verifies
this one input, with atomic record
`results/problem1/20260907_round304_phase_fork.json`.
Both deletion implementations reach zero for the FIRST time at N=26604.
Formula (3) gives a positive integer y of EXACT bit length 53208. The
record includes its complete hexadecimal value. Every bit of all sixteen
A updates agrees between packed arithmetic and explicit Boolean cell
updates (851328 bit comparisons), including the final return to y.
Its low symbols are precisely b, so its least A-period is 16. Both
2y and 2y+1 have least period 16, and their entire cycles are disjoint.
The complementary traces displayed above agree with the computed lifts.

The trajectory SHA256 (raw symbol bytes, initial through zero) is
`5176e4491284eab5136894a4e3b3ba95dda6cd95ef7617f1cc6702187d3071fb`.
The source y SHA256 (minimal little-endian bytes) is
`1a03ba42f43e5e91429982cb129a256f4882b1465a135053b99be0fbad4564f7`.
The run used full Git `c6873e33ee8b657fdc7c647aa050e02cf7b064e5`, took
1.665 seconds, and measured 29286400 bytes peak RSS. Full software,
hardware, source hashes, component timings and caps are in the record.

This certifies a finite spatial source rather than assuming that a
dyadic temporal word must be nilpotent. Its six high-bit 1s disprove
the proposed odd-parity restriction. The two finite cyclic rows explicitly
realize the two phase responses; this is not an inference from absence of
a counterexample in a search. The local one-bit classification itself is
imported from the existing work and is not a new theorem claimed here.

## 4. The phase distinction survives a common complete fringe (`partial-proof`)

For the certified y, let z_0=2y and z_1=2y+1. More generally this section
holds for any even-parity y satisfying Section 1. Attach the SAME arbitrary
complete initial right half to these two center-and-left rows. Denote their
actual rows at physical time t by Y^0_t and Y^1_t. The existing physical
diagonal identity, without a periodic-center premise, gives

    sigma^t Y^e_t = A^t z_e.

Equation (1) shows A^t z_0 and A^t z_1 differ in exactly their low bit,
at EVERY t. Therefore the HIGHEST bit where Y^0_t and Y^1_t differ is
exactly t. In physical coordinates their leftmost disagreement is exactly
at position -t. It never erases, regardless of the common right fringe.
The common bit at position -t-1 is zero: it is bit_0(A^t y).

A second, direct physical derivation starts with the difference at position
0. Finite cones make all sites left of -t agree at time t. At the next
leftmost output site, the Rule 30 OR has common center bit zero and reads
the differing right neighbor, so the difference propagates one step left.
The zero center bit on this characteristic follows from the A trace of y,
whose cone never reaches the attached right half. This proves the same
all-time statement without identifying cycle phase with physical time.

For a finite common fringe both entire physical configurations are initially
finite. Their period-16 starting cycles still cannot be identified by ANY
temporal phase shift: projecting such a shift to y forces a multiple of 16,
which fixes each lift. Thus finiteness does not make this a mere different
starting time on a universal finite cycle. Subsequent complete cycle clocks
need not agree, and no assertion about subsequent centers is made.

This is a phase difference BETWEEN TWO cyclic realizations. Each initial
row has zero internal cycle-entry delay. It is NOT a disagreement between
a row and its own phase-correct completion, and cannot be used as an
infinite delay-birth example on one FULL orbit. Its role is to exclude
forgetting phase choices merely because they occurred without clock growth.

## 5. Scope fence

This tests one word from a primary source. It does not establish the first
spatial depth at which a fork occurs, an unbounded supply of forks, or density
of finite cyclic birth fibers. No two initial finite right fringes are being
identified, and the two choices in (1) are not interchangeable along ONE
actual physical orbit. In particular its low source bit is zero, so this
is not a cyclic FULL doubling source. The zero boundary and entire future
remain essential for a proof on the critical path.

Dependencies: `problem1_activity_sparse_temporal_codes.md` Sections 1-2;
`problem1_physical_time_cycle_defects.md` Section 4; the exact renewal in
`problem1_cycle_delay_renewal.md` Section 1. The literature only selects the
fixed candidate; the certificate and local derivation must carry the result.
