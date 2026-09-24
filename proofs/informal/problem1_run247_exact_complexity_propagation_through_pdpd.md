# Problem 1 — run 247: exact complexity propagation through the genuine P/D/P/D blocks

Problem 1 remains open.

Run 246 found the first genuine `P/D/P/D` order blocks and sampled constant plateau complexities

\[
L(X_{16})=451,\qquad L(X_{18})=964,
\]

but left the base value `L(X_14)=194` unexplained and the constancy statements unproved.  In fact the earlier run-243 and run-242 lemmas already combine to prove all three values exactly for every state with the corresponding full prefix-period history.

## 1. The apparently new base value 194 is exactly the run-243 theorem

The exact global order history from run 246 contains

\[
O_{11}=64,\quad O_{12}=128,\quad O_{13}=256,\quad O_{14}=256.
\]

This is precisely the run-243 pattern

\[
Q\to2Q\to4Q\to4Q
\]

with `Q=64`.  Therefore run 243 gives immediately

\[
\boxed{L_{14}(256)=3Q+2=194.}
\]

More strongly, inspect any state whose actual prefix periods satisfy

\[
(p_{11},p_{12},p_{13})=(64,128,256).
\]

The proof of run 243 is statewise: full period 256 at level 13 forces the coordinate-12 word over 128 steps to have complementary 64-halves, hence complexity 65.  The run-242 OR half-difference identity at the plateau extension then gives forcing complexity 193 and cyclic integration gives

\[
\boxed{L(X_{14}^{[256]})=194.}
\]

Thus 194 is not a new unexplained constant and does not require computation.

## 2. Exact propagation to 451

Now condition on the genuine history used in run 246:

\[
(p_{14},p_{15},p_{16})=(256,512,512).
\]

Since the transition 14→15 doubles the actual state period, the length-512 coordinate-15 word has complementary 256-halves.  The run-242 plateau-after-doubling half-block identity applies statewise to coordinate 16 and gives

\[
L(X_{16})=256+L(X_{14})+1.
\]

For the states arising from the full preceding history above, the previous section gives `L(X_14)=194`.  Hence

\[
\boxed{L(X_{16})=256+194+1=451.}
\]

Therefore the constant 451 observed in all 922 run-246 samples is a theorem for every state satisfying the complete period history

\[
(64,128,256,256,512,512)
\]

through levels 11–16.  The sampled constancy was not accidental.

## 3. Exact propagation to 964

The next observed block has

\[
(p_{16},p_{17},p_{18})=(512,1024,1024).
\]

Applying the same statewise run-242 identity to the doubling 16→17 followed by the plateau 17→18 gives

\[
L(X_{18})=512+L(X_{16})+1.
\]

Substituting the proved value 451 yields

\[
\boxed{L(X_{18})=512+451+1=964.}
\]

Thus the run-246 sample value 964 is likewise forced by the complete prefix-period history.

## 4. General propagation lemma

The useful abstraction is the following statewise rule.

Suppose a state has actual prefix period `P` at level `r-2`, doubles to `2P` at level `r-1`, and remains at `2P` at level `r`.  If the length-`P` coordinate word at level `r-2` has complexity `L>1`, then the run-242 half-block calculation gives

\[
\boxed{L(X_r^{[2P]})=P+L+1.}
\]

Consequently, once one exact complexity is established at the start of a repeated `D/P` chain, every subsequent `D/P` pair propagates it deterministically:

\[
L_{j+2}=P_j+L_j+1.
\]

For the present history this is

\[
194\xrightarrow{P=256}451\xrightarrow{P=512}964.
\]

The following doubling decision is irrelevant to these complexity values.  This rigorously confirms the reinterpretation suggested by run 246.

## 5. What remains

The first genuine `P/D/P/D` examples therefore do not create a new complexity-compatibility obstruction.  Their plateau complexities are completely explained by:

1. one `D/D/P` seed, handled by run 243; and
2. deterministic `D/P` propagation, handled by run 242.

The next useful target is no longer 194.  It is to determine whether every observed long order-decision history decomposes into seeds whose complexity is fixed by consecutive doublings followed by deterministic `D/P` propagation, or whether there is a first plateau pattern (especially consecutive plateaus such as the observed `64→64→64`) where the complexity entering the next doubling is not fixed by these lemmas.  The triple plateau around coordinates 9–11 is the earliest such candidate and should be analyzed before pushing to larger widths.
