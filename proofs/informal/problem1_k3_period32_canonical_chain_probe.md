# Problem 1: reduced period-32 canonical-chain probe

Status: exact finite-exhaustive finite-depth computation on the canonical period-32 lift language. This is NOT a period-32 exclusion. Problem 1 remains OPEN.

## 1. Why p=32 is not a 4^28 word search

For a finite exact-period-32 A-cycle, let the first spatial layer where period drops be

    per(x_j)=32,  per(x_(j+1))=16.

The one-bit lift theorem forces the period-doubling layer x_j to have a binary anti-periodic temporal code

    c = q (1-q),

where q is an arbitrary 16-bit binary word. Thus there are only

    2^16 = 65,536

canonical anti-periodic starting layers to consider before the subsequent period-preserving lifts.

This overincludes the finite-core domain: no finiteness condition is imposed on q.

## 2. Exact period-preserving child map

For a parent temporal word e of period 32, a one-bit child d has

    d_s = a_s + 2(e_s mod 2),

    a_(s+1) = floor(e_s/2)
              XOR ((e_s mod2) OR a_s).

A period-32 child is therefore found by solving the two-state recurrent response for a_0 in {0,1}. The computation retains all recurrent period-32 children and explicitly checks for zero, one, or two such responses.

Starting from all 65,536 anti-periodic binary layers, the exact computation gives:

    every node has exactly ONE period-32 child
    through spatial lift depth 1000.

Moreover the 65,536 children at each tested depth are all distinct, so there are no mergers between canonical chains through depth 1000.

This is a finite theorem through the stated depth only; it is not yet an all-depth uniqueness theorem.

## 3. Exit-node scan

A candidate K=3 exit node must satisfy:

1. temporal prefix 2221;
2. exact backward resetting exit phase
       gamma = 1[b_ell=1].

Within lift depths 0 through 928 of the 65,536 canonical chains, exactly

    118,359

nodes satisfy those two conditions.

The first such nodes occur at lift depth 7. Thus the p=16 local prefix-inversion bound "at least four lifts below the doubling layer" strengthens empirically at p=32 to at least seven lifts on this exact canonical language.

## 4. Source-to-source test

Because the chains are unique through depth 1000, every exit node through depth 928 has its complete shadow descendants available for a +64 physical source horizon.

If c_m denotes the temporal code at spatial lift depth m, then for an exit at chain depth d:

- the complete driver at physical offset n is shift^n(c_(d+n));
- the shadow right pair is read from the low bits of c_(d+n+1) and c_(d+n+2) at temporal phase n.

The checker then applies exactly the same pushed cyclic/one-bit/repair source automaton used in the period-16 elimination.

Result:

    tested exit nodes: 118,359
    surviving nodes:  0
    latest contradiction offset: +34.

Failure histogram:

    4:22112
    6:53236
    8:22741
    10:11198
    12:5089
    14:2149
    16:1028
    18:435
    20:203
    22:92
    24:38
    26:19
    28:12
    30:5
    34:2.

So there is no period-32 K=3 exit lying within the first 928 period-preserving lifts below its canonical doubling layer.

## 5. What this does and does not prove

This is strong evidence that the p=16 contradiction is inherited at the next dyadic scale, but it is NOT an all-depth p=32 theorem. A hypothetical finite p=32 exit could lie deeper than 928 lifts below the canonical layer.

The computation does establish a much smaller proof target than raw p=32 enumeration:

> prove all-depth uniqueness/nonmerger of the canonical period-32 lift chains, and prove that every 2221/backward-phase exit node on such a chain violates the source automaton within a uniformly bounded number of later lifts.

The observed bound is +34 through depth 928.

Do not extend the raw depth cap merely for a larger number. The next useful theorem should explain either:

1. why the unique canonical lift chain cannot acquire a phase fork/doubling while it remains period 32; and
2. why the source contradiction is forced from a finite chain-local invariant.

Checker:
`experiments/problem1_nonperiodicity/check_k3_period32_canonical_chain_probe.cpp`.

Atomic result:
`results/problem1/20260929_k3_period32_canonical_chain_probe.json`.

Dependencies: `problem1_period16_doubling_layer_reduction.md`;
`problem1_k3_period16_exit_elimination.md`;
`problem1_one_bit_extension_cycle_lifting_theorem.md`;
`problem1_full_driver_exit_phase.md`;
`problem1_three_bit_exit_repair.md`;
`problem1_shadow_gate_birth_phase.md`.
