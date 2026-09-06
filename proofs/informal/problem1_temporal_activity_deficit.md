# Temporal activity and the original-position deficit

Status: `partial-proof` for the all-depth statements below. The declared
finite checks are complete; a usable complete external proof review is
still missing. Scoped review and its corrections are recorded in Section6.
Round four independently verifies the Section3 last-time/harmonic lemmas
and the spatial-limit argument as used for the single-column V theorem;
this does not imply acceptance of every Z-specific section here.
This is a new support criterion and a reformulation of the active
period-two bottleneck, not an exclusion of period two or a solution of
Problem 1. Base checkpoint: `a60d87f4c88343afe22b7ee5ee9f8180b96ecaee`.

## Admission and route selection

The current boundary functional is Psi_s=D_s+beta_s, with beta_s>=0.
Its original-history lower bound motivated a subunit upper bound, but
the last round showed that sparse interruptions can change Psi by a
linear amount. No further comparator, suffix-width, or memory sweep is
admitted. The ranked structural alternatives are:

1. Retain D_s alone and its ordered temporal interpretation. An
   all-depth support criterion would remove the appended-letter cost
   from this route without discarding any observed gate.
2. Close the projected boundary evolution. Its exact update needs four
   further lower bits; the visible row alone is not a closed state.
   This failure does not rule out averaged inequalities with more state.
3. Control a nonlinear observable on the complete prescribed history.
   This remains available if the temporal criterion adds no mechanism.

Choose route 1. The proof comes before computation. The proposed
equivalence is: for ANY 2-adic input x, bounded Z_s=s-D_s is equivalent
to T^h(x) being a nonnegative integer for some finite h. It is NOT
equivalence to x itself being a nonnegative integer. The negative
integer -1 and the nonintegral rational -1/7 are mandatory controls.

Verification admission, fixed before execution: check the temporal
identity and finite-entry bound by two simple independent methods on
the named rational inputs 0,1,2,3,5,7,-1,-2,-3,-1/7,1/3,-1/3 and
ages 1..16 only. One method may use modular bit operations and A;
the other must use cell-array T evolution with sufficient initial
precision. Check all 256 local eight-bit neighborhoods for the charge-5
transition, and the 64 pairs of length-three finite temporal words for
the last-activity identity whenever their induced third word is finite.
The latter check must include the terminal time; it is only a local
identity check, not a spatial-orbit census. Compute exact rational
harmonic thresholds for K=0,1,2. Replay only the stored ordinary
endpoint 7's defined forced prefix, plus the named two-branch inputs
7 and 43, to check the one-step deficit seam for ages 1..16; the
algebraic seam needs a first gate only, not a longer observed word.
No other input, frontier, occurrence, comparator or width is admitted.

A mismatch refutes an identity, constant, or seam used in the proof.
Agreement verifies exactly these finite controls and cannot establish
the compactness or all-depth implications. The latter need independent
derivation and fresh adversarial review. Each implementation is local,
one CPU, at most 120 seconds and 1 GiB, with atomic JSON, full Git,
executed source and admission snapshots, hashes, software/hardware facts,
timings and limitations. No optimized backend or benchmark is involved.

## 1. A fixed spatial window (`partial-proof`)

Use the established maps on the 2-adic integers:

    T(x)=x XOR((x<<1) OR(x<<2)),
    pi(x)=x>>2,       A(x)=pi(T(x)),
    I(z)=1 if z mod64 is 0 or 5, and 0 otherwise.

Right shift deletes the lowest two binary digits, also for negative or
nonintegral 2-adic inputs. Bitwise operations have their usual digitwise
meaning. The original cost note defines, for s>=1,

    D_s(x)=sum_(d=0..s-1) I(A^(s-1-d)(pi^d(x))),
    Z_s(x)=s-D_s(x).                                      (1)

These definitions require no forced gate or ordinary membership.
Always 0<=Z_s<=s. The previously proved commutation pi A=A pi gives

    A^r(x)=pi^r(T^r(x))                                  (2)

for all r>=0: if it holds at r, commute A past pi^r and use A=pi T.
It follows, putting r=s-1-d in (1), that

    D_s(x)=sum_(r=0..s-1) I(pi^(s-1)(T^r(x))).             (3)

Thus Z_s counts the times r=0,...,s-1 when the SIX-cell window
at positions 2s-2,...,2s+3 is neither 000000 nor 101000, with
bits written from low index to high index. It samples one fixed
spatial window at consecutive times. It is not the sum along a
closed trajectory of projected boundary rows.

For a finite observed branch word of length s+1, the existing cylinder
precision 2s+4 determines every term in (1), hence Z_s. This is a
schedule functional when that entire word is actually observed.
An unobserved admissibility letter supplies no precision.

## 2. Finite entry gives bounded deficit (`partial-proof`)

Suppose y=T^h(x) is a nonnegative integer, h>=0, and put
k=ceil(bitlen(y)/2), taking bitlen(0)=0. Then for every s>=1,

    Z_s(x)<=min(s,max(h,k)).                              (4)

For r>=h, the highest possible nonzero position of T^r(x) is below
2k+2(r-h); if y=0 the whole row is zero. Its window starting at
2s-2 is therefore zero whenever h<=r<=s+h-k-1.
If h>=k, all r>=h in the sampled range are zero windows and at most
h earlier times can pay Z. If k>h, at most h early and k-h late
times can pay. When s<=max(h,k), use Z_s<=s. This proves (4),
without assuming anything about the other sampled windows.

In particular a positive finite x of complexity k has Z_s<=k at
every age. No generator history or ordinary-frontier condition is needed.

The converse cannot say that x is finite. Exactly,

    T(-1)=1,       Z_s(-1)=1;
    T(-1/7)=-1,    T^2(-1/7)=1,
    Z_s(-1/7)=min(s,2).                                  (5)

For -1/7 the initial spatial word repeats 100; its six-bit rotations
are 9,18,36, all uncharged by I. Its next row is -1, also uncharged.
All later sampled windows are zero, by the speed bound with h=2,k=1.
These are exact identities, not extrapolations of the verification ages.

## 3. Last activity is spatially rigid (`partial-proof`)

Here use the SAME local rule on a BI-INFINITE spatial row, with
time t>=0:

    u_i(t+1)=u_i(t) XOR(u_(i-1)(t) OR u_(i-2)(t)).

Suppose each spatial column has finitely many active times. Define
E_i={t>=0:u_i(t)=1}, and m_i=max(E_i), with max(empty)=-infinity.
Then either the whole spacetime is zero, or there is one M>=0 such
that m_i=M for EVERY i. In the second case row M is identically one
and all rows after M are identically zero.

Indeed the temporal difference of a finite-support binary sequence
has the same last nonzero time as that sequence, including time zero:

    last(u_i(t+1) XOR u_i(t))=m_i.

The local rule identifies that difference with the OR of the two
lower-index columns. Hence

    m_i=max(m_(i-1),m_(i-2)).                             (6)

This makes m_i>=m_(i-1), and then
m_(i+1)=max(m_i,m_(i-1))=m_i. It holds at every spatial index,
so all last times are equal, including the possible value -infinity.

There is also a quantitative bound. If EVERY column has at most B
active times, the nonzero case satisfies

    sum_(r=0..M) 1/(2r+1) <= B.                          (7)

At time M-r, each spatial interval of length 2r+1 contains a one:
otherwise the rightmost cell of that interval would still be zero
after r updates, whereas row M is all ones. Partition N consecutive
columns into such intervals. At that time there are at least
floor(N/(2r+1)) active cells in those columns. Sum over r=0,...,M,
compare with BN, divide by N, and let N tend to infinity. The sum
over r is finite, so no interchange of infinite sums is involved.

The odd harmonic sums diverge (grouping r into dyadic intervals
already proves this). Thus a uniform bound B on per-column activity
gives a uniform finite extinction time. This is proved for this rule
and this domain; no general cellular-automaton nilpotency theorem is used.

## 4. Bounded deficit forces finite entry (`partial-proof`)

For an integer K>=0 define the finite integer

    h(K)=min{h>=0: sum_(r=0..h) 1/(2r+1)>2K}.             (8)

**Theorem.** For every 2-adic x, if Z_s(x)<=K for all s>=1, then
T^h(K)(x) is a nonnegative integer.

First, check the only local conversion needed. If the current six-bit
window equals 5, its next window equals 26 or 27, depending on the
two bits just below it. Both are uncharged by I. The bits in positions
2,...,5 of the next window are always 0,1,1,0, independently of
those lower boundary bits. Thus every charge-5 time is followed by a
noncharge time. On an infinite temporal word with at most K noncharge
times, there are at most K charge-5 times and at most 2K times with
a NONZERO window. Distinct charge-5 times have distinct successors.

Extend the binary digits of x by zero at negative spatial indices.
Take any subsequential spatial limit obtained by shifting x by even
amounts j_n tending to infinity, and call its bi-infinite initial row
v. A subsequence exists by diagonal selection on finite windows.
For every fixed even offset 2a and finite time horizon, the window
of v at 2a is the limit of the windows of x at j_n+2a. Those input
windows are controlled by (3) at ages (j_n/2)+a+1, which tend to
infinity. Local evolution commutes with these limits: each fixed
output window and finite time uses only finitely many input cells,
eventually far from the artificial negative-index boundary.

Consequently every even-aligned six-cell window of v has at most K
noncharge times over ALL t>=0. If it had K+1, their finite set of
times would contradict the corresponding sufficiently large input age.
The local conversion above gives at most 2K nonzero times per such
window. Every spatial column lies in an even-aligned window, so each
column of v has at most 2K active times.

Apply Section 3 with B=2K. Either v is already zero or its common
last time M satisfies the harmonic bound (7), hence M<h(K). In
either case T^h(K)(v) is the zero row. For K=0, h(0)=0 and the
activity bound already says v itself is zero.

Every such spatial limit is therefore zero after the SAME finite
time h(K). If T^h(K)(x) had infinitely many nonzero binary digits,
choose even shifts immediately below a sequence of these positions.
After taking a subsequence, one of positions 0 or 1 of the shifted
output is always one. A limit of the shifted INPUT rows then has
a nonzero output at that position after h(K) updates, a contradiction.
Thus the output has only finitely many nonzero binary digits.

Combining Sections 2 and 4 proves the exact equivalence

    sup_(s>=1) Z_s(x)<infinity
      iff T^h(x) is nonnegative finite for some h>=0.      (9)

The output support size is not bounded by (8). It may depend on x;
the theorem bounds an entry time, not a uniform support window.
The proof uses bounded activity in SPATIAL LIMITS, not a false claim
that the original one-sided columns become temporally zero.

## 5. The forced-orbit seam and remaining target (`partial-proof`)

Suppose x has an infinite actual forced orbit x_r=F^r(x), with the
usual gate 7 or 11 modulo16 at every step. The established identity

    pi^r(F^r(x))=A^(2r)(x)

and (2) imply

(The local identities also hold on 2-adic gate cylinders: every fixed
finite gate prefix is preserved by sufficiently precise nonnegative
truncations, and all involved maps are continuous there.)

    some T iterate of x is nonnegative finite
      iff some actual F iterate of x is nonnegative finite. (10)

In one direction, if T^h(x) is finite, choose 2r>=h. Then
A^(2r)(x)=pi^(2r)(T^(2r)(x)) is finite, and adding back the r
deleted low pairs makes F^r(x) finite. In the other direction,
finite F^r(x) makes A^(2r)(x) finite; adding back 2r deleted low
pairs makes T^(2r)(x) finite. Deleting finitely many low digits
does not turn an infinite high tail into a finite one.

Thus unbounded Z_s on an infinite forced survivor is equivalent to
EVERY one of its actual forced states having infinite support. This
is an equivalence of escape from eventual finite support, not a proof
that the survivor in the actual period-two problem escapes.

There is also a direct finite seam identity. If the first gate of x
is defined, the established D recurrence gives, for every s>=1,

    Z_(s+1)(x)-Z_s(F(x))
       =1+I(A^(s-1)(F(x)))-J(pi^(s-1)(x)),
    -1 <= Z_(s+1)(x)-Z_s(F(x)) <= 2,                    (11)

where J(y)=I(A(y))+I(pi(y)). Its algebra only needs this first
actual gate. To interpret both sides from observed branch WORDS
still requires the full lengths s+2 and s+1 respectively.
Iterating (11) across h actual steps bounds the difference between
Z_(s+h)(x) and Z_s(F^h(x)) between -h and 2h. Hence unboundedness
is unchanged by removing any fixed finite actual branch prefix.

For an observed infinite schedule define the monotone record

    R_N^D=max_(1<=s<=N) Z_s.                             (12)

Any proof that R_N^D tends to infinity on the ACTUAL required
survivor would exclude finite support, with every finite temporal
transient handled by (11). A uniform positive linear growth rate,
or growth at every age, is not necessary. For positive finite input
of original complexity k, (4) gives R_N^D<=k.

This removes beta_s from the sufficient inequality target. Precisely,

    s-1-Psi_s=Z_s-1-beta_s <= Z_s-1.

Unbounded positive deficit of Psi therefore implies unbounded Z,
while the reverse implication is not established here. The old
periodic-comparator and terminal-edit results concerned Psi; their
slopes and sensitivity claims must not be silently transferred to D.
No new all-depth growth assertion is made for the actual survivor.
Least temporal periods >=3 remain outside this auxiliary forced route.

## 6. Verification and scope

Status: `finite-exhaustive` for the completed declared controls. Modular
A-diagonal arithmetic and independent T cell arrays with rational long
division agree on all192 full temporal score vectors,160 finite-entry
bounds,256 local neighborhoods,64 temporal-word pairs, the three exact
harmonic thresholds h(0)=0,h(1)=7,h(2)=418, two two-step gate orbits,
and32 complete seam rows, including both separate I and J terms.
The records are `20260906_temporal_activity_deficit_`
`{initial,primary,independent,verification}.json` in `results/problem1/`.

Muse supplied a partial primary implementation before its followup and
delayed retry ended in provider429. It supplied no usable all-depth
proof verdict. Lead review corrected an unadmitted modular finite-entry
search: a truncated value looking small does not prove a finite 2-adic
tail. The initial source/record is retained as superseded provenance;
the accepted controls instead corroborate the exact stipulated identities.
Lead also added resource enforcement, full executed-note snapshots and
complete comparisons. The initial primary's finite D vectors themselves
agree with the corrected implementation and independent cell vectors.

The MiMo primary fallback was closed while running without a usable
correction or verdict. Fresh proof-only Muse review and its delayed retry
also returned429. Its MiMo fallback independently checked the last-time
recurrence and harmonic-density argument; those scoped derivations are
retained. Lead rejected its blanket acceptance: the report wrongly used
a universal V hypothesis instead of the ONE fixed input's Z bound,
replaced an OR identity by a false equality, and confused the finite
terminal remainder with the infinite-time bound2K. These were review
errors, not demonstrated flaws in the source proof.

The corrective response supplied a scoped source/quantifier audit and
correct source hashes, fixing those three statements. It did not supply
the requested complete replacement derivation or a renewed complete
verdict. Thus full external proof verification remains missing; the
initial blanket acceptance is not counted as complete. All threads are
closed. Exact disposition, critical initial excerpts, the full corrective
response and reviewed source snapshots are archived in
`results/problem1/20260906_temporal_activity_review.json`.
The finite checks do not discharge the missing review or actual growth.
Round-four update: a fresh complete Muse derivation of the single-column
finite-entry theorem, including this note's last-time/harmonic lemmas and
its common-time spatial-limit argument, is now accepted in that precise
scope. See `problem1_activity_finiteness_independent_review.md`; it also
records correction of the review's subsequently inserted false one-sided
commutation claim. No blanket verdict on all Z-specific sections follows.
The immutable reference is unchanged, and source/admission hashes reload.
The signed-mass and B_all routes
remain open; this note proves neither a new occurrence exclusion nor
the required unboundedness on the actual fringe.

Dependencies are the exact definitions and D recurrence in
`problem1_critical_cost_schedule_identity.md`, the all-bit and
forced leading-block identities in `problem1_frontier_head_dynamics.md`,
and the finite branch-cylinder precision in
`problem1_finite_schedule_repetition_bound.md`. Section 3 and the
spatial-limit argument in Section 4 are proved in full here.
