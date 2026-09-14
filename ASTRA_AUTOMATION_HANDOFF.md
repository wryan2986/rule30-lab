# Automation research handoff — 2026-09-13

Problem 1 remains **OPEN**. Continue on `research/astra-next`.

This handoff supplements, and does not replace, `ASTRA_HANDOFF.md` and its archived predecessors.

## Repository-state warning

The pushed `ASTRA_HANDOFF.md` says these round309 drafts existed only in its worktree checkpoint:

- `proofs/informal/problem1_three_bit_complete_core_system.md`
- `proofs/informal/problem1_complete_core_phase_transport.md`
- `proofs/informal/problem1_fixed_fringe_phase_collapse.md`

They are not present in the pushed branch. Do not reconstruct or cite their proofs from handoff summaries alone. The pushed `problem1_nonreset_return_birth_spacing.md` is inspectable.

## 1. Shift-tail excess reduction

Read `proofs/informal/problem1_shift_tail_excess_reduction.md`.

For a fixed nonzero finite original row, let `R` end its right support and put `v=L_R(r)>0`. Then

    L_(R+n)(r)=2^n v.

The global-front threshold identity gives

    tau(Y_(R+n)) = max(tau(2^n v)-(R+n),0).

Thus an eventual finite physical delay strip is equivalent to boundedness above of

    e_v(n)=tau(2^n v)-n.

The existing theorem `tau(2^n v)->infinity` is insufficient; a sufficient scalar target is

    limsup_n e_v(n)=infinity.

## 2. Exact residence ledger

Read `proofs/informal/problem1_shift_tail_residence_ledger.md`.

Put

    h_n=tau(2^n v),
    delta_n=h_(n+1)-h_n >= 0.

Define

    Z_v(N)=#{0<=n<N:delta_n=0},
    P_v(N)=sum_(delta_n>=2, n<N)(delta_n-1).

Then exactly

    e_v(N)=tau(v)+P_v(N)-Z_v(N).

Geometrically `delta_n` is the residence length of characteristic `R+n+1`: skip `delta=0` contributes `-1`, one-step residence contributes `0`, and long residence contributes `delta-1`.

The desired theorem is therefore unbounded positive excursions of `P_v-Z_v`.

## 3. Transient stripping

Read `proofs/informal/problem1_transient_stripping_zero_extensions.md`.

For finite `y`, let

    H=tau(y),
    u=T^H(y),
    x_m=A^H(2^m y).

Then

    tau(2^m y)=H+tau(x_m).

For `m<=2H`,

    x_m=sigma^(2H-m)u,

so the tower increment problem becomes a chain of nested one-bit lifts after the inherited transient is removed.

For `y=2^n v`,

    delta_n=tau(x_1),
    delta_n+delta_(n+1)=tau(x_2).

A skip is exactly `tau(x_1)=0`.

## 4. Periodic one-bit lift classifier

Read `proofs/informal/problem1_periodic_one_bit_lift_classifier.md`.

For periodic `z_s=A^s(z)`, write

    b_s=bit_0(z_s),
    c_s=bit_1(z_s),

and a one-bit lift as `A^s(w)=2z_s+a_s`. Then

    a_(s+1)=c_s XOR (b_s OR a_s).

If the low trace `b_s` is identically zero, both lifts are periodic. Otherwise there is one recurrent initial lift bit. If

    q=min{s>=0:b_s=1},

then the recurrent lift has preperiod zero and the other lift has preperiod exactly `q+1`.

Therefore universal two-step compensation is false for arbitrary periodic lifts. Do not retry it without common-origin tower structure.

## 5. Exact maximal skip-block ledger

Read `proofs/informal/problem1_maximal_skip_block_ledger.md`.

If a maximal block begins at tower index `n` and contains `k>=1` consecutive skips, transient stripping gives periodic nested lifts

    x_0,...,x_k

followed by first nonperiodic `x_(k+1)`.

The whole block plus its exit residence has exact ledger charge

    B=tau(x_(k+1))-(k+1).

Let

    q_k=min{s>=0:bit_0(A^s(x_k))=1}.

The one-bit classifier gives

    tau(x_(k+1))=q_k+1,

hence

    B=q_k-k.

So local block compensation is exactly the inequality `q_k>=k`.

That inequality is false for arbitrary nested periodic lifts. The exact chain

    1 -> 3 -> 6 -> 13 -> 27 -> 55 -> 111

consists of periodic nested lifts, while the next lift `223` has preperiod one. This gives `k=6`, `q_k=0`, `B=-6`. Thus any successful block theorem must use the shared origin `x_m=A^H(2^m y)`.

## 6. Exact zero-extension / physical-time renormalization

Read `proofs/informal/problem1_zero_extension_time_renormalization.md`.

The packed Rule-30 map satisfies

    T(2^m q)=2^m T(q).

Consequently, for all `n,t>=0`,

    A^t(2^(n+2t)v)=2^n T^t(v).

Using `tau(A^t x)=max(tau(x)-t,0)` gives the exact identity

    tau(2^n T^t(v))
      = max(tau(2^(n+2t)v)-t,0).

Equivalently,

    h_(T^t v)(n)=max(h_v(n+2t)-t,0).

At `n=0`,

    tau(T^t(v))=max(h_v(2t)-t,0).

Thus the even tower subsequence has a sharp pointwise dichotomy between A-periodic physical rows and positive physical-row preperiod.

## 7. Physical-time tail conjugacy

Read `proofs/informal/problem1_physical_time_tail_conjugacy.md`.

For every nonzero finite `v`, the established theorem `h_v(n)->infinity` removes the max branch after any fixed physical restart. Fix `t>=0`. There is `N_t` such that for every `n>=N_t`,

    h_(T^t v)(n)=h_v(n+2t)-t,

hence

    e_(T^t v)(n)=e_v(n+2t)+t.

The residence increments therefore satisfy, eventually exactly,

    delta_(T^t v)(n)=delta_v(n+2t).

So skips, one-step residences, long residences, and their `P-Z` ledger are transported under physical time by deletion of a finite prefix and translation of indices.

In particular,

    limsup e_(T^t v) = t + limsup e_v

in the extended-real sense. Therefore the target `limsup e_v=infinity` and its negation (eventual boundedness above) are invariant under restarting at any fixed physical Rule-30 time.

This also clarifies the role of the pointwise A-periodic branch at `n=0`: an A-periodic physical row can change only a finite prefix of the restarted tower. It cannot create a permanently different asymptotic residence ledger.

## 8. Physical episode ledger telescope — forced birth route fenced

Read `proofs/informal/problem1_physical_episode_ledger_telescope.md`.

For original-cut delays `s_j`, let

    Delta_j=s_(j+1)-s_j.

For every `a<b`, exactly

    sum_(j=a..b-1)(Delta_j-1)
      =(s_b-b)-(s_a-a).

Whenever both endpoint physical delays are positive, the threshold identity
`tau(Y_j)=max(s_j-j,0)` therefore gives

    sum_(j=a..b-1)(Delta_j-1)
      =tau(Y_b)-tau(Y_a).

This closes the tempting idea that a forced local birth can automatically be
counted as an independent positive `P-Z` contribution.

For the pushed TWO-BIT nonreset source profile,

    tau(Y_t),...,tau(Y_(t+6))=2,1,0,0,0,0,1,

so the whole passage through the forced birth has exact signed ledger charge

    1-2=-1.

The forced `beta=1` birth creates a resetting one-bit `t` source at `t+6`.
Its two possible delay triples are `1,1,1` and `1,0,1`, so its complete
immediate two-step passage has charge zero. Therefore the eight-step segment
from the two-bit nonreset source through that resetting passage still has
exact charge `-1`.

For a one-bit nonreset source, if its terminal `beta=1` birth occurs then the
six-step endpoint delays are both one, hence the charge is exactly zero. If
`beta=0`, the terminal delay is zero and no positive charge is forced.

Consequently the separated-birth theorem in
`problem1_nonreset_return_birth_spacing.md` cannot be converted into an
additive positive residence budget merely by summing its forced births.
The internal long residences and skips already telescope into endpoint delay.

## Current preferred target

The previous target "force a restart-local birth and count it as positive ledger gain" is now fenced off.

A viable all-depth mechanism must instead do at least one of the following:

1. force positive endpoint physical delays themselves to increase beyond every bound;
2. control the hidden negative excess `s_j-j` at zero-delay rows, where `tau(Y_j)=0` truncates that information; or
3. construct a genuinely non-telescoping global charge, distinct from the signed residence sum, with bounded reuse on the original finite fringe.

The second option is the most direct next scalar target. At a zero-delay row, define the hidden slack

    g_j=j-s_j >= 0.

The residence ledger across a segment with a zero-delay endpoint depends on this slack, while the physical strip variable forgets it. A useful next theorem would constrain how large `g_j` can become, or how quickly a later FULL source must repay it, using the same complete-core / global-shadow structure. Without such a theorem, births can be locally real but globally absorbed by skipped characteristics.

Do not resume finite sampling merely to estimate asymptotic drift. Do not retry generic nested-lift compensation. Do not sum separated births as if they were independent positive ledger charges. Do not claim a Problem 1 solution without an all-depth contradiction.
