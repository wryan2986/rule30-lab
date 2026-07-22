# Repository instructions

This repository is a computational mathematics project, not a software demo.
Correctness, provenance, and reproducibility take priority over speed.

## Current critical path

The active research focus is Problem 1. New research work must directly bear
on the following whole-tail question:

> Can an eventually periodic center trace with `c_0 = 1` reconstruct an
> initial left half that is eventually zero?

Infrastructure, benchmarking, larger finite-prefix searches, Problems 2 and
3 parameter sweeps, and additional backend ports are frozen unless required
to test a concrete mathematical hypothesis on this critical path. In
particular, do not extend first-nonzero periodic-trace boxes: finite sideways
first witnesses are exactly trusted-prefix mismatches. See
`docs/problem1_focus_program.md` for admission and stopping criteria.

## Non-negotiable rules

1. Never edit `src/python/rule30_research_reference.py`. Its hash and source
   provenance are recorded beside it.
2. Do not accept an optimized backend until it matches shared vectors
   bit-for-bit, including boundary and partial-word cases.
3. Never present a finite experiment as proof of an infinite statement.
4. Every mathematical claim must carry one of the statuses defined in
   `docs/experiment_protocol.md`.
5. Problem 3 claims must state the machine model, input encoding, output,
   uniformity, preprocessing/advice, time unit, and memory model.
6. Generated results must include exact parameters, software/hardware facts,
   a full Git commit, timings, hashes, limitations, and an atomic write.
7. Keep workloads local to this computer. Do not add cloud, remote, or
   distributed execution.
8. Do not modify GPU clocks, voltage, power limits, drivers, or safety controls.
9. Before adding an experiment, state how either outcome would change the
   whole-tail argument. If neither outcome would, do not run it.

## Editing ownership

Parallel workers must use disjoint files or isolated worktrees. A worker owns
only the paths named in its assignment. Integrate and independently review
every contributed change before committing it.

## Verification order

Derive small cases by hand, compare two independent simple implementations,
freeze shared vectors, test optimized implementations, run sanitizers, and
only then benchmark or launch larger experiments.
