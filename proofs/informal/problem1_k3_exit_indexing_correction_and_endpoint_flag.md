# Problem 1: K=3 exit indexing correction and exact endpoint flag

Status: exact correction to the two immediately preceding K=3 spatial notes; Problem 1 remains OPEN.

## 1. Indexing correction

Section 5 of `problem1_three_bit_exit_repair.md` says: "Write the first five right cells of the shadow at v as (0,a,b,c,d)." At the exit, the already-established condition is `hat r_1(v)=0`. Therefore the intended coordinates are

    (hat r_1,hat r_2,hat r_3,hat r_4,hat r_5)(v)=(0,a,b,c,d),

not `(hat r_0,...,hat r_4)=(0,a,b,c,d)`.

The previous note `problem1_k3_exit_spatial_repair_constraint.md` shifted this tuple one cell left and consequently identified `a` with `hat r_1(v)`. That identification is false: `a=hat r_2(v)` is not fixed by the exit condition. The derived five-prefix filter and the follow-up five-state closure discussion must therefore not be used as proved restrictions.

This correction is independently forced by the repair note's own four-step formula. Direct Rule-30 transport with center inputs 0,1,1,1 and initial right cells `(r_1,...,r_5)=(0,a,b,c,d)` gives

    h=hat r_1(v+4)=(1 XOR a)(1 XOR b)(c OR d),

exactly equation (6) of the repair note. Shifting the tuple to `(r_0,...,r_4)` does not reproduce that equation.

## 2. Correct spatial repair filter

The repair condition is `h=0`, hence

    a=1 OR b=1 OR (c,d)=(0,0).

Thus among the 16 four-bit words `(a,b,c,d)`, only

    0001, 0010, 0011

are excluded. There is no justified `a=0` restriction. The correct necessary filter has 13 words, not five.

## 3. Exact formula for the previously unresolved endpoint bit

Extend the initial shadow by one more right cell:

    (hat r_1,...,hat r_6)(v)=(0,a,b,c,d,e).

Four direct Rule-30 updates with the same justified shadow-center inputs 0,1,1,1 give

    k=hat r_2(v+4)
     = (b AND NOT a)
       OR (NOT a AND NOT c)
       OR (d AND NOT b AND NOT c)
       OR (e AND NOT b AND NOT c).

This is an exact Boolean identity. Together with `e_endpoint=d_0(v+6)=1 XOR k`, it resolves most endpoint types already at the exit.

On the repair domain `h=0`:

* If `a=0`, then necessarily `k=1`; every repaired word in this subcase ends CYCLIC (`e_endpoint=0`). The five words previously listed happen to be exactly the repaired `a=0` words, but they are only one subcase, not the whole exit domain.
* If `a=1,b=0,c=1`, then `k=0`, independent of `d,e`; the endpoint is center-only.
* If `a=1,b=1`, then `k=0`, independent of `c,d,e`; the endpoint is center-only.
* If `(a,b,c,d)=(1,0,0,1)`, then `k=1`, independent of `e`; the endpoint is cyclic.
* The only repaired four-bit prefix whose endpoint type still needs the sixth right cell is `1000`; there `k=e`.

So the unresolved endpoint datum has been reduced from a generic extra bit to one exceptional prefix `1000`. A correct source state need not always retain an additional endpoint flag: the first four post-zero right bits determine it in 12 of the 13 repaired prefixes.

## 4. Research consequence

`problem1_k3_exit_spatial_repair_constraint.md` and `problem1_k3_five_prefix_closure_blocker.md` contain an indexing error and should be treated as superseded by this note. Their temporal dependencies (`2221`, period >=5, backward phase restrictions) are unaffected.

The next source-restricted target is now sharper: couple the complete periodic driver to the correctly indexed bit `a=hat r_2(v)`. If the complete-core phase forces `a=0`, every K=3 exit repairs cyclically. If it forces `a=1`, the endpoint is already determined except at prefix `1000`, where one more shadow cell `e=hat r_6(v)` is required. This is a substantially smaller closure problem than an unrestricted extra endpoint flag.

Dependencies: `problem1_three_bit_exit_repair.md`, `problem1_k3_exit_period_phase_restriction.md`. Supersedes: `problem1_k3_exit_spatial_repair_constraint.md`, `problem1_k3_five_prefix_closure_blocker.md`.
