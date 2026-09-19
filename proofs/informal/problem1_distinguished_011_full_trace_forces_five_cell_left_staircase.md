# FULL center trace forces a five-cell left staircase at the distinguished 011 source

Status: `partial-proof`. Problem 1 remains OPEN.

## Setup

Use the distinguished cyclic source from the forced-birth passage. At physical time `q=t+2`, the previous source/provenance analysis gives the global shadow cells

\[
(\hat r_{-2}(q),\hat r_{-1}(q),\hat r_0(q),\hat r_1(q),\hat r_2(q))=(0,1,1,1,0).
\]

The first three entries are the distinguished `011` obstruction. In the two-bit source case the return identity gives the right pair `(1,0)`, so the complete known local word is `01110` on positions `-2,...,2`.

FULL supplies the center trace

\[
\hat r_0(q+s)=1,0,1,0,1,0\qquad (s=0,\ldots,5).
\]

No assumption on cells at positions `3,4,...` is needed below.

## Exact backward-left forcing

Write

\[
p=\hat r_{-3}(q),\quad u=\hat r_{-4}(q),\quad v=\hat r_{-5}(q).
\]

Direct Rule-30 evolution of the local cone from the known `01110` word gives

\[
\hat r_0(q+3)=1\oplus p.
\]

FULL has center zero at `q+3`, hence

\[
\boxed{p=1}.
\]

With this value substituted, the next center is

\[
\hat r_0(q+4)=1\oplus u.
\]

FULL has center one at `q+4`, hence

\[
\boxed{u=0}.
\]

Substituting both values, the next center is

\[
\hat r_0(q+5)=1\oplus v.
\]

FULL has center zero at `q+5`, hence

\[
\boxed{v=1}.
\]

Therefore every distinguished two-bit-return source has the exact eight-cell shadow word

\[
\boxed{(\hat r_{-5},\ldots,\hat r_2)(q)=10101110.}
\]

Equivalently, the five cells immediately left of the center are forced to

\[
\boxed{\hat r_{-5},\ldots,\hat r_{-1}=10101.}
\]

The forcing through `-5` is independent of the unknown wider right fringe.

## Where the collapse stops

This does **not** continue indefinitely from center alternation alone. Beginning with the next new left cell, the required value can depend on the wider right fringe. Exact finite-cone experiments with arbitrary right cells show that positions `-1,...,-5` remain `1,0,1,0,1`, while position `-6` is not fixed uniformly once the right fringe beyond position 2 varies.

Thus this is an episode-specific finite collapse, not a proof that FULL forces an infinite alternating left tail. This is consistent with the left-permutivity result that arbitrary finite center traces can be realized from finite-support rows.

## Additional two-step right identity

If

\[
a=\hat r_3(q),\qquad b=\hat r_4(q),
\]

then the same exact cone gives at `q+2`

\[
\hat r_1(q+2)=1\oplus a,\qquad \hat r_2(q+2)=1.
\]

So the second shadow cell to the right of center is forced to one at the next cyclic source, independently of the wider fringe. This is compatible with the already established `t` then `u` gate passage; it is a useful concrete local constraint if a later source-relative finite-state collapse is attempted.

## Significance and stopping fence

The distinguished `011` obstruction is therefore embedded in substantially more rigid local data than the three-cell provenance calculation alone exposed: `10101110` is forced at the two-bit-return cyclic source. This is genuine use of the FULL center phase together with the complete return right pair.

However, the forcing stops before becoming an all-depth left-tail invariant. The next useful test is whether the exact `10101110` motif, together with the complete cyclic-source gate at `q+2` and `q+4`, forces a repeatable finite-state relation on the *wider right driver* (`a,b,...`). Merely extending the center trace farther by left-permutivity should not be pursued: beyond this local collapse it starts consuming unconstrained right-fringe information.
