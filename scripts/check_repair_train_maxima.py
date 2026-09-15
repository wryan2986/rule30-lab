#!/usr/bin/env python3
"""Exact finite-extension census of same-period alternating repair trains.

Builds the A^p-fixed finite-extension graph, reconstructs every finite fixed
word, and measures consecutive fixed/collision/fixed nodes under T^2.
Intended for p <= 8; p=8 uses 65536 low states.
"""
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
        for b in (0, 1):
            block = state | (b << m)
            if (iterate(A, block, p) & 1) != (state & 1):
                continue
            nxt = (block >> 1) & (n - 1)
            reverse[nxt].append((state, b))
    reachable = [False] * n
    successor = [None] * n
    reachable[0] = True
    queue = deque([0])
    while queue:
        nxt = queue.popleft()
        for state, b in reverse[nxt]:
            if reachable[state]:
                continue
            reachable[state] = True
            successor[state] = (nxt, b)
            queue.append(state)
    return reachable, successor


def reconstruct(q, p, successor):
    m = 2 * p
    state, z, pos = q, q, m
    while state:
        nxt, b = successor[state]
        if b:
            z |= 1 << pos
        state, pos = nxt, pos + 1
    return z


def return_data(z, p):
    tp = iterate(T, z, p)
    R = tp - (z << (2 * p))
    G = 2 * p - R.bit_length() if R else None
    return R, G


def repair_train(z, p):
    out = []
    while iterate(A, z, p) == z:
        R, G = return_data(z, p)
        out.append((z, R, G))
        y = T(z)
        if iterate(A, y, p) == y:
            break
        z = T(y)
    return out


def census(p):
    reachable, successor = extension_graph(p)
    periods = Counter()
    best = []
    max_len = 0
    for q, ok in enumerate(reachable):
        if not ok or q == 0:
            continue
        z = reconstruct(q, p, successor)
        ep = exact_period(z, p)
        periods[ep] += 1
        if ep != p:
            continue
        train = repair_train(z, p)
        n = len(train)
        if n > max_len:
            max_len, best = n, [(z, train)]
        elif n == max_len:
            best.append((z, train))
    return periods, max_len, best


def main():
    for p in (1, 2, 3, 4, 5, 6, 7, 8):
        periods, max_len, best = census(p)
        print(f"p={p}: period spectrum {dict(sorted(periods.items()))}; exact-p max train={max_len}")
        if max_len:
            print(f"  maximizers={len(best)}")
            for z, train in best[:2]:
                print(f"  z={z}")
                print("  fringes/gaps=" + repr([(R, G) for _, R, G in train]))


if __name__ == "__main__":
    main()
