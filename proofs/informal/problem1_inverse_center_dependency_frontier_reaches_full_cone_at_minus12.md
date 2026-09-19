# Problem 1: inverse-center dependency frontier reaches the full cone at offset -12

Problem 1 remains OPEN.

## Setup

At the distinguished cyclic source `q`, previous runs establish

`(r_-5,...,r_2)(q) = 10101110`

and FULL requires the center trace from `q` onward to alternate

`1,0,1,0,...`.

Run 145 found the first entry of farther right-driver information:

`r_-10(q) = (NOT r_3) AND (r_4 OR r_5 OR (NOT r_6))`.

The next question was whether the minimal right-driver depth needed for successive forced left bits grows slowly enough to define a useful finite transducer, or instead reaches the generic Rule-30 light-cone frontier.

## Exact finite-cone computation

I enumerated all assignments of the source bits `r_3,...,r_16`. For each assignment I solved successively for the unique bits `r_-6,...,r_-16` that force the alternating FULL center trace. Uniqueness at each step follows directly from Rule 30's left-permutivity:

`F(l,c,r) = l XOR (c OR r)`.

For each forced bit `r_-n`, I then tested every right-driver coordinate for genuine Boolean dependence by pairing assignments that differ in only that coordinate.

The essential right-driver coordinates are:

- `r_-6`: `r_3,r_4`
- `r_-7`: `r_3,r_4`
- `r_-8`: `r_3,r_4`
- `r_-9`: none
- `r_-10`: `r_3,r_4,r_5,r_6`
- `r_-11`: `r_3`
- `r_-12`: **every coordinate `r_3,...,r_12`**

The last line is the decisive stopping fence. At offset `-12`, the forced opposite-side bit genuinely depends on `r_12`, the farthest right source coordinate that can possibly influence the center at time 12. Thus the dependency frontier has already reached the generic light-cone boundary.

## Explicit boundary-dependence witness

Fix

`(r_3,...,r_11) = (1,0,1,1,0,1,0,0,0)`.

Solving the FULL center constraints through time 12 gives different forced values of `r_-12` when only the farthest cone-boundary bit `r_12` is changed:

- with `r_12=0`, the required value is `r_-12=0`;
- with `r_12=1`, the required value is `r_-12=1`.

All source bits `r_-5,...,r_11` are identical in the two cases, including the distinguished motif and every nearer right-driver bit. Therefore no right prefix ending before `r_12` can determine `r_-12` under the FULL constraints.

## Consequence

The delayed dependence seen in runs 144-145 is real but transient. It does **not** produce a sublinear dependency frontier or a fixed-width inverse-center transducer: by time/offset 12, information from the extreme right edge of the entire available light cone is genuinely required on the opposite side.

This closes the proposed strategy of extending the inverse-center dependency table in search of a bounded-width compression. Further table extension may reveal incidental cancellations, but cannot restore a uniform bounded-width state once full-cone boundary dependence has already occurred.

The next useful route should return to the cyclic episode/gate quotient question: seek an observable tied specifically to the return/birth event that forgets most of the wider fringe, rather than trying to reconstruct the entire FULL-compatible source row from a bounded right prefix.
