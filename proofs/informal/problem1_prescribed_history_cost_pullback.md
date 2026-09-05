# Pulling history costs through prescribed forced updates

Status: `partial-proof` for the exact fixed-age cost and language identities;
`finite-exhaustive` for the declared certificates; `refuted` for W* descent
on all once-prescribed admissible three-return blocks. Problem 1 remains open.
Base checkpoint: `3fb18567ecd16ee71b8a338248b48ee9f34d4ac6`.

## Bottleneck, route ranking and admission

The preceding zero-cost language note refutes universal W* descent on
ordinary histories. Its zero words are outside every positive-time
prescribed image, so that result leaves the prescribed-history restriction
open. The exact bottleneck tested here is:

For every original ordinary history v in phase a, with endpoint z and an
admissible forced prefix Q0 ututut, must W* strictly decrease over the six
steps starting from the actual prescribed history H(v)Q0?

This is a necessary test for universal descent on prescribed histories;
it is weaker than the remaining near-boundary synchronized restriction.
Initial complexity k belongs to v, and the tested cut is c=1.

Ranked routes (`heuristic`):

1. Pull the nonnegative cost back through one prescribed update and use
   the exact fixed-block graph. High falsifiability and computational
   testability, low cost; the reduction itself can hold at every word
   length. An accepting zero-cost path refutes the restriction, while
   full nonreachability proves positive starting cost on this language.
2. Pull back the complete signed block change. More expressive, moderate
   cost, but unnecessary to test strict descent if route1 finds zero.
3. Couple elapsed age to initial length in the synchronized family.
   Highest direct relevance to the occurrence boundary, but no finite
   state reduction or promising invariant is established; higher cost.

Choose route1. Fixed residue precision65536 follows from seven observed
gates, not from a frontier complexity cutoff. Admit both phase roots,
the motif ututut, a single preceding actual forced update, and full
prefix admissibility including the UNOBSERVED final u. Independent
forward and reverse graph methods test shortest zero-cost predecessors.
Small word checks cover nonroot lengths0..5 and scanner ages1..3; actual
witness replays verify seven forced updates. Each local run is bounded
by120seconds and1GiB and writes atomic JSON with full provenance.

## Definitions

Use the exact conventions of `problem1_history_synchronization.md`:

    T(x)=x XOR ((x<<1) OR (x<<2)),  U(x)=T(x) XOR1,
    P(x)=T(2x+1)>>1,  A(x)=T(x)>>2,
    S_0=t, S_1=u, S_2=S_3=p.

Roots are rho_p=3 and rho_u=1. The ordinary word v=g1...gn excludes
the fixed root; its prefix endpoints are z0=rho, zi=G_gi(z_(i-1)).
All ordinary words are permitted, including words whose GENERATOR
letters contain factors forbidden for FORCED schedules.

At a permitted endpoint z, Q(z)=u for z=7 mod16 and t for z=11 mod16.
Then F(z)=Q(z)(P(z>>2))=Q(z)(A(z)), and the exact history update is
v -> H(v)Q(z). The scanner's ith prefix evaluates to A(zi).
Admissible forced schedules avoid uu, ttttt and ututtu.

Let W_omega be the sum of fixed nonnegative edge weights
omega(old prefix mod2^b,g), excluding the root, with b>=2.
The candidate W* uses b=4 and weights1 precisely at (0,t),(1,u).

## Exact fixed-age pullback (`partial-proof`)

Fix integers s>=1 and r>=1. Suppose z=z_n has s defined forced steps,
with x_t=F^t(z), x_0=z, and branch Q_(t-1) at x_(t-1).
Let v_s be the history produced by those s prescribed updates.
For an original edge with old prefix q and generator g, define

    lambda_s(q,g)=omega(A^s(q) mod2^b,
                         S_(A^(s-1)(G_g(q)) mod4)).             (1)

For a letter born at update t, 1<=t<=s, put

    ell_(s,t)=Q_(t-1)                         if t=s,
    ell_(s,t)=S_(A^(s-t-1)(x_t) mod4)          if t<s.

Define the nonnegative terminal contribution

    beta_s(z)=sum_(t=1..s)
       omega(A^(s-t+1)(x_(t-1)) mod2^b, ell_(s,t)).             (2)

Then at EVERY finite original history length n,

    W_omega(v_s)=sum_(i=1..n)lambda_s(z_(i-1),g_i)+beta_s(z).  (3)

Proof. The synchronization identities give A^s(z_(i-1)) as the old
prefix of the ith original letter after s updates, and give its letter
as S_(A^(s-1)(zi) mod4). These are exactly the summands in (1).
At final time s, the prefix immediately before birth-position n+t is
A^(s-t+1)(x_(t-1)). For t=1 it is the transformed original endpoint;
for t>1 it is the later image of the preceding birth prefix x_(t-1).
The birth-letter formula gives ell_(s,t), proving (2) and (3).
Empty original words n=0 cause no exception.

The local map A loses at most two bits of congruence precision. Thus
lambda_s depends only on q modulo2^(b+2s): its first argument uses
b+2s bits; its S-index uses at most2s bits, because G preserves
congruence. This is sufficient precision, not a claim of minimality.

## Exact fixed-age language (`partial-proof`)

Fix a verified r-branch motif sigma whose input cylinder is a modulo
2^(2r+2), as proved in `problem1_zero_cost_return_language.md`. Put

    m=2s+max(b,2r+2).

On residues modulo2^m, retain the ordinary generator edge q -> G_g(q)
exactly when lambda_s(q,g)=0. Start at the appropriate phase root.
Accept a terminal residue q precisely when:

1. Its first s forced steps exist.
2. F^s(q)=a modulo2^(2r+2).
3. beta_s(q)=0.
4. Any specified filter on those s branch letters followed by sigma
   and an unobserved final letter is satisfied.

These conditions are well-defined on residues. First, m>=2(s+r)+2
supplies all s+r gate tests. After s steps it supplies the motif's
2r+2 bits. For the first argument of every term of beta_s, the losses
from F^(t-1) and A^(s-t+1) total at most2s. The nonfinal birth-letter
index likewise needs at most2s original bits. The final Q is determined
by the already checked gates. Hence m>=b+2s suffices for the costs.

Accepted paths are EXACTLY original ordinary words whose prescribed
age-s histories have zero cost and admit the specified motif/filter.
Indeed every path lifts to its one concrete generator word from the
root; (3) and nonnegativity make zero total equivalent to zero on every
edge and beta_s=0. The terminal tests give precisely the required
actual gates and filter. Conversely such a word projects to an accepted
path. No endpoint splicing or word-count interpretation of signed mass
enters this argument.

The theorem quantifies over all finite n for EACH fixed s,r,b. It does
not provide one fixed graph for ages s growing with initial complexity.
It neither forgets the original endpoint nor canonicalizes other
representations of a later endpoint.

## Specialization to W* and one preceding update

Claim status: `partial-proof`. Every permitted append has W* cost0.
If z=7 mod16, A(z)=2 mod4, and Q=u would require an old prefix1 mod16
to pay. If z=11 mod16, A(z)=1 mod4, and Q=t would require0 mod16.
Both are impossible. Thus beta_1=0 on the entire permitted domain.

The pulled-back edge cost is omega(A(q) mod16,S_(G_g(q) mod4)), of
residue memory6. Its six nonzero edge types modulo64 are

    (0,t), (58,p), (59,t), (60,u), (63,u), (63,p).

This finite table is independently checked, not inferred from larger
histories. With s=1, r=6, sigma=ututut, the exact graph has65536
vertices and190464 allowed edges.

There are two raw terminal classes for an actual preceding gate and
the following motif:9879 (Q0=u) and65019 (Q0=t). The first gives
observed prefix uututut; appending the UNOBSERVED u leaves forbidden
factor uu. It is rejected for a genuine cut1 occurrence. The only
accepted terminal class is65019, with observed prefix tututut and
admissibility word tutututu. This is seven observed gates; the eighth
letter is not executed. The earlier unfiltered acceptance test was too
weak for the original occurrence domain and was corrected before proof
adoption. No graph size or frontier cap was increased.

## Once-prescribed counterexamples

Claim status: `finite-exhaustive` for the certificates, `refuted` for
strict descent and even nonincrease on all such prescribed blocks.

| Phase | ORIGINAL k | Original word FROM ZERO | Original endpoint z | W* at times1 and7 |
| --- | --- | --- | --- | --- |
| p | 19 | pttutututpttututtuu | 0x32173ffdfb | 0,2 |
| u | 16 | utttttuttttputut | 0x6f34fdfb | 0,1 |

Both have exactly the checked observed prefix tututut, so these are
genuine cut1, gap222 occurrences from original ordinary histories.
Their time1 endpoints are0xc8e7900387 and0x1bd9c4387 respectively.
Their time1 histories are the actual H(v)t, with no reselection.
The six-step comparisons use times1 and7, not the predecessor's cost.
Nonnegativity and initial zero alone refute strict descent; the positive
final values also refute nonincrease. These examples do not refute
signed nonvanishing or an occurrence-cut bound.

Reverse distances from65019 reach all65536 vertices. For each allowed
edge q->y, d(q)<=1+d(y); every q!=65019 has an edge with d(y)=d(q)-1,
and only65019 has distance0. Thus the stored distances certify exact
shortest paths. The root distances18 in p and15 in u minimize original
nonroot word length in this specific zero-cost language. They are not
minimum integer counterexamples, not minimal among all costs, and not
a claim of physical finite-seed realization.

The original complexities put c=1 well before the near-boundary cuts
c=k-4. No assertion that these histories are already synchronized follows.
The earlier grammar obstruction is therefore resolved only for the
once-prescribed class; elapsed-time/initial-length restrictions remain.

## Independent checks and next obligation

Muse independently derived the fixed-age pullback, the precision bound
and zero append cost. Fresh adversarial mathematical review accepted
the formulas, including the birth-prefix indices and fixed-age scope.
Separate forward and reverse implementations agree on both witnesses.
The complete verifier checks73,365 forward nodes and167,670 attempted
edges, as well as the reverse certificate on all190,464 allowed edges.
It verifies the exact retained original records, source/raw/input hashes,
and reused phase-u transcript. That reuse is valid because the original
u search found65019 without ever discovering the rejected class9879.

The independent cell implementation checks728
small words at ages1..3, all65536 residue gate tests, and every edge of
the fixed graph. Actual witness replays check16 states,14 forced updates,
287 reconstructed formula letters and14 complete48-edge decompositions.
Those finite checks support the proof review; they do not replace it.

Records in `results/problem1/`:

- `20260905_once_prescribed_zero_primary.json`: the complete filtered
  forward certificates, with original records and the complete earlier
  unfiltered prerequisite retained for exact reuse provenance. Its rejected
  phase-p witness is not used as a genuine occurrence.
- `20260905_once_prescribed_zero_independent.json`: independent cell-rule
  reverse graph, full distance certificate and actual word/formula replays.
- `20260905_once_prescribed_zero_verification.json`: portable comparison
  of complete certificates, hashes and scope-critical acceptance fields.

The verifier reads only committed records and supports
RULE30_REPLAY_ROOT and RULE30_REPLAY_OUTPUT. The original implementation
sources and all reused raw inputs are embedded in the primary record.
Final read-only review accepted all five checkpoint files, including
finite comparisons, reuse provenance and hash linkage, with no remaining
corrections. All runs finished within their local limits; the immutable reference
hash is unchanged. No frontier census, other motif or higher-age graph
was generated.

Next (`inconclusive`): seek a structural constraint tying prescribed age
to INITIAL word length, or a new potential with a justified invariant.
Do not automatically increase the tested age: the general theorem's
residue width grows with age, and another fixed-age counterexample
does not resolve the critical diagonal relation c>=k-4. The surviving
near-boundary occurrence exclusion, B_all, signed nonvanishing and the
whole-tail question remain open.
