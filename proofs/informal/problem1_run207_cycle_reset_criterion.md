# Problem 1 run 207 — cycle reset criterion for adjacent tower increments

This is a corollary of `problem1_run207_exact_adjacent_tower_defect_automaton.md`.

Let q have A-preperiod a=tau(q), and let r_k=A^k(q). Write

    A^k(2q)=2r_k XOR d_k.

The exact defect recurrence is driven by the low pair of r_k:

    00: d'=d
    01: d'=1 XOR d
    10: d'=1
    11: d'=0.

From time a onward, r_k is periodic. Thus its low-two-bit driver word is periodic.

## Reset dichotomy

If the eventual driver cycle contains no symbol with r_0=1, then it consists only of 00 and 01. Every driver action is bijective on the one-bit state d (identity or toggle). Therefore d is periodic from time a (with period dividing P or 2P if P is a period of r), and consequently

    tau(2q) <= a.

So a strict adjacent-tower increase tau(2q)>tau(q) is impossible in this case.

If the eventual driver cycle does contain r_0=1, then the first subsequent 10 or 11 symbol is a reset: its action is constant (respectively 1 or 0), independent of the incoming d. From the output of that reset onward, the defect is on the unique periodic response to the periodic driver. Hence

    tau(2q) <= a + h,

where h is at most one driver period and is the number of steps from cycle entry until the first reset has been applied.

More precisely, there is a unique periodic defect phase at time a. If d_a already equals that phase, then the upper trajectory is periodic from a. If d_a differs, the intervening 00/01 maps are bijections, so the mismatch cannot disappear before the first reset; at that reset it disappears exactly. Therefore, modulo the possibility that the upper trajectory happened to enter a cycle before time a,

    tau(2q)>a

is equivalent to a mismatch between d_a and the unique periodic defect phase, and the excess transient ends exactly at the first reset.

For the shift tower a_n=tau(2^n x), this gives a concrete necessary condition for every positive increment a_n>a_{n-1}: the eventual A-cycle at level n-1 must contain a low bit 1, and the accumulated defect bit at cycle entry must be out of phase with the unique reset-selected periodic response.

This reduces the increment problem to two finite pieces of complete-cycle data at the lower level: (1) the cyclic low-two-bit driver word and (2) the defect phase d at first cycle entry. It is substantially sharper than the run-206 first-defect condition.

## Remaining global gap

The FULL contradiction still requires showing that the stronger renewal events

    a_n > max(a_{n-1}, b+n)

cannot occur infinitely often for a fixed finite x. The reset criterion does not yet bound how often the cycle-entry phase mismatch can recur as n increases. The next useful target is therefore a relation between the defect phase for q=2^(n-1)x and the complete code/phase of the next shift-tower level, rather than additional local Rule-30 propagation.
