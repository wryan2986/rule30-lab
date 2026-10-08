# Independent review: autonomous period-two half-row maps

Status: **PASS for the stated local identities and injectivity claim**;
**FINITE-EXHAUSTIVE** for the independent bounded controls. This review does
not prove termination of the gate and does not solve Problem 1.

## Mathematical review

I derived the two-step compatibility equations directly from
`F(h,l,x)=h XOR (l OR x)`. For `L=3 mod 4`, the initial center and its left
neighbor are both one, so the next center is zero. Writing `ell_j` for the
bits of `L` and `r_0,r_1` for the first two bits of `R`, one literal update
gives

    x'_-1 = 1 XOR ell_2,       x'_1 = 1 XOR (r_0 OR r_1) = q(R).

The next center and left neighbor are

    x''_0  = 1 XOR ell_2 XOR q(R),
    x''_-1 = ell_3 XOR ell_2.

Both are one iff `(ell_2,ell_3)=(q,1 XOR q)`. Along with
`ell_0=ell_1=1`, this is exactly `L=7 mod 16` when `q=1` and `L=11 mod 16`
when `q=0`. This establishes both necessity and sufficiency of the stated
gate for the pair `(center,left-neighbor)` to return to `11` after two steps.

The complete-half maps also check out. At left output site `-(j+1)`, the
local inputs are bits `ell_(j+2),ell_(j+1),ell_j`, so deleting the low bit
of the new left half gives `A(L)`. Since `A(z)>>1=A(z>>1)`, two updates give
the upper left half `A^2(L)`; the gate supplies its low bits `11`, hence
`Psi(L)=4A^2(L)+3`. For the right half, one update with center input `c` is
`D(R) XOR c`; the two center inputs are `1,0`, giving
`F(R)=D(D(R) XOR 1)`. This retains the whole finite right half.

The infinite-orbit equivalence in section 3 is valid: under every successful
gate, the two-step identity supplies the actual complete halves at the next
center-one phase, so induction gives sufficiency. An alternating center
forces its left neighbor to be one at each center-one phase; applying the
same local equations gives the gate at each iterate, proving necessity.
Rebasing an eventual alternating center trace is legitimate for a finite
support row because every finite-time Rule 30 row still has finite support.
The note correctly leaves universal gate termination open.

The inverse argument in section 5 is sound on ordinary finite integers.
For `J(z)=z XOR ((z>>1) OR (z>>2))`, output bit `y_j` determines input bit
`x_j` from already determined higher bits. Descending from above the highest
set bit gives a unique finite preimage and proves that `J` is a bijection.
The identities `D(z)>>1=J(z)`, `J(z)>>1=J(z>>1)`, and
`F(R)>>2=J(J(R))` then give the unique candidate
`R=J^(-2)(R_next>>2)`. The full forward check is necessary because the
discarded two low output bits impose an image condition; the note explicitly
retains that check.

For the left inverse, expanding the two applications of `A` gives the
furthest-bit recurrence

    (A^2 L)_j = ell_(j+4) XOR B(ell_j,...,ell_(j+3)),

where, with `a_j=ell_(j+2) XOR (ell_(j+1) OR ell_j)` and
`a_(j+1)=ell_(j+3) XOR (ell_(j+2) OR ell_(j+1))`, one valid explicit form is

    B = (ell_(j+3) OR ell_(j+2)) XOR (a_(j+1) OR a_j).

Thus fixed low four input bits and the whole output determine all later
input bits recursively. There is at most one ordinary finite left preimage
for each fixed gate branch, though there need not be a finite preimage at
all. Since the recovered right half fixes `q(R)`, it fixes which low-four-bit
branch is permitted. This proves injectivity of the full map
`(Psi,F)` on admissible finite pairs. It does not assert that the left map
alone is injective, and the displayed `171/199` collision correctly
illustrates why the right branch matters. The warning distinguishing a
finite integer from an infinite recursively generated (2-adic) bit sequence
is essential and correctly stated.

The added 16-state test for one inverse passage is also correct. For a
low-to-high input window `(a,b,c,d,e)`, direct expansion gives

    (A^2 L)_j = e XOR [(d OR c)
                       XOR ((d XOR (c OR b)) OR (c XOR (b OR a)))].

The verifier checked this equality for all 32 five-bit windows. The update
`e=y XOR B(a,b,c,d)` followed by `(a,b,c,d)<-(b,c,d,e)` therefore decodes
each next input bit from the next output bit, starting from the prescribed
gate residue 7 or 11. If `z>0` has `N` bits, any finite preimage must have
exactly `N` bits because `A^2` preserves positive bit length; hence the
window after those `N` steps must be zero. Conversely, a zero terminal
window stays zero for all later zero output bits because `B(0,0,0,0)=0`,
so it yields a finite preimage. For `z=0`, the only finite preimage under
`A^2` is zero, which matches neither gate residue. This is a valid exact
finite-support criterion for a single inverse branch and a single output;
it says nothing about termination of iterating the diagonal phase map.

I found no algebraic or indexing error in the reviewed note. The bounded
checks below independently corroborate the formulas; the all-integer
conclusions above rest on the displayed local identities and recurrences,
not on extrapolating those checks.

## Independent finite controls

The checker used a sparse dictionary of one-cells and a literal Rule 30
update, separately from its integer formulas for `A`, `D`, `Psi`, `F`, `J`,
and the inverse recurrences. It exhausted all 4,096 pairs with
`0 <= L < 256`, `L=3 mod 4`, and `0 <= R < 64`. Of these, 1,024 passed the
gate and 3,072 failed. Every pair had first-step center zero; after two
steps, the center and left neighbor returned to `11` exactly for the 1,024
gate pairs. All 1,024 valid pairs matched the entire proposed `Psi` left
half, while all 4,096 right halves matched `F`; the upper left bits matched
`A^2(L)` for all 4,096 pairs, including invalid gates. The full successor
pairs were distinct over the 1,024 valid controls.

The additional integer checks confirmed the stated bit-length growth, the
explicit `A^2` local recurrence for 49,152 bit positions, and both inverse
directions for `J` on 4,096 inputs. The proposed `F` inverse recovered all
4,096 generated successors. For arbitrary candidate successors below 1,024,
the script performed the required forward check and rejected 768 candidates;
for example, candidate output `0` yields inverse candidate `0`, whose actual
image is `3`. The controlled left recurrence recovered all 64 tested
`L=3 mod 4` inputs in its finite range with their fixed low-four residues,
including both gate-compatible and other residues. It also
recovered the two distinct inputs `171` and `199` from the common upper
output `A^2(L)=202` once their respective low-four branches `11` and `7`
were supplied. The appended 16-state criterion passed all 32 local-window
truth cases and all 8,192 comparisons (every `z<4096`, each of the two gate
branches) against the exhaustively tabulated finite preimages; 512
branch/output pairs had terminal state zero and a finite preimage.

The run took 0.21 seconds in CPython 3.12.14 on Linux x86-64. The checker
enforced a 60-second CPU/wall limit and a 256 MiB address-space limit. The
atomic JSON record carries the exact domains, provenance, and canonical
payload hash.

## Provenance and scope

- Reviewed note SHA-256: `cf712dfcdcb59fc7c303671918f6e62fe85f2de242a0926eb676c47df458772b`
- Independent verifier: `experiments/problem1_nonperiodicity/verify_period_two_phase_maps_20261008.py`
- Verifier SHA-256: `299c288f1613b113831e246e7f44ba231d9bf8f45fb3a51190c6a1ae02003546`
- Result: `results/problem1/20261008_period_two_phase_maps_independent.json`
- Result SHA-256: `dfbd551fb61d7dd2115b6a4e7634102280d67c81ab2100baa7cb4744be45b355`
- Git commit observed: `ddc53f28dbe30a98764f3dec8a7725ec5be1dbe8`

The exact all-iterate termination claim remains open. The finite controls do
not establish that every finite pair eventually violates the gate, nor do
they rule out an infinite admissible orbit.

## Addendum: global-support bridge review

Reviewed `proofs/informal/problem1_global_support_bridge_20261008.md`
(SHA-256 `44b55833614658a62f528e6085f22c50e9b5ba136962c16ba76262b850beadcb`).
The old-notation identity and the original-cut delay orientation are
consistent with the phase-map derivation and the repository's global-front
identities.

For the notation check, `T(z)>>2=A(z)` follows by shifting
`T(z)=z XOR ((z<<1) OR (z<<2))` right by two. Bitwise, for `L=4w+3`,
`A(L)` has bit zero `w_0 XOR 1`, bit one `w_1 XOR 1`, and for `j>=2` bit
`w_j XOR (w_(j-1) OR w_(j-2))`; these are precisely the bits of
`P(w)=T(w) XOR 1 XOR (2 if w is even else 0)`. The gate gives
`w=1 mod4` when `q=1` and `w=2 mod4` when `q=0`. In the first case
`P(w)=2 mod4`, so `T(P(w))=2 mod4` and flipping bit zero via `U_1`
forces low bits `11`; in the second case `P(w)=1 mod4`, so `T(P(w))`
already has low bits `11`. In both cases its upper bits are `A(P(w))`,
giving exactly `L_next=4A^2(L)+3`. Thus the branch-specific inverse formula
uses the correct order: apply `u` or `t` first, then `p`, then form
`4w+3`. The two inverse descriptions select the same unique 2-adic branch;
ordinary finiteness remains exactly the terminal-zero condition already
reviewed above. The addendum uses `t,u,p` for inverse maps as explicitly
defined in the bridge; this is clear from its local definition.

The cut-delay identity has the correct orientation. The existing physical
front relation is `Y_t=L_0(r(t))=A^t L_t(r)`; the least-preperiod identity
then gives `tau(Y_t)=max(tau(L_t(r))-t,0)`. Extending an original cut past
the right support gives `L_(b+n)(r)=2^n L_b(r)`, so substitution yields
`tau(Y_(b+n))=max(tau(2^n v)-(b+n),0)` with the stated signs and offset.
The bridge keeps one fixed original seed and does not turn a finite inverse
test into an all-iterate termination argument. No nine-state composite
automaton claim is used or accepted here.
