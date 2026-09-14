#!/usr/bin/env python3
"""Check the run-27 fringe-determinism and core-commutator reduction.

Standard library only. Exhaustively verifies deterministic A^p-fixed extension
for p<=8, then checks the fringe-core formula against every exact-period-8
11-leading even-corridor state from the finite-type graph.
"""

from collections import Counter, deque


def T(x: int) -> int:
    return x ^ ((x << 1) | (x << 2))


def A(x: int) -> int:
    return T(x) >> 2


def iterate(f, x: int, n: int) -> int:
    for _ in range(n):
        x = f(x)
    return x


def exact_period(x: int, pmax: int):
    y = x
    for p in range(1, pmax + 1):
        y = A(y)
        if y == x:
            return p
    return None


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


def F(d: int, s: int) -> int:
    a = d & 1
    b = (d >> 1) & 1
    x = s & 1
    y = (s >> 1) & 1
    z = (s >> 2) & 1
    ap = (a ^ x) | (b ^ y)
    bp = (b ^ y) & (1 - z)
    return ap | (bp << 1)


def fringe_core(R: int) -> int:
    L = R.bit_length()
    assert L % 2 == 0
    n = L // 2
    y = invT_power_mod(R, n - 1, L)
    d = 0
    u = y
    for _ in range(n - 1):
        d = F(d, T(u) & 7)
        u = A(u)
    return d


def unique_extension_check(p: int):
    m = 2 * p
    mask = (1 << m) - 1
    counts = Counter()
    for state in range(1 << m):
        legal = 0
        for b in (0, 1):
            block = state | (b << m)
            if (iterate(A, block, p) & 1) == (state & 1):
                legal += 1
        counts[legal] += 1
    assert counts == Counter({1: 1 << m}), (p, counts)
    return counts


def extension_graph(p: int):
    m = 2 * p
    nstates = 1 << m
    mask = nstates - 1
    reverse = [[] for _ in range(nstates)]
    for state in range(nstates):
        for b in (0, 1):
            block = state | (b << m)
            if (iterate(A, block, p) & 1) != (state & 1):
                continue
            nxt = (block >> 1) & mask
            reverse[nxt].append((state, b))

    reachable = [False] * nstates
    successor = [None] * nstates
    reachable[0] = True
    q = deque([0])
    while q:
        nxt = q.popleft()
        for state, b in reverse[nxt]:
            if reachable[state]:
                continue
            reachable[state] = True
            successor[state] = (nxt, b)
            q.append(state)
    return reachable, successor


def reconstruct(q: int, p: int, successor) -> int:
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


def fringe(q: int, p: int) -> int:
    mask = (1 << (2 * p)) - 1
    x = q
    for _ in range(p):
        x = T(x) & mask
    return x


def actual_dp(z: int, p: int, G: int) -> int:
    D = G // 2
    x = iterate(T, z, D + 1)
    d = 0
    u = x
    for _ in range(p):
        d = F(d, T(u) & 7)
        u = A(u)
    return d


def check_p8_core_formula():
    p = 8
    reachable, successor = extension_graph(p)
    checked = 0
    by_G = Counter()
    g4_prefix = Counter()

    for q, ok in enumerate(reachable):
        if not ok:
            continue
        R = fringe(q, p)
        if R <= 0:
            continue
        G = 2 * p - R.bit_length()
        if G < 4 or G % 2:
            continue
        if R >> (R.bit_length() - 2) != 3:
            continue

        z = reconstruct(q, p, successor)
        if exact_period(z, p) != p:
            continue

        D = G // 2
        C = fringe_core(R)
        predicted = (1 if C != 1 else 0) ^ (D & 1)
        observed = actual_dp(z, p, G)
        assert predicted == observed, (q, R, G, C, predicted, observed)

        checked += 1
        by_G[G] += 1
        if G == 4:
            prefix4 = R >> (R.bit_length() - 4)
            g4_prefix[(prefix4, observed)] += 1

    return checked, by_G, g4_prefix


def main():
    print("Unique extension check")
    for p in range(1, 9):
        counts = unique_extension_check(p)
        print(f"  p={p}: {dict(counts)}")

    checked, by_G, g4_prefix = check_p8_core_formula()
    print("\np=8 fringe-core formula")
    print("  exact-period-8 11-leading even corridors checked:", checked)
    print("  by G:", dict(sorted(by_G.items())))
    print("  G=4 (four-bit prefix, d_p) counts:")
    for key in sorted(g4_prefix):
        print("   ", key, g4_prefix[key])


if __name__ == "__main__":
    main()
