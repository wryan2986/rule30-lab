# Problem 1: canonical doubling layer inside every finite period-16 core

Status: exact structural reduction; Problem 1 remains OPEN.

## 1. Statement

Let `x>0` be a finite `A`-periodic state of exact period 16. Put

    x_j = x >> j.

Repeated one-bit projection commutes with `A`, and the exact one-bit cycle-lifting theorem says that the exact period at each lift either stays fixed or doubles. Since `x_j=0` for all sufficiently large `j`, there is a largest projection depth `j` at which the exact period is still 16. Equivalently,

    per(x_j)=16,   per(x_(j+1))=8.                    (1)

(The parent period cannot be 1,2, or4, because one lift can increase exact period by at most a factor two.)

Write

    u=x_(j+1),   x_j=2u+a_0,
    u_s=A^s u,
    a_(s+1)=bit_1(u_s) XOR (bit_0(u_s) OR a_s).       (2)

Then the period doubling in (1) forces, exactly,

    bit_0(u_s)=0 for every s,
    XOR_(s=0..7) bit_1(u_s)=1.                        (3)

Consequently the scalar return over eight steps is a toggle,

    a_(s+8)=1-a_s,                                    (4)

and if `c=Theta(x_j)` is the complete temporal code at this distinguished doubling layer, then

    c_(s+8) = c_s XOR 1                               (5)

for every integer phase `s` (where XOR 1 toggles only the low bit of the symbol in `{0,1,2,3}`).

Thus every finite exact-period-16 core contains a canonical spatial layer whose 16-letter temporal word has the anti-periodic form

    c = q (q XOR 1)

for an 8-letter word `q`.

## 2. Proof

Projection by one low spatial bit commutes with `A`, so each `x_(j+1)` is periodic and its exact period divides that of `x_j`. The one-bit lifting theorem sharpens the quotient to

    per(x_j) in { per(x_(j+1)), 2 per(x_(j+1)) }.

Starting at exact period 16 and projecting until zero therefore forces a first drop `16 -> 8`; this is (1).

At that lift the parent cycle cannot contain a reset row `bit_0(u_s)=1`, because a reset makes the periodic lift unique with the SAME exact period as the parent. Hence the parent low trace is identically zero. In the no-reset case the eight-step fiber return is

    a -> a XOR S,
    S = XOR_(s=0..7) bit_1(u_s).

The child has exact period 16 rather than 8, so `S=1`. This proves (3), and applying the same eight-step return starting at any phase proves (4).

Finally

    Theta(x_j)_s = bit_0(A^s x_j) + 2 bit_1(A^s x_j)
                 = a_s + 2 bit_0(u_s)
                 = a_s,

because the parent low trace is zero. Therefore at the doubling layer the temporal code actually uses only symbols 0 and 1, and (4) gives (5). In particular the stronger form is

    c_s in {0,1},   c_(s+8)=1-c_s.                   (6)

## 3. Consequence for the K=3 exit problem

The current K=3 exit core itself has temporal prefix `2221`, so it CANNOT be the distinguished `16 -> 8` doubling layer: (6) contains no symbol 2 or3. Therefore every period-16 K=3 exit core lies at least one one-bit lift BELOW the canonical doubling layer (toward the physical low-bit end).

More precisely, if `x=x_0` is such an exit core and `j` is defined by (1), then

    j >= 1.                                           (7)

All lifts

    x_j -> x_(j-1) -> ... -> x_0

preserve exact period 16. Each is therefore one of the two period-preserving branches classified by the one-bit theorem:

1. a resetting parent, giving one unique recurrent lift; or
2. a nonresetting parent with even fiber parity, giving two period-16 lifts.

No further period doubling is possible along this chain.

This changes the period-16 target from an unconstrained `4^16` temporal-word census into a spatial lift-chain problem: start from an anti-periodic `{0,1}` doubling layer and ask whether any finite sequence of period-preserving one-bit lifts can first reach a complete code with the K=3 exit constraints

    b_0 b_1 b_2 b_3 = 2221

plus the backward exit phase and the six-step FULL repair/source-transport conditions.

The reduction is exact and all-depth; it does not assume uniqueness of finite `A` cycles at a given bitlength and does not use the empirical threshold `401`.

## 4. Useful next target

Derive the induced transformation on complete temporal words for ONE period-preserving low-bit lift and invert it from the required exit prefix `2221`. Because the doubling-layer alphabet is only `{0,1}` and anti-periodic after eight phases, backward propagation of the exit constraints may force a bounded minimum number of lift layers or an impossible reset/parity pattern. This is preferable to enumerating arbitrary period-16 words.

Dependency: `proofs/informal/problem1_one_bit_extension_cycle_lifting_theorem.md`.
