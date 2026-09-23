# Problem 1 run 226 — cocycle top-flip identity

Problem 1 remains open.

## Setup

For the width-`R` edge automaton `T_R` on coordinates `x_0,...,x_R`, run 225 showed that the extension to width `R+1` is

\[
T_{R+1}(x,z)=(T_Rx, z\oplus f_R(x)),
\qquad f_R(x)=x_R\lor x_{R-1}\quad(R\ge1),
\]

and that the extension doubles precisely when the orbit cocycle

\[
g_R(x)=\bigoplus_{t=0}^{O_R-1} f_R(T_R^t x)
\]

is 1 somewhere. Here `O_R=ord(T_R)` and `O_R/O_{R-1}` is either 1 or 2.

## New identity

Let `e_R` denote flipping only the top coordinate `x_R`. Because the top coordinate is a one-bit skew fiber over `T_{R-1}`, the two trajectories starting from `x` and `x\oplus e_R` remain complementary in coordinate `R` and identical below it for all time.

For bits `z,b`,

\[
(z\lor b)\oplus((z\oplus1)\lor b)=1\oplus b.
\]

Therefore, for every `R>=1`,

\[
\boxed{
 g_R(x)\oplus g_R(x\oplus e_R)
 = \bigoplus_{t=0}^{O_R-1}(1\oplus x_{R-1}(t)).
}
\]

For `R>=1`, `O_R` is even, so the constant-1 contribution cancels and

\[
\boxed{
 g_R(x)\oplus g_R(x\oplus e_R)
 = \bigoplus_{t=0}^{O_R-1}x_{R-1}(t).
}
\]

The lower trajectory has period dividing `O_{R-1}`. Writing

\[
q_R=O_R/O_{R-1}\in\{1,2\},
\]

the right side is `q_R` repetitions (mod 2) of the parity over one `O_{R-1}` block. Hence

\[
\boxed{
q_R=2 \Longrightarrow g_R(x)=g_R(x\oplus e_R)\text{ for every }x.
}
\]

If `q_R=1`, then

\[
\boxed{
 g_R(x)\oplus g_R(x\oplus e_R)
 = \bigoplus_{t=0}^{O_{R-1}-1}x_{R-1}(t).
}
\]

Thus the doubling cocycle's dependence on the newest coordinate is itself controlled by a lower-width orbit parity. In particular, immediately after an order-doubling extension, the *next* cocycle is blind to flipping the newest coordinate.

## Why this matters

Run 225 reduced the order hierarchy to an apparently fresh cocycle `g_R` at every width. The identity above shows these cocycles are not independent: top-coordinate sensitivity recursively descends to a lower-width orbit parity, and a preceding doubling forces that sensitivity to vanish completely.

This does not yet prove long non-doubling blocks or a sublinear bound for `m_R`; `g_R` may still be nonconstant through lower coordinates. So the result is structural progress, not a solution.

## Finite consistency check

The previously enumerated orders

`1,2,2,4,8,8,16,32,32,64,64,64,128,256,256,512,512,1024`

are consistent with the identity. No closed formula is inferred from this finite table.

## Next target

Study the lower orbit parity

\[
p_R(x)=\bigoplus_{t=0}^{O_R-1}x_R(t)
\]

as its own cocycle. Derive its top-flip/lower-projection recursion and seek a finite recursion coupling `(g_R,p_R)`. Such a recursion could turn the observed doubling/non-doubling word into a provable substitution or automaton and yield asymptotic control of `m_R`.