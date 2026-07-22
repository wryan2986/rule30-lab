# Exact period-two equations and current barrier

Status: exact local deductions plus explicitly bounded finite counterexamples
to three candidate proof mechanisms. Eventual center period two remains open,
and no statement here proves or refutes Problem 1.

## Setup

Assume that, from some time onward, the center alternates:

\[
c_{t+1}=1-c_t.
\]

Write the five cells at time \(t\) as

\[
(x_{-2},x_{-1},c,x_1,x_2).
\]

Imposing both the next alternating center bit and return after two steps gives
four allowed five-cell words in each phase:

\[
\begin{array}{c|l}
c=0 & 01000,\ 10010,\ 01001,\ 10011\\
c=1 & 11100,\ 01110,\ 01101,\ 01111.
\end{array}
\]

The bit order in each word is the spatial order displayed above. Every one of
the four assignments to \((x_1,x_2)\) occurs in each phase. Thus the exact
two-step constraint is lossless in the right pair and supplies no right-side
forbidden pattern.

Equivalently, the left cells satisfy

\[
\begin{aligned}
c_t=0:&\qquad x_{-1}(t)=1-x_1(t),\quad
                 x_{-2}(t)=x_1(t),\\
c_t=1:&\qquad x_{-1}(t)=1,\quad
                 x_{-2}(t)=1-(x_1(t)\lor x_2(t)).
\end{aligned}
\]

The last expression is also \(x_1(t+1)\) in the one-center phase.

## Exact two-step right-boundary identity

At a zero-center phase, write

\[
(a,b,d)=(x_1(t),x_2(t),x_3(t)).
\]

After one step,

\[
x_1(t+1)=a\lor b,
\qquad
x_2(t+1)=a\mathbin\oplus(b\lor d).
\]

The next center value is one, so

\[
\begin{aligned}
x_1(t+2)
&=1\mathbin\oplus
  \bigl(x_1(t+1)\lor x_2(t+1)\bigr)\\
&=1-(a\lor b\lor d).
\end{aligned}
\]

This NOR identity is exact and was checked on all eight triples. It is not a
closed temporal recurrence for \(x_1\), because it imports two farther-right
cells at every two-step update.

## Three mechanisms that did not survive finite controls

### 1. Narrower local cone

The complete five-cell enumeration above leaves \((x_1,x_2)\) arbitrary.
This matches the general period-defect analyzer: the period-two constraint
uses the full cone and uniquely solves the leftmost cell rather than forbidding
a pattern in the other four.

### 2. A small uniform zero-gap from the alternating boundary alone

Sideways reconstruction was run with an alternating center and every binary
adjacent-right trace through horizon 16. For the phase beginning with center
zero, the right trace

```text
00100010001000000
```

reconstructs the depth-ordered initial-left word

```text
1000000100000000
```

which contains eight consecutive zeros. This is an exact counterexample to
the candidate bound seven. It does not refute every possible finite gap bound,
but the observed maximum had already grown with the horizon, so increasing
only that horizon has no admitted proof value.

The adjacent-right trace in this counterexample is arbitrary and in fact
cannot be extended even locally to a Rule 30 right half. At time two it has
\(c_t=0\), \(x_1(t)=1\), and \(x_1(t+1)=0\), whereas Rule 30 would force

\[
x_1(t+1)=0\mathbin\oplus(1\lor x_2(t))=1.
\]

It therefore refutes only an argument that treats the adjacent-right column
as unconstrained. It is not a counterexample to the whole-tail conjecture.

### 3. Rapid settling of the forced finite right half

Starting the right half identically zero and forcing the center to alternate,
two independently written evaluators generated 4,096 values of the adjacent
right column. No period from 1 through 256 matched throughout the final 1,024
values. This refutes only that finite rapid-settling criterion. It does not
prove that the right column is nonperiodic.

## 2-adic lift diagnostic

The pure alternating trace beginning with one is the 2-adic number

\[
1+2^2+2^4+\cdots=-\frac13.
\]

The unique 1,024-bit prefix of its inverse diagonal lift had 541 ones, with a
one at position 1,022, and no preperiod at most 128 followed by a period at
most 128 repeated at least four times. These are finite observations only.
Unlike the period-one lifts \(\pm1/3\), no short rational spatial pattern was
found to promote into an exact algebraic identity.

## Current stopping barrier

Period one succeeded because setting the center to zero removed the XOR input
from the right-neighbor update and created a monotone Boolean column. A
nonconstant alternating center replaces that update by alternating OR and NOR
steps. The exact two-step NOR formula continually imports farther-right cells,
and the zero finite right half already generates a long nonrepeating adjacent
trace.

Accordingly, none of these results justifies a larger period box or horizon.
The unresolved period-two theorem remains:

> No positive odd finite right-edge seed has an eventually alternating
> growing diagonal.

Equivalently, the inverse 2-adic lift of every eventually alternating odd
trace must have infinitely many one bits. Progress now requires a new
finite-support invariant or a renormalized argument controlling the imported
right tail; the tested local and rapid-settling mechanisms do not provide one.
