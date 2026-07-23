# Period-two past/future dual-cut criterion

Status: complete informal proof of an exact all-depth factorization and
past/future prefix-matching criterion for terminal-zero runs. This is a partial
structural result. It does not prove infinitely many resets, exclude eventual
center period two, or solve Rule 30 center nonperiodicity.

## 1. Setup

Let `Q={00,01,10,11}` be the pair-state alphabet of the exact right-to-left
whole-word transducer. For an inverse-generator word `W` and a pair state
`v in Q`, one complete scan returns

```text
(W|_v, W(v)).
```

The period-two accumulated word update is

```text
U_q(W) = (W|_11) p q,       q in {t,u}.
```

The terminal output pair is

```text
e(W)=W(11).
```

The preceding terminal-order result proves that `e(W)=00` increments the
leading-`t` order by one and every nonzero pair resets it. The present note
describes the complete *forward* zero-run length from a cut, rather than the
immediately preceding run.

## 2. Fresh future boundary word

Fix a future branch driver

```text
q_0,q_1,q_2,...
```

and start a second accumulated word from the identity:

```text
C_0 = empty,
C_(j+1) = U_(q_j)(C_j).
```

Define its terminal pair at depth `j` by

```text
s_j = C_j(11).
```

The infinite state word

```text
V(q)=s_0 s_1 s_2 ...
```

depends only on the future branch schedule. In particular `s_0=11`; the prefix
through `s_(L-1)` depends only on `q_0,...,q_(L-2)`.

Now start the same driver from an arbitrary past accumulated word `G`:

```text
G_0 = G,
G_(j+1) = U_(q_j)(G_j),
e_j = G_j(11).
```

The sequence `e_0,e_1,...` is the terminal-pair stream seen after the cut.

## 3. Section composition

For two inverse words `A,B` and a pair state `v`, the standard section rule is

```text
(AB)|_v = (A|_(B(v))) (B|_v).
```

For a state word `v_0...v_(j-1)`, write

```text
G|_(v_0...v_(j-1))
```

for the iterated section obtained by successively taking sections at those pair
states.

## 4. Exact past/future factorization

### Theorem 1

For every `j>=0`,

```text
G_j = (G|_(s_0...s_(j-1))) C_j.                    (1)
```

For `j=0`, both sides are `G`.

Assume (1) at depth `j`. Applying one block gives

```text
G_(j+1)
  = (G_j|_11) p q_j
  = (((G|_(s_0...s_(j-1))) C_j)|_11) p q_j.
```

Using section composition and `C_j(11)=s_j`,

```text
G_(j+1)
  = (G|_(s_0...s_j)) (C_j|_11) p q_j
  = (G|_(s_0...s_j)) C_(j+1).
```

This proves (1) by induction.

Taking the action of both sides of (1) on `11` gives

```text
e_j
  = (G|_(s_0...s_(j-1)))(s_j).                    (2)
```

Equation (2) says exactly that the state word emitted by the dual action of
`G` on

```text
s_0...s_(L-1)
```

is

```text
e_0...e_(L-1).
```

Thus:

> **Past/future dual-cut identity.** The terminal-pair word after a cut is the
> dual tree action of the complete past accumulated word on a state word
> generated solely by the future branch schedule.

This is an all-depth identity. No fixed observation width is being held while
the strip grows.

## 5. Unique past zero target

Every input-letter column of the whole-word transducer permutes the four pair
states. Therefore every inverse word `G` acts by an automorphism of the rooted
four-ary tree `Q*`.

For each depth `L`, there is consequently one and only one state word

```text
Z_L(G) in Q^L
```

such that

```text
tau_G(Z_L(G)) = 00^L,                               (3)
```

where `tau_G` denotes the dual action of `G`.

The depth targets are compatible under truncation, so they define one infinite
boundary word `Z(G)` in the usual prefix sense. It is determined completely by
the past word `G`.

Combining (2) and (3) proves:

### Theorem 2

The next `L` terminal pairs are all zero exactly when

```text
V_L(q) = Z_L(G),                                    (4)
```

where `V_L(q)=s_0...s_(L-1)` is the future boundary prefix.

Equivalently, the number of consecutive terminal `00` pairs beginning at the
cut is exactly

```text
LCP(V(q), Z(G)),                                    (5)
```

the common-prefix length of the future-schedule boundary word and the unique
past dual zero target. An infinite final zero tail occurs exactly when the two
infinite boundary words are equal.

## 6. Relation to the terminal-order cocycle

At block `m` of the actual period-two orbit, let `G_m` be the accumulated past
word and let `q_m,q_(m+1),...` be the actual future fringe schedule.

The preceding terminal-order theorem gives

```text
ord_t(G_m)
```

as the length of the immediately preceding terminal-zero run.

The present theorem gives

```text
LCP(V_m, Z(G_m))
```

as the length of the terminal-zero run beginning at `m`.

Together, these two exact quantities measure the zero island on both sides of
the cut:

```text
past zero length | cut m | future zero length.
```

A mismatch at dual depth `r` means the terminal pair at block `m+r` is nonzero,
and the leading-`t` order resets at the following update.

## 7. Actual-orbit regression campaign

The analyzer independently verifies:

- Theorem 1 and the complete dual output identity for every initial word through
  length five and every branch driver through depth six.
- Unique inversion of the all-zero target through depth seven, with complete
  brute-force uniqueness checks through depth four.
- The cut mismatch/common-prefix identity at selected cuts of the exact
  zero-initialized fringe orbit through block 10,000.

The exact finite campaign checks:

```text
46,228 initial-word / driver factorization cases,
2,912 word / target-depth inversion cases,
12 actual-orbit cuts at depth 12.
```

The 10,000-block prefix has a longest terminal-zero run of length five at
blocks `2948` through `2952`, matching the prior terminal-order campaign.

A separate nondefault 20,000-block extension finds the first run of length six
at blocks `18888` through `18893`. This refutes any attempted proof based on a
small numerical bound such as five. It is finite diagnostic evidence only.

## 8. Research consequence

The final-zero hypothesis at a cut `m` is no longer merely “the output pairs
stay zero.” It is the exact infinite matching condition

```text
V_m = Z(G_m).                                       (6)
```

The two sides of (6) are generated from opposite temporal directions:

- `Z(G_m)` is determined by the complete accumulated past word.
- `V_m` is determined by the complete future autonomous fringe schedule.

This is the desired cross-characteristic formulation. It avoids the free-middle
obstruction because both objects are full boundary words at every depth.

The remaining target is now specific:

> Prove that, for infinitely many actual cuts `m`, the future boundary word
> `V_m` differs from the past zero target `Z(G_m)` at some finite depth.

That statement is equivalent to nonzero terminal pairs recurring infinitely
often. A bounded computation can locate mismatches but cannot prove their
infinite recurrence.

## 9. Scientific boundary

This result does not prove that the alternating inverse lift has infinite
support, exclude eventual center period two, or solve Rule 30 center
nonperiodicity.

It supplies an exact all-scale past/future cut identity and turns each reset
into a unique dual-boundary mismatch. The open step is to force such mismatches
infinitely often using a property special to the zero-initialized fringe orbit.
