# Problem 1 run 213 — exact period lift law for adjacent zero extensions

Problem 1 remains open.

## Setup

Use the reviewed scan map

    A(q) = (q >> 2) XOR ((q >> 1) OR q).

For a finite state q, let tau(q) be its eventual-cycle entry time and let pi(q) be the minimal eventual period.

Runs 207–209 proved that along the adjacent lift one has exactly

    A^k(2q) = 2 A^k(q) XOR d_k,    d_k in {0,1},

and, writing the two low bits of r_k=A^k(q) as (r0,r1), the defect update is

    00 : d -> d
    01 : d -> 1 XOR d
    10 : d -> 1
    11 : d -> 0.

The last two symbols are resets.

## Theorem: the eventual period can only stay the same or double

Let P=pi(q). Then

    pi(2q) in {P, 2P}.

In particular,

    pi(q) | pi(2q) | 2 pi(q).

### Proof

Projection gives

    floor(A^k(2q)/2) = A^k(q)

at every k. Therefore the minimal period P of the lower eventual cycle divides the minimal period P' of the lifted eventual cycle.

Once the lower orbit is on its P-cycle, the defect is a one-bit system driven by a P-periodic word. Compose its P successive update maps. Each individual update is one of

    identity, toggle, constant-1, constant-0.

Their composition M on {0,1} is therefore either a constant map, identity, or toggle. Hence every defect orbit under one full lower period has period at most 2. Consequently P' divides 2P.

Together P | P' | 2P, so P'=P or 2P. QED.

## Exact doubling criterion

The preceding argument can be sharpened completely.

If the lower P-cycle contains any state with low bit r0=1, then one of the P defect updates is a reset (10 or 11). The period monodromy M is then constant. Thus the defect has a unique P-periodic phase and

    pi(2q) = P.

Suppose instead r0=0 at every state of the lower P-cycle. Then the only defect maps are

    00 : identity,
    01 : toggle.

Let N01 be the number of cycle positions at which (r0,r1)=01. The P-step monodromy is toggle exactly when N01 is odd, and identity exactly when N01 is even. Therefore

    pi(2q) = 2P

iff BOTH

    (i) r0=0 at every point of the lower eventual cycle, and
    (ii) N01 is odd.

Otherwise pi(2q)=P.

This criterion is exact, not merely sufficient.

## Tower consequence

For q_n=2^n x and P_n=pi(q_n),

    P_n / P_(n-1) in {1,2}.

Hence every tower period has the form

    P_n = P_0 * 2^{e_n}

for a nondecreasing integer e_n whose increments are 0 or 1. A period doubling at level n can occur only when the entire eventual cycle at level n-1 has least-significant bit zero and the next bit is 1 an odd number of times around that cycle.

This is independent of the preperiod increment law from runs 208–210. It gives a second exact adjacent-level invariant: preperiod increments are reset-gap synchronization delays, while period increments are binary and have the explicit no-reset/parity criterion above.

## Check on the canonical x=1 tower

Direct exact orbit detection gives period changes

    n=0 : P=1
    n=3 : P=2
    n=8 : P=4
    n=29: P=8

and no further period change through n=150 in the bounded diagnostic. The theorem explains why only doublings occur. For example, the n=2 lower cycle (q=4) is [6], whose low pair is 10 in the conventional bit order (r1 r0), i.e. (r0,r1)=01: there is no reset and exactly one toggle, so the lift to n=3 doubles the period from 1 to 2.

The bounded computation is evidence only; the theorem itself is exact for every finite q.

## Strategic consequence

Run 212 proposed studying the n-bit period return map. The theorem above shows that one important part of that return map is already completely classified one fiber bit at a time: adding one zero-extension cannot create an arbitrary new cycle period. It either preserves the lower period or doubles it, and doubling is possible only across a lower cycle with no reset at all.

This does not yet bound the preperiod surplus a_n-n, so it does not settle FULL. The next useful target is to couple the two exact laws: determine whether long positive preperiod increments (which end at the first reset after a phase mismatch) constrain subsequent period doublings, or conversely whether a long run of no-reset cycles needed for period growth forces enough matched lifts to control the residence surplus. That is a concrete interaction not captured by either invariant separately.
