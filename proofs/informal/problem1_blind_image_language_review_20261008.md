# Independent review: all-width blind-image language

Status: **PARTIAL-PROOF** for the exact spatial image-language lemma at every
finite width. The temporal double-reset conjecture and Problem 1 remain open.

## Finding

I independently reconstructed the raw-context automaton and verified the
all-width chaining argument in
`problem1_blind_image_language_20261008.md`. I found no error in its context
encoding, transition relation, quotient, or infinite-word description.

Write the two raw rows as `a_j=X_j` and `b_j=X_j XOR Y_j`. The normalized
boundary pairs `(X_-1,Y_-1)=(1,0)` and `(X_0,Y_0)=(0,1)` therefore give raw
boundaries `(a_-1,b_-1)=(1,1)` and `(a_0,b_0)=(0,1)`. At column `j`, the raw
Rule 30 outputs are

    c_a = a_(j-2) XOR (a_(j-1) OR a_j),
    c_b = b_(j-2) XOR (b_(j-1) OR b_j).

Blindness through depth `r` is exactly `c_a=c_b` at every `j=1,...,r`.
When they agree, the common output is the normalized `X` output for either
driver label, since the label term multiplies the vanishing output `Y` bit.

The context `(a_(j-2),b_(j-2),a_(j-1),b_(j-1))` contains all information
needed for the next local test. Choosing `(a_j,b_j)` yields a transition
labelled by the common output if and only if both raw outputs agree, and shifts
the context to `(a_(j-1),b_(j-1),a_j,b_j)`. The initial context is `1101`.
Induction on the number of scanned columns proves both directions: every
accepted NFA path is a pair of raw prefixes with equal outputs at each column,
and every such pair of prefixes gives an NFA path. This proof has no width
cutoff; the finite context set gives the same local rule at every next column.

## Independent automaton check

My checker used tuple-valued contexts and a direct truth-table map for
`F(a,b,c)=a XOR (b OR c)`. It enumerated all 16 contexts and four next input
pairs per context, obtaining the 32 admissible labelled transitions. A direct
subset construction found 11 reachable subsets. A pair-distinguishability
table-filling minimizer (separate from the supplied Moore-refinement code)
found eight equivalence classes and the same initial-state numbering:

| State | On 0 | On 1 | Accepting |
|---:|---:|---:|:---:|
| 0 | 1 | 2 | yes |
| 1 | 2 | 3 | yes |
| 2 | 2 | 2 | no |
| 3 | 4 | 5 | yes |
| 4 | 4 | 6 | yes |
| 5 | 2 | 1 | yes |
| 6 | 2 | 7 | yes |
| 7 | 4 | 4 | yes |

The complete 32-transition list, all reachable subsets, and distinguishable
state-pair certificate are in the independent JSON record. Its raw transition
list, subset list, and subset-DFA transitions also compare exactly with the
supplied result. The supplied quotient identifications `A4~A8`, `A6~A9`, and
`A7~A10` respect acceptance and transitions, so quotienting preserves the
recognized language. The independent minimizer additionally confirms that
the eight states are minimal, though minimality is unnecessary for the lemma.

The infinite-word decomposition follows directly from the eight-state graph.
From state 0, a surviving path must read `0` then `1`, reaching state 3. At
state 3, reading `111` returns to state 3; reading `0` enters state 4. From
state 4, the return-to-state-4 blocks are exactly `0`, `110`, and `111`:
after a first `1`, state 6 forces another `1`, and state 7 then returns on
either symbol. Thus the infinite accepted words are

    0 1^omega
    or 0 1^(1+3k) 0 v,  where k>=0 and v in {0,110,111}^omega.

All nondead states have an infinite continuation, so each accepted finite word
is a prefix of an accepted infinite word; conversely every such prefix avoids
the dead state. The equivalent run statement is also correct: the initial
positive run of ones, when completed, has length `1 mod 3`; each later
completed positive run has length `0 or 2 mod 3`; a terminal infinite run of
ones is allowed. Finite observations constrain only runs that have already
ended.

## Scope, provenance, and remaining work

The result proves an exact spatial description of which common rows can arise
from a blind transition. It does not prove that this language is invariant
under a temporal passage between blind gates, that an impulse resets, or that
the proposed double-reset/return argument works. Those remain separate
obligations on the critical path.

- Repository full commit: `ddc53f28dbe30a98764f3dec8a7725ec5be1dbe8`
- Reviewed proof-note SHA-256: `efaf0e45055751d13324eb96d52f14f03e6e70b20553898ae348bbb90416b9b7`
- Producer script SHA-256: `1dd6a0a6e7f02b88a262626be8dd2b04bae1f07434f51c45e974729d89a18437`
- Producer JSON SHA-256: `163492e94844d9188832d6db429eb4d78f993e3319c149f9c127604d98a50175`
- Independent verifier SHA-256: `5aea054f2edda66ba26546f6bb7b50ac23c519000a7f4af3f696238471f17d58`
- Independent JSON SHA-256: `bc68dacd1d9856e2c2b608e967a5756b59ce56540ec8c6a0a31eabbcf42f236b`

The independent run used Python 3.12.14, completed in under one second, and
peaked below 16 MiB resident memory. Its JSON records the exact domains,
transition table, software/hardware facts, full commit, source hash, and
canonical payload hash. Problem 1 remains open.

## Review update: complete infinite rows

I reviewed the revised proof note at SHA-256
`06801f188ccf25f1ec9ca1acbc023a600bf76b2a52ae24d0c44ddd3c8ca421a6`.
The finite-branching paragraph is valid: accepting paths exist at every
prefix depth, and the context tree is finitely branching, so an infinite
consistent raw-row path exists. Section 5 also correctly distinguishes the
refuted transient selector law from the cyclic gate theorem.

The eventually-zero corollary in Section 6 is sound. For either prescribed
constant tail, the backward recurrence determines that raw row uniquely all
the way to the fixed left boundary. The earlier opposite-tail argument shows
that any valid pair uses both tail choices. Existence of a valid pair supplies
the boundary-compatible order, and `a_0=0`, `b_0=1` selects that order
uniquely. Thus the update's uniqueness proof is consistent with, and shorter
than, my earlier terminal-context argument. This claim concerns a complete
infinite spatial row only; it gives no finite-support budget for the physical
orbit.

## Review update after proof-note revision

I reviewed the revised source note at SHA-256
`06801f188ccf25f1ec9ca1acbc023a600bf76b2a52ae24d0c44ddd3c8ca421a6`.
The finite-branching argument is valid: the prefix paths form a finitely
branching tree with a node at each depth, so an infinite raw preimage path
exists for each accepted infinite output word. The new Section 6 is also
correct. An eventual constant tail fixes two adjacent row bits, and the
backward equation `a_(j-2)=C_j XOR (a_(j-1) OR a_j)` determines the entire row
back to the boundary. The opposite-tail result requires both tail choices in
any valid pair; their uniquely reconstructed rows have the distinct boundary
values 0 and 1, which fixes their ordering. Thus each complete eventually-zero
common output has exactly one ordered raw preimage pair. This does not apply
to a finite prefix that merely ends in zeros.

The revised Section 5 also accurately distinguishes the refuted transient
selector law from the cyclic gate theorem. I found no issue in these additions.
