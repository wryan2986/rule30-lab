# Problem 1: all-depth finite-stack phase quotient and blind-edge obstruction

Status: exact multilift renormalization for every finite stack depth, exact finite-state sectors, and a genuine p32 obstruction to shallow unlabeled quotients. Problem 1 remains OPEN.

## 1. Setup after the universal two-lift portal normalization

Let `w` be an odd-parity binary word of even length `p`. Its derivative lift
`x` has period `2p` and is antiperiodic. After the already-proved universal
two-lift normalization, work with the phase-equivalent ordered pair

    (x, J),   J = 1^(2p).

For any length-`2p` word `z`, pair its two halves by

    H(z)_s = (z_s,z_(s+p)).

Write a paired symbol as

    (X, X XOR Y),

so `X` is the first-half bit and `Y` is the half-difference bit.

For the normalized boundary layers,

    J : (1,0),
    x : (q_s,1),

where the antiperiodic prefix bit satisfies

    q_(s+1) = q_s XOR w_s,
    q_p = 1 XOR q_0.

Let subsequent spatial lifts have paired coordinates

    z_j : (X_j, X_j XOR Y_j),   j>=1.

## 2. Exact triangular update for an arbitrary finite spatial stack

For every dynamic layer `j>=1`, one temporal step gives

    X_j^+
      = X_(j-2) XOR (X_(j-1) OR X_j),

and

    Y_j^+
      = Y_(j-2) XOR Y_(j-1) XOR Y_j
        XOR X_(j-1) Y_j
        XOR Y_(j-1) X_j
        XOR Y_(j-1) Y_j.                         (1)

The boundary values are

    (X_-1,Y_-1)=(1,0),
    (X_0,Y_0)=(q,1).

Thus the first `r` post-normalization lifts form a `2r`-bit triangular
automaton.

Let `G` be simultaneous half-swap on every dynamic paired layer,

    G(X_j,Y_j) = (X_j XOR Y_j,Y_j).

The paired recurrence is equivariant under complementing the antiperiodic
prefix bit and applying `G`:

    G Phi_q = Phi_(1 XOR q) G.                    (2)

Define the phase-normalized stack state

    R_s = G^(q_s) (dynamic stack at phase s).

Using `w_s=q_s XOR q_(s+1)`, (2) gives the exact quotient recurrence

    boxed:
    R_(s+1) = G^(w_s) Phi_0(R_s).                 (3)

The twisted half-period boundary disappears completely. Since
`q_p=1 XOR q_0` while the raw paired stack itself half-swaps after `p`
phases,

    boxed: R_p = R_0.                             (4)

Therefore, for **every finite number of spatial lifts**, the doubled-period
portal is represented by an ordinary `p`-phase finite automaton driven
directly by the original lower-period leaf bits `w`.

This is the first exact multilift half-period renormalization in the branch.
It is not a fixed-size all-depth quotient: the raw `r)-layer state has
`2r` bits. The rest of this note measures how much of that state is actually
reachable on odd dyadic drivers.

## 3. Two dynamic layers collapse exactly to five states

For the third and fourth connector lifts write the normalized state as

    R=(U,D,V,E).

The exact even-length odd-weight recurrent sector is

    A=(0,0,1,0)
    B=(0,1,0,0)
    C=(0,1,0,1)
    D=(1,1,0,0)
    E=(1,1,1,1).

Driven directly by `w_s`, the transition table is

| state | w=0 | w=1 |
|---|---|---|
| A | E | C |
| B | D | B |
| C | D | B |
| D | A | A |
| E | A | A |

Every three-symbol word beginning with `1` synchronizes this automaton:

    100,101 -> A
    110     -> D
    111     -> B.

Every odd word contains a `1`, so its cyclic five-state orbit is unique.

### Exact parity coboundary

Define

    g(A)=g(B)=g(D)=0,
    g(C)=g(E)=1.

For every labeled transition `R_s -> R_(s+1)`,

    D_s XOR E_s
      = 1 XOR g(R_s) XOR g(R_(s+1)).              (5)

The parity of the third lift is `XOR_s D_s`; the parity of the fourth is
`XOR_s E_s`. Summing (5) around the cycle gives

    boxed:
    P(z_1) XOR P(z_2) = p mod 2.                  (6)

Hence at every dyadic scale with even `p`, the third and fourth
post-normalization lifts have exactly the same XOR parity.

## 4. Adding the fifth lift gives an exact 14-state sector

Retain one more paired layer,

    R=(U,D,V,E,W,F).

The raw state space has 64 elements. For even-length odd-weight cyclic drivers,
the exact recurrent sector has only

    14 states.

There are two equivalent exact certificates.

First, every word `1ab` sends the full 64-state space into the listed
14-state set, and the set is forward-invariant. Since every odd driver contains
a `1`, every recurrent portal orbit enters it.

Second, every one of the fourteen states has an explicit even-length,
odd-weight cyclic witness (all witnesses have length <=8), so the set is not
merely an upper bound.

Two states are **blind** to the current driver bit:

    (1,1,0,0,0,1),
    (1,1,0,0,1,1),

meaning

    T_0(R)=T_1(R).

The second blind state is the one that matters for the genuine portal
certificate below.

## 5. Genuine p32 collision: portals 5 and 6

The p16 leaf words

    portal 5: 0000100100100101
    portal 6: 0000001001011001

have opposite exact p32 root behavior:

    portal 5:
      first zero depth 105,696,243
      returned target odd
      singleton component;

    portal 6:
      first zero depth 1,255,920,142
      returned target even
      branching component.

Yet their complete normalized 14-state orbits through the fifth lift are
identical up to temporal rotation.

Encoding each 6-bit state little-endian as an integer, the common canonical
state cycle is

    [4,26,51,4,26,51,4,26,51,4,31,36,31,36,26,51].

After aligning to that same state cycle, the driver words are

    portal 5: 1001001010000100
    portal 6: 1011001000000100.

They differ only at two visits to state

    51 = (1,1,0,0,1,1),

and that state is blind:

    T_0(51)=T_1(51).

Thus:

    boxed:
    the complete unlabeled multilift orbit through the fifth connector lift
    does NOT determine singleton-versus-branching behavior,
    even on the sixteen genuine p32 portal roots.

Any successful shallow quotient must retain the driver labels at blind-state
visits, or carry enough deeper-layer state to transport those hidden labels.

## 6. Why the sixth lift separates the collision

Project the next (sixth-lift) paired coordinate as `(P,P XOR Q)`.

At the blind base state

    (U,D,V,E,W,F)=(1,1,0,0,1,1),

the admissible sixth-layer extensions seen in the exact sector have
`P=1`. A direct use of (1) shows that, before phase normalization, the next
deepest pair is

    (1,Q).

After applying the driver-dependent half-swap,

    boxed:
    (1,Q) -> (1 XOR w Q,Q).                        (7)

Therefore whenever `Q=1`, the sixth lift records the hidden blind-edge bit
as `1 XOR w`. This is exactly the memory channel missing from the 14-state
projection.

For portals 5 and 6 the relevant blind visits have `Q=1`, and their
sixth-lift state orbits are no longer equal.

This identifies a concrete mechanism rather than merely saying that a deeper
classifier is needed: deeper spatial layers transport driver information that
shallower layers can provably erase.

## 7. Exact state growth: the naive stack does not stabilize

For stack depth `r`, let `M_r` be the `2r`-bit quotient automaton (3).
A state is relevant to an even-period odd leaf iff it lies on a closed walk of

    even length,
    odd driver Hamming weight.

This can be decided without imposing any finite period cap. Lift the state
graph by two parity bits: driver-weight parity and path-length parity. A state
`s` is relevant exactly when

    (s,0,0) and (s,1,0)

belong to the same strongly connected component.

The exact sector sizes are

| dynamic layers r | raw states 4^r | exact even-length/odd-weight sector |
|---:|---:|---:|
| 1 | 4 | 3 |
| 2 | 16 | 5 |
| 3 | 64 | 14 |
| 4 | 256 | 30 |
| 5 | 1,024 | 75 |
| 6 | 4,096 | 195 |
| 7 | 16,384 | 443 |
| 8 | 65,536 | 1,168 |

So the simplest hope that the exact multilift state stabilizes at five or
fourteen states is false. The quotient is dramatically smaller than the raw
stack, but its exact relevant sector continues growing through eight layers.

### Explicit observer collisions at every tested deeper depth

For each `r=4,...,8`, the following two rotation-inequivalent even-length,
odd-weight drivers have the **same unlabeled cyclic `M_r` state orbit**:

| r | period | driver A | driver B |
|---:|---:|---|---|
| 4 | 16 | `1001110011100101` | `1001110111101101` |
| 5 | 18 | `111000011100100101` | `111010011101100101` |
| 6 | 20 | `00111000011101101101` | `00111010011100101101` |
| 7 | 24 | `010011100101111010100101` | `010011101101111000100101` |
| 8 | 26 | `01011011110000111000100101` | `01011011110100111010100101` |

These are exact finite-state certificates, not sampled collisions. They show
that increasing the unlabeled observer depth from four through eight does not
make it globally injective on odd drivers.

This does **not** prove that no bounded-depth labeled quotient can decide the
Rule-30 endpoint. It specifically rules out treating the unlabeled stack orbit
as a complete encoding of the old leaf.

## 8. Exact zero-return criterion in the projective quotient

The quotient also gives a clean all-depth formulation of the portal return.

For spatial layer `j`, its length-`2p` temporal word is zero iff its paired
coordinates satisfy

    (X_j(s),Y_j(s))=(0,0)

for every temporal phase `s` in the normalized `p`-cycle.

Therefore the first zero return is exactly

    the first spatial layer j whose pair-track is identically 00.

If that first zero layer is `j`, the returned high target is layer `j-1`,
whose XOR parity is

    boxed:
    XOR_s Y_(j-1)(s).                               (8)

So the p->2p portal-root problem is now exactly:

1. run the projective multilift automaton (3);
2. locate the first all-00 spatial track;
3. read the parity of the preceding difference track.

No information is lost in this reformulation.

## 9. Research consequence

The half-period program has now reached an exact all-depth finite-stack
renormalization. The remaining obstruction is not the old twisted boundary;
that has been removed.

The new bottleneck is the **projective extension tower**

    M_1 <- M_2 <- M_3 <- ...

and, specifically, how blind driver labels are transported into deeper paired
coordinates.

The portal-5/portal-6 certificate says this hidden-label transport is
proof-relevant: two genuine roots are indistinguishable through five connector
lifts and separate only when the next layer carries the lost bit.

The preferred next target is therefore:

> derive a recursive observer/extension law for blind edges, and determine
> whether the first all-00 track can be bounded or its preceding parity
> computed without constructing an unbounded spatial stack.

Do not return to static leaf polynomials or unlabeled shallow-orbit
classifiers. Both have exact counterexamples.

Reproducer:

    experiments/problem1_nonperiodicity/analyze_portal_multilift_phase_quotient.py

Atomic record:

    results/problem1/20261002_portal_multilift_phase_quotient.json

Dependencies:

    problem1_twisted_half_period_portal_and_p32_descendants.md
    problem1_period32_complete_portal_root_census.md
    problem1_derivative_lift_antiperiodicity.md
