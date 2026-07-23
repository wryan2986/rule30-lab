# Period-two terminal-head code and fixed zero-island phase

Status: complete informal proof of an exact all-word terminal-head theorem,
zero-step deletion recurrence, and fixed phase for every consecutive
terminal-zero island. These are partial structural results. They do not prove
that resets occur infinitely often, exclude eventual center period two, or
solve Rule 30 center nonperiodicity.

## 1. Setup

Let `Q={00,01,10,11}` be the pair-state alphabet of the exact right-to-left
whole-word transducer. For an inverse-generator word `G`, one scan beginning in
`11` gives

```text
(G|_11, G(11)).
```

Write

```text
e(G)=G(11)
```

and, for a branch `q in {t,u}`,

```text
U_q(G)=(G|_11) p q.
```

The preceding terminal-order theorem showed that `e(G)=00` increments the
leading-`t` order and every nonzero terminal pair resets that order. The present
note identifies the exact first non-`t` letter carried through a zero island.

## 2. Terminal-head coding in the complete transducer

Group the twelve transducer edges by successor pair rather than by input
letter:

```text
successor 00: every edge emits t
successor 01: every edge emits p
successor 10: every edge emits u
successor 11: every edge emits p
```

Define

```text
h(00)=t,
h(01)=p,
h(10)=u,
h(11)=p.
```

### Theorem 1: terminal-head identity

For every inverse word `G`, including the empty word, and every branch
`q in {t,u}`,

```text
head(U_q(G)) = h(e(G)).                              (1)
```

For nonempty `G`, write `G=aB`. When the right-to-left scan reaches the
leftmost input letter `a`, its incoming pair is `B(11)`. The emitted leftmost
section letter and successor pair are

```text
a|_(B(11)),   a(B(11))=G(11).
```

The table property above says that the emitted letter depends only on that
successor pair, and is exactly `h(G(11))`. Appending `p q` at the opposite end
does not change the head. For the empty word, `U_q(empty)=p q`, while
`e(empty)=11` and `h(11)=p`. This proves (1).

Thus the complete terminal pair codes a visible letter at the opposite word
boundary:

```text
00 -> t
01 -> p
10 -> u
11 -> p.
```

The prior terminal-order theorem is the `00 -> t` part iterated across an
existing leading run.

## 3. Zero-domain decomposition

Suppose `e(G)=00` and write

```text
G=t^ell K,
```

where `K` begins with the first non-`t` letter. A pure power of `t` sends `11`
only between `11` and `10`, so `K` is nonempty. Write

```text
K=aB.
```

Because `K(11)=00` and `a` is not `t`, the root-action table has exactly two
possibilities:

```text
a=p and B(11)=11,
a=u and B(11)=10.                                   (2)
```

Call `a` the **zero phase** of `G`. Put

```text
v_p=11,
v_u=10.
```

Then equation (2) is simply `B(11)=v_a`.

## 4. Exact zero-step deletion recurrence

### Theorem 2

If

```text
G=t^ell a B,
e(G)=00,
a in {p,u},
```

then for either branch `q`,

```text
U_q(G)=t^(ell+1) U_q(B).                            (3)
```

To prove this, scan the suffix `B` first. By (2), the letter `a` is processed
on the unique transition that enters successor state `00`; every such
transition emits `t`. The `ell` leading input letters `t` are then processed in
state `00`, each emitting `t` and preserving `00`. Therefore

```text
G|_11 = t^(ell+1) (B|_11).
```

Appending `p q` gives (3).

Equation (3) has a queue interpretation. A zero step:

1. adds one `t` to the outer order;
2. deletes the phase letter `a` from the normalized word;
3. applies the complete block update to the remaining tail `B`.

The branch `q` still enters only at the far appended boundary.

## 5. Fixed phase of a zero island

Normalize after the zero step by removing the new `t^(ell+1)` prefix. By (3),

```text
normalize(U_q(G)) = U_q(B).
```

Theorem 1 and equation (2) give

```text
head(U_q(B))
  = h(B(11))
  = h(v_a)
  = a,                                               (4)
```

because `h(11)=p` and `h(10)=u`.

Thus every zero output propagates the same phase to the next normalized word,
independently of the branch and independently of whether the next terminal
pair is zero.

If the next terminal pair is also `00`, its zero phase is therefore again
`a`. Induction proves:

> **Fixed zero-island phase.** Every consecutive run of terminal pairs `00`
> has one constant phase `a in {p,u}`.

In particular, a hypothetical final zero tail must choose one phase once and
remain in it forever.

Writing the normalized word during such a tail as

```text
K_m=a B_m,
```

the complete final-tail recurrence becomes

```text
B_m(11)=v_a,
K_(m+1)=U_(q_m)(B_m)=a B_(m+1),
B_(m+1)(11)=v_a.                                    (5)
```

The support problem has therefore split into two fixed-terminal fibers:

```text
p phase: B_m(11)=11 for all later m,
u phase: B_m(11)=10 for all later m.
```

Each step removes one left phase letter while the exact actual fringe branch
is appended at the opposite end after a complete section scan.

## 6. Arithmetic interpretation

Let

```text
x=K^(-1)(0)
```

be the ordinary normalized state associated with a terminal-zero word `K`.
The forward generators satisfy

```text
p(0)=3,   bitlen(3)=2,
u(0)=1,   bitlen(1)=1.
```

Every subsequent forward generator `T`, `P`, or `U` raises the bit length of a
positive ordinary integer by exactly two. Therefore:

```text
phase p  iff bitlen(x) is even,
phase u  iff bitlen(x) is odd.                       (6)
```

The word phase is exactly the parity class of the normalized ordinary degree.
The fixed-phase theorem is consistent with the known zero-tail degree law
`bitlen(x_(m+1))=bitlen(x_m)+2`; it strengthens that neutral arithmetic
statement by giving the exact complete-word deletion mechanism behind it.

## 7. Finite verification

The accompanying analyzer independently checks:

- the terminal-head code on every word through length eight and both branches;
- the exact deletion recurrence on every terminal-zero word through length
  eight;
- phase propagation and all continuing-zero transitions in that exhaustion;
- the bit-length parity interpretation;
- all branch drivers through depth five from every terminal-zero word through
  length five.

At the default limits the deterministic counts are:

```text
19,682 word/branch terminal-head cases,
4,920 zero-word/branch deletion cases,
2,460 arithmetic phase cases,
7,358 zero-driver steps.
```

These are implementation checks for the all-word table arguments above.

## 8. Research consequence

The final-zero hypothesis is no longer an undifferentiated growing-word
condition. It requires an infinite orbit in one of two explicit fibers:

```text
phase p with fixed tail terminal 11,
or
phase u with fixed tail terminal 10,
```

under the deletion recurrence (5) driven by the unique zero-initialized
fringe schedule.

The next admissible target is correspondingly narrower:

> Prove that neither fixed-terminal fiber admits an infinite orbit under the
> actual fringe driver.

A fixed numerical bound on zero-run length is unnecessary and unsupported.
A useful continuation should instead derive a return-map obstruction,
monotone quantity, or forbidden cycle inside each of the two fibers.

## 9. Scientific boundary

This theorem does not prove that the actual coupled orbit leaves both fibers
infinitely often. It does not prove that the alternating inverse lift has
infinite support, exclude eventual center period two, or solve Rule 30 center
nonperiodicity.
