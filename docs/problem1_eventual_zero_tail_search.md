# Problem 1: eventual-zero reconstructed-tail search

Status: finite-exhaustive for the stated box; inconclusive for Problem 1.

## Question and admission criterion

The focused conjecture says that an eventually periodic center trace with
`c0=1` reconstructs an initial left half containing infinitely many ones. This
experiment is admitted because either outcome informs that whole-tail claim:

- a reconstructed prefix with no new one across a large extension interval is
  retained as a counterexample lead; or
- continued ones in every interval give exact finite evidence against an
  eventually-zero tail for the explicitly enumerated candidates.

Unlike the superseded first-witness searches, the experiment inspects complete
reconstructed prefixes. A first reconstructed one alone is only a trusted
center-prefix mismatch and is not the measured outcome here.

## Finite protocol

For every eventually periodic description with `q=0..4`, `p=1..8`, and
`c0=1`, the default campaign constructs the center trace through depth 2,048.
Descriptions producing the same complete finite trace are evaluated once with
exact multiplicity retained. For every distinct trace it independently
reconstructs at horizons

```text
64, 128, 256, 512, 1024, 2048
```

and verifies that every shorter result equals the corresponding prefix of the
depth-2,048 reconstruction.

At each checkpoint it records the terminal zero-run distribution and an
extremal candidate. Across each adjacent pair of checkpoints it counts traces
with no newly reconstructed one. The predeclared counterexample-lead rule is
no one in the final extension interval `(1024,2048]`. Such an outcome would
still require an exact infinite argument.

The campaign is deterministic, uses no randomness, emits bounded JSON, and
hashes every ordered finite trace and complete reconstructed prefix. Explicit
caps cover descriptions, distinct traces, horizon, logical work, and reported
candidates.

## Default campaign result

The 2026-07-22 default run exhausted 7,905 descriptions. Deduplication left
3,776 distinct finite trace classes and retained multiplicity for 4,129
duplicate descriptions. It completed 22,656 reconstructions and checked
18,880 shorter-prefix equalities. The conservative accounting charge was
31,675,262,976 logical cell updates; packed integer operations make this a
logical-work bound rather than an executed-instruction count.

Every one of the 3,776 trace classes contained a newly reconstructed one in
each tested extension interval:

```text
(64,128], (128,256], (256,512], (512,1024], (1024,2048]
```

The maximum terminal zero-run lengths at horizons 64, 128, 256, 512, 1,024,
and 2,048 were respectively 13, 16, 13, 12, 11, and 12. The corresponding
maximum internal zero runs after the first one were 19, 19, 19, 19, 19, and
22. The depth-2,048 internal-gap extremum came from canonical description
`q=4`, `p=8`, `code=0x35b`, meaning preperiod `1101` and period `10101100`
under the script's least-significant-bit-first description convention.

No predeclared counterexample lead survived. This does not establish a
uniform gap bound: the largest observed gap increased from 19 to 22, and the
candidate attaining it changed. The useful next question is whether periodic
temporal input forces a provable recurrence or obstruction in the spatial
tail, not whether another larger finite horizon also contains a one.

The scientific certificate over the ordered traces, multiplicities,
descriptions, and reconstructed prefixes is:

```text
e957c1c5b919eb115c1f354122b0b1fffb614e665062ee52edb8e30109657c27
```

The formatted standalone JSON had SHA-256
`899806101fe059e7d358041e21cf61c248f1d38897d4e678315c088e34119647`.
One conservative local run took 17.02 seconds wall time and 31,232 KiB maximum
resident memory. These performance figures are descriptive for this machine.

## Interpretation boundary

Even if every candidate contains a one in every tested interval, a final one
could still occur after depth 2,048 and be followed by an infinite zero tail.
The candidate box is finite. Therefore a zero lead count does not prove the
focused conjecture or Rule 30 center nonperiodicity.

Continuation is justified only if the extremal tails reveal a stable symbolic
pattern, bounded-gap mechanism, candidate invariant, or exact counterexample
lead. Merely increasing the horizon is prohibited by
[`problem1_focus_program.md`](problem1_focus_program.md).

The subsequent
[`whole-tail equivalence`](../proofs/informal/problem1_whole_tail_equivalence.md)
shows why this stopping rule matters: an eventually-zero reconstructed tail
is exactly a finite odd seed in the right-edge recurrence. The finite campaign
therefore probes a uniform strengthening of Problem 1 rather than a finite-state
reduction of it.

## Reproduction

```bash
cd /home/wryan/rule30-lab
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest \
  -p no:cacheprovider tests/python/test_eventual_zero_tail_search.py -q
nice -n 10 .venv/bin/python \
  experiments/problem1_nonperiodicity/search_eventual_zero_tail.py \
  > /tmp/rule30-eventual-zero-tail.json
sha256sum /tmp/rule30-eventual-zero-tail.json

rule30 experiment controlled -- \
  --profile interactive \
  --experiment-id p1-eventual-zero-tail-final-20260722 \
  problem1-eventual-zero-tail
```

The reviewed strict record is
`results/runs/p1-eventual-zero-tail-final-20260722.record.json`. It was
produced from clean commit `72376d40c075a07d36e2fafb09435e9718df2eb5`,
completed in 16.856332 seconds, and captured the same standalone JSON hash.
