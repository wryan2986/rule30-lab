# Problem 1 — run 255: exact phase-shift formula for the endpoint defect

Problem 1 remains open.

Run 254 defined
[
E_r(N;t)=igoplus_{s=0}^{N-1}x_r(t+s)oplus x_{r-2}(t)oplus x_{r-2}(t+N/2)
]
and reduced the next step to understanding (E_r(N;t+N)oplus E_r(N;t)).  This note gives that phase shift exactly once the lower prefix through coordinate (r-2) has closed.

## Theorem

Assume (N) is even and the prefix through coordinate (r-2) is (N)-periodic over the two adjacent blocks:
[
x_j(t+N+s)=x_j(t+s)qquad (jle r-2, 0le sle N).
]
Put
[
a=x_{r-1}(t+N)oplus x_{r-1}(t).
]
Then
[
oxed{
E_r(N;t+N)oplus E_r(N;t)
=
aigoplus_{substack{0le q<N\q {m even}}}(1oplus x_{r-2}(t+q)).
}
]
In particular, if (4mid N),
[
oxed{
E_r(N;t+N)oplus E_r(N;t)
=
aigoplus_{substack{0le q<N\q {m even}}}x_{r-2}(t+q).
}
]

Combining this with run 254's dyadic recursion, whose boundary term vanishes under the same (N)-periodicity hypothesis, gives
[
oxed{
E_r(2N;t)
=
aigoplus_{substack{0le q<N\q {m even}}}(1oplus x_{r-2}(t+q)),
}
]
and for (4mid N),
[
oxed{
E_r(2N;t)
=
aigoplus_{substack{0le q<N\q {m even}}}x_{r-2}(t+q).
}
]

Thus the unknown phase dependence from run 254 factors into exactly two one-bit quantities: the (N)-step skew of coordinate (r-1), and an even-time parity of coordinate (r-2).

## Proof

Write the block difference
[
y_j(s)=x_j(t+N+s)oplus x_j(t+s).
]
Lower-prefix closure gives (y_j(s)=0) for (jle r-2).

Coordinate (r-1) is driven only by coordinates (r-2,r-3), so its forcing is identical in the two blocks. Hence
[
y_{r-1}(s)=a
]
is constant.

For coordinate (r), using (ulor v=uoplus voplus uv) over (mathbb F_2), changing the first forcing input from (u) to (uoplus a) while leaving (v=x_{r-2}) fixed changes the OR by
[
(uoplus a)lor voplus(ulor v)=a(1oplus v).
]
Therefore
[
y_r(s+1)=y_r(s)oplus a(1oplus x_{r-2}(t+s)).
]
Iterating,
[
y_r(s)=y_r(0)oplus aigoplus_{q=0}^{s-1}(1oplus x_{r-2}(t+q)).
]

The endpoint terms in (E_r(N;t+N)oplus E_r(N;t)) cancel by lower-prefix closure, leaving
[
igoplus_{s=0}^{N-1}y_r(s).
]
Because (N) is even, the (N) copies of (y_r(0)) cancel.  A term indexed by (q) occurs for (s=q+1,ldots,N-1), hence (N-1-q) times.  For even (N), this multiplicity is odd exactly when (q) is even.  This proves the first formula.  If (4mid N), there are (N/2) even indices and their constant 1 contribution cancels, proving the simplified form.

Run 254 gives
[
E_r(2N;t)=E_r(N;t)oplus E_r(N;t+N)oplus x_{r-2}(t+N/2)oplus x_{r-2}(t+3N/2).
]
The last pair cancels by (N)-periodicity of coordinate (r-2), yielding the stated factorization.

## Exhaustive check

The factorization was independently checked over every initial prefix state for (r=3,ldots,8) and (N=4,8,16), conditioning only on (N)-periodicity through coordinate (r-2).  There were zero mismatches in every case.

## Consequences and limitation

This resolves the exact blocker named by run 254: the phase-shift defect is now explicit in terms of skew bits.

It does **not** by itself prove the important (E_{11}(64)=0) transport identity, because taking (N=32) would require the prefix through coordinate 9 to be 32-periodic, while the branch relevant to the (32	o64) doubling has coordinate-9 skew and hence does not satisfy that hypothesis.  Applying the theorem there would be circular/invalid.

The next target is therefore precise: derive the corresponding phase-shift formula when the lower prefix is periodic only through coordinate (r-3) and coordinate (r-2) has a constant skew bit.  That is exactly the one-extra-skew situation needed for the (r=11,N=32) triple-64 argument.
