# Exact ledger for maximal consecutive-skip blocks

Status: `partial-proof`. This note derives the exact charge of a maximal block of consecutive skipped characteristics after transient stripping. It also gives an explicit finite counterexample showing that arbitrary nested periodic lifts can sustain a long negative block charge, so no universal block-compensation theorem can hold without additional structure from the common zero-extension tower / FULL tail.

## 0. Setup

Use the zero-extension tower notation

    h_n = tau(2^n v),
    delta_n = h_(n+1)-h_n >= 0.

Fix an index n and write

    y = 2^n v,
    H = tau(y),
    x_m = A^H(2^m y).

The transient-stripping theorem gives, for every relevant m,

    h_(n+m) = H + tau(x_m).                          (1)

In particular

    delta_(n+j) = tau(x_(j+1)) - tau(x_j).          (2)

Also x_0 is A-periodic and the x_m form nested one-bit lifts:

    sigma(x_(m+1)) = x_m.                            (3)

## 1. Exact block ledger

Suppose n begins a maximal block of k >= 1 consecutive skips. Equivalently,

    delta_n = ... = delta_(n+k-1) = 0,
    delta_(n+k) > 0.                                 (4)

By (2) and tau(x_0)=0, this is exactly

    tau(x_0)=tau(x_1)=...=tau(x_k)=0,
    tau(x_(k+1))>0.                                  (5)

Thus x_0,...,x_k are periodic nested one-bit lifts and x_(k+1) is the first nonperiodic lift.

The residence-ledger contribution of the entire skip block together with its exit residence is

    B = sum_(j=0)^k (delta_(n+j)-1).

Telescoping (2) gives exactly

    B = tau(x_(k+1)) - tau(x_0) - (k+1)
      = tau(x_(k+1)) - (k+1).                        (6)

So the whole block is controlled by one scalar: the exit preperiod.

This identity is exact and does not require any estimate or asymptotic sampling.

## 2. The one-bit classifier makes the block charge explicit

Because x_k is periodic and x_(k+1) is a one-bit lift of x_k, apply the exact periodic one-bit lift classifier.

Let

    q_k = min{s>=0 : bit_0(A^s(x_k))=1}.             (7)

The low trace of x_k cannot be identically zero: if it were, both one-bit lifts of x_k would be periodic, contradicting the maximality condition tau(x_(k+1))>0.

Likewise the actual exit bit is necessarily the nonrecurrent lift bit, because the recurrent bit would make x_(k+1) periodic. Therefore the classifier gives exactly

    tau(x_(k+1)) = q_k + 1.                          (8)

Substituting into (6),

    B = q_k - k.                                     (9)

Hence a maximal block of k consecutive skips is fully compensated by its exit if and only if

    q_k >= k.                                        (10)

It has positive net surplus iff q_k>k, zero net charge iff q_k=k, and remains negatively charged iff q_k<k.

This is a sharper target than trying to lower-bound the exit preperiod abstractly: the required theorem is specifically a lower bound on the **first eraser time of the terminal periodic core** relative to the number of recurrent periodic lifts that preceded it.

## 3. Universal block compensation is false for arbitrary nested lifts

The inequality q_k>=k is false for arbitrary nested periodic lifts. There are long periodic-lift chains whose terminal periodic core begins with an eraser immediately, so q_k=0, and whose first nonperiodic child has preperiod 1.

An exact example is

    x_0 = 1,
    x_1 = 3,
    x_2 = 6,
    x_3 = 13,
    x_4 = 27,
    x_5 = 55,
    x_6 = 111,
    x_7 = 223.

Each state is a one-bit lift of the previous one:

    x_(m+1) = 2 x_m + a_m

with exposed bits

    1,0,1,1,1,1,1.

Direct Rule-30 iteration gives

    1   -> 1,
    3   -> 3,
    6   -> 6,
    13  -> 12 -> 13,
    27  -> 25 -> 27,
    55  -> 50 -> 55,
    111 -> 100 -> 111,

so x_0,...,x_6 are periodic. But

    223 -> 200 -> 222 -> 200 -> 222 -> ...,

hence

    tau(223)=1.                                      (11)

Thus this is a block with

    k=6,
    q_k=0,
    B=q_k-k=-6.                                      (12)

The example is not evidence about the actual zero-extension tower asymptotics. Its role is logical: it disproves any proposed theorem asserting that nested periodic lifts alone force the exit to repay the preceding skips.

## 4. Consequence for the remaining proof strategy

The block route survives only if one uses extra structure that distinguishes the actual tower states

    x_m = A^H(2^m y)

from arbitrary nested lifts.

For a maximal tower skip block, the exact target is now:

> Prove that the common-origin phase constraints force the terminal first-eraser time q_k to dominate k often enough that the global sum of charges q_k-k has unbounded positive excursions.

A stronger local statement q_k>=k for every maximal tower block would suffice, but the arbitrary-lift counterexample shows it cannot come from periodic-lift nesting alone.

Equivalently, since

    x_k = sigma^(2H-k) T^H(y)

whenever k<=2H, q_k is the first time the low bit of this specific shifted post-transient state becomes 1. The next useful work should therefore connect the **length k of recurrent periodic lift selection** to the **time-to-first-eraser q_k** using the shared word T^H(y), or show that cheap blocks force a later compensating event outside the block.

Do not attempt a generic nested-lift compensation lemma: equation (12) is an exact counterexample.

Dependencies: `problem1_shift_tail_residence_ledger.md`; `problem1_transient_stripping_zero_extensions.md`; `problem1_periodic_one_bit_lift_classifier.md`.

No claim of a Problem 1 solution is made here.
