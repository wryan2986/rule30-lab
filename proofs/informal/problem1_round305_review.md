# Round305 lead adversarial dispositions

Status: `partial-proof` for the scoped lead audits. This file is a LEAD
review, not an external review or a `rigorous-proof` assignment. Problem1
remains OPEN.

## 1. External review availability

Muse thread `01a07b36-d832-7f00-8d9d-b5d874a5cb16` was assigned a fresh
read-only adversarial review of the incoming global shadow and transient
phase formula while the lead studied the next bottleneck. It failed before
review text with `MissingSessionID`, reporting a missing
`x-opencode-session` in provider routing. The thread was CLOSED.
This was not429, so no rate-limit retry/fallback rule was triggered.
MiMo was not among the advertised model overrides. No other provider or
native subagent was substituted, and no provider settings were changed.
External review remains missing for the incoming notes and this round.

## 2. Full-driver phase-summary obstruction

Audited claim: the function H in
`problem1_full_driver_phase_memory_obstruction.md` Section1 does not exist
on all finite rows, even with two successive attached zero bits.

Adversarial checks:

1. The summaries must agree on the COMPLETE core, not merely its low word
   or clock. Both sources110/112 have phase-zero core111 and exact delay1,
   from their common image100 and the two-cycle100/111. Choosing first cycle
   entry100 as the representative would be wrong.
2. The source phase maps agree on BOTH possible appended bits. The cyclic
   source's low trace visits1, so it has a unique cyclic lift. The core222
   is cyclic and projects to111, proving F(a)=0 for each source and each a.
3. The actual appended bit is the same0. The child words220/224 both have
   core222, but their onset times3/1 differ. Their full traces through those
   onsets are retained, including the two late low1s in the220 transient.
4. Product-formula calculations give child maps0 and a XOR1. The separate
   scalar OR derivation gives exactly the same maps, without using that
   product formula. Both child zero branches therefore really differ.
5. Grandchildren444/445 are different PHASES on the same period4 cycle.
   No new distinct-cycle fork is claimed, and clock equality cannot repair
   the failed summary update.
6. The domain is all finite rows, not a hypothetical FULL subset. Neither
   source pair nor its attached zeros is asserted to realize an infinite
   FULL spacetime. The counterexample does not refute an independently
   justified FULL-only update or every augmented summary.

Fixed check: `check_round305_phase_transport.py` verifies14 hand edges,
14 closed cycle certificates, the four two-valued phase maps, and8
product/scalar comparisons at minimal and extended horizons. Every packed
edge agrees with independent Boolean cells. It completed within the
10-second/128MiB caps. The immutable reference hash is checked, and the
atomic JSON supplies full Git/source/payload provenance. These are fixed
controls, not a source census or machine proof of the imported lift theorem.

Disposition: accept `refuted` for exactly the stated general update;
accept `finite-exhaustive` for exactly the declared checks. No FULL bound,
all-depth exclusion, or independent-external-review claim is assigned.

## 3. Sharp width-delay bound

Audited claim: tau(y)<=bitlen(y)-1 for every positive finite y is false.
The frozen pre-run admission is `problem1_width_delay_bound_test.md`;
the outcome is `problem1_width_delay_bound_obstruction.md`.

The complete144 certificate has ten distinct rows before its first repeat:
eight transient rows followed by200/222. This proves exact delay8, width8,
period2 and phase-correct core200. The five new prefix edges have an
explicit arithmetic table; the suffix agrees with the earlier220 control.
Both independent orbit implementations agree on each checked input1..144.
The search stops at144 rather than increasing the bound or fitting a new
constant. The record's `finite-exhaustive` status is confined to that
declared interval; the all-depth proposed inequality is `refuted` by144.

The bridge to a physical orbit is checked at EXACTLY one time:
144=2^4*9 and A^4(144)=205 with delay4. The original right fringe is zero
and unchanged, but seed9 is not FULL (its first two centers are1,1).
This finite event cannot refute an eventual or a FULL-conditioned bound.
Nor does it refute every width-plus-constant estimate. Those fences are
load-bearing. External review is missing; this is a lead audit only.

## 4. Global discrepancy front and path parity

Fresh Muse thread `01a07b59-b4da-70d2-8671-c445e57100a3` was assigned the
written front note, with explicit instructions to find offset errors and
finite-to-infinite gaps. It also failed before review text with the same
MissingSessionID provider error, and is CLOSED. This was not429; no fallback
or configuration change occurred. No external review is claimed.

Lead audit of `problem1_global_discrepancy_front.md`:

1. The s_j are delays of ORIGINAL cuts for all integer j. They are not
   physical delays tau(Y_j). Monotonicity, finiteness of every s_j, zero
   values sufficiently far left, and imported divergence to the right are
   exactly what make J(u) finite for every u and unbounded over time.
2. At cut j-u, agreement of actual and shadow WHOLE left prefixes is
   equivalent to s_j<=u. The first failure is therefore a differing LOW bit
   with every bit strictly left agreeing. This proves m=J-u, rather than
   merely locating some difference in a cone.
3. Residence endpoints are s_(j-1) inclusive and s_j exclusive. For the
   last occupied time s_j-1 the neighbor at j-s_j is1 and kills the front
   on the NEXT update. This accounts for the eraser's time-minus-one.
4. Direct substitution in the physical renewal yields R_t as the positive
   part of s_(t+1)-max(s_t,t+1). Its entire interval is a SUBINTERVAL of
   one residence; early residence before center crossing is not counted.
5. The finite counting formula handles N<s_0, s_N<N, s_N>=N and N=0.
   Its set proof needs no subtraction of infinite quantities. The old
   telescoping formula is recovered as a consistency check, not advertised
   as a new stronger estimate.
6. Doubling forces equality of adjacent ORIGINAL onsets by the permutation
   lift case. Thus the skipped-characteristic statement holds at every
   physical time. The converse is not asserted: an empty residence need
   not be a clock doubling. No bound on clock skips per front jump follows.
7. The OR-difference identity expands to the same GF(2) polynomial on both
   sides. In characteristic coordinates the parent indices are j-2,j-1,j.
   This gives the cone j-2u..j and, at a residual, the earlier exact cone
   -t-1-2T..t+1. Coefficients retain the full actual AND shadow histories.
8. Swapping the mixed-coefficient factorization changes the right-hand
   side by two equal products, which cancel in GF(2). The112 hand control
   independently checks actual/shadow cancellation and factorization
   dependence. No positive-path or unique-ancestor interpretation is used.

Disposition: accept `partial-proof` for the scoped all-depth construction,
residence/injection correspondence and full-driver parity identity. This
does not prove a finite occupation budget, finite ancestor supply, bounded
reuse, a FULL exclusion, or an autonomous update at a front reset. No new
experiment was needed for these algebraic and counting arguments.
