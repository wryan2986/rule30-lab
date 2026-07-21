# Research status

Last updated: 2026-07-21.

## Verified implementation facts

- The supplied reference source is preserved unmodified at a recorded hash.
- The Windows-provided CUDA driver sees one RTX 2060 SUPER in WSL.
- Independent reference vectors have not yet passed the required three-way
  comparison.

## Reproduced empirical observations

None yet. Previously reported counts, discrepancies, linear complexities, and
2-kernel prefix results remain unverified claims.

## Finite exhaustive results

None yet.

## Partial mathematical results

- `partial-proof`: the center sequence cannot be eventually constant one. The
  local identity forces the adjacent-left column eventually zero, which would
  make the width-two trace eventually constant; Kopra's Corollary 3.7 (a modern
  route to Jen's width-two theorem) excludes this for Rule 30 and the
  single-cell seed. The exact theorem, hypotheses, deduction, and citations are
  recorded in `docs/theory_literature_review.md`. This does not exclude an
  all-zero tail or any period greater than one.

## Active conjectures

- The center sequence is not eventually periodic.
- Its limiting one-frequency exists and equals one half.
- The exact complexity question requires several separate formalizations; no
  lower-bound conjecture is adopted without a fixed model.

## Failed approaches

None recorded yet.

## Open questions

- Which exact published theorem, if any, discharges the width-two deduction?
- Can periodic-boundary sideways reconstruction be represented with a bounded
  state independent of reconstruction depth?
- Which precise Problem 3 formulation is intended by each published source?

## Potential next experiments

1. Freeze hand-derived rows and independently generated vectors.
2. Reproduce the million-bit discrepancy checkpoints.
3. Exhaust pure periods through 10 with an independently tested reconstruction.
4. Extend 2-kernel prefix diagnostics with held-out lengths.
5. Benchmark scalar cell-array versus packed row evolution before GPU work.
