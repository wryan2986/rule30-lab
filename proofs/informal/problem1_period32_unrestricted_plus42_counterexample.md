# Problem 1: the +42 source horizon is not universal at period 32

Status: exact counterexample to a tempting local strengthening. Problem 1 remains OPEN.

## 1. Motivation

The finite-domain period-32 portal audit in
`problem1_finite_lift_zero_return_existence.md` found more than ten million
genuine finite-portal exit occurrences, all failing the pushed FULL source
automaton by physical offset +42 or earlier.

That suggested the possible stronger statement:

> every exact-period-32 `2221` exit satisfying the backward exit phase
> fails the source automaton by +42, independent of finite ancestry.

This statement is false.

## 2. Exact abstract driver

Consider the purely period-32 temporal driver

    22211221323333032110021130122112.                 (1)

It has exact least period 32. Its last reset before phase zero is the symbol
1 at phase -2; the intervening suffix contains one symbol 2, so

    gamma=1=1[b_ell=1].

Thus (1) satisfies exactly the pushed backward exit-phase condition as well
as the forced K=3 prefix `2221`.

The nested recurrent shadow lifts needed through the source calculation are
unique; no same-period fork or doubling occurs in the checked window.

## 3. Exact source history

Starting from the one-bit exit at physical offset 0, the pushed source laws
give the following source sequence. Only the leading driver symbols needed
for identification are displayed.

    n=0   one  222112...  exit -> one
    n=6   one  221130...  u,h=1 -> cyclic
    n=8   cyc  322001...  birth -> one
    n=10  one  211120...  t -> one
    n=12  one  222113...  exit -> cyclic
    n=18  cyc  322130...  birth -> one
    n=20  one  212002...  t -> one
    n=22  one  211130...  t -> one
    n=24  one  222001...  u,h=1 -> cyclic
    n=26  cyc  311121...  no birth
    n=28  cyc  322121...  birth -> one
    n=30  one  212121...  t -> one
    n=32  one  212122...  t -> one
    n=34  one  212133...  t -> one
    n=36  one  212011...  t -> one
    n=38  one  211220...  t -> one
    n=40  one  221332...  u,h=1 -> cyclic
    n=42  cyc  320130...  birth -> one
    n=44  one  232003...  FAIL

The first contradiction is therefore at

    +44,                                                   (2)

where the required one-bit source has driver prefix `23` instead of
`21` or `22`.

A five-million-word deterministic random campaign over unrestricted
period-32 suffixes found this word as the unique sample reaching +44 in that
campaign; no sampled driver survived the +64 horizon. That campaign is only
context. Equation (2) is an exact certificate for the single word (1).

## 4. Projection ancestry

The exact spatial projection of a temporal code with low/high planes
`(a,b)` is

    (a,b) -> (b, R(a) XOR (b OR a)),

where `R(a)_s=a_(s+1)`.

Iterating this map on (1) for one billion projections does not reach zero
and does not drop to temporal period 16.

This does NOT prove that (1) is non-finite: a finite period-32 state can have
an extremely large bitlength, and the finite-domain theorem gives only the
coarse all-depth bound `4^32`. It does prove that the counterexample is not
one of the shallow finite portal descendants covered by the ten-million-lift
audit.

## 5. Research consequence

Do not attempt to prove a period-32 source contradiction using only:

- exact period 32,
- prefix `2221`,
- the backward exit phase, and
- the local nested shadow recurrence,

with a universal horizon +42. The statement is false on that unrestricted
domain.

The missing ingredient must use finite ancestry/root-basin information.
The current productive target is therefore a finite-portal invariant that
separates the sixteen genuine period-32 portal trees from abstract periodic
2-adic drivers such as (1).

Checker:
`experiments/problem1_nonperiodicity/check_period32_unrestricted_plus44.cpp`.

Dependency: `problem1_finite_lift_zero_return_existence.md`.
