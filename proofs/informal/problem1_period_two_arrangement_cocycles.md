# Arrangement-sensitive cocycle no-go for the period-two transducer

Status: exact classification of two edge-telescoping whole-word ansatzes. These
results preserve absolute position or complete noncommutative letter order, but
both are forced to be terminal-blind. They do not exclude period two and do not
solve Rule 30 center nonperiodicity.

## 1. Exact edge table

Write the four scan states as `0=00`, `1=01`, `2=10`, `3=11`. The complete
right-to-left whole-word transducer has the following edges, written

```text
state -- input/output --> successor
```

```text
0 -- t/t --> 0    0 -- p/p --> 3    0 -- u/p --> 3
1 -- t/p --> 1    1 -- p/u --> 2    1 -- u/u --> 2
2 -- t/p --> 3    2 -- p/p --> 1    2 -- u/t --> 0
3 -- t/u --> 2    3 -- p/t --> 0    3 -- u/p --> 1
```

A complete scan of an ordered inverse word returns both its section and its
terminal reconstructed pair. Hence any edge identity that telescopes through
this table is genuinely a whole-word statement.

## 2. Geometrically weighted additive ansatz

Let the coefficient field be arbitrary, let `lambda` be a scalar, assign a
letter weight `a_x` to each `x in {t,p,u}`, and assign a potential `V_s` to each
scan state. Suppose every edge `s -- x/y --> r` satisfies

\[
a_x-a_y=V_s-\lambda V_r. \tag{1}
\]

Multiplying the equation at word position `j` by `lambda^j` makes the potential
terms telescope. Thus (1) remembers every absolute letter position; it is much
stronger than an ordinary factor-count statistic.

The edge equations imply the following.

From the two edges out of state zero with inputs `p,u` and the same output and
successor,

\[
a_u=a_p. \tag{2}
\]

The relevant potential equations are

\[
(1-\lambda)V_0=0,
\quad V_0=\lambda V_3,
\quad V_3=\lambda V_1,
\quad V_1=\lambda V_2,
\quad V_2=\lambda V_1. \tag{3}
\]

The state-one self-loop gives

\[
a_t-a_p=(1-\lambda)V_1. \tag{4}
\]

If `lambda != 1`, equation (3) gives `V_0=0`. If `lambda` is nonzero, the chain
in (3) gives every potential zero; if `lambda=0`, `V_1=0` follows directly from
`V_1=lambda V_2`, and the remaining potentials again vanish. Equation (4) then
gives `a_t=a_p`, which combines with (2).

If `lambda=1`, equation (3) gives

\[
V_0=V_1=V_2=V_3,
\]

and (4) again gives `a_t=a_p=a_u`.

Therefore:

> **Geometric additive no-go.** Over every field and for every scalar
> `lambda`, an edge identity of form (1) has equal letter weights. For
> `lambda != 1` every state potential is zero; for `lambda=1` all four state
> potentials are equal. In particular, the identity cannot distinguish
> terminal `00` from any nonzero terminal pair.

## 3. Group-valued product ansatz

Let `G` be an arbitrary group. Assign a group element `A_x` to each input/output
letter and a gauge `C_s` to each scan state. Suppose every edge satisfies

\[
C_s A_x=A_y C_r. \tag{5}
\]

Multiplying (5) through a complete scan telescopes the intermediate gauges while
preserving the full noncommutative order of the word product. This is therefore
an arrangement-sensitive ansatz even when all count-based observables fail.

Set

\[
A=A_t,\qquad B=A_p,\qquad U=A_u.
\]

The state-zero `p` and `u` edges have the same output and successor:

\[
C_0B=BC_3,\qquad C_0U=BC_3.
\]

Left cancellation gives

\[
U=B. \tag{6}
\]

The state-one `t` edge gives

\[
C_1A=BC_1. \tag{7}
\]

The state-two `p` and `u` edges, using (6), have the same left side and give

\[
BC_1=AC_0. \tag{8}
\]

Combining (7) and (8),

\[
C_1A=AC_0.
\]

The state-zero `t` loop says `C_0A=AC_0`, so right cancellation of `A` gives

\[
C_1=C_0. \tag{9}
\]

Substituting (9) into (7) and comparing with the state-zero loop gives

\[
BC_0=AC_0,
\]

so right cancellation gives

\[
A=B=U. \tag{10}
\]

Finally, with all letter labels equal, the state-two `u` edge and state-three
`p` edge each compare directly with the state-zero loop and yield

\[
C_2=C_0,\qquad C_3=C_0. \tag{11}
\]

Thus:

> **Group-product no-go.** For every group `G`, every solution of (5) satisfies
> `A_t=A_p=A_u` and `C_00=C_01=C_10=C_11`. Consequently every invertible
> matrix representation, finite-group representation, or other group-valued
> product cocycle is terminal-blind.

The proof uses only the exact edge table and group cancellation. Small exhaustive
controls in `S3` and `D4` independently recover only the commuting-pair family
predicted by the theorem.

## 4. Consequence for the critical path

The previous factor-parity result forgot arrangement. The two classes above do
not:

- geometric weights preserve every absolute position;
- noncommutative products preserve complete letter order.

Their failure therefore closes a much stronger family of simple whole-word
bridges. The next candidate cannot be a one-pass invertible edge gauge. It must
use at least one of:

1. a noninvertible semigroup or rank-deficient matrix mechanism where
   cancellation is unavailable;
2. a recursive multiscale state that combines neighboring blocks before the
   next transducer pass;
3. an identity special to the unique actual fringe orbit rather than every
   possible inverse word; or
4. a multi-time relation not decomposable into independent single-edge
   equations.

No claim here proves the alternating inverse lift has infinite support, excludes
eventual period two, or solves the center-column problem.
