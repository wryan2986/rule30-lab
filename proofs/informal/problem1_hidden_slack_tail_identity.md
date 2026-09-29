# Problem 1: hidden slack on the finite-support shift tail

Status: exact reduction / route clarification; Problem 1 remains OPEN.

This note connects the `ASTRA_AUTOMATION_HANDOFF.md` hidden-slack target directly to the already proved shift-tail excess and residence ledger. It adds no new dynamical assumption.

## Setup

Fix a nonzero finite original row `r`, let `R` be its right-support endpoint, and put

    v = L_R(r) > 0.

The established shift-tail identity is

    L_(R+n)(r) = 2^n v.

Write

    h_v(n) = tau(2^n v),
    e_v(n) = h_v(n) - n.

For original-cut thresholds `s_j = tau(L_j(r))`, the shift tail therefore gives the exact identity

    s_(R+n) = h_v(n).

At a zero-delay row the automation handoff defines hidden slack

    g_j = j - s_j >= 0.

Hence on the shift tail

    g_(R+n) = R+n-h_v(n)
            = R-e_v(n).                 (1)

This equality is valid algebraically at every tail index if `g` is allowed as the signed quantity `j-s_j`; the condition `g>=0` is exactly the zero-physical-delay condition.

## Exact increment law

Let

    delta_n = h_v(n+1)-h_v(n) >= 0.

Then (1) gives

    g_(R+n+1)-g_(R+n) = 1-delta_n.       (2)

Thus:

- a skip `delta_n=0` increases hidden slack by exactly 1;
- a one-step residence `delta_n=1` leaves it unchanged;
- a long residence `delta_n>=2` repays exactly `delta_n-1` units of hidden slack.

This is the same signed residence ledger in the opposite coordinate. Indeed the established telescope

    e_v(N)=tau(v)+P_v(N)-Z_v(N)

is equivalent to

    g_(R+N)=R-tau(v)-P_v(N)+Z_v(N).

So hidden slack is not an independent charge that can evade the telescope; it is exactly the negative excess coordinate, shifted by the fixed support endpoint `R`.

## Consequence for the preferred target

The desired scalar theorem remains

    limsup_n e_v(n) = +infinity.

By (1), this is exactly

    liminf_n g_(R+n) = -infinity

for the signed continuation `g_j=j-s_j`.

Physical zero-delay rows see only the portion `g>=0`. Therefore merely proving that positive hidden slack cannot become arbitrarily large would give only a lower bound on `e_v`; it does **not** prove the required unbounded positive excursions of `e_v`.

A successful "slack repayment" theorem must be stronger: after sufficiently large positive slack has accumulated during skips, later admissible FULL/source structure must force repayment not merely back to `g=0`, but with arbitrarily large overshoot into `g<0`. Equivalently it must force endpoint physical delays `s_j-j=-g_j` to attain arbitrarily large positive values.

This sharpens options (1) and (2) in the automation handoff: on the finite-support shift tail they are not separate asymptotic mechanisms. Option (2) can prove the theorem only if it forces **overshooting repayment**, which is option (1) in the signed coordinate.

## Stopping fence

Do not search for a second additive invariant by renaming `j-s_j`: equations (1)-(2) show that hidden slack alone is exactly the already-known telescoping residence ledger. Any genuinely new global charge must include additional information (for example complete core/fringe state or ancestor reuse), not just `s_j`, `tau(Y_j)`, and the residence increments.

The next proof-relevant question is therefore precise: can the admissible FULL/cyclic-source mechanism force arbitrarily deep overshoot `g<0` after zero-delay slack episodes, rather than merely forcing a return to positive physical delay?
