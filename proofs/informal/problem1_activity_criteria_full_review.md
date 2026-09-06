# Full all-depth review: single-column and temporal-deficit criteria (proof-only)

Status: independent reviewer; owns only this file. No numerical run or data was produced; finite verification claims (`finite-exhaustive` counts, vector agreements) are excluded from this verdict. Already-accepted parts (last-time rigidity, harmonic bound, uniform V finite entry with fixed-input vs spatial-limit quantifiers) are cited from `problem1_activity_finiteness_independent_review.md` Part A, not re-derived. Lead closes the effective-theorem archive and audits separately. No other workers were used.

Scope: every all-depth claim in current `problem1_single_column_activity.md` Sections 1-4 and `problem1_temporal_activity_deficit.md` Sections 1-5. Theorem status stays `partial-proof`; this review reports derivation-or-flaw per claim, not Problem 1 progress.

Sources (current SHA256):
- proofs/informal/problem1_single_column_activity.md 8c476497cde6129403bba94b632c6014a53d1a33bfd784b27701538bcbab0310
- proofs/informal/problem1_temporal_activity_deficit.md ee1611d10d098737baf5826d99d2e9bedefa607cdc98f2afb161d1804d990f91
- prior scoped acceptance: proofs/informal/problem1_activity_finiteness_independent_review.md (Part A: even-limit K bound, odd 2K inequality, last-activity equation with t = 0, bi-infinite rigidity, 3K/2 harmonic count, common h_V(K), limit-to-input compactness)

Commutation rule used throughout: only pi A = A pi. In particular A^r = pi^r T^r holds by induction moving A past pi^r (never T past pi), and bit_{2s}(T^t x) = bit_0(A^t(pi^{s-t} x)) by moving A^t past pi^{s-t}. No pi-T or A-T commutation enters any derivation below.

## Single-column Section 1 (verified)

A-diagonal (2) holds by the route above. Gate precision (first s observed branches, cylinder 2s+2, s = 0 constant) is an imported dependency of the repetition-bound note and is consistent with the deficit note's 2s+4 for s+1 branches; causality (bit_{2s}(T^t x), t < s, uses only x_{<=2s}) was rechecked.

Finite propagation (3): with y = T^h(x) finite and k = ceil(bitlen(y)/2), rows past h grow at most 2 bits per step, so column 2s vanishes for h <= t <= s+h-k; at most h early plus max(k-h-1, 0) late times pay, capped by V_s <= s. Edges hold: y = 0 (k = 0) gives 0 past h; h = 0 gives (4) V_s <= k-1 for POSITIVE finite x of complexity k with no frontier assumption (x = 0 is via (3), min(s, max(0, -1)) = 0). Hand control: x = 2 has V_s = 0 against bound 0.

Original-position formula (4a): for ordinary nonroot length n and s >= n, d = s-t terms with d > n vanish since pi^n(x) is a fixed root and pi^{n+1}(x) = 0; for 1 <= d <= n the endpoint projection pi^d(x) = A^d(v_{n-d}) converts each summand to bit_0(A^s(v_{n-d})), i.e. the sum over i = 0..n-1. Empty history gives V_s = 0. Hand check: x = 27 = U(6), P(1) = 6 gives V_2 = bit_0(A^2(1)) + bit_0(A^2(6)) = 1 + 0 = 1. The domain warning (original positions only, not appended ones) is exact and is preserved.

## Single-column Section 2 (verified, constants and s = 1 horizons checked)

For (5), bit 2s sits in Z_s's six-cell window; nonzero windows are noncharges or charge 5, and each charge-5 time except possibly the last has a distinct noncharge successor (temporal Section 4 lemma, verified below), so nonzero times <= 2Z_s+1. Sharpness hand check: x = 5, s = 1 gives window exactly 5 (charge, Z_1 = 0) with V_1 = bit_2 = 1, attaining the +1; no smaller constant works.

For (6), noncharge implies nonzero, bounded by six bits. Even columns over t = 0..s-1 cost at most V_{s-1}+1 (one extra sampled time), V_s, V_{s+1} (subset of horizon) left to right; odd columns via (7) with their next evens cost at most 2V_s+1 (shifted sum needs one extra time), 2V_{s+1}, 2V_{s+2} (shifts stay inside horizons s, s+1). s = 1 uses V_0+1 = 1 with no negative age. Hand check: x = 1 has Z_1 = 1 (window 1, noncharge) with V_1 = V_2 = V_3 = 0, so constant 0 in place of +2 is impossible. This does not prove 2 is needed or optimal; no optimality claim is made here. Summing gives (6), hence records (8) with 1+3+3+2 = 9, and bounded-V iff bounded-Z. Combined with the deficit equivalence (verified below), (9) follows; record maxima are monotone by definition with no per-age monotonicity assumed.

## Single-column Section 3 (cited accepted, not re-derived)

Even-limit K bound, odd-column 2K inequality (not equality), last-time equation including t = 0, bi-infinite rigidity, 3K/2 count, common h_V(K) with h_V(0) = 0, and limit-to-input compactness without asserting one-sided column extinction are exactly Part A of the cited prior review. The schematic 'age s+a' is read as s = m_n+a for shift 2m_n; no quantifier turns on it.

## Single-column Section 4 (verified)

Seam (11): with pi F = A^2 and s-t >= 1 throughout, V_s(F(x)) = sum_{t<s} bit_0(A^{t+2}(pi^{s-t-1}(x))) = sum_{r=2..s+1} bit_{2s+2}(T^r(x)); subtracting from V_{s+1}(x) leaves times 0, 1 minus r = s+1, the last via A^{s+1} = pi^{s+1}T^{s+1}. Only pi-A commutation is used. Bounds [-1, 2] are exact bit arithmetic, iterating to [-h, 2h] across h steps, so record unboundedness is invariant under fixed finite prefix removal. The T/F finite-entry equivalence invoked here is verified under deficit Section 5 below.

## Deficit Sections 1-2 (verified)

A^r = pi^r T^r and window form (3) hold by the commutation rule above; Z_s samples one fixed six-cell window over consecutive times (not a projected-boundary trajectory). Gate precision 2s+4 is imported consistently with Section 1 above. Bound (4) max(h, k): windows vanish for h <= r <= s+h-k-1, leaving <= h early plus at most max(k-h, 0) late times (no negative count when h > k; then every r >= h in range is a zero window), capped by s. Mandatory controls rechecked by hand: T(-1) = 1 with Z_s(-1) = 1, because for FIXED s every sampled r >= 1 has T^r(-1) of bit length at most 2s-2, hence pi^{s-1} of it is 0 (charged) with no window 1 at those times; only r = 0 (the all-ones row) pays; T(-1/7) = -1, T^2 = 1 with Z_s = min(s, 2) (rotations 9, 18, 36 uncharged, then the h = 2, k = 1 speed bound). A sign-sensitive slip (pi^2(7) = 0, not 1) was caught and corrected mid-review; the identities stand.

## Deficit Section 3 (cited accepted)

Last-activity equation with t = 0, bi-infinite rigidity, harmonic count with finite-sum limit (no infinite interchange), and dyadic divergence are Part A of the cited review.

## Deficit Section 4 (verified; finite-window vs infinite Kep separate)

Charge-5 lemma rederived by hand: window 101000 (value 5) with arbitrary lower bits c_0, c_1 evolves to [NOT(c_0 OR c_1), 1, 0, 1, 1, 0], i.e. next window 26 or 27 by the lower bits, bits 2..5 always 0,1,1,0, both uncharged. Successors are injective (t+1), so on an infinite word with <= K noncharges there are <= K charges and <= 2K nonzero windows; every column of every even-shift limit has <= 2K active times (columns sit in even windows). The +1 appears only in finite-horizon comparisons like (5), never in this infinite count. With B = 2K, Section 3 gives common M < h(K) and zero limits; infinite output ones would supply a nonzero shifted-input limit with a one at position 0 or 1 after h(K) steps, a contradiction. Hence (9): bounded Z iff finite T-entry, bounding time only. Fixed-input bounds versus spatial-limit conclusions are kept distinct throughout; no one-sided column extinction is claimed.

## Deficit Section 5 (verified)

T/F equivalence (10), with a rejected review claim withdrawn: F^r = 4A^{2r}+3 is FALSE for r > 1 (hand witness: F^2(7) = 111 while A^4(7) = 6 and 4*6+3 = 27). The r = 1 formula F = 4A^2+3 does not iterate. Correct relations: pi^r(F^r(x)) = A^{2r}(x) by induction (pi^{r+1}F^{r+1} = pi^r(pi F(F^r)) = pi^r(A^2(F^r)) = A^2(pi^r F^r) = A^{2r+2}, using only pi F = A^2 and pi-A commutation), and F^r(x) = (F^r(x) mod 4^r) + 4^r A^{2r}(x). Finite-entry directions: T^h finite gives finite A^{2r} for 2r >= h, hence finite F^r by low-part-plus-shifted reconstruction; finite F^r gives finite A^{2r} = pi^r(F^r), and restoring 2r deleted low pairs keeps T^{2r} finite (deleting low digits cannot finitize an infinite tail). Gate-cylinder continuity is imported as stated. D-seam derived (not merely bounded): D_s(F) = sum_{d<s} I(A^{s-1-d}(pi^d F)); for d >= 1, pi^d F = A^2(pi^{d-1}) via pi F = A^2 and pi-A commutation, giving sum_{e<s-1} I(A^{s-e}(pi^e x)); against D_{s+1}(x) the two missing terms e = s-1, s are exactly J(pi^{s-1}x) = I(A pi^{s-1}x) + I(pi^s x), plus the d = 0 term I(A^{s-1}F). Hence D_s(F) = I(A^{s-1}F) + D_{s+1}(x) - J(pi^{s-1}x), i.e. seam (11); 1+I-J with I in {0,1}, J in {0,1,2} gives exactly [-1, 2]; iteration gives [-h, 2h]; record R_N^D inherits prefix-invariance. Psi implication is one-directional only (beta >= 0), as written; comparator/terminal-edit slopes are correctly fenced off, and no survivor growth is asserted.

## Scoped verdict

Rejected review claims (mine, not source flaws; no source counterexample was found): (a) F^r = 4A^{2r}+3 for r > 1, refuted by F^2(7) = 111 vs 27 above; (b) D-seam asserted from bounds only, now derived term-by-term; (c) +2-slack optimality wording, withdrawn to impossibility-of-0 only; (d) late-count phrasing without max(k-h, 0) and a garbled -1 window description, both corrected. Smallest flaw found in the sources: none. Every all-depth identity, constant (including s = 1 horizons, +1/+2 slacks, max(h,k-1) vs max(h,k)), edge case (h = 0, s = h, n = 0, K = 0, empty history, y = 0), and hand control (-1, -1/7, x = 1, 2, 5, 27) resolves as written; the charge-5, seam, and equivalence derivations use only pi-A commutation with fixed-input/limit and finite/infinite bookkeeping preserved. Renewed complete scoped all-depth verdict: Sections 1-4 (single-column) and 1-5 (deficit) hold as `partial-proof` claims on the corrected derivations above, excluding finite-certification counts and any Problem 1 conclusion. No theorem, archive, or established review file was modified.
