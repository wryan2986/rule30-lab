#!/usr/bin/env python3
"""Portable comparison of saved complete vectors; does not rerun research."""
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import platform
import subprocess
import time

from check_temporal_activity_deficit_independent import ROOT, atomic, sha, digest

NAMES = {
    "primary": "20260906_temporal_activity_deficit_primary.json",
    "initial": "20260906_temporal_activity_deficit_initial.json",
    "independent": "20260906_temporal_activity_deficit_independent.json",
    "single_column": "20260906_single_column_activity_independent.json",
}
OUT = ROOT / "results/problem1/20260906_temporal_activity_deficit_verification.json"


def run():
    start = time.monotonic()
    raw = {key: (ROOT / "results/problem1" / name).read_bytes() for key, name in NAMES.items()}
    records = {key: json.loads(value) for key, value in raw.items()}
    p, old = records["primary"], records["initial"]
    d, v = records["independent"], records["single_column"]
    source_audits = []
    for label, record in (("primary", p), ("initial", old)):
        assert sha(json.dumps(record["checks"], sort_keys=True).encode()) == record["result_hashes"]["primary_payload_sha256"]
        source = record["self_source"]
        assert sha(source["embedded_text"].encode()) == source["sha256"]
        if label == "primary":
            assert sha((ROOT / source["path"]).read_bytes()) == source["sha256"]
        source_audits.append([label, source["path"], source["sha256"]])
    for label, record in (("independent", d), ("single_column", v)):
        for key, value in record["results"].items():
            assert digest(value) == record["result_hashes"][key]
        prov = record["provenance"]
        assert sha(prov["source"].encode()) == prov["source_sha256"]
        assert sha((ROOT / prov["source_path"]).read_bytes()) == prov["source_sha256"]
        assert sha(prov["admission"].encode()) == prov["admission_sha256"]
        source_audits.append([label, prov["source_path"], prov["source_sha256"]])
    assert sha(v["provenance"]["dependency"].encode()) == v["provenance"]["dependency_sha256"]
    assert sha((ROOT / v["provenance"]["dependency_path"]).read_bytes()) == v["provenance"]["dependency_sha256"]
    assert sha(raw["independent"]) == v["provenance"]["deficit_record_sha256"]
    for field, hash_field in (("note_text", "note_sha256"), ("V_note_text", "V_note_sha256")):
        assert sha(p["admission"][field].encode()) == p["admission"][hash_field]
    old_note_candidates = [p["admission"]["note_text"], d["provenance"]["admission"]]
    old_note = next(text for text in old_note_candidates if sha(text.encode()) == old["admission"]["note_sha256"])

    pc, dr, vr = p["checks"], d["results"], v["results"]
    assert pc["dz_rows"] == dr["rows"]
    assert old["checks"]["dz_rows"] == pc["dz_rows"]
    assert pc["local256"]["rows"] == dr["local_charge_rows"]
    assert pc["local256"]["charge5_images"] == [26, 27]
    assert pc["temporal64"]["rows"] == dr["temporal_word_rows"]
    for row in dr["harmonics"]:
        pr = pc["harmonic"][str(row["K"])]
        assert [pr["sum_num"], pr["sum_den"]] == row["sum"]
        assert [pr["prev_num"], pr["prev_den"]] == row["previous_sum"]
        assert pr["h"] == row["h"]
    for row in dr["forced_rows"]:
        assert pc["gates"]["x" + str(row["x"])] == row["states"]
    assert pc["stopped111"]
    assert len(pc["seam_rows"]) == len(dr["seams"]) == 32
    for a, b in zip(pc["seam_rows"], dr["seams"]):
        assert [int(a["input"]), a["s"], a["Z_next"], a["Z_F"], a["I"], a["J"], a["lhs"]] == [b["x"], b["s"], b["Z_next_age"], b["Z_forced"], b["I"], b["J"], b["difference"]]
        assert a["rhs"] == a["lhs"] and a["ok"]
    dz_lookup = {(r["input"], r["s"]): r["Z"] for r in pc["dz_rows"]}
    for name, s, h, k, z, bound in dr["entry_checks"]:
        entry = pc["entry"][name]
        assert [entry["h"], entry["k"]] == [h, k]
        assert dz_lookup[name, s] == z <= bound == min(s, max(h, k))
        assert entry["bound_ok"]
    assert pc["v_rows"] == vr["rows"]
    assert pc["v_entry_bounds"] == vr["entry_bounds"]
    assert pc["v_comparisons"] == vr["comparisons"]
    assert pc["v_seams"] == vr["seams"]

    reference_hash = sha((ROOT / "src/python/rule30_research_reference.py").read_bytes())
    assert reference_hash == "358bdc07904e77080eb78b67bdd8da25822d6b51f1a91b58b5313dfe461c1d01"
    for record in (p, old):
        assert record["reference"]["sha256"] == reference_hash
    for record in (d, v):
        assert record["provenance"]["reference_sha256"] == reference_hash
    result = {
        "D_full_vectors": len(dr["rows"]), "D_entry_bounds": len(dr["entry_checks"]),
        "local_charge_rows": len(dr["local_charge_rows"]), "temporal_word_rows": len(dr["temporal_word_rows"]),
        "harmonic_thresholds": [[r["K"], r["h"]] for r in dr["harmonics"]],
        "D_complete_seams": len(dr["seams"]), "forced_orbits": len(dr["forced_rows"]),
        "V_full_vectors": len(vr["rows"]), "V_entry_bounds": len(vr["entry_bounds"]),
        "V_comparisons": len(vr["comparisons"]), "V_complete_seams": len(vr["seams"]),
        "source_audits": source_audits, "reference_sha256": reference_hash,
        "all_finite_comparisons_passed": True,
    }
    source = Path(__file__).read_bytes()
    record = {
        "experiment_id": "20260906-temporal-activity-deficit-verification",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "question": "problem1", "hypothesis": "Complete modular/cell vectors and their archived provenance agree on the admitted finite cases",
        "backend": "read-only-saved-vector-and-hash-verifier",
        "parameters": {"records": NAMES, "scientific_runs_repeated": 0, "cpu_concurrency": 1},
        "hardware": {"machine": platform.machine(), "logical_cpus": os.cpu_count()},
        "software": {"python": platform.python_version(), "platform": platform.platform()},
        "runtime_seconds": time.monotonic() - start,
        "result_hashes": {"comparison": digest(result), **{key: sha(value) for key, value in raw.items()}},
        "result_summary": result,
        "interpretation": "The complete declared finite vectors agree. Mathematical review is recorded separately and is not inferred from these checks.",
        "status": "finite-exhaustive",
        "proof_scope": "Saved row-by-row comparisons, exact finite arithmetic, and source/admission/reference hash linkage only.",
        "limitations": ["The initial primary entry-detection procedure is superseded, not accepted as an infinite certificate.",
                        "No finite run proves the compactness, last-time, or unbounded-growth assertions.",
                        "The actual survivor's record growth remains open."],
        "provenance": {"source_path": str(Path(__file__).relative_to(ROOT)), "source_sha256": sha(source), "source": source.decode(),
                       "helper_path": "experiments/problem1_nonperiodicity/check_temporal_activity_deficit_independent.py",
                       "helper_sha256": d["provenance"]["source_sha256"],
                       "initial_matching_note_sha256": sha(old_note.encode()), "initial_matching_note": old_note},
        "integration_audit": {
            "initial_primary": "Muse produced the initial modular record before returning provider429 on its delayed retry; no full mathematical verdict was supplied.",
            "initial_scope_error": "Detected modular values below2**24 were reported after an unadmitted entry search through8. These are not proofs of finite 2-adic tails.",
            "correction": "Lead used the stipulated exact entry identities, preserved the initial record, added only the separately admitted V controls and compared every vector.",
            "fallback_primary": "MiMo fallback was closed while running after approximately13minutes without a delivered correction or usable proof verdict; lead performed the essential integration.",
            "implementation_launch_issues": ["The python alias was absent; the independent script ran with python3.",
                                             "A local resource import shadowed the new top-level import; corrected before the primary computation began."],
        },
    }
    atomic(OUT, record)
    print(json.dumps({k: v for k, v in result.items() if k not in ("source_audits", "reference_sha256")}, sort_keys=True))


if __name__ == "__main__":
    run()
