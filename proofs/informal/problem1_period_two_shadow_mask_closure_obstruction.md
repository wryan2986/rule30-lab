# Exact obstruction to closing the six-state dominant-shadow mask transducer

Status: complete all-depth derivation of the twelve-symbol parent/fiber
signature algebra and exact finite counterexamples to closure of the six visible
fiber-mask pairs. The richer transition census is finite through phase
complexity 25 and does not prove the desired adjacent-shadow theorem.

## 1. Phase-frontier fibers

For phase `a` and exact complexity `k`, let `O_(a,k)` be the ordinary phase
frontier. For `q in O_(a,k)`, define the next-level base-four fiber

\[
M_{a,k}(q)=\{e\in\{0,1,2,3\}:4q+e\in O_{a,k+1}\}.
\]

The recursive lift theorem associates four exact candidate parents `Q_d(q)`.
Let

\[
P_{a,k}(q)=\{d:Q_d(q)\in O_{a,k}\}
\]

be the candidate-parent mask.

The four parent digits contribute the fixed child masks

```text
parent digit 0 -> 1011
parent digit 1 -> 1100
parent digit 2 -> 1110
parent digit 3 -> 0011
```

Therefore

\[
\boxed{M_{a,k}(q)=\bigvee_{d\in P_{a,k}(q)} C_d.}
\]

This identity is exact at every phase and complexity.

## 2. Twelve universal parent/fiber signatures

A frontier predecessor ending in base-four digit `2` always has its digit-`3`
mate. Hence

\[
2\in P_{a,k}(q)\Longrightarrow 3\in P_{a,k}(q).
\]

Of the sixteen four-bit predecessor masks, exactly twelve satisfy this
condition. Applying the fixed OR formula gives the universal signature table:

```text
predecessor / fiber
0000 / 0000
0001 / 1011
0010 / 1100
0011 / 1111
1000 / 0011
1001 / 1011
1010 / 1111
1011 / 1111
1100 / 1111
1101 / 1111
1110 / 1111
1111 / 1111
```

Thus

\[
\Sigma_{a,k}(q)=(P_{a,k}(q),M_{a,k}(q))
\]

takes values in an exact twelve-symbol alphabet. The five fiber masks used in
PR #38 are the quotient obtained by forgetting the predecessor component.

## 3. The six visible pair states are not closed

The proposed mask-pair transducer state was

\[
(M_{a,k}(q),M_{a,k-1}(p))
\]

for adjacent frontier states `q` and `p`. A shared low digit allows both states
to be divided by four. Closure would require the resulting lower mask pair to
remain dominant.

This is false even in phase `p` at small exact complexities.

### Unsafe realization

```text
q = 222 in O_(p,4)
p =  50 in O_(p,3)
shared digit = 2
visible mask pair = 1011 / 1111
```

After stripping the shared digit,

```text
q >> 2 = 55 in O_(p,3)
p >> 2 = 12 in O_(p,2)
lower mask pair = 1111 / 1100
```

The lower current mask is not contained in the lower shadow mask.

### Safe realization with the same visible data

```text
q = 3202 in O_(p,6)
p =  802 in O_(p,5)
shared digit = 2
visible mask pair = 1011 / 1111
```

Here stripping the digit gives

```text
lower mask pair = 1111 / 1111
```

which is safe.

Consequently,

\[
\boxed{
(\text{fiber pair},\text{shared digit})
\text{ does not determine the next lower pair.}
}
\]

In particular, the six observed states from PR #38 cannot be proved closed as a
standalone finite transducer because an exact realization of one of those
states already has an unsafe successor.

## 4. The twelve-symbol refinement is still nondeterministic

Remembering the complete predecessor mask repairs the information lost by the
OR map, but it does not make digit evolution deterministic.

The same source signature and digit occur in the following exact phase-`p`
transitions:

```text
source signature = 1000 / 0011
digit = 0

level 1: state    3 -> child    12 -> 0010 / 1100
level 5: state  801 -> child  3204 -> 1110 / 1111
level 6: state 3583 -> child 14332 -> 0000 / 0000
```

Thus

\[
\boxed{
(\Sigma,\text{digit})
\text{ defines a nondeterministic relation, not a transition function.}
}
\]

A successful finite proof must therefore retain a set of compatible signatures,
an exact relation between candidate parents, or another invariant that controls
which nondeterministic successor is realized.

## 5. Controlled transition census

The Python reference campaign exhausts both frontiers through configurable
complexity and verifies the parent/fiber formula for every state.

Through complexity 20:

```text
phase-p outputs:                 544,978
phase-u outputs:                 461,168
combined outputs:              1,006,146

realized signatures per phase:        12
labelled signature edges per phase:  194
```

The independent C++ campaign through complexity 25 gives:

```text
phase-p outputs:               9,118,715
phase-u outputs:               7,745,997
total outputs:                16,864,712

realized signatures per phase:        12
labelled signature edges per phase:  194
```

The identical 194-edge relation in both phases is strong finite evidence that
the twelve-symbol nondeterministic automaton has stabilized, but the census is
not promoted to an all-depth theorem.

## 6. Validation

```text
Python tests: 7 passed

Python K=16 certificate:
63e48b7d4c2f1a0751f58384477686c944ed35eafd92a9d059bc64c7fbf89f36

Python K=20 certificate:
e6fbfd4d831886361aaf1642e2466b249fb677896a3bffae9146e7848e0ae0c4

C++ K=25 output SHA256:
3baf13a5f6a6e4ad0e031840e92cce19a30f77b880060404382257bc7427cace

C++ runtime: about 27.3 seconds
C++ peak RSS: about 109,852 KiB
```

## 7. Scientific boundary

The twelve-symbol signature algebra and the two concrete closure counterexamples
are exact. The 194-edge transition census is finite.

This result does not prove closure of a richer set-valued transducer, the
all-depth adjacent-shadow inclusion, phase-complexity divergence, exclusion of
eventual center period two, or Rule 30 center nonperiodicity.

The next target is a set-valued simulation relation on the twelve signatures.
Instead of requiring one visible mask pair to have a unique safe successor, the
shadow side should carry every compatible signature needed to answer all
nondeterministic current successors with the same base-four digit.
