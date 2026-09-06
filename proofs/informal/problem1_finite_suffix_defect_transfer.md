# Exact transfer for a fixed terminal replacement width

Status: `partial-proof`, lead-derived and lead-checked; a usable complete
external review of the all-r theorem is still missing. See Section6.
This is a structural reduction for the boundary functional on periodic
comparators with a fixed finite terminal replacement. It does not provide
a uniform bound as that replacement width grows, an ordinary-frontier
criterion, or a solution of Problem 1.

## Admission and purpose

The single-terminal-letter calculation proved that bounded cost per edit
fails even at a fixed periodic comparator. The useful surviving question
is which state must be retained to compute that edit's effect. Generalize
the derived highest-two-bit defect to a FIXED suffix of r letters, proving
the state bound before considering any graph. An exact finite transfer
would turn each specified fixed-width replacement into an all-age
calculation; a failure would prevent treating this as a closed state.

This unit begins as a proof, with no suffix-width
sweep, periodic comparator, rational cycle, or frontier computation.
The r=1 calculation already checked in the terminal-sensitivity note is
the consistency specialization. Do not increase r computationally merely
because the state bound below is proved: a new discriminating mathematical
hypothesis and admission would still be required.

Subsequent verification admission (before execution): the r=2 and r=3
seams introduce respectively the first boundary transfer at d=0 and
the first nonempty terminal boundary contribution. Check ONLY these two
seams on the already proved ut comparator: tau=tt at r=2, ages3 and115;
tau=ttu at r=3, ages4 and452. The larger age in each pair is the smaller
age plus its sufficient K from (3). Compare a backward w-bit transfer
with full inverse-generator cylinder construction followed by actual
cell-array F evolution, checking every branch and the exact scores.
This is falsification of the claimed finite state and index seams,
not a search for an upper slope or more suffixes. A mismatch invalidates
the claimed closure or threshold; agreement is finite verification only
and leaves the all-r theorem dependent on its derivation. Stop after
the four fixed cases, whether they agree or fail. One local CPU,
120seconds and1GiB, exact parameters and atomic full provenance.

## 1. Moving finite defect (`partial-proof`)

Fix an infinite periodic branch word q of period p, its phase-j survivor
X_j, and the common proved spatial onset a and period lambda. Fix r>=1
and a word tau of length r over {t,u}. At each age s>=r, form the observed
word of length s+1 which follows the comparator for n=s+1-r branches
and then uses tau for its last r branches. Denote its boundary functional
by Psi_s^tau. Every finite branch word has its exact survivor cylinder;
language admissibility of the changed word is a separate condition.

Set w=2r. The common n-branch prefix fixes the low B_0=2n+2 input
bits. At total precision 2s+4=B_0+w, the difference between the two
cylinders is a w-bit XOR word delta_0 beginning at B_0. It may have
leading zero bits; no assumption that tau first differs immediately
is made. After t common-prefix updates put

    B_t=2(n-t)+2,    0<=t<=n.

The actual low B_t bits still agree. The next w bits have a defect
delta_t, and higher differences do not affect them. At t=n, the low
pair is11 and the w bits above it are determined exactly by the r-branch
cylinder of tau versus the comparator's phase-(j+n) cylinder. Thus
delta_n is a finite terminal datum. Along an arithmetic progression of
s with fixed e=j+s-2 modulo p, this datum is fixed: the comparator's
terminal phase is j+n=e+3-r modulo p.

For 0<=t<n, use the proved all-bit identity, valid at i>=2,

    F(x)_i=x_(i+2) XOR H(x_(i+1),x_i,x_(i-1),x_(i-2)).

At output i=B_t-2+l, the leading input difference is delta_t[l];
the H difference involves only lower defect coordinates. Consequently
the exact update has the unit-triangular form

    delta_(t+1)[l] = delta_t[l]
                       XOR f_(t,l)(delta_t[0],...,delta_t[l-1]),
    delta_(t+1)[0] = delta_t[0],                    (1)

for 0<=l<w. The coefficients are determined by the comparator bits
at B_t-4,...,B_t+w-1, a window of w+4 bits. This includes every bit
used in H and the original output used to form the XOR difference.
The minimum index is nonnegative since B_t>=4 for t<n.
This is a window in the KNOWN comparator, not a window lying entirely
in the common prefix. Its part at or above B_t can change, and those
changes are precisely the retained delta coordinates. Agreement is
asserted only below B_t.

Equation (1) is a bijection of the w-bit defect words: recover bits
successively from low to high. Its inverse is unit-triangular too and
fixes coordinate0. The first n gates remain the comparator's gates,
because they are below B_t>=4. Hence neither the forward derivation
nor its inverse assumes unobserved continuation.

## 2. A dyadic bound for the composed transfer (`partial-proof`)

Every permutation U of w-bit words with

    U(z)_0=z_0,
    U(z)_l=z_l XOR f_l(z_0,...,z_(l-1)), l>=1,

has order dividing 2^(w-1). Here order means a sufficient exponent
giving the identity on ALL w-bit words, not just a selected orbit.

Proof by induction on w. For w=1, U is the identity. At width w>1,
the projection to w-1 bits has exponent dividing 2^(w-2). Raising U
to that exponent fixes all lower w-1 bits and can only toggle the
last bit by a function of those fixed bits. Applying this resulting
map twice is the identity. Thus U^(2^(w-1)) is the identity. Composition
and inversion preserve the displayed form, so the bound applies to
any finite composition of the forward or backward updates in (1).
No general permutation-order or unproved finite-state assertion is used.

## 3. Reversing the boundary and exact all-age growth (`partial-proof`)

Use d=s-t-2 and e=j+s-2 modulo p. For a common-prefix time t<n,
the lowest comparator bit driving (1) has spatial index

    B_t-4 = 2(d-r+2),

and comparator phase j+t=e-d modulo p. The driver therefore has
period L=lcm(p,lambda/gcd(lambda,2)) in d once this window lies in
the periodic spatial tail. The local boundary score also needs the
comparator bits at 2d,...,2d+7. A sufficient common onset is

    D=ceil(a/2)+max(r-2,0).                          (2)

The suffix times t>=n contribute at most max(r-2,0) boundary terms.
Their exact values, and the finitely many common-prefix terms at d<D,
are determined by the fixed ending phase e and tau. They are bounded
offsets independent of the age along this ending phase.
For r>=2, the suffix sum is exactly Psi_(r-1) of the r-letter word
tau; for r=1 it is empty. The driver requires
d>=r-2+ceil(a/2), while J requires d>=ceil(a/2). Their maximum is
exactly (2). These are two different lowest-bit conditions.

For r=1, the backward transfer also uses the common-prefix time
t=s-1 (d=-1), which is not a boundary summand. Its sole role is to
set the initial defect for d=0. This is exactly eta_(-1)=0 after
undoing the last-gate change in the single-letter note. For r>=2,
the first backward common-prefix time is d=r-2. These initial
transfers are finite and independent of s at fixed e.

At every d>=D, a w-bit defect state is updated by a known periodic
sequence of inverse unit-triangular maps. Over one driver period L,
their composition has order dividing 2^(w-1), by Section2. Thus the
combined driver and defect repeat with a sufficient period

    K=2^(2r-1)*L.                                  (3)

There is no defect transient after the driver's onset: the period
composition is a permutation. The claimed bound is sufficient, often
far from minimal, and does not grow with s for FIXED r and comparator.

For completeness, the changed J term is determined by this state.
Its input window starts at 2d, while the defect starts at
B_t=2d+8-2r. Any part of the J window below B_t is unchanged; any part
at or above B_t lies within the retained w coordinates, since its
highest position is B_t+w-1=2d+7. Thus no additional defect bits are
silently discarded in evaluating J. This proves closure for the score,
not merely for a projection of the orbit.
More explicitly, for r<=4 the J window begins below or at B_t,
and for r>=4 it is wholly contained in the defect window. In the
latter case it uses defect coordinates2r-8,...,2r-1. At r=5, for
example, the defect starts at2d-2, below J; its lowest two coordinates
are still needed in the transfer, although they do not directly enter
that time's J score. No assertion that B_t>=2d at every r is made.

Let M_e^tau be the integer sum of the changed local boundary scores
over a full such period beginning at d=D. For every

    s>=max(2,r,D+1),

with the stated ending phase and terminal replacement,

    Psi_(s+K)^tau - Psi_s^tau = M_e^tau.            (4)

Increasing s by K preserves e because p divides K. It preserves all
finite terminal data and early offsets. The s-1 boundary terms gain
exactly K terms in the established periodic region, proving (4).
Original and changed words refer to the same fixed tau repositioned
at the end of each longer periodic prefix; they are not asserted to
be nested prefixes of one infinite changed schedule.

The sum divided by K is therefore an exact rational phase slope for
this fixed terminal-replacement family. Subtracting the comparator's
known score period gives the corresponding exact slope of the cost
difference. At r=1, (3) gives 2L, the sufficient period derived in the
terminal-sensitivity note; its parity test sometimes reduces that to L.

## 4. Fixed seam verification and a sharper obstruction

Status: `finite-exhaustive` for precisely these four declared inputs.
The backward packed finite defect agrees with independent full
inverse-generator cylinder construction and actual cell-array evolution:

| r | tau | age s | comparator Psi | changed Psi |
| --- | --- | --- | --- | --- |
| 2 | tt | 3 | 0 | 0 |
| 2 | tt | 115 | 8 | 12 |
| 3 | ttu | 4 | 0 | 1 |
| 3 | ttu | 452 | 32 | 53 |

The complete defect closes at K112 and K448 respectively, and every
retained score/driver row after K agrees with its predecessor. The
full moving driver, defect, and two score entries agree on all568 rows
against the actual cell histories, including agreement of every lower
common-prefix bit. This is stronger than agreement of four total costs. The
terminal summand at r=3 exists but has value0 on this chosen input;
this finite check does not by itself show why that term is necessary
on all inputs. Its presence and index follow from Section3. No suffix
other than the two declared seam controls was tested.

Status: `partial-proof` for the all-age identities, `refuted` for
transferring a periodic comparator's maximum phase slope with bounded
or sublinear edit error. Section3 and the r=2 closed state give, for
every v>=0 and s=3+112v,

    Psi_s((ut)^infinity)=8v,
    Psi_s(last two letters replaced by tt)=12v.      (5)

The changed word differs in just its PENULTIMATE observed letter:
the u at h=s-1 becomes t, while the last t is unchanged. Its prefix
is admissible. More strongly, keeping the whole subsequent alternating
continuation removes just that one u and changes neighboring return
gaps2,2 into one gap4. This infinite extension still has only gaps2,4.

The two NAMED all-age corollaries can also be certified directly from
their closed defect cycles, without the general dyadic exponent bound.
On the known pure7-periodic comparator, the local inverse transfer is
deterministic on respectively four or six defect bits and a period14
driver position. The recorded first K transfers return that exact state
and driver position, with every score matched against full cell histories.
Determinism repeats the same cycle indefinitely. Adding its score sum
therefore gives (5) and the r=3 law below at every further K-step age.
This uses a closed sufficient state, not merely two matching cost totals.

The comparator has the SAME slope1/14 in both phases. The changed
family has slope3/28>1/14. Thus replacing a fixed finite suffix cannot
in general preserve even the comparator's MAXIMUM phase slope with
an O(1), or o(s), upper error. This is stronger than the ututtt
single-final-letter example, whose changed slope stayed within that
comparator's phase maximum. It still supplies no slope reaching1 and
does not refute a larger uniform subunit upper bound.

The r=3 seam likewise gives exact values

    s=4+448v: comparator Psi=32v,
                changed Psi=1+52v,

with changed slope13/112. This is one declared verification control,
not grounds for extending the suffix-width test.

One fixed infinite counterexample to zero-density stability can now
use ONLY the phase-independent ut comparator. Set v_n=2^(2^n),
h_n=2+112v_n, and delete the u at each h_n (replace it by t), with
every other branch unchanged. Call the resulting schedule q'. All
return gaps remain2 or4, and the edit density is zero. At ages
s_n=h_n+1, its observed word differs from the single-edit word in
(5) only before h_(n-1)+1. The exact prefix-locality bound (4) in
the terminal-sensitivity note therefore yields

    |Psi_(s_n)(q')-12v_n| <= 2(h_(n-1)+1), n>=2,
    [Psi_(s_n)(q')-Psi_(s_n)((ut)^infinity)]/s_n
          -> 1/28.                                 (6)

This counterexample does not depend on phase oscillation of the
comparator. Its arbitrarily long alternating factors satisfy the
existing unbounded repetition-excess criterion, so its survivor is
already excluded from ordinary finite integers. It is a stability
counterexample on admissible schedules, not a whole-tail counterexample.

Records: `results/problem1/20260906_finite_suffix_defect_seams.json`,
with complete executed and dependency sources, exact inputs and admission,
full Git, local hardware/software facts, timings, hashes and atomic write.
Executable: `experiments/problem1_nonperiodicity/check_finite_suffix_defect_seams.py`.
Both formulations are lead-local; external proof review is separate.

## 5. Scope and the remaining uniformity gap

This is a finite transfer for a FIXED number of final replaced letters
over a fixed periodic comparator. Its state is an actual perturbation
of one prescribed cylinder, transported through each actual common
gate. It does not splice states from different ordinary histories or
claim a finite-state branch-to-survivor map.

The state width w, period bound K, offsets, and slopes may all depend
on r and the comparator. Letting r grow with s loses the fixed-state
conclusion; (3) supplies no subunit slope uniform in that limit.
Even bounds below1 for every separately checked r would need a uniform
margin and uniform offset control to support a whole-tail argument.
The single-edit counterexample shows why an additional positive bound
must be proved, rather than inferred from the small size of the edit.

For an ordinary finite input of original complexity k, its unchanged
periodic prefix already obeys the older repetition theorem:
n=s+1-r<=k+2p-2, hence s<=k+r+2p-3. This restriction is reused from
`problem1_finite_schedule_repetition_bound.md`, not a new exclusion
deduced from (4). The transfer is useful here for falsifying cost
stability; further fixed-suffix calculations do not by themselves
control arbitrary interruptions on the actual near-boundary domain.

No graph or numerical width extension is authorized by this reduction
alone. The critical next question remains a proved upper inequality on
actual ordinary histories with original length and all observed gates
retained, or another observable that controls their ordered information.

## 6. External review disposition

Muse failed on the fresh all-r review request and its single delayed
retry. The prescribed MiMo fallback supplied an initial verdict and
one targeted correction. The lead rejected BOTH as complete all-r
verification; no full external acceptance is claimed.

The initial review incorrectly placed the whole comparator window
inside the common prefix and the defect inside J at every r, and
conflated the driver's lowest bit with J's. Its correction repaired
parts of that geometry but introduced the wrong terminal phase
e-r+1. The correct phase is j+n=e+3-r, as stated in Section1.
The two expressions happen to agree modulo2 on the named ut controls,
so those controls could not detect that all-p error. The correction
also listed the wrong arguments of H: the leading x_(i+2) is separate;
H uses i+1,i,i-1,i-2. Its phrasing about reading J from defect bits
must retain XOR with the known comparator, not replace absolute bits
by differences. These are errors in the review, not adopted changes
to the source theorem.

The source now expands these exact points explicitly. The independent
named finite computations remain accepted. The review's bounded checks
of the named slopes, gap admissibility and sparse-edit limit were sound,
but they are not counted as a full review of the general transfer.
The old unrelated all-memory proof review also remains missing.

Disposition and provenance are archived in
`results/problem1/20260906_finite_suffix_defect_review.json`.
No new numerical width or comparator run follows from the review failure.
