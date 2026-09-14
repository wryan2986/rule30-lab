#!/usr/bin/env python3
"""Verify the run-28 exact quotient/commutator and four-bit fringe-core formulas.

Standard library only.
"""


def T(x: int) -> int:
    return x ^ ((x << 1) | (x << 2))


def A(x: int) -> int:
    return T(x) >> 2


def iterate(f, x: int, n: int) -> int:
    for _ in range(n):
        x = f(x)
    return x


def c(s: int) -> int:
    a = s & 1
    b = (s >> 1) & 1
    q = (s >> 2) & 1
    return (a | b) | ((b & (1 - q)) << 1)


def invT_mod(y: int, bits: int) -> int:
    x = 0
    for i in range(bits):
        yi = (y >> i) & 1
        x1 = (x >> (i - 1)) & 1 if i >= 1 else 0
        x2 = (x >> (i - 2)) & 1 if i >= 2 else 0
        xi = yi ^ (x1 | x2)
        x |= xi << i
    return x


def invT_power_mod(y: int, steps: int, bits: int) -> int:
    for _ in range(steps):
        y = invT_mod(y, bits)
    return y


def commutator_direct(x: int, k: int) -> int:
    return iterate(A, T(x), k) ^ T(iterate(A, x, k))


def fringe_core_direct(R: int) -> int:
    L = R.bit_length()
    assert L >= 4 and L % 2 == 0
    n = L // 2
    y = invT_power_mod(R, n - 1, L)
    return commutator_direct(y, n - 1)


def main():
    # General one-step quotient identity.
    for Y in range(1 << 14):
        for h in range(2, 13):
            lhs = (T(Y) >> h) ^ T(Y >> h)
            rhs = c((Y >> (h - 2)) & 7)
            assert lhs == rhs, (Y, h, lhs, rhs)
    print("quotient identity: exhaustive Y<2^14, 2<=h<=12: OK")

    # A^k(x) equals a final quotient of the physical iterate.
    for x in range(1 << 12):
        for k in range(8):
            assert iterate(A, x, k) == (iterate(T, x, k) >> (2 * k))
    print("normalized/physical quotient identity: exhaustive x<2^12, k<8: OK")

    # Closed k-step commutator formula.
    for x in range(1 << 12):
        for k in range(1, 8):
            lhs = commutator_direct(x, k)
            Y = iterate(T, x, k)
            rhs = c((Y >> (2 * k - 2)) & 7)
            assert lhs == rhs, (x, k, lhs, rhs)
    print("closed commutator formula: exhaustive x<2^12, 1<=k<8: OK")

    # Exact top-four-bit fringe-core classification for all even lengths <=18.
    table = {}
    for L in range(4, 20, 2):
        counts = {}
        for R in range(1 << (L - 1), 1 << L):
            observed = fringe_core_direct(R)
            predicted = c((R >> (L - 4)) & 7)
            assert observed == predicted, (L, R, observed, predicted)
            prefix = R >> (L - 4)
            counts.setdefault(prefix, set()).add(observed)
        table[L] = counts
    print("four-bit fringe-core formula: exhaustive even bitlengths 4..18: OK")
    print("stable prefix table:")
    for prefix in range(8, 16):
        vals = table[18][prefix]
        print(f"  {prefix:04b} -> {sorted(vals)}")


if __name__ == "__main__":
    main()
