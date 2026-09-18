# Problem 1: extremal return blocks are one-sided excursions

## Status

Exact strengthening of the bounded-slack branch developed in runs 101–102. It does not solve Problem 1, but improves the arbitrary recurrent-level return blocks of run 102 to extremal return blocks whose signed charge has a fixed sign at every internal prefix.

## Setup

As in the bounded-slack case, after deleting a finite prefix assume

    -G <= q_n <= K,
    h_n = n + R + q_n,
    delta_n = h_(n+1)-h_n >= 0.

Hence

    q_(n+1)-q_n = delta_n-1 >= -1.              (1)

Because q is integer-valued in a finite set, define the eventual extremal recurrent levels

    m = liminf q_n,
    M = limsup q_n.

For integer finite-range q, both m and M occur infinitely often, and after a finite prefix

    m <= q_n <= M.                               (2)

## Minimum return blocks

Take successive sufficiently late indices a<b with

    q_a=q_b=m

and no occurrence of m strictly between them. Then for every a<j<b,

    q_j > m.                                     (3)

For every prefix [a,j), telescoping gives

    sum_(n=a..j-1)(delta_n-1) = q_j-q_a = q_j-m >= 0.   (4)

At the endpoint,

    sum_(n=a..b-1)(delta_n-1) = 0.               (5)

Thus every minimum-to-minimum return block is a nonnegative signed-charge excursion: its cumulative long-residence surplus minus skips never becomes negative internally and returns exactly to zero at the end.

If the block is nontrivial in q (equivalently b>a+1, or q leaves m), then its first transition must satisfy

    q_(a+1)>m,

so by integrality and (1)

    delta_a = 1 + q_(a+1)-m >= 2.                (6)

Its final transition returns from q_(b-1)>m to m. Since q can decrease by at most one per step by (1), necessarily

    q_(b-1)=m+1,
    delta_(b-1)=0.                               (7)

Therefore each nontrivial minimum excursion begins with a positive residence-surplus event and ends with a skip. More generally, all compensation for its positive prefix charge is forced to occur without ever driving the cumulative charge below zero.

## Maximum return blocks

Dually, take successive sufficiently late a<b with q_a=q_b=M. Then every internal q_j<M and

    sum_(n=a..j-1)(delta_n-1)=q_j-M <= 0,         (8)

with total block charge zero at b. Thus maximum return blocks are nonpositive signed-charge excursions.

A nontrivial maximum excursion must begin by descending from M. Since downward steps are at most one, its first step is exactly

    q_(a+1)=M-1,
    delta_a=0.                                    (9)

The final return to M may be an upward jump, with

    delta_(b-1)=1+M-q_(b-1) >= 2.                (10)

So the temporal orientation is reversed: a maximum excursion starts with a skip and ends with residence surplus.

## Why this is stronger than run 102

Run 102 used an arbitrary recurrent level c and obtained only exact total balance P[a,b)=Z[a,b). Extremal recurrent levels additionally control every internal prefix of the block. At the eventual minimum, compensation cannot occur before the charge is created strongly enough to make the running balance negative; at the eventual maximum the opposite holds.

This supplies a sharper interface for a FULL/fringe argument. In bounded-slack case B, it is enough to prove that complete-fringe dynamics force, inside infinitely many late minimum-return blocks, a prefix with negative signed charge, or inside infinitely many maximum-return blocks a prefix with positive signed charge. Either event is immediately impossible by (4) or (8). Equivalently, one can target an ordering violation: a FULL episode that necessarily forces a skip before the corresponding residence surplus on a minimum excursion, or surplus before the corresponding skip on a maximum excursion.

This is potentially more useful than proving a nonzero total block charge, because it only requires an ordering theorem rather than preventing exact eventual compensation.

## Limitation

The result is still pure bounded-discrepancy combinatorics. The constant schedule q_n=C has only trivial extremal return blocks, and periodic bounded Łukasiewicz paths can satisfy all identities. A contradiction still requires Rule-30/FULL-specific information from the complete actual fringe. The new target is specifically an ordering theorem for skip/surplus events relative to extremal q-return blocks, not another ambient counting argument.
