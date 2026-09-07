# Fresh adversarial review (round 8): bounded-lag doubling controls

Reviewer model: opencode-go/muse-spark-1.3-contributor; thread 01a07956-ee3d-7431-bd4b-f0ec21cc04bd.
Review timing (orchestration bounds): worker spawn 2026-09-07 00:48:55 UTC;
completion notification received by 2026-09-07 00:51:14 UTC. No finer elapsed time is claimed.
Source reviewed: proofs/informal/problem1_bounded_lag_doubling_controls.md
Source SHA256: d45a965818b4d4c89dc4453719724a6da4bf62edcd8c5b532618b2a42e2875e5
Objective: find a fatal flaw, not confirmation.
Scope: read ONLY the target plus its listed mathematical dependencies as needed
(full-fringe temporal diagonal Secs 1-4, inverse-scan reset language Sec 2,
scan-doubling cycle lag Sec 1, anchored finite-entry A^h=pi^h T^h).
Did NOT read any prior review, sidecar, or handoff verdicts.
No experiments, searches, or code runs; hand derivation plus local reads/hashes only.
Owns only this file; no commits.

## Imported lemmas (not re-proved, checked for fit)

- Theta(4x+a)=I_a Theta(x); Phi I_a = id; Phi commutes with shift; Theta injective,
  Theta A = shift Theta (one step), Theta: Z_2 onto codes (triangular homeomorphism).
- Driven maps H_0=[0,1,3,3], H_1=[3,2,2,2], H_2=[2,3,1,1], H_3=[1,0,0,0].
- Reset-language period table: doubling (q=2p) iff tail in {0,2} with odd 2-count
  or in {0,3} with odd 3-count per least period; all other tails give q=p (or 1).
- Clock growth: fixed nonzero finite-entry input gives p(E_m)->inf, no FULL premise.
- D0=D1=D2=3 hand prefix equivalences under zero fringe; alternating-center identity.
- A^h = pi^h T^h; A preserves positive finite bit length.

## Independent verification

1. Doubling-source supply. r_m->inf plus steps in {r_m, 2r_m} forces infinitely
   many doublings with unbounded source periods (else r_m eventually constant).
   For such m, k a multiple of r_m past the preperiod gives z=A^k V_m finite,
   on-cycle, Theta(z)=shift^k E_m purely periodic. Least period is preserved:
   r_m is the least eventual period, so its purely periodic tail has least
   period r_m. No per-type unboundedness is claimed; none is needed.
2. Theta-preimage of s=(3,2,2,0,u). s is an ordinary code; preimage x in Z_2
   exists by imported surjectivity. Only A^4 x = z (finite, periodic) is claimed,
   via shift^4 s = u = Theta(z) plus conjugacy/injectivity -- not initial
   finiteness of x. T^4 x finite follows from pi^4 T^4 x = z finite. Correctly scoped.
3. Successor head. c_0=3 by I_3; c_1=H_2(3)=1 and c_2=H_0(1)=1 recomputed from
   the imported H rows. Pair actions confirmed: H_0=id, H_2=swap on {1,3};
   H_0=id, H_3=swap on {0,1}. c_2=1 lies in both pairs. Odd swap-count per least
   period gives c_(t+p)=partner(c_t), c_(t+2p)=c_t for t>=2, any phase. tau(c)<=2.
   Least period: Phi c = shift^2 s has least eventual period p, and a period-q
   input gives Phi-image period dividing q, so p|p(c); explicit 2p-periodicity
   gives p(c)|2p; the swap excludes p. Hence p(c)=2p exactly. No smaller-divisor gap.
4. Source bounds. shift^4 s = u purely periodic gives tau(s)<=4, p(s)=p.
   Positivity: s_1=2 blocks a pure {0,3} tail; s_0=3 blocks a pure {0,2} tail.
5. Zero fringe. D_0=s_0=3 immediate; D_1=(I_0 s)_2=h(1,s_1)=h(1,2)=3 recomputed
   by hand; D_2=3 from the reviewed b_2=2 equivalence. Claim is only j<=2.
   X_1 actual (not merely permitted) rests on the imported alternating-center
   identity -- flagged as imported, used within its stated range (times 0-5).
6. Quantifiers. (7) is per-P existence with x,z varying in P; single-x infinite
   transitions, FULL-orbit lag bounds, and initially-finite-x bounds are all
   explicitly excluded in Section 3. No finite-to-infinite promotion found.

## Adversarial probes (sought countercases)

- Period 1, type {0,2}: u=(2), s=(3,2,2,0,2...), c=(3,1,1,3,1,3...); tau(c)=2
  exactly, p(c)=2. Works; preperiod bound sharp, not violated.
- Period 1, type {0,3}: u=(3), c=(3,1,1,0,1,0...); tau(c)=2, p(c)=2. Works.
- Phase/shift: odd-count swap is rotation-invariant; tau<=4 and tau<=2 bounds do
  not depend on the cycle entry phase fixed by the multiple-of-r_m choice.
- Initially-finite restriction: correctly disclaimed; rephasing at time 4 changes
  the displayed source, so no refutation of that narrower bound is implied.
- Nearest misses that are NOT flaws: (a) Theta surjectivity for arbitrary s --
  covered by the imported triangular-homeomorphism package; (b) Phi period
  divisibility -- standard locality, used correctly in the p|p(c) direction;
  (c) least-period preservation of the completion -- follows from minimality of r_m.

## Verdict

No fatal flaw found in the stated per-P construction (7) with its explicit
scope. The refutation of a universal period-dependent lower bound on the two
preperiods under hypotheses (7) stands as written. Nothing here proves or
refutes the still-open infinite-FULL-orbit or bounded-preperiod-orbit claims;
the note correctly marks those inconclusive. Problem 1 remains OPEN.
