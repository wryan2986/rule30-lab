# The forced-birth sensitive route reaches an exact 001/011 dichotomy at the previous cyclic source

Status: `partial-proof` / structural refinement. Problem 1 remains OPEN.

## Setup

Continue the two-bit nonreset source notation of `problem1_nonreset_return_birth_spacing.md` and `problem1_forced_birth_sensitive_route_reuses_prior_center.md`. Let the nonreset source be at even time `t`, and put `q=t+2`. The established return theorem says `Y_q` is cyclic with actual gate `t`, while `Y_(q+2)=Y_(t+4)` is cyclic with actual gate `u`. Run129 traced the forced birth at `t+6` back to the center 1 at `t+4`.

The question here is what the sensitive-1 route from that center does on the preceding two physical steps.

## Exact route from q+2 to q+1

FULL gives center values

    r_0(q)=1, r_0(q+1)=0, r_0(q+2)=1.

Because the cyclic source at `q` has actual gate `t`, its zero-pair flag is zero. Equation (5) of `problem1_shadow_gate_birth_phase.md` gives, for gate `t` (whose code symbol `b_1=1`),

    r_1(q) OR r_2(q) = 1.

Therefore

    r_1(q+1)
      = f(r_0(q),r_1(q),r_2(q))
      = 1 XOR (r_1(q) OR r_2(q))
      = 0.

Since the center at `q+2` is 1,

    1 = f(r_-1(q+1),0,0) = r_-1(q+1).

Thus the exact neighborhood producing the center at `q+2=t+4` is

    100,

and its unique sensitive 1-parent is the left neighbor `r_-1(q+1)=1`.

So the route does NOT go directly center-to-center from `t+4` to `t+2`; it shifts one cell left.

## One more step gives an exact 001/011 dichotomy

Now determine the neighborhood at time `q` that produces `r_-1(q+1)=1`. Its right input is the center `r_0(q)=1`. Rule 30 gives

    1 = f(r_-2(q), r_-1(q), 1)
      = r_-2(q) XOR 1,

so necessarily

    r_-2(q)=0.

Hence the producing neighborhood is exactly one of

    001  if r_-1(q)=0,
    011  if r_-1(q)=1.

These are precisely the two cases relevant to sensitive-1 provenance:

- in the `001` case, the unique sensitive 1-parent is the right input, namely the distinguished center `r_0(q)=1`; the route reconnects to the previous cyclic center at `t+2`;
- in the `011` case, neither 1-parent is sensitive, so the route terminates at the unique `011` obstruction identified in `problem1_sensitive_one_provenance_breaks_exactly_at_011.md`.

Therefore the complete source-relative alternative is

    center(t+4)
      <- r_-1(t+3)
      <- center(t+2)          if r_-1(t+2)=0,

or

    center(t+4)
      <- r_-1(t+3)
      <- 011 obstruction      if r_-1(t+2)=1.

## Consequence

This is sharper than merely extending the route. Every forced two-bit-nonreset birth now traces backward through the preceding `u` source and then reaches, at the earlier cyclic `t` source, a single binary fork controlled by the one actual cell `r_-1(t+2)`.

The provenance strategy can only yield a finite birth budget if this fork has additional cross-episode structure. Repeated `001` outcomes simply reconnect the lineage to an earlier cyclic center and permit reuse; repeated `011` outcomes terminate at creation events that are not generically scarce. The missing theorem is therefore no longer an arbitrary routed-provenance statement: it must show that the source-relative bits `r_-1(q)` across successive two-bit nonreset returns have a monotone/bounded-reuse relation to the finite original row, or that one branch of this dichotomy cannot recur indefinitely on the fixed FULL orbit.

No such relation is proved here.

Dependencies: `problem1_forced_birth_sensitive_route_reuses_prior_center.md`, `problem1_nonreset_return_birth_spacing.md`, `problem1_shadow_gate_birth_phase.md`, `problem1_sensitive_one_provenance_breaks_exactly_at_011.md`.
