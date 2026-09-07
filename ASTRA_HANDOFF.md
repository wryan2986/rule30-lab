# Astra handoff: supervisor round 304 research checkpoint, 2026-09-07

Problem 1 remains OPEN. Continue on `research/astra-next`. This is a
research checkpoint, NOT goal achieved, research blocked, or research
exhaustion. The incoming round303 handoff is preserved byte for byte in
`docs/astra_handoff_archive_20260907_round304.md`; the historical round-ten
handoff remains in `docs/astra_handoff_archive_20260907_round303.md`.
Round304 base commit: `c6873e33ee8b657fdc7c647aa050e02cf7b064e5`.

Read ASTRA_GOAL.md first. The incoming archive retains the exact renewal,
highest-wait no-go, conditional one-bit episodes, and their dependencies.
Do not repeat those derivations or the round-nine/ten source controls.

## Exact bottleneck

FULL must contradict finite entry for ONE fixed actual survivor with its
complete original finite right fringe. The renewal identity forces
infinitely many delay injections and doublings, but no upper bound on
injections in terms of the original anchored Q has been proved. A uniform
K=1 physical delay bound still allows distinct bounded lag-one episodes.
The unresolved birth at a cyclic source is nonlocal in its periodic driver.

Round 303 proves a precise obstruction to deciding that birth from finite
observations on the general cyclic-row domain. It does NOT exclude a
bounded strip under infinite FULL, supply finite-support countermodels,
transfer later events to Q(Y_0), or close period two.

## Round304: finite support retains phase choices without clock growth

Status: `partial-proof` for the structural consequence, `finite-exhaustive`
for one certificate, `refuted` for the proposed odd-parity rigidity.
Read `proofs/informal/problem1_finite_cycle_phase_fork.md` and the lead
adversarial disposition `proofs/informal/problem1_round304_review.md`.
The one-bit lift classification is an import, not a repeated new result.

The tested hypothesis was that every positive FINITE cyclic row with low
trace identically zero has odd high-bit weight over its least period.
This would eliminate a retained phase choice without clock doubling.
It is REFUTED by one exact word selected from Rowland's primary-source
Section 5, author-PDF page17, not a source/period census:

    b = 0000220002020022, least period16, six 2s,
    Phi^26604 b = 0, every earlier iterate nonzero.

Thus y=Theta^(-1)(b) is a FINITE cyclic integer of bit length53208.
The record gives its full hexadecimal value. For z_e=2y+e, the low
trace satisfies v_(t+1)=v_t XOR (b_t/2), v_0=e. Consequently

    v^0 = 0000010000110001,
    v^1 = 1111101111001110.

Both z_0,z_1 are finite cyclic rows, with the SAME least period16,
but lie on TWO DISTINCT cycles. A phase joining them would project
to a return of y, hence be a multiple of16, which fixes each lift.
Their low-trace weights4 and12 give a second separation. No delay
or doubling occurs in either lift. Finite support therefore cannot
supply a unique recurrent phase or justify charging every retained
phase choice to a doubling.

Attach the SAME arbitrary complete initial right fringe to z_0,z_1.
For their actual rows, sigma^t Y^e_t=A^t z_e. The highest actual
bit difference is exactly t for EVERY t; physically it stays at -t.
The common neighbor at -t-1 is zero. With a finite common fringe
both configurations are initially finite. This is a persistent phase
DIFFERENCE BETWEEN TWO orbits, not either orbit's internal cycle defect
or an infinite R_t supply on one FULL orbit. Subsequent clocks need not
agree. It does not close the original bottleneck.

Fixed checker: `experiments/problem1_nonperiodicity/check_round304_phase_fork.py`.
Atomic record: `results/problem1/20260907_round304_phase_fork.json`.
Two deletion loops agree on the entire trajectory and reconstructed digits;
independent packed/Boolean-cell A updates compare all851328 bits over the
full16-step source cycle. Both lifted cycles and the scalar recurrences
agree. Runtime1.665s, peak RSS29286400 bytes; 60s/128MiB caps passed.
Exact source SHA256 (minimal little-endian bytes):
`1a03ba42f43e5e91429982cb129a256f4882b1465a135053b99be0fbad4564f7`.
No minimal fork depth, later-fork list, infinite fork supply, finite-birth
density, longer FULL shadow or actual prefix was searched or asserted.

The surviving nilpotence route must retain the ENTIRE compatible phase
history and the SAME original eventually-zero right boundary. Do not
retest this parity hypothesis, enumerate more even-weight words, pursue
published later fork positions, or substitute a universal left-side cycle.
The anchored-charge route remains distinct and has no valid budget bound.

## Round304: reset anchoring requires global transport

`proofs/informal/problem1_reset_anchoring_geometry.md` supplies a second
`partial-proof` unit, with a separate lead audit in the round304 review.
No numerical experiment is used.

For each actual injection R_t>0, put T=max(tau_t-1,0),
lambda=tau_(t+1)=T+R_t. Its erasing 1 is EXACTLY

    r_(-lambda)(t+lambda)=1.

The preceding R_t-1 cells on that same characteristic are zero. The
characteristic coordinate i+u equals t. Original anchored cells are
(-2n-s-epsilon,s), n>=1, 0<=s<n, epsilon=0 or1, so their characteristic
coordinates are <=-2. The reset never directly belongs to that domain.
Its SHARP L1 distance to the entire sampling domain, active or not, is

    t + ceil(2(lambda+1)/3) >= t+2.

The lower bound follows from d>=t+j and d>=t+2lambda-2j+2;
three cases lambda modulo3 attain it. Thus any actual charge to an active
original sample needs displacement growing at least linearly in t.
Do not claim that this refutes all FULL-only local-charge lemmas: the
hypothetical FULL/finite-entry domain may be empty. The same-cell charge
on general actual finite orbits is refuted by the existing55 event R_1=1.

Also Q is a supremum per ray, not a total count: A(-1)=0 gives
Q(-1)=1 but sum_n J_n(-1)=infinity. Bounded multiplicity alone therefore
needs a finite target set or another counting argument. A valid fixed
rebase repairs this capacity issue: for Q(Y_0)<=K, h=h_J(K),
H=2ceil(h/2), the ACTUAL x=Y_H is finite with

    Q(x)<=K'=K+h+H/2,
    sum_n J_n(x)<=K'(K'+1)/2.

Retain its ENTIRE actual finite right fringe; do not rebase again at each
reset. A bounded-multiplicity assignment of all later resets to these
active pair samples would contradict the renewal. No such assignment is
constructed. The geometry requires global transport, and reuse of an
ancestor still needs a bound. Repeating the direct ray shift or enlarging
local neighborhoods cannot supply the missing step.

## Round303 strategy reset: three ranked routes

Estimates and rankings are `heuristic`. Full analysis and proof:
`proofs/informal/problem1_cycle_birth_observation_no_go.md`.

| Rank | Route and assumption | What success would prove | Cheap falsification | Research cost |
| --- | --- | --- | --- | --- |
| 1, attacked | Close a whole bounded episode by deciding its initial birth from uniformly bounded observations of a cyclic source; no use of finite support or infinite FULL | A local birth rule, still requiring a global episode exclusion | Preserve an arbitrary prefix and the exact clock, then force opposite cyclic return starts beyond the observation | One structural session; now refuted at this domain |
| 2 | Charge actual inherited-horizon resetting events to original anchored P_n(Y_0,s), with bounded multiplicity and s<n | Renewal plus finite Q would exclude FULL finite entry for period two | Check one event's pulled-back depth/time and multiplicity; n=0 or an out-of-budget horizon defeats that charge | Several sessions; no valid charge yet |
| 3 | Combine Phi-nilpotence of finite cyclic codes with the infinite boundary of the same original fringe | A finite-support-specific obstruction to the required infinite reset/doubling sequence, potentially closing period two | The existing finite cyclic 55 birth already refutes a single-step ban; any induction must retain more actual history | Several sessions to weeks; surviving structural route |

Route 1 is closed only at its stated general cyclic-row scope. Route 3
must use finite support or the full infinite history; extending observed
prefixes does not repair route 1. Route 2 remains a distinct option.

## New quantitative birth no-go (`partial-proof` / scoped `refuted`)

Let w be ANY temporal word of length L>=2 beginning 3,g with g in {1,2}.
Choose ANY power of two p>=max(8,2L), and set

    B13 = w 0^(p-L-2) 1 3,  B11 = w 0^(p-L-2) 1 1,
    x13 = Theta^(-1)((B13)^infinity),
    x11 = Theta^(-1)((B11)^infinity).

Both sources are rational A-periodic permitted rows with the SAME EXACT
least period p. Symbol 0 is 3 but symbol p/2 is 0; since every proper
divisor of p divides p/2, the period cannot be smaller.

The scan for F(x) reads shift^2 Theta(x), starting at 3. In state order
0,1,2,3, H_1=[3,2,2,2], H_3=[1,0,0,0], so H_3 H_1 is constant 0 and
H_1 H_1 is constant 2. The full return finishes with these suffixes,
then H_3,H_g for the wraparound source symbols. Thus:

| Source gate | Ending 13 | Ending 11 |
| --- | --- | --- |
| g=1 (t) | recurrent start 2; tau(Fx)=1 | recurrent start 3; tau(Fx)=0 |
| g=2 (u) | recurrent start 3; tau(Fx)=0 | recurrent start 2; tau(Fx)=1 |

Every H_i merges 2/3 on its first update, so the wrong start has LEAST
preperiod exactly one. Both successor eventual periods remain exactly p.
The exact spatial separations are

    v_2(x13-x11)=2p-1,
    v_2(Fx13-Fx11)=2p-3,
    v_2(cyc(Fx13)-cyc(Fx11))=0.

The source codes differ only in the high bit of their final period symbol.
Triangular inversion of Theta and the leading-input term of A^2 prove
these valuations; the cycle completions have low pairs 2 and 3.

For every cyclic x with x mod4=3, the ACTUAL odd row 2Ax is cyclic:
the periodic scalar drive at phase -1 sees the source pair 3 and resets
the lift bit to zero. Therefore, whenever the actual fringe supplies
this first paired gate, the constructed opposite births are exactly
R_0=0 and R_1 in {0,1}, with tau(Y_0)=tau(Y_1)=0. They are new physical
injections, not inherited transients. No later strip bound is inferred.

Both birth fibers are dense in the domain of cyclic permitted 2-adic
rows; the birth predicate is nowhere continuous there, also when the
domain is restricted to dyadic periods. This refutes finite-observation
birth decisions on that domain. If the exact period is supplied as
separate certified data, reading the WHOLE period does decide the birth.
The same-clock construction excludes a uniform observation bound, not
that period-dependent algorithm.

## Same complete fringe and arbitrarily long finite FULL shadows

Fix any finite initial right fringe and its unique FULL left input x_*;
the existing triangular full-boundary homeomorphism supplies existence,
without asserting finite entry or cyclicity of x_*. For any H>=3 and
physical window [-W,R], choose L>=2 with 2L>W+H, and use the first L
symbols of Theta(x_*) for w above. Attach the SAME complete right fringe
to both constructed sources. Their actual spacetimes agree with x_*
in that entire window through time H, by finite physical cones. Their
centers therefore alternate through H, and the first gate is actual.
Yet their first delay injections differ as above.

Quantifier fence: for EACH finite observation there are new sources.
There is no single constructed infinite FULL orbit. The construction
refutes neither an infinite-FULL-only quotient nor a rule confined to
one actual survivor. It also does not assert that these sources are
finite or satisfy an eventual uniform K=1 bound.

## The finite-support condition that remains load-bearing

For a cyclic code b,

    Theta^(-1)(b) finite iff Phi^j b=0 for some j.

For an A-periodic row, finite entry is equivalent to initial finiteness.
The construction proves NO such Phi-nilpotence. Even a dyadic clock is
insufficient: Phi fixes (12)^infinity, since g(1,2)=1 and g(2,1)=2;
its row is periodic of period two with infinite spatial support.
Whether both birth outcomes can be realized densely by FINITE cyclic
sources is unproved. Do not silently extend the no-go to that domain.

The next structural attack must use this nilpotence condition together
with the entire original boundary, or produce a valid anchored charge.
Do not enumerate completions of (3), enlarge source words/periods, or
sample longer finite shadows: the observation route is already closed.

## Verification and unresolved external review

New lead adversarial disposition:
`proofs/informal/problem1_round303_review.md`.
It audits return order, least periods, valuations, actual odd-row
cyclicity, topology versus certified period data, finite cones, and
all finite-to-infinite/finite-support quantifiers.

The fixed checker is
`experiments/problem1_nonperiodicity/check_round303_birth_algebra.py`.
Atomic record: `results/problem1/20260907_round303_birth_algebra.json`.
It independently solves the two deletion equations for each of 16 scan
entries and agrees with the hand table. Every one of 256 arbitrary
four-state interior functions, two gates, two suffixes, and four starts
passes: 4,096 return checks. The 10-second/128-MiB caps passed. There
were no seed, period, word, source-supply, or physical orbit searches.
This is `finite-exhaustive` only for the declared scan algebra, not
machine verification of the all-depth proof or finite-support witnesses.

FRESH EXTERNAL REVIEW IS STILL MISSING for both the incoming three notes
and the new note. Incoming-review Muse thread
01a07ae9-2411-7281-bc32-c3b8338e4438 and new-review Muse thread
01a07af4-6793-75f2-8a90-87c5cfc869cc both failed before review text with
MissingSessionID (missing x-opencode-session). Both threads are CLOSED.
Neither returned 429; that fallback sequence was not triggered. MiMo
was not in the session's advertised model overrides. No native reviewer
was substituted and no provider configuration was changed. The next
session should obtain authorized fresh review when routing is available.
No new result has status `rigorous-proof`.

## Round304 external review and checkpoint ownership

Muse thread `01a07af9-afb9-7e03-833c-cbe7da1826b8` was assigned the missing
round303 adversarial review and failed before text with MissingSessionID
(missing x-opencode-session). It is CLOSED. No429 occurred; no fallback
was triggered. MiMo was not advertised. No native or other provider was
substituted. External review remains missing for the incoming notes and
for the new round304 unit; the new disposition is explicitly LEAD review.

The round304 proofs, lead review, fixed checker/result, incoming handoff
archive and this handoff belong to this round. The older round303 ownership
record below remains historical.

## Historical round303 checkpoint ownership

Only the round303 proof, lead review, fixed checker/result, incoming
handoff archive, and this handoff belong to the checkpoint unit. Unrelated
supervisor files, worktrees, and old untracked results remain untouched.
The immutable reference remains SHA256
358bdc07904e77080eb78b67bdd8da25822d6b51f1a91b58b5313dfe461c1d01.
Do not force-push, rewrite history, modify the reference, or merge to main.
