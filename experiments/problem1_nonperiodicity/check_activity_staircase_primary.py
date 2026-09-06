"""Only the three local cones in the pre-execution staircase admission."""
import hashlib
import json
import os
import platform
import resource
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ADMISSION = ROOT / "proofs/informal/problem1_activity_staircase_verification_admission.md"
OUT = ROOT / "results/problem1/20260906_activity_staircase_primary.json"


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def packed_a(x):
    return (x ^ ((x << 1) | (x << 2))) >> 2


def bits(x, width):
    return [(x >> i) & 1 for i in range(width)]


def main():
    started = time.perf_counter()
    resource.setrlimit(resource.RLIMIT_CPU, (120, 120))
    resource.setrlimit(resource.RLIMIT_AS, (1024**3, 1024**3))
    cases = {"local": [], "rectangle_2": [], "rectangle_3": []}
    failure = None
    for x in range(8):
        initial = bits(x, 3)
        output = packed_a(x) & 1
        premise = output == 0 and initial[2] == 0
        conclusion = initial[0] == initial[1] == 0
        passed = not premise or conclusion
        cases["local"].append(dict(input=x, initial=initial, output=output,
                                   premise=premise, conclusion=conclusion, passed=passed))
        if not passed:
            failure = ["local", x]
            break
    if failure is None:
        for length in (2, 3):
            width = 2 * length
            for x in range(1 << width):
                row, rows = x, []
                for t in range(length):
                    rows.append(bits(row, width - 2 * t))
                    row = packed_a(row)
                premise = all(r[0] == r[1] == 0 for r in rows)
                conclusion = all(r[2] == r[3] == 0 for r in rows[:-1])
                passed = not premise or conclusion
                cases[f"rectangle_{length}"].append(dict(input=x, rows=rows,
                    premise=premise, conclusion=conclusion, passed=passed))
                if not passed or time.perf_counter() - started > 120:
                    failure = [f"rectangle_{length}", x]
                    break
            if failure is not None:
                break
    raw_payload = json.dumps(cases, sort_keys=True, separators=(",", ":")).encode()
    source = Path(__file__).read_bytes()
    admission = ADMISSION.read_bytes()
    cpu_model = next((line.split(":", 1)[1].strip() for line in
                     Path("/proc/cpuinfo").read_text().splitlines()
                     if line.startswith("model name")), "unavailable")
    record = dict(
        experiment_id="20260906_activity_staircase_primary",
        timestamp_utc=datetime.now(timezone.utc).isoformat(),
        git_commit=subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        question="problem1",
        hypothesis="The staircase staggered-zero and rectangle implications hold on the exact admitted local cones.",
        backend="python-packed-A-from-T",
        parameters=dict(neighborhoods=8, rectangle_2_inputs=16, rectangle_3_inputs=64,
                        cone_widths=[[3, 1], [4, 2], [6, 4, 2]],
                        cpu_limit_seconds=120, wall_limit_seconds=120, memory_limit_bytes=1024**3),
        hardware=dict(uname=list(platform.uname()), cpu_model=cpu_model,
                      logical_cpus=os.cpu_count(), peak_rss_kb=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss),
        software=dict(python=sys.version, executable=sys.executable),
        runtime_seconds=time.perf_counter()-started,
        result_hashes=dict(payload_sha256=digest(raw_payload), source_sha256=digest(source),
                          admission_sha256=digest(admission),
                          immutable_reference_sha256=digest((ROOT / "src/python/rule30_research_reference.py").read_bytes())),
        result_summary={name: dict(cases=len(rows), premises=sum(r["premise"] for r in rows),
                                   passes=sum(r["passed"] for r in rows)) for name, rows in cases.items()},
        status="finite-exhaustive" if failure is None else "refuted",
        proof_scope="All 8 local neighborhoods,16 L=2 cones,64 L=3 cones; no all-depth inference from counts.",
        interpretation="Local seam verification only; the staircase induction and support bound require the separate reviewed proof.",
        limitations=["No actual survivor evaluated.", "No activity-level or orbit census.",
                     "No optimized backend or reference implementation acceptance claim."],
        failure=failure, payload=cases,
        source_snapshot=dict(path=str(Path(__file__).relative_to(ROOT)), sha256=digest(source), text=source.decode()),
        admission_snapshot=dict(path=str(ADMISSION.relative_to(ROOT)), sha256=digest(admission), text=admission.decode()))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fd, temp = tempfile.mkstemp(prefix=OUT.name+".", suffix=".tmp", dir=OUT.parent)
    with os.fdopen(fd, "w") as stream:
        json.dump(record, stream, sort_keys=True, indent=2)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temp, OUT)
    print(json.dumps(dict(path=str(OUT.relative_to(ROOT)), summary=record["result_summary"],
                          status=record["status"], payload_sha256=digest(raw_payload)), sort_keys=True))
    if failure is not None:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
