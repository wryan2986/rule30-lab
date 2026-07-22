# Extended exact-model searches for Problem 3

These experiments enlarge the bounded model classes used to study the Rule 30
center bit `c_n`. They are finite counterexample searches, not proofs of
nonautomaticity and not computational lower bounds.

## Affine binary-digit matrix products

For state dimension `d`, a candidate has a state `s` in `GF(2)^d`. Reading the
canonical binary expansion of `n` most-significant bit first applies

```text
s <- A_b s + v_b
```

for each digit `b`. An affine functional of the final state emits one bit. The
enumeration includes the initial state, both matrices, both translations, the
output mask, and the output bias. Its canonical encoding therefore has

```text
2 d^2 + 4 d + 1
```

bits, giving 128 labeled models at dimension 1 and 131,072 at dimension 2.
This is a mathematically structured finite transducer family with at most
`2^d` states. It is not the class of all transducers with that many states.

Models are enumerated in `(dimension, model_id)` order. Exact training fits are
selected without reading held-out data. Only after enumeration terminates are
the selected candidates applied to the held-out interval, where the first
mismatch is reported with both decimal and binary index. Tests mutate held-out
bits and require the selected model IDs and all enumeration counts to remain
unchanged.

## Multiscale finite 2-kernel refinement

A sampled 2-kernel node `(e,r)` denotes the finite observations from

```text
c_(2^e m + r).
```

Refinement round `j` classifies nodes by their first `2^j` observations. The
diagnostic compares classes across every sampled level, rather than counting
distinct prefixes separately at one level. It records the class-count profile
as the witnessed prefix doubles, hashes a canonical finite distinction
certificate, and checks whether final classes are closed and congruent under
both child operations

```text
(e,r) -> (e+1,r)
(e,r) -> (e+1,r+2^e).
```

If this same-resolution check succeeds, the finite quotient is frozen as an
LSB-first DFAO and validated on held-out bits. Equality of finite signatures
does not imply equality of infinite subsequences. Conversely, unequal finite
signatures do witness that those particular sampled infinite subsequences are
different, assuming the input prefix is correct. A growing finite class count
still does not prove that the full 2-kernel is infinite.

## Deterministic campaign

Run the default 10,000-bit campaign with:

```bash
cd /home/wryan/rule30-lab
nice -n 10 .venv/bin/python \
  experiments/problem3_complexity/run_extended_model_searches.py \
  > /tmp/rule30-problem3-extended.json
```

The script writes JSON only to standard output. It uses no randomness or
timestamps. Its default searches are:

- the complete labeled affine dimensions 1 and 2 against training interval
  `[0,64)`, then held-out interval `[64,10000)` for selected training fits;
- the same complete affine range with the deliberately shorter training
  interval `[0,8)`, solely to exercise active first-counterexample discovery
  on `[8,10000)`;
- multiscale 2-kernel refinement through level 4, with seven refinements (128
  observations per sampled kernel element), built from `[0,5000)` and with any
  constructed quotient checked on `[5000,10000)`.

Every search includes exact model/node caps and machine-readable completion
flags. A cap-triggered partial affine enumeration has status `inconclusive`,
not `finite-exhaustive`. The same is true when the training-fit validation cap
is reached: enumeration completion and validation completion are separate JSON
flags, and the overall search is complete only when both are true.

### Default campaign observed on the trusted prefix

The deterministic default campaign completed in approximately 2.6 seconds on
the project machine. Two independent replays were byte-identical; the complete
pretty-printed JSON had SHA-256
`84fd11a8f8443d2481f5ea7b4a2941a3d8fb00ecd8ad40f4a510b49e969ebcd3`.
It produced these finite results:

- all 131,200 labeled affine models in dimensions 1 and 2 were checked against
  `[0,64)`; zero fit that training prefix, so there was no substantive affine
  candidate to validate on `[64,10000)`;
- the `[0,8)` counterexample-control split had exactly 192 training fits, all
  at dimension 2; the validation cap of 256 therefore covered every fit, and
  every one first failed at `n=8` (`1000` in binary), predicting 0 where the
  trusted center bit is 1;
- the multiscale kernel profile across all 31 nodes through level 4 had class
  counts `2, 4, 16, 28, 31, 31, 31, 31` for witnessed lengths
  `1, 2, 4, 8, 16, 32, 64, 128`;
- at 128 observations all 31 sampled nodes were distinct, witnessing 465
  distinct class pairs. The same-resolution quotient was not closed: the first
  deterministic witness was the digit-0 child `(level=5,residue=0)` of
  `(level=4,residue=0)`, whose class was absent from the level-0-through-4
  state set;
- the canonical finite distinction-certificate SHA-256 was
  `d983138f265cb2671e1364430613b194b9ed206efc10923f39336188a81c79fc`.

These are exact statements about the reported finite prefix and bounded model
sets only. In particular, the 31 distinct sampled kernel elements do not imply
that infinitely many kernel elements are distinct.

## Interpretation limits

- A training failure excludes only the enumerated affine model IDs on that
  finite training interval.
- A held-out failure refutes only that fixed candidate at the reported index.
- A held-out fit does not establish an exact formula for all `n`.
- A finite quotient conflict does not prove nonautomaticity.
- No result here distinguishes the published Problem 3 lower-bound
  formulations or proves any `o(n)` impossibility, `Omega(n)` bound, or literal
  no-`O(n)` statement.
