# Problem 1 run 192: t+9 front bits reduce exactly to four left driver bits

Status: exact local continuation and negative result; Problem 1 remains open.

## Starting point

Run 191 showed that the exit of the forced resetting passage is controlled by

\[
(A,B)=(r_{-2},r_{-1})(t+7),
\]

with the three front outcomes `A=B`, `(A,B)=(1,0)`, and `(A,B)=(0,1)`.

Run 188/189 also force, on the beta=1 return trajectory, if

\[
a=r_{-2}(t+4),\qquad b=r_{-1}(t+4),
\]

then

\[
r_0(t+6)=a\oplus b=1.
\]

Hence

\[
\boxed{b=1\oplus a}.
\]

The rigid right prefix at `t+4` is

\[
(r_0,r_1,r_2,r_3)=(1,1,1,0).
\]

## Exact three-step transport of the left driver

Write the next three cells to the left at `t+4` as

\[
q=r_{-5}(t+4),\qquad r=r_{-4}(t+4),\qquad s=r_{-3}(t+4).
\]

Starting from

\[
(q,r,s,a,1\oplus a,1,1,1,0)
\]

at positions `-5,...,3`, apply Rule 30 three times and retain positions `-2,-1` on row `t+7`. Boolean simplification gives

\[
\boxed{A=q\oplus s\oplus rs\oplus a\oplus sa},
\]

\[
\boxed{B=r\oplus s\oplus a}.
\]

Thus the run-191 trichotomy is independent of every cell to the right of the already-rigid `1110` prefix, but it genuinely depends on a four-bit left driver `(q,r,s,a)`.

## Exhaustive audit and negative result

I exhaustively evaluated all `2^4=16` assignments of `(q,r,s,a)` subject to the already-forced relation `b=1 xor a`. Every one of the four pairs `(A,B)` occurs, each exactly four times:

- `(0,0)`: 4 assignments;
- `(1,1)`: 4 assignments;
- `(1,0)`: 4 assignments;
- `(0,1)`: 4 assignments.

Therefore the exceptional run-191 branch `(A,B)=(0,1)` is **not** excluded by the rigid local beta=1 return data accumulated through run 189. Likewise, neither equality `A=B` nor the exact-exit branch `(1,0)` follows from those local data alone.

This is a useful dead end: further literal right-prefix propagation cannot decide the `t+9` front. Any exclusion of `(0,1)` must use additional complete-driver/global information constraining at least one of the left cells `q,r,s,a`.

## More compact front predicates

From the formulas above,

\[
A\oplus B=q\oplus r\oplus rs\oplus sa.
\]

Hence the long-residence branch `A=B` is exactly

\[
\boxed{q\oplus r\oplus rs\oplus sa=0}.
\]

The two asymmetric branches are selected by the same nonzero predicate together with `B=r xor s xor a`:

\[
(A,B)=(1,0)\iff A\oplus B=1\ \text{and}\ r\oplus s\oplus a=0,
\]

\[
(A,B)=(0,1)\iff A\oplus B=1\ \text{and}\ r\oplus s\oplus a=1.
\]

## Consequence and next target

The precise blocker is now identified: the existing local return package fixes `b=1 xor a` but leaves all 16 assignments of `(q,r,s,a)` locally possible, and all four `(A,B)` outcomes survive.

The next useful step is not wider right propagation. It is to recover the complete beta=1 cyclic driver at `t+4` (the retained `Y_{t+4}=G(z)` / threshold data) and ask what it forces about the four left cells

\[
(r_{-5},r_{-4},r_{-3},r_{-2})(t+4).
\]

In particular, any global constraint on `q xor r xor r s xor s a` immediately selects equality versus asymmetry at the `t+9` front.

Dependencies: `problem1_run188_alpha_is_complement_terminal_center.md`; `problem1_run189_terminal_center_is_forced_one.md`; `problem1_run191_tplus9_front_trichotomy.md`.
