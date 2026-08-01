# Exact residue-aware concrete shadow beliefs

Status: exact all-depth recursion for adjacent-complexity states in one survivor
cylinder, plus finite verification that every three-return occurrence through
phase complexity 25 has a nonempty concrete belief.

## 1. Concrete shadow beliefs

For phase `a`, exact phase complexity `k>=2`, a current frontier state

\[
x\in O_{a,k},
\]

and a cylinder depth `1<=L<k`, define

\[
B_{a,k,L}(x)
 =\{y\in O_{a,k-1}:y\equiv x\pmod {4^L}\}.
\]

This is the complete set of adjacent-complexity frontier states in the same
base-four survivor cylinder. Therefore

\[
B_{a,k,L}(x)\ne\varnothing
\]

if and only if the depth-`L` cylinder of `x` has a concrete shadow at exact
complexity `k-1`.

Unlike the signature belief from the preceding pathway, every member of this
belief is one actual frontier realization. No transition can be assembled from
edges belonging to different states.

## 2. Exact recursive update

Write

\[
x=4q+d,
\qquad d\in\{0,1,2,3\}.
\]

The projection theorem gives

\[
q\in O_{a,k-1}.
\]

For `L>=2`, the exact concrete belief satisfies

\[
\boxed{
B_{a,k,L}(4q+d)
 =\{4p+d:
      p\in B_{a,k-1,L-1}(q),
      4p+d\in O_{a,k-1}\}.
}
\]

The depth-one base case is simply

\[
B_{a,k,1}(x)
 =\{y\in O_{a,k-1}:y\bmod4=x\bmod4\}.
\]

### Proof

If `y` belongs to the left side and `L>=2`, congruence modulo `4^L`
forces

\[
y=4p+d
\]

with

\[
p\equiv q\pmod {4^{L-1}}.
\]

Since `y` is in `O_(a,k-1)`, the projection theorem puts `p` in
`O_(a,k-2)`. Thus `p` belongs to `B_(a,k-1,L-1)(q)`, and its exact lift
`4p+d` belongs to `O_(a,k-1)`.

Conversely, every `p` on the right gives an actual state `4p+d` in
`O_(a,k-1)` congruent to `4q+d` modulo `4^L`. Hence it belongs to the
left side.

This proves the equality.

## 3. Realization consistency

The recursion has a direct operational interpretation.

1. Strip the current low digit.
2. Compute the complete lower-depth concrete belief.
3. Append the same digit to every member.
4. Retain only lifts that actually belong to the required frontier.

Induction on `L` shows that every surviving endpoint is one concrete state that
realizes the complete common cylinder. The update is deterministic on the
concrete set and cannot splice existential signature edges from unrelated
frontier states.

The phase-`p` counterexample from the preceding pathway is handled correctly:

\[
x=12\in O_{p,2},
\qquad x\equiv0\pmod4,
\]

but

\[
O_{p,1}=\{3\},
\qquad B_{p,2,1}(12)=\varnothing.
\]

The concrete recursion rejects the false abstract shadow immediately.

## 4. Three-return campaign through complexity 20

The Python reference implementation enumerates every admissible three-return
occurrence through the configured frontier, computes each belief both directly
and recursively, and requires exact equality.

Through phase complexity 20:

```text
phase outputs:                 1,006,146
eligible outputs:                289,745
three-return occurrences:            210
positive-cut occurrences:              58
distinct occurrence cylinders:         43
empty concrete beliefs:                  0
minimum final belief size:              20
maximum final belief size:          38,846
total concrete shadow realizations: 3,826,769
maximum cut/depth:                    4 / 5
```

The smallest configured belief is the phase-`u`, complexity-18 state

```text
x = 0x6473d46ab
cut = 4
cylinder depth = 5
residue = 0x2ab
belief trace = 665, 264, 88, 35, 20
```

Every digit update retains actual, mutually compatible frontier states.

## 5. Independent complexity-25 census

The independent C++ implementation exhausts both phase frontiers through
complexity 25 and checks the recursive theorem exhaustively through complexity
9.

```text
phase-p outputs:                 9,118,715
phase-u outputs:                 7,745,997
total outputs:                  16,864,712
eligible outputs:                4,831,012

three-return occurrences:            3,395
positive-cut occurrences:              898
shadowed occurrences:                3,395
empty concrete beliefs:                  0
distinct occurrence cylinders:         142
concrete shadow realizations:  1,000,140,318
minimum final belief size:                4
maximum final belief size:          641,962
maximum cut/depth:                   9 / 10
```

The smallest belief occurs at the known phase-`u`, complexity-25 state

```text
x = 0x1bcd3a7b3fdfb
cut = 9
cylinder depth = 10
residue = 0x3fdfb
```

Its complete adjacent-complexity belief has four concrete states:

```text
0x6473c553fdfb
0x6f34eac3fdfb
0x6f671193fdfb
0x6f671623fdfb
```

Thus even the narrowest observed terminal cylinder is realized four times at
complexity 24. This is an exact finite witness, not a signature-level
simulation.

## 6. Validation

Python:

```text
7 tests passed
K=16 certificate:
aefa388564278d291737801033e1cddc9a0902ea3982eee78050606ca2a6391d

K=20 certificate:
d01112f80788627e905f82d17f7740d78b19475b87fa81947b7fd857ddbe8b62
```

Independent C++ through complexity 25:

```text
output SHA256:
a7c36aa911634dd11ef1092111888204cc74f0c4ed6dd30e6497b209a5a91566
runtime: about 2.83 seconds
peak RSS: about 355,540 KiB
```

## 7. Scientific boundary

The concrete belief definition and recursive update are exact at every depth.
They solve the residue and realization-consistency failures of the twelve-
signature abstraction.

The nonemptiness result for three-return cylinders is still finite through
phase complexity 25. This does not prove the all-depth adjacent-shadow
inclusion, phase-complexity divergence, exclusion of eventual center period
two, or Rule 30 center nonperiodicity.

The next target is an invariant of the exact concrete belief recursion that
prevents a terminal three-return belief from becoming empty at arbitrary
complexity, without enumerating the complete frontier.
