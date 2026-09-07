# Cycle births are not determined by any finite observation

Status: `partial-proof` for the all-depth constructions and deductions below;
`refuted` for the finite-observation decision rule at the precise domain in
Section 4. Fresh external adversarial review is missing. Problem 1 is OPEN.
The countermodels are rational A-periodic rows with equal dyadic clocks.
They are NOT asserted to have finite support or an infinite FULL future.

## 0. Round 303 strategy reset and admission

The incoming bottleneck is the supply of cycle-to-lag births on ONE FULL
finite-entry orbit. The renewal identity requires infinitely many injections;
the conditional K=1 result allows bounded episodes, but leaves their births
unclassified. More first witnesses, source-word searches, and larger strips
do not address this gap. Ranked routes (`heuristic` estimates):

| Rank | Materially different route | Assumption to test | Success would establish | Cheap falsification | Estimated cost |
| --- | --- | --- | --- | --- | --- |
| 1 | Determine the birth at the start of a whole bounded episode from its cyclic return | A uniformly bounded observation of a cyclic permitted source suffices without using finite spatial support or the infinite FULL condition, even when the exact clock is supplied separately | A usable local birth rule for the episode argument; it would still need a global exclusion step | Hold an arbitrary prefix and clock fixed and force both return states by changing only the unobserved end of a period | One structural session; two reset compositions |
| 2 | Charge resetting lifts along their actual spacetime ancestry to original anchored activity | There is a finite-multiplicity charge to P_n(Y_0,s) inside s<n, controlled by Q(Y_0), for the required injections | Combined with the renewal lower bound, FULL/finite-entry incompatibility for period two | First derive the indices for one inherited-horizon reset; an n=0 endpoint, wrong horizon, or uncontrolled multiplicity invalidates that charge | Several sessions; no justified charge currently |
| 3 | Use spatial nilpotence of cyclic codes together with the complete fixed right fringe | The constraint Phi^j b=0 at some spatial depth prevents an infinite sequence of the resetting/doubling passages compatible with FULL | A finite-support-specific exclusion, potentially closing period two | The existing finite cyclic source 55 already refutes a single-step ban on births; any stronger induction must use the continuing history | Several sessions to weeks; highest global cost |

Route 1 has the quickest exact falsification and directly tests the missing
input of the proposed episode closure. It fails in a stronger, quantitative
form: arbitrarily close cyclic sources with the SAME exact dyadic period
give opposite first injections. Route 3, not a longer observation of route 1,
is the surviving structural task. Route 2 remains separate and unresolved.

Admission before computation: check only the fixed four-state scan algebra,
including every possible interior function on four states. If the suffixes
force different recurrent starts independently of that function, a uniform
finite-observation birth rule is excluded at the stated domain. If they do
not, the construction fails. Agreement cannot establish finite support or
an infinite FULL orbit. No temporal words, periods, seeds, or source supply
are enumerated. Cap: one CPU, 10 seconds, 128 MiB, one finite algebra check.

## 1. Definitions and two exact suffixes (`partial-proof`)

Import A, Theta, Phi and I_a from the reviewed temporal-code notes. In
particular Theta is a homeomorphism, its first L symbols biject with the
first 2L spatial bits, and Theta(Ax)=shift Theta(x). Pure periodic codes
are exactly A-periodic rows. Write tau for least A-preperiod, p for least
period, and cyc for the phase-correct cycle representative.

On the permitted domain, b=Theta(x) has b_0=3 and b_1=g in {1,2},
where g=1 means gate t and g=2 means gate u. The paired map satisfies

    F(x)=4 A^2(x)+3,
    Theta(Fx)=I_3 shift^2 b.

This is an actual physical step when the fixed right fringe supplies the
specified gate; the gate is not a replacement for that fringe.

The driven maps, in state order 0,1,2,3, are

    H_0=[0,1,3,3], H_1=[3,2,2,2],
    H_2=[2,3,1,1], H_3=[1,0,0,0].

Read a word from left to right, so its last letter acts last. Directly,

    H_3 H_1 = constant 0,    H_1 H_1 = constant 2.       (1)

For an independent bit derivation, H_1 sends every state into {2,3}.
For either of these states, the defining h formula gives H_3=0 and H_1=2.
Thus (1) holds without a hypothesis on any preceding letters.

If a period of b ends in 13 or 11, its scan drive starting at b_2
has return map ending respectively in

    H_g H_3 H_3 H_1,    H_g H_3 H_1 H_1.              (2)

Here the final H_3 and H_g outside the suffix correspond to b_0,b_1
at wraparound. Equations (1)-(2) give this entire return table:

| Source gate g | End of period | Recurrent start z | tau(Fx) |
| --- | --- | --- | --- |
| 1 (t) | 13 | 2 | 1 |
| 1 (t) | 11 | 3 | 0 |
| 2 (u) | 13 | 3 | 0 |
| 2 (u) | 11 | 2 | 1 |

All four return maps are constant, irrespective of the preceding scan
function. Their fixed point is the displayed z. The actual scan starts
at 3. If z=3 it is periodic from its start. If z=2, every H_i merges
states 2 and 3 on the first update, so its least preperiod is exactly one.
It cannot be periodic with some other period: a common multiple of that
period and the driving period would make its initial 3 equal to z=2.
The response has the same LEAST eventual period as b: Phi of the response
is shift^2 b, so the input period divides the response period, and the
periodic response supplies the reverse bound.

## 2. Arbitrary prefixes, identical exact dyadic clocks (`partial-proof`)

Theorem. Let w be ANY word of length L>=2 with w_0=3 and w_1 in {1,2}.
Choose ANY power of two p>=max(8,2L). Form the length-p words

    B13 = w 0^(p-L-2) 1 3,
    B11 = w 0^(p-L-2) 1 1,
    x13 = Theta^(-1)((B13)^infinity),
    x11 = Theta^(-1)((B11)^infinity).                (3)

Both sources are rational A-periodic permitted rows of EXACT least period
p. They have the prescribed temporal prefix w. Their next paired rows
have the same least eventual period p and opposite preperiods 0 and 1,
as in Section 1. More precisely,

    v_2(x13-x11)=2p-1,
    v_2(Fx13-Fx11)=2p-3,
    v_2(cyc(Fx13)-cyc(Fx11))=0.                     (4)

Proof. Both words have symbol 3 at index 0 and symbol 0 at index p/2:
the latter is in the padded interval L,...,p-3. Their least periods
divide p. Every proper divisor of a power of two divides p/2, so no
proper period is possible. Periodic coding gives A-periodicity, and the
reviewed rationality equivalence for Theta gives rational 2-adic rows.

The two codes first differ in the HIGH bit of symbol p-1: symbols 3
and 1 have the same low bit. Triangular inversion of Theta solves that
symbol's low spatial bit before its high spatial bit. Thus the first
different spatial bit is exactly 2p-1, proving the first valuation.
The A^2 cell rule has its highest input with coefficient one at offset
four, so the first disagreement after A^2 is at 2p-5. Multiplication
by four in F shifts it to 2p-3. Finally, the two phase-correct cycle
representatives have low pairs 2 and 3 by Section 1. Their difference
is odd. No ordinary absolute-value estimate is being substituted for
these exact bit statements.

This shows why even exact knowledge of the common clock does not turn a
short observed driver into a complete return: the pair shares p-1 full
temporal symbols and the low bit of the last symbol. Reading the entire
period does decide the return. The result excludes a bound uniform in p;
it does not exclude a computation allowed to read all p symbols.

## 3. The first physical injection (`partial-proof`)

For ANY A-periodic x with x mod4=3, adjoining the actual next center 0
gives an A-periodic odd row

    Y_1=2 A x.                                      (5)

To verify (5), extend the periodic code of x to all integer A-times,
writing its bits as (r_s,s_s). The scalar lift above Ax satisfies

    d_(k+1)=s_(k+1) XOR (r_(k+1) OR d_k).

The update k=-1 has r_0=s_0=1 and sends both bits to 0. Hence the unique
periodic response at phase 0 has bit 0, exactly the actual extension.
Negative indices here belong only to the pure periodic driver.

When the actual gate also supplies the next even row F(x), each source
in (3) therefore has tau(Y_0)=tau(Y_1)=0 and tau(Y_2) in {0,1}.
The exact physical renewal gives R_0=0 and R_1=tau(Y_2). Thus the
opposite outcomes in Section 2 are actual new injections at time 1,
not inherited transients or a comparison of arbitrary cycle phases.
This says nothing about bounds at subsequent physical times.

## 4. Finite observation cannot decide the birth (`partial-proof` / `refuted`)

Let P be the space of all A-periodic permitted 2-adic rows, with its
subspace topology. Define B(x)=tau(Fx) in {0,1}, justified by the existing
cyclic-source theorem or Section 1 for the constructed rows.

Every nonempty temporal-prefix cylinder in P contains both B=0 and B=1
points by (3); prefixes of length less than two can be refined. Hence
both fibers of B are dense in P, and B is nowhere continuous on P.
In particular the claim that some finite temporal/spatial observation
decides the birth on this domain is refuted. A varying finite observation
length at each input does not help when the input is supplied only by
successively observed bits: there is no determining neighborhood at ANY
cyclic permitted input. Restricting the domain to sources with
dyadic periods still leaves the same no-go, since every constructed
pair has that property. Supplying the period as separate certified data
does allow reading the entire period and deciding the birth; (4) rules
out a uniform observation bound even with that extra data, not this
period-dependent algorithm.

This can retain the COMPLETE fixed initial right fringe, not merely its
gate. Fix any finite right fringe a and its unique FULL left input x_*,
whose existence is supplied by the full-boundary triangular homeomorphism.
No finiteness or A-periodicity of x_* is assumed. For ANY finite horizon
H>=3 and window of physical sites [-W,R], W,R>=0, choose L>=2 with
2L>W+H and take w to be the first L symbols of Theta(x_*).
Construct (3), and attach the SAME complete a to both rows.

Every backward physical cone in that window through time H reads left
indices of depth at most W+H and right cells in the same fixed fringe.
The first 2L spatial bits agree with x_*, so both actual spacetimes agree
with it throughout the window. In particular both centers alternate
through H, the initial gate is the actual fringe-supplied gate, and
their actual time-two rows are F(x13), F(x11). Yet their first new
cycle-entry injections differ. The right fringe has never been reset.

The quantifiers are essential: for EACH finite observation there are TWO
new sources. There is no ONE source shown to satisfy FULL forever. These
statements do not refute a decision principle restricted to infinite FULL
survivors, nor a quotient proved only along one such orbit. They do rule
out proving that principle from an arbitrary finite shadow alone, even
with cyclic inputs and matching exact dyadic clocks.

## 5. The surviving finite-support condition (`inconclusive` for FULL)

For a purely periodic code b and x=Theta^(-1)(b),

    x finite  iff  Phi^j b=0 for some j>=0.           (6)

This is the exact spatial-deletion identity Theta(pi^j x)=Phi^j b.
Moreover, for an A-periodic x, finite entry is equivalent to x being
finite: if A^h x is finite, move forward a further finite number of
A steps around its cycle to recover x, which must then be finite.

The construction (3) proves NO nilpotence assertion in (6). Dyadic
periodicity is insufficient: the two-symbol periodic code (12)^infinity
is fixed by Phi, since g(1,2)=1 and g(2,1)=2. Its row is A-periodic of
period two and not finite. This hand example explains why the equal
dyadic clocks in (3) do not discharge the finite-entry hypothesis.

The reset therefore narrows the next task: exploit (6) together with the
infinite actual boundary, or obtain the anchored charge of route 2.
Do not extend (3) as a period/word census, sample longer finite FULL
shadows, or claim a new gate/lag quotient from the resulting pairs.
Whether both birth fibers remain dense within FINITE cyclic sources is
not established and is not needed for the present no-go.

## 6. Verification and dependencies

The lead separately checked (1) from the bit equations, the wraparound
order in (2), exact least periods, triangular valuations, and the finite
physical cones. The fixed algebra checker compares the displayed maps
with an independent enumeration solving the two deletion equations and
checks both suffixes against all 256 functions from four states to four
states. This is finite-exhaustive scan algebra only; the universal-prefix
and physical-shadow deductions are mathematical arguments, not empirical
extrapolations. Fresh external review is still missing.

Checker: experiments/problem1_nonperiodicity/check_round303_birth_algebra.py.
Record: results/problem1/20260907_round303_birth_algebra.json.
Review disposition: problem1_round303_review.md in this directory.

Dependencies: problem1_activity_sparse_temporal_codes.md Sections 1-2;
problem1_activity_temporal_gate_bridge.md Sections 1-2;
problem1_full_fringe_temporal_diagonal.md Sections 1-4;
problem1_scan_doubling_cycle_lag.md Section 3;
problem1_cycle_delay_renewal.md Sections 1-2. No literature claim or
unverified external theorem is added.
