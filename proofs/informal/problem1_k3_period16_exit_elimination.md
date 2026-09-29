# Problem 1: K=3 exits cannot have complete-core period 16

Status: exact computer-assisted finite exhaustion of the complete temporal-driver domain, with all one-bit shadow phase forks and dyadic lift doublings retained. Problem 1 remains OPEN.

## 1. Context

At an eventual-K=3 `u,h=0` exit the pushed complete-driver results force

    (b_0,b_1,b_2,b_3)=(2,2,2,1),

together with the exact backward resetting-phase condition.

Every finite A-cycle has dyadic least period: deleting one spatial low bit sends a child cycle to a parent cycle, and the exact one-bit lift theorem permits only period preservation or doubling. Hence the earlier formal period-five words cannot be finite A-cycle cores.

The preceding exact period-eight calculation excludes p=8. The concurrently added
`problem1_period16_doubling_layer_reduction.md` independently shows that a finite p=16 exit core would have to lie at least four period-preserving lifts below its canonical anti-periodic 16->8 doubling layer.

This note eliminates p=16 completely.

## 2. Coupled shadow lifts and future drivers

At an exit time v let

    C_m = L_m(hat r(v))

be the phase-correct cyclic shadow cut through right cell m, and define

    u_m(s)=bit_0(A^s C_m).

The exact nested scalar scans are

    u_1(s+1)=b_s[1] XOR (b_s[0] OR u_1(s)),
    u_2(s+1)=b_s[0] XOR (u_1(s) OR u_2(s)),
    u_m(s+1)=u_(m-2)(s) XOR (u_(m-1)(s) OR u_m(s)),  m>=3.   (1)

The physical cut identity gives

    L_0(hat r(v+n)) = A^n C_n.

Therefore the complete temporal driver at physical offset n is

    b^(n)_s = 2 u_(n-1)(s+n) + u_n(s+n),             (2)

and the shadow right pair is

    (hat r_1,hat r_2)(v+n)
      = (u_(n+1)(n),u_(n+2)(n)).                     (3)

All phases are read in the actual period of the relevant lift. Equations (2)-(3) couple every later source to the SAME original shadow.

## 3. Exact period-16 domain

Write

    b = 2221 b_4 ... b_15.

There are `4^12` suffixes. Retain:

1. exact least temporal period 16;
2. the pushed backward exit phase

       gamma = 1[b_ell=1],

   where ell<0 is the last 1/3 reset before phase zero.

Exactly

    8,388,480

period-16 words satisfy those requirements.

No finiteness condition is imposed. Thus every finite p=16 exit core is included, together with additional periodic 2-adic cores.

## 4. Source automaton used in the exhaustion

Only already-pushed FULL source laws are used.

At an even CYCLIC source:

- the complete driver begins `3g`, with `g in {1,2}`;
- gate u is exactly `g=2`;
- the exact birth law is

      chi = gate_u XOR 1[(hat r_1,hat r_2)=00];

- after two physical steps the next source is cyclic for `chi=0` and one-bit for `chi=1`.

At an even ONE-BIT source:

- the complete driver begins `2g`, with `g in {1,2}`;
- gate t returns after two steps to a one-bit source;
- gate u with `hat r_1=1` returns after two steps to a cyclic source;
- gate u with `hat r_1=0` is the K=3 exit. It must begin `2221`, repair requires

      hat r_1(t+4)=0,

  and the endpoint type is

      e = 1 XOR hat r_2(t+4),

  with e=0 cyclic and e=1 one-bit.

The checker iterates this source automaton using (2)-(3).

## 5. Phase forks and period doubling are retained exactly

A fixed-period shadow scan is insufficient. At each one-bit spatial lift, the scalar return map can have:

- one recurrent P-period response: unique phase;
- two recurrent P-period responses: a genuine same-period phase fork;
- no P-period response: the return map toggles after P, giving exact period 2P.

The last case is a legitimate period doubling, not a contradiction.

The checker therefore carries both same-period branches when two exist. When there is no P-period response, it explicitly constructs both 2P-periodic phases, repeats all earlier traces to period 2P, and continues the nested scan.

This is exactly the one-bit lifting theorem applied to the coupled shadow hierarchy.

## 6. Exact exhaustive result

Among the 8,388,480 phase-compatible exact-period-16 words:

- 8,386,657 retain a unique period-16 shadow phase long enough to hit a FULL contradiction;
- zero uniquely phased words survive;
- 1,823 words encounter a phase fork or legitimate period doubling before that contradiction.

The unique-phase failures all occur by physical offset +42. Their exact histogram is

    4:1572330
    6:3775833
    8:1602920
    10:793388
    12:356591
    14:156559
    16:71035
    18:31662
    20:14322
    22:6582
    24:2962
    26:1363
    28:622
    30:266
    32:119
    34:50
    36:12
    38:39
    42:2.

For the 1,823 exceptional words, the first non-unique/doubling lift depths are

    5:1020, 9:510, 11:128, 15:127, 17:4, 19:8,
    20:13, 21:9, 22:1, 23:1, 25:1, 28:1.

Carrying every exact phase choice through shadow depth 72 produces

    3,647

terminal shadow branches. There are at most three branches for any one base word, and the largest shadow period required is 32.

Every one of those 3,647 branches also contradicts FULL. Their failure offsets are

    4:1021, 6:1244, 8:765, 10:274, 12:200, 14:75,
    16:36, 18:20, 20:7, 22:1, 24:2, 26:2.

Thus no exceptional branch survives even to the unique-phase worst-case horizon.

Therefore

    NO exact-period-16 complete driver can support
    an eventual-K=3 u,h=0 exit.                       (4)

The calculation is exhaustive over the entire temporal-driver domain and over every recurrent shadow phase needed by the source laws. It does not assume uniqueness of finite A-cycles.

## 7. Consequence

Finite A-cycle periods are dyadic. Periods 4, 8, and 16 are excluded for a K=3 exit. Hence every such finite exit core satisfies

    p >= 32.                                          (5)

Under the pushed eventual-K=3-but-not-K=1 decomposition, infinitely many exits are required. Therefore every sufficiently late exit must carry a dyadic complete core of period at least 32.

Problem 1 remains open: (5) is not yet an all-scale growth theorem.

## 8. Research consequence / stopping fence

Brute-force p=32 enumeration would require `4^28` suffixes and is not a viable continuation.

The p=8 and p=16 exclusions instead point to an all-scale renormalization problem combining:

1. the nested lift recurrence (1), including derivative phase forks and period doubling;
2. the cyclic/one-bit/repair source automaton of Section 4;
3. the existing reverse-basin derivative singularities at dyadic scales;
4. the canonical doubling-layer reduction in `problem1_period16_doubling_layer_reduction.md`.

A useful next theorem would show that the bounded-horizon contradiction is inherited across a dyadic doubling layer, or that any source-compatible lift must force the next period doubling before the source automaton can close.

Do not start a raw p=32 word census.

Checker:
`experiments/problem1_nonperiodicity/check_k3_period16_exit_elimination.cpp`.

Atomic result:
`results/problem1/20260929_k3_period16_exit_elimination.json`.

Dependencies: `problem1_k3_period8_exit_elimination.md`;
`problem1_period16_doubling_layer_reduction.md`;
`problem1_one_bit_extension_cycle_lifting_theorem.md`;
`problem1_full_driver_exit_phase.md`;
`problem1_exit_wait_front_residence.md`;
`problem1_three_bit_exit_repair.md`;
`problem1_shadow_gate_birth_phase.md`;
`problem1_reverse_predecessor_uniqueness_reset_lemma.md`;
`problem1_derivative_lift_antiperiodicity.md`.
