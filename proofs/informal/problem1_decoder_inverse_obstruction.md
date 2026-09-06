# Exact inverse arithmetic and a failed decoder-predecessor induction

Status: `partial-proof` for the universal inverse classification and
core-head positivity lemma; `refuted` for the stated leading-core
backward-closure claim; `finite-exhaustive` for the declared probes.
The decoder-based return exclusion itself remains `inconclusive`.
Base checkpoint: `5c7876850621bf37a6bef191fa2bab8dbb100397`.
Problem 1 remains open.

## Bottleneck, routes and admitted tests

The periodic-core overlap theorem determines at most one ordinary
endpoint from phase, initial complexity and a long observed branch
prefix. It does not prove the candidate ordinary. The outstanding task
is to couple full membership to the canonical return word.

Ranked routes (`heuristic`):

1. Test exclusion on the larger leading-core decoder family. It is a
   concrete, highly falsifiable relaxation, inexpensive at the existing
   decoder thresholds. Survival would leave a structural candidate;
   failure would force retention of more membership information.
2. Reduce a decoded candidate to a smaller one by an admissible forced
   predecessor. If an appropriate all-depth closure held, induction
   would become possible. Its plausibility is uncertain and exact
   inverse arithmetic makes it cheap to falsify before a long proof.
3. Use the full ordinary-generator predecessor recurrence. It is exact,
   but no closed finite-state recurrence for the joint long-branch
   condition has been established. Higher expected research cost.

For route1 admit precisely r=11 observed branches: phase p,k19 and
phase u,k18. Enumerate all admissible branch words of that length by
exact cylinders; decode using the already stored level8 cores. Check
each accepted candidate through k+14 branches or the first undefined
gate/forbidden factor. Seek canonical three-return occurrences at
c>=k-6 in p or c>=k-7 in u. No ordinary membership is assumed.
This is a fixed decoder-language test, not a frontier census or an
all-k boundary proof.

After no such return appeared, test route2 on the SAME candidates and
their two exact forced predecessors. The first failures are at the
decoder base levels, whose parents need not yet have stabilized heads.
To distinguish that base exception from an interior obstruction, admit
only the two one-letter extensions of the first named phase-p word,
not a full r12 scan. Check the resulting named interior candidate for
ordinary membership separately; no inference from its leading core is
permitted.

The new inverse-positivity lemma is tested on the eight existing core
heads and all four incoming inverse-bit states, a complete32-case
finite transfer table. Local runs use CPU120seconds,1GiB, atomic JSON,
full Git/source/input hashes, hardware/software facts and timings.

## Universal inverse trichotomy (`partial-proof`, all inputs)

Use T(v)=v XOR((v<<1) OR(v<<2)), U(v)=T(v) XOR1 and
P(v)=T(v) XOR1 XOR(2 if v is even else0), interpreted in Z_2.
These are unit-triangular bijections on Z_2. For an integer z, the
unique T-inverse has bits

    v_i=z_i XOR(v_(i-1) OR v_(i-2)),  v_(-1)=v_(-2)=0. (1)

Let the inverse state be (a,b)=(v_(i-1),v_(i-2)), newest bit first.
The exact tail maps are:

| State | Output bit z_i=0 | Output bit z_i=1 |
| --- | --- | --- |
| 00 | 00 | 10 |
| 01 | 10 | 00 |
| 10 | 11 | 01 |
| 11 | 11 | 01 |

For z>=0, its output tail is0. Every state reaches00 or11 in at
most two steps, after which the inverse bits are constant. Thus
T^(-1)(z) is always a signed integer. For z<0 the output tail is1,
and every state enters the nonconstant cycle00->10->01->00. The
inverse bits have eventual least period3, so their rational sum has
reduced odd denominator exactly7. It cannot be an integer.

The exact reductions

    U^(-1)(z)=T^(-1)(z XOR1),
    P^(-1)(z)=T^(-1)(z XOR1 XOR(2 if z is odd else0))  (2)

follow from the parity flip of U and P. The finite low-bit corrections
preserve the sign of an integer, so the same dichotomy holds for both.
There is no exception at zero: T^(-1)(0)=0 and
U^(-1)(0)=P^(-1)(0)=-1.

Each generator sends every signed integer to a nonnegative integer:
an eventual input tail of either0 or1 gives output tail0. Combined
with the inverse result and triangular uniqueness, each restricts to a
bijection from Z onto N, where N includes0. This does not say it is a
bijection from N onto N.

For a nonnegative forced output x=3 modulo4 and q in {t,u}, define

    a=Q^(-1)(x), b=P^(-1)(a), B_q(x)=4b+3.             (3)

The branch inverse exists uniquely in Z_2, and is exactly one of:

- a nonnegative integer, if a>=0 and b>=0;
- a negative integer, if a>=0 and b<0;
- a noninteger rational with reduced denominator7, if a<0.

Indeed a is a signed integer by (1)--(2). Apply the same dichotomy
to b. In the rational case multiplication by4 and addition of3 cannot
cancel the denominator7. In the integer case4b+3 is nonnegative
exactly when b is nonnegative. The residue calculation in the established inverse
branch lemma supplies the proper gate: B_t(x)=11 mod16 and
B_u(x)=7 mod16. No ordinary membership is implied.

Small exact checks illustrating the three cases are

    B_u(27)=7,       B_t(7)=-5,
    B_t(3)=13/7,     B_u(3)=17/7.                     (4)

For example T^(-1)(-1)=-1/7 and T^(-1)(-2)=-2/7,
which follow directly by summing the period-three inverse bits.
The trichotomy is for ONE inverse forced block applied to a
nonnegative integer. It makes no denominator7 claim after arbitrarily
many inverse blocks with rational intermediate inputs.

## Two leading bytes force signed-integer predecessors

Claim status: `partial-proof`, all lower-tail lengths.
For H in {200,222}, any integer l>=2, and0<=v<2^l, put

    x=2^l H+v.

All three generator inverses T^(-1)(x), U^(-1)(x), P^(-1)(x) are
positive integers. If x=3 mod4, both forced inverses are signed
integers; the noninteger denominator7 case is absent.

Proof. Apply (1) to the arbitrary lower l output bits. Their only
effect on the remaining inverse computation is one of the four states
(a,b). Reading either byte from least to most significant sends EVERY
incoming state to00, already before the zero output tail:

| Head byte | Read order | Images of 00,01,10,11 |
| --- | --- | --- |
| 200 (11001000) | 00010011 | 00,00,00,00 |
| 222 (11011110) | 01111011 | 00,00,00,00 |

These are exact compositions of the displayed four-state maps.
Thus the inverse tail is0 regardless of the lower digits.
The corrections in (2) affect only the lowest two bits, which lie
strictly below H because l>=2, so the same transfer result applies.
Zero is impossible because the outputs here exceed every generator's
value at0. Apply (3): a is positive, so the forced inverse is an integer,
although its sign and leading head are still unrestricted.

This uses finite transfer functions as exact bases for arbitrary l;
it does not extrapolate positivity from finitely many lower tails.
It supplies no proof that the positive inverses are ordinary.

The eight level8 core heads used by the decoder all have leading byte
200 or222, so the lemma covers the entire decoder family. More strongly,
the existing aged-head theorem gives the all-depth ordinary corollary:

    p, k>=8, or u, k>=9:
    every ordinary endpoint has positive T/U/P inverses. (5)

For p use C_(p,4)={200,222}, with stabilization age4. For u use
C_(u,5)={400,401,444,445}, also with stabilization age4; shifting
one bit from these nine-bit heads gives exactly {200,222}. Both facts
are in the previously certified head data. Whenever such an ordinary
endpoint is3 mod4, its two forced predecessors are signed integers.
Their second inverse stage can still be negative, and neither positivity
nor leading-head compatibility establishes full predecessor membership.

For the decoder's notation below retain

    C_p={51292,51431,56937,57038},
    C_u={25646,25715,28468,28519}.

## Finite decoder and predecessor results

The r11 test has120 admissible words, each with one residue modulo2^24.
Decoding produces120 phase-p candidates and33 phase-u candidates.
The other u cases comprise50 missing heads and37 failures of the
full congruence check, including the extra overlap bit. All153 accepted
candidates have the declared11 actual branches. Their longest admissible
prefix lengths are11..15:123 stop at an undefined gate and30 at a
forbidden factor. No candidate has a canonical return in the tested
raw-empty layer. This is `finite-exhaustive` consistency at k19/k18,
not an all-depth exclusion or a membership result.

The same153 candidates have306 signed-integer forced predecessors.
There are241 positive and65 negative branch predecessors. Exactly122
candidates have some positive predecessor;18 have some positive
predecessor with a head in the same C8;16 also allow an admissible
prepended branch. Thus the137 failures of the combined criterion split
as31 without a positive predecessor,104 with positive predecessors but
no core head, and2 with a core head but no admissible prepend.
It would be incorrect to describe all137 simply as head failures.

The earliest failure in phase-then-integer order is p,k19,
x=0x32170146ab=215134324395, with prefix ttttututttu.
Both positive forced predecessors have head51428, outside C_p.
This base-level failure alone does not refute an induction that only
starts reducing complexities STRICTLY ABOVE k19 in p or k18 in u.

### An interior counterexample (`refuted`, exact finite witness)

Only the t extension of the named word is admissible; the u extension
ends in uu. At r12 the former decodes to

    p,k20, x=0xc8e70146ab=862869079723,
    observed prefix ttttututttut, H=51431.

Its two unique forced predecessors are

| Prior branch | Predecessor | Leading level8 block |
| --- | --- | --- |
| t | 179554548395 | 42809 |
| u | 179554548423 | 42809 |

Both are positive, have bit length38 (phase-p complexity19), and map
exactly to x under F with the displayed prior branch. The u prepend
is admissible, but neither head lies in C_p. Therefore the larger
leading-core decoder family is NOT backward-saturated even at this
interior level. The complete list of predecessors follows from the two
unique 2-adic branch inverses, not a bounded inverse search.

For an ordinary p19 predecessor the stabilized head theorem would
require membership in C_p. Thus x has no ordinary p19 forced
predecessor. The separate named membership check proves that x itself
is NOT ordinary either. Its three unique nonnegative ordinary-generator
predecessors are

    T:238857142613, U:238857142614, P:238857142616.

All have bit length38 and leading level8 block56947, outside C_p.
Every ordinary p20 history would have to end with one of these three
generators from an ordinary p19 predecessor, whose stabilized head
must lie in C_p. This gives a complete compact rejection certificate.
Thus this is NOT a counterexample to ordinary backward closure.

The initial implementation also reported a literal test
bitlen(parent)=k-1. That was an implementation-side misreading, not a
mathematical claim. The intended metric is complexity: bit length
2(k-1) in phase p and2(k-1)-1 in phase u. Re-scoring with the correct
metric leaves the16 successes and137 failures unchanged. Original
records retain that reporting mistake with this explicit correction.

## Verification and remaining obligation

Claim status: `finite-exhaustive`. The independent cell implementation
constructs the120 branch cylinders by backward modular inverses, rather
than the primary's forward lifting. It reproduces all153 decoded rows,
checks1,779 admissible trajectory steps, all306 signed predecessors,
their sign/head/admissibility partition, and the named r12 extension.
It verifies all32 full-core transfer cases, the eight leading-byte
transfers, and51 generator-inverse examples
on signed targets -8..8, with the exact four examples in (4).

For the named membership rejection, the independent check verifies the
complete three-predecessor certificate above and all10 retained negative
memo entries using the established aged-head constraints. Three explicit
ordinary generator words of length19 are positive controls; their words
are replayed independently, without repeating or claiming agreement of
the primary oracle's internal exploration counts. These are controls,
not three additional searched decoder candidates.

Records are `results/problem1/20260905_decoder_inverse_primary.json`
and `results/problem1/20260905_decoder_inverse_independent.json`.
The primary wrapper retains the four original raw JSON payloads, executed
sources and run timings; its own timing measures packaging. The portable
independent source verifies raw, source, summary and input hashes,
including links between the original temporary input records. No full
r12 atlas, larger ordinary frontier, or periodic-core extension was run.

An independent tool-free derivation accepted the inverse classification.
Fresh adversarial mathematical and four-file integration reviews accepted
the classification, leading-byte corollary, witness scope, finite
comparisons and provenance without material corrections.

The generic head-predecessor test and the two inverse branches do not
enforce full ordinary membership. The absence of boundary returns at
r11 is not promoted to an invariant. A proof still needs a relation
coupling the growing observed word to membership, or a direct return
exclusion. The known automatic advance of a leading block under A^2
does not provide backward closure: its periodic core can have transient
predecessors outside the core, as the named witness illustrates.

Next (`inconclusive`): control the second inverse sign and retain the
full membership predicate in a predecessor induction. A composed
inverse transducer might decide whether a finite leading condition
can control that sign; such a hypothesis must be stated before any
further head calculation. Alternatively find a forward invariant
separating decoded continuation states from return cylinders. Do not
increase the decoder word length merely because the first finite level
has no boundary counterexample. B_all, genuine return exclusion,
signed nonvanishing and Problem 1 remain open.
