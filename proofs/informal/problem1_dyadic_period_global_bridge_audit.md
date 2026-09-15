# Dyadic-period theorem versus the existing global FULL obstruction

Status: `route-audit`; Problem 1 remains OPEN.

## 1. Question

Run 41 proved globally that every finite periodic orbit of `A` has exact period a power of two. The natural next question was whether this newly constrains the older FULL/common-origin/finite-entry argument enough to prevent an infinite survivor from escaping through changing periods.

It does not, by itself. The relevant dyadic structure was already present in the stronger transition theorem on the actual scan orbit.

## 2. Exact comparison with the existing scan theorem

For the fixed original finite-entry input and its attached finite right fringe, write `W_m` for the common-origin states and `p_m` for the least eventual temporal periods of `Theta(W_m)`. Section 1 of `problem1_scan_doubling_cycle_lag.md` already proves

    p_m -> infinity.

Section 2 of `problem1_inverse_scan_reset_language.md`, as imported there, already proves at every transition

    p_(m+1) in {p_m, 2 p_m}.

Consequently

    p_m = p_0 2^(d_m),

where `d_m` is the number of doubling transitions before depth `m`, and `d_m -> infinity`.

Thus the run-41 theorem does not reduce the set of period transitions available to the particular FULL candidate: the old reset theorem had already restricted those transitions to preservation or doubling. In particular, replacing the old clock-growth argument by the global statement "all finite cycle periods are dyadic" gives no new contradiction.

This is useful as a continuation fence: **period arithmetic alone is exhausted on this route.** A proof still has to control the spatial/common-origin cost of the infinitely many required doublings, not merely show that the periods are powers of two.

## 3. What is genuinely stronger in run 41

The run-41 theorem is still a global classification of arbitrary finite `A`-cycles, whereas the reset theorem is a transition statement for the scan construction. It closes the finite-period spectrum question independently of FULL and is reusable elsewhere.

But for Problem 1's present bottleneck, the stronger applicable fact is still the old one:

    infinitely many actual doubling indices on one fixed common-origin realization.

Moreover `problem1_scan_doubling_cycle_lag.md` already charges every such doubling to a late source diagonal under FULL, while `problem1_bounded_lag_doubling_controls.md` shows that large source period alone cannot force a large local preperiod/lag: there are arbitrarily large doubling-source periods with source/successor preperiods uniformly bounded by 4/2 under the tested local hypotheses.

Therefore the hoped-for implication

    large dyadic period => large local lag/resource cost

is unavailable without an additional global hypothesis.

## 4. Sharpened remaining blocker

The unresolved statement can now be phrased without any period-spectrum ambiguity.

For one fixed FULL finite-entry realization there must be infinitely many indices `m` with

    p_(m+1) = 2 p_m.

Each is already known to be a late diagonal. What is missing is a quantity attached to the **same original finite input/common-origin future** that:

1. has finite total budget under finite entry; and
2. incurs a positive, non-reusable charge at every (or sufficiently many) actual doubling indices.

The bounded-lag construction rules out using only source period plus the local source/successor preperiods as that charge. The earlier spacing theorem also permits arbitrarily sparse infinite sources, so density/spacing alone is insufficient.

A productive next theorem must therefore use cross-doubling dependence: for example, prove that two or more doubling passages on the same original FULL realization cannot reuse the same finite-entry defect/birth resource, or identify a monotone common-origin quantity transported between consecutive doubling indices.

## 5. Secondary route

The primitive terminating-cylinder odd-parity lemma from runs 39-40 remains worthwhile because it would prove uniqueness of the periodic orbit at each bitlength. However, even that stronger uniqueness theorem would not automatically close the global FULL contradiction: the relevant scan periods may still double indefinitely as widths grow. Any attempt to use uniqueness globally should first exhibit the additional common-origin resource that uniqueness makes monotone.

## Conclusion

Run 41 is a valid global theorem, but it does **not** supply the missing global bridge. The precise live obstruction is no longer period arithmetic. It is non-reusable accounting across infinitely many actual period doublings on one fixed FULL finite-entry realization.
