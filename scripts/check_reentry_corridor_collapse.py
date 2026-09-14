#!/usr/bin/env python3
"""Exact p=4/p=8 finite-state check for immediate-reentry corridor collapse."""

from collections import Counter, deque


def T(x: int) -> int:
    return x ^ ((x << 1) | (x << 2))


def A(x: int) -> int:
    return T(x) >> 2


def iterate(f, x: int, n: int) -> int:
    for _ in range(n):
        x = f(x)
    return x


def exact_period(x: int, pmax: int) -> int | None:
    y = x
    for p in range(1, pmax + 1):
        y = A(y)
        if y == x:
            return p
    return None


def extension_graph(p: int):
    m = 2 * p
    n = 1 << m
    reverse = [[] for _ in range(n)]

    for state in range(n):
        for bit in (0, 1):
            block = state | (bit << m)
            if (iterate(A, block, p) & 1) != (state & 1):
                continue
            nxt = (block >> 1) & (n - 1)
            reverse[nxt].append((state, bit))

    reachable = [False] * n
    successor = [None] * n
    reachable[0] = True
    queue = deque([0])
    while queue:
        nxt = queue.popleft()
        for state, bit in reverse[nxt]:
            if reachable[state]:
                continue
            reachable[state] = True
            successor[state] = (nxt, bit)
            queue.append(state)
    return reachable, successor


def fringe_from_low_state(q: int, p: int) -> int:
    mask = (1 << (2 * p)) - 1
    x = q
    for _ in range(p):
        x = T(x) & mask
    return x


def reconstruct(q: int, p: int, successor) -> int:
    m = 2 * p
    state = q
    z = q
    pos = m
    while state:
        nxt, bit = successor[state]
        if bit:
            z |= 1 << pos
        state = nxt
        pos += 1
    return z


def census(p: int):
    m = 2 * p
    mask = (1 << m) - 1
    reachable, successor = extension_graph(p)
    counts = Counter()
    checked = 0

    for q, ok in enumerate(reachable):
        if not ok:
            continue
        R = fringe_from_low_state(q, p)
        if R <= 0:
            continue
        G = m - R.bit_length()
        if G < 3:
            continue

        z = reconstruct(q, p, successor)
        if exact_period(z, p) != p:
            continue

        D = G // 2
        x = iterate(T, z, D + 1)
        zp = T(x)
        if iterate(A, zp, p) != zp:
            continue

        # Exact transported-fringe identity.
        Rp_direct = iterate(T, zp, p) - (zp << m)
        Rp_transport = iterate(T, R, D + 2) & mask
        assert Rp_direct == Rp_transport, (p, z, R, G, Rp_direct, Rp_transport)

        Gp = m - Rp_direct.bit_length() if Rp_direct else m
        counts[(G, Gp)] += 1
        checked += 1

        # Proven collapse range.
        if G % 2 == 0 and G >= 4:
            assert Gp == 0, (p, z, R, G, Rp_direct, Gp)
        if G % 2 == 1 and G >= 5:
            assert Gp <= 1, (p, z, R, G, Rp_direct, Gp)

    return checked, counts


def main():
    for p in (4, 8):
        checked, counts = census(p)
        print(f"p={p}: {checked} immediate reentries from G>=3")
        for key in sorted(counts):
            print(f"  G={key[0]} -> G'={key[1]}: {counts[key]}")


if __name__ == "__main__":
    main()
