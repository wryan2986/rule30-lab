# Period-two finite-witness complexity

Status: complete informal proof of an exact boundedness criterion, a finite-word
counting theorem, and an almost-sure linear lower bound for phase-constrained
zero witnesses. These are all-scale structural results. They do not prove the
required divergence for the unique zero-initialized fringe schedule and do not
solve Rule 30 center nonperiodicity.

## 1. Boundary prefixes and normalized witnesses

Let

```text
q=(q_0,q_1,...),  q_j in {t,u},
```

be a future branch schedule. Starting from the empty accumulated word, form

```text
C_0=empty,
C_(j+1)=(C_j|_11) p q_j,
s_j=C_j(11).
```

The depth-`L` future boundary word is

```text
V_L(q)=s_0...s_(L-1) in Q^L,
Q={00,01,10,11}.
```

The exact first-difference theorem says that distinct branch prefixes of length
`L-1` give distinct words `V_L`.

For a phase `a in {p,u}`, define

```text
kappa_a(q,L)
```

as the minimum length of a normalized positive inverse word

```text
K in a {t,p,u}*
```

such that its dual action satisfies

```text
tau_K(V_L(q))=00^L.                              (1)
```

The phase-universality theorem proves that this minimum is finite at every
finite depth. Put

```text
kappa(q,L)=min(kappa_p(q,L),kappa_u(q,L)).
```

Leading `t` letters are omitted because they fix the all-zero target. If
`t^r K` sends a boundary prefix to `00^L`, then `K` already does so.

## 2. Monotonicity

A word satisfying (1) at depth `L+1` also satisfies it after truncation to depth
`L`. Therefore

```text
kappa_a(q,L+1) >= kappa_a(q,L).                  (2)
```

The same holds for `kappa`.

Thus finite support is represented by a monotone integer sequence rather than
by unrelated witnesses at successive depths.

## 3. Exact boundedness criterion

Fix a phase `a` and an integer `N`. Let

```text
W_a(N)={K: K begins with a and 1<=len(K)<=N}.
```

This is a finite set. For every depth `L`, define

```text
S_L(q,a,N)
  ={K in W_a(N): tau_K(V_L(q))=00^L}.
```

The sets are nested:

```text
S_(L+1) subset S_L.                              (3)
```

Suppose `kappa_a(q,L)<=N` for every `L`. Then every `S_L` is nonempty. A
nested sequence of nonempty subsets of the finite set `W_a(N)` has nonempty
intersection. Hence one word `K` satisfies

```text
tau_K(V(q))=00^infinity.                         (4)
```

Conversely, a finite word satisfying (4) bounds every finite-depth minimum by
its length. Therefore:

> **Finite-witness criterion.** A finite normalized phase-`a` word kills the
> complete future boundary if and only if `kappa_a(q,L)` is bounded in `L`.

By the dual-cut and fixed-phase theorems, this is exactly the existence of an
ordinary finite phase-`a` zero survivor for the schedule. The unresolved actual
case is now the statement

```text
kappa_p(q_actual,L) -> infinity
and
kappa_u(q_actual,L) -> infinity.                 (5)
```

Because of monotonicity, unboundedness and divergence are equivalent.

## 4. Finite-word counting theorem

There are exactly

```text
3^(n-1)
```

normalized words of length `n` in one prescribed phase: the first letter is
fixed and each remaining letter is arbitrary. Thus the number of phase-`a`
words of length at most `N` is

```text
1+3+...+3^(N-1)=(3^N-1)/2.                       (6)
```

Each such word has exactly one depth-`L` zero-target preimage under its
invertible dual action. Since the schedule-to-boundary map is injective on
length-`L-1` branch prefixes, one word can account for at most one schedule
prefix. Consequently:

```text
#{q[0:L-1] : kappa_a(q,L)<=N} <= (3^N-1)/2.       (7)
```

Allowing either phase gives

```text
#{q[0:L-1] : kappa(q,L)<=N} <= 3^N-1.             (8)
```

These are exact all-depth counting bounds. They do not assume random schedules.

## 5. Almost-sure linear growth

Put the fair Bernoulli measure on schedule space. There are `2^(L-1)` branch
prefixes of length `L-1`. Equation (7) gives

```text
P[kappa_a(q,L)<=N] <= (3^N-1)/2^L.                (9)
```

Choose any

```text
c < log(2)/log(3)
```

and set `N=floor(cL)`. The right side of (9) decays exponentially because

```text
c log(3)-log(2)<0.
```

Its sum over `L` is finite. The first Borel-Cantelli lemma, which needs no
independence, implies that almost every schedule satisfies

```text
kappa_a(q,L)>cL
```

for all sufficiently large `L`. Letting `c` approach the threshold through a
countable sequence proves

```text
liminf_(L->infinity) kappa_a(q,L)/L
  >= log(2)/log(3)
  ~= 0.6309297535714574                         (10)
```

for both phases almost surely.

Thus finite survivors are not merely measure-zero exceptions. Almost every
schedule requires linearly increasing finite witnesses.

## 6. Exact Schreier-graph computation

At fixed depth, the three dual generators act as permutations of `Q^L`. The
minimum unrestricted witness length is the directed positive-word distance from
`V_L` to `00^L`.

For a prescribed phase `a`, write a normalized witness as

```text
K=aW.
```

The rightmost word `W` acts first, so

```text
tau_(aW)(V_L)=00^L
```

is equivalent to

```text
tau_W(V_L)=tau_a^(-1)(00^L).                     (11)
```

Therefore `kappa_a` is one plus a shortest positive-word distance to the unique
phase preimage in the finite Schreier graph. Reverse breadth-first search gives
exact witnesses and distances.

## 7. Actual-prefix campaign

For the zero-initialized moving fringe, the exact minima through depth ten are

```text
L:          1  2  3  4  5  6  7  8  9 10
kappa:      1  2  2  7  8 12 13 14 17 17
kappa_p:    1  3  7  8  8 12 13 17 17 17
kappa_u:    2  2  2  7 12 14 14 14 18 19
```

Every listed value is an exact finite-graph distance. The growth and plateaus
are finite evidence only. In particular, ten values cannot establish (5).

## 8. Research consequence

Finite-depth universality says every entry of the complexity sequence is
finite. The present theorem identifies the only remaining distinction:

- an ordinary finite survivor makes one phase complexity sequence bounded;
- infinite support forces both phase sequences to diverge;
- almost every schedule has linear divergence automatically;
- the actual fringe schedule is a special deterministic path for which
  divergence remains to be proved.

The next useful target is an actual-orbit lower bound on `kappa_a`, perhaps from
return-map complexity, section-cycle growth, or a relation between witness
length and the autonomous fringe's expanding dependency cone.
