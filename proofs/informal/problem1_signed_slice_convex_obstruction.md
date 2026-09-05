# Convex-region obstruction for signed slices

Status: `partial-proof` for the connected-region obstruction below, supported
by exact finite witness replay. Three-return nonvanishing remains
`inconclusive`; Problem 1 is open.

## Admission

The sibling signed-slice note gives two phase-u cylinders at complexity 18
whose new current mask is `1011` and whose child masses have opposite signs:
`(0x642e4d2f1, L=3)` and `(0x6473d46ab, L=5)`. Before using them to constrain
an invariant on the three-return ancestor domain, their membership in that
domain must be established; mere frontier membership is insufficient.

Test only these two named cylinders and their base-four descendants obtained
by adjoining at most three low digits. For a descendant with `s` added digits,
test a gap-222 occurrence at cut `L+s-1`, including final-u admissibility.
Use exact recursive frontier membership and replay a generator witness.
Recalculate the two parent slice vectors with independent direct and recursive
concrete beliefs, building only the phase-u frontier through complexity 18.
No nonvanishing census or complexity-cap increase is authorized by this test.

If both signs occur in the admissible ancestor domain, no single convex region
containing that domain's vectors for mask `1011` can exclude its cancellation
hyperplane: a segment between opposite signs crosses it. This would close
single-region cone/order proposals, while leaving unions of regions and
schedule-dependent invariants open. If ancestry is not established within
the fixed descendant box, these examples do not establish that obstruction on
the restricted domain. Neither outcome decides signed nonvanishing.

Limits: one local Python process, 120 seconds, 1 GiB address space, two named
parent-vector checks, at most 85 descendants per named cylinder, forced
schedule cap 64. Record exact parameters, source hashes, full Git commit,
hardware/software, timing, and the output atomically. Small generator and
belief checks precede the named cases. No reference-source edits.

## Definitions and the precise invariant class

For `a in {p,u}`, let `B_a(k,L,x)` be the distinct concrete dominant belief
defined in `problem1_period_two_weighted_shadow_recursion.md`. The outgoing
slice vector of a cylinder `P=(a,h,D,q)` is

```text
V_n(P) = sum_{p in B_a(h,D,q), M_(a,h-1)(p)=n} (-1)^cost(p),
n in (0000,0011,1011,1100,1111).
```

For a child `N=(a,h+1,D+1,4q+d)` with new current mask
`m=M_(a,h)(q)`, the exact signed lift gives

```text
S(N) = ell_m(V(P)),
ell_1011(v) = v_1111 - v_1011.
```

Here the *ancestor domain* consists of admissible three-return cylinders and
every cylinder obtained from one by stripping fewer than its depth many low
digits, lowering complexity and depth together. An ancestor need not itself
start a forced zero schedule. Its ancestry must be witnessed, not assumed.

The candidate class addressed here is a single real region containing every
parent vector used on that ancestor domain with a fixed phase, parent
complexity, new current mask, and positive parent signed mass. Such a region
cannot certify nonvanishing just by avoiding `ker(ell_m)` if it is connected.
The theorem concerns this explicit relaxation in `R^5`, not arbitrary
subsets of the integer lattice or a separate region for each full state.

## Exact witnesses (`finite-exhaustive` targeted replay)

Both transitions have phase `u`, parent complexity 17, new current mask
`1011`, and positive parent signed mass. Vector order is as above.

| Quantity | Negative child | Positive child |
| --- | --- | --- |
| Child complexity | 18 | 18 |
| Child state | `0x642e4d2f1` | `0x6473d46ab` |
| Child depth | 3 | 5 |
| Adjoined digit | 1 | 3 |
| Parent vector | `(262,0,200,27,117)` | `(3,0,5,0,7)` |
| Parent mass | 606 | 15 |
| Child mass | -83 | 2 |

The negative child's admissible descendant is

```text
phase u, k=19, x=0x190b934bc7, L=4, cut=3, gaps=(2,2,2).
forced schedule: uttutututu
base prefix: utt
observed w E(g): uttututut
admissibility word w E(g) u: uttutututu
generator witness: uuputpuuuututututut
```

Stripping its low digit gives exactly `(18,0x642e4d2f1,3)`.
The positive child itself is admissible:

```text
phase u, k=18, x=0x6473d46ab, L=5, cut=4, gaps=(2,2,2).
forced schedule: ttttutututu
base prefix: tttt
observed w E(g): ttttututut
admissibility word w E(g) u: ttttutututu
generator witness: uutuuttuupupuuupup
```

The initial `u` in each generator witness denotes the phase seed `1` at
complexity one; subsequent letters are generator applications. The observed
extra final `u` is convenient in these examples; the general convention
requires only its admissibility. Direct and recursive endpoint beliefs agree
for both children and parents. Both exact vectors match the sibling note;
ancestry is the additional check needed for the present application.

## Connected-region obstruction (`partial-proof`)

Let `v-` and `v+` be the displayed vectors. If a connected set
`K subset R^5` contains both, then

```text
K intersects {v : v_1111 = v_1011}.
```

Proof. The continuous linear map `ell_1011` takes values `-83` and `2`
on `K`. Its image is connected in `R` and therefore contains zero.
This proof has no depth cap. The finite witnesses establish its premises
inside the actual ancestor domain, even after fixing phase `u`, parent
complexity 17, mask `1011`, and positive parent mass.

For a convex region the crossing point is explicit:

```text
(2 v- + 83 v+)/85 = (773,0,815,54,815)/85.
```

It is nonzero. For a convex cone the unnormalized vector
`(773,0,815,54,815)` is a nonzero element of the cancellation hyperplane.
Consequently even the weaker cone requirement `K intersect ker(ell)={0}`
is impossible for a cone containing both witnesses. Dividing each witness
by its positive parent mass preserves the opposite signs, so a single
connected region in that normalized slice also fails.

This is a class obstruction, not a cancellation example: no claim is made
that the displayed convex combination is a reachable vector. The theorem
does not exclude a connected region whose hyperplane intersection can
separately be proved unreachable. It excludes using the region's
hyperplane avoidance itself as the certificate.

## Boundaries and next route

- `refuted`: a single connected real region containing these admissible
  ancestor vectors and avoiding the local cancellation hyperplane.
- `inconclusive`: regions indexed by adjoined digit, depth, fuller schedule
  context, or sign of the child functional; disconnected unions; arithmetic
  exclusions inside a real region; endpoint pairing certificates.
- The two examples have different depths and different adjoined digits.
  They do not refute a separate invariant for each such context.
- `inconclusive`: signed nonvanishing on the full three-return domain and
  the boundary obligation `c+1<=k-2`.

The useful next test is whether a mathematically defined return-context
partition preserves a union of regions, with exact joint endpoint data
controlling its transitions. Defining the partition by the unknown sign of
the child mass alone would restate the target. A sign-reversing endpoint
pairing with a controlled nonzero remainder remains an alternative.

## Reproduction

Run `python3 scripts/check_signed_slice_convex_obstruction.py`.
The atomic record is
`results/problem1/20260905_signed_slice_convex_obstruction.json`. It includes
the full source commit, hashes, machine facts, timing, both exact vectors,
generator witnesses, and all qualifying descendants in the fixed box.
The check exhausts 85 descendants for each of two named cylinders, with
255 independent Boolean-generator comparisons and 289 small direct/recursive
belief comparisons before the named checks. It does not search for new
signed zeros, assert a smallest opposite-sign pair, or increase a census cap.

Independent Muse witness replay and proof/code review are recorded in
`problem1_three_return_boundary_review.md` and the archived atomic result
`results/problem1/20260905_boundary_convex_ancestry_replay.json`. That review
independently checks generator witnesses, schedule admissibility, and the
linear-algebra argument; it does not independently re-enumerate the two
large parent beliefs. Those retain the lead run's direct/recursive agreement.
