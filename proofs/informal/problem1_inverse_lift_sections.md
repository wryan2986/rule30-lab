# Exact branch recurrence for inverse diagonal lifts

Status: complete informal proof of the stated recurrence, plus a bounded
finite-state obstruction. This is a partial structural result, not a proof of
Rule 30 center nonperiodicity or an exclusion of eventual period two.

## 1. Binary-tree sections of the right-edge map

For a 2-adic map `F`, write

\[
F(a+2R)=\pi_F(a)+2F_a(R),\qquad a\in\{0,1\},
\]

where `pi_F` is its action on the low bit and `F_a` is its section at
input bit `a`. Let

\[
T(S)=S\mathbin{\mathtt{xor}}
((S\ll1)\mathbin{\mathtt{or}}(S\ll2)).
\]

There are two additional maps that close the sections of `T`. Define `P` by

\[
T(1+2R)=1+2P(R)
\]

and let `U=J\circ T`, where `J(S)=S\mathbin{\mathtt{xor}}1` toggles the low
bit. Direct digit calculation gives

\[
\begin{aligned}
T(2R)&=2T(R),\\
T(1+2R)&=1+2P(R),\\
P(2R)&=1+2U(R),\\
P(1+2R)&=2P(R),\\
U(2R)&=1+2T(R),\\
U(1+2R)&=2P(R).
\end{aligned}
\]

Thus, in rooted-tree notation, their root actions and sections are

\[
T=(T,P),\qquad P=(U,P)\sigma,\qquad U=(T,P)\sigma,
\]

where `sigma` swaps zero and one. The set `{T,P,U}` is closed under taking
sections. Each map is unit triangular and therefore a 2-adic isometric
bijection.

The inverse maps `t=T^{-1}`, `p=P^{-1}`, and `u=U^{-1}` also form a
section-closed set:

\[
t=(t,p),\qquad p=(p,u)\sigma,\qquad u=(p,t)\sigma.
\]

For an inverse, the section at an output-root value is the inverse of the
forward section at its unique preimage root. This gives the displayed
identities directly.

## 2. First even and odd lift identities

For a map `F`, define its orbit diagonal by

\[
\operatorname{bit}_n(\Delta_F(S))
=\operatorname{bit}_n(F^n(S)).
\]

The original diagonal map is `Delta_T`. Since
`T^n(2R)=2T^n(R)`, for `n>=1` its output bit `n` is output bit `n-1` of
`Delta_T(T(R))`. Hence

\[
\boxed{\Delta_T(2R)=2\Delta_T(T(R)).}
\]

An odd `T`-orbit remains odd and its tails evolve under `P`, so similarly

\[
\boxed{\Delta_T(1+2R)=1+2\Delta_P(P(R)).}
\]

Writing `G_F=Delta_F^{-1}` gives the exact inverse branches

\[
\boxed{G_T(2D)=2T^{-1}(G_T(D))}
\]

and

\[
\boxed{G_T(1+2D)=1+2P^{-1}(G_P(D)).}
\]

The odd branch explains why repeatedly dropping temporal bits does not leave
one copy of `G_T`: it immediately introduces a different orbit diagonal.

Iterating the even identity gives, for every `j>=0`,

\[
\boxed{\Delta_T(2^jR)=2^j\Delta_T(T^j(R))}
\]

and therefore

\[
\boxed{G_T(2^jD)=2^jT^{-j}(G_T(D)).}
\]

## 3. Exact recurrence for arbitrary section schedules

The change of diagonal map can be handled without approximation. Let
`A=(A_0,A_1,...)` be a schedule of 2-adic tree automorphisms. Starting from
`X_0=S`, set

\[
X_{n+1}=A_n(X_n),\qquad
\operatorname{bit}_n(\Delta_A(S))=\operatorname{bit}_n(X_n).
\]

Write `S=a+2R`. Let `a_n` be the low bit of `X_n` and define the tail
schedule

\[
B_n=(A_n)_{a_n}.
\]

The tails satisfy `R_(n+1)=B_n(R_n)`. Removing the first output bit therefore
gives

\[
\boxed{
\Delta_A(a+2R)=a+2\Delta_{\sigma B}(B_0(R)),
}
\]

where `sigma B=(B_1,B_2,...)`. Consequently,

\[
\boxed{
G_A(a+2D)=a+2B_0^{-1}(G_{\sigma B}(D)).
}

This is a genuine recursion for every inverse-lift bit. If `A` is periodic
with period `ell`, then its root path has period dividing `2 ell`; hence `B`
is periodic with period dividing `2 ell`. Starting from the constant schedule
`T,T,...`, every new schedule still uses only `{T,P,U}` and has an exactly
computable finite period. This does **not** give one depth-independent period:
the bound may double at the next recursion.

To emit seed bits rather than entire 2-adic tails, retain an accumulated
postcomposition `H`. For

\[
F_{H,A}=H\circ G_A,
\]

reading temporal bit `a` emits `pi_H(a)` and moves to

\[
\boxed{
(H,A)\longmapsto
(H_a\circ B_0^{-1},\,\sigma B).
}

Starting at `(id,T^infinity)` generates exactly `Delta_T^{-1}`. This is the
recurrence implemented by
`experiments/problem1_nonperiodicity/analyze_inverse_lift_sections.py`.
Its accumulated map is represented as a composition of `{t,p,u}`; the
section formulas above make every transition exact.

## 4. Exact base-4 renormalization for the alternating trace

Let

\[
A=-\frac13=1+4A,
\]

whose low-first temporal digits repeat the block `10`. For a schedule
`W`, write `G_W=Delta_W^(-1)` and

\[
F_{H,W}=H\circ G_W.
\]

Let `rho(H)` be the root flip of `H`, and let `H_v` be its section at the
input word `v`. Process one complete temporal block, first `1` and then `0`.
All three forward maps have section `P` at input one, so the first transition
appends `p=P^(-1)`. Applying the composition-section rule at the second bit
then gives the exact block transition

\[
\boxed{H^+=H_{11}\,p\,q(W),}
\]

where composition is written outermost to innermost and

\[
q(W)=
\begin{cases}
u,&W_0=T,\\
t,&W_0\in\{P,U\}.
\end{cases}
\]

The new periodic schedule `W^+` is obtained by applying the exact one-bit
schedule transition first at input one and then at input zero. Denote the
combined state transition by

\[
\mathcal R(H,W)=(H^+,W^+).
\]

The two emitted spatial bits depend on `H` as

\[
\boxed{
\beta(H)=
(1\mathbin\oplus\rho(H))
+2(1\mathbin\oplus\rho(H_1)).
}
\]

Because removing the temporal block `10` leaves `A` again, this proves the
base-4 renormalization

\[
\boxed{
F_{H,W}(A)=\beta(H)+4F_{\mathcal R(H,W)}(A).
}
\]

Starting from `Q_0=(id,T^infinity)` and writing
`Q_m=R^m(Q_0)`, the first two exact states are

\[
Q_1=(pu,(P,U)^\infty),
\qquad
Q_2=(uppt,(U,P,P,T)^\infty).
\]

Consequently, for `S=G_T(A)`,

\[
S=3+4\,pu\,G_{(P,U)^\infty}(A)
\]

and

\[
S=7+16\,uppt\,G_{(U,P,P,T)^\infty}(A).
\]

The temporal block repeats, but the inverse state does not.

This also reformulates the dyadic endpoint conjecture exactly. Base-4 block
`2^(k-1)-1` contains bit `2^k-1` as its high bit, so

\[
\boxed{
\operatorname{bit}_{2^k-1}(S)
=1\mathbin\oplus\rho((H_{2^{k-1}-1})_1).
}
\]

An induction must therefore control the root activity of a selected section
after `2^(k-1)` further applications of `R`. Each block transition replaces
`H` by `H_11` before appending two known generators. Determining the state
directly through depth `d` after `M` more blocks consequently calls for a
portrait of the current `H` whose depth grows with `2M`; the changing schedule
supplies an additional state. Group relations or a quotient could conceivably
compress this information, but no closed quotient retaining the displayed
root activity is known.

A concrete fixed-depth obstruction is available. The identity automorphism
and `p^2` act identically modulo four, but

\[
\rho((\mathrm{id})_{11})=0,
\qquad
\rho((p^2)_{11})=1.
\]

Indeed, `(p^2)_1=pu` and `(pu)_1=pt`, whose root action is a flip. Thus the
modulo-four action of the accumulated automorphism cannot determine even the
next depth-two-section activity required by the block recurrence.

## 5. The diagonal map is not finite-state

The iterated even identity gives an exact theorem, not merely a finite
diagnostic. The tree section of `Delta_T` along the input word consisting of
`j` zero bits is

\[
\Delta_T\circ T^j.
\]

These sections are pairwise distinct. If

\[
\Delta_T\circ T^j=\Delta_T\circ T^k,
\]

bijectivity of `Delta_T` would imply `T^j=T^k`. But `T^j(1)` has highest set
bit exactly `2j`: one application of `T` creates a unique new highest bit two
positions above the old one. Thus `j=k`.

> **Theorem.** `Delta_T` has infinitely many tree sections and is not a
> finite-state tree automorphism.

The inverse sections along zero input prefixes are
`T^{-j} circ G_T` and are also pairwise distinct. Hence `G_T` is not
finite-state either. This rules out a universal finite section family for the
diagonal or inverse-diagonal map. It does not rule out a smaller quotient
tailored to one periodic input word.

## 6. What the period-two control shows

For the pure alternating trace with low-first digits `1010...`, the bounded
default audit follows this exact recurrence through 16 input bits. The
induced schedule periods after each bit are

\[
1,2,2,4,8,8,16,32,32,64,64,64,128,256,256,256.
\]

The schedule therefore reaches period 256 even though the driving trace has
period two. With the stated six-bit lookahead, all 17 inverse sections along
that trace prefix are distinct. Three independent finite inverse oracles
agree on every quotient residue through width 10.

These are finite-exhaustive statements only for the listed bounds. In
particular:

- schedule growth through depth 16 does not prove unbounded growth;
- distinct six-bit section tables can merge or split at other lookaheads;
- failure of this naive finite-state closure does not exclude a smaller
  quotient sufficient for a proof; and
- the alternating lift's observed nonzero bits do not prove infinitely many
  nonzero bits.

Two small exact block controls reject still simpler lift rules. Let `S_m` be
the alternating trace's inverse prefix and let `E_m` be the next `m` seed
bits. Then

\[
S_2=3,\qquad E_2=1,
\]

so a phase-repeated independent-block rule `E_m=S_m` already fails. More
strongly,

\[
S_3=S_5=7,\qquad E_3=0,\qquad E_5\equiv6\pmod8.
\]

Depths three and five have the same period-two phase and the same complete
seed prefix value, but incompatible low three bits of the next block. This
refutes any depth-independent 2-adic block function using only
`(S_m, m mod 2)`. It does not refute a rule with additional nonlocal or
growing state.

A separate capped induction probe found

\[
\operatorname{bit}_{2^k-1}(G_T(-1/3))=k\bmod2
\]

for exactly `1<=k<=8`, at positions
`1,3,7,15,31,63,127,255`. This is a finite observation, not an induction.
If proved for every `k`, the odd exponents would provide infinitely many
nonzero lift bits and would exclude a purely alternating trace for finite
spatial support. No recurrence proving the step from `k` to `k+1` is known.

Two natural induction attempts already fail. The global rule

\[
s_{2n+1}=1-s_n
\]

would imply the endpoint pattern, but at `n=5` both `s_5` and `s_11` are
zero. Likewise, the dyadic extension blocks `E_2=1` and `E_4=12` reject the
copy rule

\[
E_{2m}=E_m+2^mE_m,
\]

which predicts 5 at `m=2`; the corresponding copied-complement value is 10,
not 12. Any successful induction must therefore use a richer invariant
specialized to the all-one binary indices `2^k-1`, not ordinary block
self-similarity.

Rowland's power-of-two local-nesting theorem was also checked as a possible
induction source. It proves convergence on each fixed edge coordinate along
power-of-two times, equivalently recovery of every fixed finite prefix as the
exponent grows. The endpoint here samples coordinate `2^k-1` at the same
scale, so it escapes every fixed recovered prefix. The theorem therefore
does not supply the missing endpoint induction. See Eric Rowland,
[“Local Nested Structure in Rule 30”](https://doi.org/10.25088/ComplexSystems.16.3.239).

## 7. Proof consequence

The desired finite-support statement has become an exact transducer-output
question: for an eventually periodic temporal input beginning with one, show
that the recurrence emits spatial one bits infinitely often. The complete
universal state cannot be bounded, by the theorem above. A useful
continuation must therefore prove a period-specific quotient or invariant of
the accumulated inverse automorphism and the section schedule that

1. has a depth-independent state bound, and
2. still detects whether all future emitted spatial bits can be zero.

Merely increasing the inverse prefix, schedule depth, or section lookahead
does not address that missing theorem.
