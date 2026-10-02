# Problem 1: blind charge regenerates across a singleton portal

Status: FAILED — COUNTEREXAMPLE FOUND (`refuted`) for the precisely stated
nonincrease conjecture below. The computed finite domain has a separate
`finite-exhaustive` record. Problem 1 remains OPEN.

## 1. Candidate and admission

Let `p>=2` be dyadic and let `w` be an odd terminating binary temporal
word of length `p`, in the finite zero-return basin of the repository.
Its derivative portal has temporal period `2p`. After the universal
two-lift normalization use the boundary `(x,J)`, where `x` is the
antiperiodic integration of `w` and `J=1^(2p)`. Construct its unique
same-period dynamic layers until the first all-zero temporal layer.
Let `h(w)` be that first post-normalization layer index.

For each existing normalized depth-r orbit, let `k_r(w)` count its blind
temporal phases. Define the single-connector charge

    kappa(w)=sum_(r=1..min(p-1,h(w))) max(k_r(w)-1,0).   (1)

The all-period cone theorem proves `u_r=0` from depth `p` onward. Thus (1)
is the COMPLETE ambiguity-dimension charge of this connector, even if
its first zero return lies billions of layers later. If an all-zero
layer is reached earlier it is retained, and its next child is not built.

Let `z` be the canonical rotation of the high temporal word at that first
zero return. Assume z is odd; the new full-period root is then a terminal
singleton, with no branching choice at this return.

CONJECTURE (now refuted): for EVERY such finite terminating w,

    kappa(z)<=kappa(w).                               (2)

This was a test of the simplest unweighted no-regeneration rule for a
charge passed along finite portal ancestry. A counterexample kills that
rule. Absence in the eight-root domain would have been finite evidence
only. No new connector census was needed in either case.

## 2. Exact counterexample

Use genuine portal index 2 from the complete p32 root census:

    w=0101101101111011,                 p=16,
    z=00001000111100010010101100101111,  p=32.

The imported root certificate gives first zero depth `1,555,560,444`,
odd returned word z of exact period 32, and a singleton component.
That depth is measured in the old connector convention, not observer
depth and not the post-normalization index `h(w)`.

The exact observer counts are

    k_r(w): 5,5,4,1,1,0,0,...  through r=15,
    k_r(z): 11,11,6,2,1,1,0,0,... through r=31.

Consequently

    kappa(w)=4+4+3=11,
    kappa(z)=10+10+5+1=26.

The proposed inequality would be `26<=11`, an explicit contradiction.
The increase is 15. Using the certificate's actual unrotated target
instead of its canonical target gives the SAME profile and charge.

Portal 2 is the smallest index in the declared eight-root domain. This
does not claim the globally smallest period or word counterexample.

## 3. Complete declared domain

All eight odd singleton roots of the complete p16-to-p32 census violate (2):

| portal | parent charge | returned-leaf charge |
|---:|---:|---:|
| 2 | 11 | 26 |
| 3 | 11 | 18 |
| 5 | 13 | 27 |
| 7 | 7 | 27 |
| 9 | 10 | 23 |
| 13 | 6 | 21 |
| 14 | 6 | 25 |
| 15 | 5 | 22 |

The eight endpoint identifications are imported from
`results/problem1/20261002_period32_complete_portal_root_census.json`
and `problem1_period32_complete_portal_root_census.md`. Their SHA256 and
all words are recorded in the new result. Their billion-lift traversals
were not repeated. Fresh work verifies the charges, temporal recurrences,
and actual/canonical phase equivalence on those certified inputs.

## 4. Reproduction and independent checks

Run from the repository root:

    python3 experiments/problem1_nonperiodicity/check_blind_charge_portal_transport.py

The script constructs only depths 1..15 of the eight parent observers and
1..31 of their returned-leaf observers, never traversing the old connectors.
It checks the polynomial packed transition and blind predicate against
the independent two-original-row implementation on 4,092 raw comparisons.
It then verifies 17,792 cyclic temporal transitions, including wraparound,
and deep blind predicates on the concrete parent, canonical-target, and
raw-target prefixes. The two implementations use the same precisely
specified flat bit encoding, not an array of packed pair codes.

Atomic record:
`results/problem1/20261002_blind_charge_portal_transport.json`.
It includes exact parameters, full base commit, source/input/payload hashes,
hardware/software, timing, and resource caps. The parent checked the script,
repaired early-zero handling and complete-depth validation, and re-ran it
after adding independent deep transition/phase checks and provenance.

Independent numerical review: `gpt-6-luna`, low effort, agent
`01a0fd9e-595e-7850-a7cc-6d1413fa7160`, read-only. It computed the same
eight pairs of charges and checked the transitions independently. Its
initial report called the first depth with `k_r=0` a zero return. The
parent rejected this terminology, and the reviewer corrected it: `k_r=0`
means BLIND-FREE OBSERVER, whereas a spatial zero return requires BOTH
paired coordinates to vanish at EVERY phase. The metric can stop once
`k_r=0` by blind-set nesting, but that is not portal termination.

Computational worker: `opencode-go/space-bunny-free`, agent
`01a0fd97-6aab-7fa0-a7b8-771971865112`, owned only the new checker/result.
Its initial encoding/driver mistakes were corrected before accepting its
results. Its informal suggestion that counts universally double is not
accepted: the first example has 5->11, and this finite ledger proves no
general growth law. Both agents were closed after parent integration.
No Astra route or escalation was used.

## 5. What is eliminated; what remains open

The unweighted scalar (1) cannot be treated as a nonincreasing resource
across a dyadic singleton portal, even when no branch choice is made.
Fixed-period boundedness and interperiod nonincrease are distinct claims.

This refutes neither the cyclic cone theorem nor every possible weighted
or decorated transport. It gives no FULL countermodel, no bound on
original-support reuse, no exclusion of all K=3 periods, and no solution
of the center-column prize problem. A surviving transport argument must
explain the exact regeneration shown here before using accumulated local
ambiguity losses as an original-support budget.
