# Round-6 sidecar: characteristic-event coupling via full-spacetime cones

Status (corrected per lead review): cone-causality facts below are
`partial-proof` (hand derivations, no machine used, corrections independently
checked by the lead; retained as exposition, not a new no-go theorem).
Every periodic-inheritance and actual-survivor growth question
is `inconclusive`. No activity-growth implication is asserted in either
direction. Problem 1 remains open. This file only was owned by this worker;
nothing else is written. No numerical run was performed or admitted.
An explicit errors disposition is retained in Sec. 5.

## 0. Exact hypotheses (imports, not re-proved)

H1. Radius-one update `c_i(s+1) = c_{i-1}(s) XOR (c_i(s) OR c_{i+1}(s))`,
hence speed-one forward/backward cones (round-5 corrected speed; the old
speed-2 error is not reused).
H2. Ray identity (transport note, Sec. 4, eq. 10): `P_n(t) = bit_{2n+2t}
(T^t x) OR bit_{2n+2t+1}(T^t x)` are the two physical cells `e_1 = -2n-t`,
`e_2 = -2n-t-1` at time `t`, for `n >= 1`, `t >= 0`.
The same bit formula defines P_0 and gives these coordinates also at n=0,
when used on the right side of the valid bridge in Section 4.
H3. Survivor setting: one fixed full history with `c_0 = 1` and eventually
period-two center, REBASED so `s = 0` is a phase-one row after the onset: all
branch-trace and gate imports below live in this rebased frame, because
eventual `0`/`1` values at the unrebased original time 0 do not supply the
gate. The ACTUAL branch letter is `b_m = 1[q_m = u] = x_{-2}(2m)` with
`x_{-3}(2m) = 1 - b_m` at rebased even rows (fringe_language.md Sec. 2;
round-5 memo Sec. 3, B2-B3). Permitted gate at rebased origin:
rebased row mod 16 in `{7, 11}`.
H4. Gate bridge (bridge note, Sec. 3): on a permitted forced chain,
`P_n(F^m x, t) = P_{n-m}(x, t+2m)` for `n >= m`; depth zero is outside
the pullback domain (hand counterexample `x = 11` imported, not rerun).

## 1. Physical coordinates (corrected)

The actual branch trace lives at columns `-2`/`-3`: `(-2, 2m)` carrying
`b_m`, `(-3, 2m)` carrying `1 - b_m`. The center is `(0, s)`; near-cut
columns are `-1`/`+1`. Direct (non-queried) boundary sources are therefore
restricted to `i >= -1`; columns `-2`/`-3` and the gate cells are treated
explicitly in Sec. 2(b), not folded into that bound.
At the rebased origin, the `P_1` event is the OR of cells `(-2, -3)`
at rebased `s = 0`: the gate bits 2,3 of `7 = 0111` / `11 = 1011` are
`(1, 0)` / `(0, 1)`, so the OR is `1` (equivalently `OR(b_0, 1 - b_0)`).
This is asserted for the rebased-origin row only, not at unrebased
original time 0.

## 2. Causality: domain of dependence only

Lemma (a). For `n >= 1`, `t >= 0`, the backward cone of the `P_n(t)` pair
is contained in `{(i,s) : i <= -2n-s}`. Proof: `|i - e| <= t - s` gives
`i <= e + (t - s) <= e_1 + (t - s) = -2n - s`. Hence no point with
`i >= -1` at any `s >= 0` lies in any `P_n` cone: no center, `-1`/`+1`,
or right-fringe point is ever queried. The time-zero slice `i <= -2n`
reproduces the reviewed endpoint statement.
Lemma (b), exact exceptional range for the EVEN-TIME branch trace. Among
branch-trace points `(-2, 2m)`, `(-3, 2m)` (`m >= 0`), the only ones in
any `P_n` (`n >= 1`) cone are `(-2, 0)` and `(-3, 0)`, and only in
`P_1(t)` cones (every `t >= 0`). The `s = 2m` restriction is essential:
e.g. `(-3, 1)` lies in the `P_1(t)` cone for `t >= 1` (via `e_1`:
`|t-1| = t-1 <= t-1`) but is not an even-time branch point; no claim is
made about odd-time `-2`/`-3` points. Proof: for
`(-2, 2m)` the necessary bound `-2 <= -2n-2m` forces `(n, m) = (1, 0)`;
for `(-3, 2m)`, `-3 <= -2n-2m` forces the same; membership is verified by
equality at `s = 0` (`|-2 - e_1| = t`, `|-3 - e_2| = t`). Every later
branch point (`m >= 1`) and every deeper cone (`n >= 2`) strictly excludes
the branch trace.
Scope. (a) and (b) are standard domain-of-dependence consequences of
H1+H2. The all-time bound follows the reviewed time-zero endpoint plus
radius one; it is recorded as exposition unless review finds otherwise.
No strict novelty or no-go status is claimed for the geometry itself.

## 3. What causality does and does not settle

Accepted (causality only): the recurrence determining `P_n(t)` never
queries values at `i >= -1`, and queries EVEN-TIME branch values at `-2`/`-3` only in the
Sec. 2(b) exceptional range. A DIRECT periodic side condition imposed
inside that recursion has nothing to read.
NOT established: any refutation of periodic inheritance as a global
theorem. An eventually periodic center may still constrain the in-cone
INITIAL data (Sec. 2(c) of the prior version is retained only in this
weakened sense: deep initial cells reach the cut after delay `>= 2n-1`,
so global consistency can couple them). No full-spacetime counterexample
is offered. The tempting transfer T-center, as a claim about global
periodic inheritance, is `inconclusive`; labeling it refuted was error E2
and is withdrawn.

## 4. Same-column cross-history identity, corrected shortfall

For a permitted chain and `n >= m`, with `e = {-2n-t, -2n-t-1}`:
E_forced^m(e, t) = E_orig(e, t+2m), by H2 in each history plus H4 (index
check `-2(n-m)-(t+2m) = -2n-t`). Endpoint consistency (no new
computation): `x = 11`, `m = n = 1`, `t = 0` gives `0 = 0` by the
reviewed `P_1(51,0) = P_0(11,2) = 0`. The per-event anchored budget
`n > t+3m` (x-side event at depth `N = n-m`, time `T = t+2m`, anchored
need `T < N`) is valid. Corrected shortfall (E4): same-`N` events at
distinct times can in principle accumulate toward unbounded `J`, so the
identity is NOT shown to be non-forcing; it supplies no multiplicity
mechanism and no source for the deep forced events. Multiplicity status:
`inconclusive` (no multiplicity supplied), not "never unbounded".

## 5. Errors disposition (accepted from lead review)

E1. Branch coordinates: prior Sec. 1 claimed every branch point satisfies
`i >= -1` and treated the branch as generic one-time freedom. False: the
actual `q`/`u` indicator is `x_{-2}(2m)` with `x_{-3}(2m) = 1 - b_m`.
Corrected in Sec. 1 and handled via the Sec. 2(b) exceptional range.
E2. Refutation overclaim: prior Sec. 3 labeled a periodic-inheritance
inference refuted/obstructed. Cone exclusion is deterministic domain-of-dependence only and cannot refute a global-constraint theorem
without a true full-spacetime counterexample. Downgraded in Sec. 3.
E3. Novelty overclaim: prior text claimed a strictly stronger theorem.
The all-time geometry largely follows the old radius endpoint; recorded
as exposition in Sec. 2 scope.
E4. Multiplicity overclaim: "one event per (m,t) yields J >= 1, never
unbounded" was too strong. Corrected in Sec. 4 to "no multiplicity
supplied".

## 6. Verdict

Frozen as corrected exposition with lead-accepted geometry; no new no-go
is asserted. Surviving (`partial-proof`, lead checked): domain-of-dependence
facts Sec. 2(a)-(b) with the exact `{(n,m) = (1,0), s = 0}` exceptional range;
same-column identity with valid budget `n > t+3m`. Open (`inconclusive`):
periodic inheritance, unbounded anchored `J` for a fixed actual survivor,
and any multiplicity route through Sec. 4. No solution is claimed.
No pending proof-critical review is attached to this expository memo.
