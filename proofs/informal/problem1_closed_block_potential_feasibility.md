# Closed-block potential feasibility and an exact dual target

Status: `inconclusive` for the bounded feasibility solve; `partial-proof`
for the exact flow obstruction; `finite-exhaustive` for the graph
certificates. Problem1 remains open.
Base: `373685affc1ae3541eb4639cb2ae1a06e8e8723b`.

## Exact question and either-outcome gate

Does there exist a nonnegative real48-edge weight vector with strict
decrease for EVERY finite ordinary history from phase root1 whose endpoint
is50055 modulo65536, across the six actual branches ututut?

By `problem1_fixed_block_potential_decision.md`, this is equivalent to the
phase-u bounded-below class on this closed sublanguage. Failure is sufficient
to refute the full shared and phase-u sixteen-state strict-descent class.
Success settles this necessary subproblem only, not the other terminal
classes, phase p, the other gap triples, or Problem1.

Use exactly the signed65536-state graph and birth vector already derived.
Generate all196608 ordinary generator edges, then trim to root1 and
acceptance50055. This is the first full graph for SIGNED differences;
its width is mandated by the six-step pullback, not a census cap increase.
Require exact forward/backward graph reachability certificates if claiming
the whole graph is retained. Check packed formulas against independently
derived cell formulas on the16 small controls and the four known terminal
classes before solving. The existing eight vector checks remain fixed.

Normalize sum omega=1, omega>=0, and maximize a free real margin epsilon:

    h(q)>=d(q,g).omega+h(G_g(q)),
    h(50055)>=B(50055).omega+epsilon,
    h(1)<=0.

The normalized system is feasible at uniform omega=1/48: edge differences
have weight0 and the birth cost is1/8, so h=0,epsilon=-1/8 works.
It has positive optimum iff a strict potential exists. A single known
accepted word bounds the optimum above; no unbounded optimum is expected.

Admit one local numerical linear solve using an isolated temporary SciPy
installation; no repository dependency or backend changes. Numerical
feasibility/infeasibility is ONLY a lead. Adopt a result only after exact
integer/rational checking of all constraints or of an LP dual certificate.
If exact conversion fails, record inconclusive and retain the compact
diagnostic, without changing the graph, adding witnesses or raising caps.

Limits: one solver thread, CPU120s, wall180s,1GiB address space for the
solve, plus1GiB final output limit; stop at the first solved/limited run.
Package download/install is separate and is not mathematical computation.
Record source, parameters, full Git, hardware/software, package hashes,
timing, exact witness/certificate data and limitations by atomic writes.
Require independent arithmetic replay of any adopted certificate; retry
the exact Muse model for external review, never substitute another model.

## Exact flow obstruction (`partial-proof`)

A prospective dual certificate has nonnegative rational flow f on the
trimmed graph, with outgoing-minus-incoming divergence
delta_1-delta_50055. Set

    D=sum_e f(e)*d(e)+B(50055).

If D is componentwise nonnegative, no nonnegative weight vector can give
strict decrease on every accepted history. To prove this, suppose omega
did. Every cycle reachable from the root and able to reach the target
must have nonpositive omega.d weight, by pumping it inside an accepted
path. Decompose the finite unit flow into nonnegative cycles and
root-to-target paths with path coefficients summing to1. Each path plus
B has strictly negative weight, while each cycle has nonpositive weight.
Thus omega.D<0, contradicting omega>=0 and D>=0.

Cycles need not be attached to the flow's path IN ITS SUPPORT: verified
reachability and coaccessibility in the full graph suffice for the pumping
argument. This decomposition concerns actual generator paths and the
universal all-history potential claim. It does not splice endpoints in a
signed belief or identify word multiplicity with distinct-endpoint mass.
The proof works for arbitrary real omega, including irrational values.

The LP dual is a source of such flows, but the exact certificate can be
verified without trusting a solver or invoking numerical infeasibility.
For a rational denominator d, verify nonnegative INTEGER flow, divergence
d*(delta_1-delta_50055), and sum f_integer(e)*d(e)+d*B>=0 using exact
integers. Through the closed-block gauge theorem, this would also rule
out all fixed REAL sixteen-state weights bounded below on ordinary
phase-u histories, including negative individual edge weights.

A second derivation uses the finite h certificate from the decision
theorem. Multiplying every edge inequality by f(e) and summing gives
omega.sum f*d <= h(1)-h(50055). Adding the birth term gives omega.D<=-1
after margin normalization. This contradicts D>=0,omega>=0 directly,
without selecting a particular flow decomposition.

## Completed bounded outcome

The admitted solve ended at its110s internal limit after82655 iterations,
with no returned primal vector, dual vector, objective value or exact
certificate. Total run time was111.288s (CPU111.219s). This is
`inconclusive`, not numerical or exact infeasibility. No second solve,
larger cap or alternative solver was run.

The sparse system had65585 variables,196610 inequality rows, one
normalization equality, and778245 inequality-matrix nonzeros. SciPy1.18.1
and the existing NumPy2.3.5 were used locally; SciPy's downloaded wheel
hash is retained. The temporary installation is outside the repository
and installation/download time is separate from mathematical run time.
The threads=1 option was passed through to HiGHS; the SciPy forwarding
warning was informational, not a successful- or failed-solve certificate.

The retained graph certificates prove that all65536 vertices are reachable
from root1 and can reach50055, so trimming removes none. Independent cell
arithmetic verifies every one of the131070 nonroot parent/next edges, and
an independent functional-tree check verifies every chain ends at its
designated root or target. The maximum stored tree depths are21 forward
and20 reverse; no new distance-minimality assertion is needed. The stored
accepting tree path is tttuttpupuuttt from root1, with endpoint0x191cc387,
an already known endpoint. Recovering that path is certificate inspection,
not another ordinary-word search.

Records: `results/problem1/20260906_closed_block_potential_` followed by
`{primary,independent}.json`. Exact source, full Git, input and compressed
array hashes, software/hardware, timestamps and timings are preserved
with atomic writes. The primary interpretation string retained its
initialization placeholder; its completed numerical fields explicitly
record the time limit. The independent record clarifies this without
silently rewriting raw bytes. No optimum or certificate is hidden behind
that placeholder. The fourth attempted fresh Muse review returned429;
the lead performed independent cell verification and the second dual
derivation locally. No model substitution or successful fresh external
review is claimed.

## Exact remaining obstruction and next directions

The finite feasibility problem remains undecided. A compact rational
unit-flow certificate with nonnegative D would close the entire phase-u
bounded-below sixteen-state universal strict-descent class. Conversely,
an exact primal omega,h certificate would establish the closed-subclass
gate only. Neither is currently available.

Do not restart this same numerical solve or merely raise its time limit.
A further computational pass needs a structural reduction, such as a
proved compression of admissible flow cycles, that makes an exact
certificate accessible. This is a proposed direction, not an established
compression theorem. The materially different mathematical route is the
existing boundary-sum inequality retaining prescribed age versus ORIGINAL
length; unrestricted potentials and literal H^6-fixed histories do not
supply that restriction. Actual return exclusion, B_all, eventual-period
two exclusion and Problem1 remain unresolved.
