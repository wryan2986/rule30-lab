# Problem 1: exact path characterization of the scalar residence ledger

## Status

Structural no-go/refinement for the bounded-slack branch. Problem 1 remains OPEN.

## Setup

For a finite survivor write

    q_n = tau(2^n v) - n - R,
    delta_n = tau(2^(n+1) v) - tau(2^n v).

The exact scalar identity is

    delta_n = 1 + q_(n+1) - q_n,

with delta_n >= 0 because the residence times tau(2^n v) are nondecreasing in n.

Runs 101--105 extracted bounded discrepancy, bounded skip runs/jumps, return-block balance, extremal excursion ordering, and an arbitrary-binary countermodel. The following observation identifies exactly how much information is present in this scalar layer.

## Exact characterization

A sequence of integers q_0,q_1,... admits a nonnegative integer residence-increment sequence delta satisfying

    delta_n = 1 + q_(n+1) - q_n

if and only if

    q_(n+1) >= q_n - 1

for every n.

Proof: If delta_n >= 0, rearranging the identity gives q_(n+1)-q_n >= -1. Conversely, for any integer path q with downward steps at most one, defining delta by the displayed identity produces delta_n in Z_{>=0} and makes every scalar telescoping identity automatic.

Thus the scalar residence ledger is exactly the class of integer paths with arbitrary upward jumps and unit-bounded downward jumps. In the bounded-strip/bounded-slack alternative, it is exactly the class of such paths confined to a finite interval.

## Consequences

Every previously derived scalar property in the bounded case follows from this path description alone:

* interval discrepancy is q_b-q_a;
* skip events delta=0 are exactly downward unit steps q_(n+1)=q_n-1;
* residence surplus delta>=2 is exactly an upward step q_(n+1)>q_n;
* bounded q-range bounds skip-run length and upward jump size;
* return blocks have zero total charge;
* extremal return blocks have one-sided prefix sums by choosing an extremal root.

Run 105's arbitrary binary coding is the special case q_n in {0,1}; the freedom is substantially larger. For example, within any finite interval [m,M], one may choose the next q value arbitrarily from {m,...,M} subject only to q_(n+1)>=q_n-1. There is no scalar restriction on upward jumps beyond the ambient strip.

Therefore no contradiction can be obtained by combining only the exact q/delta identity, nonnegativity of residence increments, and boundedness of q: those hypotheses are completely characterized by finite-interval paths with unit-bounded descent, and such paths exist indefinitely (including constant paths and arbitrarily aperiodic paths).

In particular, any future claimed scalar lemma should be checked against this characterization. If it is true for every finite-interval path with downward steps at most one, it adds no Rule-30/FULL information and cannot by itself close the bounded-slack branch. A genuinely new lemma must exclude at least one such abstract path by using survivor-specific COMPLETE-fringe dynamics, or introduce an additional state variable not determined by q alone.

## Research implication

This gives a clean stopping fence for the current scalar-ledger program: its information content is exhausted. The next useful target is not another telescoping/discrepancy consequence. It is an anchored Rule-30 theorem showing that the q-path of an actual FULL finite survivor belongs to a proper subclass of these skip-free-down paths, ideally one incompatible with bounded range.
