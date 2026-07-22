# Period-two frontier gluing obstruction

Status: complete informal proof of an exact finite-prefix gluing theorem. This
is a negative structural result: it shows that a bounded low schedule cylinder
and a bounded high-front window remain independent at every finite depth. It
does not exclude period two and does not solve Rule 30 center nonperiodicity.

## 1. Return-prefix coordinates

At a survivor-side `u` event write

\[
X=16y+7.
\]

Let

\[
r_0,r_1,\ldots,r_{n-1}\in\{2,3,4,5\}
\]

be a finite prefix of successive `u`-return gaps, and put

\[
B=r_0+r_1+\cdots+r_{n-1}.
\]

The corresponding branch word before the final return is

```text
u t^(r_0-1) u t^(r_1-1) ... u t^(r_(n-1)-1).
```

It has exactly `B` zero-emitting branches.

## 2. Unique low cylinder

Every inverse zero branch

\[
B_q(v)=4p(q(v))+3
\]

raises 2-adic agreement by exactly two bits. Begin at the final `u` cylinder
`X=7 mod 16` and compose the `B` inverse branches in reverse order. The result
is one current residue

\[
X\equiv 16c+7\pmod {2^{2B+4}}.
\]

Equivalently,

\[
\boxed{y\equiv c\pmod {2^{2B}}.}
\]

The residue is unique. Conversely, every ordinary nonnegative integer in this
cylinder follows exactly the prescribed finite return-gap prefix. Higher bits
cannot affect the branch decisions because the zero dynamics and its inverse
branches are triangular from low to high.

For one return this recovers the prior cylinders

\[
\begin{array}{c|c}
r & y\pmod {4^r}\\
\hline
2&8\\
3&60\\
4&108\\
5&940.
\end{array}
\]

## 3. Arbitrary high-front gluing

Fix any leading binary word `h` of width `w`, with first bit one. Fix any
number `f` of free middle bits and any middle word `m` of that width. Let
`L=2B`, and define

\[
y=(h\ll(f+L))+(m\ll L)+c.
\]

Then:

1. `y` is an ordinary finite integer of exact bit length `w+f+L`;
2. its highest `w` bits are exactly `h`;
3. its lowest `L` bits are exactly the required return-prefix residue `c`;
4. it follows all `n` prescribed returns.

Therefore, for every chosen high front there are exactly

\[
2^f
\]

ordinary finite states with that front and with the same finite return prefix.
Across all possible leading `w`-bit words there are

\[
2^{w-1+f}
\]

such states.

## 4. Degree evolution does not couple the fronts

The first-return degree theorem gives, after all `B` branches,

\[
\operatorname{bitlen}(y_{n})
 =\operatorname{bitlen}(y_0)+2B.
\]

Thus the prescribed high front is carried by an ordinary state whose leading
position advances at exactly the expected rate. The low return cylinder and
the high edge do not collide; the free middle remains the finite-depth buffer
between them.

## 5. Consequence for the research strategy

This proves a precise obstruction to a tempting continuation:

> No argument that examines only a fixed finite future return prefix and a
> fixed finite high-front window can exclude ordinary finite support.

At every finite depth, the exact low schedule constraints can be glued to any
finite leading pattern. Increasing only the return horizon or the fixed front
width merely increases the required finite state; it does not create an
infinite contradiction.

The theorem does **not** show that one ordinary state survives the complete
infinite schedule. The glued state changes as the tested prefix grows. It also
does not rule out:

- a quantity spanning the entire state;
- a growing-width front relation whose width is tied to elapsed return length;
- a monotone global statistic;
- or an original-spacetime obstruction that couples both expanding edges.

The next admissible target is therefore a genuinely global bridge across the
growing middle, rather than another separated low/high quotient.

## 6. Executable certificate

The exact cylinder construction and finite gluing checks are implemented in

```text
experiments/problem1_nonperiodicity/analyze_period_two_frontier_gluing.py
```

The bounded campaign validates selected finite families. The all-width gluing
statement follows directly from the unique low cylinder and disjoint binary
bit ranges.
