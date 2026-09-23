# Astra automation handoff — run 217

Problem 1 remains OPEN.

## Repository state entering run

No intervening work after run 216; branch tip was `2d3847922304fef7a69f047371fef6a0ff1a0e35`.

## New exact result

Run 216 defined

    g_j(k)=d_{j-2}(k) XOR d_{j-3}(k)

and identified a level-j reset gap with a zero run of `g_j`.

Using the run-215 defect recurrence gives the exact update

    g_j(k+1)
      = d_{j-5}(k) XOR d_{j-4}(k)
        XOR (d_{j-3}(k) OR d_{j-2}(k))
        XOR (d_{j-4}(k) OR d_{j-3}(k)).

Inside a gap, `g_j(k)=0`, so `d_{j-3}=d_{j-2}=c`. The continuation law simplifies sharply:

- if the common value is `00`, then

      g_j(k+1)=d_{j-5}(k),

  so the gap survives iff `d_{j-5}(k)=0`;

- if the common value is `11`, then

      g_j(k+1)=d_{j-5}(k) XOR d_{j-4}(k)=g_{j-2}(k),

  so the gap survives iff the next lower adjacent pair also agrees.

Full note:

`proofs/informal/problem1_run217_exact_agreement_gap_recurrence.md`

## Why this matters

Every step of a long reset gap now has an exact lower-level continuation certificate. Common `11` recursively forces agreement two levels lower; common `00` forces a zero in layer `j-5`. This is a genuine ancestry refinement of run 216.

It is not yet an amortized bound because the two certificate types may alternate, and the `00` branch does not itself force an adjacent-pair agreement.

## Next target

Trace these continuation certificates over the full stopping-time interval beginning at `a_{j-1}`. Determine whether the `11` branches force a descending staircase `g_j=g_{j-2}=...=0` that can be charged to tower depth, and whether the `00` branches admit a separate non-telescoping zero-ancestry charge. Do not assume certificate positions are disjoint without proof.
