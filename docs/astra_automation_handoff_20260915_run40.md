# Astra automation handoff — 2026-09-15 run 40

Branch: `research/astra-next`

## Repository state reviewed

Run started from `cd9483226c8965842c4db987cc770846d8b28d7e` (run 39 handoff). No newer work was present. Problem 1 remains open.

Run 39 left two sublemmas for the no-reset periodic-cylinder route: (1) prove that the seed column `a=c_1=c_2` has minimal temporal period equal to the exact period of the finite A-cycle, and (2) prove that a primitive finitely terminating seed has odd XOR parity.

## New theorem: exact period descends to the seed

The first sublemma is now proved.

Under `c_0=0`, the coordinate recurrence forces `c_1=c_2=a`. If `a` had a proper temporal period `q<p`, then every later column would also be q-periodic, because

`c_{i+2}(t)=c_i(t+1) XOR (c_{i+1}(t) OR c_i(t))`

preserves q-periodicity under time shift and pointwise Boolean operations. Thus the entire finite row sequence would satisfy `x(t+q)=x(t)`, contradicting exact period p.

Therefore a genuine exact-period-p no-reset finite A-cycle automatically gives a primitive period-p seed.

This removes the nonprimitive even-parity terminating seeds found in run 39 from the dynamical obstruction: they can only represent lower-period cycles written with an artificially enlarged time modulus.

## File added

- `proofs/informal/problem1_no_reset_seed_inherits_exact_period.md`

Research commit: `c94de53f81cddbf161f219a02ddb590119584c79`.

## Remaining blocker

Only the primitive terminating-seed parity theorem remains in this route:

`primitive periodic seed a + finite termination => XOR_t a(t)=1`.

Run 39's exact scalar parity recurrence is still not closed because it contains adjacent-column overlap parities. The next useful target is to find a telescoping invariant involving both column parity and overlap parity, or an invariant evaluated at the universal finite top boundary. A proof of odd seed parity would combine with run 38's one-bit lifting theorem to establish uniqueness of the periodic orbit at each bitlength and power-of-two period growth.