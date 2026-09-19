# Problem 1: the transported right pair does not close the full resetting-source state

## Context

Run 142 established the exact four-step transport from a distinguished two-bit-return source `q` with

`(r[-5],...,r[2])(q) = 10101110`.

Writing

- `a = r[3](q)`,
- `b = r[4](q)`,

it proved

`r[1](q+4) = a`,
`r[2](q+4) = a OR b`.

Thus the pair at the forced resetting one-bit `t` source is determined by `(a,b)`. The next question was whether this gives an autonomous small state across complete episodes.

## New stopping-fence result

The transported pair does **not** determine even the next right cell of the resetting source. Farther fringe information re-enters immediately at `r[3](q+4)`.

Take the distinguished source motif through position 2 and choose

`a=r[3](q)=0`, `b=r[4](q)=0`, `c=r[5](q)=0`.

Compare two source rows which agree on every cell through position 5 but differ at

`d=r[6](q)`.

Exact Rule-30 evolution for four steps gives:

- if `d=0`, then `(r[0],r[1],r[2],r[3],r[4])(q+4) = 10011`;
- if `d=1`, then `(r[0],r[1],r[2],r[3],r[4])(q+4) = 10000`.

In both cases the run-142 transported pair is the same:

`(r[1],r[2])(q+4) = 00`,

but `r[3](q+4)` differs.

Therefore no autonomous transition rule for the complete resetting-source right state can be based on the run-142 pair alone.

## Verification

This was checked by direct exact Rule-30 cone evolution using

`F(l,c,r) = l XOR (c OR r)`

from the fixed source block `10101110`. Exhaustion over `(a,b,c,d)` also reproduces the run-142 formulas for positions 1 and 2 while showing the dependence of farther cells on farther source bits.

## What this does and does not rule out

This does **not** show that the subsequent return/birth indicator depends on farther fringe bits. The phase/gate laws may quotient away the difference at `r[3]` and make that indicator a function of the transported pair anyway.

It does rule out the stronger and tempting claim that the pair `(r[1],r[2])` is itself a closed state for the resetting source. Any successful finite-state episode model must either:

1. prove that the gate/return observable ignores the nonclosed farther-right state, or
2. enlarge the state enough to include precisely the farther information that can affect that observable.

The next useful calculation is therefore not another unrestricted right-fringe expansion. It is an exact dependency calculation for the **next return/birth indicator itself**, conditioned on each of the three reachable transported pair classes `00`, `01`, and `11`, to determine whether the phase/gate observable closes even though the full local state does not.
