# Run 165: the unique cut itinerary collides with local shadow dynamics

Status: `partial-proof`. Problem 1 remains OPEN. This unit assumes the established sufficiently-late TWO-BIT nonresetting passage hypotheses and the global-front identities already used in runs 153--164. It does not claim a contradiction for the one-bit nonresetting source.

## 1. Input from run 164

Let `q=t+2`. Run 164 proved that a sufficiently late TWO-BIT nonresetting source at `t` would force the complete original-cut residence itinerary

    (d_2,d_3,d_4,d_5) = (0,0,3,2),

where `d_k=s_(t+k+1)-s_(t+k)`, and `s_q=q`.

Hence

    s_(q+1)=q,
    s_(q+2)=q,
    s_(q+3)=q+3,
    s_(q+4)=q+5.

For `J(u)=min{j:s_j>u}` and the global-front identity `m(u)=J(u)-u`, this forces

    m(q)=3,
    m(q+1)=2,
    m(q+2)=1,
    m(q+3)=1.                         (1)

Thus the SAME original actual row and global E-shadow must have first discrepancies at positions `3,2,1,1` on these four consecutive physical rows.

The distinguished actual source at q is already fixed through position 2:

    (r_-5,...,r_2)(q)=10101110.       (2)

In particular

    r_-2=0, r_-1=1, r_0=1, r_1=1, r_2=0.

Because `m(q)=3`, actual and shadow agree at every position below 3 and differ at position 3. Write

    x = r_3(q),     hat r_3(q)=1-x.   (3)

No cell to the right of position 3 is used below.

## 2. Exact local evolution

Use Rule 30 in the form

    F(l,c,r) = l XOR (c OR r).

At time q+1, from (2),

    r_-1' = 0 XOR (1 OR 1) = 1,
    r_0'  = 1 XOR (1 OR 1) = 0,
    r_1'  = 1 XOR (1 OR 0) = 0.

These values are identical for the shadow, because the two rows agree through position 2 at q.

At position 2, however,

    r_2'     = 1 XOR (0 OR x)     = 1 XOR x,
    hat r_2' = 1 XOR (0 OR (1-x)) = x.

So position 2 differs, exactly as `m(q+1)=2` requires.

Advance once more. At q+2,

    r_0'' = 1 XOR (0 OR 0) = 1,
    hat r_0'' = 1,

while

    r_1''     = 0 XOR (0 OR r_2')     = 1 XOR x,
    hat r_1'' = 0 XOR (0 OR hat r_2') = x.

Thus position 1 differs, exactly as `m(q+2)=1` requires, but the common position-0 value is forced to 1.

Now advance to q+3 at position 1. Since the center values at q+2 are complementary and the common left input is 1,

    r_1'''     = 1 XOR (r_1'' OR r_2''),
    hat r_1''' = 1 XOR (hat r_1'' OR hat r_2'').

A direct computation of the needed position-2 values gives

    r_2''     = 0 XOR (r_2' OR r_3')     = r_2' OR r_3',
    hat r_2'' = 0 XOR (hat r_2' OR hat r_3') = hat r_2' OR hat r_3'.

But the simpler decisive observation is at position 0. Its q+3 update uses the common q+2 center `r_0''=hat r_0''=1`, so the differing right input at position 1 is masked:

    r_0''' = r_-1'' XOR (1 OR r_1'') = r_-1'' XOR 1,
    hat r_0''' = hat r_-1'' XOR (1 OR hat r_1'') = hat r_-1'' XOR 1.

The rows agreed to the left, so `r_-1''=hat r_-1''`; hence position 0 still agrees at q+3.

To retain first discrepancy at position 1, position 1 itself would have to differ at q+3. Evaluate it without any unknown wider driver. Since `r_1''` and `hat r_1''` are complementary, there are two cases.

If x=0, then `(r_1'',hat r_1'')=(1,0)`. The actual OR in the position-1 update is automatically 1. On the shadow side `hat r_2'=0`, and the q+1 position-3 shadow update has center `hat r_3(q)=1`, so `hat r_3'=r_2 XOR (1 OR hat r_4)=1`; therefore `hat r_2''=0 OR 1=1`. The shadow OR is also 1.

If x=1, then `(r_1'',hat r_1'')=(0,1)`. The shadow OR is automatically 1. On the actual side `r_2'=0`, and the q+1 position-3 actual update has center `r_3(q)=1`, so `r_3'=r_2 XOR (1 OR r_4)=1`; therefore `r_2''=0 OR 1=1`. The actual OR is also 1.

In both cases

    r_1''' = hat r_1''' = 1 XOR 1 = 0.    (4)

Therefore actual and shadow agree at both positions 0 and 1 at q+3. This contradicts `m(q+3)=1` in (1).

## 3. Consequence

The hypotheses of a sufficiently late TWO-BIT nonresetting passage are inconsistent with the exact original global E-shadow dynamics. Therefore

    boxed: no sufficiently late TWO-BIT nonresetting source can occur.

Equivalently, the `(0,0,3,2)` itinerary found in run 164 is not merely rigid: when combined with the already established distinguished source block, it is unrealizable.

This is stronger than the previous terminal-slack result. It uses no wider right-tail assumption and no finite computation: only the first-discrepancy/global-front identity, the fixed source cells through position 2, and three exact Rule-30 steps.

## 4. Scope / next target

Do not promote this by itself to a solution of Problem 1. The existing nonreset-return theorem has both one-bit (`u=1`) and two-bit (`u=0`) source types. This unit excludes the late two-bit type only. The next useful question is structural: in the eventual K=3/FULL decomposition, does every sufficiently late nonresetting/repair episode necessarily contain a two-bit nonresetting source? The older birth-spacing note states that a two-bit N source is the offset-4 row of a repair, but that implication must be checked in the authoritative repair classification before concluding that all late nonresetting sources are excluded. If the implication is only one-way, repeat the exact-front analysis for the surviving one-bit source rather than assuming it away.
