# Run 198: the corrected t+9 branch bit is not fixed by the zero low A-trace

Status: `partial-proof` / obstruction note. Problem 1 remains OPEN.

Continue only the corrected run-193--197 chain. Run 197 reduced the corrected front at physical time `t+9` to

    p := r_-5(t+4) = bit_1(A^4 z),

with

    p=1 => m(t+9)=-1, J(t+9)=t+8,
    p=0 => m(t+9)= 0, J(t+9)=t+9.

The proposed next step was to test whether the defining nonresetting condition on the original complete core `z` forces `p`.

## Exact consequence of the zero low A-trace

Put

    w := A^4 z.

Because `z` is a nonresetting core, its low A-trace is identically zero. In particular

    w[0]=0,
    (A w)[0]=0.

The established low-bit rule for A is

    (A Q)[0] = Q[2] xor (Q[1] or Q[0]).

Therefore

    0 = (A w)[0]
      = w[2] xor (w[1] or 0)
      = w[2] xor w[1].

Since `p=w[1]`, the trace condition gives exactly

    w[2]=p.

Thus the first three low bits of `A^4 z` are

    (w[0],w[1],w[2]) = (0,p,p).

Equivalently the two locally admissible prefixes are `000` and `011`.

## Why this does not determine p

The low-trace equation at the next A-time does not set `w[1]`; it equates the next required bit with it. The zero-trace condition used in run 196 fixed `bit_0(A^4 z)=0`, hence `r_-4(t+4)=0`, but its next instance constrains a different spatial bit rather than forcing `bit_1(A^4 z)`.

This is consistent with the earlier nonresetting-core return proof: its Section 3 uses the same zero-trace recurrence to force a shared bit4 during the two-bit transient, but nowhere supplies a theorem that every higher neighboring bit of a zero-low-trace cyclic core is zero. Treating `p` as zero would therefore be an unjustified strengthening of `N_t`.

No claim is made here that both prefixes extend to an actual infinite FULL survivor. The result is narrower: the retained defining low-A-trace identity, by itself, does not choose the run-197 branch.

## Useful reformulation for the next step

Any successful attempt to eliminate one branch must use information beyond the scalar condition `N_t`: the complete cyclic code/phase of `z`, the FULL code constraints, or a global threshold/front identity. The corrected local branch can now be carried as

    A^4 z low prefix = 000...  <=> p=0,
    A^4 z low prefix = 011...  <=> p=1.

Do not revive the invalidated run-184--192 trajectory claims.

Dependencies: `problem1_nonresetting_core_returns.md`, `problem1_nonreset_return_birth_spacing.md`, and `problem1_run197_corrected_tplus9_front.md`.
