# Greatest signature simulation and its concrete lifting obstruction

Status: exact greatest-fixed-point calculation for the configured finite
signature graph, plus a small exact counterexample showing that signature-level
simulation does not lift to a same-cylinder adjacent frontier shadow.

## 1. The twelve-signature graph

For phase `a` and exact complexity `k`, every ordinary frontier state has the
parent/fiber signature

\[
\sigma(q)=(P_{a,k}(q),M_{a,k}(q)).
\]

The exact parent algebra gives twelve possible signatures. A concrete lift
`4q+d` induces a labelled edge

\[
\sigma(q)\xrightarrow{d}\sigma(4q+d).
\]

Because several concrete states can share one signature, this quotient graph is
nondeterministic.

## 2. Set-valued shadow states

Let `S` be the finite signature set. A shadow belief is a nonempty subset
`B subset S`. For digit `d`, define

\[
\operatorname{Post}_d(B)
 =\bigcup_{b\in B}\operatorname{Post}_d(b).
\]

Define an operator on relations `R subset S x (2^S minus {empty})` by retaining
`(s,B)` exactly when, for every digit `d` and every
`s' in Post_d(s)`,

\[
(s',\operatorname{Post}_d(B))\in R.
\]

If `Post_d(s)` is nonempty, the shadow update must also be nonempty. The
greatest fixed point `nu R` is the greatest same-digit set-valued simulation on
the finite quotient graph.

This construction is exact for any finite labelled graph.

## 3. Finite fixed point

For the 12-signature graph there are

\[
12(2^{12}-1)=49,140
\]

candidate current/belief pairs. On the graph exhausted through phase
complexity 25, pruning reaches its fixed point after three rounds:

```text
removed by round: 147, 464, 1,136
surviving pairs:   47,393
singleton simulations: 54
```

The singleton signature

```text
1111/1111
```

simulates all twelve source signatures in this quotient graph. Thus the
set-valued construction does not contract to a useful small obstruction; it is
nearly universal already at singleton width.

## 4. Why this does not prove a frontier shadow

The quotient graph forgets two indispensable facts:

1. the exact base-four residue required by the survivor cylinder;
2. whether a sequence of abstract edges can be realized by one consistent
   concrete frontier state.

A small exact example already separates abstract simulation from concrete
cylinder lifting.

In phase `p`, complexity two contains

\[
x=12,
\qquad
\sigma(x)=0010/1100.
\]

The greatest signature simulation accepts the abstract singleton shadow
`1111/1111`. But the depth-one cylinder is

\[
x\equiv0\pmod4.
\]

The preceding frontier is

\[
O_{p,1}=\{3\},
\]

and `3` is congruent to `3 mod 4`, not `0 mod 4`. Therefore

\[
\{y\in O_{p,1}:y\equiv x\pmod4\}=\varnothing.
\]

There is no adjacent same-cylinder shadow at all, despite the abstract
signature simulation.

Hence

\[
\boxed{
\text{signature simulation does not imply concrete cylinder simulation.}
}
\]

## 5. Concrete transition profiles

For one concrete state, its one-step profile records its source signature and
the unique target signature, if any, for each digit. These profiles retain
realization consistency for one step, unlike the aggregated signature graph.

The independent complexity-25 campaign finds:

```text
phase p distinct profiles: 448
phase u distinct profiles: 441
```

For phase `p`, the number appearing at a single complexity continues to grow:

```text
k=20: 373
k=21: 406
k=22: 413
k=23: 431
k=24: 437
```

This is finite evidence that the missing realization state is substantially
larger than the twelve-signature quotient. It is not an all-depth unboundedness
proof.

## 6. Validation

The Python reference analyzer computes the graph, the complete powerset fixed
point, singleton preorder, concrete lifting counterexample, and transition
profiles through a controlled complexity cap. Seven focused tests cover the
main identities and certificate.

```text
Python K=16 certificate:
b50a4a16bf21ad6d39ce71a4658722b63efc9bca574a93a5a73ac9377153896a

Python K=20 certificate:
4545d8c5d4c84d753d4a6081addabfaee1bc331c71153627aea488b1834cb1df
```

The independent C++ campaign through complexity 25 checks 16,864,712 outputs
and reports:

```text
signature edges per phase: 194
candidate simulation pairs: 49,140
greatest fixed-point pairs: 47,393
removed rounds: 147,464,1136
singleton simulations: 54
universal singleton coverage: 12 of 12
output SHA256:
77cfcec455fa367363e81b31d9a6c6c259dd3a73e3e8439bae10d27b5e8ea236
runtime: about 29.35 seconds
peak RSS: about 109,920 KiB
```

## 7. Scientific boundary

The fixed-point theorem is exact for a supplied finite graph, and the concrete
lifting counterexample is exact. The 194-edge stabilization and profile counts
are finite observations.

This result does not prove that no richer finite concrete abstraction exists.
It does not prove the all-depth adjacent-shadow inclusion, phase-complexity
divergence, exclusion of eventual center period two, or Rule 30 center
nonperiodicity.

The next target is residue-aware concrete simulation: states must retain enough
information to guarantee both a common cylinder and a consistent realization,
rather than combining existential edges from unrelated frontier states.
