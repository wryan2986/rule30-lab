# Physical frontier restrictions and the missing projection closure

Status: `partial-proof` for the exact finite parameterization below;
`inconclusive` for its usefulness as an all-depth nonvanishing invariant.
Problem 1 remains open.

## Strategy and admission

The physical-row membership theorem places every sufficiently late finite-seed
half-row in an ordinary phase frontier. Its converse was not proved. Before
transferring generic frontier counterexamples to the physical trajectory, this
pass tests that converse on the named Hamming-pairing obstruction. It also
tests whether physical membership survives stripping a low base-four digit,
as required for a straightforward restriction of the signed-slice induction.

The bottleneck remains an all-depth exclusion of cancellation or of arbitrarily
late admissible occurrence cuts. Ranked routes (`heuristic` judgments):

| Rank | Route | Plausibility / all-depth potential | Falsifiability / testability | Cost |
| --- | --- | --- | --- | --- |
| 1 | Restrict to coupled physical half-rows | Medium / high if closed structural constraints exist | High for named counterexamples and projection / high | Low initial, high proof cost |
| 2 | Control valuations via exact even/odd counts | Medium / high | High for a specified transfer premise / high | Low initial, high proof cost |
| 3 | Partition the joint fibers by return context | Medium / high | High only once a partition is specified / medium | High |

Muse checks only the following predeclared finite consequences:

1. For the existing occurrence `x=0x642fdfb`, degree 27, test every odd
   `1<=S<2^13` at the uniquely possible time `n=27-bitlen(S)`. These are
   4096 seeds, not a larger frontier census. Record all physical witnesses;
   for every hit independently verify its cells and whether the center
   actually alternates through the eight forced branches (`tutututu`) and
   the following center-zero step. Absence means this particular generic
   pairing obstruction does not lie in the late physical domain. Presence
   refutes that exclusion, with full coupled alternation a separate check.
2. Test `x>>2 in R_(d-2)` for every `x in R_d`, in degree order `4<=d<=12`,
   stopping at the first counterexample. A failure obstructs simply
   restricting the existing stripped-digit induction to physical half-rows.
   Finite success would require an actual closure proof, not a cap increase.

Both checks use one local CPU, 120 seconds, and 1 GiB per worker, independent
packed/cell-array comparisons, and atomic records with full provenance. Neither
is a first-witness search over eventually periodic proposed traces.

## Exact physical parameterization (`partial-proof`)

Let T be the packed forward Rule 30 map in the boundary-sufficiency note.
For each integer `d>=2`, define

```text
R_d = {T^(d-s)(S) >> (d-s) :
       S positive and odd, s=bitlen(S), 1<=s<=floor(d/2)}.
```

Then R_d is exactly the set of degree-d center-and-left half-rows
`X=T^n(S)>>n` from an original right-zero seed S, at times `n>=bitlen(S)`.
Here degree means bit length, not the highest occupied bit index.

Proof. Write `s=bitlen(S)`. The highest shifted input bit in T(S) is at
position s+1; the XOR with S cannot remove it. Thus
`bitlen(T^n(S))=s+2n`, and `bitlen(X)=s+n`. For a specified d, the time must
be `n=d-s`; the inequality n>=s is exactly `s<=floor(d/2)`. Conversely every
seed in the displayed set at that time meets the required inequalities.
This proves both inclusions. Together with the section-membership theorem,

```text
R_(2k) subset O_(p,k),       R_(2k-1) subset O_(u,k).
```

There are exactly `2^(floor(d/2)-1)` candidate seeds (the odd integers below
`2^floor(d/2)`). Different seeds may give the same half-row, so this is an
upper bound on |R_d|, not a distinct-state count. For a named x of degree d,
the displayed finite test exhausts all its late physical representations;
no time cap is separately needed. This does not cover representations with
n<bitlen(S), nor does the theorem assert membership of arbitrary frontiers.

## Coupling and ancestry obligations

Physical row membership alone does not assert that its forced zero schedule
is followed by the same finite seed. The two-step derivation also requires
`b=not(x_1(t) or x_2(t))=bit_2(X)` and `bit_3(X)=1-b`. For a finite observed
branch word, the original seed must supply these boundary conditions over
the whole word. An infinite alternating tail would supply them at every block.

Under that hypothetical tail, the actual half-rows remain physical at
successive degrees d,d+2,d+4,..., with the SAME S and times n,n+2,n+4,... .
This forward-time closure differs from the projection `x -> x>>2` used by
signed-slice ancestry. The latter lowers complexity; the physical evolution
raises it. No projection-closure theorem has yet been established here.

## Named pairing obstruction is absent (`finite-exhaustive`)

The full 4096-seed test has zero hits for `x=0x642fdfb`. A second Muse
implementation independently compared packed evolution with a cell array
at every time step for EVERY seed in the box, also obtaining zero hits.
The per-width counts are `1,1,2,4,...,2048`; all resulting half-rows have
bit length 27. The exact parameterization proves these are all possible
representations in the n>=s regime, not just a selected set of times.

Thus `0x642fdfb notin R_27`. Its previously proved pairing obstruction holds
on the generic admissible domain but cannot itself refute that pairing
property restricted to late physical rows. This is one named exclusion;
there is no assertion that all pairing obstructions are nonphysical, that
physical rows admit such pairings, or that the state has no earlier-time
representation. With no hits, the coupled-alternation assessment is vacuous.

Records in `results/problem1/`:

- `20260905_physical_pairing_obstruction.json`, reproduced by
  `scripts/check_physical_pairing_obstruction.py`;
- `20260905_physical_pairing_independent.json`, with the complete independent
  executed source embedded and every candidate trajectory cross-checked.

Lead review replaced a vacuous test and corrected the unused hit-assessment
path to compare all eight steps and the actual physical fringe bit. A positive
small hit and a deliberately wrong driver test that path. The target result
remains zero hits; neither the correction nor the test adds searched targets.

## Projection closure is refuted (`partial-proof` with finite base values)

The assertion `pi(R_d) subset R_(d-2)` for every d>=4 is false. The smallest
failure in degree and state order is d=8, x=205 (`0xcd`):

```text
S=9: 9 -> 63 -> 193 -> 839 -> 3289 under T,
X=T^4(9)>>4=205,
pi(X)=205>>2=51.
```

The seed has s=4 and n=4, so X belongs to R_8. The exact R_6 candidates are
only S in {1,3,5,7}, at times 6-bitlen(S):

| S | n | T^n(S) | X |
| --- | --- | --- | --- |
| 1 | 5 | 1783 | 55 |
| 3 | 4 | 803 | 50 |
| 5 | 3 | 443 | 55 |
| 7 | 3 | 401 | 50 |

Consequently `R_6={50,55}`, which excludes 51. These small explicit values
and the exact parameterization prove the counterexample. Minimality is a
separate finite claim: the exhaustive degree-4..7 sets have no failure, and
the only smaller state in R_8 is 200, whose projection is 50. Muse constructed
R_2..R_12 and stopped testing projection at this first failure. Degrees 9..12
were constructed but not searched for additional failures. The atomic record
`results/problem1/20260905_physical_frontier_projection.json` embeds the
independent cell-array checks and source.

This does not refute projection closure of the ordinary frontiers. Indeed
51 belongs to O_(p,3); it is specifically the physical subfamily that loses
closure. Nor is 205 claimed to be an admissible three-return state. The
counterexample blocks closure on ALL physical rows, leaving a more narrowly
coupled ancestor condition open.

## Even local physical alternation is insufficient

Status: `partial-proof` of a finite obstruction to dropping the return-word
hypothesis. Take S=3 at time n=3. The exact packed rows at times 3 through 6
are `221,803,3565,12819`; their diagonal center bits are `1010`. Thus the
physical half-row `X=221>>3=27` lies in R_5 and undergoes a genuine block
of local alternation.

Nevertheless its depth-one dominant belief at phase u, k=3 is empty.
The base frontiers are `O_(u,2)={6,7}` and `O_(u,3)={24,25,26,27}`.
The current outgoing fiber at quotient `27>>2=6` is 1111. The only adjacent
endpoint in the same low-digit cylinder is y=7, whose fiber at quotient 1
is 1100. Since 1111 is not contained in 1100, y fails dominance and the
belief has no endpoint.

This is not a three-return occurrence: the forced schedule is just `t`,
because its successor is 111, which is 15 modulo 16 and stops. The example
refutes replacing the full return-domain premise with physical membership
and one actual alternating block. It does not refute any stated three-return
conjecture. Muse independently verified the hand calculation, including
cell-array center bits, in
`results/problem1/20260905_physical_local_alternation.json`.

## Strongest remaining obligation

The physical restriction avoids one known generic obstruction, but a signed
induction restricted to this family cannot simply assume that its stripped
ancestors stay physical. Such an argument must enlarge the domain to the
required ancestors, retain coupling to the original seed, or prove a stronger
closure statement on a more specific return domain. None is established here.
An alternative is a finite occurrence-cut bound along the actual forward
physical evolution, which does not use this projection. No such bound is
proved, and least periods >=3 remain outside the alternating-tail route.

Final independent adversarial review by Muse found no outstanding domain
flaw in this note or the companion count-transfer note. The proofs above
remain partial results, with every finite test confined to its stated set.
