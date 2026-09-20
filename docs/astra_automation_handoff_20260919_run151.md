# Astra automation handoff — 2026-09-19 run151

Problem 1 remains OPEN.

## New result

Run150's mandatory distinguished `011` obstruction does not by itself yield a recurrence contradiction at the spacings allowed for distinct late nonreset sources.

An exact finite-cone Rule-30 test imposed the distinguished block

    (r_-3,...,r_0)=1011

at times 0 and `D`, together with the FULL alternating center prefix through `D`.  For every even admissible separation tested,

    D = 8,10,12,14,16,18,20,

there is a local cone witness.  A single simple right driver works in every case tested: `r_0=1,r_1=0,r_2=1` and `r_i=0` for `3<=i<=D`; left-permutivity uniquely supplies the left cells required by FULL, and one of the eight assignments to the three remaining extreme-left cone cells restores `1011` at time `D`.

Full note: `proofs/informal/problem1_run151_repeated_011_local_geometry_not_self_excluding.md`.

## Interpretation

The run150 sensitive route terminates after two backward steps at the local `011`; it does not itself continue along a characteristic to the initial-support boundary.  Repeated copies of the fixed `1011` motif are locally compatible with the alternating center trace at the first seven allowed even episode separations.  Therefore do not spend more runs seeking a contradiction from only motif recurrence + FULL center prefix + the spacing >=8 theorem.

The witnesses are finite-cone witnesses, not complete cyclic/core/gate models at both endpoints.  The remaining leverage must come from the all-depth source data omitted by this test.

## Next target

Use the complete cyclic code/core at a distinguished `q=t+2` source, not just its local `1011` block.  Test whether transporting the known pure cyclic code through to the next possible nonreset episode gives an invariant/phase constraint on the next distinguished `011`, or whether the arbitrary fringe again absorbs it.  Alternatively identify a quantity attached to the `011` creation event that is preserved or monotone until the next nonreset source.  Any local finite-prefix recurrence test should first include a genuinely new all-depth gate/core condition.
