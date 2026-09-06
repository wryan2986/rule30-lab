# Audit of the fresh all-memory fallback review

Status: `inconclusive` for fresh verification of the all-memory no-go;
`refuted` for the two specific review inferences identified below.
This audit does not refute the repository theorem or solve Problem 1.
Checkpoint inspected: `432934578b6696fa153403897f7764f8ce007e89`,
fetched and verified equal to origin/research/astra-next.

## Review provenance and disposition

The current ASTRA_GOAL.md permits MiMo after one delayed Muse retry.
Two fresh requests to opencode-go/muse-spark-1.3-contributor returned
provider429. An explicit 30-second pause preceded the single retry.
The prescribed opencode-go/mimo-v2.5 fallback returned an initial
review and one requested correction. Both contained material errors.
Do not count either positive verdict as successful proof-critical review.
All three agent threads are terminal and closed. No native subagent
was substituted and no mathematical computation was run.

The atomic archive is
`results/problem1/20260906_all_memory_mimo_review_audit.json`.
It contains exact diagnostic excerpts of the initial report, the full
corrected response, agent/request IDs, source hashes, full Git checkpoint,
local hardware/software facts, and archive-preparation timing. Provider
inference timing and hardware were not reported. The archived review text
contains rejected claims; it is evidence about the review, not a proof.

This session identifies as GPT-6. Its exposed model list does not name
Astra. The user was asked whether to authorize this lead or resume with
Astra; no answer had arrived when this checkpoint was prepared. This is
an integration audit, not a claim of Astra's final proof judgment.

## 1. Dropping the original cycle cost

The initial report concluded that circulation cancellation gives cL=0,
hence c=0. The source's equation (6) instead gives

    0 = sum_(e in cycle) [c - omega(e)],
    sum_(e in cycle) omega(e) = cL.

Status: `refuted` for the inference from this identity to c=0.
The exact symbolic control is omega(q,g)=1 for every residue and letter.
Then every pure-scanner difference is zero, c=1, and both sides of the
correct cycle equation equal L. The cost of every length-n ordinary word
is n, so this control is bounded below. Its six-step prescribed change
is +6; it is NOT a candidate satisfying universal strict descent.
It tests the intermediate algebra only, not the theorem's full hypotheses.

The followup retracted c=0 but wrote c as a sum over residues without
the factor 2^(-b). The source's normalized definition is

    c = sum_q [omega(q,t)+omega(q,u)+2omega(q,p)]/(4*2^b).

The same constant control makes the unnormalized expression 2^b,
contradicting the followup's simultaneous claim c=1 when b>=4.
Boundedness gives c>=0; requested-memory endpoint closure gives 6c>=0.
Neither argument requires c=0.

## 2. Precision and the two different evolutions

The initial report claimed A(q) modulo 2^k needs only k+1 input bits.
Status: `refuted` by k=1, q=0 and q'=4. They agree modulo 4, but
T(0)=0, T(4)=4 XOR (8 OR 16)=28, hence A(0)=0 and A(4)=7
have different low bits. This is hand arithmetic, not a new search.

The source defines A(q)=T(q)>>2. Congruence preservation of T gives
an upper bound of k+2 input bits for A modulo 2^k. Iterating gives
b+12 bits for A^6 modulo 2^b. Congruence preservation of G_g gives
12 input bits for A^5(G_g(q)) modulo 4. These are direct dependency
bounds, not an extrapolation of the existing finite controls.

The followup still replaced the word scanner H, its endpoint map A,
and the forced map F by one symbol. In particular, it substituted
H^6(X)=X for the source's F^6(X)=X in the survivor closure.
That substitution is unjustified. H acts on history words; its endpoint
intertwines with A. Forced evolution also appends birth letters. The
source's closed-endpoint argument requires F and its branch-dependent
precision bound, separately from the pure A-iterate cost formula.
The review did not discharge this obligation correctly.

## 3. Fiber bijection is distinct from scanner-output averaging

For a compatible family of finite permutations G, reduction of G
modulo 2^M commutes with reduction modulo 2^b, M>=b. Thus G sends
the fiber over q into the fiber over G(q). Injectivity and the equal
fiber cardinalities 2^(M-b) make this map onto. This is the elementary
fiber argument used in cycle conservation; controllability is not its
premise. Status: `partial-proof` for this general dependency clarification.

The followup instead described the joint distribution of A^r(q) and
the emitted letter as the fiber bijection. That averaging is a separate
argument, using the free input bits and threshold 2r-2>=b. The two
claims must be checked separately, with their actual domains specified.
The reviewer reran no finite controls, and those controls cannot stand
in for the missing all-b derivations in its response.

## Remaining frontier and resumption

No source theorem status is promoted or downgraded by this review audit.
A usable fresh adversarial check of the five named transitions remains
missing. Do not repeat requests merely to obtain a favorable verdict.
A new reviewer must derive the identities with A, H, and F separated.

The research priority remains the boundary-sum inequality over ACTUAL
returns, retaining prescribed age versus ORIGINAL history length and
every observed-gate requirement. Its existing identity is in
`problem1_critical_cost_schedule_identity.md`, equations (4)--(6).
A nonlinear or history-word observable is a distinct surviving route.
No new census, width sweep, coefficient search or solver run is justified.
The lead-model issue is an execution constraint, not mathematical
exhaustion, a context-budget stop, or successful completion of the goal.
