# The forced two-bit nonreset birth has a two-step sensitive-1 route to the prior cyclic center

Status: `partial-proof` / structural no-go for the simplest sensitive-1 charging proposal. Problem 1 remains OPEN.

## Setup

Use the fixed actual FULL orbit and notation of `problem1_nonreset_return_birth_spacing.md`. Let `t` be an even two-bit nonresetting source (`u=0`). Put `q=t+2`. The established return theorem gives:

- `Y_q` is cyclic and its actual gate is `t`;
- `Y_(q+2)=Y_(t+4)` is cyclic and its actual gate is `u`;
- the shadow return pair at `q` is `10`, hence the cyclic-source birth indicator at `t+4` is `beta=1`;
- therefore `tau(Y_(t+6))=1`, and the row at `t+6` is a one-bit `t` source.

The run128 note classified backward Boolean-sensitive 1-provenance: every Rule-30 output 1 has a sensitive 1-parent except output neighborhood `011`. The question was whether this particular forced birth immediately encounters that obstruction.

## Exact two-step route

At the cyclic `u` source time `s=t+4`, the actual right-pair zero flag is one, so

    (r_1(s), r_2(s)) = (0,0).

FULL has center values `r_0(s)=1`, `r_0(s+1)=0`, `r_0(s+2)=1` at these even/odd/even times.

First update the first right cell:

    r_1(s+1)
      = f(r_0(s), r_1(s), r_2(s))
      = f(1,0,0)
      = 1.

Now the center at `s+1` is zero and the center at `s+2` is one. Therefore

    1 = r_0(s+2)
      = f(r_-1(s+1), 0, 1).

Since `f(l,0,1)=1 XOR l`, this forces

    r_-1(s+1)=0.

Hence the exact center neighborhood producing the forced birth cell is

    (r_-1(s+1), r_0(s+1), r_1(s+1)) = 001.

By the run128 sensitivity classification, the unique sensitive 1-parent in `001` is its right input. Thus the forced actual center 1 at `s+2=t+6` routes backward to `r_1(s+1)=1`.

But that intermediate 1 itself was produced by the exact neighborhood `100` at time `s`, whose unique 1-parent is its left input. Therefore its sensitive-1 route goes backward once more to

    r_0(s)=r_0(t+4)=1.

So the complete first two backward steps are

    center 1 at t+6
        <- sensitive right 1 at (position 1, t+5)
        <- sensitive left 1 = center 1 at t+4.

No `011` obstruction occurs in these two steps.

## Consequence

This is useful but points against the simplest birth-counting interpretation of sensitive-1 provenance. The forced `beta=1` cell is not, in these first two steps, attached to a new sensitive-1 lineage: it canonically reconnects to the already-existing cyclic center 1 two physical steps earlier.

Therefore a charge of each forced birth merely to the endpoint of its local sensitive-1 route does not yet create distinct labels or consume a finite original-support resource. To obtain a finite birth budget, one would have to continue the route backward from the cyclic center at `t+4` and prove a cross-episode advancement/bounded-reuse theorem. The local forced-birth segment itself provides reuse, not advancement.

This also sharpens the run128 `011` question. For the forced birth itself, `011` is definitely avoided through the entire two-step segment back to the preceding cyclic source. Any `011` termination relevant to this provenance strategy must occur earlier than `t+4`.

## Next target

Trace sensitive-1 provenance backward from the cyclic center at `t+4` through the preceding cyclic `t` source at `t+2` and the completed nonreset return. Determine whether the route is forced into a source-relative `011`, or whether it reaches an earlier distinguished center/source. The admission criterion is a genuine cross-episode ordering or bounded-reuse statement; merely extending the route without such structure is not enough.

Dependencies: `problem1_sensitive_one_provenance_breaks_exactly_at_011.md`, `problem1_nonreset_return_birth_spacing.md`, `problem1_shadow_gate_birth_phase.md`.
