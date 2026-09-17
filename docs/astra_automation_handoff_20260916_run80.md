# Astra automation handoff — run 80

## Main result: return-existence gap closed

The off-diagonal cycles found in runs 78–79 do **not** obstruct connectors launched by actual zero-column integrations.

For the deterministic inverse map `T(a,b)=(y,a)` on `a != 0`, run 78 proved injectivity and run 77 proved that a zero return occurs exactly on a diagonal hit. Immediately after a nontrivial singular integration, every connector begins at a pair `(x,0)` with `x != 0`.

No off-zero state can map to `(x,0)`, because the second component of every image `T(a,b)` is the input `a`, which is nonzero. Thus `(x,0)` has no predecessor in the off-zero domain.

If its connector avoided the diagonal forever, finiteness would force a repeated off-zero state. Injectivity then eliminates any transient: cancelling predecessors backwards forces the initial `(x,0)` itself to lie on the periodic orbit. That would give `(x,0)` an off-zero predecessor, contradiction.

Therefore every boundary-launched connector reaches a diagonal / zero return in finite time.

Full proof:

`proofs/informal/problem1_portal_return_existence_from_boundary_state.md`

## Consequences

- Ambient off-diagonal cycles remain real but are inaccessible from actual post-zero boundary states.
- The run-78 caveat is removed for the reachable zero-return graph.
- Run 74's finite doubled-leaf portal trees are unconditional again.
- The first p=32 portal's >100,000,000-step lower bound is only a computational cost issue; it is now proved to return eventually.

## Next target

Resume the p -> 2p counting program. The main blocker is efficient exact traversal of the guaranteed-finite but extremely long p=32 connectors. Seek a multi-step accelerator or a structural formula/bound for first diagonal-return time from `(x,0)`.
