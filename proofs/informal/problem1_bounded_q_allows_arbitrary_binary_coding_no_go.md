# Problem 1: bounded normalized excess can encode an arbitrary binary tail

## Status

No-go refinement for the bounded-slack branch. This does not solve Problem 1. It shows that the scalar residence constraints proved in runs 101--104 do not imply eventual periodicity, finite-state recurrence of the residence word, or any useful low-complexity conclusion.

## Setup

Write

    q_n = tau(2^n v) - n - R,
    delta_n = tau(2^(n+1) v) - tau(2^n v).

Then exactly

    delta_n = 1 + q_(n+1) - q_n.

The bounded-strip/bounded-slack alternative places q in a finite integer interval and hence delta in a finite nonnegative alphabet. Earlier notes derived bounded discrepancy, bounded skip runs, bounded residence jumps, and zero-charge return blocks.

## Arbitrary binary coding

Let x_0,x_1,... be ANY infinite binary sequence. Define the abstract normalized-excess sequence

    q_n = x_n.

Then define

    delta_n = 1 + x_(n+1) - x_n.

Because x_n is binary,

    delta_n in {0,1,2}.

Moreover delta_n is always nonnegative, and telescoping gives

    sum_[a,b) (delta_n - 1) = x_b - x_a.

Thus every interval has signed discrepancy at most 1 in absolute value. A zero increment occurs exactly at a transition 1 -> 0, so consecutive zero increments cannot occur. A jump 2 occurs exactly at 0 -> 1. Returns to either q-level give exact zero-charge blocks, and extremal return blocks have the one-sided prefix property discussed in runs 103--104.

Yet x can be chosen completely arbitrarily: periodic, aperiodic, Sturmian, normal, or algorithmically complicated. Therefore all scalar consequences established so far are compatible with an arbitrary binary information stream.

The same construction can be shifted by any constant C, q_n=C+x_n, without changing delta. Hence it can be placed inside any bounded vertical strip containing two adjacent integer levels.

## Consequence

One cannot infer eventual periodicity, finite-state behavior, bounded combinatorial complexity, or a contradiction merely from:

* q lying in a finite interval;
* delta lying in a finite residence alphabet;
* uniformly bounded interval discrepancy;
* bounded skip runs and bounded residence jumps;
* recurrent exact zero-charge blocks; or
* the extremal one-sided-prefix ordering.

In particular, the phrase "finite residence alphabet" must not be promoted to "finite-state dynamics." The scalar q/delta ledger has enough capacity to carry an arbitrary binary tail.

Any finite-state or periodicity argument must therefore add an actual Rule-30/FULL state variable whose future is deterministic and whose state space is genuinely finite under the hypothetical bounded strip. The natural candidate would have to be anchored to the COMPLETE actual fringe (or an equivalent survivor-specific marker), not manufactured from q alone. This agrees with the cycle-lemma no-go: the missing information is external to the scalar residence ledger.

This construction is only an abstract countermodel to deductions from the proved scalar identities; it does not claim that every binary x is realizable by a Rule-30 survivor.

Problem 1 remains OPEN.
