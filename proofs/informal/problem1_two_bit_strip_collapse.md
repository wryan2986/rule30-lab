# An eventual two-bit strip collapses to the one-bit case

Status: `partial-proof` for the all-depth conditional reduction and local
obstructions. External adversarial review is missing. The fixed algebra
check has status `finite-exhaustive` only on its declared assignments.
No eventual strip bound is established. Problem 1 remains OPEN.

## 0. Admission and route choice

Round305 identifies the exact one-bit exit but leaves its subsequent
leftward motion open. Test whether the next permitted gate makes that exit
incompatible even with an eventual TWO-bit strip. If so, combine this with
the mandatory clock doublings to reduce the K=2 case to the existing K=1
bottleneck. A failure would leave a distinct K=2 mechanism requiring study.
This is an all-depth structural question, not a search over widths, gates,
sources, or longer FULL prefixes.

Ranked routes (`heuristic`): first derive the forced motion after the known
exit; second ask whether a late doubling supplies a cyclic entry into that
invariant region; retain the complete periodic driver if either local step
fails. No autonomous update of a shadow flag is assumed. The only numerical
verification admitted below checks fixed Boolean identities in the proof.

## 1. Statement on the same complete spacetime (`partial-proof`)

Fix one nonzero finite actual row, with its ENTIRE original finite right
fringe, and let r(t)=U^t r(0), hat r(t)=U^t E(r(0)). Assume FULL:
r_0(t)=1 for even t and 0 for odd t. Put

    Y_t=sum_(i>=0) r_(-i)(t) 2^i,
    tau_t=tau(Y_t), b_t=b(Y_t), p_t=p(Y_t).

Here b_t=0 when the center-and-left rows agree, and otherwise it is one
plus the highest differing bit index. It measures SPATIAL disagreement;
tau_t measures the least A-time to cycle entry. Do not identify their
values on an individual row.

Then

    [there exists T: tau_t<=2 for every t>=T]
       iff
    [there exists T': tau_t<=1 for every t>=T'].       (1)

Equivalently, eventual b_t<=2 is equivalent to eventual b_t<=1. The
nontrivial direction uses the imported eventual threshold equivalences,
the unbounded clocks of this one finite orbit, and Sections 2-4 below.
It gives no numerical bound on the time T' of the first suitable doubling.

The same statement applies after the previously justified SINGLE even
finite-entry rebase. Its actual finite fringe is retained. Nothing here
establishes either antecedent for a hypothetical FULL survivor.

## 2. The exact even-row identity needed below (`partial-proof`)

At an even FULL time v let u be the actual gate-u indicator. The existing
gate bridge gives the four low bits and the next A pair as

    (Y_v[0],Y_v[1],Y_v[2],Y_v[3])=(1,1,u,1 XOR u),
    (A Y_v)[0..1]=(1 XOR u,u).                       (2)

These also follow directly from the four actual centers 1,0,1,0. The
first 1->0 forces r_-1(v)=1. The next center update uses r_1(v+1)=u
and forces r_-1(v+1)=1 XOR u, hence r_-2(v)=u. The last 1->0 forces
r_-1(v+2)=1; updating r_-1 once more yields r_-3(v)=1 XOR u.
No shadow center values are imposed in this derivation.

## 3. An odd doubling forces a third spatial bit (`partial-proof`)

Claim. If p_(t+1)=2p_t at an ODD FULL source t, then

    b_(t+1)>=3.                                      (3)

The one-bit lift classification makes the shadow cut at t have low
A-trace identically zero. At v=t+1 its shadow cut z=cyc(Y_v) consequently
has HIGH bit trace identically zero:

    z[1]=0, (A z)[1]=0, indeed (A^s z)[1]=0 for all s.

Suppose b_v<=2. Then z and Y_v agree at bits 2,3 and all higher bits.
By (2), z[2]=u and z[3]=1 XOR u. The A rule now gives

    (A z)[1]=z[3] XOR (z[2] OR z[1])
             =(1 XOR u) XOR u=1,

contradicting its required zero value. This proves (3), without assuming
any bound on tau_t and without guessing the shadow center z[0].

An independent physical derivation follows the original doubling
characteristic: its shadow values at (-1,v) and (-2,v+1) are both zero.
Agreement at positions -2,-3 at time v instead forces the latter value
to be (1 XOR u) XOR (u OR 0)=1. Thus one of those two positions must
already disagree. This is a finite-cone contradiction, not an assertion
of periodicity of a fixed physical shadow column.

Therefore no sufficiently late ODD doubling fits inside an eventual
two-bit strip. This strengthens source lateness at the spatial level;
it does not claim that every odd doubling has tau_t>=3.

## 4. A one-bit exit necessarily reaches the third bit (`partial-proof`)

Suppose at an even FULL time v the two rows agree at every position<=-1.
Their centers may differ. The round305 table lists every next-even
alternative. Its only failure of negative-half agreement is the branch

    d_0(v)=1, actual gate u, hat r_1(v)=0,
    d_-1(v+2)=1, d_0(v+2)=0,
    d_i(v+2)=0 for all i<=-2.                        (4)

The ACTUAL no-uu theorem makes the gate at v+2 equal t. Equation (2)
therefore makes the shared cell r_-2(v+2)=hat r_-2(v+2)=0.
At the following step the discrepancy at -1 passes through this zero:

    d_-2(v+3)=1.                                    (5)

Indeed the update at -2 reads equal left cells and equal central zeros,
and its right inputs differ. All positions<=-3 still agree by their
cones. Thus b_(v+3)=3 EXACTLY. This conclusion keeps the future physical
step that was absent from the earlier two-step exit table.

In particular, in an eventual b<=2 region, no such exit can occur.
Starting at ANY even row with negative-half agreement in that region,
the table and (5) imply negative-half agreement at every subsequent even
row, by induction. At the intervening odd rows the common even left
neighbor 1 shields the center discrepancy, so their negative halves
also agree. Consequently b<=1 from that starting row onward.

This invariant-region statement concerns the TWO already specified
spacetimes. It neither chooses new shadow boundary bits nor says a
general two-bit state must enter the region without further input.

## 5. A mandatory doubling supplies entry (`partial-proof`)

Assume the left side of (1). The imported thresholds give a time M after
which BOTH tau_t<=2 and b_t<=2 hold, for every physical time t.
Finite positive widths and full-code injectivity make p_t unbounded;
physical extensions preserve or double the clock. Hence a doubling occurs
at some t>=M. By (3) it is even.

At an even FULL doubling source with tau_t<=2, the already established
two-step clock-consumption result is

    tau_(t+2)=0, p_(t+2)=2p_t.                       (6)

For clarity, its key phase point is that the first lifted periodic code
is (v_s,0), with v visiting both bits. The second lift therefore has
unique recurrent low bit 1. After applying A to the first actual
successor its upper row is cyclic, because its delay is at most one.
The actual second boundary bit is also 1, giving the cyclic row in (6).
This argument retains the actual upper transient and actual boundary.

At the even time t+2 the whole center-and-left row thus agrees with the
global shadow. Section 4 propagates b<=1 forever from there. The imported
threshold transport now gives eventual tau<=1. This proves (1); its
reverse implication is immediate.

There is also a sharper local observation that is not needed for this
proof. Under b_t,b_(t+1)<=2 an EVEN doubling source cannot have gate t:
its shadow center and the next A low bit are both 0, so (2) and agreement
at bit 2 force z[1]=u. Gate t would give d_1(t)=1 and common bit 2 zero,
forcing b_(t+1)>=3. Thus all sufficiently late doublings in the two-bit
case already have even gate u and negative-half agreement at the source.
This agrees with the conditional K=1 doubling law; it supplies no bound
on the number of subsequent births.

## 6. Fixed verification and exact frontier

The predeclared checker is
`experiments/problem1_nonperiodicity/check_round306_two_bit_collapse.py`.
It checks the odd-doubling contradiction on u in {0,1} and arbitrary
shadow center z[0] in {0,1}: four Boolean assignments. Separately it
checks (5) at the post-exit even row for the three nonzero actual right
pairs and all four shadow right pairs: twelve assignments. The actual
four low bits are fixed to (1,1,0,1), and only the shadow left neighbor
is toggled on the negative half. Other actual/shadow right bits are zero.

Direct truth-table physical updates and an independently packed A-cut
update must agree. The named assignments are Boolean-identity tests;
their second rows are not claimed to be E of their first rows. A failure
invalidates the local algebra or implementation. Agreement is
`finite-exhaustive` only for those sixteen cases, not machine verification
of (1), clock growth, no-uu, or global shadow membership.

Caps: one local CPU, 10 seconds, 128 MiB, one physical step per case,
128 KiB output. Exact parameters and atomic provenance are recorded in
`results/problem1/20260907_round306_two_bit_collapse.json`.

The whole-tail consequence is a REDUCTION: K=2 is not a distinct eventual
bounded-delay alternative to K=1 on a finite FULL orbit. Excluding K=1
would now exclude K=2 too. Neither is excluded here; no K bound is proved.
The complete actual/shadow birth supply from round305 remains unresolved.
In particular, (5) permits a third-bit excursion when K>=3 and does not
authorize a general induction on strip width or a sequence of width sweeps.

Dependencies: `problem1_physical_time_cycle_defects.md` Sections 1-5;
`problem1_global_cycle_shadow.md` Sections 1-2;
`problem1_cycle_delay_renewal.md` Section 3, especially (8a);
`problem1_one_bit_shadow_exit.md` Sections 1-2;
`problem1_period_two_fringe_language.md` for actual no-uu.
