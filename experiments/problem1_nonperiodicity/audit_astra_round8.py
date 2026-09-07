"""Archive round-eight hand mathematics and reviews; no scientific run."""
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
BASE = "69dc3a166a33687dd7416849ba44106c55bddb36"
START = datetime(2026, 9, 7, 0, 36, 14, tzinfo=timezone.utc)
REFERENCE = "358bdc07904e77080eb78b67bdd8da25822d6b51f1a91b58b5313dfe461c1d01"
OUT = ROOT / "results/problem1/20260907_round8_audit.json"


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def snapshot(name):
    raw = (ROOT / name).read_bytes()
    return {"path": name, "sha256": sha(raw), "text": raw.decode()}


def main():
    started = time.perf_counter()
    assert git("branch", "--show-current") == "research/astra-next"
    assert sha((ROOT / "src/python/rule30_research_reference.py").read_bytes()) == REFERENCE
    assert not git("diff", BASE, "--", "src/python/rule30_research_reference.py")
    archive = "docs/astra_handoff_archive_20260907_round8.md"
    assert (ROOT / archive).read_bytes() == subprocess.check_output(
        ["git", "show", BASE + ":ASTRA_HANDOFF.md"], cwd=ROOT)
    source = snapshot("proofs/informal/problem1_bounded_lag_doubling_controls.md")
    reviews = [snapshot("proofs/informal/" + name) for name in (
        "problem1_round8_bounded_lag_review.md", "problem1_round8_fresh_review.md")]
    assert all(source["sha256"] in review["text"] for review in reviews)
    dependencies = ["problem1_full_fringe_temporal_diagonal.md",
                    "problem1_activity_sparse_temporal_codes.md",
                    "problem1_inverse_scan_reset_language.md",
                    "problem1_scan_doubling_cycle_lag.md",
                    "problem1_anchored_activity_finite_entry.md"]
    record = {
        "experiment_id": "20260907_round8_audit",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "git_commit": git("rev-parse", "HEAD"), "question": "problem1",
        "hypothesis": "Round-eight hand construction and scoped reviews have authenticated recoverable sources.",
        "backend": "archival-integrity-only-no-scientific-run",
        "parameters": {"round_base_commit": BASE, "round_started_utc": START.isoformat(),
                       "scientific_runs": 0, "scope": "all P exists x; zero fringe D0=D1=D2=3; A^4 x finite periodic; source tau<=4, successor tau<=2; unbounded doubling-source periods",
                       "review_model": "opencode-go/muse-spark-1.3-contributor",
                       "source_snapshot_policy": "git_commit is the pre-checkpoint HEAD; exact working source bytes are separately snapshotted and hashed",
                       "review_roles": "sidecar worker scoped review, then new-context adversarial reviewer; IDs and timings in review files",
                       "resource_cap": "local archival work only; 20 seconds, 4 MiB output"},
        "hardware": {"uname": list(platform.uname()), "logical_cpus": os.cpu_count(), "gpu_used": False},
        "software": {"python": sys.version, "executable": sys.executable},
        "runtime_seconds": time.perf_counter() - started,
        "research_elapsed_seconds": (datetime.now(timezone.utc) - START).total_seconds(),
        "status": "finite-exhaustive",
        "proof_scope": "Finite archival integrity only; mathematics retains partial-proof/refuted local scopes.",
        "result_hashes": {"immutable_reference_sha256": REFERENCE,
                          "builder_sha256": sha(Path(__file__).read_bytes())},
        "result_summary": {"incoming_handoff_byte_identical": True,
                           "source_hash_in_both_reviews": True, "problem1": "open",
                           "infinite_FULL_exclusion": "unproved",
                           "bounded_lag_infinite_orbit_question": "inconclusive"},
        "interpretation": "The local lower-bound obstruction rests on an all-depth construction and hand review, not computed periods or a prefix census.",
        "limitations": ["The input varies with the requested source-period bound.",
                        "Initial x is finite-entry, not proved initially finite.",
                        "Only D0,D1,D2 are fixed; no FULL or infinite permitted orbit is constructed.",
                        "Sidecar initial orbit-level nonforcing overclaim and onset-three claim were rejected and corrected before acceptance.",
                        "Runtime measures archival work; research wall time is separate."],
        "proof_source": source, "reviews": reviews,
        "superseded_sidecar": snapshot("proofs/informal/problem1_round8_lag_sidecar.md"),
        "dependencies": [{"path": "proofs/informal/" + name,
                          "sha256": sha((ROOT / "proofs/informal" / name).read_bytes())}
                         for name in dependencies],
        "incoming_handoff": snapshot(archive), "current_handoff": snapshot("ASTRA_HANDOFF.md"),
        "builder_source": snapshot(str(Path(__file__).relative_to(ROOT))),
    }
    raw = (json.dumps(record, indent=2, sort_keys=True) + "\n").encode()
    assert len(raw) < 4 * 1024 * 1024 and time.perf_counter() - started < 20
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
    print(json.dumps({"path": str(OUT.relative_to(ROOT)), "sha256": sha(raw),
                      "bytes": len(raw), "scientific_runs": 0}))


if __name__ == "__main__":
    main()
