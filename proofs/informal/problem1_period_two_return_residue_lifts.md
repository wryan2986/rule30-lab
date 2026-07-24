# Period-two return-coordinate lift relation

Status: complete all-time proof of the exact lifted first-return relation from
`z mod 64`, including the minimal finite precision needed to determine one
lifted outcome. This is a no-go theorem for residue-only induction. It does not
describe the unique higher-bit actual orbit and does not exclude eventual center
period two or solve Rule 30 center nonperiodicity.

## 1. Return coordinates

At a `u` return, the packed fringe state has its first two bits zero, so write

```text
A = 4z.
```

Let `rho(z)` be the next return gap and let `R(z)` be the next return
coordinate:

```text
F^rho(z)(4z) = 4 R(z).
```

The established fringe-language theorem gives

```text
rho(z) in {2,3,4,5}.
```

We study the lifted outcome

```text
(rho(z), R(z) mod 64).
```

## 2. Exact dependency precision

One fringe block has spatial dependency radius two. To determine the next
coordinate modulo 64, one must determine the next return state modulo 256.
Across at most five blocks this requires the initial return state modulo
`2^(8+10)`. Since `A=4z`, it is enough to know

```text
z mod 2^16.
```

Thus the lifted outcome is constant on every residue class modulo `2^16`.

Complete exhaustion proves this precision is minimal. For every

```text
6 <= k < 16,
```

there are two coordinates congruent modulo `2^k` with different lifted
outcomes. For example,

```text
z=0:   outcome (4,56)
z=256: outcome (4,44).
```

They agree modulo 256, so eight coordinate bits are not enough. The analyzer
records an explicit witness at every lower precision through fifteen bits.

## 3. The exact mod-64 lift relation

Define

```text
T(r) = {(g,s): some z == r mod 64 has rho(z)=g and R(z)==s mod 64}.
```

Because sixteen coordinate bits are sufficient, `T` is obtained exactly by
checking the 65,536 residues modulo `2^16`.

The eight classes seen in the bounded actual campaign have the following rows:

```text
T(0)  = {(4,0),(4,12),(4,14),(4,24),(4,32),(4,35),
         (4,43),(4,44),(4,48),(4,56),(4,62)}
T(3)  = {(3,3),(3,11),(3,27),(3,35),(3,43)}
T(11) = {(5,3),(5,11),(5,19),(5,43),(5,59)}
T(24) = {(2,11),(2,63)}
T(35) = {(3,3)}
T(43) = {(5,11),(5,43)}
T(56) = {(2,31),(2,63)}
T(63) = {(5,12),(5,19),(5,24),(5,28),(5,35),
         (5,44),(5,51),(5,56),(5,60)}.
```

In particular, the finite actual residue set

```text
{0,3,11,24,35,43,56,63}
```

is not closed under arbitrary compatible higher-bit lifts. Class `0` already
has a lift entering bad class `44`, while class `63` has lifts entering all
three consecutive-gap-two classes `28,44,60`.

## 4. Universal closure no-go theorem

Forget the higher bits and close the initial class `0` under the existential
relation `T`. The exact layers are

```text
C0 = {0}
C1 = {12,14,24,32,35,43,44,48,56,62}
C2 = {3,6,11,28,31,38,60,63}
C3 = {19,27,39,51,55,59}.
```

No new class appears after `C3`. The closure has 25 residues and contains

```text
{28,44,60}.
```

Therefore there is no set `S` of residues modulo 64 satisfying all three
conditions:

1. `0 in S`;
2. every lifted successor of every class in `S` also lies in `S`;
3. `S` avoids `28,44,60`.

Equivalently, no proof that retains only `z mod 64` and quantifies over all
higher-bit lifts can prove that the zero-initialized actual orbit avoids two
consecutive gap-two returns.

## 5. Consequence for continuation

The actual orbit chooses one very special lift inside each mod-64 class. The
200,000-block avoidance result is therefore genuine information about the
complete finite fringe word, not a consequence of the observed residue set.
A successful continuation must retain at least enough higher-bit or global
front information to distinguish the actual lift from the other members of
`T(r)`.

This result does not show that the actual orbit ever enters a bad cylinder. It
shows only that residue-only induction cannot prove that it does not.
