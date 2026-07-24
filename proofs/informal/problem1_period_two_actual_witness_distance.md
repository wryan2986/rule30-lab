# Exact actual witness distances through depth twenty

Status: complete finite-quotient distance theorem and exact controlled campaign.
This result strengthens the actual-orbit diagnostics but does not prove that the
witness complexity diverges.

## 1. Arithmetic target at depth `L`

Let `X` be the unique 2-adic zero survivor for the zero-initialized moving-fringe
schedule, and write

```text
X_L = X mod 4^L.
```

The first `L` pair digits of `X` are exactly its lowest `2L` bits. For a
normalized inverse word `G`, put

```text
x(G) = G^(-1)(0),
```

using the ordinary forward arithmetic generators. The schedule-survivor and
dual-cut theorems give

```text
G kills the first L actual boundary pairs
    iff
x(G) = X_L mod 4^L.                                      (1)
```

This converts the depth problem from the four-letter dual tree to one finite
arithmetic quotient.

## 2. Phase starts

A normalized phase-`p` word begins with `p`, and

```text
p(0)=3.
```

A normalized phase-`u` word begins with `u`, and

```text
u(0)=1.
```

Let `d_L(a,b)` be directed distance from `a` to `b` in the positive-generator
graph modulo `4^L`, with edges

```text
x -> t(x), p(x), u(x).
```

Equation (1) immediately yields the exact identities

```text
kappa_p(actual,L) = 1 + d_L(3,X_L),
kappa_u(actual,L) = 1 + d_L(1,X_L).                      (2)
```

The leading `1` counts the prescribed phase letter.

## 3. Exact inverse edges

Each generator is unit triangular on low bits and therefore a permutation
modulo every power of two. The inverse of

```text
t(x)=x XOR ((x<<1) OR (x<<2))
```

is recovered from low to high: once bits below position `i` are known, output
bit `i` determines input bit `i` uniquely. The `u` inverse first toggles output
bit zero. For `p`, output bit zero determines the recovered input parity, which
then determines whether output bit one must also be toggled before applying the
`t` inverse.

Thus reverse breadth-first search from `X_L` follows the exact inverse edges of
the positive graph; it does not enlarge the generating set.

## 4. Sparse bidirectional certificate

Fix a reverse radius `R`. Build the complete reverse ball

```text
B_R = {x : d_L(x,X_L) <= R}
```

and record every exact reverse distance. Independently enumerate complete
forward BFS layers from phase start `3` or `1`.

If a forward layer at distance `i` meets a state of reverse distance `j`, then
there is a witness of total length

```text
1+i+j.
```

Suppose the best value found is `D`. Once every forward layer through

```text
D-1-R
```

has been exhausted, `D` is minimal. Indeed, any shorter path has at most `D-2`
post-phase edges; split it `R` edges before its target (or at its start if it is
shorter). The split vertex lies both in the completed forward layers and in
`B_R`, so that path would already have produced a smaller candidate.

This is an exact lower-and-upper certificate while visiting only the two search
balls, rather than all `4^L` quotient states.

## 5. Exact actual values

The Python reference campaign independently checks depths one through twelve.
The sparse C++ campaign extends the same theorem through depth twenty.

| `L` | `X_L` (hex) | `kappa_p` | `kappa_u` | either phase |
|---:|---:|---:|---:|---:|
| 1 | `0x3` | 1 | 2 | 1 |
| 2 | `0x7` | 3 | 2 | 2 |
| 3 | `0x7` | 7 | 2 | 2 |
| 4 | `0xc7` | 8 | 7 | 7 |
| 5 | `0x2c7` | 8 | 12 | 8 |
| 6 | `0x6c7` | 12 | 14 | 12 |
| 7 | `0x46c7` | 13 | 14 | 13 |
| 8 | `0x46c7` | 17 | 14 | 14 |
| 9 | `0x146c7` | 17 | 18 | 17 |
| 10 | `0x146c7` | 17 | 19 | 17 |
| 11 | `0x146c7` | 21 | 26 | 21 |
| 12 | `0xc146c7` | 28 | 27 | 27 |
| 13 | `0xc146c7` | 30 | 30 | 30 |
| 14 | `0x8c146c7` | 33 | 30 | 30 |
| 15 | `0x8c146c7` | 34 | 30 | 30 |
| 16 | `0x88c146c7` | 36 | 30 | 30 |
| 17 | `0x88c146c7` | 40 | 40 | 40 |
| 18 | `0x88c146c7` | 40 | 42 | 40 |
| 19 | `0x3088c146c7` | 42 | 42 | 42 |
| 20 | `0x3088c146c7` | 47 | 49 | 47 |

The plateaus are exact, not search failures. When newly exposed survivor pair
bits are zero, an existing shortest word can continue to match several deeper
quotients. A later nonzero pair forces the next jump.

## 6. Reproduction

```bash
python3 -m pytest -q tests/python/test_period_two_actual_witness_distance.py
python3 experiments/problem1_nonperiodicity/analyze_period_two_actual_witness_distance.py

g++ -O3 -std=c++20 \
  experiments/problem1_nonperiodicity/analyze_period_two_actual_witness_distance.cpp \
  -o /tmp/rule30-actual-witness-distance
/tmp/rule30-actual-witness-distance 12 20
```

The Python certificate is

```text
fafe057b3a193a61af2ef4a3107b2c43029e6f2222a4fb32efb0dd71e0071f18
```

and the exact C++ output hash is

```text
ea6c9d16dcfd1b233dcf089fbbdba06828d7e9f2d0d1dc3c5ccea4f9aabc809b
```

The depth-20 run uses a sparse reverse ball and reached a maximum resident set
below 800 MiB in the controlled environment.

## 7. Scientific boundary

The table gives exact finite values only. It does not prove that either phase
distance tends to infinity, that the alternating inverse lift has infinite
support, that eventual center period two is impossible, or that the Rule 30
center column is nonperiodic.

The next infinite target is now especially concrete: find an actual-orbit
quantity that forces new nonzero pair constraints often enough that the phase
distances cannot plateau forever. Candidate routes are a valuation recurrence
at the nonzero survivor pairs or a cross-characteristic relation tying those
pair positions to the zero-initialized fringe return system.
