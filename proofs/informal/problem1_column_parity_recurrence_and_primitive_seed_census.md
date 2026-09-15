# Problem 1: column-parity recurrence and primitive-seed census

## Context

Run 38 reduced one-bit cycle lifting to the no-reset cylinder.  Write the periodic spacetime columns as `c_i(t)` with

`c_0=0`, `c_1=a`, `c_2=a`,

and

`c_{i+2}(t)=c_i(t+1) XOR (c_{i+1}(t) OR c_i(t))`.

The remaining desired lemma is that a finite terminating cylinder whose seed `a` has the full exact temporal period must have odd XOR parity.

## Exact parity recurrence

For a p-periodic binary column `v`, define

`P(v)=XOR_t v(t)`

and the mod-2 overlap

`<v,w>=XOR_t (v(t) AND w(t))`.

Using `x OR y = x XOR y XOR (x AND y)` and invariance of XOR parity under cyclic time shift,

```
P(c_{i+2})
 = P(c_i) XOR P(c_{i+1} OR c_i)
 = P(c_i) XOR P(c_{i+1}) XOR P(c_i) XOR <c_i,c_{i+1}>
 = P(c_{i+1}) XOR <c_i,c_{i+1}>.
```

Hence

`P_{i+2}=P_{i+1} XOR <c_i,c_{i+1}>`.                       (1)

This is an exact scalar consequence of the cylinder recursion.  In particular, parity propagation is controlled only by adjacent-column overlap parity; the shifted term cancels completely.

For a finite n-bit state the top boundary is `c_{n-1}=1` and `c_n=0`.  Back-substitution also forces `c_{n-2}=1` and `c_{n-3}=0`.  Thus every terminating cylinder reaches the universal column suffix

`..., 0, 1, 1, 0`.

Equation (1) is therefore a possible route for transporting a parity obstruction from `P(a)` to the universal top boundary, but by itself it is not closed because the overlap terms remain.

## Exhaustive primitive-seed census

I exhaustively generated cylinders directly from every nonzero p-periodic seed `a`, rejecting seeds whose minimal temporal period is a proper divisor of p.  A seed was called terminating if some generated column is all ones and the next column is all zeros, exactly the finite leading boundary.

Results:

- p=1: the unique primitive seed terminates and has odd parity.
- p=2: both primitive terminating seeds have odd parity; no primitive even-parity terminating seed.
- p=3: no primitive seed terminates in the tested range.
- p=4: four primitive seeds terminate; all have odd parity.
- p=5,6,7: no primitive seed terminates in the tested range.
- p=8: eight primitive seeds terminate, first at top-column index 399; all have odd parity.  Their masks are `13,26,52,67,104,134,161,208`, the eight cyclic phases of one seed.
- exhaustive searches through p=12 found no primitive even-parity terminating seed (with 500 generated columns per seed).

The p=8 result independently recovers the run-37 threshold: `c_0=0`, so a top-column index 399 corresponds to the parent word of bitlength 400 whose child at bitlength 401 doubles period.

## Important dead end / refinement

The stronger statement "every nonzero terminating periodic seed has odd parity" is false.  Even-parity terminating seeds exist when the supplied temporal period is nonminimal.  Examples include p=4 masks 5 and 10, which are repetitions of primitive period-2 sequences.  At p=8 there are likewise terminating even-parity seeds inherited from smaller periods.

So any proof must use **primitivity / exact temporal period**, not merely periodicity plus finite termination.  This is useful because the one-bit lifting theorem is applied to an exact-period parent cycle: under the no-reset hypothesis `c_1=a`, the seed inherits the parent cycle's exact temporal period unless the higher columns somehow carry the missing phase information.  Establishing that inheritance rigorously is now an explicit sublemma.

## Sharpened target

A sufficient route is:

1. prove that for a finite exact-period-p no-reset A-cycle, `a=c_1` itself has minimal temporal period p;
2. prove the primitive-cylinder parity theorem: if a primitive p-periodic seed generates a finite terminating column system, then `P(a)=1`.

The census strongly supports (2) through p=12 and exposes why a proof that ignores exact period cannot work.
