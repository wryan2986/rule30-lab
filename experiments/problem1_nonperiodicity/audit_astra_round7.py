"""Atomically archive round-seven hand proofs/reviews; no scientific run."""
import argparse
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
OUT = ROOT / "results/problem1/20260907_round7_audit.json"
BASE = "239bff4bef739fb99350cc14128c3d8407942264"
REFERENCE = "358bdc07904e77080eb78b67bdd8da25822d6b51f1a91b58b5313dfe461c1d01"
START = datetime(2026, 9, 6, 23, 32, 42, tzinfo=timezone.utc)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def snapshot(path):
    raw = (ROOT / path).read_bytes()
    return {"path": path, "sha256": sha(raw), "text": raw.decode()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stage", choices=("core", "doubling", "final"), required=True)
    parser.add_argument("--repo-only", action="store_true")
    args = parser.parse_args()
    started = time.perf_counter()
    previous = json.loads(OUT.read_text()) if OUT.exists() else None
    assert git("branch", "--show-current") == "research/astra-next"
    assert sha((ROOT / "src/python/rule30_research_reference.py").read_bytes()) == REFERENCE
    assert not git("diff", BASE, "--", "src/python/rule30_research_reference.py")
    archive = "docs/astra_handoff_archive_20260907_round7.md"
    assert (ROOT / archive).read_bytes() == subprocess.check_output(
        ["git", "show", BASE + ":ASTRA_HANDOFF.md"], cwd=ROOT)
    source_names = ["problem1_inverse_scan_reset_language.md", "problem1_scan_cycle_entry_obstruction.md"]
    review_names = ["problem1_inverse_scan_reset_language_review.md"]
    if args.stage != "core":
        source_names += ["problem1_scan_doubling_cycle_lag.md"]
        review_names += ["problem1_scan_doubling_cycle_lag_review.md"]
    if args.stage == "final":
        review_names += ["problem1_round7_final_review.md"]
    sources = [snapshot("proofs/informal/" + name) for name in source_names]
    reviews = [snapshot("proofs/informal/" + name) for name in review_names]
    for source in sources:
        assert any(source["sha256"] in review["text"] for review in reviews), source["path"]
    initial_path = Path("/tmp/astra-round7-reset-review-initial.md")
    if not args.repo_only and initial_path.exists():
        raw = initial_path.read_bytes()
        initial = {"path": "superseded initial reset review", "sha256": sha(raw), "text": raw.decode()}
    else:
        initial = previous["superseded_initial_review"]
    assert sha(initial["text"].encode()) == initial["sha256"]
    dependencies = ["problem1_full_fringe_temporal_diagonal.md", "problem1_activity_sparse_temporal_codes.md",
                    "problem1_activity_temporal_gate_bridge.md", "problem1_anchored_activity_finite_entry.md",
                    "problem1_finite_entry_period_tower.md", "problem1_frontier_head_dynamics.md",
                    "problem1_temporal_activity_deficit.md"]
    record = {
        "experiment_id": "20260907_round7_audit", "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "git_commit": git("rev-parse", "HEAD"), "question": "problem1", "backend": "archival-audit-no-scientific-run",
        "hypothesis": "Reviewed round-seven hand proofs and exact counterexample have authenticated, recoverable sources.",
        "parameters": {"stage": args.stage, "round_base_commit": BASE, "round_started_utc": START.isoformat(),
                       "repository_only_recovery": args.repo_only, "scientific_runs": 0,
                       "reviewer_model": "opencode-go/muse-spark-1.3-contributor",
                       "reviewer_thread": "01a07911-f233-7760-b1a3-fefa4d2ff2d9",
                       "fresh_final_reviewer": ({"model": "opencode-go/muse-spark-1.3-contributor",
                           "thread": "01a07942-51c5-7812-8916-5235d1244eea", "fresh_context": True,
                           "scope": "Independent final adversarial derivation; exact timings in final review source"}
                           if args.stage == "final" else None),
                       "resource_cap": "local metadata only; 20 seconds, 16 MiB output; no trajectory computation"},
        "hardware": {"uname": list(platform.uname()), "logical_cpus": os.cpu_count(), "gpu_used": False},
        "software": {"python": sys.version, "executable": sys.executable},
        "runtime_seconds": time.perf_counter() - started,
        "research_elapsed_seconds": (datetime.now(timezone.utc) - START).total_seconds(),
        "status": "finite-exhaustive", "proof_scope": "Finite archival integrity only; source mathematics retains partial-proof/refuted statuses.",
        "result_hashes": {"immutable_reference_sha256": REFERENCE,
                          "builder_sha256": sha(Path(__file__).read_bytes())},
        "result_summary": {"accepted_proof_sources": source_names, "incoming_handoff_byte_identical": True,
                           "source_hashes_in_external_reviews": True, "problem1": "open", "full_fringe_exclusion": "unproved"},
        "interpretation": "Acceptance rests on hand derivations, fresh Muse reviews and lead audit, not a finite simulation.",
        "limitations": ["No proof of Problem1 or FULL/finite-entry incompatibility.",
                        "No word, transient, orbit, period, frontier, ray or prefix census ran.",
                        "An initial reviewer objection ignored full temporal-code injectivity and was withdrawn.",
                        "Runtime measures archival work; research wall time is separate."],
        "proof_sources": sources, "reviews": reviews, "superseded_initial_review": initial,
        "single_scan_sidecar": snapshot("proofs/informal/problem1_round7_muse_temporal_scan.md"),
        "dependencies": [{"path": "proofs/informal/" + name, "sha256": sha((ROOT / "proofs/informal" / name).read_bytes())}
                         for name in dependencies],
        "incoming_handoff": snapshot(archive), "current_handoff": snapshot("ASTRA_HANDOFF.md"),
        "builder_source": snapshot(str(Path(__file__).relative_to(ROOT))),
    }
    raw = (json.dumps(record, indent=2, sort_keys=True) + "\n").encode()
    assert len(raw) < 16 * 1024 * 1024 and time.perf_counter() - started < 20
    OUT.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=OUT.parent, prefix=OUT.name + ".", suffix=".tmp", delete=False) as handle:
            temporary = Path(handle.name)
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, OUT)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()
    print(json.dumps({"path": str(OUT.relative_to(ROOT)), "stage": args.stage, "sources": len(sources),
                      "bytes": len(raw), "sha256": sha(raw), "scientific_runs": 0}))


if __name__ == "__main__":
    main()
