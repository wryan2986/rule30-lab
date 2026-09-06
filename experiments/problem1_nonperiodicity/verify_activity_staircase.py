"""Archive and compare the two existing staircase records; no new CA run."""
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
BASE = "results/problem1/20260906_activity_staircase_"


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def snapshot(path):
    raw = (ROOT / path).read_bytes()
    return dict(path=path, sha256=sha(raw), text=raw.decode())


def main():
    start = time.perf_counter()
    out = ROOT / (BASE + "verification.json")
    prior_archive = json.loads(out.read_text()) if out.exists() else None
    primary, independent = [json.loads((ROOT / (BASE + name + ".json")).read_text())
                            for name in ("primary", "independent")]
    sources = []
    for name, record in (("primary", primary), ("independent", independent)):
        assert record["status"] == "finite-exhaustive"
        assert len(record["git_commit"]) == 40
        canonical = json.dumps(record["payload"], sort_keys=True, separators=(",", ":")).encode()
        assert sha(canonical) == record["result_hashes"]["payload_sha256"]
        for field, hashfield in (("source_snapshot", "source_sha256"),
                                 ("admission_snapshot", "admission_sha256")):
            snap = record[field]
            text_value = snap["text"] if isinstance(snap, dict) else snap
            assert sha(text_value.encode()) == record["result_hashes"][hashfield]
        current_source = snapshot(f"experiments/problem1_nonperiodicity/check_activity_staircase_{name}.py")
        assert current_source["sha256"] == record["result_hashes"]["source_sha256"]
        sources.append(current_source)
    assert primary["payload"] == independent["payload"]
    assert primary["result_hashes"]["admission_sha256"] == independent["result_hashes"]["admission_sha256"]
    expected = {"local": 8, "rectangle_2": 16, "rectangle_3": 64}
    for family, count in expected.items():
        rows = primary["payload"][family]
        assert [r["input"] for r in rows] == list(range(count))
        assert all(r["passed"] for r in rows)
        assert sum(r["premise"] for r in rows) == 1
    proof_paths = ["proofs/informal/problem1_activity_staircase_bound.md",
                   "proofs/informal/problem1_activity_transport_inequality.md"]
    proof_snapshots = [snapshot(p) for p in proof_paths]
    reviews = [snapshot("proofs/informal/problem1_activity_staircase_review.md"),
               snapshot("proofs/informal/problem1_activity_transport_review.md")]
    # Recover the exact first reviewed source: the later addition only names
    # the existing unique-preimage dependency. Verify its recorded review hash.
    first = proof_snapshots[0]["text"].replace(
        "Unit triangularity of T gives a unique 2-adic preimage of every y,\n"
        "as proved in `problem1_effective_activity_levels.md`, Section1. One\n"
        "may therefore list E_K by enumerating the explicit finite set",
        "One may now list E_K by enumerating the explicit finite set")
    initial_hash = "7b7ba8f6cb378dd84b40b597327d8e3749cecfec4065f7b36603f272cae8ed01"
    if sha(first.encode()) != initial_hash and prior_archive is not None:
        first = prior_archive["original_reviewed_staircase"]["text"]
    assert sha(first.encode()) == initial_hash
    assert initial_hash in reviews[0]["text"]
    transport_reviewed = proof_snapshots[1]
    if transport_reviewed["sha256"] not in reviews[1]["text"] and prior_archive is not None:
        transport_reviewed = prior_archive.get("original_reviewed_transport", prior_archive["proof_snapshots"][1])
    assert sha(transport_reviewed["text"].encode()) == transport_reviewed["sha256"]
    assert transport_reviewed["sha256"] in reviews[1]["text"]
    reference = sha((ROOT / "src/python/rule30_research_reference.py").read_bytes())
    assert reference == "358bdc07904e77080eb78b67bdd8da25822d6b51f1a91b58b5313dfe461c1d01"
    self_source = snapshot(str(Path(__file__).relative_to(ROOT)))
    record = dict(
        experiment_id="20260906_activity_staircase_verification",
        timestamp_utc=datetime.now(timezone.utc).isoformat(),
        git_commit=subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        question="problem1", hypothesis="Two independent local-cone payloads agree and their archived sources/reviews reload exactly.",
        backend="python-archive-comparison-no-new-scientific-run",
        parameters=dict(record_paths=[BASE + x + ".json" for x in ("primary", "independent")],
                        expected_cases=expected, review_scope="staircase Sections1-5; transport Sections1-4"),
        hardware=dict(uname=list(platform.uname()), logical_cpus=os.cpu_count()),
        software=dict(python=sys.version, executable=sys.executable),
        runtime_seconds=time.perf_counter()-start,
        result_hashes=dict(payload_sha256=primary["result_hashes"]["payload_sha256"],
                          immutable_reference_sha256=reference,
                          source_sha256=self_source["sha256"],
                          **{x+"_record_sha256": sha((ROOT / (BASE+x+".json")).read_bytes())
                             for x in ("primary", "independent")}),
        result_summary=dict(complete_payloads_identical=True, compared_cases=88,
                            reviewed_proof_units=2, all_claims_remain_partial=True),
        status="finite-exhaustive",
        proof_scope="Archive equality and exact finite domains only; independent all-depth derivations retained separately.",
        interpretation="Lead checked local trajectories, zero-window induction, packing, event assignment, limit order and coordinate seams; accepts both scoped partial proofs.",
        limitations=["No actual-survivor growth theorem.", "No new CA computation or activity census.",
                     "Published dependencies imported in their previously reviewed scope."],
        proof_snapshots=proof_snapshots, review_snapshots=reviews,
        original_reviewed_staircase=dict(sha256=initial_hash, text=first),
        original_reviewed_transport=transport_reviewed,
        source_snapshots=sources, self_source=self_source)
    fd, tmp = tempfile.mkstemp(prefix=out.name+".", suffix=".tmp", dir=out.parent)
    with os.fdopen(fd, "w") as stream:
        json.dump(record, stream, sort_keys=True, indent=2)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(tmp, out)
    print(json.dumps(dict(path=str(out.relative_to(ROOT)), **record["result_summary"]), sort_keys=True))


if __name__ == "__main__":
    main()
