# The cost of appended letters as a forced-schedule functional

Status: `partial-proof` for the exact all-age schedule and suffix-score
identities; finite certificates and refutations are stated separately.
Base checkpoint: `96a48d23a9ca9b0dbc1414aab3d02b06f24f473b`.
Problem 1, signed nonvanishing and the occurrence bounds remain open.

## Bottleneck, ranked routes and admission

The fixed-age cost pullback separates a prescribed history's cost into
its original positions and the positions appended during forced updates.
Universal W* descent already fails even on once-prescribed admissible
blocks. The unresolved near-boundary restriction couples elapsed time
to ORIGINAL history length, so increasing the fixed-age graph is not
the next step.

Ranked routes (`heuristic`):

1. Express the appended-position cost directly through the observed
   schedule. High all-age plausibility, low cost, and strong finite
   falsifiability. Test whether this contribution vanishes on continuing
   admissible trajectories before using that simplification in a proof.
2. Subtract the appended contribution and test descent of the remaining
   nonnegative cost. Low cost using already committed counterexamples;
   a failure prevents an unjustified repair of the previous potential.
3. Control both components when elapsed time is at least k-4. Direct
   relevance to the critical layer, but higher proof cost and no current
   invariant. Its original-length condition must remain explicit.

Choose routes1 and2's exact structural and falsification steps. First
replay only the two committed once-prescribed trajectories and the old
u18 trajectory. Compare actual current-position costs with the full
aged-letter formula, never with a letter's cost at birth. A positive
appended cost with another forced step refutes the zero-cost simplification;
failure of corrected descent rules out that repair on the stated domain.

The continuing zero-cost claim survived those stored rows. Admit a
second discriminating check: enumerate exact admissible branch cylinders
in increasing observed length, stopping after the first complete length
with a positive oldest appended-letter cost, or at length10 (the existing
stored observed horizon). This is a test of a cost identity, not an
ordinary-frontier or center-prefix census. If a positive cylinder is
found, test only its first16 residue lifts for ordinary membership by
exact inverse generators, stopping at the first success. The resulting
integers have complexity at most9; no frontier set is generated.
When those16 lifts all failed, admit the exact ordinary-generator
graph modulo16384 for the SAME target class5995. An accepting path
proves ordinary realization with no history-length cutoff; full
nonreachability would prove a forbidden class at every length. This
resolves the remaining scope question rather than extending the lift box.
All runs are local, bounded by120seconds and1GiB, with atomic records
and exact source, input, full Git and runtime provenance.

## Exact schedule determination (`partial-proof`)

Retain the definitions and formula (2) for beta_s from
`problem1_prescribed_history_cost_pullback.md`. In particular, omega is
indexed by an old prefix modulo2^b and the current generator, b>=2.
Let

    d=ceil((b-2)/2).

For every s>=1, two nonnegative integers having the SAME first s+d
OBSERVED forced branches have the same beta_s. More strongly, they have
the same complete ordered vector of born-letter generators and preceding
prefix residues modulo2^b at time s. No ordinary representation or phase
is needed for this assertion.

Proof. The fixed-age pullback shows that every entry of this vector
depends only on the initial integer modulo2^(2s+b), together with its
first s gates. The exact common-branch cylinder lemma supplies agreement
modulo2^(2(s+d)+2), whose exponent is at least2s+b. All s gates are
included. Hence every entry, and its weighted sum beta_s, agrees.

For W*, b=4 and d=1. One actual additional branch is sufficient to
determine beta_s from the schedule. An unobserved admissibility letter
does not supply that branch. This lemma does NOT claim beta_s=0.

## A uniform score on suffixes (`partial-proof`)

For W*, define a score K on each realizable observed branch word
tau of length l>=2. Choose any nonnegative integer z having tau as
its first l forced branches. Put e=l-2 and define

    K(tau)=omega(A(z) mod16,Q(z))                         if e=0,
    K(tau)=omega(A^(e+1)(z) mod16,
                 S_(A^(e-1)(F(z)) mod4))                if e>=1.

This is the age-e cost of the letter born at the first update, evaluated
at time e+1 after starting from z. It is
independent of the chosen z: the displayed inputs need at most2l+2
initial bits, and tau fixes exactly that cylinder. The score is either0
or1 and is defined from actual gates, not a proposed infinite future.

If q0...q_s is an observed branch word of length s+1, then

    beta_s=sum_(l=2..s+1) K(last l letters of q0...q_s).       (1)

Proof. A letter born at update t has age e=s-t at time s. Its
predecessor is x_(t-1), whose observed schedule is the suffix beginning
at q_(t-1). This suffix has length s-t+2=e+2. Its contribution in the
exact beta_s formula is precisely that suffix's K score. Sum over t.

The same construction for arbitrary memory b uses words of length
e+1+d and sums over the birth positions, with the same extra observed
tail d. Formula (1) is the b=4 specialization. It is not a finite-memory
recurrence: the suffix lengths in (1) grow with s. Proving bounded
memory or a sign/monotonicity property would require new arguments.

At length2, K=0 because every permitted append has zero W* cost.
At length3, K=0 because the first scanner pass on a born letter emits
S_(F(z) mod4)=S_3=p, which never pays W*. This reasoning does not
extend to older letters merely by repeating the zero-at-birth argument.
An initial independent derivation made that invalid inference; it was
withdrawn before adoption.

## Exact short-score obstruction

Claim status: `finite-exhaustive` for the short cylinder atlas. Each
observed word of length r has one residue class modulo2^(2r+2).
To extend a class represented by a, test its four lifts

    a+j*2^(2r+2), j=0,1,2,3.

Their r-step outputs are distinct modulo16: the exact valuation law
subtracts2r from their pairwise difference valuations. All outputs
are3 modulo4, so they run through3,7,11,15 modulo16. Exactly one lift
has each next branch t or u. This proves completeness of the finite
lifting procedure; beginning with residues11/t and7/u covers all
branch words. Discarding a prefix containing a forbidden factor cannot
discard any admissible extension.

The completed levels have2,3,5,8,12,17 admissible words at lengths
1 through6. The check stops at6, before the admitted cap10.
K is zero on every admissible word of lengths2 through5. At length6
its positive words are exactly

    ttuttu, tutttu, uttttu.

Consequently, for EVERY nonnegative integer with s+1 observed admissible
branches, beta_s=0 for1<=s<=4. At s=5, beta_5 is exactly1 when its
six observed branches are one of those three words, and0 otherwise.
This all-input implication uses the exact cylinder lemma and the complete
finite table; it is a bounded-time theorem, not extrapolation to all ages.

The first positive word in length-then-t/u order is ttuttu, with residue
representative5995 modulo16384. Its exact six-step orbit is

    5995 -> 26363 -> 103367 -> 409963 -> 1644155
         -> 6563111 -> 26329347.

At time5 the first born letter has preceding prefix A^5(5995)=1 mod16
and current generator S_(A^3(F(5995)) mod4)=u, so its cost is1.
The sixth branch is actually u; it is not an unobserved test letter.
The entire observed prefix ttuttu avoids uu, ttttt and ututtu.
Thus zero appended cost on all continuing admissible finite-integer
trajectories is `refuted`. Ordinary membership of this representative
is a separate question; it must not be inferred from its residue class.

For arbitrary s>=5, (1) also gives the all-age lower bound beta_s>=1
whenever the last six of its s+1 observed branches are one of the three
positive words. This is only a sufficient condition for positive cost:
longer suffixes can contribute, and no converse for larger s is asserted.

## Corrected descent and verification

The natural corrected cost is

    C_s(v)=W*(v_s)-beta_s(z)=W*(H^s(v)).

Claim status: `partial-proof` for this identity and0<=C_s<=n, where n
is the ORIGINAL nonroot word length. The bounds hold because H preserves
that length and each original-position weight is0 or1. They do not
establish descent on a return block.

Claim status: `refuted` for strict corrected descent on all once-prescribed
admissible three-return blocks. On the already committed cut1 witnesses,
phase p has C_1=0,C_7=2, and phase u has C_1=C_7=0. Thus subtracting
the born suffix does not repair universal strict descent, and phase p
also refutes universal nonincrease. These comparisons remain at cut1;
they do not refute the near-boundary restriction.

The phase-u endpoint at time7 has beta_7=1 but no following gate.
It refutes an unconditional all-age zero claim, not the continuing
version. The new ttuttu cylinder is needed for that stronger refutation.
Across the p/u witnesses, the seven common observed branches determine
equal beta_s for s<=6. Their unequal beta_7 values are outside the
schedule lemma's scope, because an eighth observed branch is missing
in phase u.

## Ordinary realization and finite verification

Claim status: `finite-exhaustive`. The integer5995 itself is not ordinary;
all16 tested integers5995+j*16384, j=0..15, fail exact inverse-generator
membership. These failures concern only the stated integers, not the
entire residue class. Complete inverse rejection certificates are checked
independently using bit-by-bit inversion of each generator.

The graph on16384 residues with ALL three ordinary-generator edges
has49152 edges. Independent forward and reverse methods give ordinary
representatives of the same class in both phases:

| Phase | Original k | Word FROM ZERO | Original endpoint |
| --- | --- | --- | --- |
| p | 14 | putpupupttuuuu | 0xc8e176b |
| u | 15 | utttttuutupupup | 0x190b976b |

Both prescribed trajectories execute ttuttu and have beta_5=1 with
the next actual branch u. No representation is reselected. Thus the
universal zero-suffix claim on continuing admissible ORDINARY histories
is `refuted` in both phases. Together with the complete short atlas,
time5 is the earliest possible positive beta_s in this domain, for
arbitrary original complexity. This minimum is in TIME, not integer
size. It is not a minimum over trajectories without admissibility or
without a further observed step.

Root distances13 and14 certify minimum nonroot word lengths for the
specific class5995 modulo16384, separately by phase. They do not claim
minimum complexity over all positive suffix-cost patterns. At time5,
the critical cuts k-4 are10 and11, respectively, so the examples do
not settle the near-boundary synchronized restriction. No physical
finite-seed realization or full three-return occurrence at time5 is
claimed.

Muse's stored-row implementation and the independent cell implementation
agree on all16 original cut1 rows and all11 old u18 rows. The u18 words
include a root letter; an initial parser counted it twice and was fixed
before adoption. Its corrected11 born costs are all0. This is finite
evidence only. The continuing zero-cost conjecture was tested beyond
those rows precisely because that finite absence did not prove it.

The independent implementation also reconstructs all48 cost components
at all14 new ordinary witness states. In total41 full decompositions
are checked. The short atlas is independently enumerated by residue,
while the initial probe used four-lift branch extension. Forward parent
arrays and reverse distances independently certify ordinary membership
and the stated minimum word lengths.

The portable verifier replays both forward parent arrays, including
26,589 discovered nodes and58,635 attempted edges, and checks the full
reverse-distance certificate on16,384 vertices and49,152 edges. It
compares27 old cost decompositions,14 new state/count tables and the
two new time-five born vectors. The41 full48-component decompositions
are independently checked by the cell implementation. The portable
verifier also verifies the16 inverse rejection trees and checks original
record/source/input hashes. All pass.

One original short-kernel reporting flag is preserved with an explicit
integration correction: `probe_states_match=false` compares a variable
overwritten by the later short-word scan. The runner's immediate probe
assertion passed; both independent replays verify the intended5995 orbit.
The false flag is not a failed orbit identity or accepted counterexample.

Records in `results/problem1/`:

- `20260905_born_suffix_kernel_probe.json`: the complete47-word short
  atlas, exact four-lift trials and original executed cell-rule source.
- `20260905_born_suffix_primary.json`: Muse's three completed records
  for stored rows, the independent short-kernel/inverse check, and the
  ordinary-word graph, with original sources and provenance retained.
- `20260905_born_suffix_independent.json`: independent cell-rule reverse
  graph, direct residue enumeration and all41 full cost decompositions.
- `20260905_born_suffix_verification.json`: portable complete comparison,
  graph certificates,16 inverse rejection trees and provenance checks.

The independent and verification sources support RULE30_REPLAY_ROOT
and RULE30_REPLAY_OUTPUT. They read committed inputs only. The immutable
reference remains unchanged; all completed runs stayed within their
local limits. Fresh adversarial mathematical review accepted the
identities with one incorporated wording correction: K at letter age e
is evaluated at time e+1 after its starting predecessor, not time e.
Final review accepted the mathematical and finite conclusions and
requested the two reporting clarifications above, now incorporated.
The reviewer then accepted the complete six-file checkpoint without
remaining corrections.

Next (`inconclusive`): control the original-position cost jointly with
the unbounded suffix score at ages comparable to original length.
The born cost cannot be discarded, and simply subtracting it does not
give universal descent. Do not extend the short atlas just to collect
more positive words. B_all, near-boundary three-return exclusion, signed
nonvanishing and the original whole-tail question remain open.
