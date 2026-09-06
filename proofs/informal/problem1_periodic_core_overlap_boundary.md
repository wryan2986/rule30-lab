# Periodic-core overlap separates adjacent frontier cylinders

Status: `partial-proof` for the all-depth overlap and decoding statements;
`refuted` for the forced five-position cost extension; finite checks are
separately scoped below. Problem 1 remains open.
Base checkpoint: `ec3ff5cdbde8e0e30d0ad17bf66e6db9bb88b528`.

## Bottleneck and route selection

The critical-cost identity expresses prescribed history cost by an exact
boundary sum. Nonnegativity of its local summand J gives no useful upper
bound: J can equal2. An upper bound Psi_s<=alpha*s+K with constants
alpha<1 and K independent of age and schedule would contradict the
established lower bound
Psi_s>=max(s-n-1,0) for a fixed finite ordinary initial history surviving
indefinitely. This implication is `partial-proof`; the proposed upper
bound is `inconclusive`. No density theorem has been established.

Three routes, ranked (`heuristic`):

1. Test whether forced continuation removes the first charged position
   omitted from the endpoint diagonal. Highly falsifiable at low cost;
   an all-depth extension would sharpen cost control near initial length.
2. Use the already established periodic leading blocks and their low-bit
   overlaps to constrain entire ordinary endpoints and adjacent shadows.
   High all-depth plausibility and low cost. It can strengthen necessary
   boundary conditions, but does not itself exclude a genuine occurrence.
3. Prove a density or return inequality for J with ordinary membership
   retained. Most direct potential relevance, but high cost without a
   mechanism; scalar nonnegativity alone is insufficient.

Route1 fails at age2, as shown below. Move to route2 using only existing
ordinary frontiers and cores through level8. A false overlap table would
refute the proposed boundary improvement; a correct finite table combines
with the all-depth leading-block theorem to prove it. No larger frontier,
periodic-core, branch-word, or occurrence census is admitted.

## Definitions and exact overlap lemmas

Use the definitions in `problem1_frontier_head_dynamics.md` and
`problem1_cyclic_seed_boundary.md`. The ordinary frontier O_(a,k) has
phase a in {p,u} and initial complexity k. Put pi(x)=x>>2 and
A(x)=T(x)>>2. Let C_(a,h) be the periodic core of A on O_(a,h), and
let tau_(a,h) be its stabilization age. The established identity is

    pi^(k-h)(O_(a,k))=A^(k-h)(O_(a,h)).                 (1)

Thus the left side equals C_(a,h) when k-h>=tau_(a,h).
All sets consist of distinct endpoints, not histories.

### Adjacent separation (`partial-proof`, all-depth)

Fix a phase, h>=2, b>=0 and

    d=k-h>=max(tau_(a,h),tau_(a,h-1)).

Suppose the residues of C_(a,h) and C_(a,h-1) modulo2^b are disjoint.
Then no x in O_(a,k) and y in O_(a,k-1) satisfy

    x=y modulo2^(2d+b).                               (2)

Proof. Apply (1) at the SAME projection depth d to both integers.
Their projected values lie in C_(a,h) and C_(a,h-1), respectively.
Congruence in (2) would make these values equal modulo2^b, contradicting
the disjointness hypothesis. The age of the lower frontier is d too,
not d-1.

Consequently raw adjacent shadows are empty at every base-four depth

    L>=k-h+ceil(b/2).                                  (3)

Dominant beliefs, being subsets of those raw shadows, are empty there,
and their signed mass is0. This conclusion does not need any mask or
sign calculation and holds for every ordinary cylinder in the stated
domain. A genuine return is an additional condition, not a premise
proved or disproved by (3).

### Endpoint decoding (`partial-proof`, all-depth)

Fix a phase and h, and suppose reduction modulo2^b is injective on
C_(a,h). If d=k-h>=tau_(a,h), reduction modulo2^(2d+b) is injective
on O_(a,k).

Proof. Two ordinary endpoints with the same low2d+b bits have projected
heads in C_(a,h) with the same low b bits. Injectivity identifies their
entire heads. Their low2d bits already agree, identifying the endpoints.

The branch-cylinder theorem then implies that phase, initial k and the
first r OBSERVED forced branches determine at most one ordinary endpoint
whenever

    r>=1,       2r+2>=2(k-h)+b.                        (4)

There is an explicit candidate decoder. From the branch residue q select
the unique H in C_(a,h), if any, with

    H=q>>2d modulo2^b,

and set x=4^d H+(q mod4^d). If no H exists, no ordinary endpoint realizes
the word. If H exists, the constructed integer still requires full
ordinary membership and agreement with every observed branch bit. The
overlap condition alone is not sufficient for either. In particular,
extra bits supplied when 2r+2>2d+b must also agree.

This determines endpoints, not the individual original histories of an
endpoint. It is distinct from prescribed-history synchronization. Nor
does it provide a fixed finite-state system for arbitrarily long branch
words: the decoded lower part still grows with k.

## Concrete all-depth consequences from existing cores

The following are established finite core sets; stabilization ages are
the finite equalities already certified in the head-dynamics records.

| Phase, level | Core | Stabilization age |
| --- | --- | --- |
| p,6 | 3205,3214,3558,3564 | 8 |
| p,7 | 12823,12857,14234,14259 | 9 |
| p,8 | 51292,51431,56937,57038 | 11 |
| u,7 | 6411,6428,7117,7129 | 8 |
| u,8 | 25646,25715,28468,28519 | 10 |

For phase p, the level7 and6 residues modulo16 are respectively
{3,7,9,10} and {5,6,12,14}. For phase u, the level8 and7 residues
modulo16 are {3,4,7,14} and {9,11,12,13}. Both pairs are disjoint.
For the p pair, modulo8 already suffices; rounding either3 or4 overlap
bits to a whole base-four depth gives the same threshold below.
Equation (3) therefore proves:

    p, k>=16: raw adjacent shadows are empty for L>=k-5;
    u, k>=18: raw adjacent shadows are empty for L>=k-6. (5)

These are statements at EVERY later k, not extrapolations of an
occurrence census. They sharpen the prior dominant-only empty threshold
L>=k-3 in their respective domains and apply already to raw shadows.

In the four listed p,level8 core states, residues modulo4 are 0,3,1,2,
all different. For u,level8 the residues modulo8 are 6,3,4,7, also all
different. Equation (4) proves endpoint uniqueness from observed words:

    p, k>=19: r>=k-8 suffices;
    u, k>=18: r>=k-7 suffices.                          (6)

The finite audit also computes the least sufficient overlap widths for
the other already stored levels2..8. Least width here refers ONLY to
the displayed finite core-residue tests. It does not prove optimality of
the resulting whole-frontier or branch-length thresholds; lower-bit
constraints elsewhere in the frontier might strengthen them.

## The forced five-position extension fails at age2

The tested claim was: for n=s+5, if an ordinary initial endpoint has
s+1 OBSERVED admissible forced branches, its fifth original cost at
scanner age s is0. Admissibility forbids uu, ttttt and ututtu.

At s=1 this implication does hold (`partial-proof`, bounded time and all
inputs). Write v5 for the fifth nonroot prefix. A positive fifth cost
means v5=0 or5 modulo64. Since one original letter remains, the endpoint
is G(v5) for G in {T,U,P}. Its possible residues modulo64 are exactly
{0,1,3,26,27}. None has two defined forced steps: residues other than27
fail the first gate, and residue27 has first branch t but its forced
successor is15 modulo16. This proof uses no original-length census.

At s=2, the rooted phase-p word

    ptpptput

has nonroot length7, endpoint56939 and observed branches ttu, which are
admissible. Its fifth original position has cost1 after two scanner
passes. Its exact prefix endpoints are

    3,13,50,221,803,3564,12821,56939,

and A(3564)=3205=5 modulo64. Its forced states through the three
observed branches are56939,228155,910999,3650439. The second scanner
image, with the fixed root included, is ptptpupu and has cost vector
(0,0,0,0,1,0,0). Thus C_2=1,D_2=0 and C_2-D_2=1.
Thus the extension of C_s=D_s-max(s-n-1,0) to n<=s+5 fails even with
the required extra actual branch. This is a short ordinary forced
prefix, not a genuine three-return occurrence; no stronger return-
conditioned extension is refuted by this example.

The finite falsification scans all1,458 words at n6 and all4,374 words
at n7, both phases. There are no eligible counters at age1, and38 at
age2 (10 phase p,28 phase u), all with ttu. It stops there, before the
admitted age3. The displayed p witness is first in the declared order
(age, phase p before u, endpoint, word with tie order p<t<u); no global endpoint minimality
over arbitrary lengths is asserted.

## Verification and remaining obligation

Claim status: `finite-exhaustive`. Muse replays stabilization from the
16 stored initial frontier sets and computes28 overlap entries. The
independent cell/odd-section implementation regenerates those16 ordinary
frontiers, verifies91 image-set steps, and agrees on every overlap entry.
It also independently scans all5,832 words at the two completed lengths,
using actual H iterates for costs, and matches the full38-counter list,
the age1 histogram and the named witness's states and cost gap.

Records are `results/problem1/20260905_core_overlap_primary.json` and
`results/problem1/20260905_core_overlap_independent.json`. The primary
wrapper preserves each original JSON payload byte-for-byte, its executed
source and run timing; the wrapper's own timing is packaging only.
The portable independent source verifies payload, source, summary and
input hashes. It regenerates no ordinary frontier above level8.
No all-k occurrence census is used to verify (5) or (6).

An independent tool-free derivation and a fresh adversarial mathematical
review accepted the overlap arguments, counterexample and their scope
distinctions. Final four-file integration review accepted the numerical
comparisons, ordering and provenance without material corrections.

For a proof requiring nonzero signed mass on every genuine occurrence,
(5) imposes the necessary bounds c<=k-7 in phase p for k>=16, and
c<=k-8 in phase u for k>=18, since L=c+1. Actual occurrence exclusion
at those cuts remains open. The old B_all obligation L<=k-2 keeps its
original meaning; (5) is not a proof of B_all.

In particular, the cost-formula layer c=k-5 already has an empty raw
shadow for both phases at sufficiently large k. A potential on that
layer would need to exclude the actual return; it cannot make its
empty signed belief nonzero.

Next (`inconclusive`): combine the explicit endpoint decoder with a
structural constraint on the observed return word and full ordinary
membership. Do not replace the latter with mere membership of its
leading core. Alternatively a justified boundary-sum inequality could
exclude occurrences. Neither an inequality nor decoded-candidate
exclusion is established here; Problem 1 remains open.
