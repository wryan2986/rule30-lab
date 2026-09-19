# Astra automation handoff — 2026-09-19 — run 131

Problem 1 remains OPEN.

Starting branch tip was `5be529097cf3e505499fa42989ce1b1fd6eb1a32`; no intervening work was present after run130.

## New result

At the cyclic `t` source `q=t+2` in the forced-birth sensitive route, run130 proved `r_-2(q)=0` and isolated the fork bit `a=r_-1(q)`, giving local block `0 a 1`.

Let `p=r_-3(q)`. Direct Rule-30 evaluation gives

    r_-2(q+1) = f(p,0,a) = p XOR a,

hence

    a = r_-3(q) XOR r_-2(q+1).

So the source-relative `001/011` fork bit is exactly a local transport/flip indicator along the farther-left staircase: `a=0` transports the bit unchanged, while `a=1` flips it.

This is useful because it converts the exceptional `011` branch from an arbitrary creation event into an algebraic discrepancy that may telescope across episodes. It does not yet give a finite budget: the relevant staircase can drift left through infinitely many spacetime coordinates, so finite initial support only helps if successive source episodes align these XOR identities into a single chain with controlled boundary values.

## Next target

Compute the exact source-to-source spacetime displacement for successive relevant cyclic `t` sources and test whether

    r_-3(q) XOR r_-2(q+1)

from one episode shares an endpoint with the analogous expression from the next. If these terms telescope, derive the resulting boundary invariant and test whether finite support bounds the number/parity of `011` branches. If they do not align, record the geometric obstruction rather than returning to generic ancestry arguments.

New proof note: `proofs/informal/problem1_source_fork_bit_exact_update_identity.md`.
