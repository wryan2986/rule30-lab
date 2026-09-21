# Problem 1 run 187: the t+8 candidate gate bit cancels all wider-right data

Status: proved local Rule-30 reduction; Problem 1 remains open.

## Starting point

Run 186 reduced the gate bit of a hypothetical nonresetting recurrence at physical time `t+8` to

\[
\alpha=x\oplus\omega,
\qquad
x=r_0(t+6),
\qquad
\omega=r_3(t+6)\lor r_4(t+6).
\]

The proposed next step was to transport the complete cyclic driver from the rigid cyclic row at `t+4`.  That transport simplifies more than expected: the apparently wider-right datum cancels completely.

At `t+4` the already-proved actual prefix is

\[
(r_0,r_1,r_2,r_3)=(1,1,1,0).
\]

Write the two cells immediately to its left as

\[
a=r_{-2}(t+4),\qquad b=r_{-1}(t+4),
\]

and leave every cell `r_4,r_5,r_6,...` arbitrary.

## Two-step local calculation

Use Rule 30 in the form

\[
F(L,C,R)=L\oplus(C\lor R).
\]

Propagate the row from `t+4` to `t+6`.  A direct Boolean simplification of

\[
r_0(t+6)\oplus\bigl(r_3(t+6)\lor r_4(t+6)\bigr)
\]

under the fixed prefix `1110` gives

\[
\boxed{\alpha=1\oplus a\oplus b}.
\]

Equivalently,

\[
\boxed{\alpha=1\iff r_{-2}(t+4)=r_{-1}(t+4)}.
\]

The result is independent of `r_4(t+4),r_5(t+4),r_6(t+4)` and hence of every still-wider right cell.

For audit, the four possibilities are

| `(a,b)` | `alpha` |
|---|---:|
| `00` | `1` |
| `01` | `0` |
| `10` | `0` |
| `11` | `1` |

This was also exhaustively checked over all `2^5` assignments of `(a,b,r_4,r_5,r_6)` using the literal Rule-30 update; toggling any of `r_4,r_5,r_6` never changes `alpha`.

## Consequence for a hypothetical nonresetting source at t+8

Combining with run 185:

* if `a=b`, then `alpha=1`, so a hypothetical nonresetting source at `t+8` must be gate-`u`, one-bit, with
  \[
  \tau(Y_{t+8})=1,\qquad \Delta_{t+7}=2;
  \]
* if `a\ne b`, then `alpha=0`, so it must be gate-`t`, two-bit, with
  \[
  \tau(Y_{t+8})=2,\qquad \Delta_{t+7}=3.
  \]

Thus run 186's apparent dependence on the wider terminal right driver was not genuine.  The first unresolved datum controlling the candidate recurrence is instead the equality/XOR of the two cells immediately **left** of the rigid `1110` prefix at the cyclic row `t+4`.

## Important fence

This does not by itself prove that `t+8` is nonresetting.  The delay/gate conclusions above remain conditional on the nonresetting-source hypothesis, exactly as in run 185.

Also, no assumption about arbitrary right fringe cells was used in deriving the cancellation.  The calculation is local and valid for every completion of the row consistent with the proved `1110` prefix.

## Next target

Determine `(r_{-2},r_{-1})(t+4)` from the retained complete cyclic driver / resetting-return structure.  In particular, test whether cyclicity or the global-front conditions already force `a=b` or `a\ne b`.  If they do, the candidate gate, source width, delay and residence jump at `t+8` are all decided without transporting any wider-right driver symbol.
