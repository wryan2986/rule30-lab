# Problem 1: blind-label extension law and observer delay

Status: exact local extension theorem, exact regular language for blind spatial
prefixes, and finite-exhaustive odd-necklace observer census through period 28.
Problem 1 remains OPEN.

## 1. Exact extension law at a blind edge

Use the normalized finite-stack portal quotient from
`problem1_portal_multilift_phase_quotient.md`.  A dynamic paired layer is

    (X_j,Y_j),

and the normalized driver transition is

    T_w = G^w Phi_0,

where

    G(X,Y)=(X XOR Y,Y).

Call an r-layer state R **blind** when

    T_0(R)=T_1(R).

Because G changes only the first coordinate of a pair and does so exactly when
its difference bit is one,

    boxed:
    R is blind iff every difference coordinate of Phi_0(R) is zero.

Now extend R by one deeper input pair

    (P,Q).

Let the final two old input pairs be

    (H,K), (L,M).

The deepest pair produced by Phi_0 is exactly

    P+ = H XOR (L OR P),

    Q+ = K XOR M XOR Q
         XOR L Q XOR M P XOR M Q.                 (1)

After the driver label w is applied, that deepest output pair is

    boxed:
    (P+ XOR w Q+, Q+).                             (2)

Therefore, when the r-layer projection is blind:

* if Q+=0, the current driver label remains erased after adding this layer;
* if Q+=1, the added layer records the hidden label in its first coordinate.

This is the general version of the portal-5/portal-6 sixth-lift memory channel.
It works at every stack depth.

## 2. Blindness itself is an eight-state spatial automaton

For blindness through layer j, only

    K=Y_(j-2), L=X_(j-1), M=Y_(j-1)

are needed.  Given the next input pair (X,Y), equation (1) says that blindness
continues exactly when

    K XOR M XOR Y XOR L Y XOR M X XOR M Y = 0.     (3)

The next context is simply

    (K,L,M) -> (M,X,Y).

Thus arbitrary-depth label erasure is a regular language with only eight
context states.  Encode a context by the three-bit word KLM.  The exact
transition table is

| KLM | allowed next pair -> next KLM |
|---|---|
| 000 | 00->000, 10->010 |
| 001 | 10->110, 11->111 |
| 010 | 00->000, 01->001, 10->010, 11->011 |
| 011 | 01->101, 10->110 |
| 100 | 01->001, 11->011 |
| 101 | 00->100, 01->101 |
| 110 | none |
| 111 | 00->100, 11->111 |

The portal boundary starts in context

    001.

Let b_r be the number of raw r-layer states that are blind.  The transfer
matrix of the table gives

    sum_(r>=0) b_r x^r = (1+x)/(1-x-2x^3),

so

    b_0=1, b_1=2, b_2=2,

and for every r>=3,

    boxed:
    b_r = b_(r-1) + 2 b_(r-3).                    (4)

The first values are

    1,2,2,4,8,12,20,36,60,100,172,...

The dominant growth factor is about 1.69562.

Most importantly, local algebra alone gives NO bounded recovery depth.  The
start context 001 accepts pair 11 and moves to context 111, and context 111
has an 11 self-loop.  Hence

    (11)^r

is a blind raw stack for every finite r.

So a proof cannot say that every erased driver bit must automatically
reappear within C deeper layers for a universal constant C.  Any bounded
recovery theorem has to use cyclic-driver / finite-core ancestry, not only the
local extension recurrence.

## 3. Complete odd-necklace observer census

The raw blind language overincludes the portal domain.  To measure how much
cyclic odd drivers restrict it, exhaust every rotation class of odd binary
words at each even period p and compute its complete unlabeled normalized
M_r orbit.

For each p below, the table gives the smallest r for which the unlabeled
r-layer state orbit is injective on ALL odd necklaces of that period.

| p | odd necklaces | first injective r |
|---:|---:|---:|
| 2 | 1 | 1 |
| 4 | 2 | 1 |
| 6 | 6 | 3 |
| 8 | 16 | 4 |
| 10 | 52 | 4 |
| 12 | 172 | 5 |
| 14 | 586 | 5 |
| 16 | 2,048 | 8 |
| 18 | 7,286 | 9 |
| 20 | 26,216 | 9 |
| 22 | 95,326 | 9 |
| 24 | 349,536 | 10 |
| 26 | 1,290,556 | 10 |
| 28 | 4,793,492 | 10 |

This is exact finite exhaustion, not a conjectured formula.

In particular:

* depth 8 is not universal: period 18 requires depth 9;
* depth 9 is not universal: period 24 requires depth 10;
* depth 10 happens to suffice through period 28, but no all-scale conclusion is
  claimed.

This sharply separates two facts:

1. the sixteen genuine p32 roots are already separated at r=4;
2. the ambient odd-driver language at the same and nearby scales can require
   substantially deeper observers.

The shallow p32 separation therefore uses real root-basin restrictions and is
not a generic property of odd drivers.

## 4. Explicit deep hidden-label certificates

### Period 18: hidden through r=8, visible at r=9

In checker orientation, the rotation-inequivalent odd words

    100111000011100000
    100111010011101000

have the same complete unlabeled M_8 state orbit.

After aligning that common orbit, their labels differ only at phases 6 and 17.
The corresponding 16-bit state codes are

    phase 6:  65507
    phase 17: 53219,

and both states are blind.

At M_9 the two state orbits are distinct.

### Period 24: hidden through r=9, visible at r=10

The odd necklaces represented by

    000100111010001001110101
    000001001110001000100111

have the same complete unlabeled M_9 orbit but different M_10 orbits.

After aligning their common M_9 orbit, both differing labels occur at the
same blind 18-bit state code

    118755.

The same blind state also supplies exact depth-9 collision certificates at
periods 26 and 28 in the companion computation.

These examples are direct realizations of (2): a driver label can be erased
for many projected layers and then become visible when a deeper successor
difference Q+ finally equals one.

## 5. What has and has not been solved

The recursive blind-label question is now local and exact:

    one hidden label + one new layer -> one bit Q+ decides
    whether the label remains erased or becomes visible.

And the set of arbitrarily deep raw erasure stacks is controlled by the
eight-state automaton (3), not by the exponentially growing full stack.

That is useful compression, but it does not solve Problem 1.  The regular
blind language contains arbitrarily long stacks, while actual cyclic odd
drivers eventually escape it in every finite census above.  What is still
missing is an all-depth reason that a genuine finite-core portal cannot follow
the blind language for too long without paying a finite-support resource.

The next proof-oriented target should therefore intersect the eight-state
blind automaton with finite portal/root-basin ancestry.  Concretely, seek a
charging rule for visits to the recurrent blind contexts, or prove that
finite-core ancestry forces a nonblind extension after a number of layers
controlled by the original finite support.  Do not assume a universal
constant observer depth.

Reproducer:

    experiments/problem1_nonperiodicity/analyze_blind_label_extension_delay.cpp

The full p<=28 census uses substantially more memory than the default p<=22
run; invoke it explicitly with

    ./analyze_blind_label_extension_delay --max-period 28 --max-r 10

Atomic record:

    results/problem1/20261002_blind_label_extension_delay.json

Dependencies:

    problem1_portal_multilift_phase_quotient.md
    problem1_genuine_portal_observer_depth.md
