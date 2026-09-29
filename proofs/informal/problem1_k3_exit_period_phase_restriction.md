# Problem 1: K=3 exit words force a nontrivial backward phase

Status: exact consequence of pushed complete-driver identities; Problem 1 remains OPEN.

This note combines the K=3 forward exit word from `problem1_exit_wait_front_residence.md` with the backward phase test from `problem1_full_driver_exit_phase.md`. It gives a small but genuine compatibility restriction on a K=3 repair that is invisible if the forward and backward conditions are treated independently.

## Setup

At an even one-bit `u,h=0` exit, let `b=Theta(z)` be the resetting complete driver of least period `p`. The exact waiting theorem defines

    L=min{n>=1 : b_n in {1,3}}.

Under an eventual physical strip `tau<=3`, every such exit has `L=3`, and FULL sharpens the forward prefix to

    (b_0,b_1,b_2,b_3)=(2,2,2,1).                 (1)

The complete-driver phase theorem determines the shadow bit `h` from the last reset strictly before phase zero. If

    ell=max{s<0 : b_s in {1,3}},
    gamma=XOR_(s=ell+1..-1) 1[b_s=2],

then

    h=1[b_ell=1] XOR gamma.                       (2)

An exit has `h=0`, equivalently

    gamma=1[b_ell=1].                             (3)

All negative indices below are periodic phases of this same least-period word.

## Period four is impossible

The waiting theorem previously gave only `p>=4`. Suppose `p=4`. By (1) and periodicity,

    b_-1=b_3=1.

Hence `ell=-1` and the suffix defining `gamma` is empty, so `gamma=0`. But (3) requires

    0=1[b_-1=1]=1,

a contradiction. Therefore every K=3 `u,h=0` exit satisfies

    p>=5.                                         (4)

Equivalently: the shortest periodic core compatible with the forward word `2221` is ruled out by the backward phase selected by the actual shadow. This is exactly the kind of forward/backward coupling that is lost when the two conditions are supplied independently.

## Exact period-five restriction

If `p=5`, then the phase immediately before zero is `b_-1=b_4`, while `b_-2=b_3=1`. There are four possibilities for `b_4`.

* `b_4=1`: `ell=-1`, `gamma=0`; (3) fails.
* `b_4=3`: `ell=-1`, `gamma=0`; (3) holds.
* `b_4=0`: the last reset is `ell=-2` with `b_ell=1`; the one-letter suffix has no `2`, so `gamma=0`; (3) fails.
* `b_4=2`: again `ell=-2` and `b_ell=1`, but now `gamma=1`; (3) holds.

Thus a least-period-five K=3 exit must have

    b_4 in {2,3}.                                 (5)

This is only a necessary phase condition. It does not assert that either `22212` or `22213` is realized by a genuine FULL finite-fringe orbit, nor that its least period is actually five.

## Research consequence

The K=3 repair problem now has a concrete first incompatibility: a repeated exit cannot live on a period-four `2221` core. Any bounded-delay survivor must carry a strictly longer complete core through every such exit; at period five the next symbol is already restricted to `{2,3}` by the backward phase.

This does not yet exclude K=3, because the least periods may grow and no recurrence transporting one exit core to the next is proved. It does, however, demonstrate that the pushed forward wait and backward exit-phase formulas yield additional information when coupled on the same periodic word. The next useful symbolic step is to transport the intervening repair/nonreset passage far enough to constrain the phase of the next source, rather than enumerate arbitrary periodic words.

Dependencies: `problem1_exit_wait_front_residence.md`, especially Sections 1 and 3; `problem1_full_driver_exit_phase.md`, especially Section 2.
