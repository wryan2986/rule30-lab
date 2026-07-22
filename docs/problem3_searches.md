# Problem 3 bounded exact searches

These tools search finite model classes against a finite Rule 30 center prefix.
They do not prove nonautomaticity, exclude other exact representations, or
establish a computational lower bound. A model that survives held-out testing
is likewise not proved correct for every index.

The three interpretations of Problem 3 remain separate in
`problem3_sublinear.md`, `problem3_linear_lower_bound.md`, and
`problem3_published_formula.md`.

## Shared protocol

Every search uses indices `n >= 0`, one output bit `c_n`, and the canonical
binary encoding of `n` with no leading zeroes and with `n = 0` encoded as the
single digit `0`. Each report states whether digits are consumed most- or
least-significant first. Recurrence generators do not consume the binary input;
their report still records the convention and says that `n` is an implicit
sequential counter.

The data split is always a strict pair of half-open intervals:

- training: `[0, train_length)`;
- held out: `[train_length, sample_count)`.

Enumeration, fitting, model selection, and completion-table choices use only
training bits. A fixed candidate is then tested against held-out bits. DFAO and
linear-recurrence validation compares exact recurrence equalities against the
observed sequence; the first failure occurs before any post-error history choice
can matter. Nonlinear recurrences use autonomous rollout from the observed
training boundary, so a prediction error is fed back into subsequent model
state instead of silently replacing it with the observed held-out bit.

No search uses randomness; every report records seed `0` as a deterministic
placeholder. The training-derived automaton, coefficients, initial bits, or
truth table are finite-prefix advice. They are not a uniform algorithm for the
prize problem unless a separate proof establishes correctness for every `n`.

## Searched model classes

| Search | Exact bounded model | Index handling | Single-query cost if the fixed model were valid |
| --- | --- | --- | --- |
| Labeled DFAO | Complete deterministic binary automaton with `q` labeled states, initial state 0, two transitions and one output bit per state | MSB first | `O(log(n+1))` transitions, `O(log q)` state bits |
| Finite 2-kernel quotient | DFAO formed by exact equality of fixed-length sampled 2-kernel fingerprints | LSB first | `O(log(n+1))` transitions, `O(log q)` state bits |
| Homogeneous GF(2) recurrence | `c_n = XOR(a_j AND c_(n-j))`, canonical exact order at most `L` | Sequential validation | `O(nL)` sequentially; a separately proved fixed recurrence admits matrix exponentiation |
| Boolean window recurrence | Arbitrary table `f:{0,1}^w -> {0,1}` with `c_n=f(c_(n-w),...,c_(n-1))` | Sequential validation | `O(n)` in the implemented evaluator; a globally valid fixed table would permit finite-state cycle preprocessing |

The costs in the last column describe evaluation of a fixed table. Search time,
training-derived advice, and the unproved extension from a finite prefix are
separate issues. Each JSON result gives search time, search space, query time,
and query space in its stated deterministic table/bit-operation model. No
benchmark or failed fit is interpreted as a lower bound.

### Labeled DFAO enumeration

For `q` states, the exact labeled search space has

```text
2^q * q^(2q)
```

models. State labels are intentionally significant, so isomorphic relabelings
can appear more than once. The low `q` bits of `model_id` encode state outputs;
the remaining base-`q` digits encode transitions in `(state, input_digit)`
order. This makes `(state_count, model_id)` a stable resume checkpoint.

An exhaustive no-fit result excludes only the enumerated state counts and model
IDs on the training prefix. A training-fit model is frozen before validation,
and its first held-out counterexample records the decimal index, canonical
binary index, expected bit, and predicted bit.

### Finite 2-kernel quotient

A node `(k,r)` represents the sampled subsequence

```text
c[2^k m + r],  m = 0, 1, ..., fingerprint_length - 1.
```

Nodes through the selected depth are merged only when their complete sampled
fingerprints are byte-for-byte equal. Reading a low-order input digit `b`
moves `(k,r)` to `(k+1, r + b*2^k)`, which explains the LSB-first convention.
The construction accepts a closed DFAO only if every observed child fingerprint
matches an existing class and equal parent classes induce identical child
classes for both digits.

A closure or transition-consistency failure refutes only this finite
fingerprint quotient. Finite fingerprints are not infinite subsequences, so the
failure is not evidence of nonautomaticity by itself.

### GF(2) recurrences

The exhaustive short search uses one canonical identifier per homogeneous
exact-order recurrence. ID `0` is the order-zero all-zero predictor. For a
positive ID, `bit_length(ID)` is the order, the highest-lag coefficient is one,
and lower identifier bits encode the remaining coefficients. Thus all orders
through `L` contain exactly `2^L` candidate IDs and can be resumed at
`start_candidate_id`.

The separate Berlekamp--Massey fit uses only the training prefix, then actively
looks for its first held-out failure. It is a data-dependent candidate rather
than an exhaustive search over unbounded orders.

### Nonlinear Boolean recurrences

For each window width, training contexts constrain entries in an arbitrary
Boolean truth table. If the same context has two different following bits, the
two indices are an exact finite witness excluding every table at that width on
that training prefix. Otherwise, outputs for unseen contexts are enumerated in
ascending-context order. `completion_id` bits assign those outputs and provide
a stable checkpoint.

Truth-table entries, unseen contexts, enumerated completions, reported tables,
and errors are separately capped. A cap produces `inconclusive` with a resume
checkpoint, not a no-model claim.

A fixed width-`w` recurrence is a finite-state generator and is therefore
eventually periodic. If such a candidate were independently proved globally,
one could preprocess its at most `2^w` states into transient/cycle data and use
the binary index to skip ahead. The current validator deliberately implements
the simpler sequential rollout and makes no global recurrence or shortcut
claim.

## Trusted-prefix experiment

Run the deterministic experiment payload with:

```bash
cd /home/wryan/rule30-lab
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python \
  experiments/problem3_complexity/run_exact_searches.py
```

The default input is the trusted 10,000-bit byte vector with SHA-256
`61de1c97dc3f80cb24d3a02207920bd442d6f530304497eee70189a039a47860`.
The strict split trains on `c_0` through `c_4999` and validates on `c_5000`
through `c_9999`.

The default run produced these exact finite results:

- all 5,898 labeled complete DFAOs with one through three states were checked;
  none fit all 5,000 training bits;
- the depth-5, 64-bit-fingerprint 2-kernel construction produced 63 sampled
  classes but was not closed: state 31, represented by `(level=5,residue=0)`,
  has a digit-0 child `(level=6,residue=0)` whose fingerprint matches no
  existing class;
- all 4,096 canonical homogeneous GF(2) recurrences of orders zero through 12
  were checked; none fit all training bits;
- Berlekamp--Massey fitted an order-2,500 recurrence to the training prefix;
  its first held-out failure was `n=5003` (binary `1001110001011`), where the
  expected bit was 1 and the prediction was 0;
- every Boolean suffix-window width from 1 through 12 had a repeated training
  context with conflicting next bits, giving an exact finite exclusion witness
  for each corresponding truth-table class on the training prefix.

The pretty-printed default JSON payload, including its final newline and the
absolute input path shown above, was 115,441 bytes with SHA-256
`77b0c99eebc0503201cd550d111c6fcbd739692d749faa92ea2688134da51d2a`.
The hash is a reproducibility check for this code and local path, not a
mathematical claim.

These outcomes have status `finite-exhaustive` only for the explicitly bounded
model sets and finite comparisons. They do not show that the center sequence is
nonautomatic, has no recurrence, or requires linear time.

## Resource caps and resume points

The DFAO search caps models, state count, and encoded input symbols. Its
checkpoint is `(next_state_count, next_model_id)`. The GF(2) checkpoint is
`next_candidate_id`, with a separate recurrence-order cap. The nonlinear checkpoint is
`(next_window, next_completion_id)` and has separate caps on table size and the
number of unconstrained contexts. The 2-kernel construction caps sampled nodes
and aggregate fingerprint bytes before allocation.

Example of a small resumable DFAO chunk:

```bash
.venv/bin/python experiments/problem3_complexity/run_exact_searches.py \
  --dfao-max-states 4 \
  --dfao-max-models 10000
```

Pass the reported DFAO checkpoint back through `--dfao-start-state` and
`--dfao-start-model-id`. Equivalent `--gf2-start-candidate-id`,
`--boolean-start-window`, and `--boolean-start-completion-id` options resume the
other enumerations. A resumed suffix is exact for its reported ID interval, but
only a run beginning at the bounded-space origin can claim full bounded
exhaustion.

## Reproduction tests

```bash
cd /home/wryan/rule30-lab
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest \
  -p no:cacheprovider tests/python/test_predictor_search.py
```

The tests include independent exhaustive oracles for all labeled one- and
two-state DFAOs, canonical GF(2) candidates through order three, and all truth
tables at a two-bit recurrence window. They also verify strict split isolation,
active first-counterexample reporting, LSB-first 2-kernel behavior on the
Thue--Morse sequence, autonomous nonlinear rollout, deterministic trusted-vector
payloads, resource-cap failures, and exact checkpoint partitioning.
