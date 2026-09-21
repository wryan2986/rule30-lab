# Run 183: the post-terminal gate mismatch forces a discrepancy at t+8

Status: `partial-proof`. Problem 1 remains OPEN.

## Setup

Continue the same sufficiently late one-bit gate-u nonresetting source at even physical time `t`, in the terminal branch `beta=1`.

Run 181 proved, writing `x=r_0(t+6)`, that at row `t+7`

    actual  (r_1,r_2)         = (1 XOR x, 0),
    shadow  (hat r_1,hat r_2) = (x, 0),
    m(t+7)=1,
    J(t+7)=t+8,
    s_(t+7)=t+7.

Run 182 observed that the zero-pair/nonzero-pair gate flags of these two right pairs are complementary. The present step uses that mismatch directly in the ordinary Rule-30 discrepancy update; it does NOT invoke the cyclic-source birth law.

## Exact discrepancy transport to t+8

Rule 30 is

    F(l,c,r)=l XOR (c OR r).

For actual/shadow rows, let `d_i=r_i XOR hat r_i`. Therefore

    d_i(next)
      = d_(i-1) XOR [(r_i OR r_(i+1)) XOR
                     (hat r_i OR hat r_(i+1))].       (1)

At row `t+7`, `m=1`, so position 0 agrees:

    d_0(t+7)=0.                                      (2)

For `i=1`, the two OR terms in (1) are exactly the nonzero-pair flags of the actual and shadow pairs. From the explicit pairs above,

    (r_1 OR r_2)(t+7) = 1 XOR x,
    (hat r_1 OR hat r_2)(t+7) = x.

Their XOR is therefore 1, independently of `x`. Combining with (1)-(2),

    d_1(t+8)=1.                                      (3)

Thus the unresolved center bit at `t+6` cannot erase the post-terminal discrepancy by `t+8`: position 1 is certainly still discrepant.

Equivalently,

    m(t+8) <= 1,
    J(t+8) <= t+9.                                   (4)

Using the characteristic-front residence identity, (4) implies

    s_(t+8) <= t+8.

Run 181 gave `s_(t+7)=t+7`, and monotonicity of `s` gives

    t+7 <= s_(t+8) <= t+8.                           (5)

Hence the next original-cut increment is restricted to

    Delta_(t+7)=s_(t+8)-s_(t+7) in {0,1}.            (6)

## What remains unresolved

This does not determine whether `m(t+8)=0` or `1`, because `d_0(t+8)` depends on the center/left neighborhood at row `t+7`. In particular, the complete resetting-core data currently imported do not fix the physical center `x=r_0(t+6)` or the row-`t+7` center pair strongly enough to decide `d_0(t+8)`.

The useful point is that no wider right-tail datum is needed to prove persistence at position 1. The first candidate new nonresetting-source time `t+8` therefore cannot begin from complete actual/shadow agreement near the gate: it inherits a forced position-1 discrepancy from the beta=1 terminal passage.

Do not interpret (3) as a birth. No cyclicity at `t+7` or `t+8` has been proved.

## Next target

Classify `d_0(t+8)`. If it is forced to 0, then `m(t+8)=1` and `J(t+8)=t+9` exactly. If it can be 1, isolate the complete-driver condition selecting the two branches and compare that condition with the nonresetting-source criterion at `t+8`.

Dependencies: `problem1_run181_beta_one_forces_tplus7_front.md`; `problem1_run182_post_terminal_gate_flags_are_complementary.md`; `problem1_global_discrepancy_front.md`.
