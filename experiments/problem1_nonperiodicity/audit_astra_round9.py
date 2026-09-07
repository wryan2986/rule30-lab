"""Archive this research unit and its corrected verification; no new science."""
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
BASE = "28f5570d622ceb50bcd5b9e2f78d9c579e2ed419"
START = datetime(2026, 9, 7, 2, 41, 5, tzinfo=timezone.utc)
REFERENCE = "358bdc07904e77080eb78b67bdd8da25822d6b51f1a91b58b5313dfe461c1d01"
INITIAL = "results/problem1/20260907_round9_superseded_run.json"
PROOFS = ["proofs/informal/problem1_cycle_completion_defect_transport.md",
          "proofs/informal/problem1_round9_finite_source_sidecar.md",
          "proofs/informal/problem1_physical_time_cycle_defects.md"]


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def snapshot(name):
    raw = (ROOT / name).read_bytes()
    return {"path": name, "sha256": sha(raw), "text": raw.decode()}


def write_atomic(name, record):
    raw = (json.dumps(record, sort_keys=True, indent=2) + "\n").encode()
    assert len(raw) < 8 * 1024 * 1024
    destination = ROOT / name
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=destination.parent, prefix=destination.name,
                                         suffix=".tmp", delete=False) as handle:
            temporary = Path(handle.name)
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, destination)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()
    print(json.dumps({"path": name, "sha256": sha(raw), "bytes": len(raw)}))


def main():
    started = time.perf_counter()
    assert git("branch", "--show-current") == "research/astra-next"
    assert sha((ROOT / "src/python/rule30_research_reference.py").read_bytes()) == REFERENCE
    assert not git("diff", BASE, "--", "src/python/rule30_research_reference.py")
    capture = sys.argv[1:] == ["--capture-initial"]
    assert not sys.argv[1:] or capture
    record = {
        "experiment_id": "20260907_round9_initial_archive" if capture else "20260907_round9_audit",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "git_commit": git("rev-parse", "HEAD"), "question": "problem1",
        "hypothesis": "Finite archival integrity of the exact research and verification sources.",
        "backend": "local-archival-integrity-only",
        "parameters": {"base_commit": BASE, "research_started_utc": START.isoformat(),
                       "session": "historical round nine; unattended supervisor round one",
                       "source_policy": "Git HEAD is pre-checkpoint; exact working bytes are snapshotted separately.",
                       "resource_cap": "20 seconds and 8 MiB output; local only"},
        "hardware": {"uname": list(platform.uname()), "logical_cpus": os.cpu_count(),
                     "gpu_used": False},
        "software": {"python": sys.version, "executable": sys.executable},
        "status": "finite-exhaustive",
        "proof_scope": "Finite archive integrity only; mathematical claims retain their source statuses.",
        "result_hashes": {"reference_sha256": REFERENCE},
        "builder_source": snapshot(str(Path(__file__).relative_to(ROOT))),
        "limitations": ["Archival runtime is distinct from research elapsed wall time.",
                        "No Problem 1 exclusion follows from archival checks."],
    }
    if capture:
        assert not (ROOT / INITIAL).exists(), "Do not overwrite the original capture"
        record["original_checker"] = snapshot("experiments/problem1_nonperiodicity/check_round9_one_hole_control.py")
        record["original_record"] = snapshot("results/problem1/20260907_round9_one_hole_control.json")
        record["original_sidecar"] = snapshot(PROOFS[1])
        record["result_summary"] = {"accepted_as_final_provenance": False,
                                    "defects": ["Reference hash computed but omitted from record.",
                                                "Nonzero orbit hash omitted; source bytes not snapshotted.",
                                                "Runtime field not numeric; reported caps not enforced."]}
        record["interpretation"] = "Preserve the initial same-input run before correcting its verification and provenance."
        destination = INITIAL
    else:
        archive = "docs/astra_handoff_archive_20260907_round9.md"
        assert (ROOT / archive).read_bytes() == subprocess.check_output(
            ["git", "show", BASE + ":ASTRA_HANDOFF.md"], cwd=ROOT)
        sources = [snapshot(name) for name in PROOFS]
        review = snapshot("proofs/informal/problem1_round9_fresh_review.md")
        assert all(source["sha256"] in review["text"] for source in sources)
        checker = snapshot("experiments/problem1_nonperiodicity/check_round9_one_hole_control.py")
        result = snapshot("results/problem1/20260907_round9_one_hole_control.json")
        run = json.loads(result["text"])
        assert run["result_hashes"]["script_sha256"] == checker["sha256"]
        assert run["result_hashes"]["reference_sha256"] == REFERENCE
        assert run["result_summary"]["first_repeat"] == {
            "word": [0, 3, 0, 3, 3, 0, 0, 3], "first_seen_at": 286, "repeated_at": 818}
        chain = run["result_summary"]["chain"]
        assert len(chain) == 819 and chain[286] == chain[818] and all(any(w) for w in chain)
        assert len({tuple(w) for w in chain[:-1]}) == 818
        assert sha("".join("".join(map(str, w)) for w in chain).encode()) == run["result_hashes"]["chain_sha256"]
        assert sha(run["source_snapshot"].encode()) == checker["sha256"]
        assert isinstance(run["runtime_seconds"], float)
        record.update({"proof_sources": sources, "fresh_review": review,
                       "muse_partial_review": snapshot("proofs/informal/problem1_round9_muse_partial_review.md"),
                       "scientific_checker": checker, "scientific_record": result,
                       "superseded_run": snapshot(INITIAL),
                       "incoming_handoff": snapshot(archive),
                       "current_handoff": snapshot("ASTRA_HANDOFF.md"),
                       "result_summary": {"incoming_handoff_byte_identical": True,
                                          "review_matches_sources": True,
                                          "same_input_correction": True,
                                          "stored_certificate_integrity": True, "problem1": "open"},
                       "review_provenance": {"model": "opencode-go/mimo-v2.5",
                                             "thread": "01a079e2-2a08-7383-8190-5d48dd183a2a",
                                             "orchestration_window_utc": ["2026-09-07 03:20:36", "2026-09-07 03:44:16"],
                                             "prior_Muse_partial_review_read": True,
                                             "blind_review_claimed": False, "all_workers_closed": True,
                                             "lead_disposition": "Accepted corrected source-based adversarial review; three reviewer corrections withdrawn; no Problem1 solution."},
                       "interpretation": "Exact defect transport and a refuted symbolic supply; no infinite FULL contradiction."})
        dependencies = ["problem1_activity_temporal_gate_bridge.md", "problem1_activity_sparse_temporal_codes.md",
                        "problem1_full_fringe_temporal_diagonal.md", "problem1_inverse_scan_reset_language.md",
                        "problem1_anchored_activity_finite_entry.md", "problem1_scan_doubling_cycle_lag.md",
                        "problem1_bounded_lag_doubling_controls.md"]
        record["dependencies"] = [{"path": "proofs/informal/" + name,
                                   "sha256": sha((ROOT / "proofs/informal" / name).read_bytes())}
                                  for name in dependencies]
        destination = "results/problem1/20260907_round9_audit.json"
    record["runtime_seconds"] = time.perf_counter() - started
    record["research_elapsed_seconds"] = (datetime.now(timezone.utc) - START).total_seconds()
    assert record["runtime_seconds"] < 20
    write_atomic(destination, record)


if __name__ == "__main__":
    main()
