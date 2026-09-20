# Repeated distinguished `011` local geometry is not self-excluding

Status: `finite-exhaustive stopping-fence`. Problem 1 remains OPEN.

## Question

Run150 proved that every forced birth from a sufficiently late two-bit nonresetting `t` source terminates, under sensitive-one provenance, at the distinguished cyclic return `q=t+2` with

    (r_-3,r_-2,r_-1,r_0)(q) = 1011,

and in particular the producing neighborhood at positions `(-2,-1,0)` is the unique `011` obstruction.

The next proposed route was geometric: perhaps two such distinguished events cannot recur at the same source-relative coordinates after the spacing allowed by the nonreset-return theorem, or perhaps their fixed blocks align in a way that telescopes to the finite-support boundary.

This note tests the first necessary local condition before attempting such a budget.

## Exact finite-cone test

For each even separation

    D in {8,10,12,14,16,18,20},

I imposed at time 0

    (r_-3,r_-2,r_-1,r_0) = 1011,

required the center trace through time `D` to be the FULL alternating prefix

    1,0,1,0,...,1,

and required the same block at time `D`,

    (r_-3,r_-2,r_-1,r_0)(D) = 1011.

The construction used Rule 30 directly, `f(l,c,r)=l XOR(c OR r)`.  I fixed the right half through the relevant cone to the particularly simple word

    r_0=1, r_1=0, r_2=1, r_i=0 for 3<=i<=D.

Left-permutivity then uniquely solves `r_-1,...,r_-D` to realize the prescribed alternating center prefix.  For every tested `D`, the solved values at `-3..0` are already exactly `1011`.  Only the three additional extreme-left cone cells `r_-(D+1),r_-(D+2),r_-(D+3)` remain relevant to the target block at time `D`; exhaustive enumeration of their eight assignments found at least one assignment reproducing `1011` at time `D`.

Witness extreme-left triples, in increasing distance from the center, were:

    D=8   : 110
    D=10  : 000
    D=12  : 011
    D=14  : 101
    D=16  : 101
    D=18  : 100
    D=20  : 010

(The same test also succeeds at `D=4,6`, but those separations are excluded for distinct late nonreset sources by the established spacing theorem.)

This is a finite-cone result only.  These rows are not claimed to satisfy the complete cyclic-source/core/gate hypotheses at both endpoints, nor to extend to an infinite FULL finite-support orbit.

## Consequence

The fixed `1011` / `011` source-relative motif from run150 does **not** by itself create a local spacetime incompatibility at any of the first seven admissible even separations `D>=8`.  In particular, the already-proved spacing lower bound of eight steps does not combine with the motif and the finite FULL center trace to give an immediate contradiction.

Geometrically, successive distinguished obstructions occur at the same physical/source-relative cells `(-2,-1,0)` at different even times; their sensitive route is only two steps long and terminates locally.  There is therefore no automatic common backward characteristic supplied by the run150 provenance path itself.  A telescoping argument would need an additional identity connecting the *creation data* of one `011` obstruction to the next episode, not merely the fact that both endpoints contain `1011`.

This is a stopping fence against spending further runs on motif recurrence using only the alternating center prefix and the four-cell distinguished block.  The remaining potentially useful structure is the complete cyclic code/gate/core at the endpoint.  Any next recurrence test should transport one of those all-depth objects across episodes, or derive a charge attached to the `011` event that survives until the next nonreset source.

Dependencies: `problem1_run150_distinguished_source_forces_011_provenance_obstruction.md`; `problem1_nonreset_return_birth_spacing.md`; `problem1_full_center_prefix_places_no_constraint_on_arbitrary_right_half.md`.
