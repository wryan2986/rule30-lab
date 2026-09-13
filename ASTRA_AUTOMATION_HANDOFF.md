# Automation research handoff — 2026-09-13

Problem 1 remains **OPEN**. Continue on `research/astra-next`.

This handoff supplements, and does not replace, `ASTRA_HANDOFF.md` and its
archived predecessors.

## Repository-state warning

The pushed `ASTRA_HANDOFF.md` says that the following round309 drafts were in
the worktree during its intermediate checkpoint:

- `proofs/informal/problem1_three_bit_complete_core_system.md`
- `proofs/informal/problem1_complete_core_phase_transport.md`
- `proofs/informal/problem1_fixed_fringe_phase_collapse.md`

They are **not present in the currently pushed branch tree**. Do not pretend to
audit, extend, or cite their unpushed proofs from the short handoff summaries.
The pushed and inspectable nonreset-return unit
`problem1_nonreset_return_birth_spacing.md` is present.

## First automation reduction: shift-tail excess

Read:

`proofs/informal/problem1_shift_tail_excess_reduction.md`

For a fixed nonzero finite original row, let `R` end its right support and put
`v=L_R(r)>0`. Then every later original cut is exactly

    L_(R+n)(r) = 2^n v.

Combining this with the established global-front threshold identity gives

    tau(Y_(R+n)) = max(tau(2^n v) - (R+n), 0).

Therefore an eventual finite physical delay strip is equivalent, for this row,
to boundedness above of

    e_v(n) = tau(2^n v) - n.

The existing theorem `tau(2^n v) -> infinity` is insufficient. A sufficient
scalar theorem excluding every finite strip would be

    limsup_n [tau(2^n v)-n] = infinity

for every positive finite `v` (or the corresponding FULL-domain statement if a
universal theorem is too strong).

## Second automation reduction: exact residence ledger

Read:

`proofs/informal/problem1_shift_tail_residence_ledger.md`

Put

    h_n=tau(2^n v),
    delta_n=h_(n+1)-h_n >= 0.

Define

    Z_v(N)=#{0<=n<N:delta_n=0}

and

    P_v(N)=sum_(0<=n<N, delta_n>=2)(delta_n-1).

Then exactly

    e_v(N)=tau(v)+P_v(N)-Z_v(N).

In global-front geometry, `delta_n` is exactly the residence length of
characteristic `R+n+1`. Thus:

- `delta=0` is a skipped characteristic and contributes `-1`;
- `delta=1` is a one-step residence and contributes `0`;
- `delta>=2` is a long residence and contributes positive surplus `delta-1`.

Therefore the desired unbounded excess is equivalent to unbounded positive
excursions of

    P_v(N)-Z_v(N).

Every period-doubling characteristic is already known to be skipped, hence is
one unit of the negative ledger. The converse (every skip is a clock doubling)
is not established.

A bounded physical strip of width K forces eventually

    P_v(N)-Z_v(N) <= R+K-tau(v).

This is the exact amortized form any future clock/front/eraser argument must
contradict.

### Local two-step compensation proved

There is a useful but limited exact lemma at a **purely periodic** doubling
source. If positive finite `y` is A-periodic and `z=2y` is A-periodic with
doubled least period, the doubling classification gives a periodic low trace
`b_s=bit_0(A^s z)` containing both 0 and 1. For the next extension `2z=4y`,
the low response satisfies

    w_(s+1)=b_s OR w_s,  w_0=0.

If `q=min{s:b_s=1}`, then `b_0=0`, so `q>=1`, and exactly

    tau(4y)=q+1 >= 2.

Hence the two consecutive ledger increments satisfy

    [tau(2y)-tau(y)-1] + [tau(4y)-tau(2y)-1]
      = tau(4y)-2 >= 0.

If additionally `y=2^n v` with `n>=2`, then `y_0=y_1=0`; the reviewed
`A=sigma^2 T` identity gives `b_1=y_1 XOR y_0=0`, hence `q>=2` and
`tau(4y)>=3`. The two-step contribution is then at least `+1`.

## Third automation reduction: strip inherited transients exactly

Read:

`proofs/informal/problem1_transient_stripping_zero_extensions.md`

Let finite `y` have

    H=tau(y),
    u=T^H(y),
    c=A^H(y)=sigma^(2H)u.

For `x_m=A^H(2^m y)`, the reviewed identities give exactly

    x_m=sigma^(2H)T^H(2^m y).

For `m<=2H`,

    x_m=sigma^(2H-m)u,

so `x_0=c` is periodic, `x_1` is a one-bit lift of `c`, and `x_2` is a
one-bit lift of `x_1`.

The key exact splitting theorem is

    tau(2^m y)=H+tau(x_m).

The lower bound follows from spatial deletion (`tau(2^m y)>=tau(y)=H`), and
once time `H` is reached the remaining least preperiod is exactly that of
`x_m`.

For the zero-extension tower `y=2^n v`, `H=h_n`, this yields

    delta_n=tau(x_1),
    delta_n+delta_(n+1)=tau(x_2),

and hence the two-step ledger contribution is exactly

    (delta_n-1)+(delta_(n+1)-1)=tau(x_2)-2.

In particular a skip is exactly `tau(x_1)=0`: after the inherited transient
is stripped, the first lift is periodic. Thus the transient-transport problem
has been reduced to a finite-lift phase problem over a periodic core.

Important obstruction: unlike literal multiplication by 2 at time zero, the
newly exposed low bits of `x_1,x_2` are bits of `u=T^H(y)` and are not
necessarily zero. For `y=2^n v`, `u=2^n T^H(v)` has `n` trailing zeros, but
the low bit of `x_2` is bit `2H-2` of `u`, which is forced zero only if
`2H-2<n`. That inequality is unavailable in the bounded-strip regime where
`H` may be `n+O(1)`.

So the old purely-periodic compensation proof cannot simply be transported by
waiting out the transient. The transient itself is now removed exactly; the
remaining issue is the post-transient lift phase.

## Fourth automation reduction: exact periodic one-bit lift classifier

Read:

`proofs/informal/problem1_periodic_one_bit_lift_classifier.md`

For any A-periodic finite state `z`, write

    z_s=A^s(z),
    b_s=bit_0(z_s),
    c_s=bit_1(z_s).

Every one-bit lift `w=2z+a_0` stays a one-bit lift along the orbit:

    A^s(w)=2z_s+a_s,

and the exposed bit obeys exactly

    a_(s+1)=c_s XOR (b_s OR a_s).

Thus `b_s=1` is an eraser (the next bit is independent of `a_s`), while
`b_s=0` gives an identity or toggle map and preserves the distinction between
the two lift bits.

This solves the finite-lift phase problem exactly.

- If `b_s` is identically zero, **both** one-bit lifts are periodic from time
  zero, so `tau(2z)=tau(2z+1)=0`.
- Otherwise there is a unique recurrent initial lift bit `r_0`. Let

      q=min{s>=0:b_s=1}.

  The recurrent bit gives `tau(w)=0`; the other bit gives exactly

      tau(w)=q+1.

Applied at a tower skip with `z=x_1`, `w=x_2`, this gives the exact two-step
ledger:

    tau(x_2)-2 = -2

if the actual phase chooses the recurrent lift (or if the low trace of `x_1`
is identically zero), while a nonrecurrent lift gives

    tau(x_2)-2 = q-1.

Therefore the hoped-for universal local theorem `tau(x_2)>=2 at every skip`
is **false for arbitrary periodic lifts**. This is now a closed dead route;
do not retry it without using extra FULL-tail structure.

The actual post-transient phase bit is explicit. With

    u=T^H(y),
    x_1=sigma^(2H-1)u,
    x_2=sigma^(2H-2)u,

we have

    bit_0(x_2)=bit_(2H-2)(u).

So the unresolved question is whether the common-tower origin constrains this
bit relative to the unique recurrent lift bit strongly enough to produce a
net ledger gain.

Small exact examples show the phase failure is genuine, not merely logical:
`z=12` is period two, but its lifts satisfy `tau(24)=2` and `tau(25)=0`;
`z=13` has `tau(26)=1` and `tau(27)=0`. These are sharpness examples only, not
finite-sampling evidence for the asymptotic theorem.

## Current preferred target

Seek an all-depth mechanism on the FULL finite-fringe domain proving

    limsup_N [P_v(N)-Z_v(N)] = infinity.

The best local object is no longer an isolated skip. Treat a **maximal block of
consecutive skips** as one object. After transient stripping, such a block is
exactly a chain

    x_0, x_1, ..., x_k

of consecutive nested one-bit lifts that are all A-periodic, followed by the
first nonperiodic lift `x_(k+1)`.

The next concrete target is to derive an exact block ledger formula and lower
bound the exit preperiod `tau(x_(k+1))` in terms of the block length k and the
eraser locations of the successive periodic cores. If the exit residence
always pays for all or almost all preceding skips, the remaining global burden
becomes much smaller. If not, classify the phase mechanism that permits a
long periodic-lift block to exit cheaply.

Do **not** spend more effort transporting the inherited transient itself: the
splitting identity does that exactly. Do **not** retry universal two-step
compensation for arbitrary periodic lifts: the classifier and explicit
counterexamples above rule it out.

Do not resume gate-prefix, source-prefix, shifted-row, periodic-core, or front
sampling merely to estimate average drift; the ledger is exact and finite
samples cannot settle its asymptotic imbalance.

No claim of a Problem 1 solution is made here.
