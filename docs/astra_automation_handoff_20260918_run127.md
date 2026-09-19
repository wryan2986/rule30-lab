# Astra automation handoff — run 127

Problem 1 remains OPEN.

Starting branch tip: `33ea4adef3094e1eb7b70f90d38043d9d1071904` (`research/astra-next`). No intervening work was found after run126.

## New result

Run126 left open routed provenance inside the support-saturating backward cone. The most canonical such route supplied directly by Rule 30's left-permutivity is now ruled out as a finite-support selector.

Since `f(l,c,r)=l XOR (c OR r)`, the left input is unconditionally Boolean-sensitive. Backward iteration of that unique unconditional sensitivity edge from `(j,t)` reaches time zero at `j-t`. Therefore for any fixed bounded source-relative event window `j in [a,b]`, all such intercepts lie in `[a-t,b-t]`. If the original actual support is contained in `[L,R]`, then after `t>b-L` every canonical left-sensitive intercept lies strictly left of the original support.

Thus the two simplest provenance selectors fail in opposite directions: the full backward cone eventually contains all original support (run126), while the unconditional left-sensitive ray eventually contains none of it.

Recorded in `proofs/informal/problem1_left_sensitive_routed_provenance_escapes_support.md`, commit `636ce840753a75c9200a4ccc7e33877b9a119311`.

## Next target

A surviving provenance/birth-budget route must use genuinely state-dependent branching or a richer moving-cut crossing invariant. It must prove both that the selected label remains tied to the finite original actual row and that resetting/nonresetting passages give strict advance or uniformly bounded reuse. Do not retry ordinary cone intersection or the unconditional left-sensitive characteristic.
