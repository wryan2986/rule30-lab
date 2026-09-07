# Single inverse-scan temporal forcing: sharp bounds and exact scope

Status: `partial-proof` for the single-scan lemma as an independent hand
check; SUPERSEDED as a result by the lead's exact reset language and
least-period alternatives (`problem1_inverse_scan_reset_language.md`,
Sections 1-2), from which its bounds follow as coarse corollaries. No new
substantive infrastructure is claimed here. The residual incompatibility of
FULL with finite entry is `inconclusive`. Problem 1 remains open. No
computation was run and none is admitted.

## 0. Scope, as corrected after lead audit

The prior version's `precise no-go' is withdrawn as invalid: `2m` lying
below an *upper bound* on `T_m` does not imply `2m < T_m`. The zero code
`b = 0` gives all-zero scans with actual `T_m = 0`, a direct counterexample
to the wording. The worst-case bounds below therefore decide nothing about
the diagonal values in either direction; they do not supply an
implication, and equally no impossibility of other routes is claimed. What
this note supplies is only an independent coarse check of per-scan forcing
(multiplier at most 2, transient at most `+2p` uniformly); the exact
reset language, parity doubling criterion, and no-adjacent-doubling bound
in the lead note supersede it. Imports are as before: `Theta`, `Phi`, `I_a`, `h` from
`problem1_full_fringe_temporal_diagonal.md`; the dyadic clock from
`problem1_frontier_head_dynamics.md` Section 2.

## 1. Exact state maps of one scan (`partial-proof`)

Write state `a = a0 + 2a1` and input symbol `(r, s)` with
`h((a0,a1),(r,s)) = (r XOR (a0 OR a1), s XOR (a1 OR r))`. Direct expansion
gives the full scan table `M[a][input]`, rows matching equation (3) of the
diagonal note:

```text
a=0:  [0,3,2,1]    a=1:  [1,2,3,0]
a=2:  [3,2,1,0]    a=3:  [3,2,1,0]
```

Fixing the input symbol gives the four driven state maps `H_i(a) = h(a,i)`
(columns of the table):

```text
H_0: 0->0, 1->1, 2->3, 3->3     (rank 3, projection, H_0^2 = H_0)
H_1: 0->3, 1->2, 2->2, 3->2     (rank 2, H_1^2 = const 2)
H_2: 0->2, 1->3, 2->1, 3->1     (rank 3, swaps {1,3})
H_3: 0->1, 1->0, 2->0, 3->0     (rank 2, swaps {0,1})
```

## 2. Single-scan forcing lemma, sharpened (`partial-proof`)

Lemma. Let `b` satisfy `b_{t+p} = b_t` for all `t >= T0`, and put
`c = I_a b`, i.e. `c_0 = a`, `c_{t+1} = H_{b_t}(c_t)`. Then `c` is eventually
periodic with transient at most `T0 + 2p` for every drive word, and eventual
least period dividing `2p`.

Proof. For `t >= T0` the drive is the periodic word
`w = b_{T0} ... b_{T0+p-1}` with one-period return map
`F_w = H_{w_{p-1}} ... H_{w_0}` on four states. Every return cycle has
length `L <= 2`: if `w` contains 1 or 3 then `rank(F_w) <= 2`; otherwise `w`
uses only `{0,2}`, and then (i) `H_0` fixes `{1,3}` pointwise while `H_2`
swaps them, so every such `F_w` preserves `{1,3}`, while (ii) no
`{0,2}`-composition maps 2 to 0, by induction on length (length one:
`H_0(2) = 3`, `H_2(2) = 1`; the step holds since `H_2` never outputs 0 and
`H_0(y) = 0` iff `y = 0`). A cycle of length 3 or more meets `{1,3}` and is
contained in it by invariance, of length at most 2; a 4-cycle likewise. So
the tail period `pL` has `L` in `{1,2}` and the least tail period divides
`2p`. For the transient, `F_w^2` always lands in the recurrent set. If
`w` contains 1 or 3, `Im(F_w)` has at most two points and is invariant, and
every point of a self-map on at most two points reaches a cycle in at most
one further step. If `w` uses only `{0,2}`, `F_w` restricts to a permutation
of `{1,3}` (identity or swap according to the parity of `H_2` factors), so
`{1,3}` points are already recurrent; state 2 enters `{1,3}` at the first
applied letter, hence `F_w^2(2)` is on-cycle; state 0 is fixed when `w` is
all zero (`F_w = H_0`), and otherwise goes `0 -> 2` at the first `H_2`
factor with `2 -> {1,3}` at the next letter, so it lies in `{1,3}` after at
most two full cycles and `F_w^2(0)` is recurrent. Thus the return transient
is at most 2 steps for all words, i.e. time transient at most `T0 + 2p`. The
same induction gives `F_w(2)` never 0 or 2 for `{0,2}`-words.

Sharpness is by hand identities on infinite eventually cyclic words
(`partial-proof`, not finite observations): constant input 3 from `a = 0`
gives `0,1,0,1,...` since `H_3` swaps 0 and 1, attaining multiplier 2;
constant input 1 from `a = 0` gives `0,3,2,2,...` since
`H_1: 0 -> 3 -> 2 -> 2`, attaining transient `2 = 2p` with collapse to
period 1; constant input 2 from `a = 0` gives `0,2,1,3,1,3,...`, transient 2
then the `{1,3}` 2-cycle. No multiplier 3 or 4 exists for any word.

## 3. Iterated bound with corrected finite-entry hookup (`partial-proof`)

Put `B_0 = b`, `B_{m+1} = I_0 B_m`, with `B_m` of transient `T_m` and least
period `p_m`. The lemma gives `T_{m+1} <= T_m + 2p_m` and
`p_{m+1} | 2p_m`, whence `p_m | p*2^m` and `T_m <= T0 + 2p(2^m - 1)`.

Finite entry with entry height `h`, where `A^h x` has binary width `W`:
for `W > 0` the width-`W` dyadic clock starts only after entry, so
`T0 <= h + 2^{W-1} - 1` with dyadic `p | 2^{W-1}` (the earlier version
omitted `h`; corrected here). For `W = 0` (`A^h x = 0`), `b_t = 0` for all
`t >= h`, i.e. `T0 = h`, `p = 1`. Periods stay dyadic under scans: `p_m | 2^{W-1+m}` for `W > 0`, and
`p_m | 2^m` for `W = 0` (where `p = 1`).

Exact scope: each `T_m` is an upper bound only, and actual entry can be far
earlier (the zero code has actual `T_m = 0` against an exponentially growing
bound). The iterated bound is therefore infrastructure for any future
word-level argument, which inherits the uniform `+2p` per-scan budget; by
itself it constrains no diagonal value and refutes none. Whether
`(I_0^m b)_{2m} = 3` for all `m` is compatible with finite entry remains
`inconclusive`.

## 4. Computation record

No computation was run and none is admitted. The identities in Section 2
are proved by hand; no run is needed for them.

## 5. Implication for the next step

Superseded. The lead's exact reset-language and period-alternative theorem
governs all single-scan forcing; this memo's uniform bounds follow from it
as coarse corollaries and are retained only as an independent check. The
live question stays with the lead's coupling route: FULL implies unbounded
anchored activity on the same `b`, or the finite-entry alternative
exhibited compatibly.
