# Problem 1 run 189: the beta=1 terminal center bit is forced to one

Status: proved correction/rigidification; Problem 1 remains open.

## Starting point

Runs 181 and 188 leave the beta=1 terminal center bit

\[
x=r_0(t+6)
\]

apparently unresolved.  But run 181 already contains enough information to determine it.

At physical row `t+6` the same original global shadow satisfies

\[
r_{-1}=\hat r_{-1}=1,
\qquad r_0=x,
\qquad \hat r_0=1\oplus x,
\]

and the rigid right pairs are

\[
(r_1,r_2)=(0,1),
\qquad
(\hat r_1,\hat r_2)=(1,1).
\]

Run 181 also proved from the final-residence eraser that

\[
d_0(t+7)=0,
\qquad m(t+7)=1.
\]

## Direct Rule-30 calculation forces x

Use Rule 30 as

\[
F(L,C,R)=L\oplus(C\lor R).
\]

For the actual center at `t+7`,

\[
r_0(t+7)
 =1\oplus(x\lor0)
 =1\oplus x.
\]

For the shadow center,

\[
\hat r_0(t+7)
 =1\oplus((1\oplus x)\lor1)
 =0.
\]

Therefore

\[
d_0(t+7)=r_0(t+7)\oplus\hat r_0(t+7)=1\oplus x.
\]

But the independently proved final-residence eraser gives `d_0(t+7)=0`. Hence

\[
\boxed{x=1}.
\]

So the terminal center bit was never a genuine free branch.

## Immediate rigidification

Substituting `x=1` into run 181 gives at `t+7`

\[
(r_0,r_1,r_2)=(0,0,0),
\qquad
(\hat r_0,\hat r_1,\hat r_2)=(0,1,0).
\]

Run 188 proved

\[
\alpha=1\oplus x,
\]

where `alpha` is the gate-u indicator of the actual row at `t+8`. Therefore

\[
\boxed{\alpha=0}.
\]

Using run 185's local expression

\[
\alpha=(1\oplus x)\oplus r_3(t+7),
\]

we also get

\[
\boxed{r_3(t+7)=0}.
\]

Thus the actual post-terminal row has the rigid four-cell block

\[
\boxed{(r_0,r_1,r_2,r_3)(t+7)=(0,0,0,0)}.
\]

At `t+8` its right pair is consequently

\[
\boxed{(r_1,r_2)(t+8)=(0,0)},
\]

so the actual gate there is definitely gate `t`, not merely conditionally selected by an unresolved center bit.

## Consequence if t+8 is nonresetting

The remaining classification question is whether the forced positive-delay row at `t+8` is nonresetting. If it is, run 185 now has only one possible branch:

\[
\boxed{\text{two-bit gate-}t,\quad \tau(Y_{t+8})=2,\quad \Delta_{t+7}=3.}
\]

The one-bit gate-u candidate is impossible in the beta=1 return trajectory.

Equivalently, under the nonresetting hypothesis,

\[
s_{t+8}=t+10.
\]

## Correction to earlier handoffs

Runs 181, 186, 187, and 188 treated `x` (or an equivalent left-pair XOR) as an unresolved datum. That is unnecessarily weak. The eraser identity used in run 181, combined with the direct center update already written explicitly in run 184, forces `x=1` immediately. Future work should not branch on `x`.

No cyclic-source birth law is used here at the resetting endpoint.

## Next target

The scalar/local branch is now fully rigid through the `t+8` gate. The remaining issue is structural: prove or disprove that the forced positive-delay gate-t row at `t+8` is a new nonresetting source. If it is nonresetting, its width, delay and residence increment are already fixed as above. If it is resetting, identify the complete-core condition permitting that reset despite the rigid `0000` post-terminal block.

Dependencies: `problem1_run181_beta_one_forces_tplus7_front.md`; `problem1_run185_tplus8_nonreset_candidate_has_exact_delay.md`; `problem1_run188_alpha_is_complement_terminal_center.md`.
