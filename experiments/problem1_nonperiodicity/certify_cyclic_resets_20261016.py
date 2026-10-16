#!/usr/bin/env python3
"""Generate and independently check finite certificates for S_6,...,S_23.

Admission: test a uniform collision-segment criterion with a stronger cyclic
prefix, not a longer temporal sample. Failure would invalidate that criterion;
success establishes only the explicitly checked spatial depths, at all periods.
No prize problem is claimed solved. Standard-library Python; local CPU only.
"""
from __future__ import annotations
import argparse
from array import array
from collections import deque
from functools import lru_cache
import hashlib
import json
import os
from pathlib import Path
import platform
import struct
import sys
import tempfile
import time
import zlib

BASE_COMMIT = "c424346e1a6efdf7cdd673efeff4b6578fe830b6"
PREFIX = "0111100"
DFA = ((1, 2), (2, 3), (2, 2), (4, 5), (4, 6), (2, 1), (2, 7), (4, 4))


def atomic(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as f:
        name = f.name
        f.write(data)
    os.replace(name, path)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def number(word: str) -> int:
    return sum(int(c) << j for j, c in enumerate(word))


def word(value: int, depth: int) -> str:
    return format(value, f"0{depth}b")[::-1]


def fast(a: int, b: int, r: int) -> tuple[int, int]:
    mask = (1 << r) - 1
    ta = (a << 2) ^ ((a << 1) | a)
    tb = (b << 2) ^ ((b << 1) | b)
    return (ta ^ 1) & mask, (tb ^ (b & 1) ^ 2) & mask


@lru_cache(maxsize=262144)
def literal(value: int, r: int, boundary: int) -> int:
    """Independent cell-by-cell raw update. boundary is the value at site 0;
    site -1 is one for both tracks. No packed producer transition is called.
    """
    older, previous = 1, boundary
    result = 0
    for j in range(r):
        current = (value >> j) & 1
        result |= (older ^ int(bool(previous or current))) << j
        older, previous = previous, current
    return result


def store_set(out: Path, name: str, states: set[int]) -> dict:
    values = array("Q", sorted(states))
    if values.itemsize != 8:
        raise RuntimeError("An eight-byte unsigned long long is required")
    if sys.byteorder != "little":
        values.byteswap()
    raw = values.tobytes()
    compressed = zlib.compress(raw, 9)
    atomic(out / name, compressed)
    return {"file": name, "states": len(states), "raw_sha256": digest(raw),
            "compressed_sha256": digest(compressed)}


def load_set(out: Path, record: dict) -> set[int]:
    compressed = (out / record["file"]).read_bytes()
    assert digest(compressed) == record["compressed_sha256"]
    raw = zlib.decompress(compressed)
    assert digest(raw) == record["raw_sha256"]
    assert len(raw) == 8 * record["states"]
    values = array("Q")
    values.frombytes(raw)
    if sys.byteorder != "little":
        values.byteswap()
    states = set(values)
    assert len(states) == record["states"]
    return states


def prefix_certificate(r: int, out: Path) -> dict:
    """Forward-closed upper sets exclude every unlisted cyclic blind output."""
    n = 1 << r
    sources: dict[int, set[int]] = {}
    for a in range(n):
        for b in range(n):
            p, q = fast(a, b, r)
            if p == q:
                sources.setdefault(p, set()).add(a | (b << r))
    records = []
    possible = set()
    for common, inputs in sorted(sources.items()):
        root = common | (common << r)
        reached, queue = {root}, deque([root])
        while queue:
            state = queue.popleft()
            p, q = fast(state & (n - 1), state >> r, r)
            for target in (p | (q << r), q | (p << r)):
                if target not in reached:
                    reached.add(target)
                    queue.append(target)
        if reached & inputs:
            possible.add(common)
        rec = store_set(out, f"prefix_{r}_{common}.u64.zlib", reached)
        rec.update(common=common, candidate_sources=sorted(reached & inputs))
        records.append(rec)
    expected = number("011110" if r == 6 else PREFIX)
    assert possible == {expected}
    return {"depth": r, "allowed_common": expected, "records": records}


def dfa_words(r: int) -> set[int]:
    state = 0
    for c in PREFIX:
        state = DFA[state][int(c)]
    current = {(number(PREFIX), state)}
    for j in range(len(PREFIX), r):
        current = {(v | (c << j), DFA[s][c]) for v, s in current
                   for c in (0, 1) if DFA[s][c] != 2}
    return {v for v, _ in current}


def nfa_words(r: int) -> set[int]:
    """Independent raw four-bit preimage contexts, not the quotient DFA."""
    # Context bits: older A, older B, previous A, previous B; start (1,1,0,1).
    current = {(0, frozenset({11}))}
    for j in range(r):
        new = set()
        choices = (int(PREFIX[j]),) if j < len(PREFIX) else (0, 1)
        for value, contexts in current:
            for c in choices:
                dest = set()
                for context in contexts:
                    h, k, l, m = ((context >> i) & 1 for i in range(4))
                    for a in (0, 1):
                        for b in (0, 1):
                            if h ^ (l | a) == c and k ^ (m | b) == c:
                                dest.add(l | (m << 1) | (a << 2) | (b << 3))
                if dest:
                    new.add((value | (c << j), frozenset(dest)))
        current = new
    return {v for v, _ in current}


def cone_hit(value: int, r: int, independent: bool = False) -> int | None:
    for t in range((r - 1) // 2 + 1):
        if (value >> (r - 1)) & 1:
            return t
        if independent:
            bits = [(value >> j) & 1 for j in range(r)]
            nxt = []
            for j in range(r):
                older = bits[j - 2] if j >= 2 else 0
                previous = bits[j - 1] if j >= 1 else 0
                nxt.append(older ^ int(bool(previous or bits[j])))
            value = sum(b << j for j, b in enumerate(nxt))
        else:
            value = (value << 2) ^ ((value << 1) | value)
    return None


def segment_certificate(r: int, common: int, out: Path, cap: int) -> dict:
    n, mask = 1 << r, (1 << r) - 1
    roots = {common | (common << r) | (d << (2 * r)) for d in (1, 2, 3)}
    reached, queue = set(roots), deque(roots)
    gate_edges = 0
    while queue:
        state = queue.popleft()
        a, b, d = state & mask, (state >> r) & mask, state >> (2 * r)
        p, q = fast(a, b, r)
        da = (d & 1) & (1 ^ ((a >> (r - 1)) & 1))
        db = ((d >> 1) & 1) & (1 ^ ((b >> (r - 1)) & 1))
        if p == q:
            gate_edges += 2
            if da != db:
                raise AssertionError(f"Bad first-return segment at depth {r}: {state}")
            continue
        if not (da or db):
            continue
        for x, y, e in ((p, q, da | (db << 1)), (q, p, db | (da << 1))):
            target = x | (y << r) | (e << (2 * r))
            if target not in reached:
                reached.add(target)
                queue.append(target)
        if len(reached) > cap:
            raise RuntimeError(f"State cap at depth {r}; no conclusion")
    rec = store_set(out, f"segment_{r}_{common}.u64.zlib", reached)
    rec.update(depth=r, common=common, common_word=word(common, r), gate_edges=gate_edges)
    return rec


def generate(out: Path, maximum: int, cap: int) -> None:
    start = time.monotonic()
    report = {"status": "partial-proof", "base_commit": BASE_COMMIT,
              "problem_1": "OPEN", "source_sha256": digest(Path(__file__).read_bytes()),
              "python": sys.version, "platform": platform.platform(),
              "machine": platform.machine(), "processor": platform.processor(),
              "cpu_count": os.cpu_count(), "parameters": {"max_depth": maximum,
              "segment_state_cap": cap}, "prefix": [], "depths": [], "segments": []}
    for r in (6, 7):
        report["prefix"].append(prefix_certificate(r, out))
    report["segments"].append(segment_certificate(6, number("011110"), out, cap))
    for r in range(7, maximum + 1):
        words = dfa_words(r)
        exceptions = sorted(v for v in words if cone_hit(v, r) is None)
        report["depths"].append({"depth": r, "common_words": len(words),
                                  "cone_exceptions": [word(v, r) for v in exceptions]})
        for v in exceptions:
            report["segments"].append(segment_certificate(r, v, out, cap))
        print(f"Generated depth {r}: {len(words)} words, {len(exceptions)} delayed cases", flush=True)
    report["generation_seconds"] = time.monotonic() - start
    report["limitations"] = ["Fixed depths only; arbitrary temporal periods.",
        "No all-depth theorem, original-support budget, or center nonperiodicity proof.",
        "Closure certificates need not be acyclic and do not assert bounded reset time.",
        "AI-assisted derivation; independent code checks, not independent human review or Lean."]
    atomic(out / "manifest.json", (json.dumps(report, indent=2, sort_keys=True) + "\n").encode())


def verify(out: Path, part: str) -> None:
    start = time.monotonic()
    report = json.loads((out / "manifest.json").read_text())
    assert report["source_sha256"] == digest(Path(__file__).read_bytes())
    maximum = report["parameters"]["max_depth"]
    assert report["base_commit"] == BASE_COMMIT
    assert 7 <= maximum <= 23
    assert [entry["depth"] for entry in report["prefix"]] == [6, 7]
    assert [row["depth"] for row in report["depths"]] == list(range(7, maximum + 1))
    checks = 0
    if part in ("all", "prefix"):
        for entry in report["prefix"]:
            r = entry["depth"]
            n, mask = 1 << r, (1 << r) - 1
            sources: dict[int, set[int]] = {}
            for a in range(n):
                for b in range(n):
                    p, q = literal(a, r, 0), literal(b, r, 1)
                    if p == q:
                        sources.setdefault(p, set()).add(a | (b << r))
            assert {rec["common"] for rec in entry["records"]} == set(sources)
            possible = set()
            for rec in entry["records"]:
                common, states = rec["common"], load_set(out, rec)
                assert common | (common << r) in states
                for state in states:
                    assert 0 <= state < (1 << (2 * r))
                    a, b = state & mask, state >> r
                    p, q = literal(a, r, 0), literal(b, r, 1)
                    assert p | (q << r) in states
                    assert q | (p << r) in states
                    checks += 2
                if states & sources[common]:
                    possible.add(common)
            assert possible == {entry["allowed_common"]}
            assert word(entry["allowed_common"], r) == ("011110" if r == 6 else PREFIX)
        expected = {(6, number("011110"))}
        for row in report["depths"]:
            r = row["depth"]
            words = nfa_words(r)
            assert len(words) == row["common_words"]
            exceptions = {v for v in words if cone_hit(v, r, True) is None}
            assert {word(v, r) for v in exceptions} == set(row["cone_exceptions"])
            expected.update((r, v) for v in exceptions)
        assert expected == {(rec["depth"], rec["common"]) for rec in report["segments"]}
    if part in ("all", "segments"):
        for rec in report["segments"]:
            r, common = rec["depth"], rec["common"]
            mask, states = (1 << r) - 1, load_set(out, rec)
            for d in (1, 2, 3):
                assert common | (common << r) | (d << (2 * r)) in states
            gate_edges = 0
            for state in states:
                a, b, d = state & mask, (state >> r) & mask, state >> (2 * r)
                assert d in (1, 2, 3)
                p, q = literal(a, r, 0), literal(b, r, 1)
                # Independent differences: evolve two concrete added cells per track.
                da = ((literal(a, r + 1, 0) ^ literal(a | ((d & 1) << r), r + 1, 0)) >> r) & 1
                db = ((literal(b, r + 1, 1) ^ literal(b | (((d >> 1) & 1) << r), r + 1, 1)) >> r) & 1
                if p == q:
                    assert da == db
                    gate_edges += 2
                elif da or db:
                    assert p | (q << r) | ((da | (db << 1)) << (2 * r)) in states
                    assert q | (p << r) | ((db | (da << 1)) << (2 * r)) in states
                checks += 2
            assert gate_edges == rec["gate_edges"]
            print(f"Verified depth {r}, {rec['common_word']}: {len(states)} states", flush=True)
    result = {"part": part, "passed": True, "checked_edges": checks,
              "seconds": time.monotonic() - start,
              "manifest_sha256": digest((out / "manifest.json").read_bytes()),
              "source_sha256": digest(Path(__file__).read_bytes()),
              "base_commit": BASE_COMMIT, "python": sys.version}
    atomic(out / f"verification_{part}.json", (json.dumps(result, indent=2) + "\n").encode())
    print(json.dumps(result), flush=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("generate", "verify"))
    parser.add_argument("--out", type=Path, default=Path("results/problem1/20261016_cyclic_resets"))
    parser.add_argument("--max-depth", type=int, default=23)
    parser.add_argument("--state-cap", type=int, default=400000)
    parser.add_argument("--part", choices=("all", "prefix", "segments"), default="all")
    args = parser.parse_args()
    if not 7 <= args.max_depth <= 23 or args.state_cap < 1:
        parser.error("This certified release supports maximum depths 7 through 23 and a positive cap")
    if args.mode == "generate":
        generate(args.out, args.max_depth, args.state_cap)
    else:
        verify(args.out, args.part)


if __name__ == "__main__":
    main()
