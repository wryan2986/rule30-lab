# Astra automation handoff — run 52 — 2026-09-15

## New result

Continued run 51's protected-parent-trace elimination. For a finite exact-period-`p` parent cycle `u_s`, define temporal spatial columns

    q_i(s)=bit_i(u_s).

The accelerated Rule-30 recurrence gives the exact spatial reconstruction

    q_(i+2)(s)=q_i(s+1) xor (q_(i+1)(s) OR q_i(s)).

Run 51's genuine-doubling criterion says `q_0=0` for the whole parent period and `q_1` has odd XOR parity. Therefore the entire parent spacetime cycle is determined by the single protected temporal word `c=q_1`:

    q_0=0,
    q_1=c,
    q_2=c,
    q_3=S(c) xor c,
    ...

A finite eligible doubling parent is therefore exactly an odd-parity cyclic word `c` (of exact temporal period `p`) whose induced column recursion eventually reaches two consecutive zero columns.

This is recorded in `proofs/informal/problem1_doubling_parent_temporal_word_reconstruction.md`.

## Why it matters

The doubling certificate has now been reduced from the contaminated low fiber, then from two protected parent traces, to one protected temporal column. For genuine common-origin projections that column is literal original spacetime data.

The local question is now a finite combinatorial termination/classification problem on odd cyclic words. This may either produce a rigid classification useful globally or demonstrate that local parent combinatorics is too permissive.

## Sanity check

Enumeration below `2^16` found zero-low-bit cycles `0`, `6`, and `(200,222)`; only the latter two have odd `q_1` parity and satisfy the run-51 doubling criterion. This is not used as proof.

## Next target

Analyze the word recursion

    q_(i+2)=S q_i xor (q_(i+1) OR q_i),
    q_0=0, q_1=c

for odd-parity words of dyadic length. Seek either:

1. classification of terminating words, especially a recursive relation between period `p` and `2p`; or
2. a constructive large family proving that termination alone is not restrictive enough.

Problem 1 remains open.