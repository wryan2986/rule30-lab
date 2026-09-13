# Exact classifier for one-bit lifts over a periodic Rule-30 core

Status: `partial-proof`. This note exactly classifies the least preperiod of an arbitrary one-bit lift of a finite A-periodic state. Applied after `problem1_transient_stripping_zero_extensions.md`, it converts the remaining skip-phase obstruction into one explicit initial-bit/recurrent-phase test. It does **not** prove that the actual FULL-tail phase always passes that test, and it does not close Problem 1.

## 0. Purpose

At a zero-extension skip, transient stripping gives periodic states

    x_0, x_1,

with `sigma(x_1)=x_0`, while the next state `x_2` is an arbitrary one-bit lift of the periodic core `x_1` selected by the post-transient phase. The previous note reduced two-step ledger compensation to

    tau(x_2) >= 2.

The missing point was how `tau(x_2)` depends on that exposed bit. For Rule 30 this dependence is only a two-state periodically driven recurrence, and it can be solved exactly.

## 1. One-bit lift recurrence

Use the reviewed integer form

    A = sigma^2 T,
    T(q) = q XOR ((q<<1) OR (q<<2)).

Equivalently, if `q_i=bit_i(q)`, then

    bit_i(A(q)) = q_(i+2) XOR (q_(i+1) OR q_i).      (1)

Let `z>0` be A-periodic, and let

    z_s = A^s(z).

Write its two lowest traces as

    b_s = bit_0(z_s),
    c_s = bit_1(z_s).                                (2)

Take either one-bit lift

    w = 2z + a_0,   a_0 in {0,1}.

Because Rule 30 commutes with deletion of the lowest bit,

    sigma(A^s(w)) = z_s.

Hence there is a unique scalar `a_s in {0,1}` with

    A^s(w) = 2 z_s + a_s.                            (3)

Applying (1) at the lowest output bit gives exactly

    a_(s+1) = c_s XOR (b_s OR a_s).                  (4)

Thus each time step acts on the exposed bit by one of only three maps:

    if b_s=1: a -> 1 XOR c_s,                        (5a)
    if b_s=0,c_s=0: a -> a,                          (5b)
    if b_s=0,c_s=1: a -> 1-a.                        (5c)

The `b_s=1` steps are erasers: they forget the incoming lift bit completely. All `b_s=0` steps are bijections on the two possible lift bits.

## 2. Exact preperiod classifier

Let `p` be any period of the forcing pair `(b_s,c_s)`; for example the least A-period of `z`.

### Case I: the low trace never contains 1

If

    b_s=0 for every s,                               (6)

then every map in (4) is a bijection (`identity` or `toggle`). Over one forcing period the return map on `{0,1}` is therefore either the identity or the toggle. In the first case each lift-bit trajectory is p-periodic; in the second it is 2p-periodic. In either case the full lifted state (3) is periodic from time zero. Therefore

    tau(2z)=tau(2z+1)=0.                             (7)

### Case II: the low trace contains 1

Assume now that `b_s=1` somewhere in each period. Since one step of the period is an eraser, the p-step return map on `{0,1}` is constant. Consequently there is a unique bi-infinite/recurrent periodic response

    r_s in {0,1},
    r_(s+1)=c_s XOR (b_s OR r_s),                    (8)

with the same forcing phase (its least period may divide or multiply the chosen presentation period only through the forcing phase; the corresponding full lifted state is on the unique recurrent lift cycle over `z`).

Let

    q = min{s>=0 : b_s=1}.                           (9)

Then:

- if `a_0=r_0`, the lift starts on that recurrent cycle, so

      tau(w)=0;                                      (10)

- if `a_0!=r_0`, every step before q is bijective, so the two scalar trajectories remain distinct through time q; the eraser at step q sends both to the same value at time q+1. Thus the lifted trajectory first reaches the recurrent cycle exactly at q+1, and

      tau(w)=q+1.                                    (11)

The word `exactly` is justified because a state off the recurrent lift cycle cannot itself be periodic: its forward orbit collides with the recurrent orbit at the eraser, whereas a point on a deterministic cycle cannot first merge into a different earlier trajectory.

Combining the cases gives a complete classifier:

> For a one-bit lift `w=2z+a_0` of an A-periodic state `z`, either the low A-trace of `z` is identically zero and every lift is periodic, or the low trace has an eraser and there is exactly one recurrent initial lift bit `r_0`. The recurrent bit gives `tau(w)=0`; the other bit gives `tau(w)=q+1`, where q is the first time the low trace of z equals 1.

## 3. Exact consequence at a zero-extension skip

Use the transient-stripping setup at tower index n:

    y=2^n v,
    H=tau(y),
    x_m=A^H(2^m y).

At a skip,

    delta_n=0,
    tau(x_1)=0,

so set

    z=x_1,
    w=x_2.

The previous splitting identity gives

    delta_n + delta_(n+1) = tau(x_2),

and therefore, since `delta_n=0`,

    delta_(n+1)=tau(x_2).                            (12)

The two-step residence-ledger contribution beginning at the skip is

    (delta_n-1)+(delta_(n+1)-1)
      = tau(x_2)-2.                                  (13)

Apply the classifier to the actual lift bit `a_0=bit_0(x_2)` over `z=x_1`.

If the low A-trace of `x_1` is identically zero, then

    tau(x_2)=0,

so the next characteristic is skipped as well and the two-step ledger is

    -2.                                              (14)

If the low trace contains 1, let `r_0` be its unique recurrent lift bit and let

    q=min{s>=0:bit_0(A^s(x_1))=1}.

Then exactly

    tau(x_2) = 0       if bit_0(x_2)=r_0,
               q+1     if bit_0(x_2)!=r_0.           (15)

Hence the two-step ledger is exactly

    -2               in the recurrent-phase case,
    q-1              in the nonrecurrent-phase case. (16)

This completely classifies the local compensation question:

- `q=0` and a nonrecurrent bit gives ledger `-1`;
- `q=1` and a nonrecurrent bit gives ledger `0`;
- `q>=2` and a nonrecurrent bit gives positive ledger `q-1`;
- selecting the recurrent bit gives two consecutive skips and ledger `-2`;
- an identically-zero low trace also gives two consecutive skips and ledger `-2`.

Therefore the hoped-for universal statement `tau(x_2)>=2 at every skip` is false as a statement about arbitrary periodic one-bit lifts. Any successful FULL-tail theorem must use an additional restriction on the **actual phase bit selected by the tower**, or amortize the bad phases over a longer block.

## 4. The bad phase is an explicit bit condition

The transient-stripping note writes

    u=T^H(y),
    x_1=sigma^(2H-1)u,
    x_2=sigma^(2H-2)u.

Therefore the actual lift bit is simply

    a_0=bit_0(x_2)=bit_(2H-2)(u),                    (17)

while the first two low forcing bits of `x_1` begin at

    b_0=bit_(2H-1)(u),
    c_0=bit_(2H)(u).                                 (18)

For a genuine zero-extension tower, `u=2^n T^H(v)`. The remaining global problem can thus be phrased without any ambiguity about inherited transients:

> At skip indices, compare the single phase bit `bit_(2H-2)(T^H(2^n v))` with the unique recurrent lift bit determined by the periodic core `x_1`. Show that recurrent-bit selections (and identically-zero low traces) cannot occur often enough to keep the global surplus-minus-skip ledger bounded above, or derive later forced surplus from each such selection.

This is a narrower target than merely asking for `tau(x_2)>=2`.

## 5. Sharpness examples (not used in the proof)

Small exact states show that all branches of the classifier genuinely occur, so they cannot be discarded abstractly.

For example, `z=12` lies on the period-two orbit

    12 -> 13 -> 12.

Its two one-bit lifts are

    24, 25.

Direct application of A gives

    tau(24)=2,
    tau(25)=0.

Thus the same periodic core can have a compensating lift and an immediately recurrent lift solely according to the exposed phase bit. Likewise `z=13` has lifts 26 and 27 with

    tau(26)=1,
    tau(27)=0.

These examples are included only to show sharpness of the exact formulas; no finite census is being used as evidence for the all-depth theorem.

## 6. Next target

The finite-lift phase problem is now solved locally. The next useful theorem must use structure specific to `x_m=A^H(2^m y)` coming from one common tower, rather than arbitrary lifts.

Two concrete routes remain:

1. **Bad-phase exclusion/frequency control.** Prove that at FULL-tail skips the actual bit in (17) cannot equal the recurrent bit in (15) too often, and control the `q=0` cases.
2. **Longer-block charging.** When the recurrent bit is selected and `x_2` is periodic (two consecutive skips), iterate the same classifier to `x_3,x_4,...` until the first nonperiodic lift and express the entire skip block plus exit residence as one exact ledger charge.

The second route is especially natural now: consecutive skips are precisely consecutive periodic members of the nested lift chain `x_m`, so a maximal periodic-lift block can be treated as one object instead of trying to compensate each skip independently.

Dependencies: `problem1_transient_stripping_zero_extensions.md`; `problem1_shift_tail_residence_ledger.md`; reviewed integer Rule-30 identities `A=sigma^2 T` and `T(q)=q XOR ((q<<1) OR (q<<2))`.
