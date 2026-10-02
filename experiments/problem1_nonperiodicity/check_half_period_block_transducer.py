#!/usr/bin/env python3
from __future__ import annotations

def bits(x: int, n: int) -> str:
    return "".join("1" if (x >> i) & 1 else "0" for i in range(n))

def parity(x: int) -> int:
    return x.bit_count() & 1

def scalar_child(b: int, c: int, n: int) -> int:
    if b == 0:
        raise ValueError("nonzero low plane required")
    r = b.bit_length() - 1
    a0 = 1 ^ parity(c >> r)
    a = a0
    out = 0
    for s in range(n):
        out |= a << s
        a = ((c >> s) & 1) ^ (((b >> s) & 1) | a)
    if a != a0:
        raise AssertionError("cyclic response did not close")
    return out

def broad_child(b: int, c: int, n: int) -> int:
    if b == 0:
        raise ValueError("nonzero low plane required")
    mask = (1 << n) - 1
    r = b.bit_length() - 1
    a0 = 1 ^ parity(c >> r)
    D = (c ^ b) & mask
    M = (~b) & mask
    k = 1
    while k < n:
        lo = (1 << k) - 1
        od, om = D, M
        D = (od ^ (om & ((od << k) & mask))) & mask
        M = ((om & lo) | (om & ((om << k) & mask) & (~lo & mask))) & mask
        k <<= 1
    Y = D ^ (M & (mask if a0 else 0))
    return ((Y << 1) | a0) & mask

def block_paths(b: int, c: int, p: int):
    paths = []
    for seed in (0, 1):
        y = seed
        seq = [y]
        for s in range(p):
            y = ((c >> s) & 1) ^ (((b >> s) & 1) | y)
            seq.append(y)
        paths.append(tuple(seq))
    return tuple(paths)

def block_code(b: int, c: int, p: int):
    if b == 0:
        r = p
    else:
        r = (b & -b).bit_length() - 1
    y = 0
    q = 0
    for s in range(p):
        y = ((c >> s) & 1) ^ (((b >> s) & 1) | y)
        q |= y << s
    return r, q

def paths_from_code(r: int, q: int, p: int):
    out = []
    for seed in (0, 1):
        seq = [seed]
        for s in range(1, p + 1):
            y0 = (q >> (s - 1)) & 1
            dep = 1 if s <= r else 0
            seq.append(y0 ^ (seed & dep))
        out.append(tuple(seq))
    return tuple(out)

def portal_lift(w: int, p: int):
    cur = 0
    x = 0
    for s in range(2 * p):
        x |= cur << s
        cur ^= (w >> (s % p)) & 1
    if cur != 0:
        raise AssertionError("repeated odd word should integrate cyclically at doubled period")
    return x

def is_rotation(x: int, y: int, n: int) -> bool:
    mask = (1 << n) - 1
    for k in range(n):
        z = ((x >> k) | ((x << (n - k)) & mask)) & mask if k else x
        if z == y:
            return True
    return False

def first_zero_return(a: int, b: int, n: int, cap: int):
    for depth in range(cap + 1):
        if a == 0:
            return depth, b
        z = broad_child(a, b, n)
        b, a = a, z
    raise RuntimeError("cap reached")

def main():
    print("block_transducer_count_check")
    for p in range(1, 9):
        code_to_paths = {}
        paths_to_code = {}
        for b in range(1 << p):
            for c in range(1 << p):
                code = block_code(b, c, p)
                paths = block_paths(b, c, p)
                if paths_from_code(*code, p) != paths:
                    raise AssertionError(("code reconstruction mismatch", p, b, c, code))
                if code in code_to_paths and code_to_paths[code] != paths:
                    raise AssertionError(("same code, different path transducer", p, code))
                if paths in paths_to_code and paths_to_code[paths] != code:
                    raise AssertionError(("same path transducer, different code", p, code))
                code_to_paths[code] = paths
                paths_to_code[paths] = code
        expected = (p + 1) * (1 << p)
        if len(code_to_paths) != expected:
            raise AssertionError((p, len(code_to_paths), expected))
        print(f"p={p} distinct={len(code_to_paths)} expected={expected}")

    print("broadword_crosscheck")
    for n in (2, 4, 8, 16):
        lim = min(1 << n, 256)
        for b in range(1, lim):
            for c in range(lim):
                if broad_child(b, c, n) != scalar_child(b, c, n):
                    raise AssertionError(("broadword mismatch", n, b, c))
        print(f"n={n} checked_b<{lim} checked_c<{lim}")

    print("two_lift_portal_normalization")
    total = 0
    for p in range(1, 11):
        n = 2 * p
        ones = (1 << n) - 1
        count = 0
        for w in range(1 << p):
            if parity(w) == 0:
                continue
            x = portal_lift(w, p)
            y1 = broad_child(x, 0, n)
            y2 = broad_child(y1, x, n)
            if y1 != ones:
                raise AssertionError(("first lift not all ones", p, w))
            if not is_rotation(y2, x, n):
                raise AssertionError(("second lift not phase-equivalent", p, w))
            count += 1
        total += count
        print(f"p={p} odd_words={count} failures=0")
    print(f"two_lift_total={total}")

    print("p8_half_block_collision")
    witnesses = [
        (0x01, 49731, 0, 0xFE7F),
        (0x0B, 44840, 1, 0xE7E5),
    ]
    sig0 = None
    for w, exp_depth, exp_parity, exp_target in witnesses:
        p = 8
        n = 16
        x = portal_lift(w, p)
        mask = (1 << p) - 1
        sig = (
            block_code(x & mask, 0, p),
            block_code((x >> p) & mask, 0, p),
        )
        depth, target = first_zero_return(x, 0, n, 300000)
        if depth != exp_depth or parity(target) != exp_parity or target != exp_target:
            raise AssertionError(("witness mismatch", w, depth, parity(target), target))
        if sig0 is None:
            sig0 = sig
        elif sig != sig0:
            raise AssertionError(("witness codes differ", sig0, sig))
        print(
            f"w={bits(w,p)} x={bits(x,n)} depth={depth} "
            f"target={bits(target,n)} parity={parity(target)} "
            f"half_codes=((r={sig[0][0]},q={bits(sig[0][1],p)}),"
            f"(r={sig[1][0]},q={bits(sig[1][1],p)}))"
        )
    print("collision_same_half_codes=1 collision_mixed_endpoint_parity=1")

if __name__ == "__main__":
    main()
