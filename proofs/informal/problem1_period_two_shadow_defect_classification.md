# Saturated-shadow no-go and three-defect classification

Status: exact saturated-shadow sufficiency theorem, exact finite counterexamples
to universal saturated-shadow existence, and an exhaustive complexity-25
classification of the minimum number of non-full shadow masks.

## 1. Saturated dominant shadows

For a current state `x in O_(a,k)` and a concrete same-cylinder shadow
`y in O_(a,k-1)` of depth `L`, write the current and shadow fiber-mask
sequences from low digit to high digit as

\[
(C_0,\ldots,C_{L-1}),
\qquad
(S_0,\ldots,S_{L-1}).
\]

The shadow is dominant exactly when

\[
C_j\subseteq S_j
\]

for every step `j`.

Call the shadow **saturated** when

\[
S_j=1111
\]

at every step. A saturated shadow is automatically dominant, independent of
the current mask sequence, because every current fiber is a subset of `1111`.
Thus saturated existence is a sufficient concrete certificate for the adjacent
shadow inclusion.

## 2. Defect measure

Define the defect count of a dominant shadow by

\[
\delta(y)=\#\{j:S_j\ne1111\}.
\]

A saturated shadow has defect zero. The minimum defect of one occurrence is the
minimum of `delta(y)` over every dominant same-cylinder adjacent shadow.

This measure retains exact residue and concrete realization consistency. It is
not the earlier signature-level abstraction.

## 3. Controlled Python campaigns

Through phase complexity 16:

```text
outputs:                       96,416
eligible outputs:              27,928
three-return occurrences:          19
dominant failures:                  0
saturated failures:                 0
maximum minimum defect:             0
certificate:
87fb98033cf66048cf7f44ea11c09fcd40879bf6fe8d05e1214016f65ce0b080
```

Through phase complexity 20:

```text
outputs:                    1,006,146
eligible outputs:             289,745
three-return occurrences:         210
dominant failures:                   0
saturated failures:                  0
maximum minimum defect:              0
certificate:
547b110c32c284a1fbc95f42c813403e2821f85dddd45839d84b51a71704303e
```

The phase-`u`, complexity-18, depth-five saturated language covers only
`988` of the `1024` possible residues. The observed terminal occurrence
residues still lie inside that proper subset. Therefore full residue coverage
is already false before saturated occurrence existence fails.

## 4. Complexity-25 saturated-shadow counterexamples

The independent C++ campaign exhausts all `3,395` three-return occurrences
through phase complexity 25.

Exactly two occurrences have no saturated shadow.

### First counterexample

```text
phase: u
complexity: 23
cut: 7
cylinder depth: 8
state: 0x191cf4384dfb
residue: 0x4dfb
return gaps: 222
```

A minimum-defect dominant shadow is

```text
0x6473cb14dfb
```

with low-to-high mask sequences

```text
current: 1011,1111,1011,1100,1111,1111,0011,1111
shadow:  1011,1111,1011,1100,1111,1111,1111,1111
```

The shadow has exactly three non-full masks.

### Second counterexample

```text
phase: u
complexity: 25
cut: 9
cylinder depth: 10
state: 0x1bcd3a7b3fdfb
residue: 0x3fdfb
return gaps: 222
```

A minimum-defect dominant shadow is

```text
0x6f671193fdfb
```

and both current and shadow have the low-to-high sequence

```text
1111,1111,1111,1111,1111,1011,1100,1111,1011,1111
```

Again the minimum defect is exactly three.

These are exact finite counterexamples to the proposed invariant

```text
every terminal three-return occurrence has a saturated shadow.
```

## 5. Complete minimum-defect census

Through complexity 25:

```text
three-return occurrences: 3,395
dominant failures:             0
minimum defect 0:          3,393
minimum defect 1:              0
minimum defect 2:              0
minimum defect 3:              2
maximum minimum defect:        3
```

Every occurrence still has a concrete dominant shadow. The two exceptions are
both phase-`u` occurrences with return-gap word `222`.

Only nine chosen minimum-defect mask words occur in the complete campaign:
all-`1111` words at the realized depths, plus the two exceptional words above.
This sharply isolates the missing all-depth argument to a very small exceptional
family rather than the full concrete belief space.

## 6. Validation

Python:

```text
7 focused tests passed
K=16 certificate:
87fb98033cf66048cf7f44ea11c09fcd40879bf6fe8d05e1214016f65ce0b080
K=20 certificate:
547b110c32c284a1fbc95f42c813403e2821f85dddd45839d84b51a71704303e
```

Independent C++ through complexity 25:

```text
output SHA256:
5d55dcda274110eae611c53f3b82dfd3015a705dbb1da9ac2bc8bef65358157d
runtime: about 21.42 seconds
peak RSS: about 441,220 KiB
```

## 7. Scientific boundary

Saturated-shadow sufficiency and the defect definition are exact at every
depth. The two saturated counterexamples and the `0/3` defect census are exact
for the exhausted frontiers through complexity 25.

This does not prove that three defects suffice at every complexity, prove the
all-depth adjacent-shadow inclusion, establish phase-complexity divergence,
exclude eventual center period two, or solve Rule 30 center nonperiodicity.

The next target is the exceptional phase-`u` `222` family: derive a recursive
transition law for its three non-full masks and prove that the exceptional
family always retains a dominant concrete shadow.
