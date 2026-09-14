# Astra automation handoff — 2026-09-14 run 29

Branch: `research/astra-next`

## Repository state reviewed

Run started from `7e5112c2fc12edce20d053a6443449f32b7a0aca` (run 28 handoff). No newer work was present on `research/astra-next`.

Run 28 had closed the commutator-memory subproblem by proving that the terminal commutator state is a local moving-boundary function, and asked to feed that bounded classification back into immediate re-entry and the global recurrence/residence machinery.

Problem 1 remains open.

## New result 1: exact first-collision mask and fringe-endpoint re-entry test

Added:

- `proofs/informal/problem1_collision_defect_and_endpoint_reentry_classification.md`
- `scripts/check_collision_endpoint_reentry.py`

Commits:

- `4b7792d5d1535ceef2d2671b845b07ab62c0d204` — theorem;
- `765559b4171a46ca3623fb04361887261874f6cb` — checker.

Let

\[
T^p(z)=2^{2p}z+R,
\quad
G=2p-\operatorname{bitlength}(R)>0,
\quad
D=\lfloor G/2\rfloor,
\]

and let

\[
x=T^{D+1}(z)
\]

be the first row that leaves the guaranteed return-fringe persistence block.

Using the run-28 closed commutator formula at the last persistent row gives the complete first-collision-mask classification:

\[
\boxed{G\text{ odd}\Longrightarrow E_p(x)=1,}
\]

and

\[
\boxed{
G\text{ even}\Longrightarrow
E_p(x)=
\begin{cases}
3,&R\text{ even},\\
1,&R\text{ odd}.
\end{cases}}
\]

So the collision mask is determined solely by `G mod 2` and `R mod 2`.

For odd long corridors `G=2D+1>=3`, the previous low-row criterion translates entirely to the fringe endpoint:

\[
\boxed{
E_p(Tx)=0
\iff
R\equiv
\begin{cases}
1\pmod4,&p+D\text{ even},\\
3\pmod4,&p+D\text{ odd}.
\end{cases}}
\]

For even long corridors `G=2D>=4`, every odd `R` is now excluded from immediate re-entry because it produces collision defect 1 while the run-28 terminal commutator state lies in `{0,1}`, whereas defect-1 re-entry requires terminal state 3.

For even `R`, define

\[
H(R)=0
\]

for leading four bits `1000,1001,1010,1011,1100`, and `H(R)=1` for `1101,1110,1111`. Then immediate re-entry occurs iff

\[
\boxed{H(R)=D\bmod2}
\]

and

\[
\boxed{
R\bmod8=
\begin{cases}
2,&p+D\text{ even},\\
6,&p+D\text{ odd}.
\end{cases}}
\]

Thus the complete one-step re-entry question for every long corridor uses only bounded endpoint data of `R`; no interior fringe/source-history variable remains.

The exact period-8 finite-extension graph contains 126 exact-period-8 even-corridor states with `G>=4`; the endpoint theorem has zero mismatches on all 126, including 7 genuine immediate re-entries.

## New result 2: re-entry cannot regenerate another long same-period corridor

Added:

- `proofs/informal/problem1_immediate_reentry_collapses_return_corridor.md`
- `scripts/check_reentry_corridor_collapse.py`

Commits:

- `150c452a696cb73aae1ff99c57109651de6b7ab1` — initial proof;
- `47f2e3a717a324c6e8412211afe60fc6b7110844` — tightened/corrected proof text;
- `033dce5156875eedb0292aeacf1f7fd85e9c5c3f` — exact p=4/p=8 checker.

Suppose the first collision immediately re-enters, and put

\[
z'=T^{D+2}(z),
\qquad A^p(z')=z'.
\]

If `R'` is the new return fringe of `z'`, triangularity modulo `2^(2p)` gives the exact transport identity

\[
\boxed{R'=T^{D+2}(R)\bmod2^{2p}.}
\]

A separate leading-edge lemma is useful beyond this application. If `w` is any nonzero finite word and `q>=4`, then the fifth bit from the leading edge of `T^q(w)` is always 1.

Writing relative leading bits as

\[
a_j^{(q)}=(T^q w)_{h+2q-j},
\]

they obey

\[
a_j^{(q+1)}=a_{j-2}^{(q)}\oplus(a_{j-1}^{(q)}\lor a_j^{(q)}).
\]

From `q>=2`, `a_2=0`, so

\[
a_3' = 1\oplus a_3,
\qquad
a_4'=a_3\lor a_4,
\]

which forces `a_4=1` at step 4 and forever after.

Applying that lemma to the transported fringe proves:

### Even corridor

For

\[
G=2D\ge4,
\]

`T^(D+2)(R)` has bitlength `2p+4`. Its fifth leading bit is exactly position `2p-1`, which survives reduction modulo `2^(2p)`. Hence

\[
\boxed{G'=0.}
\]

### Odd corridor

For

\[
G=2D+1\ge5,
\]

`T^(D+2)(R)` has bitlength `2p+3`. Its fifth leading bit is position `2p-2`, so after truncation

\[
\boxed{G'\le1.}
\]

Therefore, except for `G=3`, an immediate re-entry is an isolated same-period event: it cannot reset directly into another long same-period persistence plateau.

This is the first direct bridge from the local collision classification back toward the global residence/recurrence question.

## Exact finite-state evidence

At exact period 8 there are 63 immediate re-entries from corridors `G>=3`:

- `G=3`: 47;
- `G=4`: 7;
- `G=5`: 9;
- `G=6,7,8,9,10`: 0.

Their post-re-entry corridor gaps are:

- `G=3`: 31 cases with `G'=0`, 16 with `G'=1`;
- `G=4`: all 7 have `G'=0`;
- `G=5`: 2 have `G'=0`, 7 have `G'=1`.

Period 4 likewise has two `G=3` re-entries, both with `G'<=1`.

Thus the uncovered `G=3` case also collapses in every exact finite-state example currently checked, but this is not yet proved.

## Remaining sharp local case: G=3

For `G=3`, only three fringe steps occur before the re-entered state:

\[
R'=T^3(R)\bmod2^{2p}.
\]

The four-step universal leading-edge lemma does not apply.

A direct 16-case calculation on the first five leading bits shows that the fifth leading bit of `T^3(R)` can be zero only when `R` begins with one of

- `10001`,
- `10010`,
- `10011`.

All other five-bit leading prefixes already force the same `G'<=1` conclusion.

The next best target is therefore very narrow: prove that a genuine `G=3` return fringe satisfying the exact immediate-re-entry bottom-bit condition cannot begin with those three prefixes, or construct a genuine counterexample. The p=4 and p=8 exact extension graphs contain no counterexample.

## Global status

Problem 1 is still open. The old global bottleneck in `ASTRA_HANDOFF.md` remains: FULL/common-origin/residence arguments still need a finite-support contradiction for an actual survivor, not merely a local collision analysis.

However, the local obstruction is now substantially reduced:

1. first collision mask: bounded exact classification;
2. immediate re-entry: bounded exact endpoint classification;
3. regeneration after re-entry: impossible for all `G>=4` even and all `G>=5` odd;
4. only `G=3` remains before one-step re-entry can be treated uniformly as terminating a long same-period corridor.

After settling `G=3`, return to the FULL/common-origin/front-residence machinery rather than extending the already-closed commutator automaton route.