# Exact boundary growth for periodic auxiliary schedules

Status: `partial-proof` for the structural reduction; `refuted` for the
specified averaging and additive-approximation classes; `finite-exhaustive`
for the named controls. The proposed uniform subunit bound and Problem 1
remain open. Review scope and limitations are recorded below.

## Admission and route choice

The explicit ut survivor has boundary slope 1/14. General rationality of
eventually periodic auxiliary schedules is ALREADY proved in
`problem1_periodic_schedule_rationality.md` and is not repeated here.
The new question is whether the boundary functional has a computable,
phase-dependent exact growth law on each stored periodic survivor.
This is a test of the proposed schedule-only density bound, not another
periodicity search or an attempted proof from finite absence.

Use ONLY the four existing rational phase certificates for t, u, ututtt
and ttututt, and the new explicit ut control. No rational cycle, frontier,
ordinary endpoint or forced schedule is generated or extended. A slope
at least one in an admissible example would refute every uniform
subunit bound. If all named slopes are below one, retain their exact
controls and the structural phase reduction; no general upper bound
or further scan follows. Constant t/u are inadmissible controls.

Derive the all-period identity first. Compare modular evaluation of the
stored rational fractions with independent extraction from their stored
spatial bit-vector certificates. Verify one full score period and the
following period, including the spatial-onset boundary. Local one CPU,
120 seconds and 1 GiB per implementation, atomic records with exact
parameters, source/input hashes, full Git, hardware/software and timings.

## 1. Reverse the finite boundary sum (`partial-proof`)

Let q be a word of length p>=1 repeated indefinitely. Let X_j be its
phase-j 2-adic survivor, j modulo p, so F(X_j)=X_(j+1). The existing
rationality theorem supplies a COMMON spatial onset a>=0 and period
lambda>=1 for all phase digit streams. These need not be minimal.

Retain pi(x)=x>>2, I(z)=1 for z=0 or5 mod64 and 0 otherwise, and
J(y)=I(A(y))+I(pi(y)). The finite boundary functional is well-defined
on 2-adic survivors by its finite precision. Put

    d0=ceil(a/2),
    m=lambda/gcd(lambda,2),
    L=lcm(p,m),
    w_e(d)=J(pi^d(X_(e-d modp))).                    (1)

For every s>=1, setting e=j+s-2 modulo p and reversing the index
d=s-t-2 in the established sum gives exactly

    Psi_s(X_j)=sum_(d=0..s-2) w_e(d).               (2)

This keeps the ENDING phase e. Averaging it away is not justified.
The sum is empty at s=1, regardless of the chosen phase convention.

## 2. Eventual periodicity of the score and exact increments

Status: `partial-proof`. For d>=d0, all bits used by J(pi^d X_j)
are in the periodic spatial tail: the first tested position is at
least 2d>=a. Since 2m is a multiple of lambda and L a multiple of
both p and m,

    w_e(d+L)=w_e(d),  for every d>=d0.               (3)

Define the nonnegative integer

    M_e=sum_(d=d0..d0+L-1) w_e(d),
    mu_e=M_e/L.                                    (4)

Because s+L has the same ending phase as s, equations (2)--(3) imply

    Psi_(s+L)(X_j)-Psi_s(X_j)=M_(j+s-2 modp)
                                      for s>=d0+1. (5)

The threshold includes the possibly exceptional low spatial prefix.
It cannot be discarded merely because the schedule is periodic.
This is an exact identity on arithmetic progressions of ages, not a
numerical estimate or an asymptotic extrapolation.

There are at most gcd(p,m) distinct phase means. Indeed, in the
periodic spatial region,

    w_(e+m)(d+m)=w_e(d).

Summing one full period gives M_(e+m)=M_e, and M_(e+p)=M_e is
automatic. Hence M_e depends only on e modulo gcd(p,m). It need
not be independent of e when that greatest common divisor exceeds one.

## 3. Exact offsets and the uniformity obligation (`partial-proof`)

For N=s-1>=d0, write N-d0=qL+r with 0<=r<L. Then

    Psi_s(X_j)=B_e+q M_e+R_e(r),
    B_e=sum_(d=0..d0-1) w_e(d),
    R_e(r)=sum_(d=d0..d0+r-1) w_e(d).               (6)

Thus a finite certificate supplies EVERY age of this fixed periodic
schedule, including exact bounded offsets from each phase-dependent
line. The finitely many N<d0 are handled directly by (2).

If a named admissible schedule has any mu_e>=1, choose j and an
arithmetic progression of s with that ending phase. Equation (5)
then refutes an inequality Psi_s<=alpha*s+C with alpha<1 and a
constant C valid for all such ages. No ordinary endpoint is asserted;
this refutes only the stronger schedule-only version of that bound.

Conversely, mu_e<1 for every phase of several named schedules does
not prove a uniform subunit estimate on all schedules. Even a theorem
giving mu_e<1 separately for EVERY periodic word would still need
a slope bounded away from one AND uniform control of the offsets
in (6). Period and spatial onset are not bounded as the word varies.
Finite admissible prefixes also cannot be replaced by a periodic word
without verifying its continuation and retaining all observed gates.

The ordinary-domain route remains separate: with original nonroot
length n and enough actual branches, the established boundary identity
gives Psi_s>=max(s-n-1,0). A bound intended to contradict infinite
ordinary survival must hold with the needed quantifiers on those
actual histories. Equations (5)--(6) do not provide it.

## 4. A coarse split at a periodic suffix (`partial-proof`)

There is also an exact split valid on ANY sufficiently long actual
forced history, without ordinary membership. If 0<=h<=s-1, then

    Psi_s(x)=sum_(t=0..h-1) J(pi^(s-t-2)(F^t(x)))
                +Psi_(s-h)(F^h(x)).                 (7)

This simply separates the first h terms of the finite boundary sum.
In particular the first term on the right lies between 0 and 2h.
Suppose the s+1 observed branches have an alternating suffix starting
at h. Its length is s-h+1, so the finite precision theorem and the
explicit ut law give

    Psi_s(x)<=2h+ceil((s-h-1)/14).                  (8)

The extra observed branch is retained; an unobserved admissibility
letter cannot substitute for it. Equation (8) is not a theorem that
the prefix costs vanish, nor a bound independent of the suffix start.

This coarse method has an exact asymptotic limitation. More generally,
assume the periodic suffix admits `Psi_v<=mu*v+C`, with fixed
0<=mu<1 and C independent of the horizon in question. Discarding the
first h terms by `J<=2` gives only

    Psi_s <= mu*s+(2-mu)*h+C.                       (9)

Against the ordinary padding lower bound s-n-1 (fixed n), this gives
a contradiction under the sufficient condition

    limsup(h/s)<(1-mu)/(2-mu) <= 1/2.              (10)

For a suffix of fixed branch period p, the ALREADY PROVED repetition
criterion excludes ordinary infinite survival whenever
`s-2h-2p` is unbounded. It therefore already excludes every history
satisfying (10). For mu>0 the fractional threshold in (10) is strictly
smaller than 1/2. Thus this coarse splitting plus a periodic suffix
slope supplies no new asymptotic exclusion class of this form beyond
the existing repetition criterion. This is a limitation of the specified
argument, not of the full boundary functional or sharper prefix estimates.
For periods or offsets varying with s, neither comparison silently
discards their dependence on s.

An improvement must control the actual early terms in (7), rather
than merely replace every one by 2 and lengthen a periodic comparator.

## 5. Exact named controls (`finite-exhaustive`)

Modular evaluation of the stored rational fractions agrees with an
independently written cell-vector replay on the following ending-phase
totals. No source rational cycle was regenerated.

| schedule | admissible | d0 | L | M_e in phase order | phase slopes |
| --- | --- | --- | --- | --- | --- |
| t | no | 1 | 1 | 0 | 0 |
| u | no | 1 | 1 | 0 | 0 |
| ut | yes | 0 | 14 | 1,1 | 1/14 |
| ututtt | yes | 1 | 138 | 6,15,6,6,15,6 | 1/23 or5/46 |
| ttututt | yes | 1 | 364 | 29,29,29,29,29,29,29 | 29/364 |

For ututtt, gcd(p,m)=gcd(6,69)=3, and the three residue classes
of phases have totals 6,15,6. For ttututt, gcd(7,364)=7 permits
seven different means, but the named certificate has equal means.
The theorem limits how many distinct means there CAN be; it does
not assert that this maximum is attained.

No named admissible mean reaches one. This closes these controls as
countermodels to a uniform subunit slope, without proving that slope
on any broader family. Do not add more periods or comparator words.

The ut row has a separate exact dependency, not a missing general
rationality certificate: `problem1_boundary_sum_periodic_tail_probe.md`
sections 1--3 proves the pure seven-bit tails
X=-7/127 and Y=-123/127 and their F cycle. In particular cyclic
A^2 has values -126/127 and -97/127, and the permitted identity
F(z)=4A^2(z)+3 gives F(X)=Y and F(Y)=X exactly. Thus its onset0,
spatial period7 and all-age slope1/14 are proved by that elementary
cycle, independently of any finite score replay here.

## 6. Refuted averaging and bounded-increment simplifications

Status: `refuted` for a single phase-independent asymptotic slope even
on every admissible periodic schedule. For q=ututtt and ANY fixed
starting phase j, equations (5)--(6) give

    liminf_(s->infinity) Psi_s(X_j)/s = 1/23,
    limsup_(s->infinity) Psi_s(X_j)/s = 5/46.        (11)

Each ending phase occurs along an infinite arithmetic progression
of ages. Its bounded offset in (6) vanishes upon division by s.
The two unequal phase slopes therefore prove (11); no fitted trend
or finite-to-infinite step is used. In particular the all-phase average
3/46 cannot satisfy `Psi_s=(3/46)*s+O(1)` at every age, and there is
no single scalar alpha with `Psi_s=alpha*s+O(1)` on this one schedule.

Status: `refuted` for uniformly bounded one-step increments of this
boundary functional on admissible periodic schedules. For starting
phase j=0 and s=2+138v, put Delta_s=Psi_(s+1)-Psi_s. Ending phase
0 advances to phase1, so (5) gives exactly

    Delta_(s+138)=Delta_s+(15-6)=Delta_s+9.          (12)

For s=3+138v the change is instead 6-15=-9. Thus both positive and
negative one-step changes are unbounded. Nonnegativity and the local
bound J<=2 do NOT bound a horizon increment: changing s also changes
the earlier arguments and ending phase throughout the sum.

These are statements about the finite boundary functional of actual
admissible branch prefixes, represented here by a 2-adic periodic
survivor. At every finite tested horizon a sufficiently precise
nonnegative integer has exactly the same observed prefix and cost.
It is not asserted to be an ordinary frontier endpoint. The result
does not refute a uniform upper bound using the MAXIMUM phase slope,
nor the critical age-versus-original-length restriction.

## 7. No finite-state additive approximation of this functional

Status: `refuted` for the following EXACTLY SPECIFIED representation
class, including approximation with sublinear error.

A deterministic finite-state additive reader starts at one fixed state,
reads the observed branch word left to right, assigns a fixed real
weight to each state/letter transition, and outputs their sum plus a
fixed initial constant and a terminal-state correction. All states,
weights and corrections are fixed independently of word length. Let
V(sigma) denote that output. Fixed-range factor counts, or a fixed
finite automaton supplying successive scalar increments, are included.

There is no such reader with

    V(q_0...q_s)=Psi_s(X)+o(s)

on every admissible observed word. The ONE periodic schedule
q=(ututtt)^infinity already refutes it. Pair the reader state with
the input phase modulo6. This is a deterministic map on a finite set,
so its trajectory has a finite transient and a periodic cycle. Its
transition-weight sum is therefore alpha*s+O(1) for one real alpha.
The terminal correction is bounded and does not change this conclusion.
Equation (11) gives two different limiting ratios for Psi_s, making
sublinear approximation impossible.

More quantitatively, on this fixed schedule every such reader has

    limsup |Psi_s(X)-V(q_0...q_s)|/s >= 3/92.        (13)

Indeed its single limiting slope alpha must be at distance at least
half of `5/46-1/23=3/46` from one of the two subsequential slopes.
Uniform bounded error and exact representation are special cases.
Independently, the unbounded increments (12) refute bounded-error
representation directly, since a finite reader has bounded append
increments and a bounded approximation error cannot change that fact.

This no-go concerns REPRESENTING Psi or approximating it with
sublinear two-sided error. It does NOT exclude a finite-state
additive UPPER BOUND on Psi, state-dependent multiplication by an
unbounded length counter, nonlinear updates of unbounded registers,
or ordinary-history potentials on a restricted return domain.
In particular it is not an extension of the previous ordinary-prefix
residue-potential no-go to all finite automata on history words.
A deterministic additive reader of the REVERSED schedule is also
outside the stated left-to-right class.

## 8. Verification and provenance

Round 2 update (2026-09-06): a fresh bounded Muse adversarial review
ACCEPTED Section7 in its stated scope, including the periodic reader's
single slope, the two phase slopes, the 3/92 error bound and the separate
bounded-increment argument. It used Sections1--6 and the stored ututtt
certificate dependencies. The initial provider429 was followed by one
successful delayed retry. This closes the missing Section7 review below;
it is not a review of the entire older all-memory proof. Exact verdict,
reviewed source snapshot and provenance are archived in
`results/problem1/20260906_round2_additive_review.json`.

Status: `finite-exhaustive` for the declared checks. Muse implemented
the modular-fraction calculation and a vector replay. The lead wrote
a separate direct cell-vector implementation and independently reviewed
the contributed code before integration. Complete score-period and
low-prefix hashes agree on all five controls, not merely the totals.
The primary records3440 age-increment checks. The independent record
has6812 score-period checks,3423 age-increment checks and81 direct
forward-boundary checks. The larger common period remains364;
neither old rational cycle is regenerated or enlarged.

A separate literal nonnegative replay uses the SAME ututtt rational
certificate truncated modulo2^288, the precision required by its
largest named age142. It executes143 actual admissible branches and
independently verifies both F=Q A and F=4A^2+3. The six boundary values
are Psi_2=Psi_3=Psi_4=0, Psi_140=6, Psi_141=15, Psi_142=6.
The initial integer has287 bits; its exact value and orbit hash are
retained. This is one specified precision/control, not a search or
an assertion of ordinary-frontier membership.

Atomic records in `results/problem1/` are
`20260906_periodic_boundary_growth_{primary,independent,verification}.json`.
Executable sources are
`experiments/problem1_nonperiodicity/check_periodic_boundary_growth.py`
and `check_periodic_boundary_growth_independent.py` in the same directory.
The verification record embeds its complete comparison/literal-replay
source. The records retain exact inputs, admission snapshots, full base
Git, source hashes, software/hardware, timings and limitations.
Lead integration corrected the primary's proof-dependency wording:
the all-age law follows from rational-tail periodicity and index
reversal, not from the head/cylinder lemmas alone. It also clarified
that the primary was executed by the local Muse worker.

Fresh Muse review accepted the structural identities, phase-class bound,
offsets, coarse-method limitation and oscillation/increment deductions.
Its ut-dependency objection is resolved by the already reviewed exact
cycle now linked in section5. Its corollary followup and one delayed
retry returnedprovider429. The prescribed MiMo fallback returned no
verdict before the maintenance checkpoint and was closed. Section7's
new additive-reader corollary is lead-derived and lead-checked; its
fresh external check is still missing. The exact review disposition is
`results/problem1/20260906_periodic_boundary_growth_review.json`.
No missing check is counted as a successful review.

The next proof must retain ending phase and genuine correlations in
the early boundary terms. Phase averaging and a bounded additive
left-to-right computation of Psi are closed in the stated senses.
Finite-state upper bounds, reversed readers, and unbounded nonlinear
history information are not excluded. No new comparator/width search
is justified by the named slopes; the uniform subunit inequality,
general return boundary exclusion and whole-tail conjecture remain open.
