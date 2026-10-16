# Rule 30 research checkpoint — 2026-10-16

Problem 1 remains OPEN. This continuation starts from
`c424346e1a6efdf7cdd673efeff4b6578fe830b6` on `research/sol-blind-frontier`.

New computer-assisted partial theorem: the cyclic blind-gate statement S_r
holds for every spatial depth 6 through 23, for ALL temporal presentation
periods. These depth numbers are not restrictions on the period. No parity
or nonzero-parent assumption is needed for this statement.

Read `proofs/informal/problem1_cyclic_reset_certificates_20261016.md`.
Run `experiments/problem1_nonperiodicity/certify_cyclic_resets_20261016.py`
with `generate`, then `verify --part prefix` and `verify --part segments`.
The summary is `results/problem1/20261016_cyclic_reset_summary.json`.

The new mechanism has three pieces: a certified necessary cyclic common
prefix 0111100, an all-width causal-cone reset criterion, and closed
first-return difference sets for the exceptional finite words. Independent
cell-by-cell verification passed 2,283,632 edge checks. Certificates with a
missing initial case or omitted depth were rejected. No Lean or full-repo
quality-gate run is claimed.

Depth 24 exploration hit the declared state cap for three words. It is
unresolved by this run, not refuted. The useful next problem is an all-width
inductive first-return certificate for the strengthened regular language,
not a larger temporal census. Some nonzero-difference closures have cycles;
closure and safe blind exits do not imply bounded reset time.

The original-support transport obstruction remains unchanged. Even an
all-depth S_r theorem is not a proof of center nonperiodicity. Keep the
same original finite seed when reasoning across resets and period doubling.
No prize submission or sponsor contact occurred. Source and proofs were
AI-assisted and checked by independently implemented code paths, not by an
independent human reviewer.
