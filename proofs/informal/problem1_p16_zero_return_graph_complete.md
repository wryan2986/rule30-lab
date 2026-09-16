# Problem 1: complete p=16 zero-column first-return graph

## Purpose

Run 68 disproved the working uniqueness conjecture by finding two rotation-inequivalent terminating period-16 initial necklaces. The proposed replacement target was to enumerate the entire zero-column first-return graph at p=16, modulo temporal rotation.

This note completes that finite enumeration.

## Setup

Use the established recurrence

\[
q_{i+2}=S q_i\oplus(q_{i+1}\lor q_i),
\]

with cyclic temporal shift `S`, and reverse predecessor equation

\[
w=Sx\oplus(u\lor x).
\]

The exact predecessor classification from earlier runs is used throughout:

- if `u != 0`, there is exactly one cyclic predecessor `x`;
- if `u = 0` and `w` has odd XOR parity, there is no predecessor;
- if `u = 0` and `w` has even XOR parity, there are exactly two complementary predecessors.

Thus the full reverse basin can be compressed to an induced graph whose vertices are zero-column states `(0,w)`. At an even-parity vertex, integrate the two derivative predecessors and follow each deterministic reverse connector until the next zero-column state. Quotient vertices by cyclic rotation of `w`. At the terminal vertex `(0,0)`, discard the trivial all-zero self-predecessor and follow only the nontrivial branch.

## Exact enumeration result

For p=16, exhaustive exact traversal from the terminal pair closes after visiting only

\[
\boxed{36\text{ zero-target necklaces}}.
\]

They split as follows:

- **20 even-parity internal vertices**;
- **16 odd-parity leaves**;
- **39 directed connector edges** (the terminal zero vertex has one nontrivial outgoing edge; each of the other 19 even vertices has two derivative-lift edges).

After quotienting by rotation, the induced graph is a **finite directed acyclic graph**. There are no unresolved branches and no cycles in the zero-return graph.

Every odd-parity leaf has exact rotational period 16. Hence every leaf is a legal full-period odd-parity initial necklace `(0,c)`. Conversely, every reverse branch from the terminal pair ends at one of these 16 legal leaves. Therefore the complete period-16 terminating set contains exactly

\[
\boxed{16\text{ rotation-inequivalent terminating initial necklaces}.}
\]

This upgrades run 68's lower bound of two to an exact classification.

## The 16 terminating necklaces

Using lexicographically minimal cyclic rotations in the repository's forward-shift convention, the complete list is:

| representative `c` | termination width |
|---|---:|
| `0000010101000101` | 87867 |
| `0011101111101011` | 183184 |
| `0101101101111011` | 196189 |
| `0001010011100101` | 229338 |
| `0101010110111111` | 253537 |
| `0000100100100101` | 271596 |
| `0000001001011001` | 291257 |
| `0010111001100111` | 527724 |
| `0001010010001111` | 551910 |
| `0000011101010011` | 555813 |
| `0010101110101101` | 575211 |
| `0101111111011111` | 634886 |
| `0000110110000111` | 645655 |
| `0001001111001111` | 667052 |
| `0001111001111111` | 770532 |
| `0010111100111111` | 894235 |

The first entry is run 68's `c16_a`. Run 68's second representative `1001110010100010` is a rotation of the fourth canonical representative `0001010011100101`, with the same width 229338.

Each width above is also the reverse distance from the terminal zero pair to that legal initial state. Direct forward recurrence reproduces the same terminal width for every representative.

## Internal-node period structure

The 20 even-parity internal zero targets have primitive rotational periods distributed as

- period 1: 2 vertices;
- period 2: 1 vertex;
- period 4: 1 vertex;
- period 8: 1 vertex;
- period 16: 15 vertices.

Thus the graph contains the expected inherited lower-period spine, but most of its internal branching structure is genuinely new at period 16. This is the key correction to the earlier attempted uniqueness/phase-collapse induction: the inherited scale-transition singularities remain special, while fifteen full-period even-parity zero targets create the new p=16 return structure.

## Reproducibility

The enumeration requires no search over all 2^32 state pairs.

1. Start at zero-target vertex `(0,0)`.
2. Solve `Sx xor x = w` exactly. For even `w`, there are two complementary solutions; at `w=0`, discard the trivial `x=0` terminal self-loop.
3. For each retained solution, form predecessor state `(x,0)`.
4. While the first component is nonzero, use the unique-predecessor recurrence to step backward. This connector has no branching and cannot die.
5. Stop at the next state `(0,w')`, canonicalize `w'` by cyclic rotation, and add the corresponding directed edge.
6. If `w'` is odd parity, it is a leaf. If even, continue unless its canonical necklace was already processed.

The traversal visits 36 canonical zero targets and then exhausts its queue. A graph cycle check finds none.

For the 16 odd leaves, minimal cyclic-period testing gives period 16 in every case. Forward propagation from each `(0,c)` independently reaches two consecutive zero columns at the width listed above.

## Research consequence

At p=16 the correct finite object is not a single reverse path but a small zero-return DAG. The full state trajectories can be hundreds of thousands of columns long, yet all branching information compresses to only 36 zero-target necklaces.

This suggests a more viable structural program for Problem 1:

1. define the zero-column first-return graph `G_p` rigorously;
2. prove that the lower-period graph embeds into `G_{2p}` through repetition/antiperiodic derivative lifting;
3. characterize the genuinely new full-period even zero targets introduced at each doubling;
4. seek a recurrence for the number and arrangement of legal odd leaves rather than uniqueness of a leaf.

The immediate computational target should be p=32 only at the **zero-return graph level**, not by enumerating all initial words. Before attempting that potentially much larger calculation, it is worth comparing the exact p=1,2,4,8,16 graphs and their leaf counts to identify a plausible recurrence.