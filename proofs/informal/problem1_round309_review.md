# Round309 recovery and lead review

Status: `partial-proof` for accepted mathematical units and their stated
conditional scopes; `finite-exhaustive` only for declared fixed checks.
Problem 1 remains OPEN. This is supervisor round 1 of the current run,
continuing the interrupted round307/308 work, not a new proof claim.

## 1. Incoming state and ownership

The incoming authoritative handoff is preserved byte for byte in
`docs/astra_handoff_archive_20260907_round309.md`, SHA256
`ce2e4d1ddd60639416fa811d008824e4039bca7a85dd0802dfdac14fc12777f0`.
Initial HEAD was `a89d5eb0f4301fa0736347ed0b9bd42ea4e8347a`.
During this round an independent supervisor maintenance commit advanced
HEAD to `5be12e3712ea9b4259e3e08124e5e795242371d1`. The lead did not
edit or commit supervisor files or rewrite that history.

The worktree already contained an uncommitted fourth round307 unit,
`problem1_nonreset_return_birth_spacing.md`, its eight-cone checker and
result, and Section 6 added to `problem1_round307_review.md`. It also
contained interrupted complete-core and phase-transport notes and an
unfinished core-domain checker. These are recovered and audited here;
they are not reported as newly discovered in this session. Other old
untracked signed-slice work, results, logs, and worktrees remain untouched.

The inherited `problem1_round308_inherited_unit_external_review.md` is
historical draft material. Its claims about earlier provider sessions
are not used as evidence that a fresh review occurred in this round.
The successful fresh review below supplies that evidence directly.

## 2. Recovered nonresetting birth window

Fresh MiMo review: `problem1_round309_recovered_birth_review.md`, thread
`01a07c4e-caa2-7aa2-bd16-0c0ef70f6c92`, now CLOSED. It followed Muse
provider429 failures in threads `01a07c49-8a14-7590-ab28-5a1f98a2ea86`
and `01a07c4c-79a4-7330-90da-d2456b244cf9`, with a non-burst pause
before the one retry. Both Muse threads are CLOSED. Although MiMo was
not in the advertised override list, the required fallback call succeeded.
No native/other provider or settings change was used.

The fresh review found no fatal mathematical flaw in the birth-spacing
unit at its conditional scope. Lead re-checked the full phase-sensitive
argument: the source shadow cone yields centers 0,0,1 and pair
(1,u*(a OR b)); constant-one return trace plus FULL fixes gates t,u;
the two-bit source forces beta=1 at t+4 and hence a new lag-one row at
t+6. G(z)=16A^4z+7 uses the justified symbol c_2=1. It is not a formula
for an arbitrary nonresetting core without that premise.

The seven-time exclusion uses whole-trace statements only where supplied.
At t+6 with beta=0, cyclicity and the current center 1 exclude a
constant-zero core trace; they do NOT make that trace constant one.
The review's initial wording overclaimed constancy and was corrected.
The spacing >=8 is conditional separation, not density or a finite count.

The old atomic record had one stale proof linkage: it stored proof hash
`4aed14b4d83576c1b7c4c63f7e09d4862b70506fb624b552aaaea4c606c57b05`,
while the incoming proof hash was
`2ec25e3570c041d97f838b19f966b68b27f8fa4e0cd97c6ad10cd3b26d83fbde`.
All other old source hashes and its canonical payload matched at review.
This is source drift after the old run, not failure of its eight cones.
The old JSON is preserved BYTE FOR BYTE (SHA256
`2687a4afdca4ca04a5739e336f64c59364c5f90e6245893589b31fe407cfb3b6`).

The checker now accepts an output path solely to preserve that historical
record. A fresh execution of the SAME eight inputs writes
`results/problem1/20260907_round309_nonreset_return.json`, against the
current proof/checker and immutable reference. The record includes exact
fresh-child reproduction arguments. The same 10-second, 128-MiB and
128-KiB caps apply; no input or workload cap was enlarged. Dependencies
of the proof are imported, not claimed freshly reviewed end-to-end.

Disposition: accept the recovered unit at `partial-proof` scope and the
fresh cone record at its eight-input `finite-exhaustive` scope.

## 3. Complete-core domain recovery

The incoming checker had not produced a record. Inspection found three
gaps: it asserted the stricter residue predicate for EVERY gate-permitted
input, it never tested equation (13), and its physical cell cones were
not compared to A in the reversed coordinate convention. The repaired
checker tests the exact predicate equivalence, both intermediate A rows
for z and P(z) using independent cell arrays, and the actual next gate.
Its imported hand RULE source is now included in the source hashes.

The first repaired invocation caught a lead assertion that mistakenly
identified a current time-two symbol2 with the next row's gate u. The
correct correspondence is time-two symbol1 -> next gate u, as follows
from F(x)=4A^2x+3. This was a checker error, not a failed proof identity.
That failed invocation wrote no success record. The corrected finite
checker passes all 32 declared six-bit gate inputs, of which 28 meet D's
extra predicate. No cyclic state, source, driver or M orbit was searched.

Hand identities at z=8 and z=24 precede the finite comparison. Every
check uses two A steps, six retained bits and two high zero padding bits
per scalar step. The proof supplies the arbitrary-upper-word extension;
the finite result does not. Caps remain 10 seconds, 128 MiB and 128 KiB.

Lead domain audit: A^2P(z)=A^2z exactly under the stated five-bit test,
so phase-correct completion identifies cyc(P(z))=z. P's injectivity on D
then follows from uniqueness of cyc. Projection pi M(z)=A^2z is valid on
ALL finite cyclic z; inversion of A is only on its cyclic domain. The
complete original fringe uses the opposite spatial bit orientation and
the exact V map. Its compatibility is an additional all-time condition.
Neither membership in C nor the growing state is a five-bit property.

Fresh review of this unit, phase transport, and the new phase-discrimination
note is assigned to MiMo thread `01a07c5e-bad0-7e32-addd-5d284f1e33ea`.
Final disposition is pending that review and lead integration.
