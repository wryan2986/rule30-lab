# Problem 1 run 191: exact t+9 front trichotomy after the forced resetting t+8 passage

Status: exact local/global-front continuation; Problem 1 remains open.

## Starting point

Run 189 forces, on the beta=1 return trajectory,

\[
(r_0,r_1,r_2,r_3)(t+7)=0000,
\]

and the original global shadow has

\[
(\hat r_0,\hat r_1,\hat r_2)(t+7)=(0,1,0).
\]

Run 184 proves `m(t+8)=0`, while run 190 proves that the positive-delay row at `t+8` is resetting rather than a nonresetting source.

The next question is how the global discrepancy front exits this resetting passage.

## Retain only the two shared cells immediately left of the rigid block

Because `m(t+7)=1`, actual and shadow agree at every position `<=0`. Write

\[
A=r_{-2}(t+7)=\hat r_{-2}(t+7),\qquad
B=r_{-1}(t+7)=\hat r_{-1}(t+7).
\]

Since the common center at `t+7` is zero, Rule 30 gives the common cell at position `-1` on row `t+8` as

\[
c:=r_{-1}(t+8)=\hat r_{-1}(t+8)=A\oplus B.
\]

At the center, the actual neighborhood is `(B,0,0)` whereas the shadow neighborhood is `(B,0,1)`. Hence

\[
r_0(t+8)=B,\qquad \hat r_0(t+8)=1\oplus B.
\]

This rederives `d_0(t+8)=1` and identifies the two actual/shadow center values exactly.

Also, from the rigid actual/shadow right triples at `t+7`,

\[
r_1(t+8)=0,\qquad \hat r_1(t+8)=1.
\]

Thus the row-`t+8` local data needed for the next discrepancy update are

\[
\text{actual}: (r_{-1},r_0,r_1)=(A\oplus B,B,0),
\]
\[
\text{shadow}: (\hat r_{-1},\hat r_0,\hat r_1)=(A\oplus B,1\oplus B,1).
\]

## Exact discrepancy update to t+9

At position `-1`, all positions further left agree at `t+8`, so

\[
d_{-1}(t+9)
 =[(c\lor B)\oplus(c\lor(1\oplus B))].
\]

This equals `1` exactly when `c=0`. Therefore

\[
\boxed{d_{-1}(t+9)=1\oplus(A\oplus B)}.
\]

At position `0`, since `d_{-1}(t+8)=0`,

\[
d_0(t+9)
 =(B\lor0)\oplus((1\oplus B)\lor1)
 =1\oplus B.
\]

At position `1`, use `d_0(t+8)=1`, actual `(r_1,r_2)=(0,0)`, and `\hat r_1(t+8)=1`; regardless of `\hat r_2(t+8)`, the shadow OR is one. Hence

\[
d_1(t+9)=1\oplus[0\oplus1]=0.
\]

So

\[
\boxed{d_1(t+9)=0}
\]

unconditionally.

## Front trichotomy

The two shared bits `(A,B)` now give only three distinct front outcomes.

1. If `A=B`, then `d_{-1}(t+9)=1`. No discrepancy can occur further left in one step, so

\[
\boxed{m(t+9)=-1,\qquad J(t+9)=t+8.}
\]

Thus characteristic `t+8` remains the global front for a third consecutive physical row `t+7,t+8,t+9`, forcing

\[
\boxed{s_{t+8}\ge t+10,\qquad \Delta_{t+7}\ge3.}
\]

2. If `(A,B)=(1,0)`, then `d_{-1}=0` and `d_0=1`, so

\[
\boxed{m(t+9)=0,\qquad J(t+9)=t+9.}
\]

In this branch the characteristic-`t+8` residence ends exactly before `t+9`, hence

\[
\boxed{s_{t+8}=t+9,\qquad \Delta_{t+7}=2.}
\]

3. If `(A,B)=(0,1)`, then

\[
d_{-1}(t+9)=d_0(t+9)=d_1(t+9)=0.
\]

Therefore the first discrepancy, if present, is at position at least `2`:

\[
\boxed{m(t+9)\ge2,\qquad J(t+9)\ge t+11.}
\]

This branch skips characteristic `t+9` (and possibly further characteristics) at the global front. The residence identity permits such a jump only through zero-length intervening residences.

## Consequence and next target

The exit of the forced resetting `t+8` passage is controlled entirely by the two shared cells immediately to the left of the rigid `0000` block at `t+7`; no wider-right data enter the first two front tests.

The useful next target is therefore to transport the already-retained complete beta=1 return driver far enough to determine or constrain

\[
(A,B)=(r_{-2},r_{-1})(t+7).
\]

In particular, proving `A=B` would lengthen the forced residence to at least three rows, while proving `(A,B)=(1,0)` would determine the resetting exit exactly. The exceptional `(0,1)` branch produces a front jump and should be checked against the threshold/finite-entry constraints before doing wider local propagation.

Dependencies: `problem1_run184_beta_one_forces_tplus8_center_crossing.md`; `problem1_run189_terminal_center_is_forced_one.md`; `problem1_run190_tplus8_cannot_be_nonresetting.md`.
