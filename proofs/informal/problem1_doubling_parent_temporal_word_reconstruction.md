# Problem 1: reconstructing a doubling parent from one protected temporal word

Status: `partial-proof`. This continues `problem1_doubling_parent_trace_elimination.md` and removes another degree of freedom from the parent-only doubling certificate.

## Setup

Let `u_s=A^s u` be a finite exact-period-`p` parent cycle eligible for a genuine one-bit doubling. Write its temporal spatial columns

    q_i(s) = bit_i(u_s),     s in Z/pZ.

Run 51 proved that genuine doubling is equivalent to

    q_0(s)=0 for every s,
    xor_(s=0..p-1) q_1(s)=1.                         (1)

The key observation here is that once `q_0=0`, the entire parent cycle is determined by the single protected temporal word `q_1`.

## Exact column reconstruction

From

    (Ax)_i = x_(i+2) xor (x_(i+1) OR x_i),

we have along any orbit

    q_i(s+1)=q_(i+2)(s) xor (q_(i+1)(s) OR q_i(s)).

Therefore

    boxed: q_(i+2)(s)=q_i(s+1) xor (q_(i+1)(s) OR q_i(s)).   (2)

Thus `q_0` and `q_1` determine `q_2,q_3,...` recursively as temporal words on `Z/pZ`.

For an eligible doubling parent, put

    c(s)=q_1(s),  q_0=0.

Then (2) gives immediately

    q_2(s)=c(s),
    q_3(s)=c(s+1) xor c(s),

and every higher spatial column is a deterministic Boolean expression in cyclic shifts of `c`.

Hence there is at most one period-`p` parent spacetime cycle associated with a chosen word `c` satisfying (1).

## Finite-support criterion

Because `u_s` is finite for every phase, its spatial columns are eventually zero. Conversely, if the recursion (2) starting from

    q_0=0, q_1=c

reaches two consecutive zero columns, all subsequent columns are zero, and the resulting rows define a finite orbit satisfying the Rule-30 accelerated recurrence.

So eligible finite doubling parents are equivalent to cyclic binary words `c` such that

1. `xor_s c(s)=1`;
2. the column recursion (2), initialized by `(0,c)`, eventually reaches `(0,0)`;
3. the resulting row orbit has exact period `p` (rather than a proper divisor).

The third condition is automatic if `c` itself has exact temporal period `p`, because `c=q_1` is a coordinate of the row orbit.

This converts the local doubling-parent problem into a finite combinatorial termination problem for one odd-parity cyclic word.

## Why this is useful globally

Run 51 removed the forced low fiber from the certificate. The present reduction shows that even the two protected traces `b,c` are not independent: the required all-zero `b=q_0` trace forces the entire finite parent from `c=q_1` alone.

For a genuine projection of the common-origin survivor, `c(s)` is literally a temporal column of that original spacetime diagram. Therefore a late genuine doubling does not merely provide one odd-parity witness. It asserts that one protected column segment is an odd-parity cyclic word whose induced spatial reconstruction terminates.

This is a much more rigid target for the common-origin argument than scalar boundary occupancy.

## Immediate structural identities

Because `q_2=c`, every eligible parent satisfies

    bit_1(u_s)=bit_2(u_s) for every phase s.             (3)

This also follows directly from `q_0(s)=q_0(s+1)=0` in the Rule-30 recurrence at coordinate 0.

The next column is the cyclic discrete derivative

    q_3(s)=c(s+1) xor c(s).                              (4)

In particular `q_3` always has even parity. More generally, parity constraints on later reconstructed columns may expose an invariant incompatible with termination for large dyadic `p`, or classify exactly which odd words terminate.

## Small exact sanity check

Direct enumeration of finite states below `2^16` found the following cycles whose `q_0` trace is identically zero:

- `0`, period 1, with even `c` parity: not a doubling parent;
- `6`, period 1, with odd `c` parity: eligible;
- `(200,222)`, period 2, with odd `c` parity: eligible.

This computation is only a sanity check and is not used as proof.

## Refined next target

Study the word recursion

    q_(i+2)=S q_i xor (q_(i+1) OR q_i),
    q_0=0, q_1=c,

on odd-parity words of dyadic length `p`.

Two outcomes would both be useful:

- a classification/obstruction showing that terminating odd words have a rigid nested form, which could constrain infinitely many common-origin doublings; or
- a large family of terminating odd words, which would rule out trying to derive the global contradiction from parent-cycle combinatorics alone and redirect effort to common-origin compatibility between successive words.

Do not return to transporting the forced low fiber: runs 50--51 already eliminated that obstruction algebraically.