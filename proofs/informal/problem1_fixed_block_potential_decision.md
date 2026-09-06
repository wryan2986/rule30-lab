# Exact finite inequalities for a fixed-block history potential

Status: `partial-proof` for the reductions below and the scanner-fixed
obstruction; `finite-exhaustive` for the supplied-history replay. A fresh
Muse review failed with provider429; the lead checked the argument and
two arithmetic formulations locally. No feasible or infeasible whole-class
certificate is asserted. Problem1 remains open.
Base checkpoint: `72f6868` (full commit retained in the verification record).

## Bottleneck, route ranking and admission

The recovered Wdagger counterexamples refute another particular potential.
The eight stored differences cannot give a nonnegative circulation
obstruction at ANY coefficient size. Fitting another weight vector to those
differences therefore does not address universal descent.

Ranked routes (`heuristic`):

1. Express the COMPLETE signed block change as an exact finite path weight,
   then test the whole potential class through finite inequalities.
2. Couple prescribed age to original history length in the boundary-sum
   argument. This retains the strongest occurrence restriction but still
   lacks a preserved inequality.
3. Require every original edge to be unchanged by six scanner passes as
   a sufficient class obstruction. This is a stronger condition than count
   cancellation and must be falsified before a graph search is admitted.

Choose route1's algebraic reduction. Use ONLY six observed branches ututut,
old-prefix edge weights modulo16 and the established exact scanner. This
needs16 bits of original-prefix precision, hence65536 states; the precision
comes from the six scanner passes, not a frontier complexity cap. The
earlier once-prescribed language already used this state count.

Admit verification of the formulas on the eight EXISTING block pairs and
the four residues903+j*16384, j=0,1,2,3. A mismatch invalidates the reduction.
Agreement supports the separate all-length proof below, not feasibility of
its inequalities. No new ordinary word, occurrence, frontier, motif, full
graph traversal, solver installation, or coefficient search is admitted in
this verification. Local CPU120s, wall180s,1GiB. Preserve exact source/input
hashes, full Git, hardware/software, timing and atomic result records.

## Signed edge decomposition

Use T(x)=x XOR((x<<1) OR(x<<2)), U(x)=T(x) XOR1,
P(x)=T(2x+1)>>1, A(x)=T(x)>>2, and S_0=t,S_1=u,S_2=S_3=p.
The phase root is3 or1 and is excluded from counts. A fixes both roots.
The prescribed scanner H sends the ith original letter to
S_(G_g(q) mod4), where q is its old prefix endpoint. With six forced
steps, the final history is H^6(w) followed by six transformed birth letters.

Let e_(r,g) denote the unit vector in the48-dimensional old-residue/letter
count space. For a prefix residue q modulo65536 and g in{t,u,p}, define

    d(q,g)=e_(A^6(q) mod16, S_(A^5(G_g(q)) mod4))
           -e_(q mod16,g).                                     (1)

This is exactly the final-minus-initial contribution of one ORIGINAL
position. The first index needs16 original bits; the emitted letter needs
at most12. The congruence-loss bound for A and congruence preservation of
each G make (1) independent of the chosen representative q.

The four accepting residues are K={903+j*16384:0<=j<4}. They encode
exactly the six actual gates ututut. The admissibility-test u appended to
this motif is unobserved; utututu has no forbidden factor.

For a in K, set x_t=F^t(a), 0<=t<=6, with actual branches Q_(t-1).
The nonnegative integer birth-count vector is

    B(a)=sum_(t=1..6) e_(A^(7-t)(x_(t-1)) mod16, ell_t),
    ell_6=Q_5,
    ell_t=S_(A^(5-t)(x_t) mod4) for t<6.                       (2)

Every component is determined by a modulo65536: in the prefix index,
losses from F^(t-1) and A^(7-t) total twelve bits; all letter indices
need no more. The representatives a need not themselves be ordinary.

For EVERY finite ordinary history w=g_1...g_n with prefix endpoints z_i
and z_n mod65536 in K, the complete count difference is

    Delta(w)=sum_(i=1..n) d(z_(i-1) mod65536,g_i)
             +B(z_n mod65536).                                (3)

Proof: apply the original-position and birth-position formulas from
`problem1_prescribed_history_cost_pullback.md` componentwise to the48
unit edge weights, then subtract the original counts. That proof concerns
positions in the actual prescribed history and allows arbitrary signs
after taking a linear combination. No representation is reselected.
The empty history has the same formula when its endpoint is accepted.

## Exact finite path test for fixed weights

Let Gamma have residues modulo65536 and all three generator edges
q --g--> G_g(q) modulo65536, with vector label d(q,g). Start at the
chosen phase root(s), and accept at K. Trim to vertices reachable from
a chosen root and able to reach K. Every retained edge is included.
This trimming is part of the mathematical definition; no strong
connectivity claim or graph enumeration is needed for the theorem.

Every accepted graph path lifts to its concrete ordinary generator word,
and every admitted ordinary history projects to such a path. Thus, for
fixed real weights omega, universal strict block decrease is EXACTLY

    sum_(edges of p) omega.d(e)+omega.B(a)<0
       for every accepted finite path p ending at a.            (4)

If a directed cycle in the trimmed graph has positive omega.d weight,
repeat it between a root-to-cycle path and a cycle-to-acceptance path.
For sufficiently many repetitions, (4) fails. Conversely, if every
cycle has nonpositive weight, removing cycles never decreases the
accepted path score. Its maximum is therefore attained on one of the
finitely many simple accepted paths. This proves an exact decision rule
for fixed omega: exclude positive cycles and test that finite maximum.
No finite-length cutoff for arbitrary future dynamics is being asserted.

In particular strict decrease, if valid for real weights, has a uniform
positive margin on this fixed motif. This fact follows from cycle removal,
not from integer-valued weights or compactness of an infinite path set.

## Finite linear feasibility for the whole bounded-below class

The class consists of fixed real omega on the48 edge types with ONE
lower bound on W_omega over all ordinary histories from the chosen
root(s), and strict decrease over every accepted six-step block.
For independent phase weights, apply the construction separately in each
phase. Shared weights mean one system with both roots.

On the ordinary16-state generator graph trim only to root-reachable
vertices. The lower-bound condition is equivalent to the existence of
real vertex numbers phi satisfying, on every retained ordinary edge,

    omega(r,g)+phi(r)-phi(G_g(r) mod16)>=0.                     (5)

Sufficiency follows by telescoping along any history and the finite
minimum of phi. For necessity a negative reachable cycle would violate
the lower bound by repetition; with none, shortest root-to-vertex weights
are finite and satisfy (5). Use a superroot of zero-weight edges when
both phase roots are included.

On the trimmed65536-state graph introduce real h(q). Add

    h(q)>=omega.d(q,g)+h(G_g(q) mod65536),                     (6)
    h(a)>=omega.B(a)+1                 for retained a in K,   (7)
    h(rho)<=0                         for retained roots.    (8)

Then (5)--(8) are feasible IF AND ONLY IF this class has a universally
strictly decreasing potential on this motif.

For sufficiency telescope (6), use (7),(8), and obtain every block
change<=-1; (5) supplies the history lower bound. For necessity the
preceding cycle argument supplies a strictly negative largest block
score M. Rescale omega by at least1/(-M). For each retained q let h(q)
be the maximum of the scaled edge score from q to acceptance, plus its
terminal B score and1. No positive cycle exists, so the maximum is
finite and obeys (6),(7); the normalized root scores give (8).
The lower-bound certificate rescales with omega. If there are no accepted
paths the block condition is vacuous; omit the h part and take omega=0.

All coefficients in this finite system are integers. A feasible finite
system of rational linear inequalities has a rational solution: eliminate
variables by pairwise lower/upper bound inequalities, then back-substitute
rational points in the resulting rational intervals. Multiplying by a
common positive denominator yields integer weights and vertex certificates
with margin at least1. Hence allowing irrational weights cannot rescue an
infeasible rational system. This is an exact finite feasibility reduction,
not a claim that it has been solved or that any weight candidate works.

## Scope and remaining obligation

This construction tests every finite history length for ONE fixed six-step
motif and a48-parameter potential class. It does not decide unrestricted
future survival, actual near-boundary returns, or all56 gap triples. A
feasible certificate for this motif would still need the other motifs and
the full return argument; an infeasibility certificate would close this
particular sufficient potential route, not refute Problem1.

No general feasibility solver has been run in this checkpoint. The local
Python environment has no scipy, sympy or highspy, and no z3, glpsol,
highs, cbc or lp_solve binary was found. This is a tooling observation,
not a mathematical obstruction or grounds to declare the goal blocked.
The next useful work is a compact exact feasible certificate or a dual
obstruction for (5)--(8), rather than a larger coefficient box on the old
eight vectors. A computation must have its own bounded admission first.

## Verified terminal loops and a smaller necessary test

The independent-position calculation and six successive cell scanners
agree on all125 original positions of the eight saved block pairs and
on their full48-component changes. The four accepting residues have
the following exact birth suffixes; the table is exhaustive over K.

| a | A^6(a) mod16 | Birth suffix | Prefix residues before its six letters | F^6(a) mod16 |
| --- | --- | --- | --- | --- |
| 903 | 11 | ptuppt | 11,4,12,5,10,5 | 11 |
| 17287 | 15 | ptuppt | 15,0,0,1,6,9 | 15 |
| 33671 | 3 | ptuppt | 3,12,4,13,2,13 | 3 |
| 50055 | 7 | ptuppt | 7,8,8,9,14,1 | 7 |

Thus EACH B(a) is a nonnegative circulation in the ordinary16-state
graph, although three COMPLETE block differences are open. The table
extends to all accepted finite histories by the proved16-bit precision.
For any history realizing a, the birth loop is reachable from its root
via H^6(w), so its weight is nonnegative for any bounded-below omega.

Only a=50055 gives a complete closed block: both the initial and final
endpoints are7 modulo16. Restrict (4) to this accepting residue. Under
the gauge change omega'(r,g)=omega(r,g)+phi(r)-phi(G_g(r)), complete
closed-block changes are invariant by telescoping. Equation (5) makes
omega'>=0. Conversely nonnegative weights are bounded below. Hence
existence of a bounded-below strict potential on this CLOSED sublanguage
is equivalent to existence of a NONNEGATIVE strict potential there.
For this necessary subproblem one may replace (5) by omega>=0 and
retain (6)--(8) with acceptance{50055}. Failure would refute the full
class; success would not settle the other three terminal classes.

## A sufficient cancellation mechanism is impossible

Route3 proposed finding an accepted ordinary word whose original edges
were all unchanged by six scanner passes. In particular that would require
H^6(w)=w. This cannot happen, at ANY finite ordinary length, for this motif.

Indeed H^6(w)=w implies A^6(x)=x for its endpoint. Every finite positive
A-cycle has power-of-two least period, by the exact binary cycle-lifting
theorem in `problem1_frontier_head_dynamics.md`, section2. A period dividing6
therefore divides2, so A^2(x)=x. But the motif gives x=903 mod16384,
hence x=7 mod64. Two applications of A lose at most four low-bit precision
bits, and A(7)=6, A(6)=6. Consequently A^2(x)=2 mod4, whereas x=3 mod4,
a contradiction. The endpoint is positive because it is ordinary.

This is a `partial-proof` no-go for literal original-word invariance;
no fixed-word graph search is needed. It does NOT exclude aggregate
edge-count cancellation between DIFFERENT words, a combination of block
differences, or a solution of the potential inequalities. In particular
one must not infer full sixteen-state infeasibility from this stronger
mechanism's failure.

The finite replay is preserved in
`results/problem1/20260906_fixed_block_potential_verification.json`, with
its pre-result admission-note snapshot and full source. The auxiliary
structural audit checks the four loop divergences, the hand-derived
A(7)=A(6)=6 identities and the gauge cancellation, without any new graph
or word search. The fresh Muse review attempt returned provider429;
no substitute agent or successful external review is claimed.
