# Problem 1: twisted half-period portal renormalization and deeper p32 trees

Status: exact half-period conjugacy plus exact descendant certificates. Problem 1 remains OPEN.

## 1. Twisted half-period representation

For a binary temporal word z of length 2p define

    H(z)_s = (z_s,z_(s+p)),  0 <= s < p.

If a is the recurrent child of parent low/high planes b,c,

    a_(s+1) = c_s XOR (b_s OR a_s),

then with A=H(a), B=H(b), C=H(c), for phases s=0,...,p-1,

    A_(s+1) = C_s XOR (B_s OR A_s)

componentwise, with the twisted closure

    A_p = swap(A_0).

The swap is essential: advancing p phases in a 2p-cycle exchanges the two
halves. Thus period 2p is represented exactly as a p-phase four-symbol system
on a Möbius/twisted boundary, not as an ordinary p-period product system.

This is an exact conjugacy retaining all 2p bits. Proper p-period words are
exactly the all-diagonal pair words (00/11); antiperiodic words are exactly
the all-off-diagonal pair words (01/10).

## 2. Portal third-lift automaton collapses to two bits

Use the previously proved two-lift portal normal form

    (x,1^(2p))

with x antiperiodic. Write

    H(x)_s = (q_s,1 XOR q_s).

Let u be the next child and write

    H(u)_s = (U_s,U_s XOR D_s).

The paired recurrence gives exactly

    U_(s+1) = 1 XOR (q_s OR U_s),
    D_(s+1) = 1 XOR U_s XOR q_s D_s,

with twisted closure

    D_p = D_0,
    U_p = U_0 XOR D_0.

For one q-symbol the two state maps are

    q=0: (U,D) -> (1 XOR U, 1 XOR U),
    q=1: (U,D) -> (0, 1 XOR U XOR D).

Hence the two-symbol compositions synchronize:

    01 -> (0,1) independently of the incoming state,
    10 -> (1,1) independently of the incoming state.

For a doubled odd portal, q is the prefix-parity word of the lower-period odd
leaf, so q changes somewhere around the cycle. The third-lift paired state is
therefore anchored by a genuine reset at a q-change rather than by an
arbitrary cyclic seed.

A further exact consequence is that (U,D)=(1,0) can never occur on the
recurrent cycle: neither one-symbol map has that state in its image. Since
(1,0) is exactly the paired symbol 11, the third lift satisfies

    H(u)_s in {00,01,10} for every phase s.

Thus the first post-normalization lift lies in a strict three-symbol sector.
The companion checker verifies the twisted recurrence exhaustively for all
parent pairs through p=4 and verifies the portal three-symbol theorem on all
1,023 odd lower words for p=1,...,10.

This does not yet close under later lifts: the next child can reintroduce 11.
The useful new object is therefore the twisted four-symbol system together
with the synchronized three-symbol third-lift slice, not a claimed invariant
subshift.

## 3. Exact p32 descendant expansion

Using the exact broadword period-32 child map, the following first-return
certificates were obtained from even full-period targets. Every displayed
returned target has exact rotational period 32.

| connector | integration | first zero depth | canonical returned target | parity | weight |
|---|---:|---:|---|---|---:|
| `p1-c0` | 0 | 2,385,564,355 | `00001111100110011101101011001111` | odd | 19 |
| `p4-c0` | 0 | 404,356,749 | `00000100011001010100010011100001` | odd | 11 |
| `p4-c1` | 1 | 203,191,865 | `00000101010111001010001101101111` | even | 16 |
| `p4-c1-c1` | 1 | 207,230,746 | `00000000101110100100110010110101` | odd | 13 |
| `p8-c0` | 0 | 3,311,656,131 | `00000101010101001011111100011001` | odd | 15 |
| `p8-c1` | 1 | 2,912,141,700 | `00000110100100110111001000010001` | even | 12 |
| `p8-c1-c0` | 0 | 1,984,702,874 | `00010001101100011000110101001011` | even | 14 |
| `p8-c1-c1` | 1 | 3,320,394,584 | `00001100010110101000011011110001` | even | 14 |
| `p8-c1-c0-c0` | 0 | 2,119,222,437 | `00011101110011101101101110111001` | even | 20 |
| `p8-c1-c0-c1` | 1 | 1,888,558,713 | `00011101110101100101011101010101` | even | 18 |
| `p8-c1-c1-c0` | 0 | 386,045,218 | `00000110100110110010011011110111` | odd | 17 |
| `p8-c1-c1-c1` | 1 | 100,726,797 | `00001011000100010110011000110001` | even | 12 |
| `p10-c0` | 0 | 2,214,214,662 | `00000100010010011011000111110011` | even | 14 |
| `p10-c1` | 1 | 1,558,425,976 | `00001110010111011111011000111011` | odd | 19 |
| `p10-c0-c0` | 0 | 39,916,667 | `00011010100101011011111110110011` | odd | 19 |
| `p10-c0-c1` | 1 | 318,427,669 | `00000001011001101011000001110111` | even | 14 |
| `p10-c0-c1-c0` | 0 | 3,940,764,551 | `00001011000101000111100001011111` | odd | 15 |
| `p10-c0-c1-c1` | 1 | 229,417,894 | `00011111001010010110101101111101` | odd | 19 |
| `p11-c0` | 0 | 3,122,858,413 | `00000001101100110000101011000001` | odd | 11 |
| `p11-c1` | 1 | 1,990,824,624 | `00010100101111111101110011100111` | even | 20 |
| `p11-c1-c0` | 0 | 1,022,338,055 | `00000100110100000111011001111101` | odd | 15 |
| `p11-c1-c1` | 1 | 1,337,460,335 | `00000000000100101011100010110001` | even | 10 |
| `p11-c1-c1-c0` | 0 | 539,640,101 | `00010100111011011000110100010111` | even | 16 |
| `p11-c1-c1-c0-c1` | 1 | 255,992,085 | `00001100111011101000011011101111` | even | 18 |
| `p12-c0` | 0 | 91,485,337 | `00000101011111011100110100110101` | odd | 17 |

The most important structural certificate is under portal 8. Its root has an
odd child and an even child. That even child then has TWO even children:

    portal8-c1-c0  even,
    portal8-c1-c1  even.

Therefore a p32 full-period portal tree need not be a comb and there is no
rule saying every even internal vertex must have an odd terminal child.

## 4. Portal 10 is completely classified

Portal 10 has the exact finite tree

    root even
      choice 1 -> odd leaf
      choice 0 -> A even
          choice 0 -> odd leaf
          choice 1 -> B even
              choice 0 -> odd leaf
              choice 1 -> odd leaf.

Thus

    B(portal 10) = 3

exactly, and this component has four odd leaves, as required by the full
binary-tree identity O=E+1.

## 5. Improved rigorous leaf-count lower bound

Combining old and new exact certificates gives

    B(0)  >= 3
    B(1)  >= 1
    B(4)  >= 2
    B(6)  >= 5
    B(8)  >= 7
    B(10)  = 3
    B(11) >= 5
    B(12) >= 1.

All other p16 portals are singleton roots, so their B value is zero.

Therefore

    sum_l B(l) >= 27

and the dyadic leaf formula yields

    L_32 = 16 + sum_l B(l) >= 43.

This is a rigorous lower bound, not a completed p32 census.

## 6. Research consequence

Two simplistic routes are now ruled out by exact certificates:

1. one-lift half-block data do not predict root endpoint parity;
2. even p32 portal trees are not forced to have one terminal child at every
   internal vertex.

The promising structural object is the exact twisted half-period system. The
next proof-oriented target is to determine whether the synchronized
three-symbol third-lift slice induces a finite or contracting return
transducer after several spatial lifts, ideally one that controls the parity
of the first zero target without traversing billions of connector states.

Do not continue blind p32 tree expansion merely to raise L_32. Use the
descendant certificates as test cases for any proposed multi-lift quotient.

Reproducers:

    experiments/problem1_nonperiodicity/check_twisted_half_period_portal.py
    experiments/problem1_nonperiodicity/check_period32_descendant_expansion.cpp

Atomic record:

    results/problem1/20261002_twisted_half_period_and_p32_descendants.json
