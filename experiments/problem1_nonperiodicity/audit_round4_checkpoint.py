#!/usr/bin/env python3
"""Archive/provenance checks only; never rerun a scientific experiment."""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import tempfile
import time

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "results/problem1/20260906_round4_final_audit.json"
REF = "358bdc07904e77080eb78b67bdd8da25822d6b51f1a91b58b5313dfe461c1d01"
STEMS = ["activity_finiteness_review", "activity_return_nonincrease_primary",
         "activity_return_nonincrease_independent", "activity_return_nonincrease_verification",
         "activity_return_nonincrease_review", "effective_activity_levels_review",
         "activity_criteria_full_review"]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def digest(obj):
    return sha(json.dumps(obj, sort_keys=True, separators=(",", ":")).encode())


def proof_sections(source, last):
    return source.split("\n## 1.", 1)[1].split("\n## " + str(last) + ".", 1)[0]


def main():
    started = time.monotonic()
    records, record_hashes, checks = {}, {}, []

    def check(name, condition):
        assert condition, name
        checks.append(name)

    check("immutable reference", sha((ROOT / "src/python/rule30_research_reference.py").read_bytes()) == REF)
    required = {"experiment_id", "timestamp_utc", "git_commit", "question", "hypothesis", "backend",
                "parameters", "hardware", "software", "runtime_seconds", "result_hashes",
                "result_summary", "interpretation", "status", "proof_scope", "limitations"}
    for stem in STEMS:
        p = ROOT / ("results/problem1/20260906_" + stem + ".json")
        raw = p.read_bytes()
        o = records[stem] = json.loads(raw)
        record_hashes[str(p.relative_to(ROOT))] = sha(raw)
        check(stem + ": protocol fields", required <= o.keys())
        check(stem + ": full Git", bool(re.fullmatch("[0-9a-f]{40}", o["git_commit"])))
        check(stem + ": finite timing", 0 <= o["runtime_seconds"] < 120)

    f = records["activity_finiteness_review"]
    for relative, entry in f["reviewed_sources"].items():
        check("finiteness source snapshot " + relative, sha(entry["source"].encode()) == entry["sha256"])
        if entry["version"] != "working-tree":
            raw = subprocess.check_output(["git", "show", entry["version"] + ":" + relative], cwd=ROOT)
            check("finiteness historical source " + relative, sha(raw) == entry["sha256"])
        else:
            check("finiteness current theorem", sha((ROOT / relative).read_bytes()) == entry["sha256"])

    for key, review_path in (
            ("activity_finiteness_review", "problem1_activity_finiteness_independent_review.md"),
            ("activity_return_nonincrease_review", "problem1_activity_return_nonincrease_review.md"),
            ("effective_activity_levels_review", "problem1_effective_activity_levels_review.md"),
            ("activity_criteria_full_review", "problem1_activity_criteria_full_review.md")):
        o = records[key]
        check(key + ": embedded review", sha(o["review_text"].encode()) == o["result_hashes"]["review_sha256"])
        check(key + ": frozen review file", sha((ROOT / "proofs/informal" / review_path).read_bytes()) == o["result_hashes"]["review_sha256"])
        check(key + ": reference", o["reference_sha256"] == REF)
        if "summary_sha256" in o["result_hashes"]:
            check(key + ": summary", digest(o["result_summary"]) == o["result_hashes"]["summary_sha256"])

    p = records["activity_return_nonincrease_primary"]
    i = records["activity_return_nonincrease_independent"]
    v = records["activity_return_nonincrease_verification"]
    r = records["activity_return_nonincrease_review"]
    check("primary reloaded payload", sha(json.dumps(p["checks"], sort_keys=True).encode()) == p["result_hashes"]["primary_payload_sha256"])
    check("primary source snapshot", sha(p["self_source"]["embedded_text"].encode()) == p["self_source"]["sha256"])
    check("primary current executable", sha((ROOT / p["self_source"]["path"]).read_bytes()) == p["self_source"]["sha256"])
    check("primary admission", sha(p["admission"]["note_text"].encode()) == p["admission"]["note_sha256"])
    check("primary reference", p["reference"]["sha256"] == REF)
    check("independent results", digest(i["results"]) == i["result_hashes"]["results_sha256"])
    check("independent summary", digest(i["result_summary"]) == i["result_hashes"]["summary_sha256"])
    for name in ("source", "admission"):
        check("independent " + name + " snapshot", sha(i["provenance"][name].encode()) == i["provenance"][name + "_sha256"])
    check("independent current executable", sha((ROOT / i["provenance"]["source_path"]).read_bytes()) == i["provenance"]["source_sha256"])
    check("independent reference", i["provenance"]["reference_sha256"] == REF)
    check("verification summary", digest(v["result_summary"]) == v["result_hashes"]["summary_sha256"])
    check("verification source snapshot", sha(v["executed_source"].encode()) == v["result_hashes"]["source_sha256"])
    check("verification current executable", sha((ROOT / "experiments/problem1_nonperiodicity/verify_activity_return_nonincrease.py").read_bytes()) == v["result_hashes"]["source_sha256"])
    for name in ("primary", "independent"):
        check("verification input " + name, v["result_hashes"][name + "_sha256"] == record_hashes["results/problem1/20260906_activity_return_nonincrease_" + name + ".json"])
    check("stored full verification passed", v["result_summary"]["all_checks_passed"])
    for relative, expected in r["source_and_result_hashes"].items():
        check("return review input " + relative, sha((ROOT / relative).read_bytes()) == expected)
    check("return reviewed original admission", sha(r["reviewed_original_admission"]["source"].encode()) == r["reviewed_original_admission"]["sha256"])
    check("return review verification", r["result_hashes"]["verification_sha256"] == record_hashes["results/problem1/20260906_activity_return_nonincrease_verification.json"])

    e = records["effective_activity_levels_review"]
    check("effective reviewed source", sha(e["reviewed_note"].encode()) == e["result_hashes"]["note_sha256"])
    current = (ROOT / "proofs/informal/problem1_effective_activity_levels.md").read_text()
    check("effective source differs only before first section", current.split("\n## ", 1)[1] == e["reviewed_note"].split("\n## ", 1)[1])
    c = records["activity_criteria_full_review"]
    for relative, entry in c["reviewed_sources"].items():
        check("criteria reviewed source " + relative, sha(entry["source"].encode()) == entry["sha256"])
        last = 5 if "single_column" in relative else 6
        check("criteria theorem body unchanged " + relative, proof_sections(entry["source"], last) == proof_sections((ROOT / relative).read_text(), last))
    check("criteria prior review", c["result_hashes"]["prior_review_sha256"] == f["result_hashes"]["review_sha256"])

    archive = ROOT / "docs/astra_handoff_archive_20260906_round4.md"
    prior_commit = subprocess.check_output(["git", "rev-parse", "a9b1d08"], cwd=ROOT, text=True).strip()
    old = subprocess.check_output(["git", "show", prior_commit + ":ASTRA_HANDOFF.md"], cwd=ROOT)
    check("prior handoff preserved byte for byte", archive.read_bytes() == old)
    check("compact handoff at most 200 lines", len((ROOT / "ASTRA_HANDOFF.md").read_text().splitlines()) <= 200)
    check("research branch", subprocess.check_output(["git", "branch", "--show-current"], cwd=ROOT, text=True).strip() == "research/astra-next")
    source = Path(__file__).read_bytes()
    now = datetime.now(timezone.utc)
    cpu = next((line.split(":", 1)[1].strip() for line in Path("/proc/cpuinfo").read_text().splitlines()
                if line.startswith("model name")), "unknown")
    summary = {"all_checks_passed": True, "archival_checks": len(checks), "records": len(STEMS),
               "new_scientific_runs": 0, "prior_handoff_bytes": len(old),
               "handoff_lines": len((ROOT / "ASTRA_HANDOFF.md").read_text().splitlines()),
               "new_numerical_domain": "only the admitted previously stored two return endpoints"}
    result = {
        "experiment_id": "20260906-round4-final-audit", "timestamp_utc": now.isoformat(),
        "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "question": "problem1", "hypothesis": "Round-four archives, proof sources and preservation records reload exactly",
        "backend": "local-archive-only-no-scientific-rerun",
        "parameters": {"record_stems": STEMS, "prior_handoff_commit": prior_commit,
                       "round_started_utc": "2026-09-06T20:17:51+00:00", "new_scientific_runs": 0},
        "hardware": {"cpu": cpu, "machine": platform.machine(), "logical_cpus": os.cpu_count()},
        "software": {"python": platform.python_version(), "platform": platform.platform()},
        "runtime_seconds": time.monotonic() - started,
        "session_elapsed_seconds": (now - datetime.fromisoformat("2026-09-06T20:17:51+00:00")).total_seconds(),
        "result_hashes": {"summary_sha256": digest(summary), "checks_sha256": digest(checks),
                          "source_sha256": sha(source), "prior_handoff_sha256": sha(old),
                          "current_handoff_sha256": sha((ROOT / "ASTRA_HANDOFF.md").read_bytes())},
        "record_hashes": record_hashes, "reference_sha256": REF, "executed_source": source.decode(),
        "result_summary": summary, "checks": checks, "status": "finite-exhaustive",
        "proof_scope": "Exactly these archival/provenance checks, not a scientific proof or a new experiment.",
        "interpretation": "Maintenance checkpoint; actual-survivor growth and Problem 1 remain open.",
        "limitations": ["No scientific run, sublevel list or new search was performed by this audit.",
                        "Source versions are preserved and status-only prose updates are distinguished.",
                        "Final maintenance commit and push are subsequent Git operations."]}
    with tempfile.NamedTemporaryFile("w", dir=OUT.parent, delete=False) as fobj:
        json.dump(result, fobj, indent=2, sort_keys=True)
        fobj.write("\n")
        fobj.flush()
        os.fsync(fobj.fileno())
        temp = fobj.name
    os.replace(temp, OUT)
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
