# Problem 1 — run 240: Pascal parity depth is root multiplicity at 1

Problem 1 remains open.

## Entry point

Run 239 defined, on an order plateau `O_{r-1}=O_r=N=2^m`, the Pascal parity depth of the coordinate word `x_r(0),...,x_r(N-1)` by consecutive identities

\[
S_{A^j1_N}[x_r]\equiv 0,\qquad j=0,1,\ldots,d-1.
\]

At width 8 and `N=32`, exhaustive enumeration gave depth exactly 6. This note gives an exact algebraic meaning to that depth.

## Orbit-word polynomial

For a fixed initial state define the cyclic orbit-word polynomial

\[
X_r(z)=\sum_{t=0}^{N-1}x_r(t)z^t\in\mathbf F_2[z].
\]

Also define its reversal

\[
Y_r(z)=z^{N-1}X_r(z^{-1})=\sum_{u=0}^{N-1}x_r(N-1-u)z^u.
\]

Run 234 gives

\[
(A^j1_N)_t=\binom{N-1-t}{j}\pmod2.
\]

Therefore

\[
S_{A^j1_N}[x_r]
 =\sum_{u=0}^{N-1}\binom uj x_r(N-1-u).
\]

The right side is exactly the `j`th Hasse derivative of `Y_r` evaluated at `z=1`:

\[
\boxed{S_{A^j1_N}[x_r]=Y_r^{[j]}(1).}
\]

Over any field, a polynomial has a root of multiplicity at least `d` at `z=1` iff its Hasse derivatives of orders `0,...,d-1` vanish there. Hence

\[
\boxed{
S_{A^j1_N}[x_r]=0\ (0\le j<d)
\iff
(z+1)^d\mid Y_r(z).
}
\]

Reversal preserves the multiplicity of the nonzero root `z=1` (multiplication by the unit `z^{N-1}` and substitution `z -> z^{-1}` do not change it). Thus equivalently

\[
\boxed{
S_{A^j1_N}[x_r]=0\ (0\le j<d)
\iff
(z+1)^d\mid X_r(z).
}
\]

So the Pascal parity depth is not merely analogous to a moment depth: it is exactly the `(z+1)`-adic valuation of the orbit-word polynomial, minimized over initial states when the identity is required for every state.

## Relation to the forcing word

Let

\[
f_r(t)=x_{r-1}(t)\lor x_{r-2}(t),\qquad
F_r(z)=\sum_{t=0}^{N-1}f_r(t)z^t.
\]

The recurrence is

\[
x_r(t+1)=x_r(t)\oplus f_r(t).
\]

If `x_r` is `N`-periodic (in particular on `O_r=N`), then in the cyclic ring

\[
R_N=\mathbf F_2[z]/(z^N-1)
\]

we have

\[
\boxed{zF_r(z)=(1+z)X_r(z).}
\]

Since `N=2^m`, in characteristic two

\[
z^N-1=z^N+1=(z+1)^N.
\]

Thus `R_N` is exactly the local truncated ring `F_2[z]/((z+1)^N)`, and `z` is a unit at `z=1`. For every nonzero cyclic word,

\[
\boxed{
\nu_{z+1}(F_r)=\nu_{z+1}(X_r)+1
}
\]

until the valuation reaches `N` (the zero word). This is the polynomial form of run 239's shift

\[
S_{A^k1_N}[f_r]=S_{A^{k-1}1_N}[x_r].
\]

The whole Pascal-mask hierarchy is therefore just the `(z+1)`-adic filtration of cyclic orbit words.

## Width-8 interpretation

Run 239 found, for `r=8`, `N=32`, that

\[
S_{A^j1_{32}}[x_8]\equiv0\quad (j=0,\ldots,5),
\]

while the next moment is nonzero for some state. Hence the exact statement is

\[
\boxed{(z+1)^6\mid X_8(z)\text{ for every initial state, but }(z+1)^7\nmid X_8(z)\text{ for some state}.}
\]

Equivalently every width-8 top-coordinate orbit word lies in the codimension-6 cyclic ideal `((z+1)^6)` inside `F_2[z]/((z+1)^32)`.

Because `6=2+4`, Lucas/Frobenius gives the sparse factor

\[
(z+1)^6=(1+z^2)(1+z^4)=1+z^2+z^4+z^6.
\]

This may be more tractable than six separate Pascal identities.

## Why this is useful

The temporal-mask part of the problem can now be compressed completely into one valuation. Instead of tracking a family of masks, define

\[
\delta_r(N)=\min_{\text{initial states}}\nu_{z+1}(X_r(z))
\]

whenever the coordinate word is `N`-periodic. Then run 239 says `delta_8(32)=6`, while the forcing valuation is exactly one larger.

The remaining nonlinear question is sharply isolated: explain how the OR map

\[
F_r=X_{r-1}\lor X_{r-2}
\]

acts on the `(z+1)`-adic filtration of cyclic binary words. Ordinary polynomial addition is linear in this filtration, but bitwise OR is `a OR b = a+b+ab` over `F_2`, where `ab` here is coefficientwise (Hadamard) multiplication, not polynomial multiplication.

## Next target

Study the `(z+1)`-adic valuation of coefficientwise products in `R_N` and derive bounds for

\[
\nu_{z+1}(A+B+A\odot B)
\]

from the valuations/structure of `A` and `B` arising as adjacent Rule-30 coordinate words. A generic valuation inequality for Hadamard products is unlikely to be strong enough, so first test the exact adjacent-coordinate orbit words. The width-8 depth-six phenomenon is now the concrete benchmark any proposed recursion must explain.
