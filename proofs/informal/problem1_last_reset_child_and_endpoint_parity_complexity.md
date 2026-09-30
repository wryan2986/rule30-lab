# Problem 1: last-reset child formula and endpoint-parity complexity at the 8 -> 16 portal scale

Status: exact algebraic lemma plus exhaustive finite census/no-go. Problem 1 remains OPEN.

## 1. Exact recurrent child from the last reset

Write a cyclic parent temporal word as

    e_s = b_s + 2 c_s,

and let the low plane of a one-bit child be `a). The established recurrence is

    a_(s+1) = c_s XOR (b_s OR a_s).                  (1)

Assume `b` is not the zero word, so the recurrent child is unique.

Choose a linear phase cut `0,...,n-1` and let

    r = max{s : b_s = 1}.

At phase `r), (1) resets independently of the incoming child bit:

    a_(r+1) = 1 XOR c_r.                              (2)

By definition of `r`, every later phase before the cut has `b_s=0`. Hence

    a_(s+1) = a_s XOR c_s,   r < s < n.              (3)

Iterating (2)-(3) to the cyclic boundary gives

    a_n = 1 XOR XOR_(s=r..n-1) c_s.

Recurrent cyclicity requires `a_n=a_0`. Therefore the recurrent initial child bit is

    boxed: a_0 = 1 XOR XOR_(s=r..n-1) c_s.           (4)

Once (4) is known, one forward pass of (1) determines the entire child word.

More invariantly, if `r(t)` is the last reset phase `b_r=1` encountered before phase `t` in cyclic order, then

    boxed: a_t = 1 XOR XOR_(s in [r(t),t)) c_s.       (5)

Thus the low plane `b` only partitions the temporal circle into reset gaps; inside each gap, the child is the complemented prefix XOR of `c`.

This is the cyclic phase-selection counterpart of the already-settled reset-gap formula. Its practical use is that the recurrent child does not require trying both seeds `a_0=0,1`.

## 2. Exact finite verification

The checker exhaustively compares (4) against the original two-seed cyclic solver for every

    1 <= n <= 8,
    b != 0,
    c arbitrary.

That is exactly

    86,870

parent-plane pairs. Every case agrees.

For a packed period-32 connector, (4) can be evaluated from the highest reset bit of `b` plus one suffix parity of `c`, after which the existing byte transducer needs only the recurrent seed.

## 3. Exhaustive endpoint parity on every antiperiodic 8 -> 16 portal

The current p32 problem asks whether a doubled odd lower-period leaf returns first to an odd terminal target or to an even branching target.

Before fitting statistics to the two known p32 singleton portals, this question can be solved completely one scale lower.

Let `w` range over all odd-parity 8-bit words. Repeat it to `ww`, integrate

    D(x) = ww

with the canonical integration constant `x_0=0`, and follow the exact period-16 boundary connector from `(x,0)` to its first zero low plane. Let

    f_8(w) = parity(first returned zero target).

There are 128 odd words. Exact exhaustion gives

    odd returned targets  = 56,
    even returned targets = 72,

and the largest first-return depth in this census is

    214,005.

So singleton-versus-branching behavior is already genuinely mixed at the 8 -> 16 antiperiodic portal scale.

## 4. No low-degree cyclic orbit-sum classifier

For a subset `A subset Z/8Z`, define the cyclic monomial orbit sum

    M_A(w) = XOR_i  product_(a in A) w_(i+a).

These are the natural translation/phase-invariant Boolean monomials on the lower-period word.

The checker performs exact GF(2) Gaussian elimination on the 128 odd words, allowing an arbitrary constant plus arbitrary linear combinations of all distinct cyclic orbit sums with `|A| <= d`.

Result:

    d <= 6 : no formula agrees with f_8 on all 128 odd words;
    d <= 7 : a formula exists.

One exact degree-7 formula, in the repository's bit-0-first orientation, is

    f_8 =
      M_{0,2}
    + M_{0,1,2}
    + M_{0,1,6}
    + M_{0,1,2,3}
    + M_{0,1,2,6}
    + M_{0,1,2,3,6}
    + M_{0,1,2,3,4,5,6}                 (mod 2).     (6)

The checker verifies (6) on all 128 odd inputs.

This is a scoped no-go: it does NOT say that no useful endpoint statistic exists. It says that even at lower period, the full endpoint-parity map is not represented by any cyclic monomial-orbit polynomial of degree at most six.

## 5. The degree-7 lower-scale classifier does not renormalize unchanged

A tempting next step would be to reuse the same relative-offset formula (6) modulo 16 on the p16 leaf word and hope it predicts p32 first-return parity.

The two exact p32 singleton certificates already refute that scale-invariant rule.

For portal 5,

    p16 leaf = 0000100100100101,
    scaled (6) prediction = 1,
    actual p32 return parity = 1.

But for portal 13,

    p16 leaf = 0001001111001111,
    scaled (6) prediction = 0,
    actual p32 return parity = 1.

Therefore the exact p=8 classifier is not an all-scale static leaf formula.

## 6. Research consequence

Two routes are now fenced off:

1. do not spend further effort on two-seed cyclic child solving when the low plane is nonzero; use the exact last-reset seed (4);
2. do not expect a low-degree cyclic Boolean statistic of the lower leaf alone, or the literal p=8 degree-7 classifier, to decide p32 singleton versus branching behavior.

A viable p -> 2p endpoint-parity theorem must retain additional connector/half-period state or exhibit a genuine scale-dependent renormalization. The most concrete next target is to use (5) to build a multi-step reset-gap transducer that advances several spatial lifts while preserving enough half-period auxiliary data to decide the parity of the first diagonal endpoint.

Checker:

`experiments/problem1_nonperiodicity/check_last_reset_and_p16_endpoint_parity.cpp`.

Atomic record:

`results/problem1/20260929_last_reset_and_p16_endpoint_parity.json`.

Dependencies:
`problem1_periodic_one_bit_lift_classifier.md`;
`problem1_period32_billion_portal_census.md`.
