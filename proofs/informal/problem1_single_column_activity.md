# A single-column record for eventual finite support

Status: `partial-proof`, lead-derived and lead-checked; the finite checks
are complete. Round four supplies a complete scoped external derivation
of Section3's uniform finite-entry theorem; review of every other
section is not inferred. Its scoped content is recorded below.
Problem 1 remains open.
This continues `problem1_temporal_activity_deficit.md` and replaces
its six-cell score by one bit at each sampled time.

## Purpose and admission

The temporal-deficit theorem distinguishes eventual entry into finite
support from permanent infinite support. Its proof suggests that the
special weight I and the additional observed gate are unnecessary for
the resulting unboundedness target. Derive a single-column observable
first; a failed precision or finite-entry argument would invalidate
that simplification. No larger schedule or spatial-width search follows.

The optional finite verification is restricted to the SAME twelve
rational inputs and ages 0..16 already admitted in the temporal-deficit
note. Check the comparison inequality only for s=1..14 so that s+2
stays within that bound, and the seam only at x=7,43, s=1..15.
The added zero age is the empty sum. The local Rule 30 rows already
needed for D cover the bit used here. Retain full count vectors, not
only totals. A disagreement corrects a proof identity; agreement says
nothing about actual-survivor unboundedness. No input, comparator,
frontier, occurrence or memory-width extension is admitted.
Local one CPU, 120 seconds and 1 GiB per implementation; any run
must retain the full atomic protocol and source/admission snapshots.

## 1. The observable and its gate precision (`partial-proof`)

For any 2-adic x put V_0(x)=0, and for s>=1 define

    V_s(x)=sum_(t=0..s-1) bit_(2s)(T^t(x)).               (1)

It counts active times in the single spatial column 2s, before time s.
Always 0<=V_s<=s. In the notation of the preceding note,

    V_s(x)=sum_(t=0..s-1) bit_0(A^t(pi^(s-t)(x))).        (2)

This follows from A^t=pi^t T^t and pi A=A pi. Every term uses only
bits 0,...,2s of x, because T is causal toward increasing indices.
Therefore the first s OBSERVED forced branches, whose cylinder has
precision 2s+2, determine V_s. No additional observed branch or
unobserved admissibility letter is needed. The case s=0 is constant.

If y=T^h(x) is a nonnegative integer and k=ceil(bitlen(y)/2), with
bitlen(0)=0, the finite propagation bound gives

    V_s(x)<=min(s,max(h,k-1)).                            (3)

For times t>=h the column 2s is zero if t<=s+h-k. At most h early
times and max(k-h-1,0) late times remain. When the proposed bound
exceeds s, use V_s<=s. In particular, for positive finite x of
original complexity k,

    V_s(x)<=k-1  for every s.                            (4)

This bound uses ORIGINAL size and does not require ordinary-frontier
membership. An infinite initial tail is not excluded by bounded V:
the finite-entry examples -1 and -1/7 from the preceding note remain
essential scope controls.

The connection to ordinary histories is exact. If an ordinary input
has nonroot length n=k-1 and prefix endpoints v_0=rho,...,v_n=x,
then for s>=n,

    V_s(x)=sum_(i=0..n-1) bit_0(A^s(v_i)).                (4a)

To prove this, set d=s-t in (2). Terms with d>n vanish because
pi^d(x)=0. For 1<=d<=n, the existing endpoint projection identity
pi^d(x)=A^d(v_(n-d)) turns its summand into bit_0(A^s(v_(n-d))).
The empty original history has V_s=0. Thus, at these ages, V counts
odd preceding prefixes in the PURE scanner image of the original
history. It is not the cost of every position in the longer current
prescribed history: the appended positions are absent. This precise
restriction is why universal descent results for total current-history
potentials cannot be applied without checking their domains.

## 2. Quantitative comparison with the deficit (`partial-proof`)

Let R_N^V=max_(0<=s<=N)V_s and R_N^Z=max_(1<=s<=N)Z_s, for N>=1.
For all 2-adic x and s>=1,

    V_s <= 2 Z_s+1,                                     (5)
    Z_s <= V_(s-1)+3V_s+3V_(s+1)+2V_(s+2)+2.             (6)

To prove (5), the bit at 2s belongs to the six-cell window starting
at 2s-2 used by Z_s. A zero window contributes no active bit.
Every nonzero window is either a noncharge or the charge pattern 5.
Every charge-5 time except possibly the final sampled time is followed
by a noncharge time, as proved in the temporal-deficit note. Thus the
number of nonzero-window times is at most 2Z_s+1.

For (6), a noncharge window is necessarily nonzero, so bound its
indicator by the sum of its six bits. Write u_i(t)=bit_i(T^t(x)).
For any i>=2 the local rule gives

    u_(i-1)(t) <= u_i(t) XOR u_i(t+1)
                 <= u_i(t)+u_i(t+1).                    (7)

Indeed the XOR is u_(i-1)(t) OR u_(i-2)(t). Over times 0,...,s-1,
the three even columns 2s-2,2s,2s+2 have total activity at most
V_(s-1)+1, V_s, V_(s+1), respectively. Apply (7) to the three
odd columns using their NEXT even columns. Their activities are at
most 2V_s+1, 2V_(s+1), and 2V_(s+2), respectively. All sampled
times lie within the defining horizons of these V terms. For s=1,
the first even-column bound is V_0+1=1; no negative age is used.
Adding the six bounds proves (6).

Consequently

    R_N^V<=2R_N^Z+1,
    R_N^Z<=9R_(N+2)^V+2.                                (8)

In particular V_s is bounded in s if and only if Z_s is bounded.
The constants in these elementary comparisons are not claimed optimal.
Combining (8) with the preceding theorem proves

    sup_s V_s(x)<infinity
      iff some T^h(x) is nonnegative finite.              (9)

No assumption that the counts grow monotonically at every age is
made. Their RECORD maxima are monotone by definition.

## 3. A direct single-column proof and an entry-time bound

Status: `partial-proof`. The spatial-limit argument can also be made
directly with V and gives a somewhat better extinction estimate.
If V_s<=K at every s, take any spatial limit of even shifts tending
to infinity. Every even column of that bi-infinite limiting spacetime
has at most K active times. This follows by using age s+a for the
column shifted by 2a and then letting s tend to infinity.

Equation (7) implies that every odd column has at most 2K active
times: the next even column has finite support in time, hence at
most 2K temporal flips. Thus every column has finite activity.
The last-activity lemma makes the final active row identically one
at one common finite time M, unless the spacetime is already zero.

In N consecutive columns, the total activity over ALL times is at
most (3K/2)N+O(K), because half the columns have bound K and the
other half have bound 2K. The same disjoint-interval count used in
the preceding note now gives

    sum_(r=0..M) 1/(2r+1) <= 3K/2.                      (10)

Define

    h_V(K)=min{h>=0: sum_(r=0..h)1/(2r+1)>3K/2}.

All spatial limits vanish by this common time. The same compactness
argument therefore proves that T^h_V(K)(x) is nonnegative finite.
For K=0 the limiting spacetime is zero initially and h_V(0)=0.
This proof, like the deficit theorem, bounds an entry TIME, not the
size of the eventual finite row. It uses no bounded-state model of
the actual survivor and no experimental period bound.

## 4. An exact actual-gate seam (`partial-proof`)

If the first forced step of x is defined, then for every s>=1,

    V_(s+1)(x)-V_s(F(x))
      =bit_(2s+2)(x)+bit_(2s+2)(T(x))
          -bit_0(A^(s+1)(x)),
    -1 <= V_(s+1)(x)-V_s(F(x)) <= 2.                    (11)

To see this, each projection exponent s-t in (2) is at least one.
Use pi F=A^2 and commute A with pi:

    V_s(F(x))
      =sum_(t=0..s-1)bit_0(A^(t+2)(pi^(s-t-1)(x)))
      =sum_(r=2..s+1)bit_(2s+2)(T^r(x)).

Subtract this from V_(s+1)(x), whose time indices are 0,...,s.
The only unmatched terms are 0,1 and s+1. Identity A^(s+1)=
pi^(s+1)T^(s+1) gives the last term in (11).

After h actual steps the difference between V_(s+h)(x) and
V_s(F^h(x)) lies between -h and 2h. Thus record unboundedness
is invariant under removal of a fixed finite actual branch prefix.
For infinite forced survivors, (9) and the finite-entry equivalence
for T and F show that unbounded V is exactly absence of a finite
state anywhere on that forced orbit.

## 5. The remaining research obligation

Status: `inconclusive` for growth on the ACTUAL period-two survivor.
The concrete target is now an unbounded record R_N^V, using each
complete observed prefix with no extra gate. For any fixed finite
initial state, (4) instead bounds this record by its original k-1.
A proof of record growth would therefore exclude finite support.
Neither positive density nor a uniform linear slope is required.

This is an ordered temporal observable with growing sampling length.
Its late-age ordinary-history expression (4a) is additive on the
original positions; it is not the same as an additive potential on
ALL positions of the current prescribed history. The earlier no-go
results for universal total-history descent therefore do not supply
a proof or a refutation of record growth here. No growth conclusion follows merely
from naming the record or proving (9). No occurrence-cut bound,
signed nonvanishing theorem, or result for temporal least periods
at least three is established here.

Status: `finite-exhaustive` for all204 full temporal bit vectors,
170 finite-entry bounds,168 V/Z comparison rows and30 complete seam
rows in the declared ranges. The primary computes the A-diagonal
formula (2); the independent implementation uses cell-array T evolution
and rational long division. Complete vectors agree, not just their sums.
Records are `20260906_single_column_activity_independent.json` and
the shared `20260906_temporal_activity_deficit_{primary,verification}.json`
in `results/problem1/`. Executed source and admission snapshots are
retained even where later prose expanded (4a) or verification details.

The all-depth arguments above remain lead-derived and lead-checked.
Round four adds a complete fresh Muse derivation of Section3, including
the fixed-input versus spatial-limit quantifiers, odd-column inequality,
last-time rigidity, harmonic estimate and common-time compactness step.
The lead accepted that scoped derivation, archived in
`problem1_activity_finiteness_independent_review.md` with source hashes.
That record also documents a subsequently inserted false one-sided
commutation sentence: it was rejected and removed before acceptance of
the revised review. No full verdict on all other sections is inferred.
The new corrected finite-level theorem is in
`problem1_activity_level_finiteness.md`.

The earlier round-three initial
blanket acceptance was rejected for three proof-critical review errors;
the corrective source audit is retained only in its actual scope.
The provider attempts, accepted last-time/harmonic derivations and the
separate superseded primary-record correction are detailed in the
temporal-deficit note and `20260906_temporal_activity_review.json`.
That round's agent threads were closed. No all-section reviewer
acceptance or actual growth result is inferred from finite comparisons.
