# Run 182: beta=1 post-terminal gate flags are complementary

Status: `partial-proof`. Problem 1 remains OPEN.

## Setup

Continue the same sufficiently late one-bit gate-u nonresetting source at even physical time `t`, in the terminal branch `beta=1`.

Run 180 proved at row `t+6`

    actual  (r_1,r_2)       = (0,1),
    shadow  (hat r_1,hat r_2) = (1,1).

Run 181 then used the exact global front to prove

    m(t+7)=1,   J(t+7)=t+8,

and, writing

    x = r_0(t+6),

proved the row-`t+7` right pairs

    actual  (r_1,r_2)       = (1 XOR x, 0),
    shadow  (hat r_1,hat r_2) = (x, 0).                 (1)

The question left by run 181 was whether the complete resetting-core classification fixes `x`.

## Exact gate consequence without fixing x

Let `u(v_1,v_2)` denote the nonzero-pair gate flag: it is 0 exactly for pair `00`, and 1 otherwise.

From (1), if `x=0`, then

    actual pair = 10, shadow pair = 00,

while if `x=1`, then

    actual pair = 00, shadow pair = 10.

Therefore in both cases the two gate flags are complementary:

    u_actual(t+7) = 1 XOR x,
    u_shadow(t+7) = x,

and hence

    u_actual(t+7) XOR u_shadow(t+7) = 1.              (2)

Thus `x` is not needed to know the relative gate state on the first post-terminal row. The original global shadow and actual orbit have opposite zero-pair flags there, unconditionally.

This is stronger than merely retaining the position-1 discrepancy: the discrepancy is gate-visible at `t+7` even though which side carries the zero pair depends on `x`.

## Why this does not yet force a birth

The cyclic-source birth law cannot be applied at `t+7`. The beta=1 endpoint at `t+6` is a resetting one-bit t-source, not a cyclic source, and run 181 does not prove cyclicity at `t+7`. Equation (2) is therefore a gate-state classification only; treating it as a new injection/birth event would be an invalid reuse of the cyclic birth law.

Likewise, the existing complete-core statement for the beta=1 endpoint says that the row `t+6` core is resetting because its A-time-1 code equals the actual gate symbol 1. It does not, in the currently proved source theorem, specify the physical center bit `x=r_0(t+6)`. No inference fixing x is made here.

## Consequence and next target

The first candidate time not excluded by the eight-step nonresetting-source spacing is `t+8`. Any continuation to that candidate must therefore start from the unconditional gate mismatch (2), not from an arbitrary gate pair and not from an assumed value of x.

The remaining useful question is whether the resetting-core A-trace at `t+6` determines enough of row `t+7` (in particular the center/left driver) to transport (2) to `t+8`, or whether a genuinely wider complete-driver datum first enters there.

Dependencies: `problem1_run180_terminal_shadow_pair_is_rigid.md`; `problem1_run181_beta_one_forces_tplus7_front.md`; `problem1_nonreset_return_birth_spacing.md`; `problem1_shadow_gate_birth_phase.md`.
