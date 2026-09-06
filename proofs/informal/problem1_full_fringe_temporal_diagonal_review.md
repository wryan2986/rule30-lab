# Independent adversarial review: full fringe as inverse-scan diagonal condition

Reviewed source: `proofs/informal/problem1_full_fringe_temporal_diagonal.md`
SHA256 (computed locally before reading):
`87b54cc3e800c6d295c69eb79c6b2f5c450a9c48b282fad1882e04de8bed7f6e`
(195 lines, read in full.) Method: find a fatal flaw; every identity
re-derived by hand from stated definitions; only hand evaluations on small
bit/symbol cases; no numerical runs, no census, no prefix campaign.

## Verdict

ACCEPT as `partial-proof` modulo the dependencies listed in Sec. E. No
fatal flaw found. The load-bearing distinctions the note insists on --
`I_0^m` versus per-step fringe reset, initial symbol versus branch letter,
and the diagonal condition versus the gate-bridge scan -- were each
independently verified to be genuine (Secs. B, D). All hand computations
(prefix symbols, table rows, scope control) rechecked exactly. The
remaining step toward growth, incompatibility of (12) with the finite-entry
alternative, is correctly left `inconclusive`; the actual-growth gap is
stated in Sec. F. No part of this review claims anything about Problem 1
itself.

## A. Inverse scan and adjunction (Sec. 1): ACCEPT

A1. `Phi I_a = id`: `(Phi(I_a b))_t = g(c_t, h(c_t, b_t))` with
`c_t = (I_a b)_t`; first output bit
`(r XOR (a0 OR a1)) XOR (a0 OR a1) = r`, and with that `r` recovered the
second is `(s XOR (a1 OR r)) XOR (a1 OR r) = s`. Verified.
A2. Uniqueness: `c_0 = a`, `Phi c = b` forces
`(c_{t+1})_0 = r_t XOR (...)`, `(c_{t+1})_1 = s_t XOR ((c_t)_1 OR r_t)`,
which is exactly the recursion (1); hence `c = I_a b`. Verified.
A3. Table (3) re-derived from `h` for all 16 entries:
`a=0: (r, s XOR r)` gives `[0,3,2,1]`; `a=1: (NOT r, s XOR r)` gives
`[1,2,3,0]`; `a=2: (NOT r, s XOR 1)` gives `[3,2,1,0]`; `a=3` identical
to `a=2`. All rows match; `I_0 != I_3` confirmed load-bearing.
Permutation-in-input for fixed scan state rechecked (`r` from the low
output bit, then `s`). Verified.
A4. `Theta(4x+a) = I_a Theta(x)`: `c = Theta(4x+a)` has `c_0 = a`
(`(4x+a) mod 4 = a` exact) and `Phi c = Theta(pi(4x+a)) = Theta(x)` by
the imported deletion conjugacy; A2 then forces `c = I_a b`. Verified
modulo the imported conjugacy. The explicit no-shift-commutation
disclaimer is correct restraint.

## B. Right-half encoding and physical spacetime (Sec. 2): ACCEPT

B1. Encoding (4): `a_j = r_{2j} + 2r_{2j-1}` stores the outward pair
`(r_{2j-1}, r_{2j})` reversed, low bit outermost. Zero right half gives
all `a_j = 0`; finite fringe gives eventual zeros. Verified as stated;
no restriction on `x` is smuggled in.
B2. `W_m` bit layout rechecked: `W_m = 4^m x + sum_{k<=m} 4^{m-k} a_k`,
so pair `j < m` from the bottom is `a_{m-j}`: bits run
`r_{2m}, r_{2m-1}, ..., r_1` then `x` (center at bit `2m`). The
"from 2m toward the left" and reversal descriptions are exact.
`B_m = Theta(W_m)` follows by iterating A4. Verified.
B3. Identity (6) verified two ways. (i) Hand `m = 1`: with
`W_1 = (r_2, r_1, r_0, r_{-1}, ...)`, `bit_0(AW_1) = r_0 XOR (r_1 OR r_2)`
`= r_1(1)` and `bit_1(AW_1) = r_0(1)`; i.e. one `A` step advances time by
one and moves the origin left by one (the dropped pair is compensated by
the upward `T` read). Induction via translation invariance: after `2m`
steps, time `2m` and origin `2m-2m = 0`, i.e. `X_m`. (ii) Cone
containment as stated: `r_{-i}(2m)` reads initial cells `<= -i+2m <= 2m`,
so no cell right of the `2m` cut is ever needed, and the same bound covers
all cones inside `Theta(X_m)_t`. Hence infinite right halves cause no
omitted influence, and (6) is about the original spacetime, not a
reinitialized fringe. The `A^{2m} = pi^{2m} T^{2m}` power move was
exactly verified in the anchored finite-entry review (induction with the
outer-`pi`-reads-agreed-bits argument). Verified.

## C. Alternating criterion and triangularity (Sec. 3): ACCEPT

C1. Equivalence (7): `D_m = (B_m)_{2m} = A^{2m}(W_m) mod 4 = X_m mod 4`
by (6), i.e. the symbol `(r_0(2m), r_{-1}(2m))` low-bit-first. Necessity:
`r_0(2m+1) = 0` expands to `NOT r_{-1}(2m) = 0` given `r_0(2m) = 1`, so
`r_{-1}(2m) = 1`. Sufficiency: `D_m = 3` gives both even-row ones and
`r_0(2m+1) = 1 XOR (1 OR r_1(2m)) = 0` regardless of the right neighbor.
Every even and odd time is covered; no periodicity of the odd-row
neighbor or the schedule is inferred (correct restraint). Verified.
C2. Zero-fringe form (8) follows from (7) with all `a_j = 0`. The
reset warning is GENUINE, not vacuous: for `b = (3,2,1,0,...)`,
`(shift^2 I_0)^2 b` leads with `d_2 = h(1,2) = 3` while
`shift^4 I_0^2 b` leads with `e_4 = h(0,2) = 2` (hand: `c = (0,1,3,2,..)`,
`e = (0,0,3,0,2,..)`). The two operators differ at the leading symbol,
so conflating them would change `D_2`. The warning is load-bearing and
correct; crucially it was not violated anywhere in the note.
C3. Triangular homeomorphism: the note's induction is compressed but
sound; completed form: `D(m,i)`: `(F_m b)_i` depends only on
`b_0..b_{i-m}` (empty if `i < m`), by induction on `m` with inner
induction on `i` (`(F_{m+1} b)_0 = a_{m+1}` base; the step unions
`b_0..b_{i-m-2}` from the state with `b_0..b_{i-m-1}` from the input).
Unrolling `(F_m b)_k = h(S_m, (F_{m-1} b)_{k-1})` down to
`h(S_1, b_{k-m})` (indices stay `>= 1` iff `k >= m`) exhibits a
composition of input-permutations, so the map is a permutation of the
latest input `b_{k-m}` with earlier inputs fixed; at `k = 2m` that is
`b_m`, and `D_0 = b_0`. Successive unique solution of any `D` prefix and
the standard compatible-cylinder inverse limit give the homeomorphism;
right symbols stay fixed parameters. Verified.

## D. Gate recovery without discarding the fringe (Sec. 4): ACCEPT

D1. Identity (9): `Phi C_{m+1} = shift^{2m+2} Phi I_{a_{m+1}} F_m b =
shift^2 C_m`, using shift-commutation of the sliding-block `Phi`
(rechecked: both sides give `g(b_{t+1}, b_{t+2})`) and A1. No alternating
premise used. Then (10) follows from the Sec. 1 uniqueness since both low
symbols are 3 under (7). The stated non-replacement caveat is accurate:
(10) alone forgets (5)/(7). Verified.
D2. Gate formula: for a general row with code `C_m` and actual facing
right pair `a`, `shift^2 I_a C_m = Theta(Y')` for the actual row `Y'` two
steps later (checked: `(shift^2 Theta Z)_t = A^{t+2}Z mod 4`, and the
Sec. 2 step mechanism makes `A^2 Z` exactly the re-cut physical row).
`h(a,3) = 1` iff `a = 0` else `0` rechecked against all four table rows.
Requiring `(I_a C_m)_2 = 3` forces `(C_m)_1 = 2` when `a = 0`
(`row1[x] = 3` iff `x = 2`) and `(C_m)_1 = 1` when `a != 0`
(`row0[x] = 3` iff `x = 1`). These match residues 7/11 via the imported
bridge gate computation (`b_1 = 2/1`). The one-bit choice is thus read
off the actual right pair while (5) retains the whole fringe. Verified
modulo the imported bridge residue check.
D3. Hand prefix rechecked symbol by symbol: `D_0 = 3 -> b_0 = 3`;
`(I_0b)_1 = h(0,3) = 1`; `D_1 = h(1,b_1) = 3 -> b_1 = 2`;
`c = (0,1,3,...)` with `c_2 = h(1,2) = 3`, `c_3 = h(3,b_2) = 3 XOR b_2`
(`row3` is bitwise complement on two bits); `d = I_0c = (0,0,3,0,...)`
(`d_1 = h(0,0) = 0`, `d_2 = h(0,1) = 3`, `d_3 = h(3,3) = 0`);
`D_2 = d_4 = h(0,c_3) = 3` forces `c_3 = 1`, i.e. `b_2 = 2`. No further
symbols used. Verified.
D4. Scope control `x = 5/3`: `x mod 4 = 3` (`5*3 = 15 = 3`); with the
imported `A^2 x = pi x = -1/3` (`pi` drops `x mod 4 = 3`:
`(5/3-3)/4 = -1/3` exact), `b_2 = (-1/3) mod 4 = 1` (solve
`3v = -1 = 3`, `v = 1`; consistent with `-1/3 = 5 mod 16`). Then the D3
formulas with `b_2 = 1` give `c_3 = 2`, `d_4 = h(0,2) = 2`: `D_2 = 2`,
not 3, under the zero fringe. So correct first-branch symbols plus
infinite gate permission still violate (8). Correctly labeled a coordinate
check, with the free-schedule route left rejected as before. Verified
modulo the imported `5/3` data (`b_1 = 2`, fixed-point equation).

## E. Precise acceptance and dependencies

Accepted outright (proved here): A1-A4 modulo deletion conjugacy; B1-B3
modulo the `A^{2m} = pi^{2m}T^{2m}` identity (exactly verified in the
anchored finite-entry review, cited not re-proved); C1-C3; D1, D3; the
`I_0^m`-vs-reset distinction (C2, proved genuine by example).
Accepted as correct imports (not re-proved): `Theta pi = Phi Theta`
deletion conjugacy and `Theta A = shift Theta`; bridge residue table and
`b_1 = 2/1` for residues 7/11; forced-survivor `5/3` data; anchored
finite-entry theorem and support bound; `Theta` rationality
correspondence. Sec. 5 rebasing/quantifier paragraph is clean scoping:
finite support implies eventually-zero `a_j`; (7) applies at the new
origin; no identification of distinct fringe problems is made (the note
explicitly refuses it). No conflation of `I_0^m` with per-step reset, of
initial symbol with branch letter, or of the diagonal with the bridge
scan was found anywhere.

## F. Self-challenge and the actual-growth gap

(i) Hardest probe attempted: whether (6) smuggles reinitialization via
`W_m`'s finite low bits. It does not: B3 shows the low bits exactly
encode the genuine initial fringe cells and the cone bound excludes
anything further right, including infinite tails. (ii) Whether
triangularity could fail at `k = m` boundary indices: the completed
D(m,i) induction covers `i < m` (empty dependence) explicitly.
(iii) Whether (11) needs `(C_m)_0 = 3` beyond (7): it is stated as a
hypothesis for general rows, satisfied under (7); no overreach.
(iv) Whether D4's `b_1 = 2` was verified: it is an import (flagged),
while everything downstream of it (`b_2`, `c_3`, `D_2 = 2`) was recomputed
here. (v) All above-the-line work is hand symbol/bit evaluation.
Actual-growth gap (explicit, as requested): even with the diagonal (12)
fully accepted, NOTHING here forces `sup_n J_n = infinity`. The
triangular homeomorphism cuts both ways -- every `D` sequence, including
`D_m = 3` constantly, is realized by some code -- and the finite-entry
negation coexists with (8) unresolved. The note correctly claims no
incompatibility proof. The missing piece remains a concrete mechanism
showing the diagonal condition starves the explicit finite level; that
mechanism is not in this note and is not supplied by this review.
