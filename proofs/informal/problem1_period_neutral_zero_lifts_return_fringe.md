# Problem 1: period-neutral zero lifts are exactly the leading-zero gap of one return fringe

## Status

Problem 1 remains open. This note exactly classifies the period-neutral part of a literal zero-extension run over an `A`-periodic state. It sharpens the previous bound `Q <= 2p+1` and replaces the vague notion of a long period-neutral plateau by one explicit finite return-fringe word.

Dependencies:

- `A = sigma^2 T` and `T(2^q x)=2^q T(x)`;
- `T` preserves the 2-adic valuation of every nonzero state;
- the one-bit period theorem `p' in {p,2p}`;
- `problem1_period_doubling_forces_next_exit.md`.

## 1. The p-step return fringe

Let `z>0` be periodic under `A` with exact period `p`:

    A^p(z)=z.

Since

    A^p(z)=sigma^(2p) T^p(z),

there is a unique integer `R=R_p(z)` such that

    T^p(z)=2^(2p) z + R,
    0 <= R < 2^(2p).                                (1)

Call `R` the p-step return fringe.

In fact `R` is nonzero. If `R=0`, then

    T^p(z)=2^(2p)z,

but the left side has the same 2-adic valuation as `z`, while the right side has valuation `v_2(z)+2p`, impossible for `z>0` and `p>=1`.

Therefore

    1 <= R < 2^(2p).                                (2)

Let

    L = bit_length(R),

so

    1 <= L <= 2p.                                   (3)

Geometrically, `R` is exactly the finite right fringe discarded by the `2p` shifts in the return `A^p(z)=z`.

## 2. Exact p-step action on every zero extension

For `0 <= q <= 2p`, use `T^p(2^q z)=2^q T^p(z)` and (1):

    A^p(2^q z)
      = sigma^(2p) (2^q T^p(z))
      = floor(2^q T^p(z) / 2^(2p))
      = 2^q z + floor(2^q R / 2^(2p))
      = 2^q z + floor(R / 2^(2p-q)).                (4)

Define

    c_q = floor(R / 2^(2p-q)).                       (5)

Then exactly

    A^p(2^q z)=2^q z+c_q.                            (6)

Thus the question whether the q-th zero extension is still on a period-p cycle is completely determined by the top `q` bits of the single `2p`-bit return fringe `R`.

## 3. Exact neutral-depth threshold

The state `2^q z` is fixed by `A^p` iff `c_q=0`, i.e.

    R < 2^(2p-q).                                    (7)

Since `L=bit_length(R)`, this is equivalent to

    L <= 2p-q,

or

    q <= 2p-L.                                       (8)

Whenever (8) holds, the exact period of `2^q z` is not merely a divisor of `p`: it is exactly `p`. Indeed deletion of the `q` added low bits factors its orbit onto `z`, whose exact period is `p`; a smaller lifted period would force a smaller period for `z`.

Therefore:

> **Neutral-prefix theorem.** If `z` has exact period `p` and `L=bit_length(R_p(z))`, then the zero extensions
>
>     z, 2z, ..., 2^(2p-L) z
>
> all have exact period `p`, and `2^(2p-L+1)z` does not have period `p`.

The number of period-neutral lift steps after `z` is exactly

    2p-L.                                            (9)

So a long period-neutral run is equivalent to a return fringe whose binary support occupies unusually few of the available `2p` discarded cells.

## 4. The first non-neutral lift has an exact phase defect of +1

Set

    q_* = 2p-L+1.                                    (10)

This is the first zero-extension depth at which period `p` fails. Since the highest bit of `R` is exactly at position `L-1`,

    floor(R / 2^(L-1)) = 1.                          (11)

But `2p-q_*=L-1`, so (4) gives the particularly sharp identity

    A^p(2^(q_*) z)=2^(q_*) z + 1.                    (12)

Thus the first failure of period neutrality is never an arbitrary phase error: after exactly one base period it is the adjacent `+1` lift.

Now apply the existing one-bit period theorem to the transition from the last neutral state `2^(q_*-1)z` (exact period `p`) to its zero lift `2^(q_*)z`.

Because (12) rules out period `p`, only two possibilities remain:

1. `2^(q_*)z` is nonperiodic; or
2. it is periodic with exact period `2p`.

In case 2, `problem1_period_doubling_forces_next_exit.md` implies that the following zero lift `2^(q_*+1)z` is necessarily nonperiodic.

Hence the first nonperiodic depth `Q` of the literal zero-extension chain is exactly one of

    Q = q_*      = 2p-L+1,                           (13a)

or

    Q = q_*+1    = 2p-L+2,                           (13b)

where the second case occurs precisely when the first non-neutral zero lift doubles the period.

This refines the previous universal estimate `Q<=2p+1` to an exact two-valued formula once the return fringe is known.

## 5. Canonical example z=25

For the period-two state `z=25`, direct exact evolution gives

    T^2(25)=401=16*25+1.

Thus

    p=2,
    R=1,
    L=1.

The neutral-depth threshold is

    2p-L=3.

Accordingly

    25, 50, 100, 200

all have exact period `2`.

The first non-neutral depth is

    q_*=4,

and (12) gives

    A^2(400)=401=400+1.

This state is periodic of exact period `4`, so it is the doubling branch. The next zero lift `800` is nonperiodic. Therefore

    Q=5=2p-L+2,

matching the earlier sharp example exactly.

## 6. Additional valuation refinement

Let `a=v_2(z)`. Since `T^p(z)` has valuation `a`, while `2^(2p)z` has valuation `a+2p`, equation (1) implies

    v_2(R)=a.                                        (14)

Therefore

    L >= a+1.                                        (15)

Consequently the exact formula above yields

    Q <= 2p-a+1,                                     (16)

with the no-doubling branch satisfying

    Q <= 2p-a.                                       (17)

For physical-row origins `z=T^H(v)`, the valuation is invariant under `T`, so `a=v_2(v)` is fixed across all such restarts. This is only a mild improvement when `v` is odd, but it shows that the return-fringe formulation retains information invisible in the earlier pure period bound.

## 7. Research consequence

The handoff's proposed classification of period-neutral skips is now exact.

A long negative post-threshold plateau cannot consist of mysterious repeated recurrent phases. If its starting periodic physical row has period `p`, then its neutral zero lifts are exactly the leading-zero gap of the `2p`-cell return fringe

    R_p(z)=T^p(z)-2^(2p)z.

The next obstruction should therefore be phrased geometrically:

> Can FULL/common-origin structure prevent the return fringe `R_p(T^H(v))` from having arbitrarily large leading-zero gaps relative to `2p` while the excess `h_n-n` stays bounded above?

Equivalently, one wants a lower bound on `bit_length(R_p(z))` for the periodic physical rows arising along the actual Rule-30 orbit, or a repayment theorem when that bit length is small.

This is more specific than attempting to bound period-neutral skips directly, and it preserves the persistent period potential from the previous run.