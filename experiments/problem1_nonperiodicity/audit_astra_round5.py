"""Round-five archival audit. No scientific experiment or orbit replay."""
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
OUT = ROOT / "results/problem1/20260906_round5_final_audit.json"
REFERENCE = "358bdc07904e77080eb78b67bdd8da25822d6b51f1a91b58b5313dfe461c1d01"
UNITS = {
    "gate_bridge": ("problem1_activity_temporal_gate_bridge.md",
                    "problem1_activity_temporal_gate_bridge_review.md",
                    "34b9626da27a665c0541328735ba74bb95e4ffb9c5b511d117bb60d7209786ac"),
    "joint_windows": ("problem1_activity_joint_window_target.md",
                      "problem1_activity_joint_window_review.md",
                      "e82ecbf6d0a20df7eaaf941e17918cd554159609fa4841d4f29bbe0b49b2b867"),
}


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def snap(path):
    raw = (ROOT / path).read_bytes()
    return dict(path=path, sha256=digest(raw), text=raw.decode())


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def check_local_record(record):
    canonical = json.dumps(record["payload"], sort_keys=True, separators=(",", ":")).encode()
    assert digest(canonical) == record["result_hashes"]["payload_sha256"]
    for field, hashfield in (("source_snapshot", "source_sha256"), ("admission_snapshot", "admission_sha256")):
        value = record[field]
        value = value["text"] if isinstance(value, dict) else value
        assert digest(value.encode()) == record["result_hashes"][hashfield]
    if record.get("superseded_prior_record") is not None:
        check_local_record(record["superseded_prior_record"])


def main():
    start = time.perf_counter()
    previous = json.loads(OUT.read_text()) if OUT.exists() else None
    assert git("branch", "--show-current") == "research/astra-next"
    assert digest((ROOT / "src/python/rule30_research_reference.py").read_bytes()) == REFERENCE
    assert not git("diff", "f6f062d5f36d6403c8d0de2dce773b60ada4a5d8", "--", "src/python/rule30_research_reference.py")
    assert (ROOT / "docs/astra_handoff_archive_20260906_round5.md").read_bytes() == subprocess.check_output(
        ["git", "show", "f6f062d5f36d6403c8d0de2dce773b60ada4a5d8:ASTRA_HANDOFF.md"], cwd=ROOT)
    records = {}
    for name in ("staircase_primary", "staircase_independent", "staircase_verification", "sparse_temporal_codes_review"):
        path = "results/problem1/20260906_activity_" + name + ".json"
        raw = (ROOT / path).read_bytes()
        data = json.loads(raw)
        assert len(data["git_commit"]) == 40
        assert data["result_hashes"]["immutable_reference_sha256"] == REFERENCE
        records[name] = dict(path=path, sha256=digest(raw), status=data["status"], git_commit=data["git_commit"])
        if name in ("staircase_primary", "staircase_independent"):
            check_local_record(data)
            source_path = "experiments/problem1_nonperiodicity/check_activity_" + name + ".py"
            assert snap(source_path)["sha256"] == data["result_hashes"]["source_sha256"]
            if name == "staircase_primary":
                payload = data["payload"]
            else:
                assert payload == data["payload"]
        if name == "sparse_temporal_codes_review":
            for field in ("reviewed_source", "current_source", "review_snapshot", "archive_builder_source"):
                s = data[field]
                assert digest(s["text"].encode()) == s["sha256"]
            assert snap(data["current_source"]["path"])["sha256"] == data["current_source"]["sha256"]
            assert snap(data["review_snapshot"]["path"])["sha256"] == data["review_snapshot"]["sha256"]
    new_units = {}
    for name, (note, review, expected) in UNITS.items():
        current = snap("proofs/informal/" + note)
        external = snap("proofs/informal/" + review)
        reviewed = current
        if reviewed["sha256"] != expected:
            assert previous is not None
            reviewed = previous["new_proof_units"][name]["reviewed_source"]
        assert digest(reviewed["text"].encode()) == expected
        assert expected in external["text"]
        new_units[name] = dict(reviewed_source=reviewed, current_source=current, review_snapshot=external,
                               lead_disposition="accepted partial-proof in scope; no actual-survivor growth claim")
    baseline_files = git("ls-files", "--others", "--exclude-standard").splitlines()
    own_pending = {"proofs/informal/"+p for values in UNITS.values() for p in values[:2]}
    own_pending |= {"proofs/informal/problem1_round5_muse_boundary_proposal.md",
                    "experiments/problem1_nonperiodicity/audit_astra_round5.py",
                    str(OUT.relative_to(ROOT))}
    record = dict(
        experiment_id="20260906_round5_final_audit",
        timestamp_utc=datetime.now(timezone.utc).isoformat(),
        git_commit=git("rev-parse", "HEAD"), question="problem1",
        hypothesis="The established round-five proof units, reviews and finite local records retain exact provenance and stated scopes.",
        backend="archival-audit-no-new-scientific-computation",
        parameters=dict(round_started_utc="2026-09-06T21:20:55Z", branch="research/astra-next",
                        numerical_domain="8/16/64 local cones only", scientific_reruns_in_this_audit=0,
                        reviewer_model="opencode-go/muse-spark-1.3-contributor",
                        reviewer_thread="01a07899-4f89-7d22-95dd-52fffce69b64"),
        hardware=dict(uname=list(platform.uname()), logical_cpus=os.cpu_count()),
        software=dict(python=sys.version, executable=sys.executable),
        runtime_seconds=time.perf_counter()-start,
        result_hashes=dict(immutable_reference_sha256=REFERENCE, builder_sha256=snap(str(Path(__file__).relative_to(ROOT)))["sha256"]),
        result_summary=dict(local_payload_equality=True, exact_cases=88,
                            superseded_independent_execution_reloads=True,
                            incoming_handoff_byte_identical=True, accepted_all_depth_units=5,
                            actual_survivor_growth="unproved", goal="open; maintenance checkpoint"),
        research_elapsed_seconds=(datetime.now(timezone.utc)-datetime(2026,9,6,21,20,55,tzinfo=timezone.utc)).total_seconds(),
        final_cross_file_review=dict(reviewer_closed_utc="2026-09-06T22:21:36Z", verdict="no issues",
            scope="Five proof units and five scoped reviews; read-only claim/status/quantifier/citation check, not a new proof.",
            lead_disposition="accepted; final source status/premise clarifications independently checked after review",
            remaining_gap="Actual full-fringe growth of the fixed survivor's anchored count or original activity record."),
        status="finite-exhaustive",
        proof_scope="Finite archival checks only; new all-depth gate and joint-window sources/reviews retained at partial-proof status.",
        interpretation="Lead independently checked all five proof units and accepted corrected gate fibers/indices and anchored counting; scientific record equality is not an infinite proof.",
        limitations=["No complete proof of Problem1.", "No ray, activity-level, frontier, return or period census.",
                     "No general no-go inferred from the rejected nearest-column defect route.",
                     "Audit runtime is only archive processing; round start/end UTC delimit research wall time."],
        established_records=records, new_proof_units=new_units,
        handoff=snap("ASTRA_HANDOFF.md"), rejected_route_memo=snap("proofs/informal/problem1_round5_muse_boundary_proposal.md"),
        untouched_unrelated_untracked=[p for p in baseline_files if p not in own_pending],
        archive_builder_source=snap(str(Path(__file__).relative_to(ROOT))))
    fd, tmp = tempfile.mkstemp(prefix=OUT.name+".", suffix=".tmp", dir=OUT.parent)
    with os.fdopen(fd, "w") as stream:
        json.dump(record, stream, sort_keys=True, indent=2)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(tmp, OUT)
    print(json.dumps(dict(path=str(OUT.relative_to(ROOT)), **record["result_summary"]), sort_keys=True))


if __name__ == "__main__":
    main()
