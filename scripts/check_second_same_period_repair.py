#!/usr/bin/env python3
"""Exact p=4/p=8 census for second same-period repairs after a repaired long corridor."""

from collections import Counter, deque


def T(x):
    return x ^ ((x << 1) | (x << 2))


def A(x):
    return T(x) >> 2


def iterate(f, x, n):
    for _ in range(n):
        x = f(x)
    return x


def exact_period(x, pmax):
    y = x
    for p in range(1, pmax + 1):
        y = A(y)
        if y == x:
            return p
    return None


def extension_graph(p):
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


def reconstruct(q, p, successor):
    m = 2 * p
    state, z, pos = q, q, m
    while state:
        nxt, bit = successor[state]
        if bit:
            z |= 1 << pos
        state, pos = nxt, pos + 1
    return z


def fringe(z, p):
    return iterate(T, z, p) - (z << (2 * p))


def census(p):
    m = 2 * p
    reachable, successor = extension_graph(p)
    counts = Counter()
    longest = (0, None)
    for q, ok in enumerate(reachable):
        if not ok:
            continue
        z = reconstruct(q, p, successor)
        if exact_period(z, p) != p:
            continue
        R = fringe(z, p)
        if R <= 0:
            continue
        G = m - R.bit_length()
        if G < 3:
            continue
        D = G // 2
        zp = iterate(T, z, D + 2)
        if iterate(A, zp, p) != zp:
            continue

        y = T(zp)
        second = iterate(A, T(y), p) == T(y)
        Rp = fringe(zp, p)
        Gp = m - Rp.bit_length()
        counts[(G, Gp, second)] += 1

        w = zp
        fixed_nodes = 0
        while fixed_nodes < 100 and iterate(A, w, p) == w:
            fixed_nodes += 1
            w = T(T(w))
        if fixed_nodes > longest[0]:
            longest = (fixed_nodes, (z, G, R, zp))
    return counts, longest


def main():
    for p in (4, 8):
        counts, longest = census(p)
        print(f"p={p}")
        for key in sorted(counts):
            print(f"  G={key[0]} G'={key[1]} second={key[2]}: {counts[key]}")
        print("  longest alternating fixed-node train:", longest)


if __name__ == "__main__":
    main()
