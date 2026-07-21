# Mathematical background and conventions

## Local map

For `(left, center, right) in {0,1}^3`, write

```text
F(left, center, right) = left XOR (center OR right).
```

Its outputs for neighborhoods `111, 110, 101, 100, 011, 010, 001, 000` are
`0,0,0,1,1,1,1,0`, the standard Rule 30 truth table.

## Light cone and rows

With the single-cell seed, row `t` is zero outside `[-t,t]`. A complete finite
row is therefore represented in increasing spatial coordinate from `-t` to
`t`, for exactly `2t+1` bits. The center is index `t` in that representation.

## Left permutivity

Holding `center` and `right` fixed, XOR with `left` is a bijection. If

```text
next = left XOR (center OR right),
```

then XORing both sides with `(center OR right)` gives

```text
left = next XOR (center OR right).
```

This identity drives sideways reconstruction. Its local correctness is
elementary; claims about an unbounded reconstructed half-line require separate
arguments.

## Eventually-all-one candidate lemma

If `c_t = c_(t+1) = 1`, then at site zero

```text
1 = x_-1(t) XOR (1 OR x_1(t)) = x_-1(t) XOR 1,
```

so `x_-1(t) = 0`. Consequently, an eventually constant-one center tail forces
the immediately adjacent left column to be eventually zero. This is a local
partial lemma only. Any deduction using a published width-two theorem remains
conditional until the exact theorem and all hypotheses are checked.
