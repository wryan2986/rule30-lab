# Astra automation handoff — run 79

## New exact result

The off-diagonal-cycle obstruction identified in run 78 is real.  For every even ambient period `p`, the two complementary alternating words

`a = 0101...01`, `b = 1010...10`

form an exact period-two orbit of the off-zero inverse pair map:

`(a,b) -> (b,a) -> (a,b)`.

Proof: taking predecessor `y=b`, `S b=a` and `a OR b=1^p`, so `S b XOR (a OR b)=a XOR 1^p=b`; uniqueness gives the transition.  The symmetric step returns.

Therefore no proof can establish return existence by ruling out off-diagonal cycles in the ambient inverse dynamics.  It must exploit special structure of singular-integration / doubled-leaf portal states.

Full note:

`proofs/informal/problem1_offdiagonal_cycle_family_and_parity_identity.md`

## Exploratory exact census

Exhaustive small-period enumeration found off-diagonal temporal cycles (without spatial-rotation quotient):

- p=1: 0
- p=2: 1, length 2
- p=3: 0
- p=4: 2, lengths 2 and 12
- p=5: 2, lengths 5 and 110
- p=6: 8, lengths 2, 39, 60

Odd periods are therefore not automatically cycle-free either.

## New parity identity

For one unique inverse step `T(a,b)=(y,a)`, the predecessor equation implies

`P(b) = P(a & ~y)`.

Equivalently along consecutive inverse columns,

`P(x_{t-1}) = P(x_t & ~x_{t+1})`.

This is an exact local constraint on any off-diagonal periodic orbit and may be useful when combined with portal-specific antiperiodicity.

## Next target

Do not spend the next run trying to prove the ambient map cycle-free; that is false.  Focus on separating doubled-leaf portal states from the periodic set, ideally using an invariant inherited from the portal relation `S^p x = complement(x)`, or implement exact cycle detection for the first p=32 portal rather than merely extending its no-return iteration bound.
