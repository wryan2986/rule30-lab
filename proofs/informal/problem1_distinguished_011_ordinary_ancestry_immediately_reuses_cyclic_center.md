# Distinguished 011 ordinary ancestry immediately reuses the cyclic center

Status: `partial-proof` / stopping-fence refinement. Problem 1 remains OPEN.

## Setup

At the preceding cyclic `t` source `q=t+2` in the two-bit nonreset forced-birth passage, the established local identities now give

    (r_-2(q), r_-1(q), r_0(q)) = (0,1,1).

Thus the cell `r_-1(q+1)=1` on the backward route from the later forced birth is produced by the distinguished `011` neighborhood. Sensitive-1 provenance stops here because neither 1-valued parent of `011` is Boolean-sensitive.

Run135 observed that ordinary 1-ancestry can always continue through a 1-valued parent, but left open whether the *distinguished source-relative* `011` family might nevertheless have bounded reuse when routed back to finite initial support.

## Exact local reconnection

For this distinguished `011`, the two 1-valued parents are

    r_-1(q)=1  and  r_0(q)=1.

The right parent `r_0(q)` is exactly the center of the preceding cyclic `t` source. Therefore an ordinary 1-ancestry route from the forced-birth lineage can reconnect immediately to the already-existing cyclic center:

    center(t+4)=1
      <- r_-1(t+3)=1          [produced by 011]
      <- center(t+2)=1.        [choose the right 1-parent]

No additional spacetime argument or remote initial-support routing is needed. The exceptional `011` is an obstruction only to *sensitive* 1-provenance; for ordinary 1-ancestry it permits immediate reuse of the previous cyclic-center lineage.

For completeness, the next forward neighborhood is also rigid. The gate-`t` identity gives `r_1(q) OR r_2(q)=1`, hence

    r_1(q+1)=f(1,r_1(q),r_2(q))=0.

Together with FULL's center value `r_0(q+1)=0`, the neighborhood producing `r_0(q+2)=1` is exactly

    (r_-1(q+1),r_0(q+1),r_1(q+1)) = 100,

which is the already-established sensitive route back into the distinguished `011` cell.

## Consequence

This closes the simplest version of the run135 target. Merely requiring the distinguished `011` events to possess ordinary ancestry in the finite initial 1-support cannot yield a bounded-reuse theorem: locally, every such event already has a canonical-looking reuse route through the preceding cyclic center. Iterating ordinary ancestry therefore need not assign a new initial 1-site, or consume any visibly new finite resource, at each forced-birth episode.

Combined with the previous stopping fences:

- unconditional sensitive routing gives strict nonreuse but escapes into the infinite initial zero tail;
- ordinary 1-ancestry stays within finite initial 1-support but can reuse lineages;
- at the distinguished source-relative `011` itself, that reuse is not merely generic: it is explicitly available through the preceding cyclic center.

A successful finite-support contradiction must therefore attach extra data that changes across cyclic episodes (for example a moving-cut crossing state, ordered interval, or another invariant using the complete gate/right-fringe constraints). A proof that only assigns an initial 1-ancestor to each distinguished `011` should be treated as insufficient unless it separately proves bounded multiplicity despite this immediate center-reuse route.

Dependencies: `problem1_full_center_drop_forces_011_at_cyclic_t_source.md`, `problem1_forced_birth_sensitive_route_previous_source_dichotomy.md`, `problem1_initial_one_ancestry_exists_but_has_unbounded_generic_reuse.md`, `problem1_arbitrary_finite_center_trace_by_left_permutivity.md`.
