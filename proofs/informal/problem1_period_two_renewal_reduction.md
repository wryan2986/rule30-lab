# Period-two renewal law and normalized integer reduction

Status: complete informal proof of two exact all-width reductions, plus bounded
regression checks. This is a partial structural result, not an exclusion of
eventual period two and not a solution of Problem 1.

## 1. Decision gate

For the pure alternating temporal trace, the existing inverse-section
recurrence writes the accumulated inverse automorphism after block `m` as an
outermost-to-innermost word `H_m` over `t,p,u`, with

\[
H_{m+1}=(H_m)_{11}\,p\,q_m,
\qquad
q_m\in\{t,u\}.
\]

The prior support identity says that the alternating inverse lift has infinite
support exactly when

\[
m-\ell_m\longrightarrow\infty,
\]

where `ell_m` is the initial run of `t` letters in `H_m`. The immediate task
was therefore to derive a recurrence for `ell_m`, not merely inspect a longer
prefix.

The result below changes that target in two useful ways:

1. `m-ell_m` is an exact renewal counter: it increases precisely when a
   nonzero base-4 seed block is emitted.
2. A hypothetical final zero streak reduces to a partial recurrence on one
   ordinary nonnegative integer, with continuation controlled by two residue
   classes modulo 16.

Either an infinite orbit of this coupled recurrence or a proof that none can
match the period-two schedule would directly inform the finite-support
question.

## 2. The combined section-11 transducer

The inverse generators have root flips and sections

\[
t=(t,p),\qquad p=(p,u)\sigma,\qquad u=(p,t)\sigma.
\]

To compute the section `(H)_11`, scan the word from innermost to outermost.
Let `(a,b)` be the roots currently presented to the first and second section
passes. For one input letter, the exact transducer is

\[
\begin{array}{c|ccc}
(a,b)&t&p&u\\ \hline
00&(t,00)&(p,11)&(p,11)\\
01&(p,01)&(u,10)&(u,10)\\
10&(p,11)&(p,01)&(t,00)\\
11&(u,10)&(t,00)&(p,01).
\end{array}
\]

Each entry is `(output letter, next state)`. This table follows directly by
taking the first selected section, then taking its section at the second root,
and updating both root actions.

Let

\[
\beta(H)=
(1\mathbin\oplus\rho(H))+
2(1\mathbin\oplus\rho(H_1))
\]

be the emitted base-4 seed block. Starting both section passes at root one,
the state after the complete inner-to-outer scan is exactly the two-bit value
`beta(H)`.

## 3. Exact renewal law for the leading run

Assume `H` is not all `t`. Write

\[
H=t^\ell aR,
\qquad a\in\{p,u\}.
\]

Read the transducer table backwards from its final state.

### Zero emission

If `beta(H)=0`, the final state is `00`. An outer `t` has the unique
predecessor `00`, emits `t`, and leaves that predecessor state unchanged.
Peeling the `ell` initial `t` letters therefore preserves state `00`.

At the first non-`t` letter:

- an input `p` reaching state `00` must come from state `11` and emits `t`;
- an input `u` reaching state `00` must come from state `10` and emits `t`.

For the next inner letter, every transition reaching state `11` emits `p`,
while every transition reaching state `10` emits `u`. Consequently,

\[
(H)_{11}=t^{\ell+1}aR'
\]

for some suffix `R'`. Appending `p q` cannot alter this prefix, so

\[
\boxed{\beta(H)=0\implies
\ell(H^+)=\ell(H)+1,
\quad a(H^+)=a(H).}
\]

### Nonzero emission

The same table shows that every transition reaching final state `10` emits
`u`, while every transition reaching `01` or `11` emits `p`. Therefore

\[
\boxed{
\begin{aligned}
\beta(H)=1&\implies \ell(H^+)=0,\ a(H^+)=u,\\
\beta(H)\in\{2,3\}&\implies \ell(H^+)=0,\ a(H^+)=p.
\end{aligned}}
\]

This is an all-width word identity. It does not depend on the inner suffix or
on whether `q=t` or `q=u`.

## 4. The deficit is a renewal counter

Set `d_m=m-ell_m`. The preceding law gives

\[
\boxed{
 d_{m+1}=
 \begin{cases}
 d_m,&\beta(H_m)=0,\\
 m+1,&\beta(H_m)\ne0.
 \end{cases}}
\]

Thus `d_m` is nondecreasing. More precisely, `ell_m` is the number of
consecutive zero emitted base-4 blocks immediately preceding block `m`, and
`d_m` is one plus the index of the most recent nonzero emitted block, with the
initial convention at `m=0`.

Combining this with the earlier support identity gives the exact equivalence

\[
\boxed{
S\text{ has infinite support}
\iff
\beta(H_m)\ne0\text{ for infinitely many }m.}
\]

The period-two problem is therefore a renewal problem. A finite-support
counterexample would have a final nonzero base-4 block followed by zeros
forever.

## 5. Normalize a zero-emitting state

Remove the leading run of `t` from a non-all-`t` word and write the normalized
word as `K`. Define the ordinary nonnegative integer

\[
x=K^{-1}(0),
\]

where inversion applies the corresponding forward maps `T,P,U` in word
order.

Because `K(x)=0`, its low input bit is `rho(K)`. If `beta(K)=0`, then
`rho(K)=rho(K_1)=1`; the first two bits of `x` are therefore both one.
Conversely, if the first two bits of `x` are both one, the first two zero
output bits force those same root activities. Hence

\[
\boxed{\beta(K)=0\iff x\equiv3\pmod4.}
\]

Suppose now that `beta(K)=0`. The renewal proof gives

\[
K_{11}=tL
\]

for a uniquely determined suffix `L`. Section compatibility with `K(x)=0`
gives

\[
(K_{11})^{-1}(0)=\left\lfloor\frac{x}{4}\right\rfloor.
\]

Since the initial `t` fixes zero under its forward inverse `T`, this is also
`L^{-1}(0)`. The normalized successor is

\[
K^+=Lpq,
\]

so, writing `Q=T` for `q=t` and `Q=U` for `q=u`,

\[
\boxed{x^+=Q\!\left(P\!\left(\left\lfloor x/4\right\rfloor\right)\right).}
\]

This is an exact recurrence on ordinary integers during every zero-emission
streak.

## 6. Continuation is decided modulo 16

Put `y=floor(x/4)`. Directly evaluating the low two bits gives

\[
\begin{array}{c|cc}
y\bmod4&T(P(y))\bmod4&U(P(y))\bmod4\\ \hline
0&1&0\\
1&2&3\\
2&3&2\\
3&0&1.
\end{array}
\]

Another zero block requires the successor to be `3 mod 4`. Therefore

\[
\boxed{
\begin{array}{c|c}
x\bmod16&\text{unique zero-continuing branch}\\ \hline
3&\text{none}\\
7&q=u\\
11&q=t\\
15&\text{none}.
\end{array}}
\]

Equivalently, with `z>=0`, the two possible continuing tails obey

\[
\boxed{
\begin{aligned}
x=16z+7&\implies x^+=4P(U(z))+3,\\
x=16z+11&\implies x^+=4U(P(z))+3.
\end{aligned}}
\]

The period-two schedule does not get to choose freely: an infinite final zero
streak would require its actual `q_m` sequence to match the unique branch
forced by these residues at every step.

For either continuing residue, `floor(x/4)` is nonzero. Every forward map
`T`, `P`, or `U` raises the highest one position of a nonzero finite integer by
exactly two. The two maps in the recurrence therefore give

\[
\boxed{\operatorname{bitlen}(x^+)=\operatorname{bitlen}(x)+2.}
\]

In particular, the partial map has no finite ordinary-integer cycle. This does
not rule out an infinite orbit whose integers grow without bound.

## 7. Bounded controls and a killed shortcut

The companion analyzer exhausts every non-all-`t` word through length eight
and both possible `q` branches. It checks the renewal signature, the
`x mod 4` zero criterion, the integer recurrence, and the modulo-16
continuation table. These checks are regression evidence; the proofs above
are the all-width justification.

Along the actual alternating path, a proposed bound `ell_m<=2` is false. The
first new maxima occur at

```text
(m, ell_m) = (3,1), (11,2), (283,3).
```

Thus a small constant run bound cannot finish the argument. This finite
counterexample is included only because it kills that concrete shortcut; it
is not evidence for or against the required infinite renewal statement.

## 8. New theorem target

The earlier target `m-ell_m -> infinity` is now equivalent to either of the
following:

1. prove that nonzero base-4 blocks recur infinitely often; or
2. rule out an infinite orbit of the partial integer recurrence that also
   follows the exact period-two schedule branch.

The second formulation is substantially smaller than the complete accumulated
word, while retaining exact nonlocal information through the unbounded
integer `x`. The next admissible work is to seek a ranking function, forbidden
2-adic cycle, or schedule/integer cocycle for this partial map. Merely extending
the block prefix or cataloguing larger finite zero runs would not address the
remaining infinite quantifier.
