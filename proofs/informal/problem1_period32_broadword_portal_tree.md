# Problem 1: broadword recurrent-child transducer and partial p=32 portal tree

Status: exact bit-parallel transducer plus exact first-return certificates in the genuine period-32 zero-return graph. Problem 1 remains OPEN.

## 1. Affine form of the recurrent child equation

For parent low/high temporal planes `b,c` and child low plane `a`,

    a_(s+1) = c_s XOR (b_s OR a_s).

Over GF(2), write

    m_s = 1 XOR b_s,
    d_s = b_s XOR c_s.

Then each temporal phase is the affine one-bit map

    a_(s+1) = d_s XOR m_s a_s.                       (1)

Represent an affine map by the pair `(m,d)`. Composition is

    (m2,d2) o (m1,d1)
      = (m2 m1, d2 XOR m2 d1).                       (2)

The previous run proved that, when `b != 0`, the recurrent seed `a_0` is fixed exactly by the last reset phase.

## 2. Exact broadword prefix scan

Equation (2) permits all 32 temporal prefix maps to be computed simultaneously.

Initialize 32-bit words

    D = c XOR b,
    M = NOT b.

For block sizes

    k = 1,2,4,8,16,

perform one Hillis-Steele affine-prefix doubling step. If `L_k=2^k-1` is the mask of the first `k` lanes, then with old values `D0,M0`,

    D <- D0 XOR (M0 AND (D0 << k)),                  (3)

    M <- (M0 AND L_k)
         OR
         (M0 AND (M0 << k) AND NOT L_k).             (4)

After the five stages, bit `i` of `(M,D)` is the composed affine map of phases `0,...,i`.

Let `A0` be either all-zero or all-one according to the recurrent seed bit `a_0`. Then

    Y = D XOR (M AND A0)                              (5)

has

    Y_i = a_(i+1).

Therefore the entire period-32 child word is

    boxed: child = (Y << 1) OR a_0.                  (6)

The overflow bit is `a_32=a_0` and is discarded automatically.

This is algebraically identical to the cyclic response recurrence; it is not an approximation or a vectorized sample. It replaces per-phase iteration / repeated byte-table response solving by five broadword affine-prefix stages.

A deterministic million-pair period-32 comparison against the scalar recurrence found no mismatch. The previous exhaustive last-reset checker already covers the recurrent seed independently.

## 3. Four more genuine portal roots now resolved

Using (6), the genuine p32 connectors were extended beyond the previous one-billion bound.

The following first zero returns are exact.

| portal | p16 parent leaf | first zero depth | returned target parity | exact period |
|---:|---|---:|---:|---:|
| 0 | `0000010101000101` | 1,420,791,101 | even | 32 |
| 2 | `0101101101111011` | 1,555,560,444 | odd | 32 |
| 6 | `0000001001011001` | 1,255,920,142 | even | 32 |
| 7 | `0010111001100111` | 1,324,488,168 | odd | 32 |

Canonical returned necklaces:

    portal 0:
    00011101011011010111110100111011   weight 20

    portal 2:
    00001000111100010010101100101111   weight 15

    portal 6:
    00011010101101110011001100111101   weight 18

    portal 7:
    00001000100010100100010010011101   weight 11

Hence portals 2 and 7 join portals 5 and 13 as completely classified singleton terminal components:

    B(0101101101111011)=0,
    B(0010111001100111)=0.

Portals 0 and 6 return first to even primitive targets, so their new full-period components genuinely branch.

## 4. Explicit nontrivial tree under portal 0

Write `E` for even/internal and `O` for odd/terminal.

The portal-0 first return is

    E0 = 00011101011011010111110100111011.            (7)

Its two derivative integrations lead to first-return children

    O1 = 00010011011011100111010001001111
         connector depth 687,106,285,

    E1 = 00011100101001101010100011111001
         connector depth 1,919,529,090.               (8)

Following one child of `E1` gives another even target

    E2 = 00001111001000101101001010001101
         connector depth 1,649,036,947.               (9)

Thus the portal-0 full-period tree contains at least

    B_0 >= 3

even internal vertices.

## 5. Explicit nontrivial tree under portal 6

The portal-6 root is

    F0 = 00011010101101110011001100111101.            (10)

One derivative integration returns to

    F1 = 00000110011100101010000110101101
         connector depth 580,240,392,                  (11)

which is even.

A child of `F1` returns to

    F2 = 00101010111101001010110011110101
         connector depth 991,084,817,                  (12)

also even.

The two children already resolved from `F2` are

    O2 = 00001010001110101001011110111101
         connector depth 610,754,117,

    F3 = 00001111001001111101011101011111
         connector depth 958,678,924.                  (13)

Here `O2` is odd/terminal and `F3` is even/internal.

One child of `F3` returns to

    F4 = 00001100100011010001100110111001
         connector depth 575,834,567,                  (14)

again even.

Therefore the portal-6 component already contains at least

    B_6 >= 5

even internal vertices.

All displayed targets have exact rotational period 32. By the established primitive-parity branching theorem, every displayed even target is a genuine binary internal vertex.

## 6. New exact lower bound on the number of terminating p32 necklaces

The dyadic leaf-portal theorem gives

    L_32 = L_16 + sum_(l in Leaves(G_16)) B(l).

The complete p16 census established

    L_16 = 16.

The exact p32 certificates above give

    B(portal 0) >= 3,
    B(portal 6) >= 5,

while every other portal contributes a nonnegative number of internal vertices.

Hence

    boxed: L_32 >= 16 + 3 + 5 = 24.                  (15)

Equivalently, portal 0 alone must eventually contain at least four terminal p32 leaves and portal 6 at least six, regardless of the still-unresolved descendants.

This is the first exact p32 leaf-count improvement beyond the trivial one-leaf-per-portal lower bound.

## 7. Research consequence

The p32 sector is now known to contain both qualitative portal types:

- singleton components, already proved for portals 2, 5, 7, and 13;
- genuinely branching components, proved for portals 0 and 6.

So no theorem saying all doubled p16 leaves behave uniformly can be correct.

The broadword affine scan makes deeper exact graph construction much cheaper, but brute-force completion can still require enormous connector lengths. The structural next target is to renormalize the affine monoid (2) over half-period blocks or multiple spatial lifts, so that first-return parity / branching can be predicted without linearly traversing every connector state.

Reproducer:

`experiments/problem1_nonperiodicity/check_period32_broadword_portal_tree.cpp`.

Atomic record:

`results/problem1/20260929_period32_broadword_portal_tree.json`.

Dependencies:
`problem1_last_reset_child_and_endpoint_parity_complexity.md`;
`problem1_dyadic_graph_embedding_and_leaf_portal_theorem.md`;
`problem1_portal_tree_leaf_balance.md`.
