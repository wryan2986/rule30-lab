# Astra automation handoff — run 122

Problem 1 remains OPEN.

Starting branch tip: `4860ff182854c30169ea15455a4c789045d55ea3` (`research/astra-next`). No intervening work was found after run121.

## New result / stopping fence

Run121 sharpened the characteristic route to require a bridge from forced births to a finite resource in the original ACTUAL row. A weaker version of that bridge is now ruled out.

Rule 30 is left-permutive: `f(l,c,r)=l xor (c or r)`, so toggling `l` always toggles the output. Consequently every initial site `(i,0)` is a genuine Boolean dependency ancestor of `(i+t,t)` along the rightmost characteristic for every `t`.

For a nonzero finite actual row this is especially concrete at its rightmost initial 1, `R`: `x_{R+t}(t)=1` for every `t>=0`. Thus one original actual 1 has certified actual descendants at arbitrarily late times.

Therefore a proof of only

`forced birth -> some original actual 1 ancestor`

would still not give a finite birth count. Finite support plus causal ancestry does not imply bounded reuse. The missing theorem must establish bounded multiplicity / irreversible consumption for the *specific birth certificate*.

Recorded in `proofs/informal/problem1_actual_ancestry_alone_cannot_bound_births.md`.

## Revised target

Do not merely seek an original-1 ancestor for the local `001` forcing event. Seek an injective or uniformly bounded-multiplicity charge: a label/order tied to original actual support that a forced birth consumes and cannot repeatedly reuse. If no such label survives the known regenerative passage, that is the next useful no-go result.
