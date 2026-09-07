# Round306 lead review and verification limits

Status: `partial-proof` for accepted conditional deductions; local tests are
`finite-exhaustive` only on their declared inputs. No new `rigorous-proof`
status is assigned. Problem 1 remains OPEN.

## 1. External review attempts

The incoming shadow-gate/one-bit-exit review was assigned read-only to
`opencode-go/muse-spark-1.3-contributor`, thread
`01a07b76-3648-75b1-81f9-796b6893e2c6`. It failed before review text with
`MissingSessionID`: missing `x-opencode-session`. The thread was closed.

A fresh adversarial review of the NEW two-bit-collapse theorem was assigned
read-only to the same requested model, thread
`01a07b83-13c1-7e31-946c-22d09696f35d`. Its explicit goal was to find a fatal
flaw in the odd-doubling obstruction, exit escalation, or infinite induction.
It failed before review text with the same `MissingSessionID`; it too was
closed. Neither failure was a 429. MiMo was not advertised. No native or
other model was substituted, and no provider settings were changed.

Thus external review is missing for both the incoming notes and the new
theorem. The derivations below are lead checks, not reviews attributed to
either failed worker. There are no worker-authored changes to integrate.

## 2. Two-bit-collapse dispositions

Reviewed source: `problem1_two_bit_strip_collapse.md`.

* The even four-bit identity uses the actual centers through three further
  physical steps and the actual right-pair gate. It imposes no FULL values
  on the shadow.
* At an odd doubling the zero trace is along ONE moving characteristic.
  At the next even row it becomes the identically-zero HIGH A-trace.
  Assuming b<=2 makes bits 2 and 3 common and forces the next high shadow
  bit to be 1, a contradiction. This proves b>=3 there, not tau>=3 at
  the odd source. A row can have spatial discrepancy deeper than its delay.
* The one-bit exit table supplies agreement at every position<=-2 and
  disagreement at -1 at its next even row. Actual no-uu makes that row's
  gate t, hence its shared -2 bit is zero. One physical step then gives
  EXACT b=3; all still-further-left cones agree. No shadow center is needed.
* The invariant-region induction uses the eventual b<=2 premise at that
  additional odd time. Removing this future premise would invalidate the
  induction. Every intervening odd negative half is shielded by the common
  even left neighbor 1.
* The all-depth entry argument chooses a common late cutoff for tau<=2
  and b<=2. Unbounded clocks give a doubling beyond that cutoff; the new
  odd-doubling obstruction makes it even. The imported two-step result
  really assumes tau at that source is at most TWO, ensuring the upper
  row in the second extension is cyclic. Its unique cyclic low bit is 1,
  which matches the actual second even center. This supplies the cyclic
  start for the induction.
* Only after obtaining eventual b<=1 is threshold transport used to get
  eventual tau<=1. No row-wise identity b=tau, bounded period, uniform
  time to the next doubling, finite birth supply, or general induction on
  K has entered. The reverse implication is immediate.

Disposition: accept these deductions at `partial-proof` scope. They reduce
eventual K=2 to eventual K=1 for the single finite FULL orbit, and leave
existence or exclusion of that orbit unresolved.

## 3. Fixed checker audit

`check_round306_two_bit_collapse.py` freezes all eight Rule30 truth-table
values, then compares direct truth-table physical evolution with a separate
packed A-cut calculation on all sixteen declared assignments. Four check
the odd-doubling contradiction and twelve check the post-exit third bit.
The tests do not construct E shadows or infinite FULL sources and do not
search a neighborhood for a pattern.

The initial shell invocation used unavailable `python` and did not run the
checker. The successful invocation was `python3`; its atomic record is
`results/problem1/20260907_round306_two_bit_collapse.json`. All declared
10-second/128-MiB caps passed. The six current source hashes and canonical
payload hash were independently recalculated after execution and matched.
The record names the full pre-change base commit and hashes the new sources,
so their then-uncommitted state is explicit rather than concealed.

The immutable reference hash remains
`358bdc07904e77080eb78b67bdd8da25822d6b51f1a91b58b5313dfe461c1d01`.
No optimized backend, new benchmark, broad regression campaign, reference
edit, remote computation, or hardware change was involved.
