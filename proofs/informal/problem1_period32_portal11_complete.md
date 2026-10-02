# Problem 1: complete period-32 portal-11 component

Status: exact complete full-period portal component at period 32. Problem 1 remains OPEN.

## 1. Portal entry

Portal 11 comes from the terminating period-16 leaf

    0101111111011111

of Hamming weight 13.

Its doubled-period portal connector first returns after

    2,846,542,716

lifts to the even exact-period-32 target

    00010010001101100011011100101001

(the reproducer uses the raw phase representative `01001000110110001101110010100100`).

Therefore this portal genuinely enters a binary full-period p32 component.

## 2. Complete edge ledger

Every internal target below is even and every leaf target is odd. Every returned
target has exact rotational period 32. The path is the derivative-integration
choice word from the full-period root; the root itself has empty path.

| child path | integration | first zero depth | canonical target | parity | weight |
|---|---:|---:|---|---|---:|
| `0` | 0 | 3,122,858,413 | `00000001101100110000101011000001` | odd | 11 |
| `1` | 1 | 1,990,824,624 | `00010100101111111101110011100111` | even | 20 |
| `10` | 0 | 1,022,338,055 | `00000100110100000111011001111101` | odd | 15 |
| `11` | 1 | 1,337,460,335 | `00000000000100101011100010110001` | even | 10 |
| `110` | 0 | 539,640,101 | `00010100111011011000110100010111` | even | 16 |
| `111` | 1 | 6,765,909,665 | `00000111111011100010110001111011` | even | 18 |
| `1100` | 0 | 2,369,294,537 | `00001000011011011101010001011001` | even | 14 |
| `1101` | 1 | 255,992,085 | `00001100111011101000011011101111` | even | 18 |
| `11010` | 0 | 917,411,703 | `00101101111111111001111010011111` | odd | 23 |
| `11011` | 1 | 6,298,685,676 | `00001011010011110011100110110101` | odd | 17 |
| `11000` | 0 | 620,392,484 | `00000000110111110111010101111101` | even | 18 |
| `11001` | 1 | 1,147,356,616 | `00000000001011000001010101011101` | odd | 11 |
| `110000` | 0 | 201,439,386 | `00000000010011100000011101100011` | odd | 11 |
| `110001` | 1 | 454,421,730 | `00000000110100010011010101000011` | odd | 11 |
| `1110` | 0 | 1,429,186,925 | `00011110010111001001101111001111` | odd | 19 |
| `1111` | 1 | 10,313,972,740 | `00000100000111110100010011110011` | even | 14 |
| `11110` | 0 | 3,872,621,716 | `00001011100100101110011111000101` | even | 16 |
| `11111` | 1 | 2,951,840,447 | `00010100011000101101011111111111` | odd | 19 |
| `111100` | 0 | 5,364,443,153 | `00000000111000010111100010100111` | odd | 13 |
| `111101` | 1 | 785,466,342 | `00010011110101111010101001011011` | even | 18 |
| `1111010` | 0 | 4,406,394,223 | `00001110010011001011100111000111` | even | 16 |
| `1111011` | 1 | 317,183,221 | `00000011010111111100111111001001` | even | 18 |
| `11110100` | 0 | 677,140,366 | `00001001100001101100111000110001` | odd | 13 |
| `11110101` | 1 | 4,702,237,002 | `00001001100001101011010100111011` | odd | 15 |
| `11110110` | 0 | 116,187,861 | `00011010111110111100111111001101` | odd | 21 |
| `11110111` | 1 | 2,168,338,618 | `00001110111011011011111011111101` | even | 22 |
| `111101110` | 0 | 9,483,082,542 | `00001011000100010100010010101111` | odd | 13 |
| `111101111` | 1 | 1,166,528,144 | `00010001111001011000101011011011` | even | 16 |
| `1111011110` | 0 | 12,479,646,968 | `00000101011100001010101101011101` | odd | 15 |
| `1111011111` | 1 | 839,208,297 | `00001001001001000101011010111101` | even | 14 |
| `11110111110` | 0 | 4,698,029,932 | `00000010110011100100100101001111` | even | 14 |
| `11110111111` | 1 | 80,005,764 | `00101010111100111101010111011111` | odd | 21 |
| `111101111100` | 0 | 4,773,510,433 | `00000000111100001000010010110011` | odd | 11 |
| `111101111101` | 1 | 10,268,483,482 | `00001001010101101011111101001101` | odd | 17 |

There are exactly 34 child edges. All 34 returned canonical targets are
distinct.

## 3. Exact tree topology

The full-period component contains exactly

    E = 17 even internal vertices
    O = 18 odd terminal leaves.

Hence

    B(portal 11) = 17

exactly. The full-binary-tree identity is satisfied:

    O = E + 1 = 18.

The maximum graph depth from the full-period root to a leaf is 12. The exact
leaf-depth distribution is

    depth 1: 1 leaf
    depth 2: 1 leaf
    depth 4: 1 leaf
    depth 5: 4 leafves
    depth 6: 3 leafves
    depth 8: 3 leafves
    depth 9: 1 leaf
    depth 10: 1 leaf
    depth 11: 1 leaf
    depth 12: 2 leafves

and its Kraft sum is exactly one.

The 34 deterministic connectors inside this one component traverse a total of

    107,937,533,586

exact lift steps. The deepest single child connector is

    12,479,646,968

lifts.

This illustrates again that enormous connector lengths can coexist with a
small exact zero-return tree.

## 4. Improved p32 leaf lower bound

Combining this exact component with the previously certified p32 bounds gives

    B(0)  >= 3
    B(1)  >= 1
    B(4)  >= 2
    B(6)  >= 5
    B(8)  >= 7
    B(10)  = 3
    B(11)  = 17
    B(12) >= 1.

Thus

    sum_l B(l) >= 39.

Since L_16=16 and the dyadic portal theorem gives

    L_32 = 16 + sum_l B(l),

we obtain the rigorous bound

    boxed: L_32 >= 55.

This is still a lower bound because portals 0,1,4,6,8,12 are not completely
classified.

## 5. Two resource-counting no-gos

The old leaf for portal 11 has Hamming weight 13, but its new p32 component has

    B = 17.

Therefore the following two possible charging rules are false:

    B(l) <= weight(l),
    B(l) <= p  with p=16.

In particular, one cannot inject every new full-period internal vertex into
either a 1-bit of the old leaf or merely one of its 16 temporal phases.

This does not refute a bound in terms of the original finite survivor's support
width; that resource can be much larger. It only removes two natural but too
small portal-local budgets.

## 6. Relation to the multilift phase quotient

The new all-depth finite-stack quotient in
`problem1_portal_multilift_phase_quotient.md` shows why a shallow observer
can erase proof-relevant driver labels. This complete portal-11 tree is now a
larger exact test fixture for any proposed extension/observer law:

- 17 internal vertices;
- both comb-like stretches and genuine two-even-child forks;
- connector lengths from 80,005,764 up to 12,479,646,968;
- 18 terminal endpoint parities known exactly.

A candidate bounded observer should reproduce this entire finite tree before it
is trusted as an all-scale invariant.

## 7. Reproduction

Checker:

    experiments/problem1_nonperiodicity/check_period32_portal11_complete.cpp

Verify one edge by child path, for example

    ./check_period32_portal11_complete 1111011110

or run the heavy complete ledger with

    ./check_period32_portal11_complete --all

The same binary also supports resumable exact connector scans:

    ./check_period32_portal11_complete --resume START_DEPTH A_HEX B_HEX CAP

Atomic record:

    results/problem1/20261002_period32_portal11_complete.json

Dependencies:

    problem1_period32_complete_portal_root_census.md
    problem1_twisted_half_period_portal_and_p32_descendants.md
    problem1_portal_multilift_phase_quotient.md
