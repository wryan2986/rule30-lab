# Two-step discrepancy collision excludes the final positive hidden slack

Status: `partial-proof` / concrete strengthening. Problem 1 remains OPEN.

## Setup

Continue the sufficiently late TWO-BIT nonresetting passage of runs 160--162 and put `q=t+2`. Run160 excludes terminal hidden slack `g_(t+5)>=2`. Run161 proves that the only remaining positive case `g_(t+5)=1` has the unique original-cut residence itinerary

    (d_2,d_3,d_4,d_5) = (0,0,2,3),

and hence, at time `q`,

    m(q)=3,
    (r_1,r_2,r_3)(q) = (1,0,1),
    (hat r_1,hat r_2,hat r_3)(q) = (1,0,0).

The distinguished actual source block also gives `r_0(q)=1`, and because the first discrepancy is at position 3 the original global shadow agrees there: `hat r_0(q)=1`.

No shadow is restarted here: `hat r` is the SAME original global E-shadow.

## Exact two-step collision

Use `F(l,x,r)=l XOR (x OR r)`.

At time `q+1`, position 1 is shared:

    r_1(q+1) = 1 XOR (1 OR 0) = 0,
    hat r_1(q+1) = 1 XOR (1 OR 0) = 0.

At position 2,

    r_2(q+1) = 1 XOR (0 OR 1) = 0,
    hat r_2(q+1) = 1 XOR (0 OR 0) = 1.

Thus the expected residence front has moved from physical position 3 to position 2.

Crucially, the actual value at position 3 one step later is independent of every wider actual driver bit:

    r_3(q+1)
      = r_2(q) XOR (r_3(q) OR r_4(q))
      = 0 XOR (1 OR r_4(q))
      = 1.

Now evolve position 2 once more. For the actual row,

    r_2(q+2)
      = r_1(q+1) XOR (r_2(q+1) OR r_3(q+1))
      = 0 XOR (0 OR 1)
      = 1.

For the shadow row, the middle input is already 1, so its unknown right driver is irrelevant:

    hat r_2(q+2)
      = hat r_1(q+1) XOR (hat r_2(q+1) OR hat r_3(q+1))
      = 0 XOR (1 OR hat r_3(q+1))
      = 1.

Therefore

    boxed: r_2(q+2) = hat r_2(q+2) = 1.              (1)

This conclusion is independent of `r_4(q)` and of the complete wider shadow driver.

## Contradiction with the unique g=1 itinerary

For itinerary `(0,0,2,3)`, the residence of characteristic `q+3` occupies times `q,q+1`, and the next residence is characteristic `q+4`, beginning at time `q+2`. Equivalently the global-front identity gives

    J(q+2)=q+4,
    m(q+2)=J(q+2)-(q+2)=2.

By definition of `m`, actual and original shadow must therefore FIRST differ at physical position 2 at time `q+2`:

    r_2(q+2) XOR hat r_2(q+2) = 1.                  (2)

Equations (1) and (2) contradict each other. Hence

    boxed: g_(t+5) != 1.

Runs 154 and 160 already excluded `g=3` and `g=2`, while nonnegativity gives `g>=0`. Consequently the hidden slack on this passage is forced to vanish:

    boxed: g_(t+5)=0.

Using run153's exact repayment identity,

    s_(t+6)-s_(t+5)=g_(t+5)+2,

we obtain the exact terminal original-cut jump

    boxed: s_(t+6)-s_(t+5)=2.

## Significance and limit

Run162 translated `g=1` into a condition on the wider source-t shadow driver, but that driver condition is unnecessary: the required first-discrepancy itinerary collides locally after two Rule-30 steps. The collision uses the ORIGINAL global shadow and is therefore an all-depth consequence once run161's front itinerary has been established.

This closes the hidden-slack ambiguity for the sufficiently late TWO-BIT nonresetting distinguished passage. It does NOT by itself prove Problem 1 or a finite global birth budget; the next useful task is to propagate this exact zero-slack / jump-2 fact into the existing birth/renewal accounting and test whether it creates a new all-depth contradiction or merely sharpens the passage geometry.

Dependencies: `problem1_run161_g1_forces_unique_front_itinerary_and_shadow_bit.md`; `problem1_run160_global_shadow_excludes_g2.md`; `problem1_run154_distinguished_source_excludes_maximal_hidden_slack.md`; `problem1_run153_zero_plateau_slack_exact_repayment.md`; `problem1_global_discrepancy_front.md`.
