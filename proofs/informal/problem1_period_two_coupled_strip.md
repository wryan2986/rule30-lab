# Coupled moving strip for the period-two inverse lift

Status: exact all-width moving-cut and local-transfer identities, plus a
complete rational classification of one universal nearest-neighbor additive
cocycle ansatz. These are partial structural and no-go results. They do not
exclude period two and do not solve Rule 30 center nonperiodicity.

## 1. Three representations of one orbit

Let

\[
T(S)=S\mathbin{\mathtt{xor}}((S\ll1)\mathbin{\mathtt{or}}(S\ll2))
\]

be the Rule 30 right-edge map, and let

\[
S=\Delta^{-1}(-1/3)\in\mathbb Z_2
\]

be the unique 2-adic seed whose growing diagonal is the pure alternating
trace. Put

\[
R_m=T^{2m}(S).
\]

At even time `2m`, let `A_m` be the autonomous right fringe, encoded from the
center outward:

\[
A_m=\sum_{j\ge0}a_j(m)2^j,
\qquad a_j(m)=x_{j+1}(2m).
\]

The fringe starts at `A_0=0` and has exactly `2m` available positions after
`m` two-step blocks. Let `rev_n` denote reversal of exactly `n` bits.

The schedule-survivor theorem defines `X_m` as the unique 2-adic state that
emits zero forever under the actual future branch schedule beginning at block
`m`.

## 2. Exact moving-cut identity

Right-edge coordinates enumerate the row from its moving right edge inward.
At time `2m`, the center is exactly `2m` cells behind that edge. Therefore the
`2m` cells strictly to the right of center occur in the reverse order from the
center-outward encoding `A_m`. The remaining inward tail begins with the center
and continues to the left.

The previous moving-tail theorem identifies that inward tail with `X_m`.
Consequently, for every finite quotient width `W>2m`,

\[
\boxed{
T^{2m}(S)
\equiv
\operatorname{rev}_{2m}(A_m)+2^{2m}X_m
\pmod {2^W}.
}
\tag{1}
\]

This is not a numerical correspondence between two separately generated
objects: the fringe and survivor are literally the low and high halves of one
moving Rule 30 row.

There is an ordinary finite-shadow version. Let

\[
S_m=S\bmod 2^{2m}
\]

and let `H_m` be the accumulated inverse word after `m` alternating blocks.
The right-edge map is unit triangular, so its low `2m` output bits depend only
on the low `2m` seed bits. The finite arithmetic support theorem identifies the
remaining high part with `H_m^{-1}(0)`. Hence, as an equality of ordinary
nonnegative integers,

\[
\boxed{
T^{2m}(S_m)
=
\operatorname{rev}_{2m}(A_m)
+2^{2m}H_m^{-1}(0).
}
\tag{2}
\]

Equation (2) explains the exact finite shadows from the earlier gluing result:
they preserve the true fringe below the moving seam while replacing the true
survivor above it by an ordinary finite tail.

Finally, the pair emitted by the whole-word transducer is the next pair of
seed bits:

\[
\boxed{H_m(11)=(S_{2m},S_{2m+1}).}
\tag{3}
\]

Thus eventual terminal state `00` is exactly eventual termination of the
original seed, not merely an auxiliary acceptance condition.

## 3. Local width-growing strip transfer

Reverse the established outer-to-inner word `H_m` and call the low-to-high
word `J_m`. The four-state whole-word transducer scans `J_m` from left to
right, beginning in state `11`. If its emitted word is `\tau_{11}(J_m)` and
its terminal state is `e_m`, then reversal of

```text
H_(m+1) = (H_m)|_11 p q_m
```

gives

\[
\boxed{
J_{m+1}=q_m\,p\,\tau_{11}(J_m),
\qquad e_m=H_m(11).
}
\tag{4}
\]

At the same time,

\[
A_{m+1}=F(A_m)
\tag{5}
\]

under the exact autonomous two-step fringe map, and

\[
q_m=
\begin{cases}
u,&A_m\equiv0\pmod4,\\
t,&\text{otherwise}.
\end{cases}
\tag{6}
\]

Both rows have width `2m`, and both grow by two cells per block. Equations
(4)-(6) are therefore an exact coupled strip transfer:

- the fringe row supplies the left boundary letter `q_m`;
- the inverse-word row is transformed across its complete width;
- and the terminal scan state at the opposite boundary is the reconstructed
  spatial pair.

The transfer is local when the scan state is included as a horizontal tile
label. This is the precise two-row system proposed after the whole-word
transducer result.

## 4. Exact fringe-head transition relation

Write the low fringe head as

\[
h_m=(a_0(m),a_1(m)).
\]

Exhausting the two farther imported bits in the radius-two update gives the
complete local relation

\[
\begin{array}{c|c}
h_m&\text{possible }h_{m+1}\\ \hline
00&10,11\\
01&11\\
10&01,11\\
11&00,01.
\end{array}
\tag{7}
\]

It contains the directed cycle

\[
00\to10\to01\to11\to00,
\]

so any universal potential monotone on all local head tiles is constant. The
next calculation strengthens this from a head-only potential to the first
coupled word/head additive ansatz.

## 5. Nearest-neighbor coupled additive ansatz

For a nonempty word `J=j_0...j_(n-1)`, consider the most general rational
nearest-neighbor functional

\[
F(J)=L(j_0)+\sum_{i=0}^{n-2}W(j_i,j_{i+1})+R(j_{n-1}),
\tag{8}
\]

with `F(empty)=0`. Let `P_h` be a potential on the four fringe-head states,
`V_e` a potential on the four terminal scan states, and `K` a constant.

The first coupled telescoping attempt asks for

\[
F(J^+)-F(J)+P_{h^+}-P_h=V_e+K
\tag{9}
\]

on every whole-word scan, every head `h`, and every locally allowed transition
`h->h^+` in (7), where

\[
J^+=q(h)\,p\,\tau_{11}(J).
\]

Equation (9) would bridge the complete word interior while allowing the fringe
head and reconstructed pair to appear only as boundary terms.

## 6. Complete rational solution

There are 24 variables:

- nine pair weights `W_ab`;
- three left weights `L_a` and three right weights `R_a`;
- four head potentials `P_h`;
- four terminal potentials `V_e`;
- and `K`.

The equations from words of length at most three and the seven local head
edges have rank 18. Exact rational row reduction gives the following complete
parametrization. There are arbitrary numbers `r_t,r_p,r_u`, a constant head
potential `P`, a constant terminal potential `V`, and `K`. Put

\[
c=\frac{V+K}{2}.
\]

Then

\[
W_{ab}=r_a-r_b+c,
\qquad
L_a=-r_a+c,
\qquad
R_a=r_a,
\tag{10}
\]

and

\[
P_{00}=P_{01}=P_{10}=P_{11}=P,
\tag{11}
\]

\[
V_{00}=V_{01}=V_{10}=V_{11}=V.
\tag{12}
\]

Substituting (10) into (8) telescopes the `r` terms and leaves

\[
\boxed{F(J)=c\,|J|.}
\tag{13}
\]

Conversely, (10)-(12) satisfy (9) for every word because the width increases
by exactly two:

\[
F(J^+)-F(J)=2c=V+K.
\]

The finite length-three system is sufficient for a complete all-word
classification: every universal solution must satisfy that finite subsystem,
which already forces (10)-(12), and that forced form directly verifies (9) for
arbitrary length.

Therefore:

> **Coupled range-two additive no-go.** Every universal rational
> nearest-neighbor additive cocycle for the coupled head/word tiles is a
> multiple of word length, up to an identically zero boundary coboundary. The
> fringe-head potential and terminal-pair potential are constant. In
> particular, the increment cannot distinguish `q=t` from `q=u`, nor `00` from
> a nonzero reconstructed pair.

This closes the first growing-memory linear ansatz beyond single-letter
counts.

## 7. Scope and next target

The result does **not** show that no invariant exists. It leaves open:

- nonlinear functionals of the strip;
- additive functionals with memory growing with the row width;
- identities valid only on the unique actual fringe orbit rather than every
  locally allowed head tile;
- and original-spacetime arguments using more than the low fringe head.

The moving-cut identity (1) suggests the next admissible target: a nonlinear
quantity defined directly on the complete right-edge row

\[
\operatorname{rev}_{2m}(A_m)\,||\,X_m
\]

whose evolution under `T^2` detects whether the high half is an ordinary
finite integer. Another larger fixed head table or a wider linear word-count
ansatz would repeat the failure classified above.
