# Problem 1: local pair-derivative correction no-go

## Status

Problem 1 remains open. This note continues `problem1_pair_derivative_exact_dynamics.md` by testing the most direct way to eliminate the auxiliary even-sample word `r` on the special terminating basin.

## Setup

For a length-`2p` reconstruction column `q_i`, write

    r_i(j)=q_i(2j),
    s_i(j)=q_i(2j+1),
    d_i=r_i xor s_i.

Run 55 derived the exact halved system and showed that `d` alone does not obey the ordinary length-`p` reconstruction globally. A remaining possibility was that, on the special terminating trajectories, a corrected derivative

    e_i = d_i xor Phi(r_i, T r_i, ...)

might obey

    e_(i+2) = T e_i xor (e_(i+1) OR e_i).             (R)

If so, termination at length `2p` could descend to ordinary termination at length `p`.

## Exhaustive local-correction test on the known p=8 terminating trajectory

Take the known length-8 terminating necklace representative

    c = 10000110

(with the phase convention used by the reconstruction code). Its reconstruction reaches two consecutive zero columns after 400 spatial steps (402 stored columns including `q_0,q_1`). Pairing adjacent times gives length-4 words `(r_i,d_i)` along the entire trajectory.

I exhaustively tested every translation-equivariant pointwise Boolean correction of each of these forms:

    e_i(j) = d_i(j) xor phi(r_i(j)),

    e_i(j) = d_i(j) xor phi(r_i(j), r_i(j+1)),

    e_i(j) = d_i(j) xor phi(r_i(j), r_i(j+1), r_i(j+2)).

There are respectively `4`, `16`, and `256` Boolean functions `phi`; every function was tested against (R) at every spatial index of the terminating trajectory.

Result:

    radius / input width       functions tested       functions satisfying (R)
    1 bit                       4                       0
    2 consecutive bits          16                      0
    3 consecutive bits          256                     0

Thus even on the special terminating basin, the auxiliary `r` cannot be removed by any static local correction of `d` depending on up to three consecutive bits of the current `r_i`.

As an additional sanity check, the uncorrected `d` sequence fails (R) at 376 of the 400 testable spatial transitions on this length-8 trajectory. The agreement of `Delta_2(c_8)` with the lower terminating necklace is therefore an initial-word phenomenon, not evidence that the subsequent derivative trajectory shadows the lower reconstruction.

## Interpretation

This is a useful negative result. The run-54 observation

    Delta_2(c_8) ~ c_4

still holds, but it is not explained by a simple local conjugacy or by a short-range static gauge correction to the derivative. Any genuine period-halving theorem must use more structure: for example a relation involving both consecutive spatial states `(r_i,r_(i+1))`, a nonlocal functional of `r`, or a direct characterization of which initial words lie in the zero basin without requiring trajectory-by-trajectory semiconjugacy.

The last option now looks preferable. The desired implication is only

    c terminating at length 2p  =>  Delta_2(c) terminating at length p,

not equality of the two reconstructed trajectories. Requiring a corrected derivative to obey (R) at every intermediate spatial column appears substantially stronger than necessary.

## Next target

Stop expanding static local corrections `Phi(r_i,...)` unless a structural identity suggests one. Instead attack the zero-basin implication at the level of initial words. Two concrete directions are:

1. Reverse the exact recurrence from the terminal pair `(0,0)` and characterize predecessor constraints in the halved `(r,d)` coordinates, asking what they force on the initial derivative `d_1=Delta_2(c)`.
2. Build a memoized reverse-basin classifier for length `p` and use it to test the length-16 case without following every forward trajectory independently.

The computational no-go here does not disprove the unique-necklace or period-halving conjectures; it rules out a broad, natural class of simple proofs of them.
