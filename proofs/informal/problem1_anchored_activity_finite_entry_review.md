# Independent adversarial review: anchored pair activity finite entry
# (corrected; v2 supersedes the initial review, whose history is retained
# at /tmp/astra-round6-anchored-{review-initial,source-reviewed}.md)

Reviewed source: `proofs/informal/problem1_anchored_activity_finite_entry.md`
SHA256: `180c8b79b1a34129b94431559a3c495c40ecd523c5f6253c14e2f7d4dff6d2a7`
(verified by local sha256sum before reading; file read in full, 193 lines).
Method: aim to find a fatal flaw; every identity re-derived by hand from the
stated definitions; only hand evaluations of small-bit cases; no machine or
range runs. Correct stencil throughout (checked against eq. 1):
`bit_i(Az) = z_{i+2} XOR (z_{i+1} OR z_i)`, so `bit_i(A^t z)` depends on
`z[i, i+2t]` via a fixed translation-invariant Boolean `F_t`.

## Verdict (corrected)

ACCEPT as `partial-proof` modulo the stated imports. The initial review's
Section C counterexample is WITHDRAWN as a REVIEW ERROR (retained below for
the record): it extended after shifting, freezing an artificial boundary at
`i = 0`, while the proof extends `x` at negative indices BEFORE shifting,
so the artificial boundary recedes to `-infinity`. Under the proof's actual
translation formula the all-`j` transfer holds as written (re-derived in
Sec. B with explicit fixed-x/fixed-j/eventual-`l` quantifiers), the
Section D repair is unnecessary, and no flaw of any kind remains. Details:
Sections 1, 3, 4 fully verified; Section 5 correctly scoped.

## A. Section 1: ACCEPT (independently verified in full)

A1. Deletion (2): solving (1) at `2j` gives
`u_{2j+2}(t) = u_{2j}(t+1) XOR (u_{2j+1}(t) OR u_{2j}(t))`, i.e. the first
output bit `r`; solving at `2j+1` gives `u_{2j+3}(t)` with the just-solved
`r` in the OR position, i.e. `s`. Verified.
A2. Terminal identities (3): `g(0,0) = 0` direct. For `(c0,c1) = (0,0)`
and `a != 0`: `r = a0 OR a1 = 1`, `s = a1 OR r = 1`, so `g(a,0) = 3`.
Checked for all four symbols: `1 -> (1,1)`, `2 -> (1,1)`, `3 -> (1,1)`.
Verified.
A3. Last-time preservation: with `M` the last nonzero time of a
finite-support word `b`, `Phi(b)` vanishes past `M` by `g(0,0) = 0` and
`Phi(b)_M = g(b_M, 0) = 3 != 0`. Same last time; zero iff zero. Verified.
A4. Common last time: `w_{j+1} = Phi(w_j)` as temporal words by (2), so
A3 gives `last(w_{j+1}) = last(w_j)` for every adjacent pair; all pairs
share `M` (uniform `-inf` iff all zero: `w_j = 0` forces `w_{j+1} = 0`
and non-uniformity would contradict A3). Then `w_j(M) = g(w_{j-1}(M), 0)`
with `w_{j-1}(M) != 0` gives `b_j(M) = 3` for every `j`: row `M`
identically symbol 3, later rows zero. Verified.
A5. Diagonal induction (the `r+1` cone): if pairs `j..j+r` vanish at time
`M-r`, then `w_{j+k}(M-r) = g(0, w_{j+k-1}(M-r+1)) = 0` forces
`w_{j+k-1}(M-r+1) = 0` (using `g(0,c) = 0 iff c = 0`, since
`r_out = c0`, `s_out = c1 XOR c0`). Round by round the zero block shrinks
from the right; after `r` rounds `w_j(M) = 0`. The `r`-step input cone of
output `(j, M)` is exactly the `r+1` pairs = `2r+2` cells. Verified.
A6. Harmonic bound (4): partitioning `N` consecutive pairs into
`floor(N/(r+1))` disjoint `(r+1)`-blocks, each contributes `>= 1` active
pair at time `M-r` by A5. Summing `r = 0..M` (finite sums only), bounding
the total by `KN` (each pair `<= K` nonzero times, times `M-r` distinct),
dividing by `N` and letting `N -> infinity` gives `H_{M+1} <= K` with
ordinary harmonic `H`. Strict increase of `H` gives `M+1 <= h`, so
extinction by `h_J(K)`. `K = 0` gives `h_J(0) = 0` (`H_1 = 1 > 0`) and
directly zero activity. Minor exposition note (not a flaw): `M = -inf`
needs the one-line convention that the empty harmonic sum is `0 <= K`.

## B. Section 2 transfer, ALL `j`: ACCEPT (re-derived, explicit quantifiers)

The proof's translation formula: `xbar_k = x_k` (`k >= 0`), `0` (`k < 0`);
`v^{(l)}_i = xbar_{i+2n_l}` for ALL `i in Z`, with `n_l -> infinity`.
Fix `x` with `Q(x) <= K`; fix ANY `j in Z` (sign unrestricted); fix `t`.
`bit_{2j(+1)}(A^t v^{(l)})` reads the `v^{(l)}`-window `[2j, 2j+2t]`, i.e.
`xbar`-indices `[2j+2n_l, 2j+2t+2n_l]`. Since `j, t` are fixed and
`n_l -> infinity`, eventually `2j+2n_l >= 0`: every stencil bit is a
genuine `x` bit, and the window equals the one for
`bit_{2n_l+2j(+1)}(A^t x)` exactly (stencil translation invariance).
Hence pair `j` of `A^t v^{(l)}` equals pair `n_l+j` of `A^t x` eventually.
Horizon form: fix `L`; eventually `n_l+j >= max(1, L)`, so times
`0..L-1` sit inside `J_{n_l+j}(x) <= K`; discreteness of `{0,1}` moves the
bound to the limit pair. Quantifier order: `forall x forall j forall L
texists L_0 forall l >= L_0`. Every limit pair has `<= K` nonzero times in
every finite horizon, hence in total, for EVERY `j`. The artificial
boundary (`v^{(l)}_i` reading extension zeros, i.e. `i < -2n_l`) recedes to
`-infinity`; no fixed finite window ever sees it eventually. Section 1
applies unmodified; uniform extinction at `h_J(K)` holds; Step B (shifts
at nonzero pairs `p_l -> infinity`, pair-0 equality via window `[0, 2h]`,
discreteness) is intact. Theorem (5) holds exactly as written.
The initial review's `j >= 0` restriction survives only as an unneeded
one-sided alternative, not a required repair.

## C. WITHDRAWN counterexample (REVIEW ERROR, retained for the record)

The initial review claimed pair `-1` of a limit of shifts of
`x = -3*4^{n+1}` is `(1,0)` at all `t >= 1`. That computation used
`v^{(l)}_i = x_{i+2n_l}` for `i >= 0` and `0` for `i < 0`: extending AFTER
shifting, which pins an artificial zero boundary at fixed `i = 0` for all
`l` and yields the spurious limit row `1_{>=0}`. The proof never does
this. Under the actual formula, for fixed `i`, eventually
`i+2n_l >= 2n+4`, where `x`'s bits are all 1, so the limit row is biinfinite
ALL ONES. One `A` step kills it: `T(-1) = (-1) XOR ((-2) OR (-4)) =
(-1) XOR (-2) = 1`, so `A(-1) = pi(1) = 0`; every pair has exactly one
nonzero time (`t = 0`), consistent with `Q(x) = n-1 >= 1`. The
"counterexample" evaporates; the error was the reviewer's, in the
order of extension vs. shifting (fixed boundary vs. receding boundary).
No weakening of any claim is needed or made.

## D. Repair assessment: NO REPAIR NEEDED

The v1 `j >= 0` restriction is verified as a correct but unnecessary
 alternative (all steps in B go through verbatim with `j >= 0`; the full
version above is strictly stronger and matches the source). Step B never
needed it (pair 0). The source's "EVERY such spatial limit vanish" and
"true for every `j`" sentences stand as written under the formula of
Sec. B.

## E. Section 3: ACCEPT. Section 4: ACCEPT. Section 5: ACCEPT (scope)

E1. `Q(z) = N(z)` (6): top bit `B-1` persists since
`bit_{B-1}(Az) = 0 XOR (0 OR 1) = 1` and higher bits stay 0; the top pair
(always holding the top bit, even or odd `B`) is nonzero at every `A`
time, so `J_N = N`; higher pairs vanish (`2N+2 >= B`); lower `J_n <= n`;
`bitlen <= 2` gives `Q = 0`. Verified, incl. `z = 0`.
E2. Window comparison (7): `J_n(A^h x)` sums `P_n(x, .)` over
`[h, n+h-1]`; `n < h` gives `<= n <= h`, else split at `n` gives
`<= J_n(x) + h`. Sup gives `Q`. Verified.
E3. Support bound (8): `Q(z) = N(z) <= K+h` gives
`ceil(bitlen/2) <= K+h+1`, i.e. `bitlen(z) <= 2(K+h+1)`; low-digit
restoration gives `bitlen(T^h x) <= 2K+4h+2`. Containment (9) via
injective unitriangular `T^h` (`bit_j(Tx) = x_j XOR (x_{j-1} OR x_{j-2})`:
`x_j` leading, lower-bit recursion; full inverse-tail rationality stays an
import). Verified modulo stated imports.
E4. Converse (10): for `n > N(z)`, `P_n(x, t) = P_n(z, t-h) = 0` at
`t >= h` (support preserved); `J_n <= n <= N(z)` below; so
`Q(x) <= max(h, N(z))`. Equivalences (11) follow; only the last (`R`)
imports the reviewed single-column theorem, as declared. Verified.
E5. Counterexample (12): `T(-3) = 3` hand-checked bitwise
(`...1101 XOR ...1110 = ...0011 = 3`); `T(4^k v) = 4^k T(v)` exact
(bitwise ops commute with `<<k`); `A(x) = 3*4^n` exact. Pair census:
pairs `< n+1` zero at `t = 0` (bits `0..2n+1` zero); pairs `> n` nonzero
at 0, zero for `t >= 1` (finite image support `<= 2n+1`); pair `n` zero
at 0, forever nonzero after (top pair of `3*4^n`, bitlen `2n+2`, `N = n`).
Hence `Q(x) = max(1, n-1) = n-1` (`n >= 2`), `Q(Ax) = n` by (6): (7) sharp
at `h = 1`, finite `Q` levels not `A`-invariant. The `refuted` label is
correctly scoped to general inputs. Verified.
E6. Quantifiers/parity/commutations: `h_J(0/1/2) = 0/1/3` rechecked
(`H_1 = 1`, `H_2 = 1.5`, `H_4 ~= 2.083`); ordinary vs odd harmonics
correctly distinguished (block size `r+1` here vs disjoint pairs in the
staircase note); `K = 0` forces `x in {0..3}` elementarily
(`P_n(x,0) = 0` for all `n >= 1` kills bits `>= 2`), consistent with (5);
`A^h = pi^h T^h` proved exact by induction (`T pi^h` vs `pi^h T` agree on
bits `>= 2`, outer `pi` reads only those). Caution confirmed: full
`T pi = pi T` is FALSE (`z = 7` gives `7` vs `6`), so the note is right
to import the power identity without asserting commutation.

## F. Self-challenge on this corrected review

(i) The withdrawal was checked by_instance_, not by agreement: the
all-ones limit, `T(-1) = 1`, `A(-1) = 0`, and the one-nonzero-time pair
census were all recomputed by hand above. (ii) The Sec. B quantifiers were
written in `forall/exists` order deliberately; the load-bearing step is
that `j, t` are fixed BEFORE `l -> infinity`, so `2j+2n_l >= 0`
eventually holds for negative `j` too. (iii) Step B's `p_l -> infinity`
uses infinitude of nonzero pairs for the subsequence; discreteness is used
at pair 0 only. (iv) `M = -inf` convention remains a one-line exposition
nit. (v) All above-the-line computations are hand bit evaluations on
`<= 4` bits; no machine ran. (vi) The initial-review history is preserved
outside the repo at the `/tmp` paths above; this file corrects rather
than erases.

## Acceptance scope

Accept: A1-A6; B (all-`j` transfer, explicit quantifiers); E1-E6 with
stated imports (single-column finite-entry theorem; `T^h`
injectivity/inverse-tail rationality). Reject: nothing. Required changes:
none (optional: `M = -inf` convention line). The note is correct as
`partial-proof`. No fatal flaw found; the hunt disclosed only the
reviewer's own ordering error, corrected and retained above.
