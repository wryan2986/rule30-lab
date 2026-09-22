# Problem 1 run 201 — exposed driver bits are exact residence erasers

Status: `partial-proof`. Problem 1 remains OPEN.

Continue only the corrected run-193--200 chain. The run-200 handoff asked whether the complete-driver bits selecting the three front histories can be charged independently to finite original support. Comparing the classification with the established original-cut residence identity shows a sharper fact: the exposed bits are not a new independent charge. They are exactly the successive shared-left-neighbor bits in the global front's eraser trace.

## 1. Imported exact residence law

For the fixed original cuts, let `s_j=tau(L_j)` and `J(u)=min{j:s_j>u}`. The established global-front theorem gives

    J(u)=j  iff  s_(j-1) <= u < s_j.

During a residence on characteristic `j`, the shared actual/shadow bit immediately left of the front is 0 before the final row and 1 on the final row. If the residence ends at threshold `s_j`, its erasing cell is

    (i,u)=(j-s_j, s_j-1).

No new experiment is used here.

## 2. The bit p is exactly the first eraser decision

Run 196 fixes

    J(t+8)=t+8.

Run 197 gives

    r_-1(t+8)=1 xor p,

and classifies

    p=0 => J(t+9)=t+9,
    p=1 => J(t+9)=t+8.

At row `t+8`, while `J=t+8`, the front is at physical position 0, so the shared cell immediately left of it is precisely `r_-1(t+8)`.

Hence:

* if `p=0`, then `r_-1(t+8)=1`; this is the final erasing 1. The residence ends at the next row, so

      s_(t+8)=t+9,

  and the residence-law erasing cell is exactly `(-1,t+8)`;

* if `p=1`, then `r_-1(t+8)=0`; this is a nonfinal residence bit, so characteristic `t+8` persists to row `t+9`.

Thus `p` does not merely correlate with the residence choice: `1 xor p` is literally the first exposed bit of the residence eraser trace.

## 3. Conditional on persistence, w3 is exactly the next eraser decision

On the `p=1` branch, run 199 gives

    r_-2(t+9)=w3.

Run 200 classifies

    w3=0 => J(t+10)=t+8,
    w3=1 => J(t+10)=t+9.

Since `J(t+9)=t+8`, the front on row `t+9` is at physical position `-1`; its shared immediate-left cell is exactly `r_-2(t+9)=w3`.

Therefore:

* if `w3=1`, this is the final erasing 1, and

      s_(t+8)=t+10.

  The residence-law erasing cell is exactly `(-2,t+9)`, matching the run-200 local calculation;

* if `w3=0`, it is a nonfinal residence bit and the same characteristic remains the front through `t+10`. In particular

      s_(t+8) >= t+11.

So the `p=1,w3=1` branch has an exact two-row residence on characteristic `t+8`, while `p=1,w3=0` has residence length at least three rows. The run-200 wording that the latter merely gives a two-row residence understated what follows from the already-known `J(t+8)=t+8`.

For comparison, the `p=0` branch has an exact one-row residence on characteristic `t+8`, then run 200 gives `J(t+9)=J(t+10)=t+9`, so the next characteristic `t+9` has residence length at least two rows and `s_(t+9)>=t+11`.

## 4. Consequence for the proposed finite-support charge

This closes one proposed route rather than proving the theorem. The newly exposed low complete-driver bits are not, by themselves, distinct consumable resources that can be counted against the original finite support. They are a re-expression of the already established residence eraser word (zeros followed by its final one) along the same global front.

Therefore a putative argument of the form "each persistence event consumes a fresh low driver bit, hence finite support bounds the number of events" is invalid without an additional injective map from these spacetime eraser cells back to a finite set of original-support objects with bounded reuse. The global-front note already explains why such bounded reuse is the missing step: different residence erasers are distinct spacetime cells, but their ancestry can overlap and cancel, and the initial discrepancy tail is infinite.

The useful structural bridge is exact:

    complete-driver selector bits
        = shared-left-neighbor eraser trace
        = threshold/residence decisions for the fixed original cuts.

This means further local propagation of successive driver bits will only reproduce the existing residence law unless it supplies a genuinely new ancestry/reuse restriction. The next productive target should therefore be the missing bounded-reuse/global-support lemma, not another row of the corrected front table.

No claim from invalidated runs 184--192 is used.

Dependencies: `problem1_run196_complete_driver_forces_corrected_tplus8_branch.md`, `problem1_run197_corrected_tplus9_front.md`, `problem1_run199_corrected_tplus10_front.md`, `problem1_run200_complete_tplus10_front_classification.md`, `problem1_global_discrepancy_front.md` Sections 1--3.