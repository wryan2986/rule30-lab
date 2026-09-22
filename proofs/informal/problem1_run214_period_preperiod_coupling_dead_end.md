# Problem 1 — run 214: period/preperiod coupling does not by itself control residence surplus

## Status

Problem 1 remains OPEN.

Run 213 suggested coupling the exact adjacent-level period law with the exact preperiod/reset-gap law. This note records a concrete obstruction to obtaining the needed amortized bound from those two laws alone.

## Exact logical separation

For q_n = 2^n x, write

- a_n = tau(q_n) for eventual-cycle entry time,
- P_n = pi(q_n) for minimal eventual period,
- delta_n = a_n-a_{n-1}.

Runs 208–210 show that delta_n>0 occurs exactly when the lifted one-bit defect is out of phase at lower cycle entry; then delta_n=rho_n, the distance to the first reset on the lower eventual cycle.

Run 213 shows that P_n=2P_{n-1} is possible only when the lower eventual cycle has no reset anywhere. Therefore every positive preperiod increment automatically occurs at a period-preserving level:

    delta_n > 0  ==>  P_n = P_{n-1}.

This implication is exact, but it has no converse strong enough to charge positive delta_n against period growth. A period-preserving level can be matched (delta_n=0) or mismatched (delta_n=rho_n>0), and the period law supplies no budget on how many mismatched period-preserving levels may occur.

## Bounded diagnostic: x=1

To test whether a hidden empirical amortization might nevertheless be present, I performed exact orbit detection for q_n=2^n through n=300 using the reviewed scan map

    A(q) = (q >> 2) XOR ((q >> 1) OR q).

The eventual period reaches 8 at n=29 and remains 8 through every tested level n<=300. Nevertheless the preperiod continues to acquire many positive increments. At n=300,

    tau(2^300) = 389,
    pi(2^300) = 8,
    tau(2^300)-300 = 89.

Late positive increments occur repeatedly; for example among n=272..300 there are positive increments at

    272,273,274,276,277,278,280,282,283,284,285,286,287,288,289,290,295,298,299,300.

The residence surplus a_n-n reaches at least 95 in this tested range (at n=290), despite no period increase after n=29.

These are finite computational observations, not an asymptotic theorem. They are sufficient, however, to reject the proposed strategy that period growth itself supplies an effective amortized budget for reset-gap gains.

## Consequence

The exact period law remains useful structural information, but coupling only

1. positive delta_n requires a reset, and
2. period doubling requires no reset

cannot control a_n-n. Long stretches of period-preserving levels can continue to contain many mismatched lifts and positive reset-gap gains.

The next argument must constrain the *phase mismatch sequence itself* across common-origin levels, not merely classify whether the lower cycle contains a reset or whether its period doubles.

A more specific target is to derive a recurrence for the cycle-entry defect phase from level n to n+1 (or for the corresponding mismatch indicator) using the exact inverse-system/fiber recurrence from runs 211–212. Any successful amortization must see more than P_n: it must retain enough phase information to distinguish matched from mismatched period-preserving lifts.
