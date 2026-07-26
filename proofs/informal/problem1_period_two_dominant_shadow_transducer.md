# Dominant adjacent-level shadow transducer

Status: complete exact derivation of the common-digit simulation lemma and a
finite exhaustive dominant-shadow census through phase complexity 25. The
existence of dominant shadows at every complexity remains open.

## 1. Phase fibers

For phase `a in {p,u}`, let `O_(a,k)` be the ordinary outputs of exact phase
complexity `k`. For `q in O_(a,k)`, define its next-level base-four fiber

\[
M_{a,k}(q)=\{e\in\{0,1,2,3\}:4q+e\in O_{a,k+1}\}.
\]

The recursive phase-frontier theorem proves that only five masks occur:

```text
0000, 0011, 1011, 1100, 1111.
```

The mask is exact, not an empirical approximation.

## 2. Common-digit simulation

Let

\[
q\in O_{a,k},\qquad p\in O_{a,k-1}.
\]

Call `(q,p)` a dominant adjacent pair when

\[
M_{a,k}(q)\subseteq M_{a,k-1}(p).
\]

Then every digit `e` for which `4q+e` is a valid level-`k+1` output is also a
valid lift of `p` to level `k`:

\[
\boxed{
 e\in M_{a,k}(q)
 \Longrightarrow
 4p+e\in O_{a,k}.
}
\]

This follows directly from the two exact fiber definitions, but it is the local
simulation rule needed for adjacent shadows.

After taking a common digit `e`, the new pair is

\[
(4q+e,4p+e).
\]

If that pair is dominant again, the simulation can continue. Thus a finite
sequence of mask containments gives an exact synchronous transducer path.

## 3. Cylinder-path certificate

Let

\[
x\in O_{a,k},\qquad y\in O_{a,k-1}
\]

and suppose `x` and `y` are congruent modulo `4^d`. Repeatedly strip their
common low base-four digits. At step `j`, write

\[
x_j=4q_j+e_j,\qquad y_j=4p_j+e_j.
\]

If

\[
M(q_j)\subseteq M(p_j)
\]

for every `j=0,...,d-1`, then `y` is a **dominant shadow** of `x` in the same
depth-`d` survivor cylinder.

The path is an exact certificate containing only:

```text
(current fiber mask, shadow fiber mask, common digit)
```

at each cylinder digit.

A dominant shadow is stronger than the adjacent-shadow property from PR #37:
it not only lies in the same cylinder, but locally offers every digit offered by
the current state along the certified common path.

## 4. Connection to three-return plateaus

A three-return occurrence at a base prefix `w` and phase complexity `k` would be
minimal only if `w` had no witness at complexity `k-1`. Therefore any dominant
shadow of the occurrence rules out a three-return zero-penalty plateau at that
base prefix.

The all-depth target can now be strengthened to:

\[
\boxed{
\text{Every three-return occurrence admits a dominant adjacent shadow.}
}
\]

This implies the adjacent prefix-language inclusion from PR #37 and hence that
every three consecutive returns contain a positive phase penalty.

## 5. Controlled Python campaigns

The Python reference analyzer constructs exact phase frontiers and groups
level-`k-1` shadows by cylinder residue and their complete mask sequence.

Through complexity 16:

```text
phase outputs:                 96,416
eligible outputs:              27,928
three-return occurrences:          19
positive-cut occurrences:           5
dominant shadows:                   19
violations:                          0
```

Certificate:

```text
fcfe33d05d2071f0e5971df1cdd1ac4c90dae42c7485f9ce5aaab6aaf1f04a86
```

Through complexity 20:

```text
phase outputs:              1,006,146
eligible outputs:             289,745
three-return occurrences:         210
positive-cut occurrences:          58
dominant shadows:                  210
violations:                          0
```

Certificate:

```text
65c431803e07785a47a1851f3cb51358ffd8566ce5af46b6f4117adb705c3889
```

Five dominant mask pairs occur through complexity 20:

```text
1011/1011
1011/1111
1100/1100
1100/1111
1111/1111
```

## 6. Independent complexity-25 census

The independent C++ analyzer exhausts every phase output through complexity 25:

```text
phase-p outputs:               9,118,715
phase-u outputs:               7,745,997
total outputs:                16,864,712
eligible outputs mod 4 = 3:    4,831,012

three-return occurrences:          3,395
positive-cut occurrences:            898
states containing occurrences:     2,856
maximum cut:                            9

dominant shadows:                  3,395
dominance violations:                  0
```

The complete observed mask-pair alphabet is:

```text
0011/1111       1
1011/1011     296
1011/1111     675
1100/1100     214
1100/1111   1,570
1111/1111   2,095
```

The pair counts exceed the occurrence count because positive-cut certificates
contain several common cylinder digits.

The rare `0011/1111` state first appears once at complexity 25. It shows that the
five-state alphabet seen through complexity 20 was not yet complete, while the
mask-containment principle itself remained intact.

Controlled C++ evidence:

```text
output SHA256:
f970c4ea75360885e437bb4c17e72b8ee6990846bcff5e6039740f0fd65fc90e

runtime:       about 1.3 seconds
peak RSS:      about 137,912 KiB
```

## 7. What remains

The exact local theorem is now finite-state: mask containment is sufficient for
one common digit, and a sequence of containments is sufficient for an entire
cylinder.

What is not yet proved is that a dominant shadow exists for every possible
three-return-bearing state at arbitrarily high complexity. The six observed
states are a candidate invariant alphabet, not yet a proved closed transducer.

The next step is to derive all possible successor mask pairs from the recursive
partial-inverse rule and prove that the six safe states are closed for the
terminal three-return seed conditions.

This result does not yet prove the all-depth adjacent-shadow inclusion,
phase-complexity divergence, exclusion of eventual center period two, or Rule 30
center nonperiodicity.
