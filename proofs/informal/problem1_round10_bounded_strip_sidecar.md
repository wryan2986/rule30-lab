# One-bit extension preperiods and the conditional low-strip split (round-10 sidecar)

Status: `partial-proof` for the scalar extension recurrence and both tail cases (Section 2), the conditional low-strip update (Section 3), and the same-low-word witness (Section 5); `refuted` for the naive low-word-only closure at K >= 2 on the stated local class; `inconclusive` for every bounded-strip and Problem 1 target. Sections 2, 3 and 5 are hand derivations. The twelve controls verify only Section 2's scalar formulas, with status `finite-exhaustive`; they do not machine-verify Sections 3 or 5. Lead audit is recorded separately; fresh external adversarial review was unavailable. Problem 1 remains OPEN.

## 0. Scope and definitions

Sidecar task: test whether bounded least A-preperiods on ONE fixed actual alternating-center orbit admit a reduction to finitely many periodic boundary bits via shifted physical diagonals. FULL means ANY ONE fixed finite initial right fringe; the fringe is fixed once and never varied. Finite entry means the rows Y_t are finite for all sufficiently large t (equivalently, some A^h / T^h image is finite, per the imported anchored equivalence). Hypothesis (B): there exist K >= 0, T >= 0 with tau(Y_t) <= K for every t >= T on the one fixed orbit. The derivations in this memo are Sections 2, 3 and 5; everything else is import.

## 1. Imports (used, not re-proved, not claimed)

- Pair/bit transport and uniform-bound transport; one-step bridge Y_(t+1) = 2 A Y_t + c_(t+1), sigma^n Y_(t+n) = A^n Y_t; bit thresholds b(Y_(t+n)) > n iff tau(Y_t) > n; odd-row K+1 bound.
- One-bit scan classification (driven maps identity/const1/flip/const0; permutation tails preserve-or-double; reset tails preserve with unique recurrent bit); FULL doubling-source lateness (even source tau >= 1, odd source tau >= 2); waiting-time formula at highest disagreement.
- Clock growth as a `partial-proof` import: sup_t p(Y_t) = infinity on finite-entry orbits, within that note's scope. Any period-bound exclusion built on it inherits exactly this status and scope; no independent finding about bounds is recorded here.
- Strict even-row width growth; A width preservation on positive finite rows; full-code injectivity; finite-entry preservation.
- K = 0 exclusion (no eventually all-periodic FULL finite-entry orbit): round-7 import.
- Round-eight doubling family: all-depth constructive `partial-proof` (for every P an x with A^4 x finite periodic, D_0 = D_1 = D_2 = 3, period exceeding P doubling into its actual successor, small source/successor preperiods). It decides the local period-dependent lag question only, per its own fence; it is neither finite evidence nor a one-orbit statement.
- FULL diagonal condition and its unbounded scan depth as open context.

## 2. Exact scalar one-bit extension preperiods (`partial-proof`)

Let y be eventually A-periodic, T = tau(y), z = 2y + a with a in {0,1}. No FULL, fringe, or finiteness premise.

Lemma (extension never shortens preperiod). tau(z) >= T. Proof: sigma z = y and sigma commutes with A, checked bitwise: sigma(Aw)_i = w_(i+3) XOR (w_(i+2) OR w_(i+1)) = A(sigma w)_i. If A^S z is periodic then A^S y = sigma(A^S z) is periodic, so T <= S. Counterexample flag: none possible; the proof uses only commutation and leastness.

Claim A (permutation tail). If bit_0(A^s y) = 0 for all s >= T, then tau(z) = T exactly, for both a, regardless of period doubling. Proof: y' = A^T y is periodic with {0,2} code; the imported periodic classification makes both one-bit extensions of y' periodic; A^T z is one of them, so tau(z) <= T; the lemma closes it.

Claim B (reset tail). If some bit_0(A^s y) = 1 for s >= T, put rho = min{s >= 0 : bit_0(A^(T+s) y) = 1} (exists by recurrence of the periodic code). Then tau(z) = T if bit_0(A^T z) is the unique cyclic extension bit, else tau(z) = T + 1 + rho. Proof: the imported reset classification gives tau(A^T z) in {0, 1+rho}; the shift identity tau(A^T z) = max(tau(z)-T,0) lifts the positive case to T+1+rho and the zero case to <= T, hence = T by the lemma.

Hand checks (ordinary integer arithmetic, no backend). y = 7: A(7) = 1 XOR 7 = 6, A(6) = 1 XOR 7 = 6, so T = 1 with eventual low bit 0. z = 14: A(14) = 3 XOR 15 = 12, A(12) = 3 XOR 14 = 13, A(13) = 3 XOR 15 = 12; tau = 1 with doubling 1 -> 2. z = 15: A(15) = 12; tau = 1. Claim A exact on both parities. y = 3: A(3) = 0 XOR 3 = 3, T = 0, rho = 0. a = 0: z = 6 fixed, tau = 0 = T. a = 1: z = 7, tau = 1 = T+1+rho. Both Claim B branches occur. Counterexample flag: none found.

Physical corollary. A physical step is z = 2y + a with y = A Y_t, a = c_(t+1). A one-bit doubling p(Y_(t+1)) = 2p(Y_t) forces the eventual code into {0,2} (a resetting tail preserves period), so Claim A gives tau(Y_(t+1)) = tau(y) = max(tau(Y_t)-1,0). Under FULL every doubling source satisfies tau(Y_t) >= 1, so tau drops by exactly one across the step. Depends on the imported doubling-implies-permutation-tail direction; the rest is the derivation above.

## 3. Conditional low-strip split under (B) (`partial-proof`)

Assume (B). For s >= T+K put P_s = sigma^K Y_s (A-periodic by the imported threshold) and l_s = Y_s mod 2^K. For K >= 1 the update is exactly l_(s+1) = c_(s+1) + 2 * ((A(l_s + 2^K P_s)) mod 2^(K-1)), with no further reduction (c + 2w <= 2^K - 1). Bit j of A reads Y bits j..j+2, so (A Y_s) mod 2^(K-1) sees only Y_s bits 0..K: besides l_s and the known alternating c_(s+1) it depends on exactly one driver bit, bit_K(Y_s) = bit_0(P_s). For K = 1 this collapses to l_(s+1) = c_(s+1); for K = 0 the low part is empty. The even-row pair version is identical with N = ceil(K/2).

Fences. The window spillover refutes only the naive low-word-only closure (low word fed by center bits alone). It is NOT a theorem about all quotients: finite memories carrying driver phase are a different shape, undecided here. General-A doubling facts constrain pure A-dynamics only and do not by themselves touch the FULL bounded-tau question. No finite-closure no-go beyond these two fences is claimed.

## 4. Dispositions

- Uniform late boundedness of p(Y_t): excluded only to the extent of the `partial-proof` clock-growth import (Section 1); no independent finding is recorded here.
- Naive autonomous K-bit closure: `refuted` for K >= 2 by the spillover in Section 3; K = 1 is autonomous (Section 5).
- K = 0 strip: excluded round 7, import.
- Global K = 1 case: under independent lead exploration; no sidecar claim recorded.
- FULL bounded-strip exclusion and Problem 1: `inconclusive`. A separate lead main note follows the K = 1 derivation.

## 5. Same-low-word witness: the driver-bit read is genuine (`partial-proof`)

For K >= 2 the Section 3 update reads bit_0(P_s). Put y = 3 and y' = 3 + 2^K. They share the full K-low word, with cyclic high parts sigma^K y = 0 and sigma^K y' = 1. Attach the same initially zero right fringe to each. Both initial center-and-left pairs are 3, so both actual next centers are 0. Their actual next center-and-left rows are w = 2*A(y) and w' = 2*A(y'). Their bit K-1 is given by y_K XOR (y_(K-1) OR y_(K-2)). The two lower inputs agree and y_K toggles, so the output toggles. No zero value for y_(K-1) is assumed; it is 1 when K=2. In that case w=6 and w'=12, whose bits at index 1 differ. Thus low-word-plus-cyclicity does not determine this local update. These are distinct local input rows with the same initial right fringe, not two states asserted to occur on one FULL orbit.

## 6. Provenance

The Muse contributor derived Sections 2 and 3 and implemented the twelve scalar controls. Lead independently checked the mathematics and corrected the local witness and provenance wording. Section 5's all-K witness is a hand proof, not a twelve-control result. Exact superseded memo/checker/result bytes are archived in results/problem1/20260907_round10_superseded_run.json. The contributor's corrected control run succeeded at 04:14:49 UTC, then its thread ended with provider 429. Its one paused retry failed with MissingSessionID. Fresh Muse reviews and the mandated MiMo fallback also failed; see problem1_round10_fresh_review.md for the exact missing review and lead disposition. After those failures the lead completed the essential local wording/provenance correction and the necessary same-input verification. No model was silently substituted, no scientific input was expanded, and the immutable reference was untouched.
