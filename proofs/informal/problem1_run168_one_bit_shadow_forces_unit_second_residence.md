# Run 168: the one-bit global shadow forces the second original-cut residence

Status: `partial-proof`. Problem 1 remains OPEN.

## Setup

Continue from run 167. At a sufficiently late one-bit gate-u nonresetting source at even physical time `t`, the original-cut stopping times satisfy

    s_t = s_(t+1) = t+1,
    s_(t+2) in {t+1,t+2}.

Thus the first post-source characteristic `t+1` is skipped. The remaining binary question is whether characteristic `t+2` is also skipped.

Use the SAME original finite actual row and its original global E shadow. The established nonresetting-source classification fixes the one-bit gate-u source low cells as follows. FULL gives actual bits 0..3

    (r_0,r_1,r_2,r_3)(t) = (1,1,1,0),

while the global shadow has center 0, shadow bit1=u=1, and agrees with the actual row from bit2 onward, hence

    (hat r_0,hat r_1,hat r_2,hat r_3)(t) = (0,1,1,0).

No wider driver bit is needed below.

## Exact first-right discrepancy one step later

Rule 30 in these coordinates is

    r_i(t+1) = r_(i-1)(t) XOR (r_i(t) OR r_(i+1)(t)).

At physical position 1 this gives for the actual row

    r_1(t+1) = 1 XOR (1 OR 1) = 0,

and for the same original global shadow

    hat r_1(t+1) = 0 XOR (1 OR 1) = 1.

Therefore actual and shadow differ at physical position 1 at time `t+1`.

Run 167 already proved

    J(t+1) >= t+2,
    m(t+1)=J(t+1)-(t+1) >= 1.

The global-front theorem identifies `m(t+1)` with the physical position of the leftmost actual-vs-original-shadow discrepancy. Since position 1 is a discrepancy, the lower bound is sharp:

    m(t+1)=1,
    J(t+1)=t+2.

By definition `J(t+1)` is the least characteristic index `j` with `s_j>t+1`. Since run 167 gives `s_(t+1)=t+1` and monotonicity plus zero delay gives `s_(t+2)<=t+2`, the identity `J(t+1)=t+2` forces

    s_(t+2)=t+2.

Hence the second original-cut increment is exactly

    Delta_(t+1)=s_(t+2)-s_(t+1)=1.

So every sufficiently late one-bit gate-u nonresetting source begins with the exact original-cut itinerary

    (Delta_t,Delta_(t+1)) = (0,1).

Equivalently: characteristic `t+1` is skipped, while characteristic `t+2` is visited for exactly one physical step.

## Significance and next fence

This resolves the binary branch left by run 167 without confusing cyclicization delay with residence. The first increment came from the threshold identity plus monotonicity; the second is fixed by a direct cell of the SAME original global E shadow.

The next unresolved quantity is `s_(t+3)`. Existing source delay data through `t+2` do not determine it. The useful next step is to combine the now-fixed `(0,1)` prefix with the classified cyclic return at `t+2` and its global-shadow cells, then determine whether the next original-cut increment is forced or whether a genuine wider-driver branch remains.

Dependencies: `problem1_run167_one_bit_source_forces_skipped_next_characteristic.md`; `problem1_nonresetting_core_returns.md` Section 3; `problem1_global_discrepancy_front.md` for the front identity.
