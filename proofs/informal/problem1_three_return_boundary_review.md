# Three-return boundary and convex-ancestry review

Status: boundary conjecture `inconclusive`. Ancestry replay `finite-exhaustive`;
single-region obstruction `partial-proof` on verified ancestry. Signed
nonvanishing and Problem 1 `inconclusive`. No infinite nonperiodicity claim is made.

Muse Spark 1.3 Contributor reviewed the boundary question and independently
checked witness ancestry below. The lead reviewed and integrated this note.
The Python reference is untouched.

## 1. Boundary conjecture: compatibility only, bound unproved

Conjecture (`inconclusive`): every three-return occurrence x in O(a,k) with cut
c satisfies c+1 <= k-2, with prefix languages, gap triples, and admissibility
as in the adjacent-shadows note and the scope audit.

At L = c+1 = k-1 the iterated projection theorem forces the top base-four
digit to 3 for phase p and 1 for phase u. The bit-length law allows top digits
{2,3} for p and {1} for u, so projection and bit length are compatible. No
contradiction emerges from this comparison, and the bound remains unproved.
Nothing here asserts an impossibility result or a schedule-length bound.

## 2. Finite context, not a proof

`finite-exhaustive` through stated boxes only, zero adjacent-shadow violations:
k <= 16 with 19 occurrences; k <= 20 with 210; k <= 25 with 3,395. A repeat at
or below these caps would re-derive known entries, and larger caps are frozen,
so no census was run in this pass.

## 3. Independent witness and code review

Admission: if the named witnesses replayed exactly, the lead ancestry record
is corroborated; if any check mismatched, the obstruction below would be
withheld and flagged. Caps: two named states, 4,999 generator agreement cases,
in-memory, seconds, /tmp only, no repository writes, no frontier census.
Provenance: `results/problem1/20260905_boundary_convex_ancestry_replay.json`,
archived from the original `/tmp` record with the complete independent replay
source embedded and hashed. It includes machine facts, timings, full Git
commit, and status `finite-exhaustive`.

Replay (`finite-exhaustive` for the two named cases, two independent steppers
agreeing throughout): uuputpuuuututututut gives 0x190b934bc7 (k=19, 37 bits);
uutuuttuupupuuupup gives 0x6473d46ab (k=18, 35 bits). The word head letter is
the phase label over seed 1. Strip relation 0x190b934bc7 = 4*0x642e4d2f1 + 3,
so x1 membership follows by projection. Recomputed schedules match the record
(uttutututu; ttttutututu) with observed wE(g) lengths 9 and 10, gap-222 windows
at cuts 3 and 4, and clean final-u admissibility words. Arithmetic rechecked:
ell values -83 and +2; 2v- + 83v+ = (773,0,815,54,815), in ker(ell) and nonzero.

Code review by reading (no independent mass recomputation): oracle generators
match the lift-recursion note; the schedule stepper follows the renewal rule
with cap 64 never approached; level-0 fibers are unreachable at these depths;
beliefs sum over distinct endpoints per the audit convention; the mask-11
identity child mass = V15 - V11 holds numerically (-83, +2). The endpoint
enumerations (780 and 35 parents) rest on the lead run's direct/recursive
agreement and are explicitly not recomputed here.

## 4. Obstruction scope

`partial-proof` on verified ancestry: ell_1011 is linear hence continuous, takes
values -83 and +2 on any connected set K containing both vectors, so its image
is connected in R and contains 0. Nonconvex connected regions therefore also
fail strict hyperplane avoidance. Explicit witnesses: (2v- + 83v+)/85 for convex
regions, unnormalized for cones; opposite signs survive mass normalization.

Untouched (`inconclusive`): disconnected or discrete sets; regions indexed by
depth, adjoined digit, or schedule (depths 3 vs 5, transition digits 1 vs 3);
arithmetic exclusions inside a region; endpoint pairings.
Hence `refuted`: one connected region covering these ancestor vectors while
avoiding the mask-11 hyperplane. The boundary obligation c+1 <= k-2, full
signed nonvanishing, and Problem 1 stay `inconclusive`.
