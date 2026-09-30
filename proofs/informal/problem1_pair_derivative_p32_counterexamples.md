# Problem 1: pair-XOR period halving fails on genuine period-32 terminal leaves

Status: exact counterexamples to the period-halving conjecture in `problem1_temporal_necklace_pair_derivative.md`. Problem 1 remains OPEN.

## Background

The earlier note observed that for the then-known terminating necklaces at periods 4 and 8, a suitable cyclic pairing boundary made

    Delta_2(c)_(j) = c_(2j) XOR c_(2j+1)

land, up to rotation, on the known terminating necklace at half the period.

It explicitly left open the conjectural implication

    terminating(c of length 2p)
        => terminating(Delta_2(c) of length p)

for one of the two cyclic pair boundaries.

The billion-depth period-32 portal census now supplies the first two genuine terminating period-32 necklaces beyond that old test range.

## Counterexample 1

The portal-5 terminal p32 necklace is

    c = 00000000001001100000010001101101.

Across all 32 cyclic phases, `Delta_2(c)` has only two rotation-inequivalent outputs:

    0000010011100001
    0000011100101101.

The complete p16 zero-return census proves that there are exactly sixteen terminating p16 necklaces. Neither word above belongs to that set.

Therefore no cyclic pair boundary makes `Delta_2(c)` terminating at period 16.

## Counterexample 2

The portal-13 terminal p32 necklace is

    c = 00000001001101101001100111100001.

Its two rotation-inequivalent pair-XOR outputs are

    0000000100011101
    0001001111110101.

Again neither is one of the sixteen exact terminating p16 necklaces.

## Conclusion

The implication

    terminating(c at period 2p)
        => some phase of Delta_2(c) terminates at period p

is false, already at

    32 -> 16.

Thus the pairwise-XOR pattern seen at periods 4 and 8 was a low-scale coincidence, not the missing dyadic semiconjugacy.

Do not use raw decimation or pairwise XOR as the period-halving map in the p32 portal program. The exact structural relation between a p16 leaf and the parity/type of its first p32 zero-return child remains open.

Reproducer:
`experiments/problem1_nonperiodicity/check_p32_pair_derivative_counterexamples.py`.

Dependency:
`problem1_p16_zero_return_graph_complete.md`;
`problem1_period32_billion_portal_census.md`.
