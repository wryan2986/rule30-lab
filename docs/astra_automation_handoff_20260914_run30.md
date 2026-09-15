# Astra automation handoff — 2026-09-14 run 30

Branch: `research/astra-next`

## Repository state reviewed

Run started from `bb5fb5419d37dfde6f136846ae019a1a3b18ba58` (run 29 handoff). No newer work was present on `research/astra-next`.

Problem 1 remains open.

## New result: G=3 immediate-reentry exception is closed

Updated:

- `proofs/informal/problem1_immediate_reentry_collapses_return_corridor.md`

Commit:

- `bbab63401aa5b4e5a21945de61aa425ac1b9500b` — close the `G=3` case and correct the run-29 target.

Run 29 had isolated `G=3` because the universal fifth-leading-bit lemma only begins after four physical Rule-30 steps. It then examined when the fifth leading bit of `T^3(R)` could vanish. That was one bit too narrow: for corridor collapse we only need one of the two highest retained bits after truncation to survive.

For a nonzero finite word `w`, define relative leading-edge bits

\[
a_j^{(q)}=(T^q w)_{h+2q-j}.
\]

For `q>=2`, the established leading-edge recurrence gives

\[
a_3^{(q+1)}=1\oplus a_3^{(q)},
\qquad
a_4^{(q+1)}=a_3^{(q)}\lor a_4^{(q)}.
\]

At exactly three steps,

\[
a_3^{(3)}=1\oplus a_3^{(2)},
\qquad
a_4^{(3)}=a_3^{(2)}\lor a_4^{(2)},
\]

so identically

\[
\boxed{a_3^{(3)}\lor a_4^{(3)}=1.}
\]

For `G=3`, the old fringe has bitlength `m-3`, hence `T^3(R)` has bitlength `m+3` and highest position `m+2`. Reduction modulo `2^m` discards relative leading positions `j=0,1,2`; the two highest retained candidates are exactly

- `j=3`, position `m-1`;
- `j=4`, position `m-2`.

Since they cannot both vanish,

\[
\boxed{G'\le1.}
\]

Thus the local theorem is now uniform:

\[
\boxed{G\ge4\text{ even and immediate re-entry}\Longrightarrow G'=0,}
\]

\[
\boxed{G\ge3\text{ odd and immediate re-entry}\Longrightarrow G'\le1.}
\]

The three `G=3` leading prefixes singled out in run 29 are not genuine exceptions. They can make the fifth leading bit vanish, but then the fourth leading bit is forced to one. No admissibility argument is required.

## Consequence

The immediate-reentry branch of the local collision problem is closed: a long same-period return corridor can never collide, immediately re-enter, and thereby reset directly into another long same-period corridor.

The next work should return to the global bottleneck in the older FULL/common-origin/front-residence notes. The remaining issue is no longer local re-entry memory. It is to prove that a finite survivor cannot indefinitely evade long-residence loss by changing period/phase or passing through the resulting short-gap states.