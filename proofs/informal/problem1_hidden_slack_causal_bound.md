# Hidden slack has a causal half-depth bound at every visited characteristic

Status: `partial-proof`. This is an exact all-depth consequence of the pushed global-front residence identity plus finite propagation of the ORIGINAL actual row. It does not solve Problem 1. It constrains the hidden slack at characteristics actually visited by the global discrepancy front, and identifies skipped characteristics as the remaining place where arbitrarily large slack can accumulate without an immediate causal contradiction.

## 1. Setup

Fix the ORIGINAL nonzero finitely supported actual initial row `r(0)`. Let `R` be the largest physical position with

    r_R(0)=1,

so every initial cell strictly to the right of `R` is zero.

For the original cuts, keep the established notation

    s_j=tau(L_j(r(0))).

The global-front residence theorem says characteristic `j` is actually visited iff

    s_j>s_(j-1).

When it is visited, its final erasing cell is exactly

    r_(j-s_j)(s_j-1)=1.                              (1)

This is equation (7) of `problem1_global_discrepancy_front.md` at the final time of the nonempty residence.

Define the signed front offset and hidden slack by

    q_j=s_j-j,
    g_j=j-s_j=-q_j.

At a zero-delay physical row, `q_j<=0` and `g_j>=0`. The truncation

    tau(Y_j)=max(q_j,0)

forgets `g_j`.

## 2. Finite propagation forces a half-depth inequality

Rule 30 has radius one. Since the ORIGINAL actual row has no nonzero cells to the right of `R`, at every physical time `u>=0`,

    r_i(u)=0 whenever i>R+u.                           (2)

Now let characteristic `j` be visited. Its erasing cell (1) is a `1` at time

    u=s_j-1

and physical position

    i=j-s_j.

Equation (2) therefore requires

    j-s_j <= R+s_j-1.

Equivalently,

    2s_j >= j-R+1,                                    (3)

or

    s_j >= ceil((j-R+1)/2).                           (4)

In hidden-slack form,

    g_j=j-s_j <= R+s_j-1.                             (5)

Thus the front cannot finish a genuinely visited characteristic arbitrarily far to the right of the physical center relative to the elapsed time: the final erasing `1` must still lie inside the forward light cone of the finite ORIGINAL support.

No FULL assumption is needed for (3)-(5).

## 3. Shift-tail form

Let `R` also denote the end of the original right support in the shift-tail reduction, and put

    v=L_R(r(0)),
    h_n=tau(2^n v)=s_(R+n),
    delta_(n-1)=h_n-h_(n-1).

For `n>=1`, the tail characteristic `R+n` is visited exactly when

    delta_(n-1)>0.

Substituting `j=R+n` into (3) cancels the original support location and gives the clean tower statement

    delta_(n-1)>0  =>  2h_n>=n+1.                    (6)

Hence every genuine rise of the zero-extension preperiod satisfies

    h_n >= ceil((n+1)/2).                            (7)

Because the already proved theorem gives `h_n->infinity`, there are infinitely many genuine rises. Therefore there are infinitely many indices `n` satisfying (7).

This is a quantitative statement absent from mere monotone divergence, but it is still far weaker than the desired

    limsup (h_n-n)=infinity.

It only gives `h_n-n >= -(n-1)/2` at rise indices.

## 4. Consequence for maximal skip blocks

Suppose a maximal skip block has

    delta_n=...=delta_(n+k-1)=0

for `k>=1`, and exits with

    d=delta_(n+k)>0.

Then

    h_(n+k)=h_n=:H,
    h_(n+k+1)=H+d.

Applying (7) at the exit index `n+k+1` yields

    H+d >= ceil((n+k+2)/2),

so the exit residence must obey

    d >= ceil((n+k+2)/2)-H.                          (8)

Thus a long run of skipped characteristics cannot exit through an arbitrarily short residence if, by the time of exit, its inherited preperiod `H` lies below half the extension depth. The actual finite row forces a compensatingly long residence simply because the terminal erasing `1` otherwise lies outside the actual row's causal cone.

The exact ledger charge of the `k` skips plus the exit residence is

    B=d-k-1.

Equation (8) therefore gives

    B >= ceil((n+k+2)/2)-H-k-1.                      (9)

This lower bound need not be positive. In particular it does NOT prove generic skip-block compensation and does not contradict the previously recorded arbitrary nested-lift counterexample. It uses common-origin finite-support structure, but only through the causal cone.

## 5. Geometric interpretation of hidden slack

For a visited characteristic, the final front position immediately before erasure is

    m(s_j-1)=j-(s_j-1)=g_j+1.                        (10)

So hidden slack has a direct geometric meaning:

    g_j = (final rightward front displacement before erasure) - 1.

Equation (5) is exactly the statement that this erasing front position cannot outrun the rightmost possible actual `1`, whose position at that time is at most

    R+s_j-1.

This is useful because `g_j` is not merely algebraic information lost by the positive-part map. On visited characteristics it is a physical distance in the one fixed spacetime.

For a skipped characteristic, there is no residence and no final erasing cell at that label, so this argument supplies no direct bound beyond monotonic information inherited from neighboring visited labels. This is the precise remaining loophole.

## 6. What this closes and what remains

The hidden slack cannot be treated as completely unconstrained: at every rise of `h_n`, finite propagation forces the half-depth bound (7). However, this does not settle Problem 1 because arbitrarily many labels may be skipped between rises, and the exit residence is allowed to jump by an arbitrarily large amount.

The next useful target is therefore narrower than "bound `g_j` everywhere":

1. control the length of a skip block in terms of the inherited preperiod `H`; or
2. use FULL to strengthen the causal support requirement on the exit erasing `1` beyond the bare radius-one cone; or
3. show that repeated exits satisfying only the weak half-depth bound still force unbounded positive excess through some additional complete-core constraint.

Do not infer positive ledger charge from (8) alone. Equation (9) shows explicitly why the present causal estimate is insufficient.

Dependencies: `problem1_global_discrepancy_front.md` Sections 1-2; `problem1_shift_tail_excess_reduction.md`; `problem1_shift_tail_residence_ledger.md`; `problem1_highest_wait_nonforcing.md` Section 2.
