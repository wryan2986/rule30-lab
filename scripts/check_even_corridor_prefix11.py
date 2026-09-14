#!/usr/bin/env python3
"""Reproduce the run-26 even-corridor prefix-11 counterexamples.

This script uses only Python's standard library.  It verifies the explicit
period-4/period-8 witnesses and builds the finite-type extension graph for
A^p(x)=x at p=4 and p=8.
"""

from collections import deque, Counter


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


def return_data(z: int, p: int):
    tp = iterate(T, z, p)
    R = tp - (z << (2 * p))
    G = 2 * p - R.bit_length() if R > 0 else None
    return R, G


def collision_data(z: int, p: int, G: int):
    D = G // 2
    x = iterate(T, z, D + 1)
    sources = []
    d = []
    for j in range(p + 1):
        uj = iterate(A, x, j)
        vj = iterate(A, T(x), j)
        d.append(vj ^ T(uj))
        if j < p:
            sources.append(T(uj) & 7)
    E = iterate(A, x, p) ^ x
    E_next = iterate(A, T(x), p) ^ T(x)
    return D, x, sources, d, E, E_next


def extension_graph(p: int):
    """Return states that can extend upward to a finite A^p-fixed word.

    A state stores 2p consecutive bits, low bit first.  A transition appends
    one higher bit and is legal iff the leftmost A^p(x)=x constraint holds.
    Reverse BFS from zero identifies precisely the low states that admit a
    finite extension.
    """
    m = 2 * p
    nstates = 1 << m
    reverse = [[] for _ in range(nstates)]

    for state in range(nstates):
        for b in (0, 1):
            block = state | (b << m)
            if (iterate(A, block, p) & 1) != (state & 1):
                continue
            nxt = (block >> 1) & (nstates - 1)
            reverse[nxt].append((state, b))

    reachable = [False] * nstates
    successor = [None] * nstates
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


def fringe_from_low_state(q: int, p: int) -> int:
    mask = (1 << (2 * p)) - 1
    x = q
    for _ in range(p):
        x = T(x) & mask
    return x


def reconstruct_finite_word(q: int, p: int, successor) -> int:
    m = 2 * p
    state = q
    z = q
    pos = m
    while state:
        nxt, b = successor[state]
        if b:
            z |= 1 << pos
        state = nxt
        pos += 1
    return z


def classify_p8():
    p = 8
    reachable, successor = extension_graph(p)
    bad = []
    branch_counts = Counter()

    for q, ok in enumerate(reachable):
        if not ok:
            continue
        R = fringe_from_low_state(q, p)
        if R <= 0:
            continue
        G = 2 * p - R.bit_length()
        if G < 4 or G % 2 or R >> (R.bit_length() - 2) != 3:
            continue

        z = reconstruct_finite_word(q, p, successor)
        period = exact_period(z, p)
        bad.append((q, R, G, period, z))
        if period == p:
            D, _, _, d, _, _ = collision_data(z, p, G)
            branch_counts[(G, d[p - D - 1], d[p])] += 1

    return bad, branch_counts


def main():
    explicit = [
        (3_650_443, 4),
        (7_476_107_372, 8),
        (6_723_037_797, 8),
    ]

    print("Explicit witnesses")
    for z, expected_p in explicit:
        p = exact_period(z, expected_p)
        R, G = return_data(z, p)
        print(f"z={z} p={p} R={R} bin(R)={R:b} G={G}")
        if G and G >= 4:
            D, _, sources, d, E, E_next = collision_data(z, p, G)
            print(f"  D={D} sources={sources}")
            print(f"  d={d} E={E} E(Tx)={E_next}")

    print("\nFinite-state p=4 check")
    reach4, _ = extension_graph(4)
    long4 = []
    impossible_11 = []
    for q in range(256):
        R = fringe_from_low_state(q, 4)
        if 8 <= R <= 15:
            if reach4[q]:
                long4.append((q, R))
            elif R >= 12:
                impossible_11.append((q, R))
    print("  extendable G=4 low states:", long4)
    print("  nonextendable 11-prefix candidates:", impossible_11)

    print("\nFinite-state p=8 check")
    bad8, counts = classify_p8()
    exact8 = [row for row in bad8 if row[3] == 8]
    print(f"  reachable 11-prefix even-corridor states: {len(bad8)}")
    print(f"  exact-period-8 states: {len(exact8)}")
    print("  (G, pre-suffix d, terminal d) counts:")
    for key in sorted(counts):
        print(f"    {key}: {counts[key]}")


if __name__ == "__main__":
    main()
