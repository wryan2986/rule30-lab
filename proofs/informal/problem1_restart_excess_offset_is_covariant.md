# Physical restart does not amplify tail excess relative to the moving support edge

Status: `partial-proof` / strategy fence. This note combines the established physical-time tail conjugacy with finite-speed right-edge motion. It does **not** close Problem 1.

## Statement

Let `r` be a nonzero finite Rule-30 row, let `R` be its rightmost occupied site, and put `v=L_R(r)>0`. Define

    e_v(n)=tau(2^n v)-n.

After `t` physical Rule-30 steps, the rightmost occupied site is `R_t=R+t`: the outside neighborhood at the old right edge is `100`, whose Rule-30 output is `1`, while no site farther right can turn on in one step.

The established physical-time tail conjugacy says that for each fixed `t`, eventually in `n`,

    e_(T^t v)(n)=e_v(n+2t)+t.

Subtracting the restarted support endpoint gives

    e_(T^t v)(n)-R_t
      = e_v(n+2t)+t-(R+t)
      = e_v(n+2t)-R.                         (1)

Thus the quantity that actually controls physical delay,

    e_v(n)-R,

is asymptotically **covariant under physical restart**: restarting only deletes a finite prefix and reindexes the same tail values. In particular, using the global-front formula,

    tau(Y_(R+n)) = max(e_v(n)-R,0),

the restarted tail has eventually exactly the same physical-delay values as the original tail after the corresponding `2t` tower shift.

## Consequences

1. A bounded-excess contradiction cannot be obtained merely by restarting later and using the `+t` in
   `e_(T^t v)(n)=e_v(n+2t)+t`. The support endpoint acquires the same `+t`, cancelling it exactly.

2. If `e_v(n)<=C` eventually, then a restart gives `e_(T^t v)(n)<=C+t`, but its right edge is `R+t`; therefore the physical strip bound remains `C-R`, not something that improves with `t`.

3. Likewise, hidden slack is restart-covariant. Since on zero-delay rows

       g_(R+n)=R-e_v(n),

   equation (1) shows the restarted slack equals the corresponding original-tail slack after reindexing.

So physical-time restart invariance is useful for transporting any future survivor-specific theorem, but it cannot itself manufacture overshoot, positive ledger drift, or a finite-resource contradiction.

## Strategic fence

Do not attempt to turn the `+t` term in physical-time tail conjugacy into an unbounded physical-delay lower bound without tracking the moving right support endpoint. The two shifts cancel.

The remaining useful target is genuinely non-covariant information tied to the complete original fringe: for example, a bounded-use resource, an ordered erasure count, or a theorem forcing new positive overshoot of `e_v(n)-R` rather than merely transporting existing excess under restart.

Dependencies: `problem1_physical_time_tail_conjugacy.md`, `problem1_shift_tail_excess_reduction.md`, and `problem1_hidden_slack_is_negative_excess_no_go.md`.