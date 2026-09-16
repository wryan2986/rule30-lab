# Problem 1: exact adjacent-pair derivative dynamics

## Status

Problem 1 remains open. This note follows the run-54 observation that pairwise temporal XOR, after a suitable phase choice, maps the known terminating necklaces at lengths 4 and 8 to the known necklaces at lengths 2 and 4.

The main result here is an exact adjacent-pair decomposition of the reconstruction recurrence. It shows precisely why the pair derivative alone does not form an obvious Rule-30 semiconjugacy and identifies the missing auxiliary word.

## Setup

For a cyclic temporal column `q_i` of length `2p`, split adjacent time samples into two length-`p` words

    r_i(j) = q_i(2j),
    s_i(j) = q_i(2j+1),

with `j` cyclic modulo `p`. Let `T` denote cyclic shift on the `j` index, with the convention induced by `S q(t)=q(t+1)`. Then

    pair(S q_i) = (s_i, T r_i).

The exact reconstruction recurrence

    q_(i+2) = S q_i xor (q_(i+1) OR q_i)

therefore becomes

    r_(i+2) = s_i xor (r_(i+1) OR r_i),
    s_(i+2) = T r_i xor (s_(i+1) OR s_i).            (1)

This is an exact period-halved description: a length-`2p` column is represented by two length-`p` words.

## Pair derivative and the missing auxiliary word

Define

    d_i = r_i xor s_i.

Then `s_i = r_i xor d_i`, so (1) gives the closed exact system

    r_(i+2)
      = r_i xor d_i xor (r_(i+1) OR r_i),             (2)

    d_(i+2)
      = r_(i+2)
        xor T r_i
        xor ((r_(i+1) xor d_(i+1)) OR (r_i xor d_i)). (3)

Thus `(r_i,d_i)` is an exact period-halved coordinate system for the original recurrence. The derivative `d_i` alone is not closed: its next value depends explicitly on the even-sample auxiliary word `r_i` (and `r_(i+1)`).

For the doubling-parent initial condition `q_0=0, q_1=c`, one has

    r_0=d_0=0,
    r_1=even(c),
    d_1=Delta_2(c).

So the candidate lower-period necklace `Delta_2(c)` is accompanied by a definite auxiliary initial word `even(c)`.

## Direct semiconjugacy is not an identity

If `Delta_2` were an exact semiconjugacy to the same reconstruction rule, one would require

    d_(i+2) = T d_i xor (d_(i+1) OR d_i)              (4)

for all states. Equations (2)-(3) show extra `r` terms, and a one-bit local counterexample already disproves (4) as an algebraic identity: take a spatial recurrence state with constant-in-`j` pair words

    r_i=1, d_i=0, r_(i+1)=0, d_(i+1)=0.

Then `s_i=1`, `s_(i+1)=0`. From (1),

    r_(i+2)=1 xor (0 OR 1)=0,
    s_(i+2)=1 xor (0 OR 1)=0,

so `d_(i+2)=0`; this particular state is neutral. But changing only `d_(i+1)=1` gives `s_(i+1)=1`, hence

    r_(i+2)=0,
    s_(i+2)=1 xor (1 OR 1)=0,

again `d_(i+2)=0`, whereas (4) predicts `1` from `d_i=0,d_(i+1)=1`. Therefore the same-rule derivative recurrence fails even locally.

This does not disprove the weaker run-54 conjecture restricted to *terminating doubling-parent trajectories*. It does rule out proving it by a global operator identity `Delta_2 R = R Delta_2`.

## What termination gives exactly

If the original length-`2p` reconstruction terminates, then for some spatial index `N`,

    q_N=q_(N+1)=0.

Equivalently,

    r_N=d_N=r_(N+1)=d_(N+1)=0.

So the exact halved system (2)-(3) reaches the zero state. The unresolved issue is whether its derivative component `d`, started from `d_0=0,d_1=Delta_2(c)`, must independently follow a terminating trajectory of the *ordinary* length-`p` reconstruction. The auxiliary `r` is the only obstruction in the exact equations.

## Sharpened next target

Do not search for a bare `Delta_2` semiconjugacy; it is false as an operator identity. Instead, search for an invariant relation on the special terminating basin that eliminates `r` from (3), or for a correction `e = d xor Phi(r,T r,...)` whose evolution obeys the ordinary length-`p` recurrence.

A computationally useful formulation is to classify the basin of `(r,d)=(0,0)` under (2)-(3), starting from `(r_0,d_0)=(0,0)` and `(r_1,d_1)=(even(c),Delta_2(c))`. This works with length-`p` words and may expose a constrained relation between `r` and `d` on terminating trajectories without enumerating all `2^(2p)` initial words blindly.
