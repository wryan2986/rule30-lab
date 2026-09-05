# Astra handoff (2026-09-04, base `a9af399`)

Repo does not solve any prize problem. Finite evidence is never proof of an infinite statement. Claim statuses (`empirical`, `finite-exhaustive`, `partial-proof`, `inconclusive`, ...) per `docs/experiment_protocol.md`.

## Checkpoint workflow (user instruction, 2026-09-05)

After every substantive research commit, push `research/astra-next` to origin
as a checkpoint. Before a long new research phase, ensure all established
results and the current handoff are committed and pushed. Never force-push,
rewrite history, merge to main, or include incomplete temporary files.

## Active frontier after the goal continuation (2026-09-05)

Newest exact zero-cost language and counterexamples: read
`proofs/informal/problem1_zero_cost_return_language.md` first, with the
prescribed-history definitions in `problem1_history_synchronization.md`.

- `partial-proof`: a verified r-branch word has exactly one input residue
  class modulo2^(2r+2). Sufficiency propagates gate precision; necessity
  pulls back the terminal mod4 agreement through the exact valuation law.
  The appended admissibility u is UNOBSERVED, so ututut needs14 bits,
  not a seventh gate. Its residue representative is903, still nonordinary.
- For nonnegative edge weights of residue memory b, zero-cost ordinary
  histories with that finite branch word are EXACTLY paths in a graph
  modulo2^max(b,2r+2), retaining only zero-weight edges. This is an
  all-history-length reduction, not a future-orbit quotient or a census.
- W*=count_(0,T)+count_(1,U), residues mod16, is now `refuted` as a
  universal strictly decreasing potential. The shortest zero-cost words
  in the per-phase ututut languages are p12:putptttttptu at0xc84387,
  with W*0->1, and u15:utututupupuuttt at0x191cc387, with W*0->0.
  Both are genuine cut0/gap222 ordinary occurrences. Minimality is only
  within the zero-cost languages, not among all descent counterexamples.
- Taking the minimum V_a(x)=min_w W*(w) over ALL ordinary representations
  does not repair strict descent: the witnesses prove initial V=0 and
  final V>=0. In u the final minimum is exactly0. That u endpoint is
  F(0x642fdfb), so requiring once-forced-reachable ENDPOINTS does not
  rescue V either. Arbitrary canonical selectors are not ruled out.
- Crucial limit (`partial-proof`): neither new ZERO WORD is a positive-
  time prescribed descendant. H_u of a nonempty history begins P, but
  the u witness begins T after its root. If H_p begins U, its second
  letter must be P (old prefixes13 then50/51); the p witness begins UT.
  Their lengths put both letters before the final append. The same u
  ENDPOINT has an induced representation with W*=2, which is different
  from the new zero word. Restricted prescribed-history/synchronized
  descent remains open; later minimization over all words changes scope.
- `finite-exhaustive`: forward searches visit3,011/9,720 states; the
  independent reverse certificate checks all16,384 vertices and47,104
  permitted edges. Root distances11/14 certify shortest zero-cost words.
  All14 witness states,12 forced transitions, edge tables and old u-state
  linkage agree. No frontier sets, other motifs or LP were generated.
  Records: `results/problem1/20260905_zero_cost_return_`
  followed by `{primary,independent,verification}.json`.

Fresh adversarial review accepted the mathematical claims and scopes.
Its verification correction is incorporated: the old induced W*=2 is
checked against all48 modulo16 counts and an independent word replay,
rather than the coarser modulo4 table. The refreshed verifier passes;
final read-only review accepted the correction and all five checkpoint
files without remaining corrections.

Next target: the zero-cost language of H(v)+Q with an ACTUAL preceding
forced step, followed by ututut. Prove sufficient residue precision and
output-edge costs before constructing the finite graph. This addresses
the surviving prescribed-history restriction; another arbitrary zero-cost
word would not. B_all, synchronized near-boundary occurrence exclusion,
signed nonvanishing and the whole-tail problem remain open.

Newest all-depth synchronization theorem: read
`proofs/informal/problem1_history_synchronization.md` first, with scanner
definitions in `problem1_frontier_head_dynamics.md`.

- `partial-proof`: for n=k-1 nonroot history letters, every scanner pass
  makes one more trailing letter depend only on the ORIGINAL endpoint x.
  Precisely, the ith letter of H^r(w) is S_(A^(r-1)v_i mod4); using
  pi^(n-i)x=A^(n-i)v_i gives an endpoint formula when i>=n-r+1.
  Hence all initial representations of x coalesce by r=n.
- Under defined forced steps w->H(w)Q, an appended letter's birth prefix
  is F^t(x) and its later prefix is A^(r-t)F^t(x). The whole appended
  suffix is independent of the initial representation. Only the first
  max(n-r,0) original letters can remain ambiguous.
- Periodic-core bijectivity accelerates this to
  R(h)=max(n-h,1+max tau_(a,j),j=2..h+1). The proved h3 bounds are
  p:max(k-4,5), u:max(k-4,4). Thus at cut c=k-4 (L=k-3), the start of
  the new dominant-empty layer, initial representations have already
  synchronized for p,k>=9 and u,k>=8, conditional on the segment existing.
  This does NOT prove occurrence exclusion or termination.
- Synchronization concerns only the prescribed descendants of histories
  of fixed original (x,phase,k), at elapsed time r. It neither forgets x
  nor canonicalizes ALL representations of the later endpoint F^r(x).
  Later reselection remains outside the theorem; a growing word remains.
- `finite-exhaustive`: both implementations agree on19,682 words through
  k9,1,138 endpoint groups and9,096 complete endpoint/age image sets;
  all167,306 iterate and634,776 suffix-position checks pass. The first
  one-pass failure is p5,x802: nonroot tttu and tutt give H images upup
  and uppp, coalescing at2. Max ages0,1,1,1,2,3,3,3,4 in both phases
  are finite data, not an all-depth growth law. No cap was increased.
- The certified u18/0x6473d46ab/cut4/gap222 probe refutes strict block
  descent of the earlier16-state count W_0t: it stays0->0. The two-edge
  count W*=count_(0,T)+count_(1,U), residues modulo16, has2->0 on BOTH
  the oldu14 and newu18 blocks. It is nonnegative on every history, but
  universal descent remains `inconclusive`. No LP or new occurrence
  census was needed. The same ten-step orbit verifies225 formula letters
  and242 prefix identities for the forced-history extension.
- Muse independently derived the synchronization proof and checked the
  scopes. Fresh adversarial review accepted the core/forced indices and
  the distinction between initial-history synchronization and later
  endpoint canonicalization. Original sources, runner/data/input hashes
  and independent portable verification are retained in
  `results/problem1/20260905_history_synchronization_`
  followed by `{primary,independent,verification}.json`.

Final read-only review explicitly accepted all synchronization formulas,
the complete finite comparisons and provenance chains without corrections.

Next: falsify W* on another already certified block, and seek descent or
a forbidden return pattern on the explicit synchronized family. Keep k
the INITIAL complexity and state whether later history reselection is
allowed. Do not fit a coalescence law by increasing the cap. Genuine
occurrence exclusion, B_all, signed nonvanishing and the whole-tail
question remain open.

Newest history-potential obstruction: read
`proofs/informal/problem1_history_potential_obstruction.md` first, followed
by the scanner definitions in `problem1_frontier_head_dynamics.md`.

- The universal four-state additive descent class is `refuted`: fixed
  real edge weights indexed by (old prefix modulo4,input generator),
  a uniform lower bound over ALL ordinary histories, and strict decrease
  on every genuine three-return block under the prescribed history update.
  Negative individual weights are allowed. Pumping forces nonnegative
  reachable cycle weights, so a nonnegative circulation cannot decrease.
- The genuine u14/0x642fdfb/cut1/gap222 witness, from-zero word
  uuuuputptuutuu, supplies exactly such a circulation. After the first t,
  its nonroot history is pptpttpuppuppt; after the following ututut it is
  ppttpupttpupppptuppt. The added edges decompose into cycles (0,t),
  (0,p)(3,p), and (1,p)(2,u)(3,t). Their weights sum to a nonnegative
  block change for EVERY potential in the stated class (`partial-proof`).
  This also excludes representation-independent endpoint potentials in
  that class, but not phase-p-only or selected-history claims.
- The same pair does NOT exclude the sixteen-state additive class.
  Its refined edge counts fall on (0,t):2->0, (3,u):1->0 and (15,p):1->0.
  Counting (0,t) modulo16 is nonnegative on all histories and decreases
  on this pair. No universal descent property for that count is claimed.
  All48 refined counts coarsen to the verified12-edge circulation.
- Two preliminary examples were rejected before proof adoption:903 has
  no ordinary representation (head225 absent from p4; all33 last edges
  fail), and7->27 has history t->pu, not u->pu, so it alone supplies no
  letter-weight obstruction. The genuine witness is separately verified.
- `finite-exhaustive`: two implementations agree on eight genuine states,
  seven updates, all count tables and the cycle certificate; no alternate
  representations or new occurrence census. Muse independently derived
  the pumping argument and checked the scopes. Fresh adversarial review
  accepted the proof with an incorporated clarification: changing any
  premise, not merely state memory, can escape this specific no-go.
  Final read-only integration review approved all shared finite fields,
  provenance chains, timing and portable verification without corrections.
  Records: `results/problem1/20260905_history_potential_`
  followed by `{primary,independent,verification}.json`.

Next test: falsify the concrete sixteen-state count candidate on another
already certified block, or test simultaneous additive constraints on a
few named blocks with exact rational certificates. Do not enlarge an
occurrence census or infer universal descent from this one decreasing
instance. B_all, the dominant-empty-layer occurrence exclusion, signed
nonvanishing and the whole-tail target remain open.

Newest dominant-boundary theorem: read
`proofs/informal/problem1_cyclic_seed_boundary.md` first, followed by its
dependency `proofs/informal/problem1_frontier_head_dynamics.md`.

- All-depth (`partial-proof`): at residual seed complexity s=k-1-L>=1,
  dominant endpoints inject into A^L(O_(a,s)) by y->y>>2L. This is a
  necessary seed restriction, not an endpoint realization theorem.
- Dominant beliefs are empty for both phases at L=k-2,k>=3; for phase p
  at L=k-3,k>=5; and for phase u at L=k-3,k>=6. Fixed-k endpoint-set
  monotonicity extends each threshold to larger L, with old raw separation
  handling L>=k-1. The proofs use the highest mask for residual level1
  and phase-p level2, and the second-highest mask for phase-u level2.
- Uniformly k>=6, dominant nonemptiness or signed nonvanishing requires
  L<=k-4, hence c<=k-5 when L=c+1. This is NOT a proved occurrence
  bound or a strengthening of raw adjacent separation. B_all still means
  the old all-occurrence obligation L<=k-2. A genuine occurrence at
  L=k-3 or k-2 would refute the dominant/signed strengthening while
  remaining compatible with that B_all bound.
- `finite-exhaustive`: direct residue-first and independent cell/odd-section
  seed-first implementations agree on all3,391 admitted cylinders through
  k9, both phases, L in {k-3,k-2,k-1},1<=L<k. All112 raw endpoints and
  their364 mask steps agree; all19 surviving dominant beliefs are singletons.
  Exact small exceptions: p,k4,L1 at x204,205,207; u,k4,L1 at all9
  states; u,k5,L2 at x404,405,408,409,411,414,415. These refute lowering
  the respective second-level k thresholds, for ordinary cylinders only.
  No return occurrences or new frontiers beyond9 were generated.
- Muse independently derived and checked the masks/proofs; an arithmetic
  slip in its first phase-u calculation was independently caught and
  corrected. Fresh adversarial review accepted all three all-depth lemmas,
  their quantifiers and the dominant-versus-raw distinction. The lead
  independently compared every finite row and original artifact hash.
  Final fresh integration review also compared every row/base certificate
  and validated the provenance hashes, approving the checkpoint without
  remaining corrections.
  Records: `results/problem1/20260905_cyclic_seed_boundary_`
  followed by `{primary,independent,verification}.json`.

Next target: an explicit constraint coupling the forced-return language to
these high-mask obstructions via the exact growing history scanner. Merely
propagating the head condition is automatic and cannot exclude an
occurrence. Specify a falsifiable joint constraint before admitting another
run; do not enlarge an occurrence census. B_all, dominant nonemptiness,
signed nonvanishing and the whole-tail target remain open.

Newest exact frontier-head and periodic-core theorems: read
`proofs/informal/problem1_frontier_head_dynamics.md` first.

- With A(v)=T(v)>>2=(v>>2) XOR((v>>1) OR v), the exact leading-block
  marginal is pi^(k-h)(O_(a,k))=A^(k-h)(O_(a,h)). These sets shrink with
  the remaining generation count. This is an all-depth refinement of plain
  projected-prefix membership, not a sufficient test on prescribed lower bits.
- The stabilized head set is the ENTIRE periodic-point set of A at the
  corresponding phase bit length. Every such periodic point has an ordinary
  generator history: take a predecessor on its A-cycle, project two bits,
  induct to the root, and recover the last generator from the discarded digit.
  This theorem permits multiple cycles and requires no uniqueness conjecture.
- Binary cycle lifting has reset, flip and splitting cases. All cycle
  periods are powers of two; positive width w has transient at most
  2^(w-1)-1 and A_w^(2^w-1)=A_w^(2^(w-1)-1). These are all-depth
  statements (`partial-proof`), not extrapolations from the small catalogue.
- On a permitted forced step, F(x)=4A^2(x)+3. Consequently
  pi^r(F^r(x))=A^(2r)(x) for every defined orbit segment. Evaluating the
  total expression outside residues7/11 does not supply a valid continuation.
- Exact forward-history update: retain the root, scan the old generator
  word using its prefix modulo4, emit S_(new residue) with S0=T,S1=U,
  S2=S3=P, then append the actual forced Q. Tracking prefix modulo16
  also decides the gate: terminal7->U,11->T, otherwise stop. The word
  grows; this is not a finite-state endpoint quotient or an endpoint count.
- Finite checks: widths1..16 each have one cycle, periods1 on1..3,
  2 on4..8,4 on9..16. Uniqueness beyond16 remains conjectural and is
  unnecessary for the core theorem. Both implementations agree on all18
  frontier sets throughk9,90 marginals,16 cores throughh8, and234 strong
  and weak stored-orbit identities. All45 periodic-point generator histories
  and their scanner updates pass, including8 valid forced appends.
- The old456-bit counterexample is excluded already by its aged level3
  head:52 is absent from A^225(O_(p,3))={50,55}. Plain membership first
  rejected level4. No new integer or occurrence census was run. Muse
  independently derived/reviewed the all-depth results; fresh review accepted
  the core induction and exact history/gate distinction.
  Final review also approved the complete finite coverage and provenance
  integration, with no remaining corrections.
  Records: `results/problem1/20260905_frontier_head_`
  followed by `{primary,independent,verification}.json`.

The earlier proposed use of aged seeds at residual levels1,2 is now
completed by the dominant-boundary theorem above. It sharpens only the
dominant-empty boundary, not the raw-shadow or genuine-occurrence bound.
The longer target is a return-conditioned potential or forbidden pattern
for the exact growing history scanner plus forced append, excluding cuts
c>=k-2 with k the INITIAL word complexity. Simply propagating the head
membership condition is automatic under A and supplies no new exclusion.
Do not enlarge the cycle catalogue or assume a unique attractor. B_all,
adjacent inclusion, signed nonvanishing and eventual center periods>=3
remain open; the discarded digits and return language still need coupling.

Newest all-depth theorem and boundary obstruction: read
`proofs/informal/problem1_periodic_schedule_rationality.md` first.

- Every eventually periodic auxiliary branch schedule has a rational
  2-adic survivor (`partial-proof`). For a pure period p, the cyclic phase
  equations give a spatial recurrence on four p-bit vectors after bit five.
  There are at most 2^(4p) states; a repeated sufficient state certifies
  the full rational expansion. Inverse generators preserve rationality,
  handling a finite schedule preperiod. No converse or periodicity of the
  actual moving fringe is asserted.
- Consecutive nonzero base-four digits of a pure period-p survivor have
  distance <=2p, by the existing arbitrary-integer periodic-prefix bound.
  This is an all-depth spatial constraint, not B_all or signed nonvanishing.
- The named t,u,ututtt,ttututt cycles have mu0 and lambda2,2,138,728,
  with spatial onset2. Independent vector/cell-array and packed/local-QP
  implementations agree on every vector and all15 rational phase values.
  Neither zero transient nor least phase period is asserted universally.
- The bit-length-only boundary strengthening is now `refuted`. Truncating
  phase5 of the ttututt comparator at456bits gives k228 and the exact
  forced word (ttttutu)^32 ttt ututut, then termination after233branches.
  It has cut227/gap222, exceeding the claimed maximum225. This is the
  first failure in the declared finite truncation order, not a global minimum.
- The counterexample is NOT in an ordinary frontier: even bit length
  leaves only p228, but its projected top8bits are0xd2=210, absent from
  O_(p,4)={200,201,202,203,204,205,207,220,221,222,223}. The first three
  projected levels pass. Thus B_all remains open; bit length alone cannot
  replace its frontier hypothesis. No fixed leading-width sufficiency follows.
- Muse independently derived/reviewed the theorem and hand-checked the
  compact frontier rejection. Dewey ran the four-word cycle/truncation check;
  lead replay agrees on all233 witness transitions and its admissibility.
  Fresh review approved the recurrence, rationality and gap proof scopes.
  It also approved the complete boundary/nonmembership certificates and
  provenance integration, with no remaining corrections.
  Records: `results/problem1/20260905_periodic_rational_`
  followed by `{primary,independent,verification}.json`.

Next target: a frontier-conditioned boundary invariant at the five critical
cuts, or an explicit joint signed-correlation constraint. The arbitrary
integer bit-length simplification is closed; do not enlarge its box or the
periodic comparator family. This witness's four-digit rejection is a local
certificate, not a proposed universal invariant. B_all, adjacent inclusion,
signed nonvanishing and general eventual center periods>=3 remain open.

Newest actual-domain spectral obstruction: read
`proofs/informal/problem1_walsh_sign_obstruction.md` first.

- Exact all-depth endpoint lift (`partial-proof`) is a diagonal 0/+1/-1
  filter followed by injective digit embedding. Unnormalized Walsh lift:
  W F(4xi+eta)=chi_eta(d) W(a_m f)(xi), with W(a_m f) the normalized
  convolution of W a_m and W f. This retains endpoint identities and
  deduplication; it is not a nonvanishing proof or a finite closed state.
- An affine-character description of defect signs is `refuted` on the
  genuine u14/0x642fdfb/L2/cut1/gap222 belief. The exact quartet
  0x190822b,0x190825b,0x191c10b,0x191c17b has XOR0 and costs0,1,0,0.
  This excludes every affine character, even chosen separately for this
  belief or after invertible affine coordinate changes.
- The obstruction localizes to depthj1, currentmask1100, at inputs
  y>>4 =0x190822,0x190825,0x191c10,0x191c17 in O_(u,11). Their
  shadowmasks are1111,1100,1111,1111. On the affine plane with directions
  0x7 and0x1432 the local signs +,-,+,+ have Walsh coefficients
  (2,2,-2,2). The final depthj0 full-mask filter preserves all four.
- All-depth restriction lemma: a four-point XOR-zero sign pattern with
  product-1 forces a nonzero ambient coefficient in EACH of four plane
  frequency classes, for any real extension, including zero extension.
  It also holds in the affine span of the belief. A class-(0,0) coefficient
  need not be the global zero frequency. This is a lower bound, not a
  four-mode closure theorem, and it does not imply global S!=0.
- Exactly one134-point belief was reconstructed: primary Boolean carrier
  throughu13; independent cell-array seeds throughu11 plus recursive lifts.
  All134 endpoint costs/masks agree (E84,O50,S34). A sorted-triple search
  and independent8911-pair search give the same lexicographically first
  quartet. Four is the minimum possible affine-certificate cardinality.
  Muse independently checked the operator, plane theorem and concrete XOR
  without tools. No ambient Fourier array or new occurrence census ran.
  Fresh reviewer Ramanujan approved the proof scope, seed initialization,
  provenance hashes, complete table agreement and portable replay paths.
  Records: `results/problem1/20260905_walsh_sign_{primary,independent}.json`.

The exact bottleneck is now explicit in Walsh language: control the joint
coefficients contributing to zero frequency on genuine returns. One-mode
sign modulation is refuted; general multimode/nonlinear descriptions are
not. Do not automatically raise a mode or polynomial-degree cap. A useful
next step must specify a return-conditioned correlation constraint, with
deduplication retained, or a new boundary mechanism. B_all, adjacent
inclusion, signed nonvanishing and eventual periods>=3 remain open.

Newest all-depth classification and obstruction: read
`proofs/informal/problem1_two_to_one_rewrite_test.md` first.

- Exact 27-entry table (`partial-proof`) gives v2(B(A(v))-C(v)) for
  every positive v and A,B,C in {T,U,P}. Common suffixes preserve it.
  Above the two lowest bits, a successful two-to-one shortening requires
  a highly divisible actual prefix before or inside the changed block.
- If all positive proper prefixes of every fixed-phase representation
  have valuation <=H, every noninitial two-to-one rewrite has difference
  valuation <=max(H+1,2). Initial-pair replacement keeping the phase
  fails already modulo4, by the separate root calculation.
- Universal two-to-one shadows are `refuted` on the SAME genuine
  u18/0x6473d46ab/cut4 occurrence. All288 representations have only19
  proper-prefix states, maximum valuation3. Every rewrite therefore has
  difference valuation <=4, below the required10. Arbitrary exact
  re-expression of this endpoint cannot rescue the construction.
- Exactly13824 labelled noninitial rewrites,138240 modulus comparisons,
  and114 distinct local cases were independently checked. No successes;
  valuation histogram {0:7744,1:3008,2:1920,4:1152}. The word family
  covers17/18 pair/parity contexts; separate54 local checks atv1,2 cover
  the missingTP-even seam. No other occurrence or block size was tested.
- Muse independently derived the table and bound without tools. Dewey's
  packed implementation and lead cell-array/odd-section replay agree on
  the entire ordered rewrite-output stream, every local case, and all54
  auxiliary cases. Fresh review corrected odd-gamma bound wording and
  JSON-key normalization; no mathematical outcomes changed. Records:
  `results/problem1/20260905_two_to_one_{primary,independent}.json`.

Two-to-one rewriting is now refuted, not an untested next candidate. Do
not automatically increase rewrite width. The next structural direction
is an exact operator/Walsh description of return-conditioned endpoint
transfer, retaining deduplication and joint correlations. Start with
`proofs/informal/problem1_signed_slice_joint_transfer.md` and
`proofs/informal/problem1_period_two_signed_belief_derivative.md`.
Small-residue permutation parity is only a possible quantity to investigate;
no bridge to signed mass has been established. Preserve the exact scopes
of universal five-vector closure, scalar/sign-only, and valuation no-go
results. The strongest bottleneck is still B_all or return-conditioned
nonvanishing; adjacent inclusion and general periods>=3 remain open.

Newest certificate-class obstruction (`refuted`): read
`proofs/informal/problem1_generator_deletion_test.md` first.

- Exact all-depth deletion law (`partial-proof`): deleting a noninitial
  generator from a representation preserves the residue modulo 2^m iff
  it is T and its positive input is divisible by 2^(m-1). Common suffixes
  preserve the first differing bit. U/P deletion always changes parity.
- The maximum H over T-input valuations on ALL root-reaching ordinary
  representations has an exact phase-gated predecessor recursion. A
  single-deletion shadow at cut c exists iff H>=2c+1. For odd x such a
  deletion also forces c<=k-4, one cut stronger than B_all. This is a
  conditional theorem, not a proved occurrence bound.
- Both initial map counterexamples admit single-deletion shadows. For
  u14/0x642fdfb/cut1 delete position7 of its chosen word. For
  p16/0xc85f8787/cut2 the chosen word fails, but another of its216
  representations works; its global H is7. Failure of one representation
  must therefore not be mistaken for failure over all representations.
- The preselected deeper genuine occurrence u18/0x6473d46ab/cut4,
  w=tttt, gap222 REFUTES the universal single-deletion construction:
  every one of its288 representations has H=3, below the required9.
  Exact word language: u A t u A t t u D D A u A p A p, where
  A={u,p}, D={tt,up,pp}. The two independent graphs agree on all140
  nodes,417 inverse attempts,20 reachable nodes, counts and maxima.
- Muse independently reviewed the all-depth criterion, phase scope and
  conditional cut bound without tools. Dewey implemented exact partial
  inverses and certificates; lead signed-inverse/bottom-up replay agreed
  node by node and verified the288-word factorization. Only two initial
  endpoints and one already documented deeper endpoint were checked.
  Fresh reviewer Ramanujan accepted the mathematical scope and factorization;
  its comparison-script portability correction is incorporated.
  Four atomic records: `results/problem1/20260905_generator_deletion`
  followed by `{,_deep}_{primary,independent}.json`.

Next untested route: a specified shorter contiguous generator-block
replacement, first on the same288-word failure family. A successful finite
rewrite would need an all-depth selection rule. Single deletion is now
refuted, not a surviving conjecture. Adjacent inclusion, B_all and signed
nonvanishing remain open; this occurrence still has signed mass2.
The strongest bottleneck remains all-depth critical-cut exclusion or an
invariant of return-conditioned endpoint correlations. No larger census
or proof of eventual-alternation exclusion follows from these results.

Newest completed falsification (`refuted`): read
`proofs/informal/problem1_conjugated_projection_test.md` first.

- The distinct candidate y=B_w(R(F^c(x))) restores exactly the base word w
  in Z_2 and then stops. Each inverse block must include its own 4v+3.
  An exact nonnegative-inverse failure at any stage excludes y in N;
  if all stages succeed, bitlen(y)=bitlen(x)-2. These conditional facts
  are all-depth (`partial-proof`), not a frontier-membership theorem.
- Gate A (always nonnegative) is refuted by u14/0x642fdfb/cut1:
  its unique candidate is the exact negative integer -0x303f635.
- Gate B (lower-frontier membership when nonnegative) is independently
  refuted by p16/0xc85f8787/cut2, w=ut, gap422: y=0x32157a47
  has the correct size, congruence, and complete word, but is absent from p15.
  A compact proof projects to p8/0xc855. Its three generator predecessors
  all project to p5/0x37a; the exact fiber over 222 misses its digit 2.
  The certificate reduces rejection to O_(p,2)={12,13}, without a census.
- Exactly the same 19 historical labels were checked: A passes16/fails3;
  B passes14/fails2 among the16. All14 cut-zero labels pass both, and all5
  positive-cut labels fail one gate. This last pattern is finite only.
  Both constructions' failures leave adjacent inclusion and B_all open.
- Dewey implemented exact partial-inverse/lift-membership checks; the lead
  independently replayed every row using signed inverses and direct
  generator predecessors. Muse Spark 1.3 Contributor completed corrected
  tool-free inverse-branch derivation and a hand review of the compact
  rejection certificate; it did not run the finite checks. Fresh reviewer
  Ramanujan accepted the full mathematical scope; count terminology and
  replay portability were corrected. The primary record preserves its raw
  input, so the independent embedded source needs no temporary-directory
  data. Atomic records:
  `results/problem1/20260905_conjugated_projection_{primary,independent}.json`.

The proposed conjugated projection below has now been tested and refuted;
its earlier untested status is historical. Next untested candidate: delete
a generator from an ordinary representation to construct a lower state
with the required base congruence, starting with the named failures. A
failure for one representation would not exclude all representations.
No larger census follows. The strongest bottleneck remains an all-depth
critical-cut exclusion (B_all), or a return-conditioned endpoint invariant
proving nonvanishing; no such invariant has been established.

Newest all-depth result (`partial-proof`, independently reviewed): read
`proofs/informal/problem1_rounded_projection_obstruction.md` first.

- The natural root-preserving projection R(x)=(x>>2) OR 3 deletes one
  base-four digit. If the first two forced letters agree, it intertwines
  with F. If they differ, R(x) stops. More exactly, an initial run a^ell
  followed by the other letter gives COMPLETE sigma(R(x))=a^(ell-1).
- Every full-domain three-return occurrence therefore projects to an empty
  schedule or at most three t's. For ANY positive cut it fails even the
  base word w, not just the return continuation. At cut0 the base word is
  empty, so a lower-frontier R(x) could still be an adjacent cylinder witness.
- Frontier membership is separate: for a first t and k>=3, R(x) always
  lies in O_(a,k-1), by projection plus digit-2 pairing. The genuine
  u14/0x642fdfb/cut1 example projects to u13/0x190bf7f, which stops at
  residue15 and fails base word t. This refutes the direct projected witness
  on the genuine domain, without refuting adjacent inclusion or B_all.
- For the full 2-adic survivor set K, exactly
  K intersect R^(-1)(K) = R(K) intersect K = {1/3,5/3}.
  These are the constant-t/u survivors. R sends every admissible infinite
  survivor outside K; it cannot preserve a nonempty subset of K_adm.
- Same x4..4095 box: 260 equal-pair checks, 267 mixed-pair checks,
  171 first changes; all pass. All 19 historical occurrences independently
  replayed, with 18 empty projected schedules and one t; all five positive
  cuts lose the base word. No new frontier census or cut-zero membership
  check was run. Atomic records:
  `results/problem1/20260905_rounded_projection_{primary,independent}.json`.
- Muse terminated with a provider undeclared-tool routing error, not a
  completed check. Dewey implemented and independently derived the finite
  identities; fresh reviewer Ramanujan checked the full proof and Z_2 scope.

Next distinct candidate: y=B_w(R(F^c(x))), projecting at the occurrence cut
then pulling back through the inverse zero branches for w. This preserves
w in Z_2 but is NOT known to be an ordinary finite lower-frontier state.
A targeted exact check on existing occurrences could test finiteness and
membership; no such check has yet run. This avoids conflating loss of the
return continuation with the weaker base-prefix requirement for a shadow.
Use the existing exact partial generator inverses and recursive frontier
membership criterion for that targeted check, not an arbitrary-precision
truncation treated as a proof of finiteness.

Previous all-depth result (`partial-proof`, independently reviewed): read
`proofs/informal/problem1_finite_schedule_repetition_bound.md` first.

- For a positive finite integer of complexity k=ceil(bitlen/2)>=2, two
  orbit tails at i<j sharing r observed branches satisfy r<=k+j-2. The
  proof compares exact congruence modulo 2^(2r+2), valid even for terminal
  endpoints, with bitlen(x_j)=bitlen(x)+2j.
- Any p-periodic observed prefix of length n therefore has n<=k+2p-2.
  A periodic factor of length n starting at m has n-m-2p<=k-2. Thus
  unbounded such repetition excess on an infinite auxiliary schedule
  excludes a finite integer survivor, even without eventual periodicity.
  An explicit aperiodic admissible example W_0=uttt,
  W_(h+1)=W_h^3 utttt has unbounded excess. It is NOT the actual fringe.
- An occurrence of observed motif length B at cut c whose WHOLE observed
  prefix is p-periodic satisfies c<=k+2p-B-2. For B>=2p+1 this proves
  B_all on that subclass, even without frontier membership. Gaps (p,p,2)
  give c<=k-4; equal local gaps alone do not imply prefix periodicity.
  If periodicity starts at m, the bound is c<=k+2m+2p-B-2 instead.
- Exact scope obstruction: this short-period certificate forces the three
  observed u's to lie at c,c+p,c+2p, so it can cover only the four canonical
  labels with r0=r1, never the other 11. The known p15/0x37b38787/cut0
  gap242 occurrence is outside it (motif ututttut has least period6).
  This is a certificate limitation, not a counterexample to B_all.
- Reused exactly x=4,...,4095: 2,186 tail pairs, 1,391 prefix-period
  instances, 2,964 periodic factors; no violation or equality. Full cell
  replay and all counts agree. Occurrence coverage is only x903/cut0;
  positive-m occurrence cases are absent. W_0,...,W_4 also checked.
- Muse attempt terminated HTTP 429. Default contributor Dewey implemented
  and independently derived the bounds; fresh reviewer Averroes checked
  the full proof and aperiodic construction. Atomic records are
  `results/problem1/20260905_finite_schedule_repetition_{primary,independent}.json`.

The unresolved issue is still exclusion of arbitrary critical-cut prefixes.
No all-depth repetition property is known for the actual fringe; the old
seven-block mirage is not revived. A larger repetition scan is not the next
step. This criterion requires a structural recurrence forcing unbounded
excess, or a different invariant for prefixes outside its boundary subclass.

Previous exact reduction (`partial-proof`, independently reviewed): read
`proofs/informal/problem1_canonical_return_boundary.md` first.

- Canonical third gap 2 reduces the 56 labels to 15 while preserving the
  exact set of state/cut cylinders, their beliefs, signed masses, and
  ancestor closure. It changes an admissibility label, not physical returns.
- At any threshold b, an occurrence at ANY cut >=b exists iff the longest
  admissible prefix has three u's at/after b and an observed t after the
  third. This localizes the occurrence to one of b,...,b+4 using at most
  b+16 observed symbols, for finite or infinite schedules, including those
  becoming inadmissible. The appended final u remains unobserved.
- Consequently B_all is equivalent to exclusion at just five cuts
  k-2,...,k+2, depths k-1,...,k+3, using the first k+14 branches. The
  four depths >=k are not silently dropped. B_all would imply a maximum
  admissible prefix length k+13, sharpening the earlier conditional k+17.
  Moving cuts does NOT preserve signed mass: this localization is only
  for boundary existence. The quantifier over every k remains open.
- Lead checks: all 25,208 admissible words through length 22; all 8,191
  binary words through length 12; b=0,...,6. All 233,793 threshold checks
  pass. The existing 19 rows reduce to 17 unchanged cylinder certificates.
  Atomic records: `results/problem1/20260905_canonical_return_{rows,words}.json`.
- Two Muse reviews terminated with provider HTTP 429 and supplied no
  completed check. A fallback default reviewer independently accepted the
  combinatorial proofs. It flagged the same caveat corrected by the lead:
  continuation-stability applies only after the full horizon is observed,
  not when extending a shorter terminated word.

B_all, signed nonvanishing, and general eventual periods remain open. The
strongest next boundary target is an all-depth exclusion of these five
moving cut positions, retaining ordinary-frontier membership. This exact
reduction does not authorize a larger census.

The earlier bit-length-only simplification was `inconclusive`; see
`proofs/informal/problem1_boundary_bitlength_test.md`. All x=4,...,4095
were checked without frontier restrictions, with independent cell-array
full-orbit agreement (1,039 forced transitions). No boundary occurrence
was found, but only x903/k5 has ANY occurrence, at cut0, far below its
critical cut3. This is weak finite coverage, not evidence that membership
can be discarded. No box enlargement follows. The stronger arithmetic
candidate said every occurrence at c requires x>=4^(c+2); the new structured
456-bit counterexample above refutes it without enlarging that integer box.
The degree law
alone supplies no decreasing rank: bitlen(F^j(x))=bitlen(x)+2j.

Previous result: **both valuation conjectures are refuted**. Read
`proofs/informal/problem1_return_valuation_falsification.md` first.

- Actual occurrence: u/k17/`0x190b9fdfb`, L2, cut1, gap222. E=525,
  O=421, N=946, S=104; v2(N)=v2(2O)=1. Observed word `tututut`,
  admissibility word `tutututu`; the appended final u is not observed and
  need not be under the original definition. This refutes the occurrence-only
  gate without refuting signed nonvanishing.
- Genuine ancestor: u/k16/`0x6473d46a`, L3, strips two digits from the known
  u/k18/`0x6473d46ab`, L5, cut4 occurrence. E=52,O=36,N=88,S=16;
  valuations coincide at 3. Its two required lifts recover the gate:
  (E,O)=(52,36) -> (25,10) -> (11,9), current masks 1111 then 1011.
- The existing phase-u gap222 box through k18 was replayed for this new
  observable: 26 occurrences, 43 ancestors. Ancestor search stopped at 22;
  occurrence-only search stopped at 13. No truncations or excluded depths.
  The earlier 25-ancestor box originated only from occurrences through k16;
  it did not contain this ancestor of a k18 occurrence.
- Muse implemented the bounded checks and independently verified the ancestor.
  After two workers hit provider rate limits, the lead completed the actual
  occurrence and three-node-chain replay using the old independent oracle,
  with full Boolean/packed frontier agreement through k18. Four atomic
  `20260905_return_*valuation*.json` records retain exact provenance.

Current bottleneck: signed nonvanishing (or dominant nonemptiness) on genuine
return occurrences, plus the all-cuts boundary obligation B_all if using
adjacent inclusion. The exact valuation gate is no longer a surviving route.
Next structural work must control concrete endpoint correlations over genuine
returns or prove an occurrence-cut bound. No ad hoc relaxation or census-cap
increase follows from these counterexamples. General periods >=3 remain open.

Earlier refinement after publication at `f4d3eae`:

- `proofs/informal/problem1_physical_frontier_restriction.md`:
  exact physical parameterization R_d by odd seeds of bit length
  s<=floor(d/2), at the uniquely possible time n=d-s (`partial-proof`).
  The known pairing obstruction `0x642fdfb` is absent from R_27: all 4096
  candidates checked, with independent full packed/cell-array agreement
  (`finite-exhaustive`, named state only). This does not prove physical
  pairings exist. Physical projection closure is `refuted`: `0xcd` from
  S9/n4 belongs to R_8 but projects to 51, outside R_6={50,55}. Thus a
  physical-only induction needs its own ancestor-domain argument.
  Even genuine local alternation is insufficient: x27 from S3/n3 has
  centers 1010 but an empty depth-one dominant belief. Its forced word is
  only t, so this does not threaten the full three-return conjecture.
- `proofs/informal/problem1_signed_count_transfer.md`: exact all-depth
  even/odd total update from outgoing mask subtotals (`partial-proof`).
  Universal valuation preservation is `refuted`: p/k5/D1/`0x321` passes
  with (E,O)=(2,0), but digit-zero child p/k6/L2/`0xc84` cancels (1,1).
  The earlier p/k6 `0xc82`/`0xc88` collision also refutes deterministic
  closure of all TEN even/odd slice counts, not just five signed counts.
  These ordinary cylinders are not certified admissible ancestors.

Both new notes retain exact domain and proof/evidence boundaries. The
valuation conjecture was still open at this earlier milestone and is now
refuted above. Physical occurrence-cut bounds, B_all, and periods >=3 remain open. The next structural target must retain return
constraints and endpoint correlations; neither bare physical membership
nor the unrestricted parity-count update supplies a closed induction.

`ASTRA_GOAL.md` requests continued research until its proof-or-research-impasse
stopping condition. That goal is still active: there is no complete proof,
and the remaining boundary and return-correlation routes have not been exhausted.
Read these new notes before the earlier continuation below:

1. `proofs/informal/problem1_three_return_boundary_sufficiency.md`
   (`partial-proof`): an unconditional physical-row membership lemma:
   for positive S, s=bitlen(S), n>=s, `T^n(S)>>n` lies in phase frontier
   `O_(a,ceil((s+n)/2))`, with a=p for even s+n and u for odd s+n.
   Direct physical two-step evolution gives the exact forced recurrence
   under an alternating center. Thus an eventually alternating trace from
   any odd positive finite S produces an infinite admissible frontier
   schedule, including arbitrary finite temporal transients.
2. The same note proves that the unproved boundary bound `c+1<=k-2`
   on the full occurrence domain, at ANY cut c>=0 (hypothesis `B_all`),
   ALONE excludes such an infinite schedule and therefore would exclude
   eventual alternation. It is a standalone sufficient route, not merely
   cleanup required after a signed-mass proof. Even a weaker proved finite
   bound on admissible occurrence cuts at each fixed k would suffice.
   The bound itself remains open; periods of least period >=3 are unhandled.
   A bound restricted to `L=c+1<k` does not suffice for this argument;
   excluded larger cuts must also be covered. This is the original full
   adjacent-inclusion domain, not the restricted signed-mass domain.
3. `proofs/informal/problem1_signed_belief_pairing_obstruction.md`
   (`refuted` certificate class): at u/k14/`0x642fdfb`, L2, cut1, gap222,
   the belief has E=84, O=50, S=34. A negative endpoint `0x190825b` has
   no opposite-sign single-bit neighbor. Hence no sign-reversing
   single-bit involution can leave a nonempty fixed set of one sign.
   Arbitrary nonlocal pairings and structured mixed-sign remainders remain open.
4. `proofs/informal/problem1_signed_slice_orthant_test.md` (`refuted`):
   the same occurrence's stripped ancestor u/k13/`0x190bf7e`, L1 has
   V=(60,0,72,-9,34). Thus even a union of the positive and negative
   orthants does not cover the admissible ancestor domain.
5. `proofs/informal/problem1_signed_mass_valuation_gate.md` (historical
   finite candidate, now `refuted` on both stated all-depth domains): write N=E+O and S=E-O=N-2O. The condition
   `v2(N)!=v2(2O)` with v2(0)=infinity would certify S!=0. It survives
   all 19 existing full-domain occurrences, their 25 ancestors, and the
   two named k18 nodes; this is FINITE evidence, not a preserved invariant.
   Independent row comparison also resolves the old 19-row consistency
   question: primary and independent keys, masses, and counts agree exactly.
6. `proofs/informal/problem1_three_return_reduction_dependency_review.md`
   records independent proof checks and the corrected direction of the
   reduction. Do not read the older pathway arrows as logical implications
   from nonvanishing backward to its sufficient hypotheses.

Updated priorities: seek a replacement nonvanishing mechanism using exact
endpoint correlations over returns; or exploit the physical-row membership
lemma to prove a finite cut bound, possibly only on a rigorously identified
physical subfamily. The particular valuation candidate is refuted above. The phase-frontier membership lemma is not a surjectivity
theorem: generic frontier counterexamples need not be realized by a coupled
finite-seed trajectory. No larger census is authorized by finite absence.
All new checks are local, bounded, and recorded atomically with source hashes.

The previously requested GitHub push is now externally verified: origin's
`research/astra-next` reached `b86a0ea892549287d4431fce69d29a743855bf9b`.
The user subsequently authorized publishing this continuation on the same
research branch. The latest commit IDs are recorded in Git history.

## Earlier continuation (2026-09-05, on `research/astra-next`)

Read these new notes before the older frontier list below:

1. `proofs/informal/problem1_signed_slice_joint_transfer.md`: exact all-depth
   joint-fiber transfer identity (`partial-proof`) and a verified universal
   five-vector closure counterexample (`refuted`). At phase p, parent k=6,
   L=1, states `0xc82` and `0xc88` have identical vectors `(2,0,0,0,1)`;
   the same two digits `00` and masks `1011,1011` give two-lift masses -1
   and +1. Even outgoing-current-mask information does not repair this
   universal quotient. This is NOT a restricted three-return-domain no-go.
2. `proofs/informal/problem1_signed_slice_convex_obstruction.md`: a new
   connected-region obstruction (`partial-proof`). The known vectors
   `(262,0,200,27,117)` and `(3,0,5,0,7)` are now verified to lie in the
   admissible gap-222 ancestor domain. For mask `1011` their child masses
   are -83 and +2. Every connected real region containing both crosses the
   cancellation hyperplane; a convex cone contains its nonzero point
   `2v-+83v+=(773,0,815,54,815)`. Depth/digit/schedule-indexed regions,
   disconnected sets, and arithmetic exclusions remain open.
3. `proofs/informal/problem1_three_return_boundary_review.md`: independent
   Muse review of witness ancestry and proof scope; boundary cut bound still
   `inconclusive`. Top-digit comparison supplies no contradiction.

Muse Spark 1.3 Contributor was available and used for bounded implementation,
counterexample checks, and independent review. Lead review corrected a tensor
digit-membership bug and checked quantifiers before integration. New atomic
records are `results/problem1/20260905_signed_slice_{transfer_check,convex_obstruction}.json`
and `20260905_boundary_convex_ancestry_replay.json` in that directory.
No larger nonvanishing census was run. The universal transfer audit uses
parents k<=9; the restricted-domain audit retains k<=16 and has only eight
ancestor transitions. The cone check replays two existing complexity-18
vectors and at most three added low digits, establishing one explicit k=19
descendant without a frontier census at k=19.

The current best next target is a return-context partition or an arithmetic
restriction that controls the exact joint endpoint correlations and excludes
zero; a sign-reversing endpoint pairing with a nonzero remainder is another
candidate. Do not assume the five-vector is closed, or that one connected
hyperplane-avoiding region covers all admissible ancestors. No invariant of
either surviving kind has yet been established. The original all-depth
nonvanishing and boundary obligations below remain the strongest bottleneck.

The pre-existing untracked `proofs/informal/problem1_signed_slice_transfer_audit.md`
was read and preserved; its claim that Muse is unavailable is stale. Existing
untracked full-domain result files and `.worktrees/` were also preserved.

## The three prize problems (`docs/problem_statements.md`)

Rule 30: `x_j(t+1) = x_{j-1}(t) XOR (x_j(t) OR x_{j+1}(t))`, single-cell seed (`x_0(0)=1`), center `c_t = x_0(t)`, `c_0 = 1`.

1. **Problem 1 (priority):** is `(c_t)` eventually periodic? Expected answer no. Only eventual period one is excluded.
2. **Problem 2:** does `(1/N) sum_{t<N} c_t -> 1/2`? Campaigns paused.
3. **Problem 3:** exact complexity of computing `c_n` (model/encoding/output/uniformity must be fixed per claim). Campaigns paused.

## Priority and critical path (`AGENTS.md`, `docs/problem1_focus_program.md`)

Problem 1 only. Target implication: if a proposed center trace `C` with `c_0=1` is eventually periodic, its left-permutive reconstruction `L(C)` (right half forced zero) is not eventually zero. Frozen: larger prefix stats, first-witness boxes (= prefix comparisons only), Problems 2/3 sweeps, benchmarks, ports, broad Lean work.

## Established exact / all-depth results (all `partial-proof` or conditional; Problem 1 still open)

- Period-one exclusion for every finite seed (all-one tail forces left column zero; all-zero tail forces right neighbor eventually constant; contradicts width-two theorem). Lean covers local steps only; external width-two theorem not formalized.
- Whole-tail equivalence: eventually-zero reconstructed tail iff finite-support initial config with rightmost one at 0; its center is the growing diagonal `bit_t(T^t(S))`, `T(S) = S XOR ((S<<1) OR (S<<2))`, `S` odd. Fixed bit `k` has period dividing `2^k` (no diagonal control).
- `Delta` is a unit-triangular isometric 2-adic bijection; eventual periodicity iff rational output. Cycle `T(-1/3)=1/3`, `T(1/3)=-1/3` maps to period-one traces: fixed-coordinate periods alone can never contradict.
- Inverse-lift even/odd section recurrences exact; `Delta circ T^j` sections pairwise distinct, so universal finite-state routes for `Delta`/`Delta^-1` are closed.
- Prefix equivalence: first nonzero reconstructed-left depth = first center-prefix disagreement (checked horizons 0-16). Larger first-witness searches add nothing.
- Adjacent-shadow reduction (exact, sufficient but stronger than necessary): three-return zero-penalty plateau implies `T_{a,k} NOT SUBSET P_{a,k-1}`. All-depth inclusion `T_{a,k} \subseteq P_{a,k-1}` would prove every three returns carry positive phase penalty.
- Separation lemma (`partial-proof`, conditional on projection theorem): `x in O_(a,k)`, `y in O_(a,k-1)` implies `x != y (mod 4^(k-1))`; no adjacent shadow at any `L >= k-1`.
- Signed-slice lift (exact): `S(N) = sum_n epsilon_m(n) V_n(parent(N))` (proof: `proofs/informal/problem1_period_two_signed_slice_recursion.md` on sibling branch, see below). Scalar parent mass/sign provably insufficient (e.g. mass 1650 -> children 104 vs 605; positive parents -> children -83 vs +2).
- Derivative identity `S = sum_y prod epsilon` is a restated definition: zero nonvanishing content alone. `S != 0` implies nonempty belief (immediate, exact); converse false.

## Finite-only evidence (explicitly not proofs)

- Full-domain sweep k<=16, both phases, 56 gap triples: 19 occurrences / 17 cylinders, zero signed-mass zeros, min |mass| 6 (`u`, k=15, `0x1bd9c36b`, cut 2, `(2,2,2)`, +6 over 54 endpoints). Outcome B. Records: `results/problem1/20260905_three_return_signed_mass*.json`.
- Gap-`222` census thru k=28 (C++): 5,162 cylinders, 0 zeros, 59 negatives, min |mass| 1 (`0x1bcd3a7b3fdfb`, k=25). Slice-ancestor census thru k=28: 7,363 cylinders, 0 zeros.
- Adjacent-shadow census k<=20: 210 occurrences, 0 violations. Older boxes (sideways horizons, conservation widths 1-5, 5,898 DFAOs, recurrences, 2-adic/quotient campaigns) exhaustive only in stated boxes.

## Failed approaches / no-go results (do not retry without a new mechanism)

- Signed nonvanishing is NOT universal: `u`, k=5, `0x198`, depth 1 has costs {0:1, 1:1}, mass 0. Bounds the conjecture to the three-return admissible domain.
- Scalar and sign-only induction dead (counterexamples above); additive single-letter cocycles trivial; quadratic GF(2) range-3 forces constant terminal potential; six-state shadow-mask closure fails; signature simulation too coarse; budget-language/affine no-go; endpoint profiles do not lift paths.
- Period-two quotient mirages, all exact counterexamples: seven-block driver fails block 153; head+depth-2 portraits collide (blocks 11 vs 55) with different successors; endpoint law `s_(2^k-1) = k mod 2` fails at k=11.
- Mask-only or fixed-modular endpoint quotients refuted (realization-splicing); majority/density false (292 cylinders keep < half); positivity false (59 negatives).

## Strongest Problem 1 pathway

Eventual period two -> three consecutive returns must carry positive phase penalty -> adjacent inclusion `T \subseteq P` -> concrete dominant belief nonempty -> signed-mass nonvanishing -> five-component slice induction along the forced `t`/`u` schedule.

## Exact unresolved bottleneck

No all-depth proof that signed mass never vanishes on the full three-return domain (both phases, all 56 triples): prove the slice vector never lands in the cancellation hyperplane `sum_n epsilon_m(n) V_n = 0` along any forced schedule. Separately, the separation lemma empties `L >= k-1`, but the conjectured domain `L < k` still contains the lethal `L = k-1` (and `L >= k` matters for the original inclusion): an all-depth proof must also establish `c+1 <= k-2` for every occurrence or treat the boundary. Next census-cap increase is NOT the step; a counting/invariant argument is.

## Five-component signed-slice formulation (latest route, lives on sibling branch)

For parent cylinder, `V_n = sum_{p : M(p)=n} (-1)^{c(p)}` over `n in {0000,0011,1011,1100,1111}`; `S = sum_n V_n`; child mass `S(N) = sum_n epsilon_m(n) V_n(parent)`. Full note + analyzer + tests only on `origin/research/period-two-signed-slice-recursion` (`git show origin/research/period-two-signed-slice-recursion:proofs/informal/problem1_period_two_signed_slice_recursion.md`); NOT merged into this branch. Next target per that note: cone/ordering/parity/boundary invariant on `V` preserved by the return schedule that excludes the hyperplanes.

## Reasoning traps

- Finite absence (any `k` cap, any box) proves nothing at `k+1`; the k=23/25/27 positive-defect exceptions live above the k<=16 full-domain box.
- Quantifiers: conjecture is over every phase/complexity/state/cut/gap-triple; one uncaptured case kills the certificate (not the belief, not Problem 1).
- Endpoint dedup is load-bearing: min instance is +6 distinct vs -548 representation-weighted (sign flip). Final-`u` admissibility convention changes the instance set (19 vs 21). State conventions explicitly before any proof.
- Negative mass is fine; only exact zero on an admissible instance refutes. Do not splice endpoints across cylinders into abstract paths. Do not return to universal finite-state, mask-only, or scalar routes.

## Read first

1. `proofs/informal/problem1_period_two_three_return_signed_mass.md` (conjecture + gate)
2. `proofs/informal/problem1_signed_mass_scope_audit.md` (separation lemma + boundary)
3. `proofs/informal/problem1_three_return_signed_mass_independent_review.md` (Outcome B, seam audit, fixes)
4. `proofs/informal/problem1_period_two_three_return_adjacent_shadows.md` (reduction + census)
5. `proofs/informal/problem1_period_two_signed_belief_derivative.md` (derivative = definition; k<=28 census; `0x198`)
6. Sibling: `origin/research/period-two-signed-slice-recursion` note/analyzer/tests (five-component route)
7. `docs/problem1_focus_program.md` (admission/stopping; status 2026-07-22, predates frontier)
8. `AGENTS.md` (non-negotiables; never edit `src/python/rule30_research_reference.py`)

## Branch / PR status

- `main` = `b54f067` (merge PR #48, 2026-08-02). No open-PR check possible offline (`gh` absent); PRs #46-48 merged in history.
- Newest work is LOCAL-ONLY: `research/three-return-signed-mass-full-domain` (`a9af399`, 2026-09-04), one commit over `main`, never pushed. This branch `research/astra-next` = that commit + this file.
- Newest REMOTE work: `origin/research/period-two-signed-slice-recursion` (`c79b67a`, 2026-08-02), sibling off `main`, unmerged; its files are absent from this checkout (available via `git show origin/...`). Fetch 2026-09-04 confirmed up to date.
- 4 sister worktrees at `b54f067` (`.worktrees/`, untracked): `signed-full-domain-pass/-review`, `three-return-signed-cancellation/-check`. Note: `tests/python/test_period_two_three_return_signed_mass.py` hardcodes branch `research/signed-full-domain-pass`, so it fails elsewhere by construction (see baseline).

## Highest-value next questions

1. What invariant on the five-component slice vector (cone, ordering, parity, boundary) is preserved by the forced `t`/`u` schedule and excludes `sum_n epsilon_m(n) V_n = 0` on all 56 gap triples?
2. How to prove `c+1 <= k-2` for every three-return occurrence (or separately discharge `L = k-1` and `L >= k`), given the separation lemma?
3. Do the 19 per-occurrence rows of the primary analyzer match the independent replay row-for-row (canonical row hashes), not just in totals?
4. What explains the `(2,2,2)` family (min-mass instance, all known positive-defect exceptions) -- the likely first refutation or first lemma?
5. How to unify the sibling slice line (gap-`222` thru k=28) with the full-domain line (all triples thru k=16) without raising any cap?
