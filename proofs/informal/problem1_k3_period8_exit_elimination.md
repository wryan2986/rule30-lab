# Problem 1: K=3 exits cannot have complete-core period 8

Status: exact dyadic-period reduction plus finite-exhaustive period-8 classification and symbolic source transport; Problem 1 remains OPEN.

## 1. First correction: period five is not an admissible finite core

At a K=3 `u,h=0` exit, the pushed wait/phase results give

    (b_0,b_1,b_2,b_3)=(2,2,2,1)

for the complete driver `b=Theta(z)`, and the backward phase argument rules out period four, so the recent local analysis proceeded to formal period-five words.

For the actual finite cyclic core `z`, however, the least A-period is always a power of two.

Indeed, repeatedly project a finite A-cycle by one low bit. The exact one-bit cycle-lifting theorem says that a periodic child over a parent cycle of exact period `q` has exact period either `q` or `2q`, irrespective of whether the parent lift is unique. Starting from the zero/one-bit projection therefore gives only dyadic periods. Since `Theta` conjugates A to temporal shift and is injective, the least period of `b=Theta(z)` is the same dyadic period.

Hence

    p>=5  ==>  p>=8.                                  (1)

The preceding period-five shadow-scan note is algebraically consistent as a periodic-word calculation, but its two candidate words cannot be temporal codes of finite A-cycles and are vacuous for the finite FULL problem.

## 2. Exact finiteness test in temporal-code coordinates

Use the reviewed temporal code

    Theta(x)_t=A^t(x) mod 4

and the exact spatial-deletion map `Phi` satisfying

    Theta(pi x)=Phi(Theta(x)),   pi(x)=x>>2.

For a purely period-8 word `b`, let `x=Theta^{-1}(b)` in Z_2. Then

    x is a finite integer
      iff Phi^N(b)=00000000 for some N.                (2)

The forward implication follows because sufficiently many two-bit deletions kill a finite integer. The reverse implication follows from injectivity of Theta.

Because Phi acts on only `4^8` period-8 words, (2) is decidable exactly: iterate until zero or until a word repeats. No spatial-width cutoff is used.

Now enumerate only the four free suffix symbols in

    b = 2221 b_4 b_5 b_6 b_7,

retain exact least period 8, and impose the already-proved backward exit-phase condition

    gamma = 1[b_ell=1],

where `ell<0` is the last 1/3 reset before phase zero.

There are 128 phase-compatible period-8 words. Exact Phi iteration leaves only four finite cores:

| driver b | Phi steps to zero | spatial bitlength |
| --- | ---: | ---: |
| `22211033` | 152 | 303 |
| `22212223` | 34 | 67 |
| `22212330` | 107 | 213 |
| `22213330` | 146 | 292 |

Thus these four words exhaust every finite period-8 complete core compatible with the K=3 exit prefix and backward phase.

## 3. Exact source-to-source driver transport

Let

    C_m = L_m(hat r(v))

be the phase-correct shadow cut through right cell m at the exit time v, and let

    u_m(s)=bit_0(A^s C_m).

The pushed nested recurrences are

    u_1(s+1)=b_s[1] XOR (b_s[0] OR u_1(s)),
    u_2(s+1)=b_s[0] XOR (u_1(s) OR u_2(s)),
    u_m(s+1)=u_(m-2)(s) XOR (u_(m-1)(s) OR u_m(s)),  m>=3.   (3)

For each of the four finite period-8 candidates, the recurrent solution of (3) is unique through every depth used below.

There is also an exact transport formula for the complete driver at a later physical time. The shadow cut identity gives

    L_0(hat r(v+n)) = A^n C_n.

Since the low two bits of `C_n` have temporal traces `u_n,u_(n-1)`,

    b^(n)_s
      = 2 u_(n-1)(s+n) + u_n(s+n),                  (4)

with phases taken modulo 8. By the global-shadow theorem this is exactly the temporal code of `cyc(Y_(v+n))), even when the actual row is not itself cyclic.

Equation (4) is the source-to-source coupling that the recent local notes were missing.

## 4. The four candidates all fail

The exact scan through `u_12` gives:

| exit driver | (r1,...,r6) at v | e at v+6 | driver at v+6 | shadow pair at v+6 | driver at v+8 | shadow pair at v+8 | driver at v+10 |
| --- | --- | ---: | --- | --- | --- | --- | --- |
| `22211033` | `010011` | 0 | `32330011` | `10` | `20111220` | `11` | `12221331` |
| `22212223` | `001101` | 0 | `31101211` | `10` | `32321220` | `11` | `20221330` |
| `22212330` | `011000` | 1 | `21021100` | `11` | `23122331` | `10` | `03130121` |
| `22213330` | `001110` | 0 | `30201211` | `10` | `02321220` | `11` | `10221333` |

All four satisfy the exact six-step repair condition. Here `e=0` means the repaired endpoint is cyclic and `e=1` means a center-only discrepancy.

Now apply only already-pushed FULL source laws.

### 22211033

At v+6 the endpoint is cyclic with driver `32330011`. Its second symbol is 2, so the actual gate is u. The shadow right pair is `10`, hence `hat u=0`. The exact cyclic-source birth law therefore gives

    chi = u XOR hat u = 1.

So v+8 is a one-bit source. But its complete driver is `20111220`, whose first two symbols are `20`. At a FULL one-bit source with `b_0=2`, the second symbol must be 1 (gate t) or 2 (gate u). Symbol 0 is impossible. Contradiction.

### 22212223

At v+6 the endpoint is cyclic with driver `31101211`. Its gate is t and the shadow pair is `10`, so `u=hat u=0` and there is no birth: v+8 is cyclic.

At v+8 the driver is `32321220`, so the gate is u; the shadow pair is `11`, again `hat u=0`. Hence the birth law gives `chi=1`, making v+10 a one-bit source. Its driver is `20221330`, beginning `20`, again impossible for a FULL one-bit source. Contradiction.

### 22212330

At v+6 the repaired endpoint has a center-only discrepancy with driver `21021100`. The second symbol is 1, so this is the one-bit t branch, and its shadow first-right bit is 1 (shadow pair `11`).

The exact one-bit passage table for gate t, h=1 gives delays `1,0,1`; therefore v+8 is again a one-bit source. But its driver is `23122331`, beginning `23`. A FULL one-bit source permits only second symbol 1 or 2. Contradiction.

### 22213330

At v+6 the repaired endpoint is cyclic, but its driver is `30201211`, beginning `30`. A FULL cyclic even source requires its second symbol to be 1 or 2. Contradiction immediately.

Therefore

    NO eventual-K=3 u,h=0 exit can have complete-core period 8.   (5)

Combining (1) and (5), every such exit satisfies

    p>=16.                                                   (6)

Under the pushed eventual-K=3-but-not-K=1 decomposition, infinitely many exits are required, so every sufficiently late exit lies on a complete core of dyadic period at least 16.

## 5. Scope and next target

This is not a period-16 exclusion and does not bound the number of exits. The finite exhaustion is only the exact p=8 case, with no width cutoff: finiteness is decided by the reviewed Phi dynamics on all `4^8` periodic words.

The useful structural addition is (4): future complete drivers can be transported from one exit by the nested shadow scans themselves. This avoids treating the repaired endpoint as a fresh independent core.

The next useful target is therefore NOT another arbitrary core-word census. One should exploit the dyadic lift structure to classify the period-16 descendants compatible with the p=8 exclusion, or derive a general obstruction showing that a K=3 exit core cannot remain compatible with FULL after its six-step source transport.

Checker: `experiments/problem1_nonperiodicity/check_k3_period8_exit_elimination.py`.

Dependencies: `problem1_one_bit_extension_cycle_lifting_theorem.md`; `problem1_activity_sparse_temporal_codes.md` Sections 1-2; `problem1_full_driver_exit_phase.md`; `problem1_exit_wait_front_residence.md`; `problem1_three_bit_exit_repair.md`; `problem1_shadow_gate_birth_phase.md`; `problem1_k3_exit_period_phase_restriction.md`; `problem1_k3_exit_indexing_correction_and_endpoint_flag.md`.
