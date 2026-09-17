# Astra automation handoff — run 81

## Main result: boundary-to-diagonal endpoint map is bijective

Run 80 proved every post-zero boundary state `(x,0)`, `x != 0`, reaches a diagonal state `(a,a)` in finite time. Combining that with off-zero injectivity gives a stronger global statement.

At fixed period `p`, define `rho_p(x)=a` when the connector launched from `(x,0)` first reaches `(a,a)`. Then

`rho_p : {nonzero p-bit words} -> {nonzero p-bit words}`

is a bijection.

Proof idea: if two boundary states reached the same diagonal endpoint, injectivity lets us cancel the common suffix backwards. Equal connector lengths force equal boundary states; unequal lengths force one boundary state to have an off-zero predecessor, impossible because every image of the off-zero map has nonzero second component. Since boundary and nonzero diagonal each have size `2^p-1`, injectivity implies bijectivity.

Full proof:

`proofs/informal/problem1_boundary_diagonal_bijection.md`

## Consequences

- The boundary-reachable transient dynamics decomposes into exactly `2^p-1` pairwise-disjoint finite chains, each joining one boundary word to one distinct diagonal word.
- Off-diagonal periodic cycles may exist, but they are disjoint from all these chains.
- Every boundary connector has the crude unconditional length bound `< 2^(2p)`, more explicitly at most `1 + (2^p-1)(2^p-2)` T-steps under the counting convention used in the proof.
- The long-connector problem can be reframed as finding the induced bijection `rho_p` without traversing its chains column by column.

## Next target

Study `rho_p` itself. In particular, test/derive whether `rho_{2p}` obeys a recursion on doubled words and on the antiperiodic integrations arising from doubled odd leaves. A direct recursion for `rho_{2p}` could bypass the >100,000,000-step p=32 connector entirely.