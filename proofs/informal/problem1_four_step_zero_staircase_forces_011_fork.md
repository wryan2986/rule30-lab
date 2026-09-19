# Four-step zero-staircase recurrence forces the 011 fork

Status: `partial-proof` / exact local lemma. Problem 1 remains OPEN.

## Setup

Continue `problem1_source_fork_bit_exact_update_identity.md`. At a relevant cyclic source time `q`, the earlier source-relative argument gives

    r_-2(q)=0,
    a := r_-1(q),
    r_0(q)=1,

and FULL gives the center word

    r_0(q..q+4) = 1,0,1,0,1.

The run131 identity was

    a = r_-3(q) XOR r_-2(q+1).

The question was whether analogous source episodes can align into a telescoping staircase.

## New exact local lemma

Assume, in addition, that the cell four times later on the same relative diagonal satisfies

    r_-2(q+4)=0.

Then necessarily

    r_-1(q)=1.

Equivalently, under the FULL center word and zero endpoints

    r_-2(q)=r_-2(q+4)=0,

the sensitive-one provenance fork at `q` is forced to be the exceptional `011` branch; the `001` continuation is impossible.

This is an exact finite-cone statement, independent of any finite-support assumption.

## Exhaustive exact check

The union of backward cones needed for the five center bits through `q+4` and `r_-2(q+4)` is contained in the nine cells `r_-6(q),...,r_2(q)`. Exhausting all `2^9=512` assignments gives exactly six assignments satisfying

    center(q..q+4) = 10101,
    r_-2(q)=0,
    r_-2(q+4)=0.

Written in order `r_-6(q)...r_2(q)`, they are

    000101101
    000101110
    000101111
    010101101
    010101110
    010101111

and all six have `r_-1(q)=1`. The value `r_-1(q+4)` is not fixed: it is 0 in the first three and 1 in the last three.

The census is small enough to audit directly by repeated application of

    f(l,c,r) = l XOR (c OR r).

## Consequence for the proposed telescoping route

This is stronger than a failure of endpoint alignment. If successive relevant source episodes ever supply the same `r_-2=0` condition four steps apart, then the earlier fork cannot be `001` at all: it is forced to terminate at `011`.

So a four-step chain of source-relative zero conditions does not make the run131 XOR discrepancies telescope into a freely varying parity budget. Instead it rigidifies the earlier discrepancy to 1.

This does **not** yet close Problem 1. The existing forced-birth passage has cyclic sources at `t+2` and `t+4`, followed by the forced new one-bit row at `t+6`; the repository has not proved that `r_-2=0` holds again at `q+4=t+6` in the exact sense required by this lemma. Applying the lemma globally therefore requires a new bridge showing that the zero-staircase endpoint recurs at the forced birth or at another uniformly spaced family of relevant sources.

## Next target

Check the complete forced-birth identities at `t+6` and determine whether they imply `r_-2(t+6)=0`. If yes, the lemma forces every preceding `q=t+2` fork to be `011`, converting the sensitive-provenance ambiguity into a deterministic exceptional event. If not, record the exact value/freedom of `r_-2(t+6)` and abandon this four-step recurrence route rather than assuming source labels transfer the zero condition.

Dependencies: `problem1_source_fork_bit_exact_update_identity.md`, `problem1_forced_birth_sensitive_route_previous_source_dichotomy.md`, Rule 30 local rule.