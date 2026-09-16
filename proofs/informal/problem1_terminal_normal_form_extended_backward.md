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

so

    Sx = A OR x.

Because `A` contains a 1, the bit immediately after such a position in `x` is 1. Thereafter the implication `x_j=1 => x_(j+1)=1` propagates around the cyclic word. Hence `x=1`.

### 2. q_(N-6) = A

Put `y=q_(N-6)`. Using `q_(N-5)=1` and output `q_(N-4)=A`,

    A = Sy xor (1 OR y) = Sy xor 1.

Thus `Sy=not A`. For an alternating cyclic word, `S A = not A`, hence `y=A`.

### 3. q_(N-7) = A

Put `z=q_(N-7)`. Using `q_(N-6)=A` and output `q_(N-5)=1`,

    1 = Sz xor (A OR z),

or bitwise

    (Sz)_j = (not A_j) AND (not z_j).

Choose the phase `A_j=j mod 2`. Whenever `A_j=1`, this forces `z_(j+1)=0`; at the following position `A_(j+1)=0`, the just-forced zero gives `z_(j+2)=1`. Therefore the cyclic word is uniquely `z=A`. The opposite phase is identical after rotation.

### 4. q_(N-8) = 0

Put `w=q_(N-8)`. Using `q_(N-7)=A` and output `q_(N-6)=A`,

    A = Sw xor (A OR w).

At a position with `A_j=1`, this gives `w_(j+1)=0`. At a position with `A_j=0`, it gives `w_(j+1)=w_j`. Since every zero position follows a one position (up to phase), the zeros forced after the `A_j=1` positions propagate across the remaining positions. Hence `w=0`.

## Extended universal suffix

Therefore every terminating reconstruction long enough to contain these indices has the forced terminal block

    0, A, A, 1, A, 0, 1, 1, 0, 0.

Equivalently,

    q_(N-8),...,q_(N+1)
      = 0, alt_p, alt_p, 1^p, alt_p, 0, 1^p, 1^p, 0, 0.

This is stronger than the run-57 six-column normal form and, importantly, there is still no reverse branching through four additional layers.

## Pair-derivative interpretation for p=2m

Pair adjacent temporal coordinates compatibly with `A`. Under pair XOR derivative `Delta_2`,

    Delta_2(0)=0,
    Delta_2(1)=0,
    Delta_2(A)=1^m.

Hence the forced ten-column terminal block maps to

    0, 1, 1, 0, 1, 0, 0, 0, 0, 0

at half temporal length. This is not by itself an ordinary lower-period reconstruction trajectory, consistent with the earlier no-semiconjugacy result, but it gives an exact boundary condition that any reverse-basin period-halving proof must satisfy.

## Next target

Continue one predecessor farther back from the newly forced pair `(q_(N-8),q_(N-7))=(0,A)`. This is the first promising place to check whether genuine reverse branching begins. If it does, classify that branch set modulo cyclic rotation and track its pair derivative; if it does not, continue extending the universal terminal word. The goal remains the weaker implication that termination at length `2m` forces `Delta_2(c)` into the terminating basin at length `m`.
