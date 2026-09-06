# Review: activity-record return certificate (proof-only)

Status: independent reviewer; owns only this file. No computation was run; JSON summaries were inspected, not recomputed. The established finiteness review (`problem1_activity_finiteness_independent_review.md`, committed) is preserved unchanged. Lead compares full vector streams and writes verification separately; that comparison is outside this scope. No other workers were used.

Scope: admission `problem1_activity_return_nonincrease.md` plus the two named certificates (primary packed-int ordinary-history vectors; independent cell-array projected tail vectors). Objective: find any fatal flaw in the full-age maxima or in scope. Verdict is scoped to these artifacts only.

Sources reviewed (SHA256):
- proofs/informal/problem1_activity_return_nonincrease.md d2cebf65d24932014e4bbfb0b10aa2c906cd48689a9dbc0b80a1bac86f586e77 (current; admission read against original 9863cee6c7cf2412b0afd758b23f16dd1fe1fbe992ab141067e1c8b0acd2c8d3, retained as the reviewed version; the note delta after that read is not reviewed here)
- experiments/problem1_nonperiodicity/check_activity_return_nonincrease_primary.py c67470b68bff9a576f7dc5fcb96845e28f29f1417fc083bdf525c4f246b9010c
- results/problem1/20260906_activity_return_nonincrease_primary.json 199538a1cd1111bb054414a74effbf5fc64c1d46b668845e4e66e1f854473e0e
- experiments/problem1_nonperiodicity/check_activity_return_nonincrease_independent.py 65e1f42feadf8d668f0e9a713f83c8a463074ade7dc2237478acf725de2495e8
- results/problem1/20260906_activity_return_nonincrease_independent.json b175766eb452da2d5955ca90a89e96ab99b62bc057d33a1dda18a907e3e42e6b

## Admission and domain fidelity

The admitted domain is one fixed object: u18 state x0=0x6473d46ab with from-zero history uutuuttuupupuuupup, the ten observed forced branches ttttututut, the unobserved final u gate at time 10 confirmed but not executed, and the three-return block times 4..10 with gap tuple 222. Both certificates record the same parameters and orbit values with n=21 at x4 and n=27 at x10, but their contents differ: only the primary records prescribed letter histories; the independent holds no history arrays and instead reconstructs the endpoint orbit independently via cells (initial/repeated endpoint vectors, direct temporal vectors, projected tail scores). Agreement is on orbit values, indices, closures, and maxima; lead additionally matches the closures under vector reversal in the separate comparison. Return occurrence is discharged directly from the recorded 11 gates: states at times 4, 6, 8, 10 carry gate u (7 mod 16) with intervening states at 5, 7, 9 carrying t (11 mod 16), yielding three genuine returns of gap 2 each (4->6, 6->8, 8->10). This is read off the recorded orbits, not recomputed.

Root handling is exact in the primary: the first from-zero u maps 0 to the fixed root 1 (U(0)=A(1)=1), the remaining 17 nonroot letters replayed from root 1 reproduce x0, and every forced step rebuilds endpoints from letters with H-step endpoint/letter consistency asserted. Branch replay matches ttttututut gate by gate (7->u, 11->t with F=4A^2+3 asserted per step), and the final gate x10 mod 16 = 7 is tested without executing x11. No new state, branch, frontier level, occurrence, or cut enters either certificate; caps (120 s, 1 GiB, 65536 tail transitions per endpoint) were not reached.

## Full-age maxima, not horizon samples

Both certificates give all-age R via exact finite closure, not via failure to see larger values. Primary: for history length n, direct V_s for s=0..n+2 plus the A-orbit of the n prefix endpoints from age n to first repeat, with diagonal/tail agreement asserted at s=n..n+2. Independent: direct ages 0..n+2 plus its own projected w_d tail vector to its own closure. Each method therefore certifies its maximum over ALL ages s>=0 within its stated recurrence; the finite horizon alone is never the argument.

Recurrence indices confirmed: n=21 at x4, n=27 at x10 in both summaries. Maxima agree: R(x4)=13 with first maximizer age 21 (tail start), R(x10)=16 with first maximizer age 25 (direct, early since n=27). Primary closures (entry 32 cycle 8; entry 41 cycle 8) are consistent with independent all-closed true. The early-vs-eventual distinction is material only for reading the streams: x10's record is already attained at age 25, yet its all-age status still rests on the closed tail, which both methods supply independently.

## Sufficiency logic and limits of the failure

The candidate's force, had it held universally on admissible prescribed blocks, comes from finiteness of each E_K with bounded return gaps and at most +1 per single forced step: R would stay uniformly bounded along any infinite forced orbit, against degree growth. The named outcome R(x10)=16 > R(x4)=13 refutes the universal version on actual prescribed blocks, so that termination route is closed.

The failure is scoped: it does not disprove a survivor-only restriction (nonincrease along the actual infinite survivor, if one exists), exhibits no infinite survivor, and decides nothing about Problem 1. It also leaves the finite-level theorem and all prior closed vectors untouched.

## Reproducibility correction (payload hash)

Integration found the primary payload hash did not reload: integer history keys hashed numerically but reload as strings ("10" before "2"). Fixed in owned source only: history keys are now strings and the payload hash is taken over JSON-roundtripped canonical checks; reload now reproduces `primary_payload_sha256`. Scores, closures, and maxima unchanged (13 vs 16). No domain, cap, or independent-checker change.

## Verdict (final; lead verification PASSED)

Lead full verification passed (54 direct vectors, 41 tail scores, 11 states, 2 closed vectors; corrected primary hash reloads). No fatal flaw found in either certificate's full-age maxima or scope: histories, gates, closures, and maxima (13 vs 16) agree across the two independent recurrences within the admitted domain. The universal prescribed-block nonincrease is refuted on the named block; every stronger or survivor-restricted claim remains open and outside this review.
