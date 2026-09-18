# The forced two-bit nonreset birth has a three-cell local forcing cone

Status: `partial-proof` / structural no-go. This note refines the backward-certificate proposal from run119. It does not prove a finite birth budget or exclude FULL. Problem 1 remains OPEN.

## 1. Setup

Use the notation and hypotheses of `problem1_nonreset_return_birth_spacing.md`. At an even nonresetting source time t, with source type u, the selected global shadow satisfies

    shadow cells (-2,-1,0,1,2) = (u,u,0,u,1).

Let q=t+2. The established return identity is

    (hat r_1(q),hat r_2(q)) = (1, u*(a OR b)),

where a=hat r_3(t), b=hat r_4(t). In the two-bit source case u=0, the later cyclic u-source at q+2 has birth indicator beta=1 because hat r_2(q)=0.

Run119 proposed expanding this forcing event backward rather than assigning the resulting 1-cell a canonical parent.

## 2. Exact backward cone

For u=0, the only source-time shadow cells needed to force hat r_2(q)=0 are

    (hat r_0(t),hat r_1(t),hat r_2(t)) = (0,0,1).       (1)

Indeed Rule 30 is f(l,c,r)=l XOR (c OR r). At t+1,

    hat r_1(t+1) = f(0,0,1) = 1,
    hat r_2(t+1) = f(0,1,a) = 1,

independently of a. Therefore at t+2,

    hat r_2(q)
      = f(hat r_1(t+1),hat r_2(t+1),hat r_3(t+1))
      = f(1,1,*)
      = 0,                                             (2)

independently of every deeper shadow cell, including a and b.

Thus the wider-driver cancellation in the existing formula is not merely algebraic: the complete dependency certificate for the zero flag responsible for this forced birth collapses to the three-cell source-relative word 001.

The first returned bit is likewise forced locally:

    hat r_1(q)=1,

so the return right pair is exactly 10. Equation (2), combined with the already-proved cyclic-source birth law at q+2, gives beta=1.

## 3. Consequence for characteristic charging

This closes the most immediate version of the run119 forcing-set strategy. The forcing mechanism does not expose a growing or source-specific deeper set: every admitted two-bit nonreset source has the same source-relative shadow motif 001 and that motif alone forces the later zero flag. Expanding the physical dependency cone farther right cannot distinguish successive such births, because those cells are provably irrelevant to (2).

This is NOT a proof that successive occurrences reuse the same physical cells or the same time-zero ancestors. Source-relative copies of 001 occur at different spacetime locations. Therefore one cannot infer an infinite compatible FULL orbit, nor can one infer failure of every characteristic budget.

What is ruled out is narrower and useful: a finite birth budget cannot come from assigning the forced beta=1 event to additional right-shadow cells in its minimal local backward cone. There are no such required cells. Any nonrenewable charge must attach to information that is not needed to determine the local birth bit itself: for example the global provenance of the selected shadow, source/history identity, the complete core, or a characteristic continued backward beyond the minimal Boolean forcing certificate.

## 4. Next target

If characteristic charging is retained, explicitly distinguish a *causal ancestry certificate* from a *minimal forcing certificate*. The latter is now exhausted by 001. The former must continue the three source-time cells in (1) backward through the globally selected shadow and prove a monotone ordering or bounded reuse of their time-zero provenance. Without such a provenance theorem, further local cone expansion is a dead end.

Dependencies: `problem1_nonreset_return_birth_spacing.md`, `problem1_shadow_gate_birth_phase.md`, and `problem1_canonical_backward_birth_certificate_has_no_unique_parent.md`.
