# Astra automation handoff — 2026-09-16 run 74

## What changed

Continued from run 73 at branch tip `d7dcbfe00bf34637d51a306666955a04f0fde6b6`; there was no intervening work.

Added:

- `proofs/informal/problem1_dyadic_graph_embedding_and_leaf_portal_theorem.md`

Research commit: `43aa0a95b4c43cd221572d201170e19594dbbf8b`.

## New structural result

Proved an exact `p -> 2p` decomposition for the dyadic terminal zero-return tree.

Let `E_p(w)=ww`. Then every reachable proper-period vertex of `G_{2p}` is inherited from `G_p`:

`{W in G_{2p} : per(W)<2p} = E_p(V(G_p))`.

The no-merger theorem is essential: repetition already supplies the inherited route to each proper-period target, so a full-period branch cannot later return to or merge into the lower-period subgraph.

Inherited even internal vertices reproduce their old simple children. The only points where new full-period structure can leave the inherited subgraph are repeated old leaves.

If `l` is an odd leaf of `G_p`, then `ll` has even total parity and primitive block `l` of odd parity. Thus at period `2p` it becomes a unary phase-collapsed internal vertex. Its integrations satisfy `S^p x = complement(x)`, hence have exact period `2p`; its unique child enters genuinely new full-period structure.

Therefore `G_{2p}` is obtained from a repeated copy of `G_p` by replacing each old leaf with a unary **portal**, followed by a finite full binary tree consisting entirely of exact-period-`2p` vertices. New full-period components cannot merge with each other or return to the inherited subgraph.

If `B(l)` is the number of new full-period even internal vertices in the tree attached to old leaf `l`, then

`L_{2p} = sum_l (B(l)+1) = L_p + sum_l B(l)`.

This exactly explains `p=8 -> 16`: the unique `p=8` leaf becomes the unique portal, followed by 15 full-period binary vertices and 16 leaves.

## Best next target

Do not construct `G_32` monolithically. There should be exactly `L_16=16` portals at period 32, one per period-16 terminating necklace. Explore each portal's new full-period component independently and look for a way to predict its internal-node count `B(l)` from the old leaf word `l`. A formula or recurrence for these portal-tree sizes would directly give the terminating-necklace count recurrence.
