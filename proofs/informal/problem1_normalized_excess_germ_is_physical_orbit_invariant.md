# Problem 1: normalized excess germ is invariant along the physical Rule-30 orbit

## Status

Exact structural lemma obtained by combining the physical-time tail conjugacy with the cut-normalized excess. Problem 1 remains open.

## Setup

Let `r` be a nonzero finite Rule-30 row with right support endpoint `R`, and put

    v = L_R(r),
    q_r(n) = tau(2^n v) - n - R.

For a physical restart after `t>=0` Rule-30 steps, let

    r_t = T^t(r).

The right edge advances exactly one site per physical step, hence the right endpoint of `r_t` is

    R_t = R+t.

Its corresponding tail seed is `T^t(v)`. Define

    q_(r_t)(n) = tau(2^n T^t(v)) - n - (R+t).

The previous physical-time tail conjugacy gives, for every fixed `t`, and all sufficiently large `n`,

    tau(2^n T^t(v)) = tau(2^(n+2t) v) - t.

## Lemma

For every fixed `t>=0`, eventually exactly in `n`,

    q_(r_t)(n) = q_r(n+2t).                     (1)

Therefore the cut-invariant normalized-excess germ satisfies

    Q(T^t r) = Q(r).                            (2)

### Proof

Substitute physical-time tail conjugacy into the restarted normalized excess:

    q_(r_t)(n)
      = [tau(2^(n+2t)v)-t] - n - (R+t)
      = tau(2^(n+2t)v) - (n+2t) - R
      = q_r(n+2t).

This is (1). Since `Q` identifies sequences modulo deletion of finite prefixes, deleting the first `2t` entries does not change the germ, proving (2). QED.

## Consequences

The object isolated in the previous run is not merely independent of the arbitrary zero-tail cut. It is an invariant of the entire forward physical Rule-30 orbit of a finite row.

In particular, all of the following are unchanged by restarting at any finite physical time:

- boundedness of normalized excess above;
- unboundedness above;
- `limsup q = +infinity`;
- infinitely many positive normalized-excess excursions.

Thus the unresolved scalar target can be stated orbit-invariantly:

> For a FULL finite survivor, prove that its physical-orbit invariant normalized-excess germ `Q` is unbounded above.

This gives a useful freedom for future proofs. One may restart at any finite physical time chosen to obtain a convenient complete-fringe/core configuration, without changing the target germ. A successful survivor-specific argument may therefore normalize away any finite transient and work at a favorable late FULL source, provided the argument uses intrinsic fringe information rather than treating the restart itself as a source of excess.

## What this does not prove

This is not an overshoot theorem. It does not force `Q` to grow. It only shows that the remaining obstruction is a genuine forward-orbit invariant, rather than an artifact of the initial row, support cut, or finite transient.

Run 97 already showed that restart cannot amplify normalized physical excess: the `+t` in the unnormalized excess is cancelled by the moving endpoint. The present lemma packages that cancellation together with the cut-invariant germ from run 99 and makes the stronger conceptual conclusion explicit: all finite physical restarts represent the same `Q`.

## Research implication

Future complete-fringe arguments should exploit the freedom to choose a late physical representative of the same germ. This may be useful for the missing bounded-reuse/ordered-erasure theorem: prove it after entering a convenient recurrent FULL source class, while retaining the original finite fringe data needed for a non-covariant charge. Conversely, any proposed obstruction that changes merely because a finite physical prefix was removed cannot control `Q`.