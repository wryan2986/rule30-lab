# Exact endpoint operators and the affine Walsh-sign test

Status: affine Walsh-sign reduction `refuted` on a genuine return belief.
The operator and plane-restriction results are `partial-proof`; named
endpoint reconstruction and certificate checks are `finite-exhaustive`.
Signed nonvanishing, B_all, and Problem 1 remain open.

## Bottleneck and route selection

The required nonvanishing is one signed sum over distinct dominant endpoints
on genuine return occurrences. The five signed slices have no universal
closed update; exact transfer uses their joint endpoint correlations. A
Walsh reformulation must retain those correlations and cannot turn Parseval
or a nonzero vector norm into nonvanishing of one particular coefficient.

| Rank | Route | Plausibility / all-depth potential | Falsifiability / cost |
| --- | --- | --- | --- |
| 1 | Exact endpoint operator, with an affine Walsh-character reduction of defect signs | A concrete possible simplification, still needing a nonzero-coefficient theorem | High / low on one stored genuine belief |
| 2 | Higher-order joint defect-signature coefficients | Retains correlations; a constrained spectral family could give an invariant | Medium until a precise constraint is proposed / medium-high |
| 3 | Small-residue generator-permutation parity | A global character may exist, but no endpoint-restriction bridge is known | High for the bridge / uncertain cost |

The ranking is `heuristic`. No character reduction is assumed. A sign
character alone would NOT establish signed nonvanishing of its support.

## Precise candidate and admission

For a concrete belief B, ask whether there exist a binary vector a and
b in GF(2), chosen separately for this entire belief, such that

```text
cost(y) = b + dot(a,bits(y)) modulo 2, for every y in B.     (1)
```

This allows every affine Walsh character, not just endpoint parity or a
fixed character shared across phases/depths. Removing the common low
cylinder digits or making an invertible affine change of binary coordinates
does not change existence of such a representation.

Admitted input: only the already certified belief at
u/k14/x=0x642fdfb/L2/cut1/gaps222, with 134 distinct endpoints,
84 even and 50 odd defects. Read its complete endpoint/cost table from
the committed pairing record or its exact previously verified oracle if
the record does not contain that table. No new occurrence census.

Search the endpoints in increasing numerical order for the lexicographically
first a<b<c<d with a XOR b XOR c XOR d=0 and odd sum of defect parities.
Such a quadruple refutes (1): any affine character has even total parity
on these four points. Four is the smallest possible cardinality of a
distinct-point affine inconsistency certificate, since two distinct points
cannot XOR to zero and an odd number does not cancel the affine constant.
If no quadruple exists, solve the full affine linear system over GF(2),
retaining either a verified character or an exact inconsistency combination.
Do not infer consistency merely from absence of four-point witnesses.

A failure excludes one-frequency sign modulation even for a state-dependent
character and therefore requires genuine Walsh-mode mixing. Success is only
a finite character identity and still leaves its signed sum unexplained.
Either outcome stops after this named belief, without a larger box.
One local CPU, 120 seconds, 1 GiB; atomic standard-protocol JSON with full
Git base, exact input/source hashes, hardware/software, timings, limits,
full certificate and independently verified endpoint provenance.

Input clarification before reconstruction: the pairing record retains counts
and an isolated-vertex subset, not the full 134-point table. It is therefore
necessary to reconstruct this one named belief. The existing exact oracle
may materialize its phase-u carrier frontiers through level 13, solely to
evaluate the named current/shadow fibers; do not enumerate other cylinders
or occurrences. Alternatively, enumerate projected seeds through level 11
and use exact recursive membership for their two possible common lifts.
Record which method was used. This is a bounded evaluation of the stated
sign hypothesis, not a new frontier census or a larger search box.

Before adoption, Muse must independently review the affine obstruction and
the proposed operator formulas; the lead independently checks the concrete
certificate. A potential follow-up corollary is that every Boolean sign
extension of a non-affine belief requires at least four Walsh frequencies,
since Boolean functions cannot have Walsh support of size two or three.
That corollary needs its own short proof; it is not inferred from a census.

If a quadruple is found, also retain its current/shadow mask sequences and
the depth positions with an odd number of proper shadow masks across the
four endpoints. At each such position, verify the projected four-point
plane and its four local signed Walsh sums. This diagnoses the same exact
certificate and adds no endpoints or occurrence inputs.

## 1. Exact endpoint operator (`partial-proof`)

Use the joint-transfer conventions: parent (a,h,D,q), child
(a,h+1,D+1,4q+d), and m=M_(a,h)(q), with d in m. A parent
endpoint p has outgoing mask n(p)=M_(a,h-1)(p). On an ambient b-bit
space large enough to contain the parent endpoints, set

```text
f(p)=(-1)^cost(p) for p in the parent belief, 0 otherwise,
a_m(p)=epsilon_m(n(p)).
```

Outside the relevant ordinary frontier the multiplier can be set to zero;
its values outside the support of f do not affect the child. The exact
concrete recursion is

```text
F(4p+d)=a_m(p) f(p), F(z)=0 at the other low digits.         (2)
```

The digit embedding is injective. There is no sum over alternative
generator representations and no merging of distinct endpoints. As a
matrix this is E_d D_m, where E_d embeds coordinate p at 4p+d and D_m
is diagonal with entries 0,+1,-1. Its squared norm is

```text
||F||_2^2 = sum_p |a_m(p)f(p)|^2,
```

the number of surviving dominant endpoints. This can be nonzero when the
signed mass sum_z F(z) is zero; the known ordinary cancellation at p/k6/
0xc84/L2 has two surviving endpoints and signed mass zero. That example
is not claimed to be a genuine return occurrence.

At depth one, the same filter-and-embedding formula initializes the belief
from its unsigned projected seed carrier, with initial weights 1. It does
not require defining a positive-depth parent belief at depth zero. This
includes the local seed filter identified in Section 4 below.

For the unnormalized Walsh transform

```text
W_b f(xi)=sum_(p in {0,1}^b) f(p)(-1)^dot(xi,p),
```

the bit splitting and product identities give exactly

```text
W_(b+2) F(4xi+eta) = (-1)^dot(eta,d) W_b(a_m f)(xi),
W_b(a_m f)(xi) = 2^(-b) sum_zeta W_b a_m(xi XOR zeta) W_b f(zeta),
                                                        0<=eta<4. (3)
```

Proof: substitute z=4p+d in the first sum and split its binary dot
product into high and low parts. For the second identity, substitute the
inverse Walsh expansion of a_m and use character multiplication. The
coefficient at xi=eta=0 is precisely the signed child mass, not the norm.
Thus Parseval does not establish its nonvanishing. Formula (3) is an exact
operator representation, not a new proof that the mass is nonzero.

## 2. Affine obstruction and spectral consequence (`partial-proof`)

For four distinct points y_1,...,y_4 with XOR sum zero, every affine
L(y)=b+dot(a,y) satisfies

```text
sum_i L(y_i)=4b+dot(a, XOR_i y_i)=0 in GF(2).                (4)
```

An odd sum of their recorded defect parities therefore refutes (1), even
when a,b can depend on the full cylinder. This obstruction survives an
invertible affine change of coordinates. It also survives removing the
common low cylinder digits, since those are constant and are absorbed by b.
Four is minimal cardinality for a distinct-point affine inconsistency:
the augmented rows (1,bits(y)) for at most three distinct binary points
are linearly independent; a two-row dependence would repeat a point, and
an odd-row dependence cannot cancel the leading ones.

Consequently, if such a quadruple occurs in B, its signed endpoint function
f cannot have its ENTIRE Walsh spectrum equal to plus or minus a single
frequency translate of W 1_B. Walsh inversion would imply
f=plus-or-minus chi_a 1_B, contradicting (4). This does not exclude an
accidental equality of one scalar signed mass with an unsigned Walsh
coefficient, and it does not refute nonlinear or multimode operators.

There is a sharper extension statement. Any everywhere-Boolean sign
function s:{0,1}^b->{-1,+1} agreeing with the belief signs then has at
least four nonzero Walsh coefficients. A one-frequency Boolean function
is plus or minus a character. A two- or three-frequency expansion cannot
square to 1: each pair of distinct support frequencies produces a distinct
nonzero XOR frequency with coefficient twice the product of their nonzero
coefficients, so no cross term can cancel. This argument includes the
constant frequency. This squaring argument alone applies only to Boolean
sign extensions, not the zero-extended endpoint function. The stronger
restriction argument below also handles zero extensions.

## 3. Four-mode restriction and a local filter witness (`partial-proof`)

Four distinct XOR-zero points form the entire affine plane

```text
y_0+s v+t w, (s,t) in GF(2)^2,
v=y_0 XOR y_1, w=y_0 XOR y_2.
```

The directions are nonzero and distinct, hence linearly independent.
If the product of the four signs is -1, all four unnormalized Walsh
coefficients of this two-dimensional restriction are +2 or -2. Indeed
multiplication by any plane character preserves the product of the signs;
four signs with product -1 have an odd number of negatives and sum to +2
or -2.

Any ambient character restricts to a constant sign times the plane
character indexed by (dot(a,v),dot(a,w)). By Walsh inversion, each plane
coefficient is a linear combination only of ambient coefficients in that
frequency class. All four plane coefficients are nonzero, so each of the
four classes contains a nonzero ambient coefficient. Therefore EVERY
real-valued extension of the four signs has at least four Walsh modes,
including the zero-extended signed endpoint function. The same argument
works in affine coordinates on the affine span of B, without relying on
the cylinder's fixed binary coordinates to inflate the ambient spectrum.

There is also an exact local consequence. The endpoint cost is the sum
over depths j=0,...,L-1 of the proper-shadow-mask indicators. An odd total
cost across the quadruple implies that at least one depth has an odd
number of proper shadow masks. At that depth, project the four points to

```text
p_i = y_i >> (2j+2).
```

They remain distinct and have XOR zero: all endpoints share their low
2L bits, so removal of at most those bits loses no distinguishing
information. Dominance holds for all four, and the local filter values
epsilon_(m_j)(n_j(p_i)) have product -1. The local filter itself therefore
has all four Walsh modes on this plane. A single-character description
fails at an actual return-conditioned local filter, not only for the
cumulative endpoint signs. None of these restriction statements determines
the global signed mass or proves its nonvanishing.
In particular a nonzero ambient coefficient in the plane's (0,0) class
need not be the ambient zero-frequency coefficient.

## 4. Exact genuine-domain certificate (`refuted`)

The complete named belief is

```text
B=B_u(14,2,0x642fdfb), cut1, gaps222, base word t.
Observed required prefix: tututut.
Final-u admissibility word: tutututu.
Current mask sequence, low to high: (1111,1100).
```

The original endpoint has the generator witness `uuuuputptuutuu` from
zero. The 134 distinct dominant shadow endpoints have 84 costs equal to
zero and 50 equal to one, so their signed mass is 34. Among them are

| Endpoint y | Cost | Shadow masks, low to high | Generator witness from zero |
| --- | --- | --- | --- |
| 0x190822b | 0 | (1111,1111) | `utuuuuuputttp` |
| 0x190825b | 1 | (1111,1100) | `utuuutuutpuut` |
| 0x191c10b | 0 | (1111,1111) | `uupuuuttputtp` |
| 0x191c17b | 0 | (1111,1111) | `uupuuutputuuu` |

Every word has length 13 and replays to its listed endpoint. Exact
recursive membership verifies every fiber in the table and its dominance.
All endpoints agree with x modulo 16. The XOR of the first two equals
the XOR of the last two, namely 0x70, while their cost sum is 1.
Equation (4) therefore excludes EVERY affine character, even one chosen
specifically for this single belief. This is a genuine occurrence, not
merely an ordinary-cylinder or abstract-mask counterexample.

The precise nonlinear filter is at j=1. Its four parent inputs in O_(u,11)
are y>>4:

```text
0x190822, 0x190825, 0x191c10, 0x191c17.
```

Take the first as origin and the directions v=0x7, w=0x1432. The
current mask is 1100. On the four points in order 00,10,01,11 the shadow
masks are (1111,1100,1111,1111), and the local signs are

| Plane coordinate t | s=0 | s=1 |
| --- | --- | --- |
| 0 | +1 | -1 |
| 1 | +1 | +1 |

The unnormalized Walsh coefficients in frequency order 00,10,01,11 are

```text
(2,2,-2,2).                                                (5)
```

Equivalently the local sign on this plane is
`(1+chi_s-chi_t+chi_s chi_t)/2`. Thus the local return-conditioned
filter has all four plane frequencies; it cannot be a single-character
multiplier. At j=0 the same four endpoints encounter the full current
mask, all four shadow masks are full, and the local restriction is
constant +1, with Walsh coefficients (4,0,0,0). The nonlinear signs
survive this final filter unchanged.

The signed sum of these four points alone is 2. That does not prove the
whole belief nonzero: the remaining endpoints must still be included.
The full mass 34 is a separately verified finite value, not an all-depth
consequence of the plane.

## 5. Verification and provenance

The primary sorted-triple search stopped after 174 probes, having seen
21 ordered XOR-zero candidates. It found the lexicographically smallest
contradictory quadruple in this named belief. The independent search
instead grouped all 8911 unordered endpoint pairs by XOR and defect
parity and found the same minimum. This is numerical minimality within
the specified complete belief. Four-point cardinality minimality is the
general affine-independence argument in Section 2, not a wider census.

The pairing archive contained counts and an isolated-vertex subset rather
than the full endpoint table. Dewey reconstructed the single named belief
with the existing Boolean oracle's phase-u carrier through level 13;
the current level-14 mask used only exact recursive membership queries.
The lead independently generated only projected seeds through level 11,
then used recursive lifts to decide both dominance stages, checking every
endpoint with a generator witness replayed by cell-array T and P's odd
section. All 134 endpoints, exact costs, masks, and totals agree.
This is a named-belief evaluation, not a new occurrence census. No ambient
Fourier array was constructed; only the four-point restrictions were summed.

Muse Spark 1.3 Contributor independently reviewed the affine obstruction,
minimality, operator formulas, and four-mode restriction theorem without
tools, including its stronger applicability to real or zero extensions.
It also reviewed the concrete XOR and local plane calculation. The lead
retains responsibility for the interpretation and the nonvanishing boundary.

Fresh reviewer Ramanujan approved the completed note, including the unsigned
seed initialization and the distinction between four-mode necessity and
nonvanishing. Its read-only verification checked source, summary, input,
dependency and integration hashes, all 134 endpoint rows, both local plane
restrictions, and checkout-relative replay paths. No new experiment was
needed for that review.

Atomic standard-protocol records are

- `results/problem1/20260905_walsh_sign_primary.json`
- `results/problem1/20260905_walsh_sign_independent.json`

They contain the full base Git commit, exact scope, source and input hashes,
timings, hardware/software, complete endpoint tables and certificate.
The primary embeds its two oracle sources and detailed recursive mask
traces for the quartet. The independent record embeds its recursive
membership dependency and all 134 endpoint witnesses. Integration fields
contain the exact table comparison and its source. No temporary raw-data
file is required to inspect the committed result.

For independent replay, extract `source_text` to a Python file outside
the repository and run it from the checkout root, or set RULE30_REPLAY_ROOT.
It reads the committed pairing archive and membership helper and atomically
regenerates its result. The embedded integration comparison also resolves
dependencies relative to the replay checkout. Timestamps, commit and
timings change on replay; the named mathematical scope does not.

## 6. Remaining bottleneck

The exact transfer is still a convolution on the full endpoint spectrum.
The new counterexample excludes treating its signs as a single Walsh
character, even locally on the displayed actual filter. It does not
exclude general Walsh methods, nonlinear observables, or return-conditioned
families of multimode operators. The four-mode lower bound is NOT a
four-mode closure theorem. The universal five-vector closure counterexample
also retains its original scope; it was not proved on every return ancestor.

An all-depth proof still needs a constraint on the actual joint coefficients
that prevents their contribution at zero frequency from cancelling. No
bridge from generator-permutation parity is established here, and the norm
identities do not control that individual coefficient.
Adjacent inclusion, B_all, and general eventual periods remain open.
The next useful step must specify such a correlation constraint or a new
boundary mechanism before further computation; simply raising the Fourier
mode cap or fitting higher-degree signs to this table would not suffice.
