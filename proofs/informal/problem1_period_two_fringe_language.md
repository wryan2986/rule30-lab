# Period-two moving-fringe trace language

Status: complete informal derivation of an autonomous two-step fringe map, a
local self-trace identity, and three translation-invariant forbidden branch
words. The two longer forbidden words use complete finite Boolean light-cone
exhaustion. The aperiodicity corollary is conditional on Kopra's published
width-two trace theorem, already audited elsewhere in this repository. These
are partial structural results. They do not exclude period two and do not solve
Rule 30 center nonperiodicity.

## 1. Setup

Assume the center follows the pure alternating trace

\[
x_0(2m)=1,\qquad x_0(2m+1)=0.
\]

At even time `2m`, write the right fringe as

\[
a_j(m)=x_j(2m)\quad(j\ge 1)
\]

and encode it by the ordinary or 2-adic integer

\[
A_m=\sum_{j\ge1}a_j(m)2^{j-1}.
\]

The branch letter used by the period-two inverse-lift recurrence is

\[
q_m=
\begin{cases}
 u,&(a_1(m),a_2(m))=(0,0),\\
 t,&\text{otherwise}.
\end{cases}
\]

Equivalently, with `b_m=1[q_m=u]`,

\[
b_m=\neg(a_1(m)\lor a_2(m)).
\]

## 2. The branch is an actual left-column trace

The transition from center value one to center value zero gives

\[
0=x_{-1}(2m)\oplus(1\lor x_1(2m)),
\]

so

\[
x_{-1}(2m)=1.
\]

At the next odd row,

\[
x_{-1}(2m+1)=f(x_{-2}(2m),1,1)=\neg x_{-2}(2m),
\]

and

\[
x_1(2m+1)=f(1,a_1(m),a_2(m))
=\neg(a_1(m)\lor a_2(m)).
\]

The following center value is again one, so

\[
1=x_{-1}(2m+1)\oplus x_1(2m+1).
\]

The two odd-row values therefore differ. Substituting the preceding formulas
shows

\[
\boxed{x_{-2}(2m)=\neg(a_1(m)\lor a_2(m))=b_m.}
\]

Thus the auxiliary branch sequence is not merely an internal section label: it
is exactly the even-time trace of the physical cell at coordinate `-2`.
Moreover the adjacent trace `[-1,0]` is

\[
(x_{-1}(2m),x_0(2m))=(1,1)
\]

and

\[
(x_{-1}(2m+1),x_0(2m+1))=(1-b_m,0).
\]

Consequently, if `(b_m)` were eventually periodic, the complete adjacent
width-two trace `[-1,0]` would also be eventually periodic. For any nonzero
finite-support initial configuration this contradicts Kopra's Corollary 3.7,
whose Rule 30 hypotheses and coordinate conventions are checked in
`docs/theory_literature_review.md` and
`proofs/informal/problem1_period_one_exclusion.md`.

Therefore, under a finite-seed alternating-center hypothesis, the induced
branch schedule is **not eventually periodic**.

This does not itself contradict finite support: the preceding schedule-coding
result already showed only that a finite survivor would need a genuinely
aperiodic schedule.

## 3. Exact packed two-step fringe map

Include the center as bit zero of

\[
R_m=1+2A_m.
\]

For Rule 30,

\[
f(l,c,r)=l\oplus(c\lor r).
\]

Applied simultaneously to the packed row, the odd row is

\[
F_m=R_m\oplus\big((R_m\!\gg1)\lor(R_m\!\gg2)\big).
\]

The odd center is zero. Applying Rule 30 once more and dropping that center
bit gives the autonomous even-time fringe recurrence

\[
\boxed{
A_{m+1}=(F_m\!\ll1)\oplus\big(F_m\lor(F_m\!\gg1)\big).
}
\]

The analyzer independently implements this formula in packed and tuple forms
and checks every input through twelve bits.

## 4. Finite dependency cones

The low `k` bits of `A_{m+1}` depend only on the low `k+2` bits of `A_m`.
This is immediate from the displayed shifts: to determine output positions
below `k`, the largest referenced input position is below `k+2`.

Since `q_m` depends only on the low two bits of `A_m`, induction gives:

> The branch word `q_m ... q_(m+n-1)` depends only on the first `2n` bits of
> `A_m`.

Therefore a complete enumeration of all `2^(2n)` Boolean assignments is a
proof of the exact length-`n` local trace language. It is not a sample over a
larger unknown state space.

The exact realized-word counts through length ten are

\[
2,3,5,8,12,17,25,36,49,65.
\]

## 5. Three all-time forbidden words

The complete languages imply

\[
\boxed{uu\text{ is forbidden},}
\]

\[
\boxed{ttttt\text{ is forbidden},}
\]

and

\[
\boxed{ututtu\text{ is forbidden}.}
\]

These are translation-invariant statements: the dependency-cone argument can
be restarted at every block `m`.

The first exclusion also has a one-line direct proof. If `q_m=u`, then the two
low bits of `A_m` vanish. The low bit of the packed recurrence simplifies to

\[
(A_{m+1})_0=\neg(A_m)_0\lor
(\neg(A_m)_1\land\neg(A_m)_2)=1.
\]

Hence the next first fringe bit is one and `q_(m+1)=t`.

The other two exclusions are complete local truth-table arguments:

- `ttttt` depends on ten input bits, and none of the `2^10` assignments emits
  it;
- `ututtu` depends on twelve input bits, and none of the `2^12` assignments
  emits it.

The executable certificate is
`experiments/problem1_nonperiodicity/analyze_period_two_fringe_language.py`.

In particular, successive `u` positions are separated by exactly two, three,
four, or five blocks. The branch schedule has bounded gaps in both symbols:
`u` never repeats immediately and `t` never runs for five blocks.

## 6. A strict graph-directed dimension bound

Let `Y` be the binary subshift defined by forbidding

\[
\{uu,ttttt,ututtu\}.
\]

Every moving-fringe branch schedule belongs to `Y`. The exact length-six
language has the following seventeen words:

```text
ttttut  tttutt  tttutu  ttuttt  ttuttu  ttutut
tutttt  tutttu  tuttut  tututt  tututu
uttttu  utttut  uttutt  uttutu  ututtt  ututut
```

Using their length-five prefixes and suffixes gives the transition table

```text
ttttu -> tttut
tttut -> ttutt, ttutu
ttutt -> tuttt, tuttu
ttutu -> tutut
tuttt -> utttt, utttu
tuttu -> uttut
tutut -> ututt, ututu
utttt -> ttttu
utttu -> tttut
uttut -> ttutt, ttutu
ututt -> tuttt
ututu -> tutut
```

The characteristic polynomial of this adjacency matrix is

\[
\lambda^8(\lambda+1)(\lambda^3-\lambda^2-1).
\]

Its Perron root is the unique positive solution of

\[
\lambda^3=\lambda^2+1,
\qquad
\lambda\approx1.46557123187677.
\]

Hence

\[
h_{\mathrm{top}}(Y)=\log\lambda.
\]

The schedule-survivor coding contracts 2-adic diameter by exactly `1/4` per
branch. Therefore the image of all moving-fringe-compatible schedules has
2-adic Hausdorff dimension at most

\[
\boxed{
\frac{\log\lambda}{\log4}
\approx0.275731544872797.
}
\]

This strictly improves the unrestricted schedule-survivor dimension `1/2`.
It still does not exclude isolated nonnegative integers from the compatible
set, so it is not a finite-support proof.

## 7. What is now known about the actual schedule

Combining this note with the schedule-coding theorem gives an exact summary:

1. the actual branch schedule is generated by an autonomous Rule 30 fringe;
2. it is the even-time trace of cell `-2` under the alternating-center
   hypothesis;
3. it is not eventually periodic for a finite seed, by the width-two theorem;
4. it avoids `uu`, `ttttt`, and `ututtu` at every position;
5. its zero survivor lies in a graph-directed 2-adic set of dimension at most
   approximately `0.275732`.

The unresolved statement is still that the one specific actual schedule codes
an infinite-support survivor. Neither aperiodicity, bounded gaps, nor the
dimension bound alone proves that.

## 8. Next admissible target

The next proof should exploit more than a fixed finite word list. Useful forms
would be:

- an all-scale return map between successive `u` events;
- a renormalization of the autonomous fringe after return times two through
  five;
- a cocycle connecting that return map to nonzero output pairs of the survivor;
- or a transfer of the bounded-gap self-trace identity to a finite-support
  contradiction in the original spacetime.

Merely extending the exact language from length ten to a longer finite length
would be regression evidence, not continuation.
