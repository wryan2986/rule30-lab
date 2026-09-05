# Deleting a generator from an ordinary representation

Status: universal single-deletion construction `refuted` on a genuine
three-return occurrence. The deletion criterion, exact maximum recursion,
and conditional cut bound are `partial-proof`. Named-state computations
and representation counts are `finite-exhaustive`. Problem 1 remains open.

## Bottleneck and ranked routes

For a genuine occurrence x in O_(a,k) at cut c, a constructive adjacent
shadow must be a state y in O_(a,k-1) with y=x modulo 4^(c+1).
Rounded projection loses the base word; conjugating it by that word can
produce a negative integer or a state outside the lower frontier. The
current question is whether ordinary generator representations supply a
different size-reducing construction while preserving that residue.

| Rank | Route | Plausibility / all-depth potential | Falsifiability / cost |
| --- | --- | --- | --- |
| 1 | Delete one noninitial generator from some representation | Exact lower membership for free; a selection theorem would suffice | High / low on named failures |
| 2 | Replace a generator block by a shorter block with equal action on the prefix residue | More flexibility; requires an all-depth shortening rule | High once block class specified / medium |
| 3 | Control return-conditioned endpoint correlations | Could prove signed nonvanishing directly; no closed invariant yet | Medium until specified / high |

The ranking is `heuristic`. No success of any route is assumed.

## Candidate criterion and finite admission

Write a representation from zero as g_1...g_k, with g_1=a, and let v be
the positive prefix state before position i>=2. Deleting g_i leaves the
initial phase intact and gives a lower-frontier state. Every common suffix
is a 2-adic isometry. Candidate exact criterion: for m>=1 the deletion
preserves the output modulo 2^m if and only if g_i=T and
v=0 modulo 2^(m-1). For U and P the parity always changes. For T the
first changed bit is one above v's lowest nonzero bit. The required
occurrence modulus has m=2c+2. This is a candidate all-depth identity to
test independently before proof adoption.

Candidate universal witness claim: every genuine full-domain occurrence
admits some ordinary representation and a noninitial single deletion that
preserves the required base residue. Failure of just one representation
does not refute this existential claim.

Admitted check: only the two first gate failures from the previous note,
u/k14/0x642fdfb/cut1/w=t and p/k16/0xc85f8787/cut2/w=ut,
with their committed original generator witnesses and gap labels. First
replay every noninitial deletion of each named representation. Test the
criterion against direct forward congruence at m=1,...,2c+2 for those
deletions. If the named representation fails, decide the existential
single-deletion claim over ALL representations of that same named state
by exact inverse-generator predecessor recursion, with memoization and
root/phase/bit-length checks. Do not enumerate complete frontiers or
extend the occurrence input set. Recover/replay a shortened witness if
one exists; otherwise retain a complete predecessor certificate. Measure
the maximal prefix valuation before a T edge over root-reaching paths.

Either outcome changes the argument: an exact all-representation failure
closes this certificate class on the genuine domain; success isolates a
precise selection/valuation statement still needing proof. No input-box
increase follows. One local CPU, 120 seconds, 1 GiB; atomic JSON with
full Git commit, parameters, hardware/software, timings, source/dependency
hashes, and exact limitations. Independent replay must use a different
inverse or finite forward construction before adopting a counterexample.

## 1. Exact deletion criterion (`partial-proof`)

For positive v write t=v2(v). The quantity
T(v) XOR v=(v<<1) OR (v<<2) has its lowest set bit at t+1. Thus

```text
v2(T(v)-v)=v2(v)+1.                              (1)
```

Both U and P flip parity, so their differences from v have valuation zero.
Every generator has output bit j equal to input bit j XOR a function of
strictly lower input bits. Consequently it preserves the first position
where two inputs differ; any common suffix is a 2-adic isometry. After
deleting a noninitial generator from a fixed representation, the two
outputs therefore differ with valuation (1) for T, and zero for U/P.
This proves the proposed iff for every m>=1, including an empty suffix.
All relevant prefixes are positive. The excluded zero-prefix case would
have T(0)=0 and infinite valuation, but cannot arise after the phase root.

The shortened word still starts with a, so it lies in O_(a,k-1). Hence
a deletion constructs the desired adjacent shadow exactly when its T-input
has valuation at least 2c+1. This is a representation-level criterion,
not an assertion that such an input exists on every genuine occurrence.

## 2. All-representation criterion (`partial-proof`)

Fix a phase a. A node (j,n) is reachable if n belongs to O_(a,j). Let
H_a(j,n) be the largest v2(v) before any noninitial T edge on ANY
representation of that node; for a reachable node without such an edge,
set H=-1. Unreachable nodes must be marked separately, not given H=-1
and then allowed to contribute a new edge.

The only reachable level-one node is the prescribed phase root (3 for p,
1 for u), with H=-1. For j>=2 take the at most three exact nonnegative
generator predecessors v of n. Discard predecessors not reachable at
level j-1, including those of the wrong bit length. Then

```text
H_a(j,n) = max over remaining labelled predecessors (g,v) of
           max(H_a(j-1,v), v2(v) if g=T else -1). (2)
```

The node is reachable iff that predecessor set is nonempty. Proof is
induction on j: every representation has exactly one final labelled edge,
and appending that edge preserves all earlier candidates and creates only
the stated possible T candidate. All positive generators increase bit
length by two, so the recursion terminates at the fixed root. Duplicate
representations may be merged at nodes without losing the maximum.

Combining (1) and (2), the existential single-deletion claim for a specified
occurrence is equivalent to H_a(k,x)>=2c+1. This controls every ordinary
representation, not just a reconstructed witness. It does not control
arbitrary lower-frontier states or longer block replacements.

## 3. Stronger conditional cut bound (`partial-proof`)

If an odd x in O_(a,k) admits a single deletion preserving its residue
modulo 4^(c+1), c>=0, then

```text
c <= k-4.                                        (3)
```

Indeed the eligible T-input v has valuation at least 2c+1>=1, so is even.
The phase root is odd, so its prefix complexity j is at least two. Since
T(v) is even whereas x is odd, at least one suffix generator follows it;
thus j<=k-2. Every positive generator output has top two bits 11. Writing
delta=0 for p and 1 for u gives

```text
2c+1 <= v2(v) <= bitlen(v)-2 = 2j-delta-2
      <= 2k-delta-6.
```

Integrality yields (3) for both phases. In particular k<=3 has no such
deletion; there is no exceptional root case. This is conditional on a
successful deletion. If the universal deletion conjecture held, it would
imply a bound one cut stronger than B_all's c<=k-3. Neither unconditional
bound has been proved by this argument.

## 4. Initial two-state result (`finite-exhaustive`)

Both admitted initial states have single-deletion shadows, including the
one whose chosen representation fails:

| State / cut | Chosen word succeeds? | All-representation maximum | Required valuation |
| --- | --- | --- | --- |
| u14 / 0x642fdfb / 1 | Yes | Not computed | 3 |
| p16 / 0xc85f8787 / 2 | No: chosen maximum 2 | 7, over 216 words | 5 |

For the first state, delete position 7 of `uuuuputptuutuu`. Its input
is 0x640, of valuation 6. The shortened word `uuuupuptuutuu` yields
y=0x1bd9c7b in O_(u,13), congruent to x modulo 16.

For the second, a maximizing representation is `pututupuututttut`.
Deleting position 12 gives `pututupuututtut` and y=0x37b27c87 in
O_(p,15), congruent to x modulo 64. Its exact difference valuation is 8.
The same x has 216 labelled representations, despite only 38 reachable
nodes in the inverse graph. The complete graph has 243 nodes including
dead branches, 726 inverse attempts, and 338 exact nonnegative rejections.
No all-representation graph was needed or computed for the first state.

There are 142 comparisons on all 28 noninitial deletions of the original
two words, at m=1,...,2c+2. The primary also checks six moduli for the
second state's maximizing deletion. All pass. These successes do not prove
the universal selection conjecture. They do refute using failure of the
chosen p16 representation as evidence of failure over all representations.

The lead's independent signed-bit inverse and bottom-up graph computation
agrees with every chosen deletion, all 243 graph nodes, their root
reachability, representation counts, and maxima. The exact node comparison
is recorded with the primary integration; no frontier enumeration is used.

## Follow-up admission: discriminate depth dependence

Both initial named states have deletion witnesses, but the p16 witness
requires changing representation. Before attempting an all-depth selection
proof, test the specific already documented deeper occurrence
u/k18/0x6473d46ab/cut4/w=tttt/gaps222, from
`problem1_return_valuation_falsification.md`, with original word
`uutuuttuupupuuupup`. The required valuation is 9 instead of 3 or 5.
This directly tests whether the proposed selection survives increasing
cut depth on an existing exact certificate, not a census or an enlarged
frontier box. Apply the same chosen-word check and, only if that word
fails, the exact all-representation DAG. Stop after this one named input,
regardless of outcome. Preserve the first two records as a separate pass.
An all-representation failure refutes the universal deletion construction;
success leaves a precisely quantified selection conjecture, not a proof.
The same one-CPU/120-second/1-GiB and independent-replay requirements apply.

Diagnostic admission after the deeper result: the 20 root-reaching nodes
suggest the exact representation language
`u A t u A t t u D D A u A p A p`, with A={u,p} and
D={tt,up,pp}. Verify this finite factorization against the saved graph
and replay its 288 words, including their T-input valuations. This is a
compact certificate for the same single endpoint, not a new input search.

## 5. Deeper occurrence refutes the universal construction (`refuted`)

The previously verified genuine occurrence is

```text
a=u, k=18, x=0x6473d46ab, c=4, w=tttt, gaps=(2,2,2).
Original generator word: uutuuttuupupuuupup.
Observed required prefix: ttttututut.
Admissibility prefix: ttttutututu (final u not required observed).
```

Its all-representation maximum is exactly

```text
H_u(18,0x6473d46ab)=3 < 2c+1=9.                 (4)
```

Thus NO noninitial single deletion in ANY ordinary representation of x
preserves its required residue modulo 1024. This is the same genuine
occurrence used to certify an ancestor in the earlier valuation work;
it is not merely an ordinary frontier example without return constraints.
The old signed-count valuation conjecture and the present generator-input
valuation criterion are different statements. The exact criterion (1)
remains true; it is existence of a sufficiently divisible T-input that fails.

The complete predecessor certificate contains 140 nodes, of which 20 are
root-reaching, with 417 inverse attempts and 196 exact nonnegative inverse
rejections. Both implementations agree on every node's reachability,
representation count and H, and every inverse verdict. There are exactly
288 labelled ordinary representations of this endpoint.

They have the compact exact language

```text
A = {u,p}, D = {tt,up,pp},
all words = u A t u A t t u D D A u A p A p.     (5)
```

The blocks occupy fixed positions, so this contains 2^5 * 3^2 = 288
distinct length-18 words. Every one replays to x; this cardinality equals
the independently certified total representation count. Hence no words
are omitted. Their possible noninitial T-inputs are exactly

| T-input | Valuation |
| --- | --- |
| 0x6 | 1 |
| 0x1b8 | 3 |
| 0x648 | 3 |
| 0x6409 | 0 |
| 0x1bc3f | 0 |
| 0x644c1 | 0 |
| 0x1bdf47 | 0 |

Every word contains the two valuation-3 inputs, so its own maximum is
already 3. Thus (4) is not a poor choice of representation. For example,
`uutuuttuttttuuupup` attains the maximum; deleting position 6 gives
`uutuututtttuuupup`, with y=0x1bcd3a49b. Its difference from x has
valuation 4, which fails the required valuation 10 for equality modulo
1024. All other deletions fail too by the exact criterion.

Finite verification covers all 17 deletions of the original word at the
10 moduli m=1,...,10 (170 checks); the primary also checks those 10
moduli for the maximizing deletion. The independent check verifies the
exact difference valuation, as well as the 288-word factorization and all
its T-input values. There is no claim of minimality among all occurrences:
this is the single preselected deeper endpoint, not a search for the first
counterexample in a larger box.

## 6. Verification and reproducibility

Muse Spark 1.3 Contributor independently derived the deletion criterion,
confirmed the phase-gated all-representation recurrence after a requested
scope clarification, and checked the conditional c<=k-4 proof, including
small k. Its review was tool-free; it did not execute the finite checks.
Default contributor Dewey implemented the two bounded passes using exact
partial nonnegative inverses, and supplied all predecessor certificates.
The lead reviewed that code and independently replayed with signed-bit
inverses, cell-array forward generators, and bottom-up reachability/maxima.
Fresh reviewer Ramanujan accepted the full proof scope and the factorization
completeness argument, emphasizing its dependence on the exact DAG count.
Its portability correction is incorporated: comparison scripts resolve the
dependency within the replay checkout while retaining the original absolute
path as provenance.

Atomic standard-protocol records are

- `results/problem1/20260905_generator_deletion_primary.json`
- `results/problem1/20260905_generator_deletion_independent.json`
- `results/problem1/20260905_generator_deletion_deep_primary.json`
- `results/problem1/20260905_generator_deletion_deep_independent.json`

Each retains the full Git base, exact named inputs and modulus range,
timings, hardware/software, source hashes and executed source. The primary
records retain the exact dependency source and complete inverse diagnostics;
their `result_summary` is the original raw-data object, so no temporary
raw-data file is needed. Integration fields contain the independent
node-by-node comparison and its source. The independent records contain
their input hashes and complete graphs; the deeper one also records (5).

For independent replay, extract the appropriate `source_text` to a Python
file outside the repository and run Python 3 from the repository root,
or set RULE30_REPLAY_ROOT. Inputs are the committed conjugated-projection
record for the first pass and the earlier valuation note for the second.
The script atomically regenerates its own result, including current
timestamp, commit and timing; integration comparisons can then be rerun
from their embedded source. No original temporary-directory data is needed.

## 7. What remains open

Single deletion is a strictly stronger certificate than existence of any
lower-frontier shadow. Its failure here does not refute adjacent inclusion,
dominant nonemptiness, signed nonvanishing, or B_all. In particular, the
known occurrence still has positive signed mass 2, and its cut 4 is well
below either proposed boundary. General eventual periods >=3 remain open.

The next distinct representation route is a shorter contiguous block
replacement, allowing changes that a single deletion forbids. It should
first face the same exact 288-word counterexample family, with a specified
block class and exact residue comparison. No such block-rewrite check has
been run here. An all-depth shortening rule would still be required;
success on this endpoint would not supply it. Return-conditioned endpoint
correlations remain the other main structural route.
