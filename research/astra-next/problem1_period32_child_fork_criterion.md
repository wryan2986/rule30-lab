# Problem 1: exact child-fork criterion on period-32 lift chains

Status: exact algebraic lemma. This sharpens the remaining all-depth rigidity target after the canonical period-32 finite-depth probe. It does **not** exclude period 32 by itself; Problem 1 remains OPEN.

## 1. Setup

Write a period-32 parent temporal symbol as

    e_s = b_s + 2 c_s,   b_s,c_s in {0,1}.

A one-bit child has

    d_s = a_s + 2 b_s

with response recurrence

    a_(s+1) = c_s XOR (b_s OR a_s).

The only possible recurrent responses are obtained from the two initial states `a_0=0,1`.

## 2. Reset lemma

If `b_s=1` at any phase, then

    a_(s+1) = c_s XOR 1,

independently of `a_s`.

Therefore one occurrence of an odd parent symbol resets the two response trajectories to the same state. After that reset they remain identical around the rest of the cycle. Consequently:

> **Lemma.** A cyclic parent word with at least one odd symbol has exactly one recurrent one-bit child.

This is period-independent; period 32 is not used in the proof.

If instead `b_s=0` for every phase, the recurrence is linear:

    a_(s+1) = a_s XOR c_s.

After one full period,

    a_32 = a_0 XOR XOR_s c_s.

Hence:

- if `XOR_s c_s = 1`, there is no recurrent period-32 response;
- if `XOR_s c_s = 0`, both initial states recur, giving two complementary low-bit responses.

Thus zero/one/two recurrent children are characterized exactly by the low bitplane and, in the all-even case, the parity of the high bitplane.

## 3. Consequence for canonical chains

Let `L_j(s)` be the low bitplane of the temporal word at lift depth `j`. Since the child's high bitplane is the parent's low bitplane,

    H_(j+1) = L_j.

The canonical period-32 starting layer `q(1-q)` contains exactly sixteen 1s in its low plane, so its first child is unique.

More generally, along any already-defined canonical chain:

> the next lift is unique **iff** `L_j` is not the zero word.

Moreover, if a unique child at depth `j` has `L_j=0`, then applying its defining recurrence with `a=L_j=0` gives

    H_(j-1) = L_(j-1)

pointwise. Using `H_(j-1)=L_(j-2)`, this is

    L_(j-2) = L_(j-1).

Conversely, adjacent equality `L_(j-2)=L_(j-1)` forces the next response `L_j` to be zero. Therefore, before the first fork/death,

> **fork/death precursor equivalence:** `L_j=0` iff `L_(j-2)=L_(j-1)`.

So the all-depth uniqueness problem has been reduced from a two-state cyclic-response question to a binary-plane collision question:

> prove that no canonical chain descending from `q(1-q)` ever has two consecutive equal low bitplanes.

This is a substantially narrower target than re-running the 65,536-chain probe to larger depth.

## 4. Dead end checked

A tempting stronger invariant is that every low bitplane remains anti-periodic under a 16-shift. That is false already after the first lift for generic canonical seeds, so it should not be used as the rigidity invariant.

A global-vector repeat search was also run locally through more than 8,000 lift depths without finding a repeated ordered 65,536-state layer. Thus a short global period of the complete canonical layer is not the explanation for the observed depth-1000 rigidity.

## 5. Next target

Study the induced recurrence on consecutive low planes `(L_(j-1),L_j)` and exclude the diagonal `L_(j-1)=L_j` on the canonical initial family. Because `H_j=L_(j-1)`, the entire symbol word at depth `j` is already determined by this pair, so no information is lost by this reduction.

Separately, the source contradiction still needs an all-depth bounded invariant; the finite probe's observed latest failure at physical offset `+34` remains empirical rather than uniform.