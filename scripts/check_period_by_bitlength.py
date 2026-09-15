#!/usr/bin/env python3
"""Group exact finite A-cycle periods by bitlength for p <= 8."""
from collections import defaultdict, deque


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


def main():
    p = 8
    reachable, successor = extension_graph(p)
    by_period = defaultdict(lambda: defaultdict(int))
    for q, ok in enumerate(reachable):
        if not ok or q == 0:
            continue
        z = reconstruct(q, p, successor)
        ep = exact_period(z, p)
        by_period[ep][z.bit_length()] += 1

    for ep in sorted(by_period):
        counts = by_period[ep]
        lengths = sorted(counts)
        distinct_counts = sorted(set(counts.values()))
        contiguous = lengths == list(range(lengths[0], lengths[-1] + 1))
        print(
            f"period {ep}: states={sum(counts.values())}, "
            f"lengths={lengths[0]}..{lengths[-1]}, "
            f"nlengths={len(lengths)}, counts/length={distinct_counts}, "
            f"contiguous={contiguous}"
        )


if __name__ == "__main__":
    main()
