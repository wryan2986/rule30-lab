# Astra handoff: round 4 maintenance checkpoint, 2026-09-06

Problem 1 remains OPEN. This is a time-maintenance checkpoint, not goal
achieved, research blocked, or research exhaustion. Research continues on
`research/astra-next`. This round began at20:17:51UTC; the final audit records
the checkpoint timestamp. Read `ASTRA_GOAL.md` first as the user requests.
The complete previous handoff is preserved, byte for byte, in
`docs/astra_handoff_archive_20260906_round4.md`; use it only for older detail.

## Current bottleneck and reading order

Prove unbounded record R_N=max_(0<=s<=N)V_s(x) for ONE FIXED ACTUAL
period-two survivor x with its FULL moving-fringe coupling, where

    T(x)=x XOR ((x<<1) OR (x<<2)),  pi(x)=x>>2,  A=pi T,
    V_0=0,  V_s(x)=sum_(t=0..s-1)bit_(2s)(T^t x),
    R(x)=sup_s V_s(x),  E_K={x in Z_2:R(x)<=K}.

Only s OBSERVED branches determine V_s. No growth theorem on the actual
survivor is proved. Read these new notes in order:

1. `proofs/informal/problem1_activity_level_finiteness.md`.
2. `proofs/informal/problem1_activity_return_nonincrease.md`.
3. `proofs/informal/problem1_effective_activity_levels.md`.
4. `proofs/informal/problem1_single_column_activity.md` and
   `problem1_temporal_activity_deficit.md` for the preceding definitions
   and criteria, as needed. Their review gaps are now closed IN SCOPE below.

Every all-depth result here retains status `partial-proof` relative to the
full prize problem. Finite certificates are only `finite-exhaustive` in
their declared domains. No finite absence is an infinite proof.

## Round-four results: finite and effective activity levels

`partial-proof`, independently reviewed: E_K is FINITE at each fixed K.
Uniform finite entry gives h=h_V(K), the first h with
sum_(r=0..h)1/(2r+1)>3K/2, and T^h(E_K) subset N. Time translation
adds at most h activity. If finite y has bit length B and z first differs
at a>=B+4L+4, then R(z)>L. Correct window N=floor((a-B-2)/2) covers
both parities and B=0. T preserves first difference, so every point of the
compact E_K is isolated. A uniform output-size bound at fixed K EXISTS.

The old draft's longer zero-neighbor window is `refuted`: y1,z17,a4,N1
has Tz119 with bit2=1. The draft is retained with a correction pointer.
Only its time-endpoint assertion failed; sublevel finiteness survives.

Exact identities, s>=1 (`partial-proof`):

    V_s(Ax)=V_(s+1)(x)-bit_(2s+2)x;
    V_s(pi x)=V_(s+1)(x)-bit_2(A^s x);
    V_s(Gx)=V_s(x)-bit_(2s)x+bit_0(A^s x), G=T,U,P.

A and pi preserve E_K; a generator or permitted F step gives E_(K+1).
E0={0,1,2,3}. The +1 is sharp even ordinary: 27->111, R27=1,R111=2,
by A cycles25<->27 and100<->111. 111 has no further permitted gate.

`partial-proof`, independently reviewed: E_K is EFFECTIVELY finite.
T^-h(y), y in N, is an exact rational 2-adic via a2h-bit tail recursion.
For finite y=T^h x and z=pi^h y,

    V_s(x)=sum_(t<h)bit_(2s)(T^t x)+V_(s-h)(z), s>=h.

Early terms are rational spatial cycles; the finite z term has an exact
closed A-vector. Bounded V is effectively eventually periodic, and R of
each finite-entry candidate is computable. A terminating finite-cylinder
cover search plus exact candidate membership outputs E_K and a support
bound B(K). This is a PROVED ALGORITHM, NOT an executed/admitted census.
No useful complexity bound or closed formula for B(K) is provided.

For any rational input with spatial tail onset a, period p, ring temporal
transient q and period ell, put D=max(1,ceil(a/2)) and let m_i count ones
in column i of the temporal cycle. For s>=D,

    |V_s-(m_(2s modp)/ell)s|<=q+ell+D-1.

A nonzero cycle has every m_i>0, so liminf V_s/s>=1/ell. A zero cycle
gives finite entry. Thus rational inputs have bounded activity OR positive
lower LINEAR growth at all large ages, with possible phase-dependent
coefficients. R is computable on GIVEN rational numerator/denominator
inputs. This is not a dichotomy for arbitrary irrational inputs.

Finite computable lists do NOT give finite-digit-query membership for
arbitrary 2-adic oracles. Exact family2^(2m): V_s=0 for s<m, V_m=m.
Equality of a listed rational with the FULL actual survivor remains an
unresolved infinite test. No first-witness box is reopened.

## The return-monotonicity route is now refuted

Universal nonincrease of R across genuine prescribed three-return blocks,
combined with finite E_K and bounded return gaps, WOULD force termination.
It is `refuted` on the already stored u18/0x6473d46ab, original cut4,
observed ttttututut, final u gate checked but NOT executed:

| Orbit time | Endpoint | Nonroot n | First max age | R |
| --- | --- | ---: | ---: | ---: |
| 4 | 0x6473c6fc387 | 21 | 21 | 13 |
| 10 | 0x6473c7a1004b27 | 27 | 25 | 16 |

Gates at4,6,8,10 are u and at5,7,9 are t: exactly gaps222. Tail vectors
enter cycles at ages32 and41, both period8, first closures40 and49.
Complete closed recurrences, not sampled maxima, certify ALL ages.
Packed ordinary-history and independent cell/projection methods agree on
54 full direct temporal vectors,41 tail scores,11 orbit states and2 exact
closures. Lead separately replayed the closures and earliest maxima.

Only these two existing endpoints were tested. No frontier, occurrence,
activity-level, comparator, period, or suffix census was added. Primary
summary/tie-rule errors and a JSON key-order payload-hash bug were fixed;
all scores and R values stayed13/16. Source/admission snapshots reload.
This does not refute a survivor-only restriction or exhibit an infinite
finite-start forced orbit. Do not fit a compensated R or extend the box.

A related `partial-proof` warning: IF an infinite forced orbit starts at
R(x)<infinity, then R(F^r x)->infinity nonetheless, while R(F^r x)<=R(x)+r.
After finite entry its degree grows and finite E_K are left forever.
Growth across ORBIT SHIFTS therefore does not exclude finite initial
support. The required growth is in AGE of ONE fixed actual survivor.

## Review disposition and reproducibility

One Muse worker (`opencode-go/muse-spark-1.3-contributor`) supplied the
primary and fresh scoped proof reviews; it is CLOSED. No pending thread,
fallback, or provider retry remains. The lead independently checked each
contribution before acceptance. Reviews and full atomic archives:

- `problem1_activity_finiteness_independent_review.md` and
  `results/problem1/20260906_activity_finiteness_review.json`.
- `problem1_activity_return_nonincrease_review.md` and four corresponding
  `results/problem1/20260906_activity_return_nonincrease_*.json` records
  (primary, independent, verification, review).
- `problem1_effective_activity_levels_review.md` and its corresponding
  `results/problem1/20260906_effective_activity_levels_review.json`.
- `problem1_activity_criteria_full_review.md` and
  `results/problem1/20260906_activity_criteria_full_review.json`.

Review filenames above are under `proofs/informal/`. The final corrected
review covers ALL all-depth V Sections1-4 and D Sections1-5, with their
explicitly imported gate/history dependencies. This supersedes round3's
missing D/V-review disposition. It does not re-review numerical counts,
the old all-memory/all-r theorems, or the whole prize statement.

Rejected review errors were corrected before acceptance: piT=Tpi and
AT=TA are FALSE; only piA=Api is used. F^r=4A^(2r)+3 is FALSE for r>1;
correct pi^r F^r=A^(2r) restores r low pairs. Wrong +2-optimality wording,
finite-only E0 reasoning and counting seams were also removed. Full
corrected derivations, not blanket initial verdicts, are archived.

Research units committed/pushed:97d45d8 (finite levels),0ec3851 (return
counterexample),a9b1d08 (effective levels). Later review/maintenance commits
are in Git history. `results/problem1/20260906_round4_final_audit.json`
records the final archival audit; it does not repeat scientific runs.
Immutable reference SHA256 remains
358bdc07904e77080eb78b67bdd8da25822d6b51f1a91b58b5313dfe461c1d01.
Pre-existing untracked supervisor scripts/logs, ASTRA_GOAL.md, worktrees and
unrelated results were preserved. Never edit the reference or force-push.

## Next work; do not repeat completed work

The only main bottleneck remains fixed-actual-survivor record growth.
Prioritize a precise full-fringe/ordered-original-history inequality, or
an all-depth argument excluding the bounded finite-entry alternative with
its actual boundary conditions retained. Rational nonzero tail cycles
already give growth; the hard alternative is the mortal rational tail.
Naming the finite list does not settle its equality with the survivor.

Do not repeat the finite-entry proofs, isolation test, return counterexample,
rational profile derivations, or their numerical checks. No E_K enumeration,
graph, return sweep, comparator/suffix expansion, larger first-witness box,
backend work or Problems2/3 sweep is admitted. State a concrete falsifiable
all-depth lemma and how either outcome changes the whole-tail argument
before any new experiment. Neither a growth lemma nor a new experiment
has been established/admitted for the next round.

Older boundaries remain: B_all and signed nonvanishing are unproved;
least temporal periods>=3 are unhandled. Period1 is excluded. Whole-tail
finite support strengthens the single-seed prize instance to all finite
left halves with rightmost one0. Old all-memory and all-r suffix external
review limitations are unchanged. Consult the archived handoff for the
precise older no-go results and source paths only if a new mechanism
requires them. This is maintenance rollover, not research blockage.
