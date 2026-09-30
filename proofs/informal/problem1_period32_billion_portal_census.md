# Problem 1: billion-depth census of the sixteen genuine period-32 portals

Status: exact finite-exhaustive census through lift depth 1,000,000,000 for all sixteen genuine portal connectors. Two first zero returns are found and both portal components are singleton terminal leaves. Problem 1 remains OPEN.

## Result

The sixteen genuine period-32 portals are indexed by the sixteen odd exact-period-16 leaves listed in `problem1_p16_zero_return_graph_complete.md`.

Each portal was advanced by the exact recurrent one-bit child map until either

1. the first zero low temporal plane occurred, or
2. lift depth 1,000,000,000 was reached.

Exactly two portals return before the cap.

### Portal 5

Period-16 parent leaf:

    0000100100100101

First zero low-plane depth:

    105,696,243

Returned high plane:

    00000000001001100000010001101101

This word is already its lexicographically minimal rotation. It has

    weight = 9,
    XOR parity = 1,
    exact rotational period = 32.

Hence it is an odd full-period terminal leaf and has no period-32 child.

Therefore

    B(0000100100100101) = 0.

### Portal 13

Period-16 parent leaf:

    0001001111001111

First zero low-plane depth:

    65,154,360

Returned high-plane necklace:

    00000001001101101001100111100001

with

    weight = 13,
    XOR parity = 1,
    exact rotational period = 32.

This is likewise a terminal full-period leaf, so

    B(0001001111001111) = 0.

## Remaining fourteen portals

No zero low plane occurs through lift depth 1,000,000,000 on portal indices

    0,1,2,3,4,6,7,8,9,10,11,12,14,15.

This is a lower bound only. The finite fixed-period return theorem still guarantees that every one of these connectors eventually reaches a zero low plane.

## Structural consequence

The period-32 root-basin decomposition is now partly exact rather than purely hypothetical.

Of the sixteen p16 leaves that become p32 portals:

- two portal components are completely classified;
- both are singleton odd leaves;
- fourteen portal components remain unresolved beyond depth 10^9.

Thus the p16 -> p32 leaf recurrence already has two known contributions

    B(l)=0,

so those two old leaves each contribute exactly one p32 terminating leaf.

This also demonstrates that enormous connector length does not imply a nontrivial full-period subtree: portal 5 runs for more than 10^8 deterministic lifts and portal 13 for more than 6.5*10^7, yet each returns directly to an odd leaf.

## Reproduction

Checker:

`experiments/problem1_nonperiodicity/check_period32_portal_zero_returns.cpp`.

Run a single portal with

    ./check_period32_portal_zero_returns PORTAL_INDEX CAP

or reproduce the billion-depth census by running all indices 0..15 with cap 1000000000.

Atomic record:

`results/problem1/20260929_period32_billion_portal_census.json`.

Dependency:
`problem1_period32_deep_portal_return_and_source_horizon_counterexamples.md`.
