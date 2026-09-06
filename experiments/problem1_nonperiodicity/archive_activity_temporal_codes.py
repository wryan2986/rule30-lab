"""Atomic provenance for the sparse temporal-code proof; no numerical run."""
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
NOTE = "proofs/informal/problem1_activity_sparse_temporal_codes.md"
REVIEW = "proofs/informal/problem1_activity_sparse_temporal_codes_review.md"
OUT = ROOT / "results/problem1/20260906_activity_sparse_temporal_codes_review.json"
REVIEWED_SHA = "d28e7f942e6a7380e7f3fb9927e9f3ce09d5c05be703284811768161bcbffbb3"


def snap(path):
    raw = (ROOT / path).read_bytes()
    return dict(path=path, sha256=hashlib.sha256(raw).hexdigest(), text=raw.decode())


def main():
    start = time.perf_counter()
    note, review = snap(NOTE), snap(REVIEW)
    reviewed = note
    if reviewed["sha256"] != REVIEWED_SHA:
        reviewed = json.loads(OUT.read_text())["reviewed_source"]
    assert hashlib.sha256(reviewed["text"].encode()).hexdigest() == REVIEWED_SHA
    assert REVIEWED_SHA in review["text"]
    paths = ["proofs/informal/problem1_activity_level_finiteness.md",
             "proofs/informal/problem1_activity_transport_inequality.md",
             "proofs/informal/problem1_effective_activity_levels.md"]
    dependencies = [dict(path=p, sha256=snap(p)["sha256"]) for p in paths]
    reference = hashlib.sha256((ROOT / "src/python/rule30_research_reference.py").read_bytes()).hexdigest()
    assert reference == "358bdc07904e77080eb78b67bdd8da25822d6b51f1a91b58b5313dfe461c1d01"
    source = snap(str(Path(__file__).relative_to(ROOT)))
    record = dict(
        experiment_id="20260906_activity_sparse_temporal_codes_review",
        timestamp_utc=datetime.now(timezone.utc).isoformat(),
        git_commit=subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        question="problem1",
        hypothesis="The A temporal coding and sparse-code counterexample are exact; fixed-ray density is sufficient but not necessary for unbounded activity.",
        backend="proof-derivation-and-adversarial-review-archive",
        parameters=dict(note=NOTE, review=REVIEW, reviewer_model="opencode-go/muse-spark-1.3-contributor",
                        review_scope="all Sections1-4", numerical_runs=0,
                        sparse_code="any finite prefix, then symbol1 exactly at powers of two and symbol0 otherwise"),
        hardware=dict(uname=list(platform.uname()), logical_cpus=os.cpu_count()),
        software=dict(python=sys.version, executable=sys.executable),
        runtime_seconds=time.perf_counter()-start,
        result_hashes=dict(reviewed_source_sha256=REVIEWED_SHA, current_source_sha256=note["sha256"],
                          review_sha256=review["sha256"], builder_sha256=source["sha256"],
                          immutable_reference_sha256=reference),
        result_summary=dict(temporal_conjugacy="partial-proof", deletion_code_map="partial-proof",
                            rationality_equivalence="partial-proof", density_necessity="refuted on general inputs",
                            actual_survivor_growth="unproved"),
        interpretation="Lead independently rederived the triangular block inverse, g equations, two rationality directions, uniform sparse-window bound and finite-level contradiction; scoped review accepted.",
        status="partial-proof",
        proof_scope="General 2-adic counterexample, including arbitrary finite-cylinder matching; no infinite forced-survivor claim.",
        limitations=["No numerical experiments performed.", "Finite prefix matching does not imply future fringe compatibility.",
                     "The sufficient transport criterion and finite-window inequality survive.",
                     "Archive runtime is not a measurement of human/model proof-discovery time."],
        reviewed_source=reviewed, current_source=note, review_snapshot=review,
        dependencies=dependencies, archive_builder_source=source)
    fd, tmp = tempfile.mkstemp(prefix=OUT.name+".", suffix=".tmp", dir=OUT.parent)
    with os.fdopen(fd, "w") as stream:
        json.dump(record, stream, indent=2, sort_keys=True)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(tmp, OUT)
    print(json.dumps(dict(path=str(OUT.relative_to(ROOT)), status=record["status"], numerical_runs=0)))


if __name__ == "__main__":
    main()
