# Astra automation handoff — run 119

Problem 1 remains OPEN.

Starting branch tip: `db0015088bc362236580e1df2fc84b713c603ff4` (`research/astra-next`). No intervening work was found after run118.

## New result

Tested the run118 proposal to trace each forced beta=1 birth through a canonical backward 1-ancestor to time zero. The local Rule-30 rule `f(l,c,r)=l XOR (c OR r)` blocks the naive construction: output 1 has predecessor triples `001,010,011,100`, so no left/center/right predecessor is uniformly a 1-parent, and one case has two possible 1-parents. A sensitivity-based canonical left path exists but merely follows the light-cone boundary and does not provide a consumed original-support resource.

Recorded in `proofs/informal/problem1_canonical_backward_birth_certificate_has_no_unique_parent.md`.

## Next target

Do not pursue single-parent ancestry without extra phase information. Instead attach the backward certificate to the *forcing mechanism* for the established two-bit nonreset birth. In `problem1_nonreset_return_birth_spacing.md`, beta=1 at t+6 is forced because the return right pair is 10 and the relevant zero-pair flag vanishes independently of the wider shadow. Expand that exact flag dependency backward through the known centers `0,0,1` and right pair `10`. Determine whether the forcing reduces to a bounded set of time-t shadow cells, then test whether successive forced births require strictly ordered forcing sets or can reuse the same set.

This run is a stopping fence, not a contradiction or finite birth budget.
