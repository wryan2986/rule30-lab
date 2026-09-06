"""Archive the exact round-six proof/review checkpoints; no orbit replay."""
import argparse
import ast
import hashlib
import json
import os
import platform
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "results/problem1/20260906_round6_audit.json"
BASE = "a3858002719830ec8e54227ade7b5d81fe5de089"
REFERENCE = "358bdc07904e77080eb78b67bdd8da25822d6b51f1a91b58b5313dfe461c1d01"
START = datetime(2026, 9, 6, 22, 26, 45, tzinfo=timezone.utc)
UNITS = {
    "anchored_finite_entry": ("problem1_anchored_activity_finite_entry.md",
        "problem1_anchored_activity_finite_entry_review.md", "anchored-source-reviewed",
        "180c8b79b1a34129b94431559a3c495c40ecd523c5f6253c14e2f7d4dff6d2a7"),
    "full_fringe_diagonal": ("problem1_full_fringe_temporal_diagonal.md",
        "problem1_full_fringe_temporal_diagonal_review.md", "fringe-source-reviewed",
        "87b54cc3e800c6d295c69eb79c6b2f5c450a9c48b282fad1882e04de8bed7f6e"),
}
TOWER = ("problem1_finite_entry_period_tower.md", "problem1_finite_entry_period_tower_review.md",
         "tower-source-reviewed", "839113840d7829cd89b792244c43e26193c88f1413ee33c23984d00b97f730e9")


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def snapshot(path):
    raw = (ROOT / path).read_bytes()
    return {"path": path, "sha256": digest(raw), "text": raw.decode()}


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def scientific_core(source):
    start = source.index("    # ---- scientific computation")
    end = source.index("    payload_hash", start)
    # The replay-only wrapper raises its failure exception instead of
    # returning the old numeric error code. Successful computation is identical.
    return source[start:end].replace("return fail(", "fail(")


def helper_tree(source, name):
    node = next(n for n in ast.parse(source).body if isinstance(n, ast.FunctionDef) and n.name == name)
    return ast.dump(node, include_attributes=False)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage", choices=("core", "spine", "tower", "final"), required=True)
    args = parser.parse_args()
    started = time.perf_counter()
    previous = json.loads(OUT.read_text()) if OUT.exists() else None
    assert git("branch", "--show-current") == "research/astra-next"
    assert digest((ROOT / "src/python/rule30_research_reference.py").read_bytes()) == REFERENCE
    assert not git("diff", BASE, "--", "src/python/rule30_research_reference.py")
    incoming = ROOT / "docs/astra_handoff_archive_20260906_round6.md"
    assert incoming.read_bytes() == subprocess.check_output(["git", "show", BASE+":ASTRA_HANDOFF.md"], cwd=ROOT)
    units = {}
    selected = dict(UNITS)
    if args.stage in ("tower", "final"):
        selected["finite_entry_period_tower"] = TOWER
    for name, (note, review, temporary, expected) in selected.items():
        source = snapshot("proofs/informal/"+note)
        external = snapshot("proofs/informal/"+review)
        temp = Path("/tmp/astra-round6-"+temporary+".md")
        reviewed = (dict(path=source["path"], sha256=digest(temp.read_bytes()), text=temp.read_text())
                    if temp.exists() else previous["proof_units"][name]["reviewed_source"])
        assert reviewed["sha256"] == expected and expected in external["text"]
        assert digest(reviewed["text"].encode()) == expected
        units[name] = {"reviewed_source": reviewed, "current_source": source, "review": external,
                       "lead_disposition": "accepted partial-proof in declared scope; no actual-survivor growth"}
    rejected_temp = Path("/tmp/astra-round6-anchored-review-initial.md")
    initial_review = (dict(path="initial anchored review (superseded)", text=rejected_temp.read_text(),
                          sha256=digest(rejected_temp.read_bytes())) if rejected_temp.exists()
                      else previous["superseded_initial_review"])
    assert digest(initial_review["text"].encode()) == initial_review["sha256"]
    scientific = {}
    replay_check = None
    if args.stage != "core":
        for role in ("primary", "independent"):
            path = "results/problem1/20260906_anchored_spine_"+role+".json"
            raw = (ROOT / path).read_bytes()
            data = json.loads(raw)
            payload = data["payload"]
            expected_hash = digest(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode())
            assert data["result_hashes"]["payload_sha256"] == expected_hash
            assert data["result_hashes"]["immutable_reference_sha256"] == REFERENCE
            for field, key in (("source_snapshot", "source_sha256"), ("admission_snapshot", "admission_sha256")):
                snap = data[field]
                assert digest(snap["text"].encode()) == data["result_hashes"][key] == snap["sha256"]
            current_checker = snapshot(data["source_snapshot"]["path"])
            if role == "primary":
                assert current_checker["sha256"] == data["result_hashes"]["source_sha256"]
            else:
                executed = data["source_snapshot"]["text"]
                assert scientific_core(executed) == scientific_core(current_checker["text"])
                for helper in ("bits_of", "words_of"):
                    assert helper_tree(executed, helper) == helper_tree(current_checker["text"], helper)
                for entry in data["archived_executions"]:
                    old = entry["record"]
                    if entry["label"].startswith("v2"):
                        for key in ("source_snapshot", "admission_snapshot"):
                            saved = old[key]
                            assert digest(saved["text"].encode()) == saved["sha256"]
                        assert old["payload"] == payload
                        assert old["result_hashes"]["payload_sha256"] == expected_hash
                    else:
                        assert old["result_summary"] == payload
                        assert old["result_hashes"]["payload_sha256"] == digest(json.dumps(payload, sort_keys=True).encode())
                        assert old["result_hashes"]["reference_sha256"] == REFERENCE
                    assert len(old["git_commit"]) == 40
                saved_v1 = data["superseded_source_snapshot"]
                assert digest(saved_v1["text"].encode()) == saved_v1["sha256"]
                environment = dict(os.environ, SPINE_REPLAY_NO_TMP="1")
                replay = subprocess.run([sys.executable, str(ROOT/current_checker["path"]),
                                         "--verify-replay-inputs"], cwd=ROOT, env=environment,
                                        text=True, capture_output=True, timeout=20, check=True)
                assert (ROOT/path).read_bytes() == raw  # metadata-only replay must not write
                replay_check = {"current_wrapper": current_checker,
                                "executed_source_sha256": data["source_snapshot"]["sha256"],
                                "scientific_core_sha256": digest(scientific_core(executed).encode()),
                                "same_successful_scientific_code": True,
                                "wrapper_changes": "repo-archive history loading, metadata-only check, failure exceptions; not a new scientific execution",
                                "stdout": replay.stdout, "stderr": replay.stderr,
                                "returncode": replay.returncode, "scientific_reruns": 0,
                                "record_bytes_unchanged": True, "temporary_history_disabled": True}
            scientific[role] = {"path": path, "sha256": digest(raw), "payload_sha256": expected_hash,
                                "git_commit": data["git_commit"], "status": data["status"]}
            if role == "primary":
                primary_payload = payload
            else:
                assert payload == primary_payload
        note = snapshot("proofs/informal/problem1_anchored_activity_vertical_spine_obstruction.md")
        review = snapshot("proofs/informal/problem1_anchored_activity_vertical_spine_review.md")
        admitted = json.loads((ROOT / scientific["primary"]["path"]).read_text())["admission_snapshot"]
        assert admitted["sha256"] in review["text"]
        units["vertical_spine_obstruction"] = {"reviewed_source": admitted, "current_source": note,
            "review": review, "lead_disposition": "accepted exact counterexample, scoped to coefficient-one lifetime/vertical alignment"}
    dependencies = ["problem1_activity_sparse_temporal_codes.md", "problem1_activity_temporal_gate_bridge.md",
                    "problem1_activity_joint_window_target.md", "problem1_single_column_activity.md",
                    "problem1_effective_activity_levels.md", "problem1_period_two_2adic_zero_countermodels.md",
                    "problem1_frontier_head_dynamics.md"]
    initial_spine_path = Path("/tmp/astra-round6-spine-review-initial.md")
    initial_spine_review = (dict(text=initial_spine_path.read_text(), sha256=digest(initial_spine_path.read_bytes()))
                            if initial_spine_path.exists() else previous.get("superseded_initial_spine_review") if previous else None)
    final_review_path = ROOT / "proofs/informal/problem1_round6_final_review.md"
    record = {
        "experiment_id": "20260906_round6_audit", "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "git_commit": git("rev-parse", "HEAD"), "question": "problem1",
        "hypothesis": "Round-six established proof units, corrected reviews and the optional fixed witness have exact archived provenance.",
        "backend": "archival-audit-no-scientific-rerun",
        "parameters": {"stage": args.stage, "round_base_commit": BASE, "round_started_utc": START.isoformat(),
                       "reviewer_model": "opencode-go/muse-spark-1.3-contributor",
                       "reviewer_thread": "01a078d5-58aa-7ee3-9c1d-15b1bbaa1eed", "scientific_reruns": 0},
        "hardware": {"uname": list(platform.uname()), "logical_cpus": os.cpu_count()},
        "software": {"python": sys.version, "executable": sys.executable},
        "runtime_seconds": time.perf_counter()-started,
        "research_elapsed_seconds": (datetime.now(timezone.utc)-START).total_seconds(),
        "result_hashes": {"immutable_reference_sha256": REFERENCE,
                          "builder_sha256": snapshot(str(Path(__file__).relative_to(ROOT)))["sha256"]},
        "result_summary": {"accepted_units": list(units), "incoming_handoff_byte_identical": True,
                           "scientific_payload_equality": True if scientific else "not yet in this stage",
                           "actual_survivor_growth": "unproved", "problem1": "open"},
        "interpretation": "Proof acceptance comes from independent derivation and lead review, not finite computation.",
        "status": "finite-exhaustive", "proof_scope": "Finite archival integrity checks only; mathematical sources retain their own partial-proof/refuted scopes.",
        "limitations": ["No solution of Problem1 or actual full-fringe growth mechanism.",
                        "No period, frontier, ray or activity-level census.",
                        "Initial review used the wrong extension/shift order; corrected before acceptance.",
                        "Runtime is archive processing; research elapsed seconds is separate."],
        "proof_units": units, "scientific_records": scientific,
        "replay_wrapper_check": replay_check,
        "final_cross_file_review": snapshot(str(final_review_path.relative_to(ROOT))) if final_review_path.exists() else None,
        "superseded_initial_review": initial_review,
        "superseded_initial_spine_review": initial_spine_review,
        "review_error_disposition": "Reject the review's half-line-limit counterexample: extend first, then translate the full row; fixed negative offsets eventually read genuine input bits.",
        "dependency_snapshots": [snapshot("proofs/informal/"+name) for name in dependencies],
        "handoff": snapshot("ASTRA_HANDOFF.md"),
        "corrected_coupling_exposition": snapshot("proofs/informal/problem1_round6_muse_characteristic_coupling.md"),
        "builder_source": snapshot(str(Path(__file__).relative_to(ROOT))),
        "prior_audit_summary": ({"sha256": digest(OUT.read_bytes()), "timestamp_utc": previous["timestamp_utc"],
                                  "git_commit": previous["git_commit"], "stage": previous["parameters"]["stage"]}
                                if previous else None)}
    fd, name = tempfile.mkstemp(prefix=OUT.name+".", suffix=".tmp", dir=OUT.parent)
    with os.fdopen(fd, "w") as stream:
        json.dump(record, stream, sort_keys=True, indent=2)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(name, OUT)
    print(json.dumps({"path": str(OUT.relative_to(ROOT)), **record["result_summary"]}, sort_keys=True))


if __name__ == "__main__":
    main()
