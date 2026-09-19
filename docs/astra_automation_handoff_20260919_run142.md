# Astra automation handoff — 2026-09-19 run 142

## Starting state

Started from `research/astra-next` at `3d345b800a44190708aeeb49099159338c10a850`, immediately after run 141. No intervening research work was found.

Problem 1 remains OPEN.

## New exact transport relation

Run 141 established the distinguished cyclic-source motif

    (hat r_-5,...,hat r_2)(q)=10101110,

with `q=t+2`. Write

    a=hat r_3(q), b=hat r_4(q), c=hat r_5(q), d=hat r_6(q).

Exact Rule-30 cone evolution gives at the intermediate `u` source

    hat r_1(q+2)=1 XOR a,
    hat r_2(q+2)=1,
    hat r_3(q+2)=a OR ((NOT b) AND (NOT c)),

with `hat r_4(q+2)` still depending on `a,b,c,d`.

The important new collapse appears two steps later:

    hat r_1(q+4)=a,
    hat r_2(q+4)=a OR b.

Thus at the forced resetting one-bit `t` source `q+4=t+6`, the shadow right pair depends only on the first two wider driver bits at the distinguished source, not on the rest of the fringe.

The zero-pair flag there is exactly

    (NOT a) AND (NOT b).

So the `t -> u -> t` passage has a genuine two-bit finite-state quotient for this flag, even though the unrestricted wider driver does not close.

Full note: `proofs/informal/problem1_distinguished_source_four_step_right_pair_transport.md`.

Research commit: `7c25977b2e6a06ee93b1e2489fe7027827210718`.

## Stopping fence

This does not yet bound births. The resetting one-bit source at `q+4` may still reuse either flag value indefinitely unless its resetting phase/gate identities impose a further restriction. Do not claim a driver recurrence for the entire right fringe from this pair identity.

## Best next target

Combine the exact pair

    (hat r_1,hat r_2)(q+4)=(a,a OR b)

with the existing resetting one-bit `t` source phase/gate laws. Determine whether its subsequent return/birth indicator is a function of this pair alone, or whether farther driver bits re-enter. If it closes, iterate the resulting small transition system across complete episodes; if farther bits re-enter, record the minimal obstruction rather than expanding an arbitrary driver prefix.

Problem 1 remains OPEN.
