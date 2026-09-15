# Astra automation handoff — 2026-09-15 run 39

Branch: `research/astra-next`

## Repository state reviewed

Run started from `faffb0ceff94236f323d9fb02fdb3a828ca075c7` (run 38 handoff). No newer work was present. Problem 1 remains open.

Run 38 reduced uniqueness/power-of-two periods to a parity obstruction for the no-reset spacetime cylinder.

## New exact identity

For periodic columns `c_i(t)` satisfying

`c_{i+2}(t)=c_i(t+1) XOR (c_{i+1}(t) OR c_i(t))`, define `P_i=XOR_t c_i(t)` and `<v,w>=XOR_t(v(t) AND w(t))`. Then

`P_{i+2}=P_{i+1} XOR <c_i,c_{i+1}>`.

The time-shift parity cancels exactly. A finite top boundary also forces the universal suffix `...,0,1,1,0` in the last four columns.

## Computational refinement

Direct cylinder enumeration found no primitive (minimal temporal period p) even-parity seed that terminates at a finite top boundary through p=12, searching 500 columns per seed. At p=8 exactly eight primitive seeds terminate, all odd parity, at top-column index 399; they are the eight phases with masks `13,26,52,67,104,134,161,208`. This independently recovers the bitlength-400 parent at the 401 period-doubling threshold.

However, the stronger statement without primitivity is false: even-parity terminating seeds exist when the declared period is nonminimal (for example p=4 masks 5 and 10, inherited from period 2). Thus exact temporal period is essential to any parity proof.

## File added

- `proofs/informal/problem1_column_parity_recurrence_and_primitive_seed_census.md`

Research commit: `690e869fb6554be5c75f688b35329dab02111fbc`.

An attempted checker-file write was rejected by the connector safety layer, so no script was committed in this run; the mathematical note contains the census specification and exact results.

## Next target

First prove or disprove that in a finite exact-period-p no-reset A-cycle, the seed column `a=c_1` must itself have minimal temporal period p. If true, attack the sharpened primitive-cylinder theorem: a primitive periodic seed that terminates in the finite `...,0,1,1,0` top boundary must have odd XOR parity. The scalar parity recurrence is exact but not yet closed because adjacent-column overlap parities remain.