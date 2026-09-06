#!/usr/bin/env python3
"""Independent check of the anchored vertical-spine hand certificate.

Implements ONLY the physical Rule 30 rule
    r_i' = r_{i-1} XOR (r_i OR r_{i+1})
on 6 cyclic cells (plain cell lists; no packed-A and no g/Phi reuse),
starting from r_i = u_{-i} with u = 50 = bits [0,1,0,0,1,1] low-to-high,
for 6 updates (rows t = 0..6). Each physical row is converted to the
A-row via u_i(t) = r_{(-i-t) mod 6}(t) and compared against the hand
vectors 50,23,10,45,36,63,0. Single fixed input; no search, no sweep.

Admission: lead note problem1_anchored_activity_vertical_spine_obstruction.md
(ONLY admitted verification: these three six-symbol words + one six-cell
period for six updates). Agree => fixed witness stands (finite-exhaustive
on this singleton trajectory only); disagree => exit nonzero, no record,
certificate withdrawn. Either way no infinite inference is drawn.

Provenance v4 (loader repair): replayable from repo artifacts alone and
robust to record overwrite. The authenticated v2 execution is located
through ONE shared loader -- either raw v2 bytes (pre-overwrite) or the
working record's archived_executions entry labelled v2-provenance-repair
(post-overwrite) -- authenticated by a FIXED canonical-JSON digest plus
content source/admission SHA checks in both cases; OUT_REL is never assumed
to still be v2. Admission resolves live-note-bytes first, else the primary
record's snapshot (content SHA re-verified). `--check-load-only` verifies
reference/admission/history/artifact integrity with zero science and zero
writes. Scientific formula and inputs unchanged since v1.
"""
import hashlib
import json
import os
import platform
import re
import resource
import signal
import subprocess
import sys
import time

# ---- enforced budgets (fail closed; wall enforced via signal.alarm) ----
CPU_BUDGET_S = 120
RAM_BUDGET_B = 2 ** 30  # 1 GiB
WALL_BUDGET_S = 120     # explicit wall budget; expected use << 1 s

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REF_REL = "src/python/rule30_research_reference.py"
REF_SHA = "358bdc07904e77080eb78b67bdd8da25822d6b51f1a91b58b5313dfe461c1d01"
LEAD_REL = "proofs/informal/problem1_anchored_activity_vertical_spine_obstruction.md"
LEAD_ADMISSION_SHA = "e7e44fcb19b358ff3191a9e8fdde80ae85e8af8de644ad389906d2c835141ee7"
PRIMARY_REL = "results/problem1/20260906_anchored_spine_primary.json"
SELF_REL = "experiments/problem1_nonperiodicity/check_anchored_spine_independent.py"
OUT_REL = "results/problem1/20260906_anchored_spine_independent.json"
PRIOR_RECORD_PATH = "/tmp/astra-round6-spine-independent-initial.json"
PRIOR_SOURCE_PATH = "/tmp/astra-round6-spine-independent-source-initial.py"
PRIOR_RECORD_SHA = "6134fdf096f8b97d2c8405cfcda9c0f9d773ba4379a1dafb640a0bea37f70be5"
PRIOR_SOURCE_SHA = "a2c1f6cc9c7f23850e2a312fc74ecdd74f9fccc121b7485b4c259cb3bf95fc70"
V2_RECORD_SHA = "aea8ea2dbfea2aa0b8b6c6707f48420c7d4c6d5c4cda5482321bd3bfe7e66ad8"
V2_CANONICAL_SHA = "350b38f38af7cd1a1a9db07228eeea23dd8bef27f6bf9ae459238f5f807f13ec"
EXPECTED_PAYLOAD_SHA = "b58afe368e42e8a1ddffbe08493adde4f6997cac05ac575048ffdbba94c95522"

HAND_WORDS = [50, 23, 10, 45, 36, 63, 0]


class FailClosed(Exception):
    pass


def fail(msg):
    raise FailClosed(msg)


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()


def read_exact(path):
    with open(path, "rb") as f:
        return f.read()


def bits_of(word, n=6):
    return [(word >> i) & 1 for i in range(n)]


def words_of(a_rows):
    return [sum(b << i for i, b in enumerate(row)) for row in a_rows]


def check_snapshot_content(snap, label):
    if sha256_bytes(snap.get("text", "").encode("utf-8")) != snap.get("sha256"):
        fail("%s content SHA mismatch" % label)


def load_admission():
    """Exact original admission text; live bytes first, committed artifact fallback."""
    live = read_exact(os.path.join(REPO, LEAD_REL))
    if sha256_bytes(live) == LEAD_ADMISSION_SHA:
        return {"path": LEAD_REL, "sha256": LEAD_ADMISSION_SHA,
                "text": live.decode("utf-8")}, "live-note"
    try:
        primary = json.loads(read_exact(os.path.join(REPO, PRIMARY_REL)).decode("utf-8"))
        text = primary["admission_snapshot"]["text"]
    except Exception as exc:  # noqa: BLE001
        fail("admission fallback unreadable: %s" % exc)
    if sha256_bytes(text.encode("utf-8")) != LEAD_ADMISSION_SHA:
        fail("admission content SHA mismatch")
    return {"path": LEAD_REL, "sha256": LEAD_ADMISSION_SHA, "text": text,
            "recovered_from": PRIMARY_REL}, "primary-fallback"


def load_v2_authenticated():
    """Locate the v2 execution via raw v2 bytes OR the working record's
    archived entry; authenticate canonical digest + content SHAs either way.
    Never assumes OUT_REL is still v2."""
    raw = read_exact(os.path.join(REPO, OUT_REL))
    if sha256_bytes(raw) == V2_RECORD_SHA:
        v2 = json.loads(raw.decode("utf-8"))
        via = "raw-v2-bytes"
    else:
        try:
            doc = json.loads(raw.decode("utf-8"))
            hits = [e for e in (doc.get("archived_executions") or [])
                    if e.get("label") == "v2-provenance-repair"]
        except Exception as exc:  # noqa: BLE001
            fail("working record unparseable: %s" % exc)
        if len(hits) != 1:
            fail("authenticated v2 not locatable (no raw bytes, no archive entry)")
        if sha256_bytes(canonical(hits[0]["record"])) != V2_CANONICAL_SHA:
            fail("archived v2 canonical digest mismatch")
        v2 = hits[0]["record"]
        via = "archived-entry"
    check_snapshot_content(v2.get("source_snapshot") or {}, "v2 source")
    check_snapshot_content(v2.get("admission_snapshot") or {}, "v2 admission")
    if (v2.get("admission_snapshot") or {}).get("sha256") != LEAD_ADMISSION_SHA:
        fail("v2 admission SHA mismatch")
    return v2, via


def load_history():
    """ONE shared loader for both /tmp and repo-fallback paths."""
    v2, v2_via = load_v2_authenticated()
    v1_record = v1_source_text = None
    hist_via = None
    if os.environ.get("SPINE_REPLAY_NO_TMP") != "1":
        try:
            tmp_rec = read_exact(PRIOR_RECORD_PATH)
            tmp_src = read_exact(PRIOR_SOURCE_PATH).decode("utf-8")
        except Exception:
            tmp_rec = tmp_src = None
        if (tmp_rec is not None
                and sha256_bytes(tmp_rec) == PRIOR_RECORD_SHA
                and sha256_bytes(tmp_src.encode("utf-8")) == PRIOR_SOURCE_SHA):
            v1_record = json.loads(tmp_rec.decode("utf-8"))
            v1_source_text = tmp_src
            hist_via = "tmp/%s" % v2_via
    if v1_record is None:
        sup_src = v2.get("superseded_source_snapshot") or {}
        v1_source_text = sup_src.get("text")
        v1_record = v2.get("superseded_prior_record")
        if not v1_record or not v1_source_text:
            fail("v2 lacks v1 retention")
        check_snapshot_content(sup_src, "v1 source")
        hist_via = "repo-fallback/%s" % v2_via
    try:
        hist_words = words_of(v1_record["result_summary"]["a_rows"])
    except Exception:  # noqa: BLE001
        fail("history is for a different computation")
    if hist_words != HAND_WORDS:
        fail("history is for a different computation")
    return {
        "v1_record": v1_record,
        "v1_source_text": v1_source_text,
        "v2_record": v2,
        "history_via": hist_via,
    }


def check_load_only():
    """Repo-only verification of the written artifact: no science, no writes."""
    ref_sha = sha256_bytes(read_exact(os.path.join(REPO, REF_REL)))
    if ref_sha != REF_SHA:
        return fail("reference hash mismatch")
    adm, adm_via = load_admission()
    hist = load_history()
    doc = json.loads(read_exact(os.path.join(REPO, OUT_REL)).decode("utf-8"))
    payload_digest = sha256_bytes(canonical(doc["payload"]))
    if payload_digest != EXPECTED_PAYLOAD_SHA:
        return fail("artifact payload digest mismatch")
    print("load-only OK: ref ok; admission via=%s sha=%s" % (adm_via, adm["sha256"][:12]))
    print("load-only OK: history via=%s; v1+v2 archived; payload=%s" %
          (hist["history_via"], payload_digest[:16]))
    return 0


def main(argv):
    signal.alarm(WALL_BUDGET_S)  # fail-closed wall enforcement
    try:
        resource.setrlimit(resource.RLIMIT_CPU, (CPU_BUDGET_S, CPU_BUDGET_S))
        resource.setrlimit(resource.RLIMIT_AS, (RAM_BUDGET_B, RAM_BUDGET_B))
    except Exception as exc:  # noqa: BLE001 -- fail closed, never tolerate
        print("FAIL-CLOSED: rlimits unset: %s" % exc, file=sys.stderr)
        return 3
    try:
        if "--verify-replay-inputs" in argv or "--check-load-only" in argv:
            return check_load_only()
        return run_science()
    except FailClosed as exc:
        print("FAIL-CLOSED: %s" % exc, file=sys.stderr)
        return 3


def run_science():
    # Immutable reference: hash-check only, never imported or reused.
    ref_sha = sha256_bytes(read_exact(os.path.join(REPO, REF_REL)))
    if ref_sha != REF_SHA:
        fail("reference hash mismatch: %s" % ref_sha)

    admission_snapshot, _ = load_admission()

    # Source snapshot: exact bytes of THIS script.
    self_data = read_exact(os.path.join(REPO, SELF_REL))
    source_snapshot = {
        "path": SELF_REL,
        "sha256": sha256_bytes(self_data),
        "text": self_data.decode("utf-8"),
    }

    hist = load_history()
    v1_record, v1_source_text, v2_record = (
        hist["v1_record"], hist["v1_source_text"], hist["v2_record"])
    v1_source_snapshot = {
        "path": PRIOR_SOURCE_PATH,
        "repo_path": SELF_REL,
        "sha256": sha256_bytes(v1_source_text.encode("utf-8")),
        "text": v1_source_text,
    }
    archived_executions = [
        {"label": "v1-initial", "record": v1_record},
        {"label": "v2-provenance-repair", "record": v2_record,
         "record_sha256": V2_RECORD_SHA,
         "record_canonical_sha256": V2_CANONICAL_SHA},
    ]

    # Full git, validated 40-char commit, fail closed.
    try:
        proc = subprocess.run(["git", "rev-parse", "HEAD"], cwd=REPO,
                              capture_output=True, text=True, timeout=30)
        git_commit = proc.stdout.strip()
        proc2 = subprocess.run(["git", "status", "--porcelain"], cwd=REPO,
                               capture_output=True, text=True, timeout=30)
        git_status = proc2.stdout.strip()
    except Exception as exc:  # noqa: BLE001
        fail("git unavailable: %s" % exc)
    import re as _re
    if not _re.fullmatch(r"[0-9a-f]{40}", git_commit):
        fail("git commit not a 40-char hash: %r" % git_commit)

    # ---- scientific computation (unchanged formula/inputs) ----
    n = 6
    u = bits_of(50, n)  # [0,1,0,0,1,1]
    if sum(b << i for i, b in enumerate(u)) != 50:
        fail("initial word decode")
    r = [u[(-i) % n] for i in range(n)]

    a_rows = []
    t_start = time.perf_counter()
    for t in range(7):
        a_rows.append([r[(-i - t) % n] for i in range(n)])
        if t < 6:
            # physical Rule 30 on the cyclic row; comprehension reads old r
            r = [r[(i - 1) % n] ^ (r[i] | r[(i + 1) % n]) for i in range(n)]
    elapsed = time.perf_counter() - t_start

    got_words = words_of(a_rows)
    if got_words != HAND_WORDS:
        print("MISMATCH: got %r expected %r" % (got_words, HAND_WORDS),
              file=sys.stderr)
        return 1  # no record written; certificate withdrawn

    temporal_pairs = []
    for j in range(3):
        temporal_pairs.append([a_rows[t][2 * j] + 2 * a_rows[t][2 * j + 1]
                               for t in range(7)])
    pair_activity_counts = [sum(1 for s in col if s != 0)
                            for col in temporal_pairs]
    first_zero_time = next(t for t in range(7)
                           if all(b == 0 for b in a_rows[t]))
    if pair_activity_counts != [5, 5, 5] or first_zero_time != 6:
        fail("derived counts differ")

    # Top-level payload: exact assigned keys.
    payload = {
        "period_bits": 6,
        "initial_word": 50,
        "a_rows": a_rows,
        "temporal_pairs": temporal_pairs,
        "pair_activity_counts": pair_activity_counts,
        "first_zero_time": first_zero_time,
    }
    payload_hash = sha256_bytes(canonical(payload))

    record = {
        "experiment_id": "20260906_anchored_spine_independent",
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "git_commit": git_commit,
        "git_status_porcelain": git_status[:2000],
        "question": "problem1",
        "hypothesis": ("Cyclic-6 physical Rule 30 from r_i=u_{-i}, u=50, "
                         "converted via u_i(t)=r_{(-i-t)}(t), reproduces the "
                         "hand A-rows 50,23,10,45,36,63,0."),
        "backend": "physical-cell-list-6cyclic-independent (no packed-A, no g/Phi)",
        "parameters": {
            "period_bits": 6,
            "initial_word": 50,
            "updates": 6,
            "rule": "r_i'=r_{i-1} XOR (r_i OR r_{i+1}) mod 6",
            "conversion": "u_i(t)=r_{(-i-t) mod 6}(t)",
            "cpu_budget_s": CPU_BUDGET_S,
            "ram_budget_b": RAM_BUDGET_B,
            "wall_budget_s": WALL_BUDGET_S,
            "wall_enforcement": "signal.alarm fail-closed",
            "history_via": hist["history_via"],
        },
        "hardware": {
            "platform": platform.platform(),
            "cpu_count": os.cpu_count(),
            "cpu_model": platform.processor() or platform.machine(),
        },
        "software": {
            "python": sys.version.replace("\n", " "),
            "repo": "local only, no cloud/remote",
        },
        "runtime_seconds": elapsed,
        "payload": payload,
        "source_snapshot": source_snapshot,
        "admission_snapshot": admission_snapshot,
        "source_sha256": source_snapshot["sha256"],
        "admission_sha256": LEAD_ADMISSION_SHA,
        "immutable_reference_sha256": ref_sha,
        "result_hashes": {
            "payload_sha256": payload_hash,
            "payload_canonical": "json.dumps(sort_keys=True, separators=(',',':'))",
            "source_sha256": source_snapshot["sha256"],
            "admission_sha256": LEAD_ADMISSION_SHA,
            "immutable_reference_sha256": ref_sha,
        },
        "result_summary": payload,
        "interpretation": ("Agreement certifies ONLY this fixed witness "
                            "trajectory; no infinite inference is drawn."),
        "status": "finite-exhaustive",
        "proof_scope": ("singleton fixed trajectory: one 6-cell cyclic "
                         "physical Rule 30 input, 6 updates"),
        "limitations": [
            "single fixed witness; not a census over periods, inputs, or heights",
            "agreement checks the certificate only; growth claims untouched",
            "low pair 2: not a permitted actual survivor",
        ],
        "admission": {
            "basis": ("lead-note admission section + problem1_focus_program "
                       "critical path (aligned-witness strengthening test)"),
            "either_outcome": ("agree=>witness stands; disagree=>withdrawn, "
                                "no search expansion"),
        },
        "provenance_repair": {
            "reason": ("v4 loader: shared authenticated-history loader; "
                        "overwrite-robust v2 location; load-only verification"),
            "reruns": 2,
            "executions_total": 3,
            "scope": "same input, same 6 updates; repair, not expansion",
        },
        "superseded_prior_record": v1_record,
        "superseded_source_snapshot": v1_source_snapshot,
        "archived_executions": archived_executions,
    }
    out_path = os.path.join(REPO, OUT_REL)
    tmp_path = out_path + ".tmp-%d" % os.getpid()
    with open(tmp_path, "w") as f:
        json.dump(record, f, indent=2)
        f.write("\n")
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp_path, out_path)
    signal.alarm(0)
    print("wrote %s words=%r elapsed=%.4fs payload=%s via=%s" %
          (OUT_REL, got_words, elapsed, payload_hash[:16], hist["history_via"]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
