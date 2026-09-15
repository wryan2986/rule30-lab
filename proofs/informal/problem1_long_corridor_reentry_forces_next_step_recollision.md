# Long-corridor re-entry forces next-step same-period recollision

Status: `partial-proof`. This is a direct global-use corollary of the exact collision/re-entry results through run 31; it does not close Problem 1.

## Statement

Let `z` be a finite `A^p`-fixed row with return fringe

    T^p(z)=2^(2p) z + R,

and positive corridor `G=2p-bitlength(R)`. Put `D=floor(G/2)`. The established corridor geometry says that the first same-period boundary collision occurs at

    x=T^(D+1)(z).

Assume this collision immediately re-enters the same `A^p`-fixed class, and write

    z'=T(x)=T^(D+2)(z).

Let `R'` be the return fringe of `z'` and `G'=2p-bitlength(R')`.

For every long corridor `G>=3`, the run-30/run-31 results give

    G'=0                         if G is even,
    G' in {0,1}                  if G is odd,

with the odd value exactly

    G'=1 XOR H(R) XOR (D mod 2),

where `H(R)` is the four-leading-bit flag from the exact commutator/fringe-core theorem.

Therefore in all cases

    floor(G'/2)=0.

Applying the same first-collision formula to the re-entered state `z'`, its next same-period collision is

    T^(floor(G'/2)+1)(z') = T(z').

Hence:

> After an immediate re-entry from any corridor `G>=3`, the re-entered `A^p` phase cannot enjoy even one further collision-free physical step. Its very next physical successor is again a same-period boundary collision.

Equivalently, a long same-period corridor followed by immediate re-entry has a terminal same-period residence tail

    ... -> x (collision) -> z' (re-entered fixed row) -> T(z') (collision).

The only way to continue beyond this point without confronting another collision is to change the effective period/phase mechanism at that next step. A long corridor cannot regenerate directly at the same period after re-entry.

## Why this is useful globally

The older FULL/common-origin bottleneck allowed arbitrarily sparse births/nonresetting sources, so spacing alone could not bound them. The local corridor work now gives a stronger structural restriction than spacing: every successful long-corridor same-period repair immediately lands at a state whose same-period safe residence is exactly one row (the re-entered row itself).

Thus any hypothetical finite survivor with infinitely many long corridors cannot obtain those corridors by repeatedly repairing and remaining in one fixed `p`-phase. Between successive long corridors it must pass through a new period/phase episode after the forced next-step recollision.

This does **not** yet prove that the period must increase, nor that only finitely many such changes can occur. Those are the remaining global questions. In particular, no monotonicity of minimal `A`-period under physical `T` is asserted here.

## Dependency boundary

Used results:

- `problem1_immediate_reentry_collapses_return_corridor.md`: even `G>=4` gives `G'=0`; odd `G>=3` gives `G'<=1`.
- `problem1_exact_odd_reentry_gap_from_four_fringe_bits.md`: exact odd `G'` formula.
- established corridor geometry: first collision from a fixed row with corridor `G` is at physical offset `floor(G/2)+1`.

No new finite census, gate-prefix search, or density assumption is used.
