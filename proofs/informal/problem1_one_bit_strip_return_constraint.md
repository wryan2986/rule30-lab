# A conditional return law for an eventual one-bit defect strip

Status: `partial-proof`, lead-audited; fresh external adversarial review
could not be completed. See problem1_round10_fresh_review.md for the exact
missing review and lead disposition.
The global existence of such a strip under FULL and finite entry remains
`inconclusive`. Problem 1 is OPEN. No computation is used.

## 0. Admission and quantifiers

The delay-renewal identity leaves the smallest positive bound K=1 open.
Test whether the actual fringe's already proved no-uu condition sharpens
the motion of those single-bit defects. A forced return to the cycle at
each u gate would identify which future passage must create the next
defect; failure would rule out that proposed renewal description. This
is a symbolic all-period argument, not a graph or a longer gate prefix.

Fix ONE actual FULL orbit and its complete original finite right fringe.
Assume tau(Y_t)<=1 for every sufficiently large physical time t. Write
X_m=Y_(2m), C_m=Theta(X_m), and q_m in {t,u} for its ACTUAL gate. The
reviewed bit-depth transport also gives b(Y_t)<=1 at all sufficiently
large times. Choose m so all these late statements apply here and later.

The second bound is load-bearing. A single row with tau=1 can disagree
from its phase-correct cycle representative in several bits. That is not
allowed to substitute for the eventual one-bit-strip hypothesis above.

## 1. Exact lag-one transitions (`partial-proof`)

Claim. If tau(X_m)=1, then under the stated hypotheses

    q_m=t => tau(X_(m+1))=1,
    q_m=u => tau(X_(m+1))=0.                         (1)

Let b=C_m, p=p(X_m), and let b* be its phase-correct periodic completion.
FULL gives b_0=3. The strip bound b(X_m)<=1 means its only possible
spatial disagreement is the center bit. Since tau(X_m)=1 it does differ,
so b*_0=2. Also b_s=b*_s for every s>=1, and the gate gives b_1=1
on t, b_1=2 on u. The exact permitted scan is

    C_(m+1)=I_3 shift^2 b.                            (2)

Its input shift^2 b is PURELY p-periodic. Use the reviewed four driven
maps H_i, in state order 0,1,2,3:

    H_0=[0,1,3,3], H_1=[3,2,2,2],
    H_2=[2,3,1,1], H_3=[1,0,0,0].

For the t case, p>=2 since the completion contains both 2 and 1.
The last two input symbols over one period starting at b_2 are b*_0=2
and b_1=1. The return map therefore ends with H_1 H_2. H_2 has image
{1,2,3}, all of which H_1 sends to 2. The return map is constant 2.
The unique periodic response starts at 2, while (2) starts at 3.
Every H_i identifies the two states 2 and 3 at its first update.
Thus the actual response has least preperiod EXACTLY one. This proves
the first implication, independently of the period length.

For the u case, the next gate is t: the actual fringe forbids uu. Since
(C_(m+1))_1=H_(b_2)(3), the already required b_2 in {1,2} must therefore
equal 2. The periodic drive contains a 2 (b_1=2).

If the whole completion lies in {0,2}, the response starting at 3 is
already in the invariant pair {1,3}; every driving map on that pair is
a permutation. It is purely periodic, with period p or 2p, so the next
preperiod is zero.

Otherwise the completion contains 1 or 3 as well as 2. The scan is
resetting and has a unique periodic response. When p>=2 its return map
ends with H_2 H_2 and hence has image in {1,3}. The case p=1 here cannot
occur: a period-one word containing 2 is the constant-2 case just treated.
The recurrent starting state is therefore either 1 or 3. If it is 3,
the response (2) is periodic. If it is 1, the two starts 1 and 3 remain
distinct after the first update H_(b_2)=H_2, which swaps them. The actual
response would then have least preperiod at least two. The assumed bound
tau(X_(m+1))<=1 excludes that possibility. Thus the response is periodic
also in this resetting case, proving the second implication of (1).

## 2. A bounded duration for a lag-one episode (`partial-proof`)

The existing actual-fringe theorem bounds successive u gaps by 2 through
5 blocks. Consequently a run of late even rows with preperiod one lasts
at most five rows. Indeed t steps preserve lag one by (1), the next u
source still has lag one, and its successor has lag zero. From any source
index, a u occurs within at most four subsequent block indices.

This uses the actual full fringe only through its already proved gate
language and bounded u gaps. It proves no converse: a periodic even row
may produce a new lag-one row under the local permitted scan. The
round-seven cycle-source lemma gives only tau(X_(m+1)) in {0,1} there.

Under finite entry the actual clocks grow without bound. Only lag-one
even rows can supply late physical doublings under the K=1 hypothesis:
odd doublings require lag at least two, while periodic sources cannot
double. Every paired clock doubling thus consumes one of these lag-one
episodes at its u step. Before another such episode, a separate paired
transition from lag zero to lag one is necessary.

## 3. A doubling cannot be an immediate birth (`partial-proof`)

Take m sufficiently late that m-1 is also in the range where both bounds
apply. Suppose the even step from X_m doubles its clock. Under the all-physical
bound, the doubling is at physical time 2m, and tau(X_m)=1. Its periodic
completion u=Theta(cyc(X_m)) is contained in {0,2}. The actual gate is u,
and the no-uu condition supplies the three symbols

    u_0=u_1=u_2=2.                                  (3)

Temporal subscripts on this PURE periodic code may now be any integers,
using its unique periodic extension. They are not negative actual times.
Let v=Theta(cyc(X_(m-1))). Cycle completion of the actual bridge gives

    Phi u=shift^2 v, hence
    v_0=g(u_(-2),u_(-1)), v_1=g(u_(-1),u_0).         (4)

For symbols in {0,2}, the four relevant deletion values are

    g(0,0)=0, g(0,2)=2, g(2,0)=3, g(2,2)=1.         (5)

If X_(m-1) were cyclic, v_0=3. Equations (4)-(5) would force
u_(-2)=2, u_(-1)=0, and then v_1=2. Its actual gate would therefore
also be u, contradicting two adjacent u gates. Thus X_(m-1) has lag one.
Its actual gate is t, by (1), because its successor has lag one. The
one-bit strip then gives v_0=2, v_1=1. Equations (4)-(5) now force

    u_(-2)=0, u_(-1)=2,
    (u_(-2),u_(-1),u_0,u_1,u_2)=(0,2,2,2,2).       (6)

Therefore every sufficiently late doubling consumes an episode containing
at least the preceding lag-one t row and the current lag-one u row.
An episode in which a doubling occurs has between two and five lag-one
even rows. No assertion that every episode doubles is made.

The four consecutive 2s and their phase in (6) are necessary for ONE
actual history under the conditional strip bound. They do not produce a
finite-cycle supply with that word, nor authorize extending the failed
one-hole family from round nine. The already constructed period-one and
period-four local sources do not meet this additional past condition;
their original finite-horizon assertions remain unchanged.

## 4. The unclosed transition (`inconclusive`)

The pair (current gate, current lag) has not been shown to determine what
happens at a lag-zero row. Its periodic scan return still depends on the
complete temporal driver. Equations (1) therefore do not constitute an
autonomous finite-state quotient, do not bound the number of episodes,
and do not exclude infinitely many distinct bounded episodes and doublings.

The surviving K=1 attack is to control the actual cycle-to-lag-one births
between these u returns. Enlarging a gate prefix or drawing a finite graph
on these two observables does not supply that missing dependence. No such
experiment is authorized here.

Dependencies: problem1_cycle_delay_renewal.md Sections 1-3;
problem1_physical_time_cycle_defects.md Sections 2,5;
problem1_scan_doubling_cycle_lag.md Section 3;
problem1_period_two_fringe_language.md (no uu and u gaps 2 through 5);
problem1_full_fringe_temporal_diagonal.md Section 4;
problem1_inverse_scan_reset_language.md Sections 1-2.
