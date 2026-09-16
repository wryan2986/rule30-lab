# Problem 1: dyadic zero-return graph embedding and leaf-portal theorem

## Purpose

Run 73 reduced the dyadic counting problem to reachable even zero targets with even-parity primitive block. The comparison through `p=16` also suggested an inherited lower-period spine plus genuinely new full-period branching. This note proves the exact separation between those two pieces under `p -> 2p`.

## Setup

Let `G_p` be the simple terminal reverse zero-return tree modulo cyclic rotation at dyadic ambient period `p=2^n`, with the trivial `(0,0)` self-loop discarded. Vertices are zero targets `w`; even-parity targets are internal and odd-parity targets are leaves.

Write

\[
E_p(w)=ww
\]

for repetition from length `p` to length `2p`.

We use the previously proved facts:

1. reverse propagation is unique whenever the middle column is nonzero;
2. the reverse map is shift-equivariant;
3. the reachable zero-return component is a finite rooted tree (in particular, no mergers);
4. at dyadic length, odd parity forces full period;
5. an even target genuinely branches iff its primitive block has even parity.

The cellular recurrence commutes with repetition, so any finite connector at period `p` repeats to a connector of the same length at period `2p` unless the status of its starting zero target changes because total parity changes.

## Theorem 1: every reachable proper-period target at `2p` is inherited

Let `W` be a reachable vertex of `G_{2p}` whose exact rotational period is at most `p`. Then

\[
W=E_p(w)=ww
\]

for a unique length-`p` necklace `w`, and `w` is reachable in `G_p`.

Equivalently,

\[
\boxed{\{W\in G_{2p}:\operatorname{per}(W)<2p\}=E_p(V(G_p)).}
\]

### Proof

Because `2p` is dyadic, every proper divisor of `2p` divides `p`. Hence any proper-period length-`2p` word is a repetition `ww` of a length-`p` word.

First, every vertex of `G_p` does occur after repetition in the terminal reverse basin at length `2p`. Starting from the terminal root, repeat the corresponding period-`p` reverse connectors. At an even period-`p` target, the repeated target is still even and its derivative integrations reproduce the repeated period-`p` integrations when the primitive block has even parity; at a primitive-odd target the two length-`2p` integrations are phase-equivalent, so the inherited route is still represented by a unique simple edge. Thus the inherited path to `E_p(w)` exists.

Now suppose a reachable proper-period vertex `W=E_p(w)` could also be reached through some route not descending from the repeated `G_p` route (for example from a genuinely full-period vertex). The repeated route already gives `W` its unique parent/path from the root. A second route would create a merger at `W`, contradicting the no-merger theorem. Therefore every reachable proper-period target lies on the inherited repeated tree and corresponds to a reachable `w` in `G_p`. QED.

## Theorem 2: inherited internal vertices reproduce their old children

Let `w` be an even internal vertex of `G_p`. Then `W=ww` has the same primitive block as `w`, and its simple children in `G_{2p}` are exactly repetitions of the simple children of `w` in `G_p`.

### Reason

If the primitive block of `w` has even parity, derivative integration over one primitive period returns to the same integration bit. Hence the integrations of `ww` already have period dividing `p`; they are precisely repetitions of the period-`p` integrations. Unique nonzero-column propagation then repeats the old connectors.

If the primitive block has odd parity, both at `p` and at `2p` the complementary integrations phase-collapse to one necklace. The repeated deterministic connector again gives the inherited child, and no-merger forbids an additional child leading back into the proper-period subgraph.

Thus old internal branching structure is copied unchanged.

## Theorem 3: old leaves become the only portals to new full-period structure

Let `l` be a leaf of `G_p`. By run 73, `P(l)=1` and `l` has exact period `p`.

At length `2p`, the repeated target

\[
L=ll
\]

has even total parity but primitive block `l` of odd parity. Therefore `L` is no longer a leaf. By the primitive-parity branch criterion it is a **unary phase-collapsed internal vertex**.

Moreover its derivative integrations have exact period `2p`: integrating through the first `p` positions flips the integration bit because `P(l)=1`, so

\[
S^p x=\bar x.
\]

Thus its unique simple child is full-period.

Combining this with Theorems 1--2 gives

\[
\boxed{\text{the only edges from the inherited proper-period subgraph into new full-period vertices originate at repeated leaves of }G_p.}
\]

Hence every old terminating necklace becomes exactly one **portal** into a new full-period component at doubled period.

## Corollary: exact decomposition of `G_{2p}`

The terminal zero-return tree at doubled dyadic period decomposes as follows:

1. a repeated copy `E_p(G_p)` containing **all** reachable proper-period vertices;
2. each repeated old leaf is converted from an odd leaf into an even unary portal;
3. from each such portal, one edge enters a component consisting entirely of exact-period-`2p` vertices;
4. every even vertex inside a new full-period component is a genuine binary branch (run 73);
5. every odd vertex inside it is automatically a legal full-period leaf;
6. no new full-period component can merge into another or return to the inherited subgraph, by the no-merger theorem.

Thus `G_{2p}` is obtained from `G_p` by replacing each old leaf with a unary portal followed by a finite full binary tree of new full-period targets.

This precisely explains the observed `p=8 -> 16` transition: `G_8` has one leaf, so `G_16` has one portal; after it lie the 15 full-period even internal vertices and 16 full-period odd leaves found computationally.

## Counting consequence

Let `L_p` be the number of terminating period-`p` necklaces. For each leaf `l` of `G_p`, let `B(l)` be the number of new exact-period-`2p` even targets in the full-period binary tree entered through its repeated portal. A finite full binary tree with `B(l)` internal vertices has `B(l)+1` leaves. Therefore

\[
\boxed{L_{2p}=\sum_{l\in\mathrm{Leaves}(G_p)}(B(l)+1)=L_p+\sum_l B(l).}
\]

The unresolved problem has therefore narrowed again: the `p -> 2p` recurrence does not need to track arbitrary lower-period targets at all. It only needs to determine the size of the new full-period binary tree attached to each old leaf.

For `p=8`, `L_8=1` and the unique portal has `B=15`, giving `L_{16}=16`.

## Next target

Study the full-period tree attached to a portal in terms of the old leaf word `l`. In particular, seek an invariant or finite return transformation that predicts `B(l)` directly from `l`. At `p=32` there should be exactly `L_16=16` such portals, one for each period-16 terminating necklace; they can be explored independently rather than constructing the entire period-32 state space at once.
