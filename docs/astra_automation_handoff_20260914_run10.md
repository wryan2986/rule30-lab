# Astra automation handoff — run 10

Problem 1 remains **OPEN**.

This run starts from branch head `699c04d3561d039d60348169b694599e8d1a210a` and adds `proofs/informal/problem1_skip_plateau_common_origin_threshold.md`.

## New exact result

Let

    h_n = tau(2^n v).

Suppose a height-`H` tower plateau begins at index `n`, so `h_n=H`. Transient stripping gives

    x_m=A^H(2^(n+m)v),
    h_(n+m)=H+tau(x_m).

Writing

    w=T^H(v),

one has exactly

    x_m=sigma^(2H)(2^(n+m)w).

Hence

    x_m=sigma^(2H-n-m)w    if n+m<=2H,
    x_m=2^(n+m-2H)w        if n+m>=2H.

At the absolute tower depth `2H`, the stripped state is exactly the physical row

    x_(2H-n)=T^H(v).

Beyond that point, the stripped plateau is not a generic nested-lift chain at all. It is the literal zero-extension tower

    w, 2w, 4w, ...

of `w=T^H(v)`.

For a genuine noninitial plateau entry, the hidden-slack causal bound from run 9 gives

    H >= ceil((n+1)/2),

so

    n <= 2H-1.

Thus every genuine plateau begins before its common-origin threshold. It either exits before `2H`, or it reaches the threshold and thereafter is controlled by zero-extensions of `T^H(v)`.

## Exact post-threshold scalar

If the plateau reaches `2H`, define

    Q_H=min{q>=0 : tau(2^q T^H(v))>0}.

Then `Q_H>=1` and is finite. For `0<=q<Q_H`,

    h_(2H+q)=H,

while

    h_(2H+Q_H)=H+d_H,
    d_H=tau(2^Q_H T^H(v)).

Applying the run-9 causal rise bound at the exit index `2H+Q_H` yields

    d_H >= ceil((Q_H+1)/2).

So a post-threshold periodic prefix of length `Q_H` forces an exit residence recovering at least half its depth.

## Important limitation / dead route

This is not enough for the target

    limsup (h_n-n)=infinity.

Across the post-threshold segment,

    e_v(2H+Q_H)-e_v(2H)=d_H-Q_H,

and the proved lower bound can still be approximately `-Q_H/2`. The present all-depth constraints therefore remain compatible with schematic growth `h_n~n/2`, which would make `e_v(n)->-infinity`.

So the common-origin threshold by itself does not close Problem 1, and merely combining it with the radius-one causal bound cannot do so.

## Preferred next target

Study

    Q_H=min{q : tau(2^q T^H(v))>0}

for the special physical rows reached at plateau heights. A successful theorem needs extra FULL/global-front information to do one of:

1. bound `Q_H` much more strongly than the light-cone estimate;
2. force `d_H` to repay essentially all of `Q_H` (coefficient 1 rather than 1/2), with recurrent positive surplus; or
3. couple successive plateau exits so that half-depth deficits cannot repeat indefinitely.

Do not treat arbitrary nested periodic lifts as valid models beyond absolute tower depth `2H`; past that threshold the states are literal zero-extensions of `T^H(v)`.

New proof commit before this handoff: `f55a21daabfd9c8f7c50f27522ff6a490db0328e`.
