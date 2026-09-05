# Testing endpoint pairings for the three-return signed certificate

Status: `refuted` for the single-bit, single-sign-remainder certificate;
`partial-proof` for the exact obstruction argument below. Problem 1
remains open. This pass follows `ASTRA_GOAL.md` from source commit
`b86a0ea892549287d4431fce69d29a743855bf9b`.

## Route selection

The exact joint-fiber identity now explains why a universal five-vector
recurrence is unavailable. The connected-region obstruction also prevents
a single real region from certifying all admissible ancestor vectors by
hyperplane avoidance. Neither result excludes an explicit endpoint pairing.

Updated ranking (`heuristic`, not a mathematical assertion):

| Rank | Route | Plausibility / all-depth potential | Falsifiability / testability | Cost |
| --- | --- | --- | --- | --- |
| 1 | Sign-reversing endpoint involution with a nonzero remainder | Medium / high | High for concrete pair rules / high | Low initial, high structural proof |
| 2 | Return-context partition controlling the joint fiber table | Medium / high | High for specified partitions / high | Medium to high |
| 3 | Arithmetic exclusion inside a region that meets cancellation | Low without an arithmetic mechanism / high | High / high | Low initial |
| 4 | Boundary depth bound using complete return residues | Medium / partial necessary obligation | High / medium | High |

This pass first tests the broad class of pairings that exchange one free
binary coordinate of a concrete endpoint. It does not posit a fixed
coordinate or a deterministic rule for choosing the coordinate.

## Exact proposed certificate and falsification gate

Let `B=B_a(k,L,x)` be the distinct dominant adjacent-shadow belief, with
weight `w(y)=(-1)^cost(y)`. An involution `I:B->B` is sign-reversing away
from its fixed points if `w(I(y))=-w(y)` whenever `I(y)!=y`. Each nonfixed
orbit then contributes zero. A nonempty fixed set with a common sign would
certify `S(B)!=0`.

The first candidate requires only that every nonfixed pair differ in one
binary coordinate: `y xor I(y)=2^b`. Since both endpoints lie in the same
depth-L cylinder, this automatically requires `b>=2L`. The bit `b` may
depend arbitrarily on the pair; no finite-state assumption is imposed.

Form the bipartite graph whose vertices are the positive and negative
endpoints of `B` and whose edges are all such single-bit pairs. A matching
saturating the smaller sign class would leave only the larger sign class
unmatched. If the two class sizes differ, it supplies the proposed finite
certificate. An explicit subset of the smaller class with fewer graph
neighbors than vertices would rule out every such saturating matching.

Admission, fixed before the run:

- Such a deficient set on one admissible occurrence refutes the proposed
  single-bit-involution certificate. It would require a pairing with some
  nonlocal pairs, a mixed-sign remainder with additional structure, or a
  different invariant. It would not refute nonvanishing or the adjacent
  shadow inclusion.
- If the matching succeeds on all existing occurrences, the next task is a
  structural proof of the matching property using the frontier recurrence,
  not a larger census. Finite success is not an all-depth theorem.

Use only the existing full-domain box: both phases, complexities at most 16,
all 56 admissible triples and every cut, with final-u admissibility. Expected
instance set has 19 occurrences. Order by complexity, phase p then u, state,
cut, and gap triple. Stop the pairing search at the first failure or exhaustion.
Every graph uses distinct concrete endpoints, not generator representations.

Limits: one local CPU, 120 seconds, 1 GiB address space, forced-schedule cap
64. Hand graph cases and exhaustive tiny-graph comparison precede the
frontier graph checks. Compare direct and recursive endpoint beliefs, and
verify any reported deficient set by independently recomputing its complete
neighborhood. The analyzer must write exact parameters, full source commit,
source/output hashes, hardware/software, timings, and limitations atomically.
Muse implements the bounded check; the lead owns the resulting theorem and
scope interpretation.

## Exact counterexample on the admissible domain

The first failure in the specified existing box is

```text
phase u, k=14, x=0x642fdfb, L=2, cut=1, gaps=(2,2,2).
forced schedule: tutututu
base prefix: t
observed w E(g): tututut
final-u admissibility word: tutututu
generator witness: uuuuputptutpuu
```

The leading `u` of the witness denotes phase seed 1 at complexity one.
There are 134 distinct dominant endpoints: 84 of even defect and 50 of odd
defect, giving signed mass `34`. This is an actual three-return occurrence,
not merely a stripped ancestor or an abstract mask path.

The opposite-sign Hamming graph has 10 edges. A maximum matching covers only
9 of its 50 negative vertices. More directly, 41 negative vertices are
isolated, with no positive Hamming neighbor. The smallest is

```text
y*=0x190825b.
```

Every shadow has 25 bits by the phase-u bit-length law at complexity 13.
Bits below position 4 cannot change without leaving the depth-two cylinder;
flipping a bit at position 25 or above cannot produce a complexity-13 shadow.
The complete finite bit check is therefore positions 4 through 24 inclusive.
No flip of `y*` in that range gives a positive endpoint of this belief.

## Single-bit pairing obstruction (`partial-proof`)

For this belief there is no sign-reversing involution whose nonfixed pairs
differ in one bit and whose fixed set is nonempty and has a common sign.

Proof. In any such involution, the isolated negative vertex `y*` cannot be
paired with a positive vertex differing in one bit. Sign reversal prevents
pairing it with a negative vertex. Hence it must be fixed, so a fixed set of
one sign would have to be negative. But all nonfixed pairs cancel and the
total signed mass is positive (`34`); the sum of the fixed weights must
therefore be positive. Contradiction.

This proves an impossibility result for the entire stated class of pair rules,
including rules that choose different bits at different endpoints. It does
not assume the matching algorithm is optimal: one independently checked
isolated negative vertex and the exact positive signed mass suffice. The
41-vertex empty-neighborhood set supplies a larger Hall certificate but is
not needed for this proof.

The identity involution remains sign-reversing away from fixed points
vacuously; it has both signs among its fixed points. Thus omitting the
single-sign fixed-set condition would make the refuted assertion false as a
description of this result.

## Verification and scope

`finite-exhaustive`: the existing occurrence domain through k=16 was rebuilt
with 19 occurrences. The pairing search stopped at its third instance, the
first obstruction. The other 16 instances were not tested for this property.
Direct and recursive concrete beliefs agree on all three tested instances.
Packed and Boolean frontier generators agree on the small verification box.
Seven hand matching cases and all 26 bipartite graphs with one or two vertices
on each side check the matching routine; the decisive graph is also checked
by independent endpoint-pair and bit-toggle traversals.

The exact record is `results/problem1/20260905_signed_belief_hamming_pairing.json`;
reproduce it with `python3 scripts/check_signed_belief_hamming_pairing.py`.
The record distinguishes complete enumeration of the occurrence domain from
the pairing search's deliberate first-counterexample stop. It includes the
full deficient set, the isolated witness, exact parameters, hashes, full
source commit, timings, and software/hardware facts.

`inconclusive`: involutions with some pairs changing multiple bits; fixed
sets of mixed signs whose net mass has another structural certificate;
other arithmetic or boundary invariants; all-depth signed nonvanishing.
There is no logical obstruction here to a nonlocal pairing. This experiment
does not justify a larger Hamming-radius sweep without a specific proposed
pair map or structural mechanism.
