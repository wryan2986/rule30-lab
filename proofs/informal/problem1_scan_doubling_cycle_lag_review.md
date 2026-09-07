# Adversarial review: each clock doubling forces a distinct late diagonal

Verdict: no fatal flaw; accepted with no outstanding corrections. The
growth theorem (1), the width/period count (3), the witness injection (4),
and the local lemma are accepted as `partial-proof`. All corrections raised
in Section 4 below have been applied in the current source, as recorded in
Section 7; their original wording is retained for audit. The honesty fence
is accurate. No computation was run; all checks are hand re-derivations.
The lead file is untouched.

Reviewed source: `problem1_scan_doubling_cycle_lag.md`, SHA256
`8dd71687c76baaeaf9d2aec864266cd70f46fb1071bd3988e96a4309763d47af`.

## 1. The operator identity survives probing (no correction)

The sentence `A^h = pi^h T^h` looked suspect because `pi T != T pi` as
operators (`T(pi(1)) = 0` while `pi(T(1)) = pi(7) = 1`). I verified the
identity is nevertheless true, by the defect lemma: bit-level expansion
gives `bit_n(Tx) = bit_n(x) XOR (bit_{n-1}(x) OR bit_{n-2}(x))`, from which
`T(pi^k z)` and `pi^k(T z)` agree on all bits `>= 2` for every `k >= 1`, so
their difference lives in bits 0-1 and dies under the next `pi`. Induction
then yields `(pi T)^h = pi^h T^h` exactly. With `T(4^k y) = 4^k T(y)`
(rechecked including the `n < 2k` edges) and `pi(4z) = z`, equation (2)
follows for `m >= J + h` by stepwise deletion of `h` zero low pairs, which
is what the draft's disclaimer describes. The justification stands.

Unit-triangularity of `T` is confirmed by the same bit formula, so `T^h`
is injective, `Y != 0` follows from `y != 0` (itself from `pi^J y = x != 0`).
[Correction: the source uses `x != 0` only as sufficient for `y != 0`, not
as necessary. Dropping it would permit all-zero `x` with all-zero fringe
(`W_m = 0`, `p_m = 1`, no growth), while a nonzero fringe (e.g. `a_1 = 1`,
rest zero, giving `W_m = 4^{m-1}`) can still drive growth from `x = 0`.] The `A^h x = 0` case is included correctly,
since `Y != 0` never needed finiteness of `A^h x`, only `y != 0`.

## 2. Width/period count (3): verified solid (`partial-proof`)

`Phi^n c = Theta(pi^n z)` by the conjugacy; each side is a nonzero word by
injectivity. The width edges check out for even and odd `L`: `pi^n z != 0`
for `n < ceil(L/2)`, zero at `n = N`. Distinctness via the `Phi^{N-j}`
argument is exact (`N-j+i < N` contradicts nonvanishing below `N`).
Available period `p` survives `Phi` by shift commutation, and `4^p - 1`
counts the nonzero `p`-periodic words. No phase error; (3) holds, and (1)
follows from it directly since `L_m -> infinity`.

## 3. Witness injection (4): verified, indices exact (`partial-proof`)

Doubling alternatives are exhaustive: all-zero tails give `q = 1` (never a
doubling) and synchronizing tails give `q = p`, so `m in E` forces an odd
`{0,2}` or `{0,3}` tail, each containing the operative symbol. The alphabet
forcing has no off-by-one: case `{0,2}` puts `D_m = 3` outside the tail
 alphabet, so `tau_m > 2m` at depth `m`; case `{0,3}` puts `B_{m+1}`
eventual symbols in `{0,1}`, so `D_{m+1} = 3` at index `2m+2 = 2(m+1)`
forces `tau_{m+1} > 2(m+1)` at depth `m+1`. Nonadjacent doubling indices
give disjoint `{m,m+1}` pairs, so `j` is injective and (4) holds with exact
`d_N = log_2(p_N/p_0)`. All witnesses use the same original code and fixed
fringe; nothing is selected anew.

## 4. Required corrections (all non-fatal)

(a) Section 1 max-width inference needs one sentence. `States with a given
available period p inject into the 4^p codes' does not directly bound
`states of least period at most P' (least `l <= P` need not divide `P`).
Fix by a finite union over `l = 1..P`, or inject into `4^L` with
`L = lcm(1..P)`. The finiteness conclusion is unaffected.

(b) Section 3 broader-class scope overreaches as worded. The
`(C_m)_0 = 3` substitute (valid on any permitted `F`-orbit) supports
distinct depths with positive preperiod, but NOT the `2j`-lag count: (4)'s
thresholds come from the FULL diagonal indices, which have no analog on a
general orbit. Replace `Consequently (4) is a necessary constraint even on
that larger class' with the weaker distinct-positive-preperiod count. The
FULL-case (4) is unaffected.

(c) Section 0 attribution. `The prior note proves tau_m ... is exactly the
least temporal preperiod of B_m' is a two-line corollary of the reviewed
homeomorphism, not an explicit prior statement: preperiod `T` of `B_m`
means `Theta(A^T W_m)` purely periodic, which by shift plus injectivity is
exactly `A^T W_m` on-cycle. Confirmed true; cite as corollary or add the
lines.

## 5. Honesty fence: accurate (`inconclusive` retained)

Section 3 correctly claims neither unbounded lags, nor positive density,
nor any anchored-activity transfer (`W_j` prefixes vs the fixed `Q(x)`
budget). The 55-certificate characterization is fair. The census fence
stands. No height, density, or activity growth is inferred anywhere.

## 6. Re-review of strengthened version (source-late witnesses, local lemma)

Reviewed source (current): SHA256
`714315933161f83e7e94396105f7d7807686d134600349cc24924af35109a471`.
The Section 3 paragraph of this review verified the earlier
source-or-successor version and is explicitly superseded by what follows;
Sections 1, 2, 4(a), 4(c), and 5 stand unchanged.

The extra gate symbol (4a) is the reviewed full-fringe Section 4
calculation, correctly imported with its actual-right-pair dependency:
under FULL every even-index 3 is followed by 1 or 2. Both doubling cases
now force the source `m` itself late (`tau_m > 2m` via `D_m = 3` outside
`{0,2}`; `tau_m > 2m + 1` via the gate symbol at index `2m+1` outside
`{0,3}`), with the successor bound retained as well. Indices are exact,
witnesses are the identity map so no injection is needed, and (4) follows
in its redefined form. Stronger than before, no new assumption.

The new Section 3 local lemma is verified in full. `R(2) = R(3)` holds
because every `H_i` identifies 2 and 3 (`H_0:[3,3]`, `H_1:[2,2]`,
`H_2:[1,1]`, `H_3:[0,0]` on those states), at the first applied factor;
`R(z) = z` follows since the middle factors agree on `{2,3}` (the `p = 2`
case via `H_3` itself), giving the unique `p`-periodic response. The
`preperiod exactly 1' conclusion is true: with `R(c_0) = z != c_0` and
`c_{np} = z` for all `n >= 1`, pure `q`-periodicity would force `2 = 3`
at a common multiple index; the draft elides this gcd step, which should
be added as one line. `q = p` via `Phi c = shift^2 b` is exact, and (7)
follows through `Theta` conjugacy with `z = 2` recomputed for the 55 case
(`R = H_2 H_3`, `R(2) = H_2(0) = 2`), matching 222-periodic/223-transient.
Consistency with the reset note holds precisely because the gate's
`b_1 in {1,2}` forces the synchronizing alternative there. `p >= 2`,
`tau(Fx) in {0,1}`, and the stated scope limitation are all exact.

Corrections update: 4(a) (union/lcm sentence) and 4(c) (preperiod
attribution) remain outstanding, text unchanged. Former 4(b) is narrowed:
the new middle sentence on the larger class (positive preperiod, `>= 2` in
the `{0,3}` case via `(C_m)_0 = 3` and `(C_m)_1 in {1,2}` on any permitted
orbit) is accurate; only the trailing `(4)' label still overreaches, since
the `2j` thresholds are diagonal-specific. Replace it with the explicit
weaker count.

## 7. Final acceptance record (all clarifications applied)

Current source SHA256
`5ea825b811ec3aa807ce44681b2a8111c770e501594fa84003b3932636bd539f`.
All four items are present as specified: finite union over `p = 1..P` in
Section 1; explicit preperiod-homeomorphism identification in Section 0;
the common-multiple argument against any other pure period in Section 3;
and the separate general-`F` positive-preperiod count with its explicit
disclaimer from (4)'s `W_m`/`2m` thresholds in Section 4. Status and review
pointer updated. Accepted with no outstanding corrections.

Independent check as requested: `{0,3}`-input doubling forces lag at least
two. The gate symbol at diagonal index `2m+1` lies in `{1,2}`, outside the
`{0,3}` tail alphabet, so index `2m+1` is pre-tail and
`tau_m >= 2m+2`, i.e. lag `>= 2`. The general-orbit analog is identical
with `(C_m)_1`: preperiod exceeding one. Confirmed correct in both places.

## 8. Strengthening record: (4b) and lag three (accepted)

Current source SHA256
`7b8c6844007d9c45916fda267df3edf5d7274d135810eb6b3f41e26035144a5c`.
Only the (4b) paragraph, the `{0,3}` lag upgrade, and the general-`F`
sentence are new; all four prior clarifications verified still present.

(4b) is exact: `(C_{m+1})_1 = H_{(C_m)_2}(3)` from `I_3` scan indexing, and
`H_i(3) in {1,2} iff i in {1,2}` recomputed from table (1)
(`H_0(3) = 3`, `H_1(3) = 2`, `H_2(3) = 1`, `H_3(3) = 0`). With the gate at
`m+1` giving `(C_{m+1})_1 in {1,2}`, `(B_m)_{2m+2} in {1,2}` follows.
`{0,3}` doubling now puts two consecutive indices outside the tail
alphabet, so `tau_m > 2m+2`, lag `>= 3` for integer lags; the previous
`>= 2` remains valid weaker. General-`F` analog verified: the next
permitted gate gives `(C_m)_1, (C_m)_2 in {1,2}` on any infinite permitted
orbit, forcing preperiod exceeding two in the `{0,3}` case. Accepted with
no outstanding corrections.
