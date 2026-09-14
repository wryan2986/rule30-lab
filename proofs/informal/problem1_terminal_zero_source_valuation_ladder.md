# Problem 1: terminal zero-source runs are exact valuation ladders

Status: exact structural lemma plus computational evidence for genuine return-fringe collision states. Problem 1 remains open.

## Setup

Use

\[
T(x)=x\oplus((2x)\lor(4x)),\qquad A(x)=T(x)\gg2.
\]

For a normalized orbit

\[
u_j=A^j(x),\qquad s_j=T(u_j),
\]

the run-21 commutator automaton is driven by `s_j mod 8`. The previous handoff identified source `0 mod 8` as the exact identity symbol of the commutator automaton and therefore the main obstruction to bounded-suffix synchronization.

This note characterizes such source-zero suffixes exactly.

## 1. Rule 30 is negation modulo 8

A direct check of the three low bits gives

\[
\boxed{T(x)\equiv -x\pmod 8.}
\]

Indeed the residue table is

\[
0,1,2,3,4,5,6,7
\mapsto
0,7,6,5,4,3,2,1.
\]

Therefore the source symbol can be read directly from the current normalized state:

\[
\boxed{s_j\equiv -u_j\pmod8.}
\]

In particular,

\[
\boxed{s_j\equiv0\pmod8\iff u_j\equiv0\pmod8.}
\]

The synchronizing source symbol `6 mod 8` from run 21 is equivalently

\[
\boxed{s_j\equiv6\pmod8\iff u_j\equiv2\pmod8.}
\]

So the commutator's identity/reset symbols have a direct orbit-state description: residues `0` and `2` modulo 8 respectively.

## 2. Exact valuation descent on a zero-source step

For every nonzero integer `y`, Rule 30 preserves the 2-adic valuation:

\[
\boxed{v_2(T(y))=v_2(y).}
\]

This is immediate because the least set bit of `y` is untouched by the shifted terms `2y` and `4y`.

Hence if `u_j` is divisible by 8, then no truncation ambiguity occurs in the normalization and

\[
\boxed{v_2(u_{j+1})=v_2(u_j)-2.}
\]

Thus consecutive source-zero symbols are not arbitrary repetitions of the automaton identity: they are forced by a strict 2-adic descent.

## 3. Classification of a length-k zero suffix

Suppose

\[
s_{m},s_{m+1},\ldots,s_{m+k-1}\equiv0\pmod8.
\]

Then every

\[
u_m,u_{m+1},\ldots,u_{m+k-1}
\]

is divisible by 8. Iterating the valuation descent gives

\[
\boxed{v_2(u_m)\ge 2k+1.}
\]

More precisely, write

\[
 u_m=4^k r.
\]

The zero-source condition through the last step is equivalent to `r` being even. Because Rule 30 commutes with powers of four,

\[
T(4^q y)=4^qT(y),
\]

we obtain

\[
\boxed{u_{m+k}=T^k(r)}.
\]

Conversely, if

\[
u_m=4^k r
\]

with `r` even and nonzero, then the next `k` source symbols are all zero modulo 8 and

\[
u_{m+k}=T^k(r).
\]

Therefore:

> **Valuation-ladder classification.** A terminal block of `k` source-zero symbols is exactly a physical Rule-30 evolution of an even core `r`, hidden underneath `k` factors of four in the normalized state.

This is stronger than the abstract automaton statement that source zero acts as the identity: actual zero-source repetitions consume two powers of two per normalized step.

## 4. Bit-length consequence

Every nonzero finite Rule-30 word gains exactly two bits per physical step:

\[
\operatorname{bitlength}(T^k(r))=\operatorname{bitlength}(r)+2k.
\]

Since `r` is even and nonzero, `bitlength(r)>=2`. Thus any length-`k` terminal zero-source run ending at `u_{m+k}` satisfies

\[
\boxed{
2k+2\le \operatorname{bitlength}(u_{m+k}).
}
\]

Equivalently,

\[
\boxed{
k\le\left\lfloor\frac{\operatorname{bitlength}(u_{m+k})-2}{2}\right\rfloor.}
\]

This does not give a period-independent constant bound, but it turns an apparently arbitrary memory-preserving suffix into a rigid finite-ancestor condition.

## 5. Specialization to boundary defects

For a genuine return-fringe boundary collision `x`, the previous notes show

\[
A^p(x)=x\oplus\varepsilon,
\qquad \varepsilon\in\{1,3\}.
\]

If the normalized `p`-orbit has a terminal length-`k` source-zero suffix, the classification above forces an even finite word `r` such that

\[
\boxed{x\oplus\varepsilon=T^k(r).}
\]

At the same time `x` itself is a positive physical-time descendant of the periodic return state that generated the collision. Therefore a terminal zero suffix requires two nearby words,

\[
x\quad\text{and}\quad x\oplus\varepsilon,
\]

to possess distinct finite physical Rule-30 ancestry, with the second ancestry of depth at least `k` and even ancestor core.

This reframes the run-21 obstruction in a form that can potentially interact with FULL/common-origin machinery: long memory-preserving suffixes are equivalent to deep finite physical ancestry of the low-bit-perturbed collision row.

## 6. Computational check on genuine collision states

An exhaustive integer scan was performed for periodic return states

- `1 <= z < 2,000,000`,
- exact pure `A`-period `p <= 20`,
- valid positive return fringe `0 < R < 2^(2p)`,
- positive corridor length `G=2p-bitlength(R) >= 1`.

For each such state, the first boundary-collision row

\[
x=T^{\lfloor G/2\rfloor+1}(z)
\]

was constructed and its length-`p` normalized source word was checked.

The scan found 27 genuine collision states (periods 1, 2, and 4 in this range). **None had even one terminal source-zero symbol.** In every case,

\[
 s_{p-1}\not\equiv0\pmod8.
\]

This is evidence only, not a proof. Arbitrary near-return states can certainly end in source zero; for example there are small `x` with `A^p(x)=x xor 1` or `x xor 3` and terminal source-zero symbols. The observed exclusion is therefore specific to the genuine return-fringe collision geometry rather than to the defect equation alone.

## 7. Research consequence

The best next target is now sharper than merely bounding long zero suffixes:

> Prove or disprove that a genuine first return-fringe boundary collision can **never** satisfy `u_{p-1} == 0 (mod 8)`.

If this empirical exclusion is true, the strongest abstract memory obstruction from run 21 disappears immediately for genuine collisions. One should then classify the remaining terminal source symbols and their transition semigroup, looking for a short synchronizing suffix forced by collision geometry.

A promising proof route is the finite-ancestry formulation above: terminal source zero would imply

\[
x\oplus\varepsilon=T(r)
\]

for an even finite `r`, while `x` is itself a prescribed physical descendant of the periodic return state. The contradiction, if present, should come from the common-origin/return-fringe relation rather than from the defect equation alone.
