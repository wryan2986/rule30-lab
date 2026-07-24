# Period-two arithmetic witness quotient and Pell counting

Status: complete informal proof of an exact arithmetic quotient, Pell-growth
counting bound, and improved almost-sure witness-complexity lower rate. A bounded
campaign and an independent 64-bit replay extend the actual-prefix exclusions.
These are partial structural results. They do not prove divergence on the actual
zero-initialized fringe schedule, exclude eventual center period two, or solve
Rule 30 center nonperiodicity.

## 1. Normalized witnesses and their arithmetic image

Let

```text
G=a_1...a_n,  a_1 in {p,u},  a_j in {t,p,u}
```

be a normalized inverse word. Define its ordinary arithmetic state by

```text
x(G)=G^(-1)(0).
```

Writing

```text
T(x)=x XOR ((x<<1) OR (x<<2)),
```

the three forward generators used to compute `x(G)` are

```text
t(x)=T(x),
u(x)=T(x) XOR 1,
p(x)=T(x) XOR 1 XOR (2 if x is even else 0).
```

The first phase letter gives

```text
p(0)=3,
u(0)=1.
```

Both are positive odd states. Every later word letter applies one of the three
maps above.

Different words may have the same arithmetic state. The finite-witness problem
therefore factors through the much smaller set of distinct values `x(G)`, rather
than the raw ternary word set.

## 2. Exact parity transition

The shifted terms in `T(x)` have zero low bit, so

```text
T(x) mod 2 = x mod 2.
```

Consequently:

- `t` preserves parity;
- `p` and `u` flip parity;
- if `x` is odd, the extra bit-one correction in `p` vanishes and
  
  ```text
  p(x)=u(x);
  ```
- if `x` is even, `p(x)` and `u(x)` differ exactly in bit one and are distinct.

Thus one odd state has at most

```text
one odd child and one even child,
```

while one even state has at most

```text
two odd children and one even child.
```

Cross-parent collisions can only decrease the number of distinct successor
states.

## 3. Pell-growth theorem

For one fixed initial phase, let

```text
E_n = number of distinct even states x(G) from exact length-n words,
O_n = number of distinct odd states x(G) from exact length-n words.
```

The parity transition gives

```text
E_(n+1) <= E_n + O_n,
O_(n+1) <= 2 E_n + O_n.                         (1)
```

At length one there is one odd state and no even state:

```text
(E_1,O_1)=(0,1).
```

Let `P_n` be the Pell sequence

```text
P_0=0,
P_1=1,
P_n=2P_(n-1)+P_(n-2).
```

Iterating the equality version of (1) from `(0,1)` gives total populations

```text
1,2,5,12,29,... = P_1,P_2,P_3,P_4,P_5,...
```

because the transition matrix

```text
M = [[1,1],
     [2,1]]
```

has characteristic polynomial

```text
lambda^2-2lambda-1
```

and dominant eigenvalue

```text
rho=1+sqrt(2).
```

Induction using (1) therefore proves:

> **Pell arithmetic-image bound.** For either fixed phase `a in {p,u}`, the
> number of distinct arithmetic states represented by normalized words of exact
> length `n` is at most `P_n`.

Summing exact lengths gives

```text
sum_(n=1)^N P_n = (P_(N+1)+P_N-1)/2.             (2)
```

Hence the number of distinct phase-`a` arithmetic witness states represented by
words of length at most `N` is at most the right side of (2). Allowing both
phases doubles this bound.

This is strictly stronger than the raw word count

```text
(3^N-1)/2
```

used previously.

## 4. Transfer to future-driver counting

For a future driver prefix of length `L-1`, let `V_L(q)` be its depth-`L` fresh
boundary word. The schedule-to-boundary prefix map is injective.

For a normalized word `G`, the unique dual zero target

```text
Z_L(G)=tau_G^(-1)(00^L)
```

is exactly the first `L` low bit-pairs of `x(G)=G^(-1)(0)`, with the two bits in
each pair written in the established pair-state order. This follows recursively:
choosing the unique input pair mapped to `00` removes the low pair of `x(G)`,
and the next section acts on the remaining higher bits.

Therefore one arithmetic state determines at most one depth-`L` zero-target
boundary word. Combining this with injectivity of `q -> V_L(q)` gives

```text
#{q prefixes: kappa_a(q,L) <= N}
    <= (P_(N+1)+P_N-1)/2.                         (3)
```

For either phase,

```text
#{q prefixes: kappa(q,L) <= N}
    <= P_(N+1)+P_N-1.                             (4)
```

Equations (3)-(4) are exact all-depth counting bounds.

## 5. Improved almost-sure lower rate

Under fair Bernoulli measure, every driver prefix of length `L-1` has
probability `2^(-(L-1))`. Since

```text
P_N = Theta((1+sqrt(2))^N),
```

(3) gives, for `N=floor(cL)`,

```text
Pr[kappa_a(q,L) <= cL]
    <= C ((1+sqrt(2))^c / 2)^L.
```

This is summable whenever

```text
c < log(2)/log(1+sqrt(2)).
```

Borel-Cantelli, followed by a countable limit over rational `c` below the
threshold, proves:

```text
liminf_(L->infinity) kappa_a(q,L)/L
    >= log(2)/log(1+sqrt(2))
    ~= 0.7864397013573949                         (5)
```

for Bernoulli-almost every schedule and for each phase. The previous raw-word
argument gave only `log(2)/log(3) ~= 0.63093`.

The same rate holds for unrestricted phase complexity because doubling the
count changes only the constant factor.

## 6. Exact actual-survivor agreement formula

Let `X` be the unique 2-adic zero survivor of the actual future schedule. Its
first `L` low bit-pairs are exactly `V_L(q_actual)`.

For an arithmetic witness state `x=x(G)`, the number of complete terminal-zero
blocks matched by `G` is

```text
floor(v_2(x-X)/2).                                (6)
```

Indeed, matching `L` complete pair states is equivalent to

```text
x = X mod 2^(2L).
```

Equation (6) allows exact enumeration in the arithmetic quotient without
retaining any representative word. It also automatically deduplicates all word
relations.

## 7. Controlled campaigns

The Python analyzer exhausts the configured arithmetic images independently in
both phases, verifies every parity and Pell inequality, reconstructs the actual
survivor residue, and records the best valuation in (6).

An independent optimized C++ replay uses the exact 64-bit actual survivor
residue

```text
X mod 2^64 = 0x7fe13f3088c146c7
```

and enumerates every distinct arithmetic state through normalized word length
26. The largest complete pair matches are:

```text
phase p:
  length <=20: at most 10 pairs
  length  21: first 11-pair witness
  length <=26: still at most 11 pairs

phase u:
  length <=25: at most 10 pairs
  length  26: first 11-pair witness
  length <=26: at most 11 pairs
```

Therefore the exact actual-prefix consequences are

```text
kappa_p(q_actual,11)=21,
kappa_u(q_actual,11)=26,
kappa(q_actual,11)=21,

kappa_p(q_actual,12)>=27,
kappa_u(q_actual,12)>=27,
kappa(q_actual,12)>=27.                            (7)
```

The replay is finite. In particular, (7) is not an infinite divergence theorem.

## 8. Research consequence

The witness-complexity problem now has three nested levels:

```text
raw words:          growth 3^N,
arithmetic quotient: growth at most (1+sqrt(2))^N,
actual orbit:       exact exclusions through N=26.
```

The quotient removes a large family of exact word collisions and gives a faster
route to deeper controlled exclusions. More importantly, it identifies the next
structural target:

> Prove an actual-fringe-specific sub-Pell bound, or a recurring valuation
> obstruction, that forces the maximum in (6) to remain below `2L` whenever
> `N` is bounded relative to `L`.

A further generic counting improvement alone will still not settle the one
deterministic schedule. The missing step must use a property of the
zero-initialized fringe orbit, not merely parity of arbitrary arithmetic states.

## 9. Scientific boundary

This result does not prove that witness complexity diverges on the actual
schedule, prove that the alternating inverse lift has infinite support, exclude
eventual center period two, or solve Rule 30 center nonperiodicity.

It supplies an exact quotient theorem, an improved almost-sure rate, and deeper
finite actual-prefix certificates.
