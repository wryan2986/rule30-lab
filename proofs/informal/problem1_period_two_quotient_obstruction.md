# Period-two quotient obstruction from the moving fringe

Status: two exact all-width identities, an exhaustive four-state local
corollary, and two finite counterexamples. This is a partial structural result,
not an exclusion of eventual period two and not a solution of Problem 1.

## 1. Question and decision gate

For the pure alternating low-first trace

\[
A=1+2^2+2^4+\cdots=-\frac13,
\]

let `S=Delta_T^(-1)(A)`. The preceding inverse-section analysis left two
concrete possible induction states:

1. the first map in the induced schedule appeared to follow a seven-block
   cycle; and
2. the lift bits appeared to satisfy
   `bit_(2^k-1)(S)=k mod 2`.

Either exact law would materially change the whole-tail argument. A periodic
schedule driver could make a finite period-specific quotient plausible, while
the endpoint law would supply infinitely many nonzero seed bits. An exact
counterexample to either law kills that candidate; finite survival proves
nothing beyond the tested bound.

Both candidates have exact counterexamples below.

## 2. The schedule head is a two-cell spacetime fringe

Write

\[
X_n=T^n(S),\qquad
T(X)=X\mathbin{\mathtt{xor}}
((X\ll1)\mathbin{\mathtt{or}}(X\ll2)).
\]

After the first `d` diagonal bits have been removed by the exact inverse
recurrence, let `W^(d)` be the remaining forward schedule. An induction on
`d` gives

\[
\boxed{
W^{(d)}_n
=T_{\operatorname{low}_d(X_{n+d})},
}
\]

where the subscript denotes the binary-tree section along the listed
low-first input word. For `d=0` this is the constant schedule `T`. If the
formula holds at depth `d`, removing the next root bit takes the corresponding
section of every scheduled map and shifts time once, which is exactly the
formula at depth `d+1`.

The transducer for `T` remembers only its last two input bits. If those bits,
in increasing-position order, are `(a,b)`, then

\[
T_{\cdots ab}=
\begin{cases}
T,&(a,b)=(0,0),\\
U,&(a,b)=(1,0),\\
P,&b=1.
\end{cases}
\]

Consequently, after `m` complete temporal blocks `10`, the first schedule map
is determined exactly by

\[
(r_2(m),r_1(m))
=\bigl(
\operatorname{bit}_{2m-2}(X_{2m}),
\operatorname{bit}_{2m-1}(X_{2m})
\bigr).
\]

This is an identity for every `m`, not a finite pattern inference.

## 3. Autonomous two-step fringe recurrence

Set `r_0=1` at an even phase and write `r_j` for the bit `j` places behind
the sampled diagonal. The next alternating bit is zero. It forces the one bit
immediately ahead of the diagonal to equal one. Define

\[
g_j=r_j\mathbin\oplus(r_{j+1}\lor r_{j+2})
\qquad(j\geq0)
\]

and put `g_(-1)=0`. Two direct Rule 30 updates in the moving frame give

\[
\boxed{
r'_j=g_{j-2}\mathbin\oplus(g_{j-1}\lor g_j),
\qquad j\geq1.
}
\]

The initial inward tail is all zero. Thus the complete schedule-head driver
is an autonomous one-sided recurrence; computing the full exponentially
growing schedule is unnecessary. The formula also explains why the two-cell
state alone need not close: its next value imports `r_3` and `r_4`.

For `(r_2,r_1)` and all four assignments to `(r_3,r_4)`, the exact transition
relation is

\[
\begin{array}{c|c}
(r_2,r_1)&\text{possible }(r'_2,r'_1)\\ \hline
00&01,11\\
01&10,11\\
10&11\\
11&00,10.
\end{array}
\]

The directed cycle

\[
00\longrightarrow01\longrightarrow10\longrightarrow11
\longrightarrow00
\]

is realized by contexts `01`, `10`, `00`, and `01`, respectively, where a
context is written `(r_3,r_4)`. Hence this four-state relation is strongly
connected.

> **Pair-local monotonicity obstruction.** Any real-valued function of only
> `(r_2,r_1)` that is nondecreasing, or nonincreasing, on every locally
> allowed two-step transition is constant.

Indeed, monotonicity around the displayed directed cycle forces equality at
all four states. This excludes a universal monotone invariant of only the
schedule-head pair. It does not exclude a nonlocal tail functional or an
observable valid only on the unique true orbit.

## 4. An actual-path depth-two quotient conflict

The two-bit seed block emitted from an accumulated inverse automorphism `H`
is determined by the root activities of `H` and `H_1`. A natural candidate
quotient therefore retains

\[
O_2(m)=\left(
W_m[0],
(\rho((H_m)_v))_{v=\epsilon,0,1,00,01,10,11}
\right).
\]

This contains the schedule head and the complete root-activity portrait
through depth two. Along the actual alternating path,

\[
O_2(11)=O_2(55)
=\left(T,(0,1,0,0,1,0,1)\right).
\]

The currently emitted blocks are also equal to three. Nevertheless, after
one exact block transition,

\[
\beta(H_{12})=0,
\qquad
\beta(H_{56})=2.
\]

Thus this candidate state does not determine even whether the next emitted
spatial block is zero. This is an exact finite conflict on the unique pure
alternating path. It refutes this depth-two quotient, not every deeper or
nonlocal quotient.

## 5. Exact counterexample to the seven-block driver

The autonomous fringe, the direct rows `T^(2m)(S)`, and the full exact
section schedules agree wherever the full schedule is retained. The head
sequence starts

```text
T P U P T P T P P U P T P T P P ...
```

From block `m=2`, this shadows repetitions of

```text
U P T P T P P
```

through block 152. It first fails at block 153:

\[
\text{candidate head}=T,
\qquad
(r_2(153),r_1(153))=(1,1),
\qquad
\text{actual head}=P.
\]

This is an exact finite counterexample to the proposed seven-block law, not
evidence merely from a hash collision. It also illustrates the hidden-tail
problem: the same apparent phase can receive new information from farther
inside the fringe.

## 6. Exact counterexample to dyadic endpoint parity

The unique finite lift modulo `2^2048` was checked by both packed and ordinary
cell-array forward evolutions. The proposed law

\[
\operatorname{bit}_{2^k-1}(S)=k\bmod2
\]

holds for `1<=k<=10` but fails at the next exponent:

\[
\boxed{
\operatorname{bit}_{2047}(S)=0\ne1=11\bmod2.
}
\]

The 2,048-bit lift has 1,076 ones, its last one is at position 2,046, and its
packed little-endian SHA-256 is

```text
279385743213d9b8b175fd080dbe07762652f5b3e3cf3a25386cd60e6a00da7c
```

These values certify the finite counterexample only. In particular, the zero
at position 2,047 does not suggest that the lift terminates there.

## 7. Exact arithmetic finite-support criterion

The failed finite portraits still leave a narrower, nonlocal arithmetic
target. For the remainder of this section let `m>=1`, let `H_m` be the
accumulated inverse automorphism after `m` temporal blocks, and let

\[
S_m=S\bmod4^m.
\]

After `2m` diagonal bits have been removed, the residual transformed seed is

\[
Y_m=\left\lfloor\frac{T^{2m}(S)}{4^m}\right\rfloor,
\]

and the original seed tail is `H_m(Y_m)`. Replace the original seed by its
truncation `S_m`. Its seed tail is zero, while all consumed diagonal bits and
therefore `H_m` are unchanged. Consequently,

\[
\boxed{
H_m^{-1}(0)=
\left\lfloor\frac{T^{2m}(S_m)}{4^m}\right\rfloor.
}
\]

Let `h_m` be the highest one position of `S_m`. Every application of `T` to a
nonzero finite integer raises its highest one position by exactly two: the
shift by two creates a unique new highest bit. Therefore

\[
\boxed{
\deg(H_m^{-1}(0))=2m+h_m.
}
\]

It follows immediately that

\[
\boxed{
S\text{ has finite support}
\iff
\deg(H_m^{-1}(0))-2m\text{ is bounded}.
}
\]

There is a sharper word form. Write `H_m` outermost-to-innermost as a word of
length `2m` in `t,p,u`, and let `ell_m` be its initial run of `t` letters.
The word is never all `t`; let `epsilon_m=1` when its first non-`t` letter is
`p`, and zero when it is `u`.

To compute `H_m^(-1)(0)`, apply the corresponding forward maps in word order.
Each initial `t` applies `T` to zero and leaves zero. The first `p` sends zero
to 3, of degree one, while the first `u` sends zero to 1, of degree zero.
Every remaining forward map `T`, `P`, or `U` raises the degree of a nonzero
finite integer by exactly two. Hence

\[
\deg(H_m^{-1}(0))=4m-2\ell_m-2+\epsilon_m
\]

and comparison with the preceding identity gives

\[
\boxed{
h_m=2m-2\ell_m-2+\epsilon_m.
}
\]

Parity in this identity gives `epsilon_m=h_m mod 2`, and rearrangement gives
the particularly simple equality

\[
\boxed{
m-\ell_m=\left\lfloor\frac{h_m}{2}\right\rfloor+1.
}
\]

Thus the pure alternating lift has infinite support exactly when

\[
\boxed{m-\ell_m\longrightarrow\infty.}
\]

If the lift instead terminated with highest one at `h`, then eventually

\[
\ell_m=m-\left\lfloor\frac h2\right\rfloor-1,
\]

and the first non-`t` letter would be `p` for odd `h` and `u` for even `h`.
This is an exact reformulation, not yet a growth proof. The recurrence for the
leading run still depends on sections of the complete inner suffix of `H_m`.

## 8. Consequence for the focused program

The complete inverse schedule still has an exact period-two description, but
neither of the two proposed small induction states survives:

- its apparent seven-block driver is false;
- its dyadic endpoint parity law is false; and
- its head-plus-depth-two portrait does not preserve next-block zero status;
- every monotone observable of only the two-cell schedule fringe is trivial.

The strongest surviving target is now explicit: prove that `m-ell_m` tends to
infinity under the exact block recurrence. This retains genuinely nonlocal
word information while asking for only one asymptotic quantity. Enlarging the
observed driver prefix, testing another unguarded endpoint pattern, or storing
a wider fixed fringe without a depth-independent theorem would repeat the
same failure mode.
