# Bounded Problem 1 experiments

`run_sideways_search.py` emits deterministic JSON to standard output. It
checks pure-period and preperiod-plus-period descriptions with exact finite
parameters, validates the trusted true center trace by sideways reconstruction,
and summarizes explicitly fixed-width state graphs.

Default run:

```bash
cd .
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python \
  experiments/problem1_nonperiodicity/run_sideways_search.py \
  > /tmp/rule30-problem1-sideways-default.json
```

The JSON includes compact first-failure certificates and labels the result
`finite-exhaustive`. It does not claim eventual nonperiodicity.

See [`docs/problem1_sideways_research.md`](../../docs/problem1_sideways_research.md)
for conventions, validation, exact default results, and limitations.

Focused exact analyzers support the current right-edge proof work:

```bash
cd .
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python \
  experiments/problem1_nonperiodicity/analyze_period_defect.py
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python \
  experiments/problem1_nonperiodicity/analyze_two_adic_diagonal.py
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python \
  experiments/problem1_nonperiodicity/analyze_period_two.py
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python \
  experiments/problem1_nonperiodicity/analyze_inverse_lift_sections.py
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python \
  experiments/problem1_nonperiodicity/analyze_period_two_quotient.py
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python \
  experiments/problem1_nonperiodicity/analyze_period_two_renewal.py
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python \
  experiments/problem1_nonperiodicity/analyze_period_two_2adic_zero_countermodels.py
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python \
  experiments/problem1_nonperiodicity/analyze_period_two_schedule_survivor.py
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python \
  experiments/problem1_nonperiodicity/analyze_period_two_schedule_coding.py
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python \
  experiments/problem1_nonperiodicity/analyze_period_two_fringe_language.py
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python \
  experiments/problem1_nonperiodicity/analyze_period_two_first_return.py
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python \
  experiments/problem1_nonperiodicity/analyze_period_two_frontier_gluing.py
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python \
  experiments/problem1_nonperiodicity/analyze_period_two_global_transducer.py
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python \
  experiments/problem1_nonperiodicity/analyze_period_two_coupled_strip.py
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python \
  experiments/problem1_nonperiodicity/analyze_period_two_quadratic_parity.py
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python \
  experiments/problem1_nonperiodicity/analyze_period_two_arrangement_cocycles.py
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python \
  experiments/problem1_nonperiodicity/analyze_period_two_dual_multiscale.py
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python \
  experiments/problem1_nonperiodicity/analyze_period_two_multitime_bulk.py
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python \
  experiments/problem1_nonperiodicity/analyze_period_two_characteristic_front.py
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python \
  experiments/problem1_nonperiodicity/analyze_period_two_terminal_order.py
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python \
  experiments/problem1_nonperiodicity/analyze_period_two_dual_cut.py
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python \
  experiments/problem1_nonperiodicity/analyze_period_two_zero_phase.py
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python \
  experiments/problem1_nonperiodicity/analyze_period_two_phase_universality.py
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python \
  experiments/problem1_nonperiodicity/analyze_period_two_witness_complexity.py
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python \
  experiments/problem1_nonperiodicity/analyze_period_two_arithmetic_quotient.py
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python \
  experiments/problem1_nonperiodicity/analyze_period_two_canonical_relations.py
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python \
  experiments/problem1_nonperiodicity/analyze_period_two_complete_local_quotient.py
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python \
  experiments/problem1_nonperiodicity/analyze_period_two_actual_witness_distance.py

g++ -O3 -std=c++20 \
  experiments/problem1_nonperiodicity/analyze_period_two_arithmetic_quotient.cpp \
  -o /tmp/rule30-arithmetic-quotient && /tmp/rule30-arithmetic-quotient 26

g++ -O3 -std=c++20 \
  experiments/problem1_nonperiodicity/analyze_period_two_complete_local_quotient.cpp \
  -o /tmp/rule30-complete-local-quotient && /tmp/rule30-complete-local-quotient

g++ -O3 -std=c++20 \
  experiments/problem1_nonperiodicity/analyze_period_two_actual_witness_distance.cpp \
  -o /tmp/rule30-actual-witness-distance && \
  /tmp/rule30-actual-witness-distance 12 20
```

The first exhausts each listed radius-`p` Boolean cone for the condition
`c_(t+p)=c_t`. The second exhausts finite 2-adic quotient maps and checks the
exact `-1/3,1/3` countermodel. The third audits three concrete mechanisms for
the smallest unresolved period, two. The fourth checks the exact inverse-lift
section recurrence. The fifth refutes three resulting finite quotient
candidates and verifies an exact arithmetic support criterion. The sixth
checks the exact renewal law and reduces any final zero streak to a partial
ordinary-integer recurrence controlled modulo 16. The seventh verifies two
rational 2-adic fixed points of that partial map and the linear shadowing bound
for their finite truncations. The eighth constructs the unique zero survivor
for the actual future moving-fringe schedule, proves the exact mismatch
valuation law, identifies the shift-zero survivor with the alternating inverse
lift, and emits its coupled output-pair transducer. The ninth verifies the exact
first-difference schedule coding, finite cylinder counts, ordinary degree law,
and the 304-bit consequence of the actual seven-block periodic shadow. The tenth
checks the autonomous packed fringe map, identifies the branch sequence with
the even-time cell-minus-two trace, and proves the all-time forbidden words
`uu`, `ttttt`, and `ututtu` from complete local dependency cones. The eleventh
derives the exact four-bit first-return selector at `u` events, the four
variable-length survivor return cylinders, and the shared neutral degree
cocycle. The twelfth proves the finite-prefix frontier-gluing obstruction:
return cylinders constrain only low bits, while arbitrary high fronts and free
middle words remain compatible. The thirteenth gives the exact four-state
right-to-left transducer for the complete growing inverse word, proves that all
single-letter additive cocycles are trivial, and records a branch word showing
that the three known short schedule exclusions alone do not bound zero-pair
runs. The fourteenth identifies the fringe and survivor as the two halves of
one moving right-edge row, verifies the exact width-growing coupled transfer,
and completely classifies the universal rational nearest-neighbor coupled
cocycle ansatz. The fifteenth exactly eliminates quadratic `GF(2)` cocycles
built from factor-count parities through range three and proves that their
terminal-pair potential is forced constant, even with an arbitrary exact-fringe
state potential. The sixteenth closes geometric position-weighted and
invertible ordered-product edge cocycles. The seventeenth proves that the
invertible dual is self-replicating and level-transitive on every scan-state
level, then measures maximal section growth on the actual period-two word
through depth eight. The eighteenth proves that every fixed-lag two-seam
transfer has a branch-independent radius-two bulk, exact radius-`2k` causal
cones, and constructive block surjectivity from iterated right permutivity.
The nineteenth identifies the opposite characteristic frontier with an exact
shifted Rule 30 evolution and proves that every fixed high-front window is
eventually periodic with a power-of-two period. The twentieth proves the exact
nonlinear terminal-zero/leading-`t` order cocycle across the complete word and
reformulates finite support as eventual unit-slope growth of that order. The
twenty-first proves the exact all-depth past/future factorization: the terminal
pair word after a cut is the dual action of the complete past accumulated word
on a state word generated solely by the future schedule. A length-`L` zero run
is exactly a depth-`L` match with the unique past preimage of `00^L`. Its
bounded actual-orbit campaign records runs through length five, while an
independent 20,000-block extension finds a length-six run. The twenty-second
proves that the terminal pair determines the next word head, derives the exact
zero-step deletion recurrence, and shows that every zero island has a fixed
`p` or `u` phase equal to the normalized ordinary state's bit-length parity. A
final zero tail must therefore stay forever in one of two fixed terminal
fibers. The twenty-third proves that positive dual level transitivity and
finite-order phase padding let both fixed phases realize every finite future
driver. Thus no finite forbidden branch word, finite dual depth, or finite
phase cylinder can settle the final-tail problem. The twenty-fourth defines
minimum phase witness complexity, proves its monotonicity and exact boundedness
criterion, derives finite-word counting and almost-sure linear lower bounds,
and records exact actual-prefix values through depth ten. The twenty-fifth
factors normalized words through their ordinary arithmetic states, proves a
Pell-growth bound with rate `1+sqrt(2)`, improves the almost-sure complexity
constant to `log(2)/log(1+sqrt(2))`, and extends exact actual-prefix exclusions
through normalized length 26. The twenty-sixth proves three state-conditioned
arithmetic relations, constructs a terminating canonical reduction and a
six-state automaton with growth root given by
`lambda^3-2 lambda^2-lambda+1`, and improves the generic almost-sure complexity
constant to `log(2)/log(lambda)`. The twenty-seventh constructs complete local
same-length relation tables through span five and proves by an exact 112-step
row-sum certificate that the canonical witness language has growth rate below
two. The twenty-eighth identifies phase witness complexity with directed
positive-generator distance to the actual survivor residue modulo `4^L` and
uses sparse bidirectional search to compute both phase distances exactly
through depth twenty. Their JSON status is `finite-exhaustive` or
`partial-proof`; the all-width arguments are separately stated in
`proofs/informal/` and no analyzer proves center nonperiodicity.

Tracked results are:

- `results/problem1/20260722_period_two_renewal_reduction.json`
- `results/problem1/20260722_period_two_2adic_zero_countermodels.json`
- `results/problem1/20260722_period_two_schedule_survivor.json`
- `results/problem1/20260722_period_two_schedule_coding.json`
- `results/problem1/20260722_period_two_fringe_language.json`
- `results/problem1/20260722_period_two_first_return.json`
- `results/problem1/20260722_period_two_frontier_gluing.json`
- `results/problem1/20260722_period_two_global_transducer.json`
- `results/problem1/20260722_period_two_coupled_strip.json`
- `results/problem1/20260722_period_two_quadratic_parity.json`
- `results/problem1/20260723_period_two_dual_multiscale.json`
- `results/problem1/20260723_period_two_multitime_bulk.json`
- `results/problem1/20260723_period_two_characteristic_front.json`
- `results/problem1/20260723_period_two_terminal_order.json`
- `results/problem1/20260723_period_two_dual_cut.json`
- `results/problem1/20260723_period_two_zero_phase.json`
- `results/problem1/20260723_period_two_phase_universality.json`
- `results/problem1/20260724_period_two_witness_complexity.json`
- `results/problem1/20260724_period_two_arithmetic_quotient.json`
- `results/problem1/20260724_period_two_canonical_relations.json`
- `results/problem1/20260724_period_two_complete_local_quotient.json`
- `results/problem1/20260724_period_two_actual_witness_distance.json`

The original controlled-run records contain machine-local operational metadata
and are intentionally untracked. Public certificate hashes, source commits,
direct reproduction commands, and scope statements are stored in
[`docs/public_provenance/20260722_controlled_run_manifest.json`](../../docs/public_provenance/20260722_controlled_run_manifest.json)
under these entries:

- `p1-period-defect-20260722`
- `p1-two-adic-diagonal-20260722`
- `p1-period-two-audit-20260722`
- `p1-inverse-lift-sections-20260722`
- `p1-period-two-quotient-20260722`
