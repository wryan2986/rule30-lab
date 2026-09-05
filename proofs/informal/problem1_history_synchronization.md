# Representation synchronization of the exact history scanner

Status: `partial-proof` for the exact all-depth synchronization statements;
`finite-exhaustive` for the declared checks; `refuted` for one-pass
universality and the previous single-edge strict-descent candidate.
Base checkpoint: `d399db5af183bfda440857e0ddf1bb51d74d59a7`.
The whole-tail question, occurrence bounds and Problem 1 remain open.

## Bottleneck, route selection and admission

Four-state additive descent potentials bounded below on all histories are
refuted on a genuine three-return block. The same block leaves the
sixteen-state class open. Independently, the current dominant-boundary
argument has no proof that actual returns avoid the empty layers. A
representation-dependent potential can choose histories, so understanding
how much representation freedom survives the prescribed update matters.

Ranked routes (`heuristic`):

1. Exact synchronization from pi G=A and the periodic head cores. High
   all-depth potential and low proof cost; highly falsifiable on existing
   history words. It may remove representation ambiguity at critical cuts,
   but cannot itself exclude a return.
2. Sixteen-state additive descent constraints on named return blocks.
   Direct potential relevance, uncertain plausibility, and low initial
   cost. A finite feasible potential would still require a universal proof.
3. More state memory or nonlinear history potentials. Plausibility unknown;
   higher cost until a concrete functional or obstruction is specified.

Start route2's immediate probe on the already certified u18 occurrence
0x6473d46ab, cut4, prefix tttt, gaps222. Its from-zero history is
uutuuttuupupuuupup. Verify its ten observed branches ttttututut and compare
the two histories at times4 and10. Test the prior candidate counting T
edges entered at prefix residue0 modulo16, and retain all48 edge deltas.
Reuse the committed u14 comparison. Do not enumerate other starting
states, alternate representations or longer schedules for this probe.
For the same ten-step orbit, also verify the complete history reconstructed
by the initial-prefix and appended-letter formulas below; this adds no
states or transitions. After both count tables are available, exact sums
of their already recorded entries may supply a common finite weight vector.

Prioritize route1's new structural candidate before any LP expansion.
Admit all ordinary words of lengths n=k-1, k1..9, both phases, using the
same frontier cap9 already recorded. Check scanner iterates r=0..n,
grouping words by their original endpoint. Test the exact endpoint suffix
formula below and the proposed full-coalescence bounds. Retain per-endpoint
representation counts and first coalescence ages. As a sharper falsifiable
diagnostic, seek the smallest endpoint (k, phase p first, integer x) whose
representations do NOT coalesce after one scanner pass, retaining a pair
of words if one exists. No pairwise quadratic search is needed.

If a synchronization identity fails, its exact counterexample kills that
argument. If it survives, attempt the structural proof using projection;
the finite passage alone proves no all-depth bound. The u18 outcome either
refutes the specific sixteen-state count or adds a finite constraint for
that class, without enlarging an occurrence census. Local CPU only,
120seconds and1GiB per independent run; atomic JSON with full Git,
exact source/input hashes, timings and hardware/software provenance.

## Definitions and exact suffix identity

Use `problem1_frontier_head_dynamics.md`: roots rho=3 for phase p and1
for phase u; ordinary generators T,U,P; A(v)=T(v)>>2; pi(v)=v>>2;
and S_0=T,S_1=U,S_2=S_3=P, where the subscript is reduced modulo4.
The exact identities are pi G=A, pi A=A pi, and A fixes the roots.

Let w=g_1...g_n be an ordinary history AFTER the fixed root, so its
complexity is k=n+1. Set v_0=rho and v_i=g_i(v_(i-1)); x=v_n.
The scanner H emits S_(v_i mod4) at position i. Its prefix at position i
evaluates to A(v_i), and H(w) evaluates to A(x).

Claim status: `partial-proof` (all-depth). For r>=1 the ith letter of H^r(w) is

    S_(A^(r-1)(v_i) mod4).                            (1)

Since each generator adds one base-four position and pi commutes with A,

    pi^(n-i)(x)=A^(n-i)(v_i).                         (2)

For every i>=n-r+1, (1) therefore equals the endpoint expression

    S_( A^(r-1-(n-i))(pi^(n-i)(x)) mod4 ).            (3)

Consequently the last min(r,n) letters are determined by x, the phase,
n and r, independently of the initial representation. All representations
of x have the same H^n history. The empty history n=0 is already unique.
For r=0 no letter formula is asserted.

Proof. Induction gives A^(r-1)(v_i) as the ith prefix endpoint after
r-1 passes, so the next scanner emits (1). Equation (2) is iterated
projection. The nonnegative exponent in (3) is exactly the
condition i>=n-r+1. No canonical choice is imposed on the starting word.

## Forced-history extension (`partial-proof`)

Suppose the forced orbit x_t=F^t(x) is defined through time r. At each
permitted step append Q_t to H of the current history, where x_t mod16=7
selects U and residue11 selects T. The branch is determined by the actual
endpoint, not by a representation choice.

The first n letters after r updates are exactly H^r(w). A letter appended
at time t (1<=t<=r) has prefix endpoint x_t when born. At later time r,
its prefix endpoint is A^(r-t)(x_t); if r>t its letter is

    S_(A^(r-t-1)(x_t) mod4),                         (4)

while at r=t it is the appended Q_(t-1). Thus the entire appended suffix
is independent of the original representation at every time. Among the
original n positions, only the first max(n-r,0) can remain ambiguous.
The basic full-synchronization bound is r>=n, conditional on the forced
segment being defined. The unbounded history still grows by one letter
per step; this is not a finite-state endpoint quotient or termination.

## Acceleration by periodic head cores (`partial-proof`)

Let tau_(a,j) be the first age at which A^tau(O_(a,j)) is stable. The
head theorem proves that the stable set is the entire A-periodic core,
and A is bijective on that set. This does not assume a unique cycle.

If v,v' in O_(a,j) satisfy A^b(v)=A^b(v'), then

    A^min(b,tau_(a,j))(v)=A^min(b,tau_(a,j))(v').     (5)

When b<=tau this is the premise. Otherwise the two states at age tau
are in the periodic core; their further A^(b-tau) images agree, so
bijectivity forces them to agree already.

For two histories of the same endpoint, take v=v_i, v'=v_i', j=i+1
and b=n-i in (5). The ith emitted letter is representation-independent
once r>=1+tau_(a,i+1). For 1<=h<=n, combining the first h positions
with the endpoint suffix (3) yields the sufficient full-sync bound

    R_(a,k,h)=max(n-h, 1+max_(2<=j<=h+1) tau_(a,j)). (6)

The basic r>=n bound remains available if (6) is larger. The established
small stabilization ages are tau_(p,2)=0, tau_(u,2)=1, both tau_(a,3)=2,
and tau_(p,4)=4, tau_(u,4)=3. Hence h=2 gives

    r>=max(k-3,3),             k>=3, either phase,  (7)

and h=3 gives

    r>=max(k-4,5),             k>=4, phase p;
    r>=max(k-4,4),             k>=4, phase u.       (8)

In particular at cut c=k-4, all initial representations have synchronized
when p,k>=9 or u,k>=8, provided that many forced steps exist. This is
exactly the start of the newer dominant-empty region L=c+1=k-3. Larger
cuts remain synchronized under the deterministic update. This removes
initial representation freedom there; it does not assert that any such
cut contains a genuine return occurrence.

The synchronized history is a function of the ORIGINAL endpoint, phase,
k and elapsed time. It is not asserted to be the unique ordinary history
of the later endpoint F^r(x), which can have other representations outside
this induced family. Thus selecting a different initial representation
cannot help after synchronization under the prescribed update; reselecting
or renormalizing representations at later times is not ruled out.

## Finite verification and a sharp one-pass obstruction

Claim status: `finite-exhaustive`. Both implementations agree on all
19,682 ordinary words across both phases and k1..9, giving 1,138 endpoint
groups. The primary performs 167,306 iterate-endpoint checks and634,776
suffix-position checks with no violation. The lead independently builds
histories from cell-array A-orbits of their full prefix values, rather
than repeatedly scanning a word. Its9,096 endpoint/age image sets agree
with all28,835 distinct images retained by the primary, after removing
the primary's explicitly retained phase-root letter. All2,255 applicable
h2/h3 endpoint-bound checks agree, including separately labelled basic-n
fallbacks when a proposed R exceeds n.

The maximum first coalescence ages at k1..9 are, in BOTH phases,

    0,1,1,1,2,3,3,3,4.

These are finite values, not an all-depth growth law or sharpness claim
for (6). There are394 endpoint groups whose representations do not
coalesce after one pass. The first in the declared order is phase p,k5,
x=802, with nonroot histories

    tttu -> H image upup,
    tutt -> H image uppp.

Both initial words from root3 give802; both different images give891.
They coalesce at r=2. Thus one-pass universality is `refuted`; complexity5
is minimal by exhaustive coverage of every smaller level. This is an
ordinary-cylinder counterexample, not a genuine return occurrence. The
earlier hand example885 is valid but not minimal and is not needed here.

The u18 comparison independently agrees on all11 states,10 forced
updates and48 edge counts. Applying (1)/(4) to the SAME recorded orbit
also reconstructs every complete history, checking225 emitted letters
and242 prefix values. No additional trajectory was generated for that
formula check.

## Sixteen-state potential probe

Claim status: `refuted` for strict decrease on every genuine block of
W_0t, the count of T edges entered at old prefix residue0 modulo16. On
the already certified u18 block it has values0->0, whereas on the prior
u14 block it has values2->0. This does not refute nonincrease or a
longer-block amortization argument.

An exact common finite weight vector is

    W*(w) = count_(old residue0 mod16,T)(w)
          + count_(old residue1 mod16,U)(w).

| Named block | First edge count | Second edge count | W* |
| --- | --- | --- | --- |
| u14,cut1->7 | 2->0 | 0->0 | 2->0 |
| u18,cut4->10 | 0->0 | 2->0 | 2->0 |

The displayed values are `finite-exhaustive`. W*>=0 on every history is
an elementary all-depth fact (`partial-proof`), since both coefficients
are1. Thus the sixteen-state class satisfies these two finite constraints;
no numerical LP is needed. Universal strict descent of W* remains
`inconclusive` and is not assumed in the synchronization proof.

## Review, records and remaining obligation

Muse Spark 1.3 Contributor independently derived (1)--(8), including the
forced suffix, core bijectivity and cut indices. It also checked the
one-pass and finite-weight scopes. Fresh adversarial review accepted the
mathematical synchronization argument and the qualification that only
prescribed descendants of initial representations are synchronized.
Final read-only review explicitly accepted formulas (1)--(8), compared
the complete stored image/count/bound tables, audited the225-letter and
242-prefix reconstruction, and validated the three original provenance
chains, runner/input hashes and aggregate timing. It found no correction
and repeated no scientific run.

Records in `results/problem1/`:

- `20260905_history_synchronization_primary.json`: complete original
  u18, all-word synchronization and one-pass diagnostic records, source,
  runner, raw word-image sets, timings and source/input/payload hashes.
- `20260905_history_synchronization_independent.json`: independent
  cell/odd-section prefix-orbit construction and the fixed u18 replay.
- `20260905_history_synchronization_verification.json`: complete image-set
  comparison, small counterexample, forced-formula reconstruction, exact
  two-edge weight check and original provenance-chain verification.

Primary aggregate timing is the sum of its original run timings, not
contiguous elapsed time. Original primary paths are retained; their
intermediate diagnostic inputs are embedded and shared frontier/u14
inputs remain recoverable from committed records. Independent and
verification sources support RULE30_REPLAY_ROOT and RULE30_REPLAY_OUTPUT
and need no historical temporary files. Runs stayed local within120seconds
and1GiB; the immutable reference hash is unchanged.

The theorem constrains surviving initial-representation ambiguity, not
signed endpoint mass or return existence. At the stated critical cuts,
choosing a different initial history and following the same prescribed
update cannot change the resulting history. Later reselection remains
outside the theorem, and a nonlinear or original-x-dependent potential
can escape the older additive no-go without contradicting synchronization.

Next question (`inconclusive`): does W* survive another already certified
return block, and can the explicit synchronized suffix be used to prove
descent or a forbidden return pattern on its induced family? Specify
that family and its INITIAL complexity before testing. A proof must still
exclude genuine returns in the dominant-empty layers or establish another
all-depth occurrence bound; synchronization alone does neither. Do not
increase the word/frontier cap merely to fit the observed coalescence ages.
