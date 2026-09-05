# Aged cyclic seeds and the dominant-shadow boundary

Status: `partial-proof` for the all-depth seed bound, monotonicity and empty
layers below, independently reviewed. Status: `finite-exhaustive` for the
specified 3,391-cylinder check. No occurrence bound or Problem 1 theorem is
claimed; these remain `inconclusive`.
Base checkpoint: `53ce1f745fb77acffb6fabfb055f1b4456ba2fa3`.

## Bottleneck, route selection and admission

The whole-tail target remains whether an eventually periodic center trace
with c_0=1 can reconstruct an eventually zero initial left half. The active
adjacent-shadow route has an unresolved occurrence boundary: every genuine
admissible three-return occurrence must have L=c+1<=k-2, with k the INITIAL
ordinary-frontier complexity. This is the existing B_all obligation. It is
not implied by a signed-mass calculation on a finite collection of returns.

The new head theorem in `problem1_frontier_head_dynamics.md` gives an exact
age-dependent restriction on a shadow seed. Three possible uses, ranked:

1. Compare the highest masks at residual seed levels s=1,2. Plausibility and
   all-depth potential are high for a necessary boundary lemma: finite base
   masks plus exact head marginals suffice. Falsifiability and testability
   are high; cost is low. This cannot itself prove an occurrence exclusion.
2. Couple the growing generator-history scanner to the forced return word.
   This could resolve the occurrence bound itself, but plausibility is
   uncertain and cost is higher: automatic head membership supplies no
   exclusion, and a suitable forbidden pattern is not yet specified.
3. Retain signed correlations on the cyclic seeds and seek a nonzero
   functional. Potentially all-depth, but currently lower plausibility and
   higher cost: scalar/sign closure and simple affine defect patterns have
   already failed. A concrete functional would be needed before testing.

Choose route 1 first. The candidates are emptiness at L=k-2 for both
phases k>=3; at L=k-3 for phase p,k>=5; and at L=k-3 for phase u,k>=6.
The justification to test is structural: survival establishes stronger
necessary boundary obligations for the dominant certificate; failure locates
the first incorrect mask/head inference and rules out that sharpening.

Admitted finite test: all ordinary states already stored through k=9,
both phases, L in {k-3,k-2,k-1} with 1<=L<k. Order by k, phase p before u,
integer x, then L. Compare distinct endpoint beliefs, costs and raw shadow
sets with an independent seed-first reconstruction. Check the general
aged-seed cardinality bound when k-1-L>=1. No new frontiers beyond 9,
branch schedules, return occurrences, or period boxes are admitted.
One local CPU per run, 120 seconds and 1 GiB; atomic records with exact
source, base Git, input/source hashes, timing, hardware and software.

## Definitions and structural arguments

Use the exact ordinary frontiers and fiber masks from the head and weighted
recursion notes. T(v)=v XOR((v<<1) OR(v<<2)), U(v)=T(v) XOR1 and
P(v)=T(v) XOR1 XOR(2 if v is even else 0). Starting from
O_(p,1)={3}, O_(u,1)={1}, take the union of their three images to obtain
the next frontier. Endpoints are distinct integers, not generator words.
Write pi(v)=v>>2 and A(v)=T(v)>>2. The established all-depth theorem is

    pi^(k-h)(O_(a,k))=A^(k-h)(O_(a,h)),  1<=h<=k.

A selfmaps each frontier, so these iterated images are nested.
Let M_(a,h)(q)={d in {0,1,2,3}:4q+d in O_(a,h+1)}.
Masks below are integers with bit d representing digit d.

For x in O_(a,k), k>=2 and 1<=L<k, B_a(k,L,x) is the set of y in
O_(a,k-1) having y=x mod4^L and satisfying, for every 0<=j<L,

    M_(a,k-1-j)(x>>2(j+1)) subset
    M_(a,k-2-j)(y>>2(j+1)).

At L=k-1 the same-residue set is already empty by the established raw
adjacent-level separation theorem; no level-zero fiber is evaluated.
The same convention extends B to L>=k-1. On surviving endpoints the cost
is the number of nonfull shadow masks, and S=sum_(y in B)(-1)^cost(y).

### Seed bound

Claim status: `partial-proof` (all-depth).
If 1<=L<=k-2 and s=k-1-L, then

    {y>>2L:y in B_a(k,L,x)} subset A^L(O_(a,s)),
    |B_a(k,L,x)| <= |A^L(O_(a,s))|.

Indeed the head theorem applies to every y in the adjacent frontier, and
y=4^L q+(x mod4^L) uniquely reconstructs y from its seed q. It can fail
frontier membership or dominance, so this is not a sufficient condition.
After the finite image stabilizes, the right side is the number of ALL
A-periodic points at the corresponding width; uniqueness is not assumed.
A singleton bound implies S=+1 or -1 if B is nonempty, but says nothing
about nonemptiness.

At fixed a,k,x, the endpoint sets B_a(k,L,x) decrease with L: the first
L mask tests are identical, and congruence modulo4^(L+1) is stronger.
Costs need not stay fixed. This monotonicity extends an empty threshold
to greater L; raw separation handles all L>=k-1.

### First residual level

Claim status: `partial-proof` (all-depth). For either phase, k>=3,

    B_a(k,k-2,x) is empty for every x in O_(a,k).

Put L=k-2. At the highest tested position j=L-1 the current head is in
A^L(O_(a,2)), and the shadow head is the level-one root. Exact tables:

| Phase | Current head | Current mask M_(a,2) | Shadow head | Shadow mask M_(a,1) |
| --- | --- | --- | --- | --- |
| p | 12 | 12 | 3 | 3 |
| p | 13 | 11 | 3 | 3 |
| u | 6 | 15 | 1 | 12 |

A swaps 12 and13, and maps both6 and7 to6, so these lists cover all L>=1.
Each containment fails. The frontier bases required are
O_(p,3)={50,51,52,53,55} and O_(u,3)={24,25,26,27}.

### Second residual level, phase p

Claim status: `partial-proof` (all-depth). For k>=5,

    B_p(k,k-3,x) is empty for every x in O_(p,k).

Here L=k-3>=2. The current highest head lies in
A^L(O_(p,3))={50,55}, because

    A(50,51,52,53,55)=(55,55,51,50,50).

Both these current heads have full mask15 at level3. The shadow head
lies in A^L(O_(p,2))={12,13}, whose level2 masks are12 and11. A full
mask is contained in neither. The required level4 frontier is
{200,201,202,203,204,205,207,220,221,222,223}.

### Second residual level, phase u

Claim status: `partial-proof` (all-depth). For k>=6,

    B_u(k,k-3,x) is empty for every x in O_(u,k).

Now L=k-3>=3. A shadow seed y>>2L must be6. Use the second-highest
tested position j=L-2, and put H=x>>2(L-1). The head theorem gives

    H in A^(L-1)(O_(u,4)) subset A^2(O_(u,4))={100,110,111}.

The common digit in position L-1 forces
y>>2(L-1)=24+(H mod4). The exact masks are

| H | Current mask M_(u,4)(H) | Shadow head | Shadow mask M_(u,3) |
| --- | --- | --- | --- |
| 100 | 15 | 24 | 0 |
| 110 | 15 | 26 | 11 |
| 111 | 11 | 27 | 12 |

Every containment fails. The zero shadow mask in the first row already
prevents frontier membership; allowing that seed as a candidate is harmless.
The required small set is
O_(u,4)={100,101,102,103,104,105,107,110,111}; its first A image is
{100,101,102,103,110,111}, its second is {100,110,111}.
The current masks use the next frontier, calculated directly as

    O_(u,5)={400,401,402,403,404,405,408,409,411,
             414,415,440,441,442,443,444,445,447}.

For a short arithmetic certificate, the T images of the ordered O_(u,4)
list are (444,443,442,441,408,415,405,402,401). Adjoining U and P images
gives exactly the displayed set. In particular 440=U(103) and
443=T(101). These finite base computations plus the head theorem and the
three mask failures prove the result for every k>=6; the k<=9 check is not
used to extrapolate the conclusion.

## Scope of the consequence

Claim status: `partial-proof` (all-depth). Monotonicity gives emptiness for every
L>=k-3 when p,k>=5 or u,k>=6. Uniformly k>=6, a nonempty dominant
certificate would therefore require L<=k-4. For L=c+1 this is c<=k-5.

This is a statement about dominant beliefs, not all adjacent shadows.
For example p,k=3,L=1,x=52 has raw same-residue shadow y=12; dominance
fails because mask11 is not contained in3. Thus the result does
not strengthen raw separation, prove an occurrence bound, or replace B_all.
It is a stronger necessary obligation for a proof demanding dominant
nonemptiness or signed nonvanishing on every genuine return occurrence.
No ordinary-cylinder exception below is asserted to be a return occurrence.

## Finite exceptions and verification

Claim status: `finite-exhaustive`. Two implementations agree on every one
of the 3,391 admitted cylinders through k=9: 112 raw endpoints occur in
108 cylinders, and 19 dominant endpoints occur in 19 cylinders. Every
surviving belief is a singleton. The complete list of nonempty layers is:

| Phase,k,L | x | Unique y | Cost |
| --- | --- | --- | --- |
| p,4,1 | 204,205,207 | 52,53,55 respectively | 1 |
| u,4,1 | 100,101,102,103 | 24,25,26,27 respectively | 0 |
| u,4,1 | 104,105,107,110,111 | 24,25,27,26,27 respectively | 0 |
| u,5,2 | 404,405 | 100,101 respectively | 0 |
| u,5,2 | 408,409,411,414,415 | 104,105,107,110,111 respectively | 1 |

All other admitted cylinders are empty. The signed mass in a surviving
cylinder is (-1)^cost. These exact finite exceptions refute lowering the
phase-p second-level threshold to k>=4 or the phase-u threshold to k>=5
(`refuted`). The first-level hypothesis k>=3 is simply its minimal
nonvacuous domain, since L=k-2>=1; no preceding exception is asserted.

The worker used stored distinct frontiers and a direct residue-first
endpoint filter, independently checking all 18 frontiers with cell arrays.
The lead independently reconstructed the same frontiers using a cell-array
T and the odd-section P(v)=T(2v+1)>>1, then reconstructed raw candidates
from aged seeds and common low digits. The two records agree on all
endpoint sets/costs, all 364 mask steps on raw pairs, all 26 complete aged
seed-set equalities, 35 base masks and 20 small A-image sets. The seed
cardinality bound passes on all 2,255 cylinders with positive residual.
Primary iteration used (k,phase,L,x), while the independent record and
comparison use (k,phase,x,L); neither found a counterexample, and both
exhausted precisely the admitted domain. No minimal-counterexample claim
depends on the loop-order difference.

Muse Spark 1.3 Contributor independently derived the seed and boundary
arguments. A hand-arithmetic discrepancy in T(101) and T(103) was caught
against the cell calculation and corrected by redoing the binary OR/XOR;
the corrected values above restore the proposed phase-u threshold without
altering its proof. The fresh adversarial reviewer accepted all three
lemmas, the indices, and the dominant-versus-raw scope. That proof review
did not itself certify the finite census; the separate lead comparison
provides its finite cross-check.

The subsequent fresh integration review independently compared all 3,391
rows, 112 raw pairs, 364 mask steps, 26 seed sets, 35 masks and 20 A-images,
confirmed all 19 exception costs, and validated embedded-source, summary,
original payload/raw, operative-input and verification-file hashes. It
approved the final proof/evidence boundaries with no remaining correction.

Records in `results/problem1/`:

- `20260905_cyclic_seed_boundary_primary.json`: original worker record,
  exact executed source and complete raw masks/endpoints, with their hashes.
- `20260905_cyclic_seed_boundary_independent.json`: cell/odd-section
  seed-first implementation, complete admitted rows and small certificates.
- `20260905_cyclic_seed_boundary_verification.json`: full comparison and
  original payload/source/input-hash validation. Its embedded integration
  script records the original worker temporary paths; the independent
  source supports RULE30_REPLAY_ROOT and RULE30_REPLAY_OUTPUT.

All runs used local CPU only, below the stated 120-second/1-GiB caps.
The immutable reference hash was checked unchanged. The original run
records retain their full base Git and provenance; no reference or old
result file was altered.

## Strongest remaining bottleneck

Status: `inconclusive`. It remains unknown whether genuine admissible
three-return occurrences can enter these dominant-empty layers. Finding
such an occurrence at L=k-3 or k-2 would refute the dominant/signed
strengthening without violating B_all's numerical bound. Their exclusion
is necessary for that stronger certificate, and has not been proved here.

Next target: couple the exact forced-return language to the two concrete
high-mask obstructions above using the growing history scanner. A useful
lemma must restrict jointly realizable current/shadow histories or return
cuts; propagating ordinary head membership alone is automatic. Before a
new bounded run, specify a scanner constraint whose truth would exclude
these layers and whose failure would rule out that constraint. Do not
enlarge an occurrence census merely to seek more examples. Signed
nonvanishing in the interior and the original whole-tail question remain
open.
