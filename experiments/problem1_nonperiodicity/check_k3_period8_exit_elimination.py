from itertools import product

def lo(x):
    return x & 1

def hi(x):
    return (x >> 1) & 1

def phi_symbol(a, b):
    a0, a1 = lo(a), hi(a)
    b0, b1 = lo(b), hi(b)
    r = b0 ^ (a0 | a1)
    s = b1 ^ (a1 | r)
    return r | (s << 1)

def Phi(w):
    p = len(w)
    return tuple(phi_symbol(w[i], w[(i + 1) % p]) for i in range(p))

def min_period(w):
    n = len(w)
    for d in range(1, n + 1):
        if n % d == 0 and all(w[i] == w[i % d] for i in range(n)):
            return d
    raise AssertionError

def exit_phase_ok(w):
    p = len(w)
    for k in range(1, p + 1):
        x = w[-k]
        if x in (1, 3):
            suffix = w[p - k + 1:p]
            gamma = sum(a == 2 for a in suffix) & 1
            return gamma == (x == 1)
    return False

def finite_phi_hitting_time(w):
    zero = (0,) * len(w)
    seen = set()
    cur = tuple(w)
    for n in range(4 ** len(w) + 1):
        if cur == zero:
            return n
        if cur in seen:
            return None
        seen.add(cur)
        cur = Phi(cur)
    raise AssertionError("finite-state bound exceeded")

def recurrent_trace(word, m, prev):
    p = len(word)
    sols = []
    for init in (0, 1):
        u = [None] * p
        u[0] = init
        cur = init
        for s in range(p):
            if m == 1:
                nxt = hi(word[s]) ^ (lo(word[s]) | cur)
            elif m == 2:
                nxt = lo(word[s]) ^ (prev[0][s] | cur)
            else:
                nxt = prev[m - 3][s] ^ (prev[m - 2][s] | cur)
            if s < p - 1:
                u[s + 1] = nxt
            cur = nxt
        if cur == init:
            sols.append(tuple(u))
    return sols

def traces(word, M):
    out = []
    for m in range(1, M + 1):
        sol = recurrent_trace(word, m, out)
        assert len(sol) == 1, (word, m, len(sol))
        out.append(sol[0])
    return out

def driver_at(tr, n):
    p = len(tr[0])
    return tuple(
        2 * tr[n - 2][(s + n) % p] + tr[n - 1][(s + n) % p]
        for s in range(p)
    )

def pair_at(tr, n):
    p = len(tr[0])
    return tr[n][n % p], tr[n + 1][n % p]

phase = []
finite = []
for tail in product(range(4), repeat=4):
    w = (2, 2, 2, 1) + tail
    if min_period(w) != 8 or not exit_phase_ok(w):
        continue
    phase.append(w)
    hit = finite_phi_hitting_time(w)
    if hit is not None:
        finite.append((w, hit))

assert len(phase) == 128

expected = [
    ((2, 2, 2, 1, 1, 0, 3, 3), 152),
    ((2, 2, 2, 1, 2, 2, 2, 3), 34),
    ((2, 2, 2, 1, 2, 3, 3, 0), 107),
    ((2, 2, 2, 1, 3, 3, 3, 0), 146),
]
assert finite == expected, finite

expected_rows = [
    ("22211033", "010011", 0, "32330011", "10", "20111220", "11", "12221331"),
    ("22212223", "001101", 0, "31101211", "10", "32321220", "11", "20221330"),
    ("22212330", "011000", 1, "21021100", "11", "23122331", "10", "03130121"),
    ("22213330", "001110", 0, "30201211", "10", "02321220", "11", "10221333"),
]

rows = []
for w, hit in finite:
    tr = traces(w, 12)
    r = [u[0] for u in tr[:6]]
    _, a, b, c, d, e6 = r

    repair = ((1 ^ a) & (1 ^ b) & (c | d)) == 0
    assert repair

    k = (
        (b & (1 ^ a))
        | ((1 ^ a) & (1 ^ c))
        | (d & (1 ^ b) & (1 ^ c))
        | (e6 & (1 ^ b) & (1 ^ c))
    )
    endpoint = 1 ^ k

    c6 = driver_at(tr, 6)
    c8 = driver_at(tr, 8)
    c10 = driver_at(tr, 10)
    p6 = pair_at(tr, 6)
    p8 = pair_at(tr, 8)

    rows.append((
        "".join(map(str, w)),
        "".join(map(str, r)),
        endpoint,
        "".join(map(str, c6)),
        "".join(map(str, p6)),
        "".join(map(str, c8)),
        "".join(map(str, p8)),
        "".join(map(str, c10)),
    ))

assert rows == expected_rows, rows

print("phase_compatible_period8_words =", len(phase))
print("finite_period8_exit_cores =", len(finite))
for row in rows:
    print(*row)
