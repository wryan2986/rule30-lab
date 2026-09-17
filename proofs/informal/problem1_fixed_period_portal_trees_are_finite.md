# Problem 1: fixed-period portal trees are automatically finite

## Context

Run 90 proved that, after a unique portal birth into the exact-period-`n` sector, every even-parity full-period zero-return vertex has exactly two distinct child necklaces and every odd-parity full-period vertex is terminal. Together with the previously established unique-parent/no-merger property, the handoff left open whether such a full-period portal tree can have an infinite branch.

At a **fixed finite period `n`**, it cannot. No new dynamical statistic is needed for this particular question: finiteness of the necklace state space plus unique parent already rules it out.

This note is deliberately scoped to fixed `n`. It does **not** give a useful uniform depth bound as `n` grows and therefore does not by itself close the original finite-support/FULL contradiction in `ASTRA_HANDOFF.md`.

## Proposition

Fix ambient period `n`. Consider a portal child `v_0` in the exact-period-`n` zero-return sector, whose parent `p` is a proper-period vertex. Assume the established zero-return facts used in runs 85--90:

1. every nonzero zero-return target has a unique parent under `P_n = D o rho_n^{-1}` (equivalently, no mergers);
2. all descendants under consideration remain in the exact-period-`n` sector until terminal odd parity (period cannot increase under ancestry, and the portal construction enters the full-period sector);
3. child edges are the reverse orientation of the parent map.

Then the descendant component rooted at `v_0` is finite. In particular every branch reaches an odd-parity terminal vertex in finite depth.

## Proof

There are only finitely many binary necklaces of length `n`, hence only finitely many exact-period-`n` necklaces.

Suppose a descendant branch from `v_0` were infinite:

`v_0 -> v_1 -> v_2 -> ...`.

Because the exact-period-`n` necklace set is finite, some necklace must repeat. Choose the first repetition along the branch. The repeated segment is a directed cycle in the child orientation, equivalently a cycle of the parent map `P_n`.

That cycle cannot be entered from outside. Indeed, let `v_j` be the first vertex of the cycle reached from `v_0`. If `j>0`, then `v_j` has two distinct parents in the child-edge sense: its predecessor `v_{j-1}` on the entry path and its predecessor on the directed cycle. Equivalently, reversing orientation, the unique-parent/no-merger structure is violated.

The only remaining possibility is `j=0`, so the portal child itself lies on the cycle. But `v_0` already has the proper-period portal parent `p`, while the cycle supplies a distinct full-period predecessor. Again this violates unique parent. (The two predecessors cannot coincide because `p` has proper period and the cycle predecessor has exact period `n`.)

Therefore no descendant branch from a portal child can repeat a necklace. Since only finitely many exact-period-`n` necklaces exist, every branch is finite.

By run 90's branching theorem, a nonterminal exact-period-`n` vertex has exactly two children and an odd-parity vertex has none. Hence every maximal branch ends at an odd-parity leaf, and the entire portal component is a finite full binary tree.

## Crude quantitative consequence

Let `N_prim(n)` denote the number of primitive binary necklaces of length `n`:

`N_prim(n) = (1/n) * sum_{d|n} mu(d) 2^(n/d)`.

Every vertex in a full-period portal component is a primitive necklace and no branch can repeat one. Thus every branch has fewer than or equal to `N_prim(n)` full-period vertices. This is only a finite-state bound, asymptotically about `2^n/n`; it is far too weak to replace the desired structural bound.

For dyadic `n=2^m`, the primitive-necklace count simplifies to

`N_prim(2^m) = (2^(2^m) - 2^(2^(m-1))) / 2^m`,

because the only square-free divisors contributing to the Mobius sum are `1` and `2`.

## Strategic consequence

The specific question posed at the end of run 90 -- whether a fixed-period full-period portal tree can be infinite -- is resolved: **no**.

However, this should not be mistaken for a solution of Problem 1. The authoritative `ASTRA_HANDOFF.md` bottleneck concerns turning FULL for an actual finite-support survivor into a contradiction / finite birth budget. Fixed-`n` state-space finiteness supplies no uniform control as the relevant period/width grows and does not exclude the one continuing finite-support candidate identified in the older phase-collapse work.

The next useful target should therefore not be another proof of fixed-period termination. It should connect the zero-return/portal formulation back to the original finite-support width or birth budget, ideally by proving a bound on portal depth or number of full-period births in terms of original support that is substantially smaller than the trivial primitive-necklace count.

## Status

This closes the run-90 subproblem of fixed-period portal-tree finiteness. Problem 1 remains open.
