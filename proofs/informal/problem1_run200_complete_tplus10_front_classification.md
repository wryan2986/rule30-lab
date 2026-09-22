# Problem 1 run 200 — complete corrected t+10 front classification

Status: `partial-proof`. Problem 1 remains OPEN.

Continue only the corrected run-193--199 chain. Run 199 left one case unresolved:

    p=1, w3=1,

where `w=A^4 z`, `(w0,w1,w2)=(0,p,p)`, and the zero low-A trace further gives `w4=w3` on the `p=1` branch.

Run 197 gives in this branch

    m(t+9)=-1, J(t+9)=t+8,
    d_-1(t+9)=1, d_0(t+9)=1.

Run 199 gives

    r_-2(t+9)=w3=1,

so `d_-2(t+10)=0`. It remained to decide whether the discrepancy at `-1` survives.

## 1. Compute the common cell r_-2(t+8)

For `p=1`, the complete driver `Y_(t+4)=16w+7` and the retained right prefix give the physical block needed for the four-step light cone of `r_-2(t+8)`:

    (r_-6,r_-5,r_-4,r_-3,r_-2,r_-1,r_0,r_1,r_2)(t+4)
      = (1,1,0,0,1,1,1,1,1).

Here `r_-6=w2=p=1`, `r_-5=w1=p=1`, `r_-4=w0=0`, the low `+7` suffix gives `00111` through position 0, and the retained beta=1 right prefix gives `r_1=r_2=1`.

Four literal Rule-30 updates on this finite light cone give

    r_-2(t+8)=0.

This calculation does not use `w3`; indeed the light cone begins at `r_-6(t+4)`.

Run 197 already gives `r_-1(t+8)=1 xor p=0` and `r_0(t+8)=0`. Hence

    r_-1(t+9)=F(0,0,0)=0.

Because `m(t+9)=-1`, actual and shadow agree at `-2`, differ at `-1`, and also differ at `0`. In the present `w3=1` branch the common left input at row `t+9` is `r_-2=1`; moreover the actual pair is

    (r_-1,r_0)=(0,0).

Since `d_-1=d_0=1`, the shadow pair is `(1,1)`. Therefore at position `-1` on the next row,

    actual: F(1,0,0)=1,
    shadow: F(1,1,1)=0,

so

    d_-1(t+10)=1.

Together with `d_-2(t+10)=0`, this fixes the unresolved front:

    p=1,w3=1 => m(t+10)=-1, J(t+10)=t+9.

## 2. Complete t+10 classification

Combining with run 199:

    p=0:
      J(t+9)=t+9,
      J(t+10)=t+9.

    p=1,w3=0:
      J(t+9)=t+8,
      J(t+10)=t+8.

    p=1,w3=1:
      J(t+9)=t+8,
      J(t+10)=t+9.

Thus every corrected branch through `t+10` is now classified. The first two cases give a two-row residence on a single characteristic; the `01111...` low-prefix branch advances from characteristic `t+8` to `t+9` between the two rows.

## 3. Structural consequence

The branching is not caused by arbitrary physical neighbors. It is selected by successive bits of the same complete cyclic driver `w=A^4z`:

- `p=w1` decides whether the `t+9` front is characteristic `t+9` or `t+8`;
- conditional on `p=1`, `w3` decides whether characteristic `t+8` persists through `t+10` or releases to `t+9`.

The zero scalar trace restricts the relevant prefixes to `000...`, `01100...`, and `01111...` through the currently exposed bits, but does not yet supply the finite-support charge needed to rule out infinitely many nonresetting returns.

No claim from invalidated runs 184--192 is used.

Dependencies: `problem1_run197_corrected_tplus9_front.md`, `problem1_run198_p_is_not_fixed_by_low_trace.md`, `problem1_run199_corrected_tplus10_front.md`.