# Terminal-branch perturbations of the exact boundary functional

Status: `partial-proof` for the exact perturbation and locality identities;
`refuted` for the specified bounded-edit and zero-density stability
claims; `finite-exhaustive` for the named controls. The scoped external
review and lead corrections are recorded below. This concerns auxiliary observed schedules, not ordinary-frontier
membership. Problem 1 and the whole-tail question remain open.

## Admission and ranked routes (before computation)

The current bottleneck is control of the early terms of Psi when an
alternating observed history has interruptions. Rank: (1) derive the exact
effect of ONE changed final observed branch; (2) bound cost by the number
of interruptions; (3) construct an ordered-history upper bound. Route 1
has an all-age finite perturbation state derived below, and can falsify
route 2 before an unsupported bounded-error argument is attempted.

Test ONLY the already proved two phases of the ut survivor and, if needed,
the stored ututtt and ttututt phase certificates. For each ending phase
which allows flipping the final letter while preserving the three known
finite-word exclusions, evaluate the one-bit defect recurrence for two
full periods of its periodic driver. A nonzero mean score difference
refutes a uniform bounded cost per changed branch, using one edit at
arbitrarily large ages. Zero mean on the named controls closes only this
specific falsification class; it neither proves a general stability bound
nor authorizes more comparator words or larger periods.

The finite-state assertion here applies ONLY to the two highest bits of
a perturbation above an unchanged lower prefix. It is derived from the
all-bit formula for F before any finite calculation. It is not a finite
state quotient of arbitrary forced histories or a search for one.

Hand-check the Boolean derivative and the first ut age with an admissible
last-letter change. Compare packed arithmetic with independently written
cell-array forward evolution on the named cylinders; then verify exact
driver/defect cycle closure. No ordinary frontier, return occurrence,
core, coefficient, first-witness or periodic-survivor census is run.
Local one CPU, 120 seconds and 1 GiB per implementation. Atomic result
records must retain full base Git, exact source and input/admission
snapshots, hashes, hardware/software facts, timings and limitations.

## 1. All-bit perturbation identity (`partial-proof`)

Retain A(x)=(x>>2) XOR((x>>1) OR x), pi=x>>2,
I(z)=1 for z=0 or5 modulo64, J(y)=I(A(y))+I(pi(y)), and permitted
F(x)=4A^2(x)+3. For i>=2,

    F(x)_i = x_(i+2) XOR H(x_(i+1),x_i,x_(i-1),x_(i-2)),
    H(a,b,c,d)=(a OR b)
        XOR ((a XOR(b OR c)) OR (b XOR(c OR d))).

The Boolean derivative of H in a is c OR d: the derivatives of its
two terms are NOT b and NOT(b XOR(c OR d)), whose XOR is c OR d.

Fix s>=2. For a finite actual prefix of s+1 branches, its cylinder precision is
2s+4. Put b_t=2s+2-2t. Change only input bits b_0,b_0+1 by XOR
(1,epsilon_0). At time t the first change is still at b_t with value1,
and the next changed bit is epsilon_t, where

    epsilon_(t+1)=epsilon_t XOR (x_t[b_t-2] OR x_t[b_t-3]).

For t<s, b_t>=4, so the first s gates are unchanged. The last gate at
t=s changes u to t or t to u precisely when epsilon_s=1. This determines
epsilon_0 uniquely. At t=s-1 the displayed OR equals1, since every
permitted endpoint has bit1=1, so epsilon_(s-1)=0.

Reverse the boundary index: d=s-t-2, y_d=pi^d(x_(s-2-d)), and put
epsilon_(-1)=0. Rename the reversed epsilon by eta to avoid conflating
the increasing time t with increasing projection depth d. The exact
last-letter change is

    eta_(-1)=0,
    eta_d=eta_(d-1) XOR (y_d[4] OR y_d[3]),
    Psi_s(changed)-Psi_s(original)
      =sum_(d=0..s-2) [J(y_d XOR64 XOR(128*eta_d))-J(y_d)].  (1)

Proof of the precision statements. Induct on t using the displayed
all-bit F formula. Bits below b_t agree. The output at b_t-2 toggles
by1 because its lower Boolean term is unchanged. At b_t-1, only the
first argument of H and the leading input bit can change; its derivative
therefore gives the epsilon recurrence. Unspecified higher bits cannot
affect these outputs. For t<s, unchanged low four bits guarantee the
same actual gate, so use of F remains valid. At t=s, the low pair still
agrees and is11. Changing its gate pair from01 to10, or from10 to01,
requires exactly epsilon_s=1. Back substitution gives one and only one
choice of the initial two-bit change. This is the unique other final
branch cylinder with the first s branches unchanged. It need not satisfy
the finite-word language filter; that is checked separately below.

For a boundary summand, the projection removes b_t-6 bits. Thus its
low eight input bits change precisely at positions6 and7 by (1,eta_d).
The epsilon recurrence in reverse order starts at epsilon_(s-1)=0;
its driver becomes y_d[4] OR y_d[3]. Summing the changed local scores
proves (1). The low-eight-bit interpretation is intended in (1); higher
bits of the two projected integers may differ and J ignores them.

## 2. Periodic driver, including its defect state (`partial-proof`)

On a phase-j survivor of a period-p schedule, put e=j+s-2 modulo p.
Then y_d=pi^d(X_(e-d)). The already proved common spatial onset a and
period lambda give d0=ceil(a/2) and L=lcm(p,lambda/gcd(lambda,2)).
The entire low-eight-bit driver is L-periodic for d>=d0, not merely J.

Let P_e be the XOR of y_d[4] OR y_d[3] over one driver period. Iterating
the one-bit recurrence gives eta_(d+L)=eta_d XOR P_e for d>=d0.
Therefore the PAIR consisting of the driver and defect state repeats
after L if P_e=0 and after 2L in all cases. A finite cycle check is
complete for this derived state; it does not claim bounded memory of
the original branch-to-survivor map.

The score difference in (1) is thus eventually periodic in d. Increasing
the age by a full joint period keeps e fixed and adds its exact integer
total to the cost difference, for every s>=d0+1. Finite low-prefix
offsets must be retained, exactly as in the original periodic-growth
theorem. This proves all-age progressions from a checked driver period.

## 3. Exact controls and one-edit instability

Status: `finite-exhaustive` for the finite driver tables below. Only ut
and the already stored ututtt certificate were used; the test stopped
at the first nonzero control. No ttututt calculation was needed.

| base schedule | ending e | d0 | driver L | driver parity | joint period | base total | changed total |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ut | 0 | 0 | 14 | 1 | 28 | 2 | 2 |
| ututtt | 0 | 1 | 138 | 0 | 138 | 6 | 15 |
| ututtt | 2 | 1 | 138 | 0 | 138 | 6 | 9 |
| ututtt | 4 | 1 | 138 | 0 | 138 | 15 | 0 |

The other ending phases fail the final-letter language filter. The
ending phase e concerns the last boundary summand; the changed branch
is phase e+2 modulo p. For ututtt at e=0 its last six observed letters
change tttutu to tttutt; for e=2, tututt to tututu; for e=4, tutttu to
tutttt. All three changed finite words avoid uu, ttttt and ututtu.
All their earlier factors are unchanged. The small initial horizons
are checked directly; for e=0, age2 changes utu to utt.

Status: `partial-proof` for the all-age consequences, and `refuted` for
bounded cost per changed branch. Let v>=0 and s=2+138v. Start at phase0
of (ututtt)^infinity and let sigma_v be its first s+1 observed letters.
Let sigma'_v differ ONLY in its last letter, which changes u to t.
Both are admissible finite observed words and have nonnegative integer
representatives in their exact cylinders. The latter fact makes no
ordinary-frontier assertion. From the e=0 table, the initial age2
values0,0, and Section2,

    Psi_s(sigma_v)=6v,
    Psi_s(sigma'_v)=15v,
    Psi_s(sigma'_v)-Psi_s(sigma_v)=9v.               (2)

Here Psi_s(sigma) means the schedule-determined functional on any
representative of its length-(s+1) cylinder. In particular,

    no constant C satisfies
    Psi_s(tau) <= Psi_s(sigma) + C*d_H(tau,sigma)     (3)

uniformly on admissible equal-length words, even when sigma is always
a prefix of this ONE fixed periodic comparator. In (2), d_H=1 while
9v is unbounded. A uniform two-sided bounded-edit estimate fails too.
This is a positive cost increase, not just a negative variation.

The same control has changed slope15/138=5/46. It does not exceed the
maximum phase slope of the original comparator, so a max-phase upper
bound is NOT refuted by this control. Nor is a bound on ordinary histories established
or disproved without the original-length and membership hypotheses.
The separate r=2 seam in `problem1_finite_suffix_defect_transfer.md`
does refute preserving the ut comparator's own maximum phase slope
under a finite edit; it still does not refute a larger uniform subunit
upper bound on arbitrary schedules.

## 4. A single zero-density interruption schedule (`partial-proof`)

The finite family (2) already refutes (3). One can also refute the
claim that a single infinite admissible schedule with zero-density
changes from a periodic comparator must have Psi difference o(s).
No new numerical inputs or periodic-survivor certificates are needed.

First, an exact locality bound: if two observed words of length s+1
agree from position h onward, where 0<=h<=s-1, then

    |Psi_s(tau)-Psi_s(sigma)| <= 2h.                 (4)

Use the established exact split into the first h boundary terms and
Psi_(s-h) of the suffix. Equal observed suffixes have s-h+1 letters,
which supply the full needed precision for that suffix functional.
The suffix costs are equal, and each initial partial sum lies in
[0,2h]. This proves (4) on finite observed words, without a choice of
ordinary representative or an unobserved gate.

Let q=(ututtt)^infinity, v_n=2^(2^n), s_n=2+138v_n for n>=1. Form
one infinite q' by changing q_(s_n) from u to t and q_(s_n+2) from
t to u for every n. The pairs of edits are disjoint and widely spaced.
Each pair reverses neighboring u-return gaps (2,4) to (4,2); every gap
of q' remains2 or4. Hence q' avoids all three forbidden factors.
The second edit is essential to the infinite admissibility argument:
the first edit alone, followed by the unchanged periodic continuation,
would create a forbidden ttttt later. No unobserved repair is used to
justify any gate in a finite prefix.

Only two letters per edit pair differ from q, so their density is zero
(the number up to s_n+2 is exactly2n, and s_n grows faster than n).
At age s_n, the repair at s_n+2 is outside the observed prefix. Compare
q'[0:s_n+1] with the one-terminal-flip word sigma'_v_n in (2). Their
earlier differences are all before h_n=s_(n-1)+3 for n>=2. They agree
from h_n through the final branch. By (4),

    |Psi_(s_n)(q')-15v_n| <= 2h_n.

Since h_n/s_n tends to zero, (2) gives the exact subsequential limit

    (Psi_(s_n)(q')-Psi_(s_n)(q))/s_n -> 3/46.        (5)

Status: `refuted` for zero-density Hamming stability of this boundary
functional, including a one-sided o(s) upper error relative to q.
Allowing a fixed additive constant depending on this one q' does not
repair (5). This is not a claim about all sublinear-error bounds, nor
an ordinary finite-survivor counterexample. Indeed q' has arbitrarily
long period6 factors with unbounded repetition excess; the existing
finite-schedule repetition theorem already proves its survivor is not
an ordinary finite integer. Its role here is a cost-stability obstruction.

## 5. Verification status and remaining obligation

Independent direct cell evolution checks both actual cylinders, all
observed gates, exact Psi values, and every moving two-bit difference
at the declared finite ages. The cell implementation solves the two
high input bits by four explicit lifts, independently of the defect
formula used for the period calculation. The corrected primary modular
calculation matches all442 complete period rows and three low-prefix
rows, not just their totals. There are13 direct cell cylinder replays,
78 modular-versus-long-division checks,16 Boolean derivative checks,
and128 checks of the two bulk boundary bit equations. The hand age2
inputs135 and199 have words utu and utt and cost0 in each case.
No infinite implication is inferred merely from the finite literal ages.

The initial worker implementation omitted the low-prefix parity at
ending e4 and compared unlike phases for closure. Its totals happened
to agree despite a wrong vector. Lead review required both corrections;
the corrected two-period fields and independent cell vectors agree.
Lead integration also supplied missing protocol metadata and exact
source/admission snapshots, despite the worker's mistaken claim that
all such fields were already present. The immutable reference is unchanged.

After Muse failed on the primary task and on one delayed retry, the
prescribed MiMo fallback completed the modular calculation and accepted
Sections1--4 in an adversarial pass. Its prose miswrote the forbidden
word ututtu; the lead checked the correct gap pattern2,3, which the
constructed gap set2,4 excludes. This does not change the source proof.
Its finite-representative domain and the separately cited repetition
theorem for the infinite constructed schedule remain explicit.

Atomic records are `20260906_terminal_branch_sensitivity_`
`{primary,independent,verification}.json` in `results/problem1/`.
The verification archive retains the supplied pre-correction worker
record, corrected raw source/record, reviewed-note snapshots, exact
lead corrections and mathematical review content. Executables are
`check_terminal_branch_sensitivity_{primary,independent}.py` in
`experiments/problem1_nonperiodicity/`. The all-r transfer proof has
its own separate verification and review scope.

The interrupted-history upper-bound route must retain where changes
occur and how they affect the early boundary terms. Counting changes,
or using zero asymptotic change density alone, does not transfer the
phase-specific comparator cost with bounded or sublinear upper error.
General subunit bounds and bounds retaining actual ordinary membership
remain open. No further comparator or suffix-width sweep is admitted.
