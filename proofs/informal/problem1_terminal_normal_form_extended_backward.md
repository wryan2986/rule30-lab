# Problem 1: extended backward terminal normal form

## Status

Problem 1 remains open. This note continues the exact reverse-predecessor calculation from the run-57 terminal normal form.

Let

    q_(i+2) = S q_i xor (q_(i+1) OR q_i)

on cyclic binary words of even temporal length `p`. Let `N` be the first index with `q_N=q_(N+1)=0`, and write `A=alt_p` for the alternating word forced at `q_(N-4)`.

Run 57 proved

    q_(N-4),...,q_(N+1) = A, 0, 1, 1, 0, 0.

Here `0` and `1` denote the constant all-zero and all-one words.

## Four more predecessors are forced

Assume the indicated predecessor indices exist.

### 1. q_(N-5) = 1

Put `x=q_(N-5)`. Since `q_(N-3)=0` and `q_(N-4)=A`,

    0 = Sx xor (A OR x),

so `Sx=A OR x`. Because `A` contains a 1, the bit immediately after such a position in `x` is 1. Thereafter `x_j=1 => x_(j+1)=1` propagates around the cyclic word. Hence `x=1`.

### 2. q_(N-6) = A

Put `y=q_(N-6)`. Using `q_(N-5)=1` and output `q_(N-4)=A`,

    A = Sy xor (1 OR y) = Sy xor 1.

Thus `Sy=not A`. For an alternating cyclic word, `S A=not A`, hence `y=A`.

### 3. q_(N-7) = A

Put `z=q_(N-7)`. Using `q_(N-6)=A` and output `q_(N-5)=1`,

    1 = Sz xor (A OR z),

or `(Sz)_j=(not A_j) AND (not z_j)`. Choose phase `A_j=j mod 2`. Whenever `A_j=1`, this forces `z_(j+1)=0`; at the following position `A_(j+1)=0`, the just-forced zero gives `z_(j+2)=1`. Therefore uniquely `z=A`.

### 4. q_(N-8) = 0

Put `w=q_(N-8)`. Using `q_(N-7)=A` and output `q_(N-6)=A`,

    A = Sw xor (A OR w).

At `A_j=1` this gives `w_(j+1)=0`; at `A_j=0` it gives `w_(j+1)=w_j`. The forced zeros therefore propagate across every position, so `w=0`.

Thus every sufficiently long terminating trajectory has

    q_(N-8),...,q_(N+1)
      = 0, A, A, 1, A, 0, 1, 1, 0, 0.

## The first reverse branch: q_(N-9)

Now put `v=q_(N-9)`. Since `(q_(N-8),q_(N-7))=(0,A)`,

    A = Sv xor v.

This is the cyclic binary discrete-derivative equation. It is solvable iff `A` has even XOR parity. Since `A` contains exactly `p/2` ones, solvability is equivalent to

    p/2 = 0 mod 2,

that is,

    p = 0 mod 4.

When solvable, the kernel of `S xor I` consists exactly of the two constant words, so there are exactly two solutions, complementary to one another. Integrating the alternating right-hand side shows they are the two cyclic phases of the period-four pattern

    0011 0011 ...

(up to the shift convention for `S`).

Therefore, if the first zero pair occurs late enough that `q_(N-9)` exists (`N>=9`), then

    p is divisible by 4,

and the first reverse branching is exactly a two-element complementary/rotational pair of period-four words.

This sharpens run 57's necessary evenness condition. It also explains why the exceptional known `p=2` terminating trajectory can exist: its first zero pair occurs at `N=8`, so the `q_(N-9)` predecessor does not exist and this divisibility-by-four obstruction is never encountered.

## Pair-derivative interpretation

For `p=2m`, pair adjacent temporal coordinates compatibly with `A`. Under pair XOR derivative `Delta_2`,

    Delta_2(0)=0,
    Delta_2(1)=0,
    Delta_2(A)=1^m.

Hence the forced ten-column terminal block maps to

    0, 1, 1, 0, 1, 0, 0, 0, 0, 0

at half temporal length. The new period-four predecessor has a simple paired image as well: pairing `0011` in aligned adjacent pairs gives an alternating length-`m` word (with pairing phase determining its rotation/complement). Thus the first reverse branch at length `2m` lands, under `Delta_2`, on exactly the alternating predecessor that appears universally near the terminal basin at length `m`.

This is the first exact structural compatibility found between the reverse basins at successive temporal scales. It does not yet prove period halving, but it is stronger evidence than the earlier initial-necklace observation because it arises from forced reverse dynamics.

## Next target

Continue backward from the two period-four solutions for `q_(N-9)`. Determine whether their predecessor sets map under `Delta_2` to the predecessor set of the lower-period alternating state. If this compatibility persists inductively through every reverse branch, it would give the desired basin-level period-halving theorem without requiring a forward semiconjugacy.
