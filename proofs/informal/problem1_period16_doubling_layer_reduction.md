# Problem 1: canonical doubling layer inside every finite period-16 core

Status: exact structural reduction; Problem 1 remains OPEN.

## 1. Canonical doubling layer

Let `x>0` be a finite `A`-periodic state of exact period 16 and put `x_j=x>>j`. Projection commutes with `A`, and the exact one-bit lifting theorem says a lift preserves or doubles exact period. Since sufficiently deep projections are zero, there is a largest `j` with

    per(x_j)=16,   per(x_(j+1))=8.                    (1)

Write `u=x_(j+1)` and `x_j=2u+a_0`. At (1), the parent cannot contain a reset row `bit_0(A^s u)=1`, since a resetting lift preserves the parent's period. Hence

    bit_0(A^s u)=0 for every s,
    XOR_(s=0..7) bit_1(A^s u)=1.                     (2)

The exposed lift bit therefore toggles after one parent period,

    a_(s+8)=1-a_s.                                    (3)

For `c=Theta(x_j)`, the parent low trace in (2) vanishes, so

    c_s=a_s in {0,1},
    c_(s+8)=1-c_s.                                    (4)

Thus every finite exact-period-16 core contains a canonical spatial layer whose complete temporal word is an anti-periodic binary word `q (1-q)`.

## 2. Exact temporal rule for one low-bit lift

If a parent periodic state has complete temporal word `e_s=Theta(u)_s` and a periodic child is `w=2u+a_0`, then its complete word `d=Theta(w)` is

    d_s = a_s + 2 (e_s mod 2),                        (5)
    a_(s+1) = floor(e_s/2) XOR ((e_s mod2) OR a_s).   (6)

Equations (5)-(6) can be inverted symbolically from any prescribed child prefix. This is only the one-bit theorem written in temporal coordinates; no finite-state census is involved.

## 3. Inverting the K=3 exit prefix

At a K=3 exit the child word begins

    d_0 d_1 d_2 d_3 = 2 2 2 1.                       (7)

Apply (5)-(6) one spatial projection at a time.

### First projection

From `d_0=d_1=d_2=2`, the exposed bits are `a_0=a_1=a_2=0` while the parent low bits are all 1. Equation (6) then forces

    e_0=e_1=3,
    e_2=1.

Since `d_3=1`, the parent low bit at phase 3 is zero. Hence

    Theta(x>>1)[0:4] = 3 3 1 q,   q in {0,2}.         (8)

### Second projection

Invert either word in (8). In both cases (5)-(6) force

    Theta(x>>2)[0:3] = 1 1 2.                         (9)

The fourth symbol is unrestricted after the two possibilities in (8) are combined:

    Theta(x>>2)[0:4] = 1 1 2 q,   q in {0,1,2,3}.     (10)

### Third projection

Inverting (10) forces

    Theta(x>>3)[0:2] = 0 2,                           (11)

and the third symbol is 1 or3 (the fourth remains phase-dependent). In particular this layer still contains a symbol 2.

### Fourth projection

One further inversion forces only

    Theta(x>>4)[0:2] = 0 1.                           (12)

At this depth binary words become possible; all four values can occur in later unconstrained prefix positions under the local inversion.

Because the canonical doubling layer (4) is binary, (8), (9), and (11) prove the stronger bound

    j >= 4.                                           (13)

So a period-16 K=3 exit core cannot occur at, one lift below, two lifts below, or three lifts below its unique `16 -> 8` period-doubling layer. It requires at least FOUR subsequent period-preserving one-bit lifts.

This is a genuine restriction on any period-16 exit core and does not assume uniqueness of finite cycles or the empirical bitlength threshold 401.

## 4. Remaining period-16 target

All lifts from the canonical layer `x_j` down to the exit core `x_0` preserve exact period 16. Each is therefore either a resetting unique lift or a nonresetting even-parity period-preserving lift. The local exit prefix alone permits first contact with a binary ancestor at depth four, so prefix inversion by itself does not exclude period 16.

The next useful computation/theorem should combine the FULL 16-phase conditions with this exact lift chain: impose the backward exit-phase condition and six-step repair/source transport on `x_0`, propagate the FULL 16-letter word upward by (5)-(6), and require that the first `16 -> 8` layer satisfy the anti-periodic binary condition (4). This searches lift depth/phase structure rather than arbitrary `4^16` words.

Dependency: `proofs/informal/problem1_one_bit_extension_cycle_lifting_theorem.md`.
