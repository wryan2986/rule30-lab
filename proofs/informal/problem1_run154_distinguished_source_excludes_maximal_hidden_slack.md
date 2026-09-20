# Distinguished source excludes maximal hidden slack

Status: `partial-proof`. Problem 1 remains open.

## Setup

Use the established TWO-BIT nonreset passage at time `t`, and put

    q=t+2.

Run153 writes the terminal hidden slack as

    g=g_(t+5) in {0,1,2,3}

and proves that the final original-cut jump is

    d_5=s_(t+6)-s_(t+5)=g+2.

The global discrepancy-front residence formula says that characteristic

    j=t+6

is resident for exactly

    [s_(t+5),s_(t+6))

and its shared left-neighbor trace is zero at every nonfinal residence time, followed by the final erasing `1`.

Because `e_(t+5)=-g`,

    s_(t+5)=t+5-g,
    s_(t+6)=t+7.

Therefore the residence forces the diagonal zero string

    r_g(t+5-g)=0,
    r_(g-1)(t+6-g)=0,
    ...,
    r_0(t+5)=0,

followed by

    r_-1(t+6)=1.                                  (1)

This is an exact consequence of the one global front, not a new local-driver assumption.

## Compare with the distinguished cyclic source

At `q=t+2`, the established distinguished source motif is

    (r_-5,...,r_2)(q)=10101110.

Write, as in runs144--146,

    a=r_3(q).

If `g=3`, the first zero in (1) occurs at

    (position,time)=(3,t+2)=(3,q),

so the residence requires

    a=0.                                           (2)

But the next zero in the same residence occurs at

    (position,time)=(2,t+3)=(2,q+1).

Rule30 gives, using `r_1(q)=1`, `r_2(q)=0`, and `r_3(q)=a`,

    r_2(q+1)
      = r_1(q) XOR (r_2(q) OR r_3(q))
      = 1 XOR a
      = NOT a.

The residence requires this cell to be zero, hence

    a=1,                                           (3)

contradicting (2). Therefore

    g_(t+5) != 3,
    g_(t+5) <= 2.                                  (4)

Combining with run153,

    s_(t+6)-s_(t+5)=g+2 <= 4.                     (5)

Thus the complete Rule30 geometry improves the scalar-ledger terminal jump set from `{2,3,4,5}` to

    {2,3,4}.

## Additional local implication

The same calculation shows that any `g>=2` forces `a=1`. In fact the next required zero, `r_1(q+2)=0`, is also automatic when `a=1` and is independent of `b=r_4(q)`; direct two-step Rule30 evaluation from the distinguished motif gives

    r_1(q+2)=NOT a.

Hence the presently known local geometry does not exclude `g=2`: for `a=1`, the residence-required zeros at `(2,q+1)` and `(1,q+2)` agree with the distinguished source evolution. This is a useful stopping point for this immediate two-cell argument.

## Interpretation

Run153 showed that scalar monotonicity alone permits maximal hidden slack `g=3`, corresponding to a cut jump of five. The global residence trace plus the rigid distinguished source rules that case out exactly. This is the first improvement of the hidden-slack bound using complete spacetime geometry rather than only the physical delay profile.

The next target is to distinguish `g=2` from `g<=1`. Since the two nearest residence zeros are compatible when `a=1`, doing so requires an additional cyclic/gate/global-shadow condition beyond the rigid source motif itself; extending the same two-cell Rule30 calculation cannot suffice.

Dependencies: `problem1_run153_zero_plateau_slack_exact_repayment.md`; `problem1_global_discrepancy_front.md`; `problem1_full_trace_couples_distinguished_right_pair_to_far_left_bits.md`; `problem1_nonreset_return_birth_spacing.md`.
