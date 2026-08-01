# Exact one-step endpoint profiles do not lift two-step paths

Status: exact one-step profile theorem and exact concrete two-step path-lifting
obstruction, plus a finite phase-`u` gap-`222` census through complexity 27.

## 1. Endpoint fibers

For a phase-`u` frontier state

\[
q\in O_{u,k},
\]

define its base-four child fiber

\[
M_k(q)=\{d\in\{0,1,2,3\}:4q+d\in O_{u,k+1}\}.
\]

The realized masks are the familiar five-symbol alphabet

```text
0000, 0011, 1011, 1100, 1111.
```

A concrete adjacent-complexity endpoint pair consists of

\[
q\in O_{u,k},\qquad p\in O_{u,k-1}.
\]

For the synchronized/full pathway, the pair is admissible when it has the same
low base-four digit and

\[
M_k(q)\subseteq M_{k-1}(p),
\]

with the stronger condition

\[
M_{k-1}(p)=1111
\quad\text{or}\quad
M_{k-1}(p)=M_k(q).
\]

Thus each local shadow fiber is either saturated or synchronized with the
current fiber.

## 2. Exact one-step endpoint profile

Define the endpoint profile

\[
\Pi_k(q)
 =\bigl(M_k(q);C_0(q),C_1(q),C_2(q),C_3(q)\bigr),
\]

where

\[
C_d(q)=
\begin{cases}
\bot,&4q+d\notin O_{u,k+1},\\
M_{k+1}(4q+d),&4q+d\in O_{u,k+1}.
\end{cases}
\]

The absent marker is distinct from the realized fiber `0000`. Without this
distinction, a missing child and a terminal child would be incorrectly
identified.

For a concrete pair `(q,p)`, use the paired profile

\[
\bigl(\Pi_k(q),\Pi_{k-1}(p)\bigr).
\]

### Exact one-step theorem

The paired profile determines, for every digit `d`:

1. whether both concrete children `4q+d` and `4p+d` exist;
2. their local fiber masks;
3. whether the lifted pair is dominant; and
4. whether the lifted pair remains synchronized/full.

This is immediate from the definition: existence and child fibers are entries
of the two profiles, and the two local relations are mask comparisons.

Therefore the paired endpoint profile is an exact abstraction for one common
digit lift.

## 3. Two-step path-lifting obstruction

Exactness for one lift does not imply realization consistency for two lifts.
Consider phase `u`, current complexity 19, and

```text
current:      q  = 0x1bcd3a1c36
good shadow: pg = 0x642e240c2
bad shadow:  pb = 0x642e27436
```

Both concrete pairs are synchronized/full and have identical paired one-step
profiles.

The current endpoint profile is

```text
own fiber:    1100
child fibers: absent, absent, 1111, 1011
```

Both shadow endpoint profiles are

```text
own fiber:    1111
child fibers: 1111, 1111, 1111, 1111
```

Hence the quotient identifies `(q,pg)` and `(q,pb)`.

Now append the common base-four word

```text
30
```

### Good realization

The first digit gives

```text
current: 0x6f34e870db   mask 1011
shadow:  0x190b89030b   mask 1111
```

and the second gives

```text
current: 0x1bcd3a1c36c  mask 0000
shadow:  0x642e240c2c   mask 0000
```

Both lifts remain synchronized/full.

### Bad realization

The first digit gives

```text
current: 0x6f34e870db   mask 1011
shadow:  0x190b89d0db   mask 1111
```

so the first lift is also valid. But the second digit gives

```text
current: 0x1bcd3a1c36c  mask 0000
shadow:  0x642e27436c   mask 1011
```

The current mask is still contained in the shadow mask, so ordinary dominance
has not failed. The synchronized/full condition does fail: `1011` is neither
`1111` nor equal to `0000`.

Thus the paired one-step profile class admits the abstract two-digit word `30`
because of the good realization, while the bad concrete realization in the
same class cannot follow that word inside the synchronized/full relation.

This is an exact path-lifting obstruction. The profile quotient has spliced the
first lift of one concrete endpoint pair with the second lift available only to
another pair.

## 4. Relevance to the gap-222 certificates

The two pairs are not arbitrary frontier artifacts. The independent
complexity-27 campaign finds both inside deterministic minimum-defect
certificates for the same phase-`u`, complexity-21 current state

```text
0x1bcd3a1c36b
```

Specifically:

```text
cut 2 shadow: 0x642e240c2b
cut 4 shadow: 0x642e27436b
```

After stripping their common low digits, the two certificate paths contain the
complexity-19 endpoint pairs above.

The one-step no-go therefore occurs inside the exact restricted pathway being
studied, not merely in the unrestricted frontier graph.

## 5. Independent finite census

The C++ campaign retains the exact complexity-27 gap-`222` totals from the
weighted-recursion pathway:

```text
phase-u outputs:              23,270,776
gap-222 occurrences:              2,989
dominant failures:                    0
minimum defect 0:                 2,986
minimum defect 3:                     3
```

The deterministic minimum certificates contain

```text
4,323 distinct concrete endpoint-pair positions.
```

For a controlled profile census restricted to endpoint complexity at most 22:

```text
endpoint pairs analyzed:                  456
level-specific paired profile classes:    241
unlevelled paired profile classes:        148
classes containing multiple pairs:         62
classes with divergent two-digit language: 19
maximum class size:                        53
```

The explicit word-`30` obstruction is one of these divergent classes.

These counts are finite evidence that the issue is systematic rather than a
single accidental collision. They are not an all-depth growth theorem.

## 6. Validation

Python:

```text
7 tests passed
outputs built through complexity 22: 1,444,495
certificate:
4434461668a668758e7f5f4744824bd530a77aafe423d97d415e175b5beb2d67
```

Independent C++:

```text
compiled with -O3 -std=c++20 -Wall -Wextra -Werror -pedantic
output SHA256:
8fdfbd18fd71ac33cccac436647bcc42b18e97c131461028a456149ede7e4ea8
runtime: about 11.90 seconds
peak RSS: about 319,320 KiB
```

## 7. Scientific boundary

The endpoint-profile definition, one-step exactness, and concrete word-`30`
path-lifting obstruction are exact.

This result rules out the paired one-step endpoint profile as a sound
realization-consistent invariant for arbitrary-length synchronized/full lifts.
It does not rule out a richer finite endpoint state, prove that every fixed
lookahead radius fails, prove that three defects suffice at every complexity,
or prove the all-depth adjacent-shadow inclusion.

The next target should retain a concrete continuation language rather than one
layer of child masks. A natural candidate is a recursively refined endpoint
profile or a residual-language state, tested for stabilization and exact path
lifting before using it in an all-depth argument.
