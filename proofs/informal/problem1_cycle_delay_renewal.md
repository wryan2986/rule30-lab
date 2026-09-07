# Exact renewal of cycle-entry delay at physical extensions

Status: `partial-proof`, lead-audited; fresh external adversarial review
could not be completed. These are exact
conditional identities, not a proof of FULL/finite-entry incompatibility.
Problem 1 remains OPEN. The separate shift-tower note supplies a scoped
`refuted` local bound. No larger actual prefix or parameter search is used.

## 0. Admission and route choice

The round-nine highest-disagreement formula describes the first erasure of
one row. The current bottleneck needs the future of ONE fixed actual FULL
orbit. Three possible routes were ranked as follows:

1. Derive the exact gain or loss of least preperiod at a physical extension.
   This has a local falsification test and may identify which actual events
   replenish the delay consumed by the necessary clock doublings.
2. Use bounded preperiod to close a finite spatial strip. The previously
   identified higher driver remains present; a fixed strip alone does not
   prove closure. The sidecar locates the dependency without claiming an
   impossibility theorem for all possible quotients.
3. Control the whole-row delay from its current highest-disagreement wait.
   A positive bound would justify focusing on that wait alone. An unbounded
   separation would require following later erasures too. The separate
   shift-tower note settles this local question negatively.

Route 1 is the main attack: all-depth plausibility and falsifiability are
high, and research cost is low. Route 2 lacks a closure mechanism. Route 3
is useful only as a falsification of a possible intermediate lemma. None
of these rankings asserts that the unresolved global implication is likely
to follow. The fixed twelve-case check tests route 1's identities only;
agreement is `finite-exhaustive` on its named controls, not an infinite proof.

Use the existing A(y)=(y>>2) XOR ((y>>1) OR y), sigma(y)=y>>1,
least A-preperiod tau(y), least eventual period p(y), and phase-correct
cyc(y). The one-bit scan law is imported from the round-nine physical note.
All y below are eventually A-periodic. Initially finite y suffice but are
not required for the local theorem.

## 1. General one-bit extension, including an inherited transient (`partial-proof`)

Let z=2y+a, a in {0,1}, T=tau(y). Put

    u_s=bit_0(A^s y), v_s=bit_1(A^s y),
    w_s=bit_0(A^s z).

Spatial deletion and the A bit rule give, for every s>=0,

    sigma A^s z=A^s y,
    w_(s+1)=v_s XOR (u_s OR w_s).                    (1)

Projection preserves periodicity, so tau(z)>=T. At time T the upper row
q=A^T y is A-periodic. Set e=bit_0(A^T z). Exactly two cases remain.

* If bit_0(A^s q)=0 for EVERY s>=0, both extensions 2q and 2q+1
  are A-periodic: each scalar update is a permutation. Consequently

      tau(z)=T.                                    (2)

* Otherwise the periodic drive contains a low 1. Exactly one extension
  2q+e_* is A-periodic. Define

      rho=min{s>=0:bit_0(A^s q)=1}.

  This minimum exists. The exact alternatives are

      tau(z)=T             if e=e_*,
      tau(z)=T+rho+1       if e!=e_*.               (3)

For (3), the two scalar responses remain opposite under every preceding
permutation and coalesce at the first constant map, which is the update
at time rho. Thus the wrong response's last disagreement with its
phase-correct periodic response is at time rho, and its least onset is
rho+1. This is the round-nine periodic-input lemma applied AFTER the
inherited transient; tau(A^T z)=tau(z)-T supplies the equality for z.
The inequality tau(z)>=T is needed here and prevents an accidental early
entry from being counted as a negative residual.

An independent derivation follows the skew product over the p(y)-cycle.
When the low drive is always zero, the return map on the two scalar states
is identity or swap, so every state is recurrent. When a low 1 occurs,
the return contains a constant map, so it has a unique recurrent response.
Tracking the two responses to their first constant factor gives the same
least delay in (3). No upper bound on the driving period is used.

## 2. The exact physical delay recurrence (`partial-proof`)

Now keep ONE actual spacetime and its actual center bits c_t. Assume every
Y_t is eventually A-periodic and write

    Y_(t+1)=2 A Y_t+c_(t+1),
    tau_t=tau(Y_t), p_t=p(Y_t),
    T_t=max(tau_t-1,0),
    R_t=tau_(t+1)-T_t.                              (4)

Apply Section 1 to y=A Y_t. It proves R_t>=0 exactly. Put

    q_t=A^(T_t+1)Y_t,
    e_t=bit_0(A^(T_t) Y_(t+1)).

The periodic row q_t is the upper part of A^(T_t) Y_(t+1). If its low trace is
identically zero, R_t=0. Otherwise let e_* be its unique periodic lift
bit and let rho_t be the first time its low trace is 1. Then

    R_t=0             if e_t=e_*,
    R_t=rho_t+1       if e_t!=e_*.

Thus the exact recurrence is

    tau_(t+1)=max(tau_t-1,0)+R_t.                   (5)

R_t measures a NEW delay beyond the inherited cycle-entry time. It is
not automatically a disagreement born at the current physical low bit:
e_t is evaluated at A-time T_t, which can be positive. The actual bit
interpretation, from the physical diagonal identity, is

    e_t=r_(-T_t)(t+1+T_t).                          (6)

The initial right fringe has never been replaced. The q_t, e_t and R_t
all concern this same actual spacetime and its cycle completions.

## 3. Clock doublings consume delay exactly (`partial-proof`)

For a physical step, the period is preserved or doubled. A doubling
p_(t+1)=2p_t requires the eventual low trace of Y_t, equivalently of
A Y_t, to be identically zero. Section 1 therefore proves, WITHOUT FULL,

    p_(t+1)=2p_t => R_t=0 and
    tau_(t+1)=max(tau_t-1,0).                       (7)

Under FULL, c_t=1 at even t and 0 at odd t, with the fixed complete initial
right fringe retained. The previously proved source lateness gives
tau_t>=1 for an even doubling source and tau_t>=2 for an odd source.
Consequently under FULL the stronger exact statement is

    p_(t+1)=2p_t => tau_(t+1)=tau_t-1.              (8)

This improves a lower bound on the source by identifying the exact amount
spent. It does NOT say that a nondoubling step must add delay: such a step
can also have R_t=0, including a permutation tail with even flip parity.

There is also a two-step consequence at an EVEN doubling source under
FULL. If tau_t<=2, then

    p_(t+1)=2p_t => tau_(t+2)=0 and p_(t+2)=2p_t.    (8a)

Indeed (8) gives tau_(t+1)<=1, so A Y_(t+1) is periodic. The eventual
code of Y_(t+1) has form (v_s,0), with a recurring 1 in v because the
doubling response visits both bit states. The next scalar scan therefore
has maps w -> v_s OR w and unique recurrent bit 1. Its upper row is
already cyclic and its ACTUAL initial bit is c_(t+2)=1. This is the
correct lift, proving tau_(t+2)=0. The recurring reset preserves the new
period. This argument is local to these actual steps and does not exclude
later delay injections.

Let H_t=t+tau_t be the physical time corresponding to cycle entry. Equation
(5) gives

    H_(t+1)=max(H_t,t+1)+R_t.                       (9)

Hence H_t is nondecreasing, and a FULL doubling has H_(t+1)=H_t. If a
sequence of consecutive steps has tau_t>0 and R_t=0 at each source, H
is constant throughout it and tau decreases by one per step. At that
same physical time H, sigma^(H-t)Y_H=A^(H-t)Y_t is on its A-cycle.
This is an interpretation along one spacetime, not a bounded-state model.

## 4. A necessary infinite supply of resetting delays (`partial-proof`)

For N>=0 put

    V_N=#{0<=t<N:tau_t>0},
    D_N=#{0<=t<N:p_(t+1)=2p_t}=log_2(p_N/p_0).

Telescoping (5) yields exactly

    sum_(t=0..N-1)R_t=tau_N-tau_0+V_N.              (10)

Under FULL, (8) makes D_N<=V_N, whence

    sum_(t=0..N-1)R_t >= D_N-tau_0.                 (11)

For a nonzero finite-entry input and one fixed finite initial right fringe,
the reviewed finite-width/code argument proves p_N tends to infinity.
Thus D_N tends to infinity. Each R_t is finite, so (11) requires infinitely
many distinct steps with R_t>0. Every such step is the wrong resetting lift
in (3) and preserves the clock. Infinite doublings and infinite delay
injections must coexist on this SAME hypothetical orbit.

If tau_t<=K for all t>=M with K>=1, each later R_t<=K. Applying (10) on
[M,N) gives the additional conditional count

    K * #{M<=t<N:R_t>0}
       >= #{M<=t<N:p_(t+1)=2p_t}-tau_M.            (12)

This is only a budget identity and inequality. It permits infinitely many
bounded injections and arbitrarily sparse doublings; it forces neither
unbounded delay heights nor a positive event density. In particular it
does not bound the sum on the left by the original anchored Q(Y_0).

## 5. Remaining obligation and verification fence (`inconclusive`)

The useful refinement is to control the actual resetting lifts at the
inherited horizon, including e_t and the future low trace of q_t. Under
bounded delay all these horizons stay a bounded distance from physical
time, but their periodic drivers can have unbounded periods. No invariant
has yet bounded their total injection budget on a FULL finite-entry orbit.

The K=1 parity restriction remains unresolved here: only even-time
doublings can occur, and (8) then puts their successors on-cycle. Following
a few such cyclic successors does not exclude later injections. No claim
that the process closes after those few steps is made.

The finite check is restricted to y in {0,2,3,6,7,12} and a in {0,1}.
It checks inherited transients, both lift choices, an immediate reset, a
delayed reset, a permutation without doubling, and a permutation with
doubling. No larger input, period or future horizon is authorized by it.
Checker and record: check_round10_delay_renewal.py and
20260907_round10_delay_renewal.json in the existing experiment/results
directories. The lead disposition and exact missing external review are
recorded in problem1_round10_fresh_review.md. These deductions are accepted
only at the stated partial-proof scope, never as a complete prize proof.

Dependencies: problem1_physical_time_cycle_defects.md Sections 1,4-6;
problem1_cycle_completion_defect_transport.md Section 1;
problem1_scan_doubling_cycle_lag.md Section 1; the reviewed full temporal
code conjugacy for least periods. The sidecar independently derives
Section 1; it is not represented as a fresh adversarial review.
