# Problem 1: terminal normal form for terminating temporal-word reconstruction

## Status

Problem 1 remains open. This note follows the run-56 recommendation to attack the zero basin directly rather than continue searching for local pair-derivative gauges.

## Setup

Let `q_i` be cyclic binary words of temporal length `p`, with reconstruction

    q_(i+2) = S q_i xor (q_(i+1) OR q_i),

where `S` is cyclic temporal shift. Suppose a nonzero reconstruction terminates, and let `N` be the *first* index for which

    q_N = q_(N+1) = 0.

Thus `q_(N-1) != 0`.

## Exact terminal normal form

The last columns before the first zero pair are forced.

From the recurrence at index `N-1`,

    0 = q_(N+1)
      = S q_(N-1) xor (q_N OR q_(N-1))
      = S q_(N-1) xor q_(N-1).

Hence `q_(N-1)` is invariant under cyclic shift, so it is a constant word. Minimality excludes zero. Therefore

    q_(N-1) = 1^p.

At index `N-2`,

    0 = q_N
      = S q_(N-2) xor (1^p OR q_(N-2))
      = S q_(N-2) xor 1^p,

so

    q_(N-2) = 1^p.

At index `N-3`,

    1^p = q_(N-1)
        = S q_(N-3) xor (1^p OR q_(N-3))
        = S q_(N-3) xor 1^p,

hence

    q_(N-3) = 0.

Finally, at index `N-4` (when `N >= 4`),

    1^p = q_(N-2)
        = S q_(N-4) xor (0 OR q_(N-4))
        = S q_(N-4) xor q_(N-4).

Thus adjacent temporal bits of `q_(N-4)` differ everywhere. A cyclic binary word with this property exists iff `p` is even, and then it is one of the two alternating words.

Therefore every nontrivial terminating reconstruction whose first zero pair occurs at `N >= 4` has the universal terminal suffix

    ..., alt_p, 0, 1^p, 1^p, 0, 0,

where `alt_p` is `0101...` or `1010...` cyclically.

## Consequence: even temporal length is necessary

For `N >= 4`, termination forces `p` even. This is a proof, not a computational observation.

The exceptional very-short case matters: at `p=1`, the known reconstruction `0,1,1,0,0` terminates with `N=3`, so the `q_(N-4)` step does not exist. Thus the theorem is consistent with the length-1 base case.

## Check against the known p=8 terminating necklace

The complete known `p=8` trajectory ends with

    ..., 01010101, 11111111, 01010101, 00000000,
        11111111, 11111111, 00000000, 00000000.

Its final six columns agree exactly with the forced suffix above.

## Why this helps the period-halving route

This gives a rigid description of the *target* zero basin without requiring the pair derivative to obey the ordinary lower-period dynamics along the whole trajectory. In adjacent-pair temporal coordinates, the forced alternating predecessor `alt_(2p)` has pair XOR derivative `1^p` for either compatible pairing phase. Thus every terminating length-`2p` trajectory enters the halved `(r,d)` zero basin through a fixed small collection of terminal states.

This suggests a more economical reverse classifier: start from the universal suffix rather than from all `(r,d)` states, enumerate its predecessor layers, and quotient by cyclic rotation. The reverse map branches only where an OR input masks a predecessor bit, so this may be substantially smaller than forward enumeration of all odd initial words at `p=16`.

## Next target

Derive the predecessor relation one or two layers farther backward from

    alt_p, 0, 1^p, 1^p, 0, 0

and express the branching constraints in paired `(r,d)` coordinates. In particular, test whether every reverse path reaching a legal initial pair `(q_0,q_1)=(0,c)` forces the pair derivative of `c` into the lower-period terminating basin. That is exactly the weaker implication needed for period halving; no trajectory semiconjugacy is required.