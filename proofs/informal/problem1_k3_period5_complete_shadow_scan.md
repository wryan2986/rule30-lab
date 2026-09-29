# Problem 1: K=3 period-five cores determine the exit shadow prefix

Status: exact complete-driver calculation on the two period-five candidates left by the pushed forward/backward phase restrictions; Problem 1 remains OPEN.

## 1. Setup

At an eventual-K=3 one-bit `u,h=0` exit at even time `v`, the pushed complete-driver results give a resetting least-periodic word `b=Theta(z)` with

    (b_0,b_1,b_2,b_3)=(2,2,2,1),

and the backward phase test rules out period four. If the least period is five, the same test leaves exactly

    22212, 22213.

The corrected repair coordinates are

    (hat r_1,...,hat r_6)(v)=(0,a,b,c,d,e).

This note computes those shadow bits from the SAME complete periodic core rather than supplying them independently.

## 2. Nested scalar scans

Let `u_m(s)` be the low A-trace of the shadow cut through right cell `m`; thus `u_m(0)=hat r_m(v)`. Projection of A gives the exact nested recurrences

    u_1(s+1)=b_s[1] XOR (b_s[0] OR u_1(s)),
    u_2(s+1)=b_s[0] XOR (u_1(s) OR u_2(s)),
    u_m(s+1)=u_(m-2)(s) XOR (u_(m-1)(s) OR u_m(s)),  m>=3.      (1)

The first line is the already-pushed one-bit scan. The second is the same Rule-30 low-bit rule applied to `4z+2u_1+u_2`; for `m>=3`, bit 1 of the cut through cell m is `u_(m-2)` and bit 0 is `u_(m-1)`, giving (1).

For a fixed periodic pair of input traces, each line is a two-state affine/reset scan. Its recurrent period-p solutions can therefore be checked exactly by one traversal from each initial bit. No free right-fringe bits are introduced.

## 3. Exact period-five evaluation

For both candidate cores the unique recurrent first trace compatible with the exit phase `u_1(0)=h=0` is

    u_1 = 01011                 (phases 0,...,4).

Iterating (1) around the same five-cycle gives unique recurrent traces through `u_6` in both cases.

For core `22212`:

    (u_1(0),u_2(0),u_3(0),u_4(0),u_5(0),u_6(0))
      =(0,1,1,0,0,0).

Hence

    (a,b,c,d,e)=(1,1,0,0,0).

For core `22213`:

    (u_1(0),u_2(0),u_3(0),u_4(0),u_5(0),u_6(0))
      =(0,0,1,0,0,1),

so

    (a,b,c,d,e)=(0,1,0,0,1).

These values are periodic-shadow phases selected by the complete core; they are not arbitrary local assignments.

## 4. Consequences for the corrected repair flag

The corrected endpoint note gives

    k=hat r_2(v+4)
     =(b AND NOT a)
       OR (NOT a AND NOT c)
       OR (d AND NOT b AND NOT c)
       OR (e AND NOT b AND NOT c),

with endpoint center discrepancy `e_endpoint=1 XOR k`.

Substitution yields:

* `22212`: `a=b=1`, hence `k=0` and `e_endpoint=1`. The six-step repair returns to a center-only discrepancy.
* `22213`: `a=0`, hence `k=1` and `e_endpoint=0`. The six-step repair returns CYCLIC.

Both satisfy the necessary repair condition. Thus period five is NOT eliminated by the corrected spatial phase calculation. Instead its two surviving complete cores have different, fully determined endpoint types.

In particular the exceptional local prefix `1000`, whose endpoint required the sixth right bit in the corrected four-bit analysis, does not occur for either period-five core.

## 5. Research consequence / stopping fence

This calculation removes the apparent freedom in `a=hat r_2(v)` for the shortest remaining complete cores: the nested complete-driver scan determines not only `a` but the whole shadow prefix needed by the repair law. However, neither period-five candidate is contradicted locally.

The next useful question is therefore global: determine how a repaired endpoint with core `22212` (center-only) or `22213` (cyclic) transports to the NEXT source/core on the same finite FULL orbit. Enumerating longer periodic words at one isolated exit would repeat a local classification without addressing that coupling.

Dependencies: `problem1_full_driver_exit_phase.md`, `problem1_k3_exit_period_phase_restriction.md`, `problem1_three_bit_exit_repair.md`, `problem1_k3_exit_indexing_correction_and_endpoint_flag.md`.
