# Source-based adversarial review: bounded-lag doubling controls

Objective: find a fatal flaw. None found. Standing `partial-proof` route-block sustained;
Sec-3 `refuted` applies solely to the hypothetical universal bound as formulated in (7).
No rigorous-proof claim is made or planned. No machine run, hand check only.

Reviewed file: proofs/informal/problem1_bounded_lag_doubling_controls.md
FINAL hash: sha256 d45a965818b4d4c89dc4453719724a6da4bf62edcd8c5b532618b2a42e2875e5
git hash-object b6bb686dbf6cc82f8f0eea4e22be23ed4d78a98c, 8039 bytes, mtime 2026-09-07 00:48 UTC.
(A pre-header draft reviewed 2026-09-07T00:47:52Z carried sha256 f9ecdd8d...; the only
change since is the header finalization to neutral verification-record references;
Sections 1-4 re-verified identical in the final file.)
Final-hash verification 2026-09-07T00:48:54Z; reviewer model
opencode-go/muse-spark-1.3-contributor; thread ID 01a0794c-5067-7e52-82c3-5f0904605ecc.
Notation lock: b = (2,0,u) is the DRIVE (not permitted); s = (3,2,b) the permitted
SOURCE; c = Gs the OUTPUT.

## Withdrawn reviewer error (explicit)

A prior review version asserted in C11 that s not eventually zero implies x cannot be
finite, via the false premise that finite x forces eventually-zero Theta. WITHDRAWN:
temporal Theta was conflated with spatial digits -- e.g. finite x = 1 has
Theta(1) = 1^infinity, and the finite cycle codes u here are nonzero periodic. Correct
replacement: the construction leaves x finite-or-infinite undetermined; only "may be
infinite at time zero" follows. Consequence unchanged and matching the source's own
correct weaker statement: no finite-x counterexample is supplied, so local bounds
restricted to initially finite x are untouched. The source never made the withdrawn claim.

## Corrected import dispositions

C3 (z finite): needs ONLY "A maps finite to finite" -- z = A^k(4^m) with 4^m finite
positive, via imported positive bit-length preservation
(`problem1_inverse_scan_reset_language.md` l.177). No width argument is used. z > 0
follows from that same preservation along the orbit (no injectivity claim on A is made).
C5 (x = Theta^{-1}(s)): CLOSED, not a flag. Theta as computable homeomorphism from Z_2
is an existing import (`problem1_activity_sparse_temporal_codes.md` l.34).

## Check results

C1 supply of doubling inputs: PASS. Seed x = 1 is nonzero finite-entry with zero fringe,
so the no-FULL growth theorem applies; nonzero cycle-code tails (z > 0 above) exclude the
all-zero row, giving monotone periods, infinite doublings, and unbounded source periods;
rotation of the tail preserves alphabet, odd count, and least period. C2 pure completion:
PASS (both conjugacy directions plus Theta injectivity). C4 entry identity A^4 x = z:
PASS in temporal-shift form. C6 tau(s) <= 4, p(s) = p: PASS. C7 tau(c) <= 2, p(c) = 2p:
PASS, re-derived including singleton edges; divisibility attribution exact (Phi gives
p | q, available 2p gives q | 2p, swap excludes p). C8 c_2 = 1 in both pairs: PASS.
C9 D_0 = D_1 = D_2 = 3 actual: PASS, converse verified biconditional by row permutations
and confined to s_0..s_2 by triangularity. Actual time-two identification c = Theta(X_1)
reconstructed and licensed: Phi C_1 = shift^2 s always, upgraded by (C_1)_0 = D_1 = 3
with Sec-1 uniqueness. Source-lag positivity: a purely periodic s would repeat s_0 = 3
(type {0,2}) or s_1 = s_2 = 2 (type {0,3}) at tail positions, contradicting the tail
alphabet -- no case split needed. C10 scope: PASS -- isolated-pair route-block only;
infinite-F/FULL, single-x, and per-type unboundedness correctly disclaimed. C12 wording:
PASS -- b never called permitted; lags attached to s and c respectively.

## Verdict and commit clearance

No fatal flaw. Non-fatal notes only: state the all-zero-tail exclusion for monotonicity
explicitly; the pi^4-finiteness step behind the T^4 remark is valid but implicit.
Admit Secs 1-2 as `partial-proof`, Sec 3 as stated. The corrected sidecar
(`problem1_round8_lag_sidecar.md`: superseded note, divide-direction fix, 2P-subscript
fix -- all verified present) is marked superseded with its scoped result preserved.
No unresolved review item blocks committing the main note.
