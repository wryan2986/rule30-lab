# One global spacetime contains all phase-correct cycle representatives

Status: `partial-proof` for the global construction, the infinite initial
right-disagreement result, and the ancestry identities. The proposed
cycle-only zero-extension recursion is `refuted` by a hand certificate.
No FULL survivor or uniform delay bound is obtained. Problem 1 remains
OPEN. Fresh external review is missing. Sections 1-5 use no numerical
experiment; Section 6 has one `finite-exhaustive` check of twelve fixed cases.

## 0. Admission and the fixed original boundary

The current bottleneck requires ONE original finite configuration and its
ENTIRE finite right fringe. Treating successive periodic drivers as separate
objects loses that requirement. Test whether their phase-correct cycle
representatives are the cuts of one genuine Rule 30 spacetime. If they are,
the source of cycle defects can be studied in a single coupled evolution;
if not, a global shadow argument is invalid. This is an all-depth structural
question, not a source or prefix search.

The phase-fork note has already refuted selecting one universal cycle from
finite support and a clock. The reset-anchoring note has shown that the
erasing 1 needs global transport to the original Q budget. This note instead
retains the complete history in a compatible family of cycle representatives.
It does NOT replace the actual fringe by the shadow fringe when asserting
FULL. The shadow is a second, explicitly different initial row.

For a finite-entry hypothesis one may first make the single even physical
rebase justified in `problem1_reset_anchoring_geometry.md` Section 3. The
actual row and the actual right fringe are then both finite. The construction
below applies at that fixed origin. No later reinitialization is used.

## 1. Compatible cuts define a whole row (`partial-proof`)

Write U for the physical Rule 30 map,

    (Ur)_i = r_(i-1) XOR (r_i OR r_(i+1)).

Work on the domain of binary rows r indexed by ALL integers which are zero
sufficiently far to the LEFT. The right half may be arbitrary. For each
integer j, encode the initial left half ending at j by the finite integer

    L_j(r) = sum_(i<=j) r_i 2^(j-i).

Every such integer has a finite A-orbit, where
A(y)=(y>>2) XOR ((y>>1) OR y). The two exact cut identities are

    sigma L_(j+1)(r)=L_j(r),
    L_j(Ur)=A L_(j+1)(r).                           (1)

The second follows bit by bit: output bit d reads input bits d+2,d+1,d
of the cut at j+1. This derivation includes the cell just to the right of
j, and therefore does not impose an artificial right boundary.

Put C_j=cyc(L_j(r)), using the phase-correct completion, not first entry
onto the cycle. The imported commutation of cyc with sigma gives

    sigma C_(j+1)=C_j.                              (2)

Hence there is a UNIQUE full binary row E(r) whose cut at every j is C_j.
Explicitly E(r)_j=bit_0(C_j); iterating (2) recovers every higher bit of
C_j from the earlier C_i. All sufficiently far-left cuts of r are zero,
so the same is true of E(r). This constructs the row by compatible finite
cuts; it is not a limit that selects new phases independently at each depth.

The construction is defined on the entire stated left-zero domain, including
its generally infinite right halves. Since all cuts of E(r) are cyclic,

    E(E(r))=E(r).                                   (3)

## 2. This row evolves by the actual Rule 30 rule (`partial-proof`)

Commutation of cyc with A and (1) give for every integer j

    L_j(E(Ur)) = cyc(A L_(j+1)(r))
               = A cyc(L_(j+1)(r))
               = L_j(U(E(r))).

Equality of every cut proves the WHOLE-row identity

    E(Ur)=U(E(r)).                                  (4)

Let r_i(t) be the actual evolution from r, and let hat r_i(t) be the
evolution from E(r). Iterating (4), for every cut and every physical time,

    L_j(hat r(t))=cyc(L_j(r(t))).                    (5)

In particular for the actual center-and-left row Y_t,

    sum_(i>=0) hat r_(-i)(t)2^i=cyc(Y_t).           (6)

A second derivation checks the full initial cones directly:
L_j(r(t))=A^t L_(j+t)(r). The cut of the shadow is
A^t C_(j+t)=cyc(A^t L_(j+t)(r)), proving (5) without induction on E.
The original right symbols through j+t have been retained in both
calculations. They have not been chosen from a later gate or periodic phase.

Thus every cycle defect Y_t XOR cyc(Y_t) is the actual disagreement
between TWO fixed global Rule 30 spacetimes, restricted to positions <=0.
The auxiliary boundary bits in the previous cycle-defect recurrence are
now the physical center of this same shadow evolution. They are still not
the actual center bits, and (4) asserts no global temporal period for E(r).

There is also a limit description with a necessary moving-coordinate fence.
Let S be the physical shift to the right, (Sr)_i=r_(i-1), and B=SU.
Then L_j(B^n r)=A^n L_j(r). Every finite A-cycle has dyadic period by
the one-bit lift theorem starting above its support. For every FIXED cut,
2^k eventually exceeds its onset and is divisible by its period. Hence

    E(r)=lim_(k->infinity) B^(2^k)r
        =lim_(k->infinity) S^(2^k) U^(2^k)r         (6a)

in the topology of agreement on finite physical windows. The cut-wise
argument proves this limit without a uniform onset or period. Since U is
local and commutes with B, (6a) gives another proof of (4).
However the ACTUAL physical center at time 2^k appears at position 2^k
after the shift. It escapes every fixed observation window. Thus even
an infinite FULL premise cannot be passed to a fixed center of E(r)
merely by taking this limit. No such finite-to-infinite inference is made.

## 3. A finite actual row has infinitely many initial right disagreements

Claim (`partial-proof`). Let r be nonzero and finitely supported, with
L_0(r)>0 and r_i=0 for i>R, where R>=0 is any support bound. Then E(r)
has infinitely many 1s to the right of R. Consequently

    {i>R:r_i != E(r)_i}

is infinite. Finite actual support does not make its global cycle-defect
initial condition finite.

Proof. Let L=bitlen(L_0(r)) and p_j be the least A-period of C_j, j>=0.
The actual cut L_j(r) has width L+j. A preserves the positive finite width,
so C_j also has width L+j. There are only finitely many finite cyclic rows
with period at most any fixed P: inject them by Theta into the finite union
of the four-symbol period-p codes, 1<=p<=P. Thus p_j tends to infinity.
One-bit cyclic extension in (2) preserves or doubles the least period.
There are therefore infinitely many doubling indices

    B={j>=0:p_(j+1)=2p_j}.

For j in B, the one-bit lift theorem forces the low A-trace of C_j to be
identically zero. The low trace v_s of C_(j+1) then obeys a permutation
scan with odd parity per input period, and visits both 0 and 1. The code
of C_(j+1) has low/high bits (v_s,0). The next lift's low bit w_s satisfies

    w_(s+1)=v_s OR w_s.

Since C_(j+2) is cyclic and v has recurring 1s, its unique cyclic low
response is w_s=1 for EVERY s. In particular

    E(r)_(j+2)=1 for every j in B.                  (7)

The positions j+2 are distinct and unbounded. Beyond R their actual initial
bits are zero, proving the claim. More quantitatively, for every N,

    #{R<i<=N+1:r_i != E(r)_i}
      >= #{j in B:0<=j<N, j+2>R}.                 (8)

No positive density or rate of clock growth follows. This is an exact
one-disagreement-per-doubling inclusion, not a sampled list of positions.

An independent contradiction check uses the prior zero-extension theorem.
If E(r) were eventually zero to the right, its later cuts would be
2^k times one fixed positive finite cyclic cut. Every cut is cyclic by
construction, giving an entirely cyclic zero-extension tower, which the
highest-wait note excludes. This verifies the infinite-tail conclusion
without relying on the particular locations in (7).

The stronger w_s=1 statement also describes constant-1 moving
characteristics of the SHADOW. It is not a constant actual center trace,
and it supplies no infinite FULL countermodel.

The infinite right-disagreement conclusion holds at EVERY finite physical
time, not only initially. Apply this section to the nonzero finite row
U^t r, and use E(U^t r)=U^t E(r). Both evolutions have the same finite
left-edge position, and the actual right half is still eventually zero.
This is not a claim that one particular initial discrepancy survives forever.
It states that no finite-time rebase makes the GLOBAL discrepancy set finite.
If the center-and-left row happens to be cyclic at a given time, (6) makes
all its discrepancies at positions <=0 vanish, while infinitely many remain
to the right. In particular, under the previous conditional one-bit episode
theorem, return to a cyclic even row does not empty the right-hand supply.

## 4. The true ancestry set for an injection (`partial-proof`)

Let d_i(t)=r_i(t) XOR hat r_i(t). This is disagreement between two actual
Rule 30 evolutions, so if every initial difference in a cell's finite
backward cone is zero, that cell's difference is zero too.

For R_t>0 put T=max(tau_t-1,0). The renewal's actual residual bit is
e_t=bit_0(A^T Y_(t+1)). Its phase-correct counterpart is
bit_0(A^T cyc(Y_(t+1))): its upper projection is the same cyclic q_t,
and the resetting lift has only one cyclic response. Hence (6) gives

    d_(-T)(t+1+T)=1.                               (9)

Finite cones then imply an initial ancestor k with

    -t-1-2T <= k <= t+1,   d_k(0)=1.               (10)

This is the valid initial discrepancy source, not an automatic charge to
an original nonzero bit r_k or to P_n(Y_0,s). Its right half is infinite
by Section 3, even though r itself is finite. One cannot bound its total
capacity by the original anchored Q or the finite actual support.

If the initial center-and-left row is already cyclic, d_k(0)=0 for k<=0;
then (10) necessarily has 1<=k<=t+1. There is no asserted uniqueness or
bounded reuse of such ancestors in general, and no assertion that every
initial right disagreement ever reaches the center.

The existing 55 control makes the nonlocal source explicit without a new
prefix experiment. Its initial right fringe is zero. The first three cuts
and their phase-correct representatives are

| j | L_j(r) | C_j |
| --- | --- | --- |
| 0 | 55 | 55 |
| 1 | 110 | 111 |
| 2 | 220 | 222 |

The new middle entry is the hand cycle
110 ->100 ->111 ->100, so cyc(110)=111 (not100). The last entry is the
existing 220 ->201 ->223 ->200 ->222 ->200 certificate. Thus d_1(0)=1,
d_2(0)=0, and there are no initial differences at positions <=0.
At physical time1 both center-and-left rows are100; at time2 the actual
row is223 and the shadow row222. The injection R_1=1 therefore has
its ONLY initial discrepancy ancestor within its cone at position1,
although the newly included initial position2 agrees. This refutes the
shortcut that each physical injection is the fresh discrepancy at t+1.
It neither enumerates later injections nor constructs an infinite survivor.

## 5. The shadow still requires the original transient history (`refuted` shortcut)

The relation sigma C_(j+1)=C_j does not justify computing the next
representative by appending the ACTUAL new initial bit to C_j. In general

    cyc(2y+a) != cyc(2cyc(y)+a),

even for positive finite y and a=0. The hand control y=7 has cyc(7)=6.
The existing cycles give

    cyc(14)=13,   cyc(12)=12,

since 14 ->12 ->13 ->12, whereas 12 is cyclic already. Thus the
two displayed expressions differ, although their projected cycle is
the same6 and their least periods are both2.

The correct construction always uses cyc(L_j(r)) from the ORIGINAL
cut, including its transient. The phase fork in the other round304 note
is a further obstruction to reducing this history to a clock: even two
cyclic extensions can belong to different cycles without clock growth.
Neither observation permits choosing a replacement right fringe.

## 6. Exact transient data for a permutation lift (`partial-proof`)

The failed recursion in Section 5 leaves a concrete question: which data
from the ORIGINAL cut select its next phase when the cyclic driver never
resets? An exact formula would identify the information that must be
transported; failure would invalidate that proposed reduction. The following
is a one-step identity, not a closed finite-state model or a new search.

Let y be finite, z=cyc(y), and assume bit_0(A^s z)=0 for every s>=0.
Choose ANY T>=tau(y), and write for 0<=s<T

    u_s=bit_0(A^s y), v_s=bit_1(A^s y),
    w_s=bit_1(A^s z).

Products below are products of Boolean bits; all sums are XOR. Empty
products are 1 and empty sums 0. Define

    eta = product_(s=0..T-1)(1 XOR u_s),
    theta = XOR_(s=0..T-1) [(v_s XOR u_s)
                 product_(k=s+1..T-1)(1 XOR u_k)]
                 XOR XOR_(s=0..T-1) w_s.           (11)

Then for each actual initial bit a in {0,1},

    cyc(2y+a)=2z+(eta*a XOR theta).                  (12)

Proof. The actual low response f_s of 2y+a obeys the affine recurrence

    f_(s+1)=(v_s XOR u_s) XOR ((1 XOR u_s)*f_s),
    f_0=a.

Composing it through time T gives eta*a plus the first sum in (11).
The cyclic lift of z with phase-zero low bit b has response
b XOR XOR_(s=0..T-1)w_s at time T, because its low driver is always zero.
Matching these two responses gives b=eta*a XOR theta. Their upper rows
also agree at T. Both extensions of z are cyclic, so this match identifies
the phase-correct representative uniquely and proves (12).

The formula is independent of the chosen T once T>=tau(y). At a further
step u_T=0 and v_T=w_T, so eta is unchanged and the two new contributions
to theta cancel. If an actual u_s=1 occurs during the transient, eta=0:
the original bit a has been forgotten even though the EVENTUAL driver is
permutative. In the first sum in theta, only the last such reset and the
following suffix survive. If no such reset occurs, eta=1 and

    theta = XOR_(s=0..T-1)(v_s XOR w_s).             (13)

Thus even a transient with no low-bit reset can change the recurrent phase
through its high-bit parity. At a cyclic source T=0, eta=1 and theta=0.
For a cyclic driver which DOES contain a low 1, the earlier unique
resetting-lift theorem instead determines the extension from z alone.

Two hand controls distinguish the mechanisms. For y=7, z=6, T=1,
(u_0,v_0,w_0)=(1,1,1), giving eta=0, theta=1. Hence both original
bits a select the phase13, consistent with 14 ->12 ->13 and 15 ->12 ->13.

For a no-reset control, a hand-solved finite preimage of the existing
cyclic state222 is y=166:

    A(166)=41 XOR247=222,
    A(222)=55 XOR255=200,
    A(200)=50 XOR236=222.

Thus tau(166)=1, cyc(166)=200, and its low trace is zero at EVERY time.
Here (u_0,v_0,w_0)=(0,1,0), so eta=1, theta=1. Equation (12) gives

    cyc(332)=401,   cyc(333)=400.

An independent hand cycle verifies these phases:
400 ->444 ->401 ->445 ->400, with 332 ->445 and 333 ->444.
All four cycle states are distinct. This is not a source supply or clock
census; it checks the transient-parity term in the exact formula.

The pair (eta,theta) suffices for this ONE extension once the full cyclic
driver is known. No recurrence updating (eta,theta) under the next spatial
extension from those two bits alone has been proved. Computing the next
pair can require a new complete transient and an unbounded-period driver.
In particular (12) does not reopen the finite-observation birth quotient
closed in round303.

Fixed verification (`finite-exhaustive`):
`experiments/problem1_nonperiodicity/check_round304_phase_memory.py` checks
only y in {7,166}, a in {0,1}, T in {1,2,5}. The product formula and an
independent Boolean-cell/iterated-OR response agree on all12 cases and
the hand phase values. Fifteen hand transitions and eight fixed source,
core and lift cycle certificates also agree. The declared caps are
16 updates per cycle, 10 seconds and128MiB. Any disagreement invalidates
the stated formula/control; agreement is finite verification of the two
mechanisms, not proof of the all-depth identity or global construction.
Atomic provenance is `results/problem1/20260907_round304_phase_memory.json`.

## 7. Remaining target (`inconclusive`)

This constructs one global auxiliary spacetime with exactly the cycle
representatives required by the existing renewal. It exposes an infinite
initial supply of right-hand disagreements under every finite actual
support hypothesis, rather than erroneously treating those disagreements
as a finite set. It also identifies the true finite cone for each injection.

It does not determine which initial shadow differences survive to the
physical center, how often a single ancestor can contribute, or how FULL
constrains that survival. Eventual bounded cycle-defect width, if assumed,
means the TWO spacetimes agree at all sufficiently left positions near the
center for all late times; finite support alone does not prove this bound.

A surviving route must use the actual eventually-zero initial right boundary
TOGETHER WITH this uniquely selected entire shadow, including the transient
phase data in (11), and derive an obstruction to the FULL crossing history.
The older anchored route still needs a global assignment into its finite
post-rebase target set with bounded reuse.
No additional shadow prefixes, doubling positions, or cycle trees should
be enumerated merely to illustrate the all-depth construction.

Dependencies: phase-correct cyc commutations in
`problem1_cycle_completion_defect_transport.md` Section 1;
the one-bit lift theorem and physical bridge in
`problem1_physical_time_cycle_defects.md` Sections 1 and 4;
Theta injectivity and finite-code counts in the temporal-code notes;
`problem1_highest_wait_nonforcing.md` Section 1 for the independent
infinite-tail check; the exact renewal and the existing 7/55 certificates.
