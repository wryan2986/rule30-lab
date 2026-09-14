#!/usr/bin/env python3
"""Verify the collision-mask and fringe-endpoint re-entry formulas.

Uses only the standard library.  The p=8 finite-extension graph is exact:
A^8(x)=x is a radius-16 finite-type constraint, and reverse reachability to
zero finds precisely the low states that extend to finite fixed words.
"""

from collections import deque


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
    R = iterate(T, z, p) - (z << (2 * p))
    if R <= 0:
        return R, None
    return R, 2 * p - R.bit_length()


def collision_data(z: int, p: int, G: int):
    D = G // 2
    x = iterate(T, z, D + 1)
    defect = iterate(A, x, p) ^ x
    reentry = iterate(A, T(x), p) == T(x)
    return D, x, defect, reentry


def predicted_collision_defect(R: int, G: int) -> int:
    if G & 1:
        return 1
    return 3 if (R & 1) == 0 else 1


def leading4(R: int) -> int:
    return R >> (R.bit_length() - 4)


def H(R: int) -> int:
    return 1 if leading4(R) in (0b1101, 0b1110, 0b1111) else 0


def predicted_reentry(p: int, R: int, G: int) -> bool | None:
    D = G // 2

    if G & 1:
        if G < 3:
            return None
        target = 1 if ((p + D) & 1) == 0 else 3
        return (R & 3) == target

    if G < 4:
        return None

    if R & 1:
        return False

    target_low = 2 if ((p + D) & 1) == 0 else 6
    return (R & 7) == target_low and H(R) == (D & 1)


def extension_graph(p: int):
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


def small_direct_scan(limit: int = 500_000, pmax: int = 8):
    checked_defects = 0
    checked_reentry = 0
    for z in range(1, limit):
        p = exact_period(z, pmax)
        if p is None:
            continue
        R, G = return_data(z, p)
        if R <= 0 or G is None or G <= 0:
            continue

        D, x, defect, reentry = collision_data(z, p, G)
        assert defect == predicted_collision_defect(R, G), (
            "defect mismatch", z, p, R, G, defect
        )
        checked_defects += 1

        pred = predicted_reentry(p, R, G)
        if pred is not None:
            assert reentry == pred, (
                "reentry mismatch", z, p, R, G, D, x, defect, reentry, pred
            )
            checked_reentry += 1

    return checked_defects, checked_reentry


def exact_p8_check():
    p = 8
    reachable, successor = extension_graph(p)
    checked = 0
    reentries = []

    for q, ok in enumerate(reachable):
        if not ok:
            continue
        R = fringe_from_low_state(q, p)
        if R <= 0:
            continue
        G = 2 * p - R.bit_length()
        if G < 4 or (G & 1):
            continue

        z = reconstruct_finite_word(q, p, successor)
        if exact_period(z, p) != p:
            continue

        D, x, defect, reentry = collision_data(z, p, G)
        assert defect == predicted_collision_defect(R, G), (
            "p8 defect mismatch", z, R, G, defect
        )
        pred = predicted_reentry(p, R, G)
        assert pred is not None
        assert reentry == pred, (
            "p8 reentry mismatch", z, R, G, D, x, defect, reentry, pred
        )
        checked += 1
        if reentry:
            reentries.append((R, G, leading4(R), R & 7))

    return checked, reentries


def main():
    defect_n, reentry_n = small_direct_scan()
    print(f"small direct scan: {defect_n} collision masks verified")
    print(f"small direct scan: {reentry_n} long-corridor reentry cases verified")

    checked, reentries = exact_p8_check()
    print(f"p=8 exact finite-extension check: {checked} even G>=4 states")
    print(f"p=8 immediate reentries: {len(reentries)}")
    for row in reentries:
        R, G, top4, low3 = row
        print(f"  R={R} ({R:b}), G={G}, top4={top4:04b}, low3={low3:03b}")


if __name__ == "__main__":
    main()
