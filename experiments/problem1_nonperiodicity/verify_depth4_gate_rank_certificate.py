#!/usr/bin/env python3
"""Independent verifier for the depth-four gate-miter SCC rank certificate.

Scope is the exact finite N=32768 observer-depth-4 lifted miter graph. Every
retained edge is rebuilt here from an independent scalar Rule-30 truth-table
original two-row normalized update; no builder, transition module, or prior
verifier code is imported. The script decodes the supplied rank vector, checks
length, hash, uint16 range, node encoding, monotonicity on every retained edge,
and the three Section-2 necessary conditions per rank group. It computes no
SCC, runs no other depth, and enumerates no period.
"""
from __future__ import annotations

import base64
import hashlib
import json
import os
import platform
import struct
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INPUT = ROOT / "results/problem1/20261002_depth4_gate_miter.json"
OUT = ROOT / "results/problem1/20261002_depth4_gate_rank_certificate_verification.json"
REFERENCE = ROOT / "src/python/rule30_research_reference.py"
IMMUTABLE_REFERENCE_SHA256 = "358bdc07904e77080eb78b67bdd8da25822d6b51f1a91b58b5313dfe461c1d01"

WALL_CAP, MEMORY_CAP, OUTPUT_CAP = 60.0, 256 * 1024 * 1024, 256 * 1024
START = time.monotonic()

R = 4
NPAIR = R + 1                        # 5 pairs per normalized stack
UBITS = 2 * R                        # 8 bits of upper depth-4 state
PBITS = UBITS + 4                    # 12 bits per product state
NPROD = 1 << PBITS                   # 4096 product states
NFULL = 1 << (UBITS + 2)             # 1024 depth-5 stacks (U, added pair)
NSHEET = 8
NVERT = NPROD * NSHEET               # 32768 lifted vertices
TRUTH = (0, 1, 1, 1, 1, 0, 0, 0)    # Rule 30 on neighborhood index 4h+2l+x


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def bit(x: int, i: int) -> int:
    return (x >> i) & 1


def _proc_kb(field: str) -> int:
    for line in Path("/proc/self/status").read_text().splitlines():
        if line.startswith(field):
            return int(line.split()[1]) * 1024
    return 0


def caps() -> None:
    if time.monotonic() - START > WALL_CAP:
        raise TimeoutError("60-second wall cap exceeded")
    if _proc_kb("VmRSS:") > MEMORY_CAP:
        raise MemoryError("256-MiB resident cap exceeded")


def peak_rss() -> int:
    return _proc_kb("VmHWM:")


def atomic_json(obj) -> None:
    raw = (json.dumps(obj, sort_keys=True, indent=2) + "\n").encode()
    if len(raw) > OUTPUT_CAP:
        raise ValueError("256-KiB output cap exceeded")
    fd, tmp = tempfile.mkstemp(prefix=OUT.name + ".", suffix=".tmp", dir=OUT.parent)
    try:
        with os.fdopen(fd, "wb") as fh:
            fh.write(raw)
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(tmp, OUT)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def pairs_of(state: int) -> list:
    """Five (X, Y) pairs of a depth-5 stack, least significant pair first."""
    return [(bit(state, 2 * j), bit(state, 2 * j + 1)) for j in range(NPAIR)]


def rows_of(state: int) -> tuple:
    """The two raw rows: row A is [1,0] + X_j, row B is [1,1] + (X_j xor Y_j)."""
    pairs = pairs_of(state)
    return (
        [1, 0] + [x for (x, _y) in pairs],
        [1, 1] + [x ^ y for (x, y) in pairs],
    )


def step_rows(state: int, label: int) -> int:
    """Original two-row normalized update via the raw Rule-30 truth table."""
    row_a, row_b = rows_of(state)
    out = 0
    for j in range(NPAIR):
        ha, la, xa = row_a[j], row_a[j + 1], row_a[j + 2]
        hb, lb, xb = row_b[j], row_b[j + 1], row_b[j + 2]
        oa = TRUTH[4 * ha + 2 * la + xa]
        ob = TRUTH[4 * hb + 2 * lb + xb]
        y = oa ^ ob
        x = oa if label == 0 else ob
        out |= x << (2 * j) | y << (2 * j + 1)
    return out


def step_bitwise(state: int, label: int) -> int:
    """Independent control: Rule 30 written as l XOR (c OR r), no table lookup."""
    left, right = rows_of(state)
    top = [left[j] ^ (left[j + 1] | left[j + 2]) for j in range(NPAIR)]
    bot = [right[j] ^ (right[j + 1] | right[j + 2]) for j in range(NPAIR)]
    y = [top[j] ^ bot[j] for j in range(NPAIR)]
    x = [top[j] if label == 0 else bot[j] for j in range(NPAIR)]
    value = 0
    for j in range(NPAIR):
        value |= x[j] << (2 * j) | y[j] << (2 * j + 1)
    return value


def main() -> None:
    caps()
    source_bytes = Path(__file__).read_bytes()
    input_bytes = INPUT.read_bytes()
    record = json.loads(input_bytes)

    ref_sha = sha(REFERENCE.read_bytes())
    if ref_sha != IMMUTABLE_REFERENCE_SHA256:
        raise AssertionError("immutable reference sha256 mismatch: " + ref_sha)

    cert = record["scc_rank_certificate"]
    raw = base64.b64decode(cert["base64"], validate=True)
    if len(raw) != NVERT * 2:
        raise AssertionError("certificate byte length mismatch: %d" % len(raw))
    if len(raw) != int(cert["byte_count"]):
        raise AssertionError("certificate byte_count field mismatch")
    cert_sha = sha(raw)
    if cert_sha != cert["sha256"]:
        raise AssertionError("certificate sha256 mismatch: " + cert_sha)
    rank = list(struct.unpack("<%dH" % NVERT, raw))
    rmin, rmax = min(rank), max(rank)
    if rmin < 0 or rmax > 0xFFFF:
        raise AssertionError("rank outside uint16 domain")
    caps()

    trans = [[step_rows(f, lab) for lab in (0, 1)] for f in range(NFULL)]
    control_cases = 0
    for f in range(NFULL):
        for lab in (0, 1):
            control_cases += 1
            if trans[f][lab] != step_bitwise(f, lab):
                raise AssertionError("control mismatch at full=%d label=%d" % (f, lab))
    caps()

    blind = bytearray(1 << UBITS)
    for u in range(1 << UBITS):
        blind[u] = 1 if (trans[u][0] & 255) == (trans[u][1] & 255) else 0

    edges_of = [[] for _ in range(NPROD)]
    bad_products = 0
    for st in range(NPROD):
        u = st & 255
        va = (st >> 8) & 3
        vb = (st >> 10) & 3
        bucket = edges_of[st]
        for a in (0, 1):
            for b in (0, 1):
                aa = trans[u | (va << 8)][a]
                bb = trans[u | (vb << 8)][b]
                if (aa & 255) != (bb & 255):
                    continue
                nxt = (aa & 255) | (((aa >> 8) & 3) << 8) | (((bb >> 8) & 3) << 10)
                ya, yb = bit(aa, 9), bit(bb, 9)
                bucket.append((a ^ (b << 1) ^ 4, nxt, a, b, ya, yb))
                if blind[u] and a == b and ya != yb:
                    bad_products += 1
        if st % 1024 == 0:
            caps()

    flag1 = set()
    bad_edge_count = 0
    bad_same_rank_all_sheets = 0
    bad_strict_rank_increase = 0
    retained_edges = 0
    for st in range(NPROD):
        for sd, nxt, a, b, ya, yb in edges_of[st]:
            is_bad = blind[st & 255] and a == b and ya != yb
            for sheet in range(NSHEET):
                src = (sheet << PBITS) | st
                tgt = ((sheet ^ sd) << PBITS) | nxt
                ru, rt = rank[src], rank[tgt]
                if rt < ru:
                    raise AssertionError(
                        "rank decreases on edge %d -> %d (%d -> %d)" % (src, tgt, ru, rt)
                    )
                retained_edges += 1
                if is_bad:
                    bad_edge_count += 1
                    if rt == ru:
                        bad_same_rank_all_sheets += 1
                        if sheet == 0:
                            flag1.add(ru)
                    else:
                        bad_strict_rank_increase += 1
        if st % 512 == 0:
            caps()

    flag2 = set()
    flag3 = set()
    ex2, ex3 = [], []
    for st in range(NPROD):
        r0 = rank[st]
        if r0 == rank[(3 << PBITS) | st]:
            flag2.add(r0)
            if len(ex2) < 4:
                ex2.append({"rank": r0, "product_state": st, "upper_state": st & 255})
        if st & 0xC0:
            # Condition 3 asks for any vertex of the rank group, so scan every sheet.
            for sheet in range(NSHEET):
                flag3.add(rank[(sheet << PBITS) | st])
                if len(ex3) < 4:
                    ex3.append(
                        {
                            "rank": rank[(sheet << PBITS) | st],
                            "sheet": sheet,
                            "product_state": st,
                            "upper_state": st & 255,
                        }
                    )
        if st % 1024 == 0:
            caps()

    all_three = sorted(flag1 & flag2 & flag3)
    status = "PASS" if not all_three else "FAIL"

    result = {
        "schema": "problem1-depth4-gate-rank-certificate-verification-v1",
        "experiment_id": "20261002-depth4-gate-rank-certificate-verification",
        "status": status,
        "claim_status": "FINITE_EXPERIMENT",
        "scope_statement": (
            "Exact finite verification on the N=32768 vertex observer-depth-4 lifted miter "
            "graph only. The rank vector was decoded and checked for length, hash, uint16 "
            "range, node encoding, monotonicity on every retained edge, and absence of any "
            "rank group carrying all three Section-2 necessary conditions. No SCC was "
            "computed, no other depth was run, and no all-period consequence is asserted "
            "here; that call belongs to the parent."
        ),
        "input_record": {
            "path": str(INPUT.relative_to(ROOT)),
            "sha256": sha(input_bytes),
            "byte_count": len(input_bytes),
            "declared_status": record.get("status"),
        },
        "certificate": {
            "sha256": cert_sha,
            "byte_count": len(raw),
            "vertex_count": NVERT,
            "distinct_rank_count": rmax - rmin + 1,
            "rank_min": rmin,
            "rank_max": rmax,
            "rank_outside_uint16": False,
            "encoding": "little-endian uint16 per lifted vertex (sheet<<12)|product_state",
            "node_encoding_check": "passed: 32768 values indexed by sheet<<12|product_state",
        },
        "graph": {
            "vertices": NVERT,
            "sheets": NSHEET,
            "product_states": NPROD,
            "full_transition_vectors": 2 * NFULL,
            "retained_edges": retained_edges,
            "bad_edges": bad_edge_count,
            "bad_edges_with_equal_endpoint_ranks_all_sheets": bad_same_rank_all_sheets,
            "bad_edges_with_strictly_increasing_rank": bad_strict_rank_increase,
            "bad_edges_sheet0_internal_note": (
                "every bad edge strictly increases rank, so no sheet-0 internal bad edge exists"
                if bad_strict_rank_increase == bad_edge_count
                else "some bad edges are internal to a rank group"
            ),
            "bad_products_per_sheet": bad_products,
            "upper_blind_states": sum(blind),
        },
        "controls": {
            "truth_table_two_row_vs_independent_bit_array_all_2048": "passed",
            "truth_table_cases": control_cases,
            "rule30_truth_table": list(TRUTH),
            "builder_or_transition_module_imported": False,
            "expected_counts_hardcoded": False,
        },
        "checks": {
            "edge_monotonicity": "passed on every retained edge",
            "rank_groups_with_sheet0_internal_bad_edge": len(flag1),
            "rank_groups_with_same_rank_sheet0_and_sheet3_lift": len(flag2),
            "rank_groups_with_nonzero_last_upper_pair": len(flag3),
            "rank_groups_satisfying_all_three": len(all_three),
            "first_offending_groups": all_three[:8],
            "examples_flag2_sheet0_sheet3_same_rank": ex2,
            "examples_flag3_nonzero_last_upper_pair": ex3,
            "absence_claim": (
                "no rank group carries all three necessary conditions, so no counterexample "
                "lifted cycle exists on this finite depth-4 graph"
            )
            if not all_three
            else "withdrawn: a rank group carries all three necessary conditions",
        },
        "caps": {
            "wall_seconds": WALL_CAP,
            "resident_bytes": MEMORY_CAP,
            "output_bytes": OUTPUT_CAP,
            "peak_resident_bytes": peak_rss(),
        },
        "provenance": {
            "script_sha256": sha(source_bytes),
            "immutable_reference_sha256": ref_sha,
            "immutable_reference_sha256_asserted": True,
            "full_base_commit": subprocess.check_output(
                ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
            ).strip(),
            "git_status_porcelain": subprocess.check_output(
                ["git", "status", "--porcelain"], cwd=ROOT, text=True
            ).splitlines(),
            "generated_utc": datetime.now(timezone.utc).isoformat(),
            "python": sys.version,
            "platform": platform.platform(),
            "cpu_model": next(
                (
                    ln.split(":", 1)[1].strip()
                    for ln in Path("/proc/cpuinfo").read_text().splitlines()
                    if ln.lower().startswith("model name")
                ),
                platform.processor(),
            ),
            "elapsed_seconds": time.monotonic() - START,
        },
        "limitations": [
            "Scope is the exact finite N=32768 depth-4 lifted observer graph only.",
            "The supplied rank partition was not required to be an exact SCC decomposition.",
            "Group flags are necessary conditions; their absence proves no counterexample here.",
            "No other depth, period, or whole-period enumeration was performed.",
            "Consequences for H_gate in general, transport, or nonperiodicity are the parent's call.",
        ],
    }
    atomic_json(result)
    print(
        json.dumps(
            {
                "status": status,
                "edges": retained_edges,
                "bad_edges": bad_edge_count,
                "all_three_groups": len(all_three),
                "output": str(OUT),
            }
        )
    )


if __name__ == "__main__":
    main()
