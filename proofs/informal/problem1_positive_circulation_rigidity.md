# Positive circulation and rigidity of fixed-block potentials

Status: `partial-proof` for exact rigidity and the LP optimum; `refuted`
for the whole sixteen-state bounded-below universal strict-descent class
specified below; `finite-exhaustive` for the rank certificates. Independent
cell/scanner arithmetic and an integer determinant verify the rank gate.
Fresh Muse proof review has been unavailable due provider429; review
status is recorded explicitly below and in the handoff. Problem1 remains open.
Base: `934cef45b8c19b3725140799035f3f8da08a6352`.

## New mechanism and admission

The preceding65536-state inequality solve timed out and is not repeated.
Instead exploit a strictly positive circulation with EXACT zero total
signed count change. This can force every cycle inequality to equality,
reducing the potential question to exact linear algebra in48 coordinates.

The candidate rigidity claim is that every real edge potential satisfying
these equalities is a constant per letter plus an endpoint coboundary.
If proved, its bounded-below members cannot decrease on a closed block
that appends six letters. A rank defect would leave additional potential
directions, giving a smaller EXACT linear subspace to investigate; it
would not establish a universal potential or justify repeating the old LP.

Use ONLY the existing65536-state signed graph, stored root1 spanning
tree and closed acceptance50055. Derive root-path signed count vectors
from that tree. Examine edges in increasing (q,g) order, g=t,u,p, for
independent cycle-difference rows, stopping immediately at rank32 or after
all196608 edges. The proved upper bound32 makes that stopping rule exact.
No new ordinary frontier, occurrence, motif, coefficient box, larger graph
or numerical solver is admitted. Recover only the short tree words needed
to verify selected rows. Local CPU120s, wall180s,1GiB, atomic records with
full Git, source/input/package facts, hashes and timings. Use exact modular
rank over verified prime65537; a nonzero modular minor proves the same
integer minor is nonzero. Independent verification must derive selected
rows through actual cell/scanner histories, not reuse packed path sums.

## A positive zero-change circulation (`partial-proof`)

Use d(q,g) from `problem1_fixed_block_potential_decision.md`. Every G_g is
a permutation modulo any power of2: its output bit i is input bit i XOR
a function of lower input bits. Thus putting one unit on every edge of
a fixed generator is a circulation. Write C_g for the sum of d over those
65536 edges.

Fix the lower12 input bits. The emitted letter
S_(A^5(G_g(q)) mod4) is fixed. Varying the upper four bits gives each
A^6(q) mod16 exactly once, since that output is triangular with diagonal1
in those upper four bits. Across the4096 lower inputs, G_g modulo4096
is a permutation, and A^5 modulo4 takes each value exactly1024 times.
The emitted letters t,u,p therefore occur1024,1024,2048 times. At EVERY
residue r modulo16, the triples of count changes are

    C_t(r)=1024*(-3, 1, 2),
    C_u(r)=1024*( 1,-3, 2),
    C_p(r)=1024*( 1, 1,-2).

Consequently C_t+C_u+2C_p=0 exactly. The circulation F putting weight1
on every t and u edge and weight2 on every p edge is strictly positive
on EVERY labelled edge, and sum_e F(e)*d(e)=0 as a48-vector.

All vertices of this graph are verified reachable from root1 and able to
reach50055. If omega gave strict decrease on every accepted finite path,
every directed cycle would have omega.d weight<=0 by pumping inside an
accepted path. Given ANY directed cycle, subtract a sufficiently small
positive multiple of its edge vector from F. The remainder is still a
nonnegative circulation and decomposes into cycles of nonpositive weight.
As F has weight0, neither the chosen cycle nor that remainder can have
strict negative weight. Hence EVERY directed cycle has weight EXACTLY0.

Every signed circulation is a difference of two nonnegative circulations:
add a sufficiently large multiple of the strictly positive F to remove
its negative coordinates. Therefore every signed circulation also has
omega.d weight0. This argument requires neither nonnegative omega nor
a lower bound on ordinary-history costs; it follows from universal strict
path descent alone. In particular all three global generator sums
sum_r omega(r,g) are equal, by the displayed formulas for C_g.

## Tree constraints and the sharp rank gate

Let P_q be the vector sum of d along the retained root1-to-q tree path.
For every edge q --g--> y, the signed flow consisting of that tree path,
then the edge, minus the root-to-y tree path has zero divergence. Thus
every universally strict omega must annihilate

    R(q,g)=P_q+d(q,g)-P_y.                                    (1)

These are constraints in48 coordinates, irrespective of the number of
tree vertices. A selected set of32 independent rows is sufficient below;
their tree words need not represent the same FULL ordinary integer,
only the same residue modulo65536 at their ends. Equation (1) is a
signed circulation constraint, not an identification of those integers.

There is always a16-dimensional subspace of solutions to all these
equalities:

    omega(r,g)=c+phi(r)-phi(G_g(r) mod16).                     (2)

Indeed constant c cancels from d, and the remaining d cost is
psi(q)-psi(y), with psi(q)=phi(A^6(q) mod16)-phi(q mod16).
It telescopes to zero on (1). The16-state ordinary graph is strongly
connected: the proven root reachability at width16 projects to all
sixteen states, and finite permutation generators make each orbit
strongly connected (an inverse permutation is a positive power).
Its coboundaries have dimension15. The constant edge function is
independent of them because the t edge at residue0 is a self-loop.
Thus (2) has dimension16, and the rank of ANY row family (1) is at most32.

If32 independent rows are verified, their common annihilator has
dimension16 and equals (2). This proves rigidity of EVERY universally
strict real omega without solving or approximating an inequality system.
A modular rank certificate is used only to certify a nonzero integer
minor; all constraints and the dimension argument are over the reals.

## Consequence of the verified rank gate

For (2), every ordinary history w has

    W(w)=c*length(w)+phi(root)-phi(endpoint mod16).

Boundedness below over all finite ordinary histories forces c>=0;
otherwise take histories of arbitrarily large length and use bounded
phi on sixteen states. Across a closed six-step block, history length
increases by6 and both endpoints are7 modulo16, so the change is6c>=0.
That contradicts strict decrease. The accepted class is nonempty by the
existing root-to50055 certificate. The passed rank gate therefore
refutes the ENTIRE phase-u real sixteen-state bounded-below class on this
closed sublanguage, and consequently any universal shared-weight class.

This concerns potentials over ALL ordinary histories and
representations. It does not rule out a restriction linking prescribed
age to original length, nonlinear potentials, more memory, or a proof
that uses some increases together with a net decrease over longer blocks.
It does not solve Problem1 or refute the whole-tail conjecture.

## Exact rank result and quantified no-go theorem

The gate passed after just44 edges in the declared order:32 independent
rows were selected among q=0..14. All32 rows were independently recovered
using cell-array generators, SIX actual scanner passes on both retained
tree words, and complete48-component counts. No packed path-sum table was
reused by this independent derivation. The selected integer minor has
determinant EXACTLY1 by fraction-free Bareiss elimination. Thus the
real-rank conclusion needs no floating-point or modular-rank extrapolation.
All512 row dots with the16 known kernel vectors vanish. A separate
rational determinant check of their complementary16-column minor also
gives1, directly verifying their independence. Independent
arithmetic also checks the12288 lower-input emitted-letter cases, giving
1024,1024,2048 for each input generator.

The resulting theorem is:

For EVERY real omega on the48 old-residue/letter edges, if W_omega has
one lower bound over ALL finite ordinary words from root1, then there
EXISTS a finite ordinary word w whose endpoint is50055 modulo65536
and for which the prescribed six-step ututut block has

    W_omega(final)-W_omega(w)>=0.

Proof: the negation would be universal strict decrease on that closed
sublanguage; the circulation, rank and boundedness arguments above yield
a contradiction. No bound on the witness length, common witness for all
omega, or physical finite-seed realization is claimed. The exact real
weights that DO give universal strict descent without the lower-bound
condition are precisely (2) with c<0. Necessity is rigidity and change6c;
sufficiency is the same telescoping formula on every accepted history.

The phase-u no-go already rules out a universal shared-weight potential
and independently chosen phase weights required to work in BOTH phases.
It makes no separate assertion of a phase-p-only counterexample here.

## The previous LP is now solved exactly, without another solve

This is an algebraic conclusion about the previously timed-out normalized
LP, not a revision of its numerical output. Let

    s(e)=h(q)-h(y)-omega.d(e)>=0.

Summing against the strictly positive circulation F cancels the h terms
and the d terms, so sum F(e)*s(e)=0. Hence EVERY slack is0. The same
tree-row constraints and rank32 certificate force (2) for any feasible LP
weights, irrespective of the sign of its margin.

Each generator permutes the sixteen original residues. Therefore
sum_(r,g)omega(r,g)=48c, since all phi differences cancel. The LP's
normalization gives c=1/48. Its closed block change is consequently1/8,
and telescoping its h constraints gives epsilon<=-1/8. The simple exact
primal omega(r,g)=1/48, h(q)=0, epsilon=-1/8 attains this bound: each d
has coordinate sum0, and the birth vector has coordinate sum6.

Thus the exact optimum is -1/8. There is no positive margin. The old
numerical timeout remains a timeout; no returned solver certificate is
invented, and no longer solve or new optimizer was run. This exact
rigidity proof supersedes the unresolved feasibility question and the
need to search for an explicit unit-flow dual certificate for this class.

## Verification provenance and next boundary

Records: `results/problem1/20260906_positive_circulation_rank_` followed by
`{primary,independent}.json`. The primary preserves the pre-result admission
snapshot, the32 original rows/tree words, the prime, source and hashes.
The independent record preserves the32 cell/scanner row calculations,
integer minor, determinant1,512 kernel dots and emitted-letter counts.
It needs only standard-library Python, not the numerical solver. The
root/target reachability dependency is the independently replayed full
graph certificate in `20260906_closed_block_potential_independent.json`.
All sources include exact parameters, full Git, timing and hardware/software
facts, and all result writes are atomic. No reference source was modified.
The compact `20260906_positive_circulation_final_audit.json` links the
reachability dependency hashes, verifies the independent kernel minor,
and records the exact constant primal and normalization/birth arithmetic.

Five fresh Muse attempts before this result returned provider429. The
lead performed the independent arithmetic and checked the proof through
both cycle-pumping and nonnegative-slack arguments. A sixth fresh
adversarial Muse review requested after the determinant1 result also
returned429. No other subagent model was used and no successful fresh
external proof review is claimed. The arithmetic implementations, exact
determinants and the two lead proof derivations remain distinct from such
an unavailable review.

The sixteen-state universal additive route is now closed, not merely
unrefuted by a finite list of examples. Do not refit its weights, enlarge
its coefficient box, rerun its fixed graph or revive its timed-out LP.
The whole-tail bottleneck remains a bound on ACTUAL returns that retains
prescribed age versus original length. A broader additive-memory claim
would need a structural all-memory proof, not another width sweep. The
positive-circulation counting identity suggests such a question but the
rank32 calculation alone proves nothing at larger memory. Nonlinear or
age-restricted potentials and the boundary-sum argument remain open.
