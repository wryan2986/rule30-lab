# Complete local canonical quotients for period-two witnesses

Status: complete informal proof of the equal-length locality lemma, the
fixed-span canonical reduction, regular-language arithmetic-image bounds, and
the exact span-five below-binary certificate. These are generic structural
results. They do not prove divergence for the deterministic zero-initialized
fringe survivor and do not solve Rule 30 center nonperiodicity.

## 1. Arithmetic witness maps

For an ordinary nonnegative state `x`, write

```text
T(x) = x XOR ((x << 1) OR (x << 2)).
```

The three forward generators are

```text
t(x) = T(x),
u(x) = T(x) XOR 1,
p(x) = T(x) XOR 1 XOR (2 if x is even else 0).
```

A normalized inverse word `G` begins with `p` or `u`, acts from left to right,
and represents the arithmetic state

```text
x(G) = G^(-1)(0).
```

The preceding arithmetic-quotient results used a small hand-selected family of
state-conditioned relations. The present construction uses every same-length
relation through a chosen local span.

## 2. Equal-length locality lemma

Suppose two inputs `x,y` satisfy

```text
x XOR y < 2^k.
```

They agree in every bit position `i>=k`. Output bit `i` of `T` depends only on
input bits `i,i-1,i-2`. Therefore, for `i>=k+2`,

```text
bit_i(T(x)) = bit_i(T(y)).
```

The corrections distinguishing `t,p,u` live only in output bits zero and one.
Consequently, for arbitrary generator letters `a,b`,

```text
x XOR y < 2^k
    implies
 a(x) XOR b(y) < 2^max(k+2,2).                    (1)
```

Start two equal-length words `v,w` of length `m` from the same input. After the
first letters their outputs differ below bit two. Repeated application of (1)
gives

```text
v(x) XOR w(x) < 2^(2m).                           (2)
```

The maps are triangular from low bits to high bits, so the lowest `2m` output
bits of either word depend only on `x mod 2^(2m)`. Combining this with (2)
gives the exact finite-table theorem:

> **Equal-length locality.** For words `v,w` of common length `m`, whether
> `v(x)=w(x)` is determined exactly by `x mod 4^m`. Equality modulo `4^m`
> implies equality as ordinary integers because the two outputs cannot differ
> above that modulus.

Thus a complete all-width identity table for length `m` is obtained by checking
only the `4^m` starting residues and `3^m` words.

## 3. Complete span-s reduction

Fix a span `s`. For every

```text
1 <= m <= s,
r in Z/(4^m),
```

and every length-`m` word `v`, choose

```text
min(r,v)
```

to be the lexicographically least word, under `t<u<p`, having the same output
as `v` from residue `r` modulo `4^m`.

By the locality lemma, if an occurrence of `v` begins after a prefix whose
arithmetic state is `r mod 4^m`, then replacing it by `min(r,v)` preserves the
complete ordinary arithmetic state represented by the whole word. The
replacement also preserves total word length and strictly decreases the whole
word lexicographically whenever it changes the block.

Repeatedly replace the first nonminimal block of length at most `s`. The process
must terminate because there are only finitely many words of the fixed total
length and each replacement strictly decreases the word.

The terminal word is **span-s locally canonical**: every block of length at
most `s` is lexicographically minimal at its exact starting residue.
Confluence is unnecessary. Existence of one canonical representative for every
arithmetic state is sufficient for counting.

## 4. Finite automaton

All generator maps are permutations modulo `4^s`. To decide whether appending a
letter creates a nonminimal suffix of length at most `s`, an automaton need only
remember

```text
(current arithmetic residue mod 4^s,
 last at most s-1 letters).
```

After appending a letter, invert the candidate suffix through the generator
permutations modulo `4^s` to recover its exact starting residue. The finite
identity table then accepts or rejects the suffix.

Hence the span-`s` canonical words form a regular language. Let `A_s` be the
reachable adjacency matrix after the initial phase letter and let

```text
lambda_s = spectral radius(A_s).
```

Every fixed-phase arithmetic state of normalized length `N` has a canonical
representative accepted by this automaton. Therefore

```text
# arithmetic states of phase a and length N = O(lambda_s^N).  (3)
```

Increasing `s` adds all shorter-span rules and possibly more, so

```text
lambda_(s+1) <= lambda_s.                         (4)
```

## 5. Exact finite hierarchy

The executable construction gives

```text
span    modulus    reachable states    lambda_s (approx.)
  1         4              6           2.414213562373095
  2        16             40           2.211188613748176
  3        64            332           2.083700790873340
  4       256          2,718           2.026379512399217
  5     1,024         21,615           1.983711482571876
```

Span one recovers the parity/Pell quotient. Spans two through five use the
complete local equality tables, not a selected relation list.

At normalized length eighteen, the span-five language contains

```text
phase p: 148,083 canonical words
phase u: 131,940 canonical words.
```

The exact arithmetic images contain only

```text
phase p: 75,905 states
phase u: 64,247 states,
```

so further nonlocal or longer-block collisions remain. The canonical language
is an upper bound, not a unique normal form.

## 6. Exact below-binary certificate

A numerical eigenvalue alone is not used to prove `lambda_5<2`. Starting from
every reachable span-five automaton state, count all accepted continuations of
length 112. The exact maximum is

```text
M = 5184503427587892562141101478138477.
```

But

```text
2^112 = 5192296858534827628530496329220096,
```

and therefore

```text
M < 2^112.                                         (5)
```

The maximum row sum of `A_5^112` is exactly `M`. By the standard spectral-radius
bound,

```text
lambda_5^112 <= ||A_5^112||_infinity = M < 2^112,
```

so

```text
lambda_5 < 2.                                      (6)
```

This is an integer certificate over the complete 21,615-state graph. It is not
a floating-point inference.

## 7. Witness-complexity consequence

The schedule-to-boundary prefix map is injective, and one arithmetic state has
one dual zero-target boundary prefix. Equation (3) therefore bounds the number
of length-`L` driver prefixes admitting a phase witness of length at most `N`
by `O(lambda_5^N)`.

Under fair Bernoulli measure on driver schedules, Borel-Cantelli gives

```text
liminf_(L->infinity) kappa_a(q,L)/L
    >= log(2)/log(lambda_5).                       (7)
```

Numerically,

```text
log(2)/log(lambda_5) ~= 1.011938638805349.
```

The qualitative point follows already from (6): the generic witness must grow
strictly faster than one generator letter per tested future block. The earlier
canonical quotient gave only `0.85617` letters per block.

## 8. Scientific boundary

The span-five threshold is generic. A language of exponential rate below two
can still contain the one deterministic zero-initialized fringe path. The
result does not prove

```text
kappa_p(q_actual,L) -> infinity
or
kappa_u(q_actual,L) -> infinity.
```

It does, however, narrow the exceptional set substantially and supplies a
systematic hierarchy rather than isolated relations. The next useful step is
either to extend the complete local hierarchy, identify an actual-fringe factor
absent from every bounded-complexity canonical path, or construct a
cross-characteristic invariant coupling the canonical arithmetic word to the
zero-initialized fringe orbit.
