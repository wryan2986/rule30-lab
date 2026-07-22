# Problem 1: sideways reconstruction and prefix disagreement

Status date: 2026-07-21

## Result

For a finite proposed center trace with a fixed initial center bit and a zero
initial right half, the first nonzero bit recovered by sideways reconstruction
is exactly the first time the proposal differs from the center trace generated
by an all-zero initial left half. For `c0=1`, that reference is the true
single-cell Rule 30 center sequence.

The complete causal/permutivity argument is in
[`problem1_sideways_prefix_equivalence.md`](../proofs/informal/problem1_sideways_prefix_equivalence.md).
It is a rigorous finite lemma for arbitrary horizon, but it is not a proof that
the center sequence is nonperiodic.

## Independent finite checks

[`analyze_sideways_prefix_equivalence.py`](../experiments/problem1_nonperiodicity/analyze_sideways_prefix_equivalence.py)
checked every binary proposed trace at every horizon from 0 through 16, for
both possible initial center bits:

- 262,142 traces;
- 91,226,096 conservatively charged logical cell updates;
- zero disagreements between first reconstructed-one depth and first prefix
  mismatch;
- canonical case-certificate SHA-256
  `4d5014bc4acc68d8080ea5a3cbd4d3392f81c16a33bc4dd4b873a6d3bfbbb28f`.

At each horizon `H`, exactly two traces reconstructed an all-zero left prefix:
the zero-seed and single-seed reference traces. For each depth `d=1..H`, the
number of traces first differing at `d` was exactly `2 * 2**(H-d)`, accounting
for both initial center bits and every unrestricted later suffix.

The same tool then compared the trusted center prefix directly against every
eventually periodic description in the box `q=0..8`, `p=1..12`, `H=64`, with
`c0=1`:

- 2,092,545 descriptions checked;
- zero descriptions matching through the complete horizon;
- direct first-mismatch histogram identical to the CUDA reconstruction's
  description-level first-nonzero histogram at every depth 1 through 20;
- canonical description-certificate SHA-256
  `9248bbd4d7c9aa0fb5a242a0dd088a14629a8c5cbf98d727cae03938ba3c9460`.

The deterministic formatted JSON is 9,010 bytes with SHA-256
`1d530a4fa8f8e7f6da7692509a6d702035785e799aa2e20be3f5f798e518ea74`.

## Research consequence

The equivalence is both useful and cautionary:

- sideways reconstruction supplies exact local witnesses for a mismatching
  candidate;
- a search that records only the first reconstructed one is mathematically a
  prefix-comparison search in more expensive form;
- proving that every eventually periodic proposal reconstructs *some* one is
  equivalent to proving that the true center is not eventually periodic; and
- the nontrivial remaining route is to control the entire reconstructed tail,
  for example by showing it is not eventually zero.

The earlier depth-independent four-forbidden-block image subshift remains a
real structural fact, but it has not yet supplied the needed tail invariant.

## Reproduction

```bash
cd .
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest \
  -p no:cacheprovider tests/python/test_sideways_prefix_equivalence.py -q
nice -n 10 .venv/bin/python \
  experiments/problem1_nonperiodicity/analyze_sideways_prefix_equivalence.py \
  > /tmp/rule30-sideways-prefix-equivalence.json
sha256sum /tmp/rule30-sideways-prefix-equivalence.json
```

The test suite also independently reconstructs every description in a smaller
eventual-period box and compares that histogram with the direct-prefix path.
