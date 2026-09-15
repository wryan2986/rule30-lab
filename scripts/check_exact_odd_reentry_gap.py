#!/usr/bin/env python3
"""Check the exact leading-four-bit formula for odd corridor re-entry gaps."""


def T(x: int) -> int:
    return x ^ ((x << 1) | (x << 2))


def iterate(x: int, n: int) -> int:
    for _ in range(n):
        x = T(x)
    return x


def H_from_prefix4(prefix: int) -> int:
    assert 8 <= prefix <= 15
    return int(prefix in (0b1101, 0b1110, 0b1111))


def main() -> None:
    # Exhaust every fringe for modest word sizes and every odd long gap.
    checked = 0
    for m in range(6, 17):
        mask = (1 << m) - 1
        for G in range(3, m, 2):
            D = G // 2
            L = m - G
            if L < 4:
                continue
            for R in range(1 << (L - 1), 1 << L):
                prefix4 = R >> (L - 4)
                H = H_from_prefix4(prefix4)
                Rp = iterate(R, D + 2) & mask
                assert Rp != 0
                Gp = m - Rp.bit_length()
                predicted = 1 ^ H ^ (D & 1)
                assert Gp == predicted, (m, G, R, prefix4, Gp, predicted)
                checked += 1

    print(f"checked {checked} odd-gap fringe transports")
    print("exact formula G' = 1 xor H(R) xor (D mod 2): PASS")


if __name__ == "__main__":
    main()
