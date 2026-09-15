# Problem 1: no-reset seed inherits the exact temporal period

## Statement

Consider a finite periodic `A`-orbit of exact period `p`, written as spacetime columns `c_i(t)` with time modulo `p`, satisfying

`c_{i+2}(t) = c_i(t+1) XOR (c_{i+1}(t) OR c_i(t))`.

Assume the no-reset condition `c_0(t)=0` for every `t`. Then the seed column

`a(t) := c_1(t) = c_2(t)`

has minimal temporal period exactly `p`.

This closes the first sublemma left open in run 39.

## Proof

Because `c_0=0`, the coordinate-zero recurrence gives

`c_2(t)=c_1(t)`

for every `t`; hence `c_1=c_2=a`.

Suppose, toward a contradiction, that `a` has a smaller temporal period `q<p`, with `q | p`.

We show inductively that every column `c_i` is `q`-periodic in time.

The base columns are immediate:

- `c_0=0` is `q`-periodic;
- `c_1=a` is `q`-periodic;
- `c_2=a` is `q`-periodic.

Now assume `c_i` and `c_{i+1}` are `q`-periodic. The recurrence

`c_{i+2}(t) = c_i(t+1) XOR (c_{i+1}(t) OR c_i(t))`

uses only a one-step cyclic time shift and pointwise Boolean operations. Both preserve `q`-periodicity. Therefore `c_{i+2}` is also `q`-periodic.

By induction every spatial column of the finite state is `q`-periodic. Consequently the entire state row satisfies

`x(t+q)=x(t)`

for all `t`, contradicting that the `A`-orbit has exact period `p`.

Therefore `a` cannot have any proper temporal period and must have minimal period exactly `p`. QED.

## Consequence for the run-38/39 lifting obstruction

The qualification by primitivity found computationally in run 39 is automatic for genuine finite exact-period no-reset cycles. Thus the remaining parity obstruction can now be stated without an extra dynamical sublemma:

> If a primitive periodic binary seed `a` generates, under the column recurrence, a finite terminating cylinder with top boundary `...,0,1,1,0`, prove that `XOR_t a(t)=1`.

The even-parity terminating examples at declared nonminimal periods (such as the period-4 representations of period-2 seeds) cannot arise from a genuine exact-period-4 no-reset orbit, because the argument above forces the whole cylinder to inherit their smaller seed period.

## Why this matters

Combined with the one-bit extension theorem from run 38, an odd-parity theorem for primitive terminating seeds would rule out the only branch that splits one parent cycle into two child cycles. Inductively this would establish the observed uniqueness of the finite periodic orbit at each bitlength and force its exact period to change only by doubling.