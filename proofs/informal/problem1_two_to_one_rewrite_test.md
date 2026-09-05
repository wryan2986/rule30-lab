# Two generators replaced by one

Status: exact all-depth classification and conditional proper-prefix bound
are `partial-proof`. The universal two-to-one shadow construction is
`refuted` on a genuine occurrence. Fixed-input checks are `finite-exhaustive`.
Adjacent inclusion, B_all, signed nonvanishing, and Problem 1 remain open.

## Bottleneck, ranking, and admission

The single-deletion construction fails on the genuine occurrence
u/k18/x=0x6473d46ab/cut4, w=tttt, gaps222. Every representation has
maximum T-input valuation 3, below the required 9. The desired adjacent
shadow still means a lower ordinary state congruent to x modulo 1024.

| Rank | Route | Plausibility / all-depth potential | Falsifiability / cost |
| --- | --- | --- | --- |
| 1 | Replace two adjacent noninitial generators by one | Changes a letter as well as length; a universal selection rule would suffice | High / low on the existing exact word family |
| 2 | An all-depth bound on how far a shortening must change a representation | Could identify a structural obstruction or a necessary nonlocal mechanism | High once a width theorem is stated / medium |
| 3 | Return-conditioned endpoint correlations | Direct nonvanishing route; still lacks a closed invariant | Medium until specified / high |

This ranking is `heuristic`. Increasing rewrite width is not automatically
authorized by failure of the first route.

Write AB for applying A first, B second. For positive prefix v, let
alpha=v2(v)+1 and beta=v2(U(v))+1. Set gamma=beta for odd v and 2 for
even v; delta=1 for odd v and 2 for even v. Proposed exact table for
v2(B(A(v))-C(v)), where C is the replacement generator:

| AB | C=T | C=U | C=P |
| --- | --- | --- | --- |
| TT | alpha | 0 | 0 |
| TU | 0 | alpha | 1 |
| TP | 0 | 1 | alpha |
| UT | 0 | beta | gamma |
| PT | 0 | gamma | beta |
| UU | beta | 0 | 0 |
| UP | 1 | 0 | 0 |
| PU | gamma | 0 | 0 |
| PP | delta | 0 | 0 |

The common suffix is an isometry, so the same valuation should equal the
full-output difference. In particular, for m>=3 a successful replacement
modulo 2^m requires a prefix before or inside that two-letter block to
be divisible by 2^(m-1). For A=P, note v2(P(v))=v2(U(v)). This necessity
is stronger than the finite claim, and needs proof plus independent review.

Admitted input: exactly the already certified 288 length-18 representations
of this one endpoint, from the committed generator-deletion deep record:

```text
A={u,p}, D={tt,up,pp},
u A t u A t t u D D A u A p A p.
```

Check every adjacent pair starting at one-based positions 2,...,17, and
each replacement in {T,U,P}: 288*16*3=13824 labelled rewrites. Preserve
the initial phase letter. Replay the entire shortened word; check the
proposed local valuation against the local and full-output differences,
and direct congruence at m=1,...,10. Record a maximizing rewrite and every
distinct local (prefix,pair,replacement) case, with aggregated counts rather
than thousands of redundant word traces. Also measure all proper-prefix
valuations over this same word set to test the claimed barrier. Do not
enumerate other frontiers, occurrences, or larger replacement blocks.

A failure of the table changes the proposed all-depth classification.
If every rewrite fails the target modulus, this refutes the universal
two-to-one certificate class on a genuine occurrence, not adjacent inclusion.
A successful rewrite would isolate a new selection mechanism still needing
proof. Either outcome stops this finite pass without increasing the box.
One local CPU, 120 seconds, 1 GiB; atomic standard-protocol JSON with full
Git base, exact parameters, source/input hashes, hardware/software, timings,
limits, and independently reviewable local cases. Independent implementation
and Muse's mathematical review precede adoption of any all-depth result.

Small-case diagnostic admission: the named word family omits TP with an
even block input. Check the full 27-entry table also at v=1 and v=2,
the smallest positive odd and even inputs (54 local comparisons), to cover
that parity seam without an occurrence or frontier search. These are
auxiliary finite table tests, distinct from the 13824 named rewrites.

## 1. Exact local classification (`partial-proof`)

The table above holds for every positive integer v. Positivity ensures
that a two-generator output has bit length two greater than a one-generator
output, so the difference is never zero. All valuations are therefore finite.
The first-difference argument also shows that common bitwise XOR by any
constant preserves difference valuation, just as a common generator suffix
does.

Put z=U(v), and let e=2 for even v and 0 for odd v. Then

```text
P(v)=z XOR e, T(v)=z XOR 1,
v2(P(v))=v2(U(v)),
v2(T(s)-s)=v2(s)+1 for every s>0.                (1)
```

The first 14 zero entries follow from parity: T preserves it, while U and
P flip it. The other entries split into the following exact cases.

- TT/T, TU/U and TP/P have a common final map, so their valuations are
  alpha by isometry and (1).
- TU/P and TP/U have valuation 1. If v is odd, e=0 and the common-map
  difference already has alpha=1. If v is even, alpha>=2 but the extra
  XOR by 2 changes bit 1 and no lower bit.
- UT/U and PT/P are T(s) versus s at s=U(v) or P(v), giving beta.
- UT/P and PT/U give gamma. For odd v, U(v)=P(v) and the value is beta.
  For even v, the relevant s is odd and the comparison is T(s) versus
  s XOR 2. For ANY odd s, (T(s) XOR s) modulo 8 equals 6; the extra
  XOR by 2 leaves 4, giving valuation exactly 2.
- UU/T becomes T(z) versus z after common XOR by 1, giving beta.
- UP/T becomes T(z) versus z XOR (2 if z is even else 0). For odd z,
  its value is 1 by (1); for even z, the extra XOR by 2 creates a
  bit-1 difference, also giving 1.
- PU/T becomes T(P(v)) versus U(v) after common XOR by 1, the same
  comparison as PT/U, giving gamma.
- PP/T gives 1 for odd v by the UP/T calculation, since P(v)=U(v).
  For even v, P(v) is odd, so the comparison reduces to PU/T and has
  value 2. This is delta.

These exhaust all 27 entries without extrapolating finite data. The
generators and suffix isometry are the established ones in
`problem1_generator_deletion_test.md`.

## 2. Proper-prefix valuation barrier (`partial-proof`)

Let a fixed-phase representation have length k>=3. Replace its generators
at positions i,i+1 by one generator, where 2<=i<=k-1. The input v is
its positive prefix state at level i-1; the state A(v) inside the block
is its proper prefix at level i. Both precede the final output.

For m>=3, constants 0,1,2 in the table cannot preserve the residue modulo
2^m. A surviving alpha entry requires v2(v)>=m-1. A surviving beta or
odd-gamma entry requires v2(U(v))>=m-1 and has A=U or P. By (1), this
is the valuation of the actual intermediate prefix A(v), even for A=P.
Consequently a successful rewrite requires one of these actual prefix
states to be divisible by 2^(m-1).

More generally, let H bound valuations of all positive proper-prefix
states in every representation of a specified endpoint from its fixed
phase root. Then every such two-to-one rewrite has full-output difference
valuation at most

```text
max(H+1,2).                                     (2)
```

Indeed alpha, beta, and odd-gamma entries are at most H+1; all remaining
entries are at most 2. The common suffix preserves this exact difference valuation.
This is a conditional all-depth bound, not an assertion that H is uniformly
bounded on genuine occurrences. It uses only root-reaching representations;
unreachable inverse predecessors cannot contribute prefix values.

The initial pair is a separate root case, since its input would be zero.
Keeping the phase requires replacing it by the initial phase letter a.
At the phase-u root 1 the second generator produces 7 or 6, differing
from 1 with valuation 1 or 0. At the phase-p root 3 it produces 13 or
12, differing from 3 with valuation 1 or 0. A common suffix preserves
these values. Thus an initial-pair replacement cannot preserve even the
required modulo-4 root cylinder, at any cut c>=0. This root argument
does not apply the positive-input table to zero.

## 3. Exact obstruction on the genuine occurrence (`refuted`)

For x=0x6473d46ab in O_(u,18), cut4, w=tttt, gaps222, all 288
representations have their proper-prefix states among the 19 states below
(the common endpoint is excluded):

```text
1, 6, 1a, 67, 1b8, 648, 1bf8, 6409, 1bc3e, 1bc3f,
644c1, 1bdf46, 1bdf47, 6420d9, 1bce32e, 6472dd3,
1bd9d23c, 642e3ec7, 1bcd2c158.                    (hexadecimal)
```

Their maximum valuation is exactly 3. Completeness is supplied by the
previously verified representation graph and is independently replayed
here from both the graph and its exact word factorization. Applying (2)
gives an upper bound of 4 on the difference valuation of every noninitial
two-to-one rewrite. The target cylinder requires valuation at least 10,
since c=4. The initial-pair case is excluded by the separate root argument.
Therefore no phase-preserving replacement of two adjacent generators by
one can construct this occurrence's adjacent shadow, in ANY representation.

For example, the maximizing rewrite in the recorded order is

```text
original word: uptupttupppppupppp,
replace PT by U at position 5, with prefix v=0x67,
short word:    uptuutupppppupppp,
y=0x1bcd3a49b in O_(u,17), v2(x-y)=4.
x mod1024=683, y mod1024=155.
```

It agrees modulo 16 but already fails modulo 32. Every one of the
13824 labelled noninitial rewrites fails modulo 32 and hence modulo 1024.
This is a finite exact counterexample to a universal certificate class,
not a claim that a different lower-frontier shadow is absent.

## 4. Finite checks and independent review

The fixed 288-word, 16-position, three-replacement box has

| Full-output difference valuation | Labelled rewrites |
| --- | --- |
| 0 | 7744 |
| 1 | 3008 |
| 2 | 1920 |
| 4 | 1152 |

All 138240 direct congruence comparisons at m=1,...,10 agree with the
local table and suffix-isometry prediction. The box has 114 distinct
local (prefix,pair,replacement) cases and 19 distinct proper-prefix states.
These counts refer to labelled rewrites, not distinct resulting states.
All nine pair types occur, covering 17 of the 18 pair/parity contexts;
only TP with an even prefix is absent from the named word family.
The separate 54 local checks at v=1,2 cover all parity contexts and pass.
These finite checks do not replace the all-depth proof in Section 1.

Muse Spark 1.3 Contributor independently derived all 27 entries and the
conditional bound without tools. Dewey implemented the bounded packed-
generator check and the separate smallest-parity diagnostic. The lead
independently used cell-array T, the odd-section definition of P, and
word reconstruction from the certified predecessor graph. The complete
ordered stream of 13824 shortened words, values, and valuations has the
same SHA-256 in both implementations. Every local case, multiplicity,
proper-prefix value, valuation histogram, maximum, and auxiliary case
also agrees individually.

Fresh reviewer Ramanujan accepted the all-depth proof and conditional
scope. Its corrections are incorporated: odd-gamma entries belong in the
H+1 bound, and JSON object keys must be normalized before canonical hashing.
The independent source was corrected and rerun; the primary record retains
the original executed source and the separate normalization source and
hashes. These were proof-wording and serialization corrections, with no
change to the mathematical results.

Atomic standard-protocol records:

- `results/problem1/20260905_two_to_one_primary.json`
- `results/problem1/20260905_two_to_one_independent.json`

They retain exact input scope, full Git base, timings, hardware/software,
source/input hashes, and executed sources. The primary records its separate
54-case diagnostic and hash-normalization provenance; `result_summary`
contains the complete raw-data object. Integration fields contain the
independent comparison and its source. Historical temporary paths identify
the original execution; they are not dependencies of independent replay.

For portable replay, extract the independent `source_text` to a Python
file outside the repository and run it from the checkout root, or set
RULE30_REPLAY_ROOT. It reads only the committed deep deletion certificate
and atomically regenerates its result. The embedded integration comparison
is likewise runnable from that checkout. Timestamps, commit and timings
change on replay; the named mathematical scope does not.

## 5. Remaining research direction

Arbitrary exact re-expression of the original generator word cannot evade
this obstruction, since all representations of the endpoint were covered.
Longer block replacements and changes preserving only the residue rather
than the exact endpoint are different constructions and remain untested.
Neither the table nor this counterexample excludes arbitrary adjacent
shadows, signed nonvanishing, or B_all. The genuine occurrence still has
signed mass 2. General eventual center periods >=3 remain unhandled.

No automatic increase to three-to-two rewriting follows. The stronger next
structural question is whether the full return-conditioned endpoint transfer
has a useful operator or Walsh description, retaining deduplication and
joint endpoint correlations. The universal five-vector closure counterexample,
scalar/sign-only failures, and refuted v2(N)!=v2(2O) gate must retain their
exact scopes; they do not rule out every return-conditioned invariant.
Small-residue permutation parity is a possible quantity to
examine, but no bridge from it to the signed mass is established here.
