# Run 184: beta=1 forces the original-cut front to cross the center at t+8

Status: `partial-proof`. Problem 1 remains OPEN.

## Setup

Continue the same sufficiently late one-bit gate-u nonresetting source at even physical time `t`, in the terminal branch `beta=1`.

Run 181 proved, writing `x=r_0(t+6)`, that at `t+6`

    d_0(t+6)=1,
    r_(-1)(t+6)=hat r_(-1)(t+6)=1,
    actual  (r_1,r_2)         = (0,1),
    shadow  (hat r_1,hat r_2) = (1,1),

and at `t+7`

    actual  (r_1,r_2)         = (1 XOR x,0),
    shadow  (hat r_1,hat r_2) = (x,0),
    m(t+7)=1,
    J(t+7)=t+8,
    s_(t+7)=t+7.

Run 183 correctly proved `d_1(t+8)=1`, but its subsequent inference from `J(t+8)<=t+9` to `s_(t+8)<=t+8` had the threshold direction reversed. The present note computes the missing center discrepancy exactly and corrects that consequence.

## The row-t+7 center cells are already determined

At `t+6`, write

    r_0(t+6)=x,
    hat r_0(t+6)=1 XOR x,

because `d_0(t+6)=1`. The shared left neighbor is the final residence eraser and equals 1. Rule 30 gives

    r_0(t+7)
      = 1 XOR (x OR r_1(t+6))
      = 1 XOR (x OR 0)
      = 1 XOR x,

while

    hat r_0(t+7)
      = 1 XOR ((1 XOR x) OR hat r_1(t+6))
      = 1 XOR ((1 XOR x) OR 1)
      = 0.

Thus the center/right-one pairs at `t+7` are

    actual  (r_0,r_1)         = (1 XOR x, 1 XOR x),
    shadow  (hat r_0,hat r_1) = (0, x).

This uses no cyclic-source birth law and no wider-right datum.

## The center discrepancy at t+8 is forced

Since `m(t+7)=1`, all positions `i<=0` agree at `t+7`, so in particular `d_(-1)(t+7)=0`. The ordinary discrepancy update at position 0 is

    d_0(t+8)
      = d_(-1)(t+7)
        XOR [(r_0 OR r_1) XOR (hat r_0 OR hat r_1)](t+7).

The two OR terms are

    (r_0 OR r_1)(t+7)         = 1 XOR x,
    (hat r_0 OR hat r_1)(t+7) = x.

Hence

    d_0(t+8)=0 XOR (1 XOR x) XOR x = 1.

A discrepancy cannot appear at a negative position in this step because every input in the neighborhoods of positions `i<0` lies at position `<=0`, where the two rows agree at `t+7`. Therefore

    m(t+8)=0,
    J(t+8)=t+8.

So the beta=1 terminal passage forces the same characteristic `t+8` front to move from physical position 1 at `t+7` to the center at `t+8`.

## Corrected residence consequence

The global-front residence identity is

    {u:J(u)=j}=[s_(j-1),s_j) intersect Z.

Since

    J(t+7)=t+8,
    J(t+8)=t+8,
    s_(t+7)=t+7,

characteristic `t+8` has a residence containing both `t+7` and `t+8`. In particular

    t+8 < s_(t+8),

and because `s_(t+8)` is integral,

    s_(t+8) >= t+9.

Therefore the original-cut increment satisfies

    Delta_(t+7)=s_(t+8)-s_(t+7) >= 2.

Equivalently, the physical delay at row `t+8` is certainly positive:

    tau(Y_(t+8))=max(s_(t+8)-(t+8),0) >= 1.

The renewal injection at `t+7` is also certainly positive:

    R_(t+7)
      = max(s_(t+8)-max(s_(t+7),t+8),0)
      = s_(t+8)-(t+8)
      >= 1.

This is substantially stronger than run 183's invalid conclusion `Delta_(t+7) in {0,1}`; that conclusion must not be reused.

## What this does and does not prove

The first time allowed by the eight-step spacing theorem is not merely a possible positive-delay row: in the `beta=1` branch, positive delay at `t+8` is forced, with a center crossing of the same global characteristic `t+8`.

This still does NOT prove a new nonresetting source at `t+8`. The remaining question is the actual core type there: resetting versus nonresetting (or cyclic, if applicable under the repository's source classification). No cyclic-source birth law was used above.

The useful next target is therefore no longer `d_0(t+8)`: it is the complete-core classification of `Y_(t+8)` under this forced positive-delay crossing. If the resetting endpoint cannot remain/reset again under the rigid local trace, then a new nonresetting source may be forced; if it can, isolate the complete driver selecting that branch.

Dependencies: `problem1_run181_beta_one_forces_tplus7_front.md`; `problem1_run183_gate_mismatch_forces_tplus8_discrepancy.md`; `problem1_global_discrepancy_front.md`.