# Repository instructions

This repository is a computational mathematics project, not a software demo.
Correctness, provenance, and reproducibility take priority over speed.

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

## Editing ownership

Parallel workers must use disjoint files or isolated worktrees. A worker owns
only the paths named in its assignment. Integrate and independently review
every contributed change before committing it.

## Verification order

Derive small cases by hand, compare two independent simple implementations,
freeze shared vectors, test optimized implementations, run sanitizers, and
only then benchmark or launch larger experiments.
