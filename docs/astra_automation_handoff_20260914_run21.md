# Astra automation handoff — 2026-09-14 run 21

Branch: `research/astra-next`

## Repository state reviewed

Run started from `514adff83d03fdded8a3f365b6d60c920ad3bb1f` (run 20 handoff). No newer branch work was present.

The active question was whether the terminal commutator state `d_p` can be compressed from the full length-`p` source word to a bounded suffix for genuine return-fringe collision states.

## New result

Added:

`proofs/informal/problem1_commutator_automaton_three_bit_reduction_and_memory_obstruction.md`

commit `8d53c67ef5ce2f3b5830c935d749d3c77e8b0fcc`.

### Three-bit / three-state reduction

Writing the discrepancy as

\[
d=a+2b
\]

and the low source bits as `s_0=x`, `s_1=y`, `s_2=z`, the exact transition is

\[
\boxed{a'=(a\oplus x)\lor(b\oplus y)}
\]

and

\[
\boxed{b'=(b\oplus y)\land\neg z}.
\]

Consequences:

- the transition depends only on `s mod 8`, not `s mod 16`;
- state `2` is impossible after one transition;
- starting from `d_0=0`, the automaton lives on exactly the reachable state set `{0,1,3}`.

Equivalently, with `r=s mod 4`,

\[
F(d,s)=0\iff d=r.
\]

For a mismatch, `F=3` exactly when the high bits of `d` and `r` differ and `s_2=0`; all other mismatches give `F=1`.

### Orbit interpretation

Since

\[
T(u_j)=4u_{j+1}+r_j,
\]

`r_j` is exactly the two-bit remainder discarded by normalization, while source bit 2 is the parity of `u_{j+1}`. Thus the automaton compares its two-bit memory to the genuinely discarded low pair at each normalized step.

### Synchronization and obstruction

On reachable states:

- source symbol `6 mod 8` is a complete reset: every state maps to `1`;
- source symbol `0 mod 8` is the identity: `0->0`, `1->1`, `3->3`.

Therefore, after the last source-6 symbol, all earlier commutator history is irrelevant. But the abstract automaton cannot admit any universal bounded-suffix theorem, because an arbitrarily long common suffix of zero symbols preserves distinct prior states exactly.

This is a precise negative result for the run-20 target: bounded-suffix compression, if true for actual collision states, must use return-fringe/common-origin geometry. It cannot follow from automaton theory alone.

The zero source symbol has the concrete meaning

\[
T(u_j)\equiv0\pmod8\iff u_j\equiv0\pmod8,
\]

using triangular bijectivity of `T mod 8`. So the geometric question becomes whether genuine collision histories can contain arbitrarily long terminal blocks of normalized states divisible by 8.

## Best next target

Specialize the source words to genuine return-fringe boundary-collision states.

Two concrete alternatives:

1. Prove that long corridors force a synchronizing source symbol `6 mod 8` within a bounded distance of the end of the normalized `p`-orbit. Then `d_p` would depend only on a bounded suffix after that reset.
2. Construct genuine collision states with arbitrarily long terminal source-0 runs. Such a family would show that even collision geometry does not give bounded-suffix memory, closing off this route cleanly.

A weaker but still useful target is to bound terminal runs `u_j ≡ 0 (mod 8)` using FULL/global-front structure or the physical common-origin condition.

## Status

Problem 1 remains open. This run reduced the commutator automaton from four states / four source bits to three states / three source bits, found an exact synchronizing symbol, and proved an automaton-only obstruction to bounded-suffix compression.
