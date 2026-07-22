# Period-two first-return system at `u` events

Status: complete informal derivation of the exact first-return selector, the
variable-length survivor cylinders, and a shared ordinary-degree cocycle. These
are partial structural results. They do not exclude period two and do not solve
Rule 30 center nonperiodicity.

## 1. Moving-fringe return coordinates

Let `A_m` be the even-time right-fringe integer from the period-two moving
fringe, and let `F` denote its autonomous two-step map. The branch is `u`
exactly when the first two fringe bits vanish. At a `u` event write

\[
A_m=4z_m.
\]

The previous trace-language theorem proves that the next `u` event occurs after
one of the four gaps

\[
r_m\in\{2,3,4,5\}.
\]

Define the first-return map

\[
\mathcal R(z)=\frac{F^{\rho(z)}(4z)}4,
\]

where `rho(z)` is the next return gap.

## 2. Exact four-bit return selector

A branch word of length six depends on only the first twelve bits of `A_m`.
After substituting `A_m=4z`, it depends on only the first ten bits of `z`.
Complete exhaustion of those `2^10` assignments shows that the answer is
constant on every residue class modulo sixteen:

| `z mod 16` | next `u` gap |
|---:|---:|
| 0 | 4 |
| 1 | 3 |
| 2 | 4 |
| 3 | 3 |
| 4 | 2 |
| 5 | 3 |
| 6 | 4 |
| 7 | 5 |
| 8 | 2 |
| 9 | 3 |
| 10 | 4 |
| 11 | 5 |
| 12 | 2 |
| 13 | 3 |
| 14 | 4 |
| 15 | 5 |

Thus

\[
\boxed{\rho(z)\text{ is determined exactly by }z\bmod16.}
\]

This is an all-time statement. The finite exhaustion is over the complete
Boolean dependency cone, and the argument can be restarted at any `u` event.

The exact two-return language contains every ordered pair in
`{2,3,4,5}^2` except

\[
(2,3).
\]

The exclusion is exactly the already-proved forbidden branch word `ututtu`.
Every other pair has an explicit finite fringe witness in the analyzer.

## 3. Fringe degree cocycle

For every positive ordinary fringe integer `A`, one application of `F` raises
its bit length by exactly two. Indeed, if the highest one of `A` is at position
`d`, then `R=1+2A` has highest one at `d+1`. The shifted terms in

\[
R\oplus((R\!\gg1)\lor(R\!\gg2))
\]

cannot cancel that top bit. In the second Rule 30 step, the left shift creates
a new top bit two positions above the original one, while every other term is
strictly lower.

Consequently, for `z>0`,

\[
\boxed{\operatorname{bitlen}(\mathcal R(z))
=\operatorname{bitlen}(z)+2\rho(z).}
\]

The unique exceptional starting state is `z=0`; its first return has gap four
and lands at `z=56`. Every later actual return state is positive.

## 4. Survivor return coordinates

For the normalized zero-survivor dynamics, a `u` event is exactly the cylinder

\[
x=7\pmod{16}.
\]

Write

\[
x=16y+7.
\]

Let

\[
B_q(v)=4p(q(v))+3
\]

be the inverse zero-branch contraction from the schedule-survivor theorem. If
the next `u` event is `r` blocks later, the branch word is

\[
u\,t^{r-1}\,u.
\]

Starting from the next `u` cylinder and composing the first `r` inverse
branches gives one unique current cylinder. After removing the fixed low value
seven, the exact normalized residues are

| gap `r` | required `y mod 4^r` | branch word through next return |
|---:|---:|---|
| 2 | 8 | `utu` |
| 3 | 60 | `uttu` |
| 4 | 108 | `utttu` |
| 5 | 940 | `uttttu` |

Equivalently, if `C_r` is the backward return contraction on `y`, then

\[
C_r(y')=c_r\pmod{4^r},
\]

with `c_2=8`, `c_3=60`, `c_4=108`, and `c_5=940`.

Each `B_q` raises 2-adic agreement by two. Therefore

\[
v_2(C_r(a)-C_r(b))=v_2(a-b)+2r.
\]

The return gap is thus a variable-length schedule code: a gap of length `r`
fixes exactly `2r` additional low bits of `y`.

## 5. Survivor degree cocycle

On an ordinary finite state that follows the required zero branches, every
single zero step raises bit length by exactly two. Grouping the steps between
successive `u` events gives

\[
\boxed{\operatorname{bitlen}(y_{n+1})
=\operatorname{bitlen}(y_n)+2r_n.}
\]

The analyzer checks each of the four exact residue cylinders on bounded
ordinary samples. Those checks are regression evidence for the all-width
branch and degree arguments.

## 6. The shared first-return cocycle

Assume, for contradiction, that the alternating inverse lift is an ordinary
finite integer. Let `m_n` be successive `u` blocks of the actual moving-fringe
schedule and define

\[
A_{m_n}=4z_n,
\qquad
X_{m_n}=16y_n+7.
\]

Both sides use the same return gap

\[
r_n=m_{n+1}-m_n.
\]

After the exceptional initial fringe return from `z_0=0`, the two exact degree
laws give

\[
\operatorname{bitlen}(z_{n+1})-
\operatorname{bitlen}(z_n)=2r_n,
\]

and

\[
\operatorname{bitlen}(y_{n+1})-
\operatorname{bitlen}(y_n)=2r_n.
\]

Hence

\[
\boxed{
\operatorname{bitlen}(y_n)-\operatorname{bitlen}(z_n)
\text{ is constant along all later `u` returns.}
}
\]

This is the desired exact first-return cocycle, but it is **neutral**: it does
not by itself contradict a finite survivor. The two finite fronts can advance
at the same speed while retaining a fixed offset.

## 7. What the result rules out

The return time is not an unbounded or hidden state variable. It is a four-bit
observable of the normalized fringe. Likewise, the survivor-side low cylinder
is completely determined by the return gap. Therefore the next proof should
not search for longer raw gap prefixes or a return-time growth estimate.

The unresolved information lies in the **high-front shape** of the two ordinary
return states, or equivalently in the nonzero output-pair content of the
survivor transducer. A successful continuation must strengthen the neutral
degree cocycle to a shape-sensitive cocycle, a forbidden coupled return cycle,
or an original-spacetime obstruction.

## 8. Executable certificate

The exact tables and bounded checks are implemented in

```text
experiments/problem1_nonperiodicity/analyze_period_two_first_return.py
```

The finite campaign does not prove that the actual survivor has infinite
support. It only validates the finite dependency-cone and ordinary-integer
instances used alongside the all-width arguments above.
