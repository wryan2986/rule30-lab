# Adversarial review: reset words and periodic tails of the full inverse scans

Verdict: no fatal flaw; accepted with no pending corrections. Sections 1
and 2 are accepted as `partial-proof` in their stated scope. Section 3 is
accepted as `partial-proof`: two earlier objections were fully withdrawn in
Section 8 (original wording retained there for audit), and the Kopra-free
bit-length argument assessed in Section 6 is adopted in the current draft.
No computation was run; every check below is a hand re-derivation. The lead
draft is untouched.

## 1. Reset language: independently re-derived, accepted (`partial-proof`)

I recomputed all four driven maps from `h` and every entry of the image
table element by element; all agree. Completeness of the six nonsingleton
images holds: from the full set one letter reaches only
`{0,1,3}`, `{2,3}`, `{1,2,3}`, `{0,1}`, and images of those under all
inputs add only `{1,3}` and singletons, so no reachable nonsingleton image
is missing. Singletons are absorbing, so a word is non-reset exactly when
its full image path stays in the table.

Both directions of (2) check out. Sufficiency: `{0,2}*` words stay in
`{{0,1,3},{1,2,3},{1,3}}` because `H_0,H_2` permute `{1,3}`; `{0,3}*` words
stay in `{{0,1,3},{0,1}}` because `H_0,H_3` permute `{0,1}`; a `{0,3}`-prefix
leaves image full, `{0,1,3}`, or `{0,1}`, and a final 1 or 2 sends each of
these onto the nonsingleton `{2,3}` or `{1,2,3}` (verified: full/1 to
`{2,3}`, full/2 to `{1,2,3}`, `{0,1,3}`/1 to `{2,3}`, `{0,1,3}`/2 to
`{1,2,3}`, `{0,1}`/1 or /2 to `{2,3}`). Necessity: `{2,3}` is terminal
(every letter collapses it, recomputed all four), so paths ending there
cannot be extended; `{1,2,3}` and `{1,3}` die on 1 or 3; `{0,1}` dies only
by leaving to `{2,3}` via 1 or 2. The enumerated path shapes are exactly
(2). The order-sensitivity remarks are correct: `20*3` resets while
`30*2` needs one further letter, both confirmed against the table.
`H_j H_1` constant for all `j` confirmed (`H_1` image `{2,3}`, every `H_j`
identifies it). The empty word as identity is consistent.

## 2. Period alternatives: accepted with quantifiers verified (`partial-proof`)

The least-period hypothesis does load-bearing work and is used coherently:
`T` reads as an onset of the least eventual period `p` itself, and parity
counts over one length-`p` window are rotation-invariant, so even/odd is
well defined; the draft's explicit guard against arbitrary multiples
closes the `2p`-window parity trap. `p | q` via the local image
`Phi c = b` holds in all rows (row 1 forces `p = 1` through leastness, so
no `p|q` gap there). Row-by-row: all-zero onset `T+1` via `H_0^2 = H_0`;
`{0,2}` entry into `{1,3}` in at most `p+1` tail letters (first 2 plus next
letter, both images recomputed); `{0,3}` entry into `{0,1}` in at most `p`
letters with 0-as-identity and 3-as-swap confirmed; the last-letter
exceptions leave image exactly `{2,3}`, so one more tail letter collapses
them, and the `c_T`/`c_{T+p}` coupling argument correctly yields period `p`
from `T+p+1` with `a`-independence. The `p = 1` onset-attainment example
`0,3,2,2,...` is correct. No-doubling adjacency is exact: doublings land
in `{1,3}` or `{0,1}` visiting both points, so the next drive contains 1
and synchronizes; (3) follows, including `d_m <= ceil(m/2)` with exact
least periods `p_m = p*2^{d_m}` for arbitrary fringe symbols. Nothing here
constrains pre-tail diagonal values, as the draft honestly states.

## 3. Section 3: accepted (raised corrections withdrawn in Section 8)

The contradiction chain is valid: (6) from FULL, the `{0,3}`-exclusion via
the recurrent 3, sync to one `p`, finiteness of the `4^p` code set giving
`m`-eventual-periodicity of `C_m`, and the imported branch/trace/Kopra
dependencies, all explicitly named with no hidden deduction. The negation
forming (4) is the correct negated quantifier. Two corrections:

(a) The two `Equivalently' claims overstate direction. `C_m` purely
periodic follows from `X_m` on-cycle, but not conversely: a mod-4 shadow
can cycle while higher `A`-bits stay transient, since low bits never
constrain high bits. Hence non-periodic `C_m` implies
`tau_A(W_m) > 2m`, but `tau_A(W_m) > 2m` does not imply non-periodic
`C_m`. Fix: downgrade both to `Consequently'/`In particular'. The proof
uses only the forward direction, so nothing else changes, and (5) stands
as a consequence with `tau` in `N UNION {infinity}`.

(b) The parenthetical `finite for every finite-entry y' is unproved as
applied to `W_m`, whose finite-entry status is not established in the
draft. Fix (a) already moots this: with `infinity` allowed, (5) needs no
finiteness. Alternatively prove finite-modification stability separately;
not required here.

## 4. Kopra-free simplification: sound, with exact honest scope

The proposed chain is valid modulo already-reviewed dependencies: same-`p`
`m`-periodic `C_m` (kept from Section 2, which still uses FULL for (6) and
the recurrent 3) plus `Theta` injectivity gives a finite `X_m` value list;
eventual finiteness of rows (same finite-propagation fact as the draft)
plus even-time center 1 gives finite nonzero values; on-branch
`F(X_m) = 4A^2(X_m)+3` with exact bit-length preservation by `A` yields
`bitlen(X_{m+1}) = bitlen(X_m)+2` per step, against the finite list. The
`X_{m+1} = F(X_m)` step itself follows from `Theta` conjugacy
(`Theta(4y+3) = I_3 Theta(y)`), `Theta(A^2 x) = shift^2 Theta(x)`, and
injectivity; these should be cited explicitly when the simplification is
written, but none is a new gap.

Honest scope, as the lead already intends: the terminal step uses nothing
about which fringe is actual beyond gate retention, so it excludes
same-`p` eventually-`m`-periodic `C_m` tails along ANY infinite permitted
`F`-orbit with finite values, and discriminates no actual fringe. FULL is
still assumed (for (6) and the `{0,3}`-exclusion); only Kopra and the
fringe-language trace identity are shed. Non-eventually-periodic `C_m`
behavior in `m` remains untouched and `inconclusive`.

## 5. Status summary

Reset language and period alternatives: `partial-proof`, accepted in scope
with no change requested. Full-fringe consequence: `partial-proof`,
accepted with no pending corrections (former 3(a)-(b) withdrawn and
superseded per Section 8). Bit-length simplification: adopted in the draft;
assessed sound as scoped in Sections 4 and 6. Obstruction certificate:
`partial-proof` for the identities, `refuted` for the two stated
hypotheses (Section 7). No computation proposed or authorized by this review.

## 6. Re-review of edited Section 3 (Kopra replaced by bit-length growth)

The edited proof is valid and strictly leaner: same-`p` sync (kept, still
using FULL for (6) and the recurrent 3), `Theta` injectivity to a finite
`X_m` value list, eventual finite nonzero rows, then (7) with exact
bit-length preservation giving `+2` per block against eventual repetition.
The `X_{m+1} = F(X_m)` step rests on the imported conjugacy
`Theta(4y+3) = I_3 Theta(y)`, `Theta(A^2 x) = shift^2 Theta(x)`, and
injectivity; worth citing explicitly, but no new gap. [The next two sentences are superseded by Section 8 and retained for audit.] Two prior
corrections are still outstanding in the current text: the `Equivalently'
before `X_m is not an A-periodic point' remains bidirectional while only
the forward direction holds (periodic shadow does not imply on-cycle
state), and the `finite for every finite-entry y' parenthetical still
assumes `W_m` finite-entry without proof. Same one-word fixes: downgrade
to `Consequently' with `tau` in `N UNION {infinity}', which moots the
finiteness point. The added general `F`-orbit scope is coherent: any
infinite permitted `F`-orbit with finite-entry start has finite values
with `+2` bit-length per step, hence cannot be eventually periodic in `m`;
this discriminates no actual fringe, as now stated. Section 3 accepted as
`partial-proof` pending those unchanged wording fixes.

## 7. After/reset review: cycle-entry obstruction certificate

I independently recomputed every line: `A(55) = 50`, `A(50) = 55` (2-cycle,
consistent with the known 50/55 core); `F(55) = 223`; `A(223) = 200`,
`A(200) = 222`, `A(222) = 200` (200/222 2-cycle, 223 strictly transient,
all bit operations verified). Zero-fringe `W_1 = 220` gives
`220 -> 201 -> 223 -> 200 <-> 222`, three states off-cycle, so
`tau_A(W_1) = 3 > 2` with `D_0 = D_1 = 3` and a genuine alternating block
at times 0-3. Temporal cross-check also verified: `Theta(55) = (3,2)^inf`,
`I_0 b = 0,1,3,0,2,0,2,...` with least preperiod exactly 3 (attaining the
primary note's `T+p+1` onset bound), and `C_1 = Theta(223) = 3,0,2,0,2,...`
recomputed both ways. `223 mod 16 = 15` sits outside both gates, so the
`F`-orbit terminates and no infinite survivor is claimed; the note states
this boundary explicitly, and it does not touch FULL-conditioned claims.
Both `refuted' labels are correctly scoped to the two universal shortcuts,
and the `inconclusive' fence in its Section 3 is honest. Accepted as
`partial-proof` for the identities and `refuted` for the two stated
hypotheses. It coheres with the primary note: a valid early block with
late cycle entry is exactly the transient alternative that Section 4
leaves open, and the terminating gate-15 state is consistent with the
general `F`-orbit non-repetition scope in Section 6 above.

## 8. Correction withdrawal and fresh Section 3 review (lead rebuttal sustained)

Reviewed source (current version):
`problem1_inverse_scan_reset_language.md`
SHA256 `f7c5cc481d4fac7d90783a28d2028898b312e3e75dfdd6f1ed80011df6c2f406`;
companion obstruction note SHA256
`5584c7178b1ed20217e0a6321dfb1b154fd6cd7beeb96b8c891c9556f7a5dd2b`.
The superseded initial review is preserved for audit at
`/tmp/astra-round7-reset-review-initial.md`.

Withdrawn rejected argument (mine, retained explicitly): in former
Section 3(a) I claimed the `Equivalently' overstated direction because `a
mod-4 shadow can cycle while higher A-bits stay transient, since low bits
never constrain high bits.' This is false as applied to `Theta`: low bits
at one time do not constrain high bits, but `Theta(X)` records low bits at
ALL times, and that joint record determines `X` triangularly. Independent
rederivation: if `C = Theta(X)` satisfies `C_{t+p} = C_t` for all `t`, then
`Theta(A^p X)_t = A^{t+p}(X) mod 4 = C_{t+p} = C_t`, so
`Theta(A^p X) = Theta(X)`, and injectivity gives `A^p X = X`; i.e. `X` is
on-cycle. The generic-shadow intuition ignored the temporal span of the
code. No weakening of the equivalences: with the homeomorphism, `C_m`
purely periodic holds exactly when `X_m` is A-periodic, and (4) holds
exactly when (5) holds. Correction 3(a) is withdrawn in full.

Correction 3(b) is superseded by the lead's proof, here rederived: from
`W_m = 4W_{m-1}+a_m`, `pi^m W_m = x`; commuting gives
`pi^m A^h W_m = A^h pi^m W_m = A^h x`, finite by the entry hypothesis; a
2-adic whose `pi^m`-image is finite is itself finite (finite high part plus
2m low bits), so `A^h W_m` is finite and `W_m` is finite-entry. A finite
`z = A^h W_m` is fixed (zero) or stays in its finite width class by exact
bit-length preservation, so its orbit cycles and `tau_A(W_m)` is finite.
The parenthetical holds as stated, generally.

Fresh quantifier check of current Section 3: the (4) negation is the exact
negated quantifier; both equivalences are now exact per the rederivation
above; `tau` finiteness is proved, so (5) typechecks; (6), the `{0,3}`
exclusion via the recurrent 3, sync to one `p`, the `4^p` code set with
`m`-eventual-periodicity, `Theta` injectivity to `X_m`, eventual finite
nonzero rows, (7) with `+2` bit-length growth against eventual repetition,
and the permitted-`F` scope plus stopping fence all stand as previously
accepted. Section 3 is accepted as `partial-proof` with no changes
requested. Prior Sections 1, 2, 6, 7 of this review are unaffected.

## 9. Final hash record (headers-only update verified)

Both notes are untracked, so no Git diff exists. The metadata-only nature
of the update is established by lead-authenticated reconstruction, not by
this reviewer: reversing the one added status paragraph (reset note) and
the two added pointer lines (obstruction note) reproduces the exact
Section 8 reviewed sources, SHA256 `f7c5cc48...` and `5584c717...`
respectively. No line counts are asserted here; those are left to incoming
tool output. Current accepted hashes, verified unchanged just now:

- `problem1_inverse_scan_reset_language.md` SHA256
  `7b6848922bacb79ee8630fb36b98b4e7397992cb5e36ee80c7e18e37538b55f5`
- `problem1_scan_cycle_entry_obstruction.md` SHA256
  `5793bd078c48bbed28db85c72ede2ed9d0a119f8cde45ea804c905c00fb259e2`

Review accepted with no pending corrections; Section 8 retains the
withdrawn wording for audit.
