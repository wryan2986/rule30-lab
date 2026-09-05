# Signed-slice transfer: exact correlation requirement and a closure obstruction

Status: `partial-proof` for the all-depth identities and the obstruction to
universal deterministic closure. The restricted three-return nonvanishing
claim remains `inconclusive`. Problem 1 is open.

## Strategy and source boundary

The source checkout is `a49f624342c434aab29f95b6ad1ffe1107e8e22d`, branch
`research/astra-next`. The signed-slice scalar identity was read from sibling
commit `c79b67a1df3e9d32681223a4bf8bc0a98d8bf928` at
`proofs/informal/problem1_period_two_signed_slice_recursion.md` using
`git show origin/research/period-two-signed-slice-recursion:...`.
No sibling branch was merged. The local weighted-shadow, adjacent-shadow,
projection, lift-recursion, full-domain signed-mass, and scope-audit notes
supply the definitions and boundary conditions used here.

The bottleneck is to show `S_a(k,c+1,x) != 0` for every full three-return
occurrence, and separately rule out occurrences with `c+1>=k-1`. To induct
using five-component slices, one must either determine their evolution or
control all possible evolutions. A dot-product formula for a scalar is not
by itself a vector recurrence.

Route ranking (`heuristic`, qualitative research judgments):

| Rank | Route | Plausibility | All-depth potential | Falsifiability / testability | Cost |
| --- | --- | --- | --- | --- | --- |
| 1 | Check vector transfer; then seek a preserved region | Medium | High if sufficient structure exists | High / high | Low initial |
| 2 | Sign-reversing endpoint pairing with a nonzero remainder | Medium | High | Medium / medium | High |
| 3 | Prove the boundary cut bound | Medium | Partial but necessary for this route | High / high | Medium to high |
| 4 | Modular or valuation exclusion of cancellation | Low without a new mechanism | High | High / high | Low initial, uncertain thereafter |

Route 1 was selected for a bounded falsification test before attempting an
invariant proof. A separate review of route 3 found no depth bound. The
companion connected-region obstruction narrows route 1 further.

## Definitions and exact transfer (`partial-proof`)

Let `M_(a,j)(z)={e:4z+e in O_(a,j+1)}`. Use the five-mask alphabet
`A=(0000,0011,1011,1100,1111)` and distinct concrete endpoint beliefs from
`problem1_period_two_weighted_shadow_recursion.md`.

Write a parent cylinder and its child as

```text
P=(a,h,D,q),    N=(a,h+1,D+1,4q+d),
h>=3, 1<=D<=h-2, 4q+d in O_(a,h+1), q in O_(a,h).
```

The nonboundary range suffices here; at greater valid depths the separation
lemma empties the belief. Put `m=M_(a,h)(q)`, so `d in m`. For each parent
shadow `p in B_a(h,D,q) subset O_(a,h-1)`, write `w(p)=(-1)^cost(p)` and
`n(p)=M_(a,h-1)(p)`. The parent vector is

```text
V_n(P) = sum_{p in B(P), n(p)=n} w(p).
```

Define a joint signed table for the prescribed digit `d`:

```text
J^d_(n,r)(P) = sum w(p),
```

where the sum is over the SAME concrete endpoints `p in B(P)` satisfying

```text
n(p)=n, d in n, and M_(a,h)(4p+d)=r.
```

For `d notin n` set this entry to zero. Every child `4p+d` in this definition
exists by `d in n`; the outgoing fiber `r` may be empty.

Then the exact marginal and vector identities are

```text
sum_r J^d_(n,r)(P) = 1[d in n] V_n(P),
V_r(N) = sum_n epsilon_m(n) J^d_(n,r)(P),
```

with `epsilon_m(n)=0` if `m` is not contained in `n`, `+1` for `n=1111`
when dominant, and `-1` otherwise when dominant.

Proof. A fixed eligible endpoint `p` has exactly one outgoing child fiber
`r`, giving the marginal identity. The concrete lift theorem identifies each
child shadow uniquely with `4p+d`. Its new dominance test depends on `n(p)`
and its weight becomes `epsilon_m(n(p)) w(p)`. Group these actual children
by their outgoing fibers `r` to get the second identity. Since `m` contains
`d`, every omitted row has multiplier zero; summing over `r` recovers

```text
S(N)=sum_n epsilon_m(n) V_n(P).
```

These are all-depth identities, with no endpoint splicing. The joint table
retains a correlation discarded by the vector. It is not claimed to evolve
as a closed 25-component state, nor does this identity itself prove
nonvanishing.

## Exact universal collision (`refuted` closure assertion)

The assertion being refuted is: phase, parent complexity and depth, adjoined
digit, current new mask, and full parent slice vector determine the child
slice vector on all ordinary cylinders. Even supplying the next outgoing
current mask and the next high-position current mask does not repair it.

The collision has phase `p`, parent complexity 6, depth 1, digit 0,
new mask `1011`, and parent vector `(2,0,0,0,1)` in both cases:

| Quantity | First transition | Second transition |
| --- | --- | --- |
| Parent state | `0xc82` | `0xc88` |
| Child state, complexity 7, depth 2 | `0x3208` | `0x3220` |
| Child vector | `(0,0,1,0,0)` | `(0,0,0,0,1)` |
| Parent signed mass | 3 | 3 |
| Child signed mass | 1 | 1 |
| Child outgoing current mask | `1011` | `1011` |
| High current mask (position 1 in child) | `1111` | `1111` |

The complete concrete parent beliefs are small:

```text
P1: (endpoint, cost, outgoing mask)
    (0x322,0,1111), (0x372,0,0000), (0x376,0,0000).
P2: (endpoint, cost, outgoing mask)
    (0x320,0,1111), (0x370,0,0000), (0x374,0,0000).
```

Only the full-fiber endpoint survives the first lift in each case:

```text
N1: (0xc88,0,1011).
N2: (0xc80,0,1111).
```

Thus `J^0_(1111,1011)=1` in the first transition and
`J^0_(1111,1111)=1` in the second. The other entries contributing to the
child vector are zero. These distinct correlations have identical marginals.

Adjoin digit zero once more. The common next current mask is `1011`, so
the resulting complexity-8, depth-3 current states and signed masses are

```text
0xc820: -1, unique shadow 0x3220 of cost 1;
0xc880: +1, unique shadow 0x3200 of cost 0.
```

Consequently the initial five-component vector does not even determine the
two-lift scalar mass when both common digits `00` and both introduced masks
`1011,1011` are prescribed. Any universal deterministic map or transfer
matrix on that proposed state would give equal outputs for equal inputs,
contradicting these exact witnesses. The scalar one-lift identity survives.

The examples are ordinary cylinders, not demonstrated members of the
all-depth three-return ancestor domain. They do not refute deterministic
closure restricted to that domain. Their low digits are not the required
three-return base digit, but that alone would not exclude their being
stripped ancestors at some higher complexity.

## Bounded check and admission

The test was admitted before execution in the pre-existing, untracked
`problem1_signed_slice_transfer_audit.md`, which this pass preserves.
The question was the universal closure assertion above, plus its stronger
input key, with a separate check on ancestors of the full three-return
domain. A collision closes only the corresponding deterministic quotient;
finite absence gives no infinite closure theorem and authorizes no larger
census. The outgoing mask and the already-used high mask are distinguished
explicitly in the final implementation.

Caps: universal parent complexity at most 9, both phases, all valid depths;
three-return occurrences through complexity 16, all 56 admissible gap
triples, every cut, final-u admissibility; schedule cap 64, one local CPU,
120 seconds and 1 GiB. The universal search is ordered by parent complexity,
phase `p` then `u`, depth, state, and digit. Each collision search stops at
its first collision; the bounded independent belief/identity verification
also covers the complete universal transition box.

Results (`finite-exhaustive` only within the stated boxes): the collision
above is first under this order. The restricted-domain check sees 19
occurrences, 25 distinct ancestor cylinders, and only 8 parent-child
transitions, with no vector collision. That last check is too small to
justify an all-depth closure claim; it is reported to keep the domain
quantifiers explicit.

Muse supplied the analyzer and tests. Lead review independently recalculated
the displayed parent and child endpoint tables with the pre-existing
independent signed-mass oracle and corrected issues before integration.
The precise verification counts, timings, hashes, and software/hardware facts
are in `results/problem1/20260905_signed_slice_transfer_check.json`.

Final integration check: 39 tests pass, comprising the 15 new transfer tests
and the existing weighted-shadow and independent signed-mass tests:

```text
.venv/bin/python -m pytest \
  tests/python/test_period_two_signed_slice_transfer_check.py \
  tests/python/test_period_two_weighted_shadow_recursion.py \
  tests/python/test_three_return_signed_mass_independent.py -q
```

The record's source and output hashes were independently checked against the
files being committed. The immutable reference hash remains
`358bdc07904e77080eb78b67bdd8da25822d6b51f1a91b58b5313dfe461c1d01`.

## Consequence for the next proof attempt

Two independent obligations now stand out. A transition argument needs
actual joint endpoint information or a theorem restricting it on the
three-return domain. A hyperplane-avoidance region must also distinguish
the opposite-sign contexts in `problem1_signed_slice_convex_obstruction.md`;
a single connected real region covering them cannot work.

Neither result refutes a union of regions indexed by genuine return context,
an arithmetic exclusion inside a real region, or a concrete sign-reversing
pairing with a provably nonzero remainder. These are possible next targets,
not established invariants. The separate boundary obligation and the eventual
period-two reduction hypotheses remain unresolved; nothing here excludes
eventual period two or general eventual periodicity.

Subsequent endpoint-operator result:
`problem1_walsh_sign_obstruction.md` gives the exact diagonal-filter,
digit-embedding, and Walsh-convolution formulas. A four-point certificate
on an actual three-return belief rules out affine-character sign modulation
and exhibits four local plane modes. This is distinct from the universal
five-vector closure collision above, and does not prove nonvanishing or
exclude general multimode transfer.
