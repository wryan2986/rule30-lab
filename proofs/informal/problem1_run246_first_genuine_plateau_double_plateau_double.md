# Problem 1 — run 246: first genuine plateau / double / plateau / double pattern

Problem 1 remains open.

Run 245 identified the correct next computational target: find a `D/P/D` pattern whose first doubling is itself preceded by a plateau, so that run 243's consecutive-doubling compatibility theorem cannot explain the intermediate plateau complexity.

## Exact order computation through coordinate 19

I exhaustively enumerated the triangular Rule-30 permutation on every state for widths 1 through 20. Because all observed cycle lengths are powers of two, the permutation order is the maximum cycle length. The resulting prefix orders are

\[
(O_0,\ldots,O_{19})=
(1,2,2,4,8,8,16,32,32,64,64,64,128,256,256,512,512,1024,1024,2048).
\]

The new part beyond the previously used width-9 data is especially useful:

\[
O_{13}=256,\quad O_{14}=256,\quad O_{15}=512,\quad O_{16}=512,\quad O_{17}=1024.
\]

Thus the first genuine decision pattern of the type requested by run 245 is

\[
\boxed{P/D/P/D}
\]

across the transitions `13->14->15->16->17`, i.e.

\[
\boxed{256\to256\to512\to512\to1024}.
\]

Equivalently, the local `D/P/D` block

\[
256\to512\to512\to1024
\]

has its initial doubling preceded by a plateau. Therefore run 243's `double/double` compatibility theorem does not apply to this example.

There is immediately another instance:

\[
\boxed{512\to512\to1024\to1024\to2048}
\]

across coordinates 15 through 19.

## Sampling the first genuine case

For 20,000 uniformly random width-18 initial states I computed the exact prefix-state periods through coordinates 14, 15, 16, and 17. I retained states satisfying

\[
(p_{14},p_{15},p_{16})=(256,512,512),
\]

which realizes the genuine `P/D/P` history through the plateau at coordinate 16. For each retained state I computed the cyclic binary linear complexity of the length-512 coordinate-16 word, and separately recorded whether the next prefix period doubles to 1024.

The sample split was:

- 457 states with `p_17=1024` (the final doubling occurs),
- 465 states with no final doubling.

Every one of all 922 retained states had

\[
\boxed{L(X_{16})=451}.
\]

So in the first unconfounded `P/D/P/D` setting, the next-doubling functional does **not** appear to select between low- and high-complexity plateau branches. Both outcomes of the final decision occur while the plateau complexity is the same.

This is stronger evidence than runs 244–245 in an important sense: the fixed plateau complexity persists even though the preceding doubling is *not* the second of two consecutive doublings.

## Second genuine case

I repeated the same experiment one scale higher with 20,000 random width-20 states, retaining

\[
(p_{16},p_{17},p_{18})=(512,1024,1024).
\]

The retained states split into:

- 221 states with `p_19=2048`,
- 241 states without that final doubling.

Every retained state again had the same plateau complexity,

\[
\boxed{L(X_{18})=964}.
\]

Thus the same phenomenon repeats at the next `P/D/P/D` block.

## Relation to the run-242 half-block formula

Run 242's plateau-after-doubling identity predicts, in the first case,

\[
L(X_{16})=256+L(X_{14})+1
\]

on the compatible branch. The observed value 451 therefore corresponds to

\[
L(X_{14})=194.
\]

Likewise the second observed value gives

\[
964=512+451+1.
\]

This strongly suggests that the useful recursive object is not “does the following doubling select the maximal plateau branch?” but rather the complexity forced by a **full prefix-period history**. The numbers line up recursively:

\[
\boxed{194\longmapsto451=256+194+1\longmapsto964=512+451+1.}
\]

The next task should therefore move one level earlier and explain the base value 194 at coordinate 14 from its actual order history. If that can be derived structurally, the run-242 half-block recurrence may propagate exact complexity through the later `P/D/P` blocks without any appeal to a following doubling.

## Status / caution

The order sequence through coordinate 19 is exhaustive and exact. The linear-complexity statements at coordinates 16 and 18 are sampled computational evidence, not yet universal proofs. They are nevertheless enough to show that both outcomes of the final-doubling decision occur in the same observed complexity class, so the selection interpretation from run 244 is no longer the promising target.
