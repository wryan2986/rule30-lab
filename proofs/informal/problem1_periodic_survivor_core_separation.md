# Separating the alternating-branch survivor from ordinary leading cores

Status: `partial-proof` for the all-depth separation and restricted
boundary consequences; `finite-exhaustive` for the reused-core
comparison. General B_all and Problem 1 remain open.

## Admission before execution

The newly explicit rational survivors -7/127 and -123/127 permit a
sharper test of long alternating FORCED branch prefixes. This means
branches utut..., not an assumed alternating center conclusion.
The existing finite repetition theorem already bounds any period-2
branch prefix by k+2 using only integer size. Do not repeat that proof
or increase a frontier cap. Test the additional ordinary leading-core
constraint using ONLY the committed cores h<=8 and stabilization ages.

Candidate exact separation: let a be a phase, h a stored core level,
b a residue width, and k-h at least the stored stabilization age.
If the residues of C_(a,h) modulo2^b are disjoint from every rotation
of BOTH 7-bit survivor patterns, then an ordinary endpoint in O_(a,k)
cannot have an alternating observed prefix of length
`r>=k-h+ceil(b/2)-1`. Its cylinder fixes 2r+2 low bits; projection
by 2(k-h) bits would put the same residue in these disjoint sets.

Compare b=1,...,bitwidth(C) for the existing 16 cores. A separating
entry gives an all-k ordinary-domain bound via the established head
theorem; no separation leaves this proposed refinement unproved at the
available levels and does not authorize larger cores. Retain the exact
best entries and derive the cut consequences before claiming them.
This only refines a rigorously identified repetition subclass of the
boundary problem; arbitrary return prefixes remain outside its scope.

Packed periodic-word extraction and independent cell rotation must
agree on the same stored core inputs. Do not regenerate any frontier,
scan any new ordinary endpoint, or enumerate forced schedules. Local
one CPU, 120 seconds and 1 GiB, atomic provenance with exact source,
input hashes, full base Git, hardware/software, timings and limitations.

## 1. Separation with the original head clock (`partial-proof`)

Let x belong to O_(a,k), and suppose its first m forced updates exist.
Put x_m=F^m(x). Fix h<=k. The existing head and forced-projection
identities give

    pi^(k+m-h)(x_m)
      = A^(2m)(pi^(k-h)(x))
      belongs to A^(k-h+2m)(O_(a,h)).                (1)

Indeed `pi^m F^m(x)=A^(2m)(x)`, and pi commutes with A. Therefore
the projected state in (1) belongs to the stable core C_(a,h) whenever

    k-h+2m >= tau_(a,h).                            (2)

The clock is k-h+2m, retaining BOTH the original complexity and the
elapsed forced age. Using only the later complexity k+m would lose
this stronger stabilization condition.

Suppose the next r OBSERVED branches starting at m alternate, beginning
with either u or t. The exact finite cylinder theorem, compared with
the corresponding rational survivor Z in {-7/127,-123/127}, gives

    x_m = Z mod 2^(2r+2).                           (3)

The equality holds even if the next gate after those r branches fails.
No unobserved admissibility letter is used. Let P_b contain all low b-bit
residues of all seven rotations of both periodic survivor words. If

    (C_(a,h) mod2^b) intersect P_b is empty,         (4)

then (1)--(3) are incompatible as soon as

    2r+2 >= 2(k+m-h)+b.

Consequently, under h<=k and (2), EVERY such alternating branch segment
obeys

    r <= k+m-h+ceil(b/2)-2.                         (5)

For clarity, division in (3) projects the periodic rational Z by
2(k+m-h) bits, which is one of its seven rotations. It does not assert
that the ordinary integer x_m itself is spatially periodic. This is
the precise overlap that (4) excludes. The rounding in (5) is obtained
by first excluding integer r>=k+m-h+ceil(b/2)-1.

## 2. Two explicit six-bit separations (`partial-proof`)

The already verified head data give

| phase a | h | tau_(a,h) | core residues modulo64 |
| --- | --- | --- | --- |
| p | 7 | 9 | 23,26,51,57 |
| u | 8 | 10 | 39,46,51,52 |

The exact common periodic-tail set is

    P_6={3,7,14,28,31,33,47,48,55,56,59,61,62,63}.

Both displayed core sets are disjoint from P_6. Thus (5) specializes to

    p: r<=k+m-6,  provided k>=7 and k+2m>=16;
    u: r<=k+m-7,  provided k>=8 and k+2m>=18.        (6)

At m=0 this improves the existing size-only bound r<=k+2 to
r<=k-6 for p,k>=16 and r<=k-7 for u,k>=18. This is a consequence
of ordinary membership and stable leading blocks, not a stronger
integer-size inequality and not a claim for every positive integer.

## 3. Restricted three-return boundary exclusion (`partial-proof`)

Suppose a genuine gap-222 occurrence starts at cut c>=m and the
WHOLE observed segment from m through its six branches is alternating.
Its length is r=c-m+6. Equation (6) gives

    p: c <= k+2m-12;
    u: c <= k+2m-13,                                (7)

with the corresponding conditions in (6). In particular, this proves
the required B_all inequality c+1<=k-2 on this subclass whenever

    p: 0<=m<=4, k>=7, k+2m>=16;
    u: 0<=m<=5, k>=8, k+2m>=18.                     (8)

The first m branches may be arbitrary actual admissible branches.
There is no assumed periodicity of those branches and no restriction
on later unobserved branches. This extends the earlier repetition-only
boundary certificate, which did not discharge B_all at positive m.

The hypotheses are load-bearing. A locally alternating six-branch
motif does not make its entire preceding segment alternating. An
arbitrary late start m need not satisfy (8). No exclusion of other
gap triples, arbitrary cuts or eventual center alternation follows.
Even the unrestricted gap-222 boundary question remains open.

## 4. Verification, provenance and next obligation

Status: `finite-exhaustive`. Two representations of the same rational
tails agree on 136 comparisons across the 16 stored cores: one expands
the repeating binary words, and the other computes -a/127 by modular
inversion before projecting. Both use exactly the committed core sets,
whose original construction is not rerun. There are no new frontier
states, forced orbits, widths or schedule inputs.

The atomic record
`results/problem1/20260906_periodic_survivor_core_separation.json`
contains both matching hashes, every residue set and intersection,
the exact core-input snapshot, the pre-execution admission and source,
full base Git, source/input hashes, hardware/software facts and timings.
Its executable is
`experiments/problem1_nonperiodicity/check_periodic_survivor_core_separation.py`.
Both computations are lead-local; mathematical external review is
recorded separately. The infinite quantifiers in (5)--(8) come from
the head/cylinder lemmas and the exact finite disjointness, not from
absence of examples in a search. Fresh Muse adversarial review accepted
the head clock, residue projection, rounding and restricted B_all
consequences; its report and reviewed source snapshots are in
`results/problem1/20260906_boundary_survivor_muse_review.json`.

Dependencies: `problem1_frontier_head_dynamics.md` sections 1 and 4
(head and forced-projection identities),
`problem1_finite_schedule_repetition_bound.md` section 1 (finite
common-prefix cylinder), and
`problem1_boundary_sum_periodic_tail_probe.md` sections 1--2 (the
explicit rational survivors).

Next (`inconclusive`): an arbitrary near-boundary return may contain
interruptions of alternation throughout the preceding history. The
new bound covers a proved short-transient subclass, not that domain.
Control of those interruptions, or a different history observable,
is still needed. Do not increase the core or periodic-tail cap.
