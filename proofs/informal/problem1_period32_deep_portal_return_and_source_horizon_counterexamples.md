# Problem 1: deep period-32 finite-portal certificates

Status: exact finite certificates. The previously preferred finite-portal `+42` source-horizon conjecture is false, and one genuine period-32 portal component is now completely classified as a singleton terminal leaf. Problem 1 remains OPEN.

## 1. The finite-portal +42 conjecture is false

`problem1_finite_lift_zero_return_existence.md` audited all sixteen genuine period-32 portal connectors through ten million period-preserving lifts. Every K=3 exit occurrence in that range failed the pushed source automaton by physical offset +42 or earlier.

That numerical ceiling does not persist deeper on the genuine finite domain.

Using the same exact period-32 child recurrence and the same source automaton, the following genuine finite-portal exit occurrences are exact certificates:

| portal | period-16 parent leaf | lift depth | phase | first source failure |
| ---: | --- | ---: | ---: | ---: |
| 0 | `0000010101000101` | 20,274,660 | 7 | +44 |
| 1 | `0011101111101011` | 24,780,812 | 13 | +50 |
| 3 | `0001010011100101` | 54,261,234 | 5 | +52 |
| 5 | `0000100100100101` | 24,689,363 | 18 | +52 |

Their phase-normalized complete temporal drivers are respectively

    22212110133330210332200210123202
    22211331222013202222130300102223
    22211211321100012231222211000103
    22211221332003333211223311223203

Each state is reached by deterministic period-preserving lifts from one of the sixteen genuine finite portals, so these are not unrestricted 2-adic countermodels.

Therefore:

> There is no universal `+42` contradiction bound even on genuine finite period-32 portal connectors.

A scan of every genuine portal through depth 100,000,000 found observed per-portal maxima

    0:44, 1:50, 2:42, 3:52,
    4:40, 5:52, 6:48, 7:46,
    8:48, 9:48, 10:42, 11:44,
    12:46, 13:42-before-return, 14:50, 15:48.

This is finite evidence only; +52 is not claimed as a theorem or final ceiling.

## 2. First explicit period-32 zero return in the genuine portal campaign

Portal 13 starts from the period-16 terminating leaf

    0001001111001111.

Its exact period-32 boundary lift remains unique and nonzero through lift depth

    65,154,359.

At lift depth

    65,154,360

the low temporal plane is exactly zero. The high temporal plane is

    11001111000010000000100110110100,

whose lexicographically minimal cyclic rotation is

    00000001001101101001100111100001.                 (1)

The word in (1) has

- Hamming weight 13;
- odd XOR parity;
- exact rotational period 32.

At a zero low plane with odd high-plane parity, the one-bit lift classifier gives no period-32 child: the next periodic lift must double period. Equivalently, in the period-32 zero-return graph the target (1) is a terminal odd full-period leaf.

Because this is the FIRST zero low-plane event on the deterministic connector launched from portal 13, the full-period component attached to the repeated period-16 leaf `0001001111001111` consists of exactly this one terminal vertex. In the notation of the leaf-portal theorem,

    B(0001001111001111) = 0.

So one of the sixteen new period-32 portal trees is now classified completely.

## 3. Consequences

Two previously plausible continuations are now fenced off.

1. Do not seek a finite-ancestry theorem forcing every period-32 K=3 exit to fail by +42. Exact finite counterexamples reach +52.
2. Do not assume every period-32 portal component contains a nontrivial binary full-period subtree. Portal 13 enters a terminal odd leaf immediately at its first zero return.

The p=32 program should instead exploit the zero-return/tree structure directly. The most concrete new target is to determine which of the remaining fifteen period-16 leaves have singleton period-32 portal components and, for non-singleton components, classify the first returned even target before attempting any source-horizon theorem.

## 4. Reproduction

Fast exact checker:

`experiments/problem1_nonperiodicity/check_period32_deep_portal_certificates.cpp`.

It reconstructs the four source certificates directly from their genuine portal starts and independently advances portal 13 from its boundary state to its first zero return, verifying depth, returned necklace, parity, exact period, and absence of a period-32 child.

Atomic record:

`results/problem1/20260929_period32_deep_portal_certificates.json`.
