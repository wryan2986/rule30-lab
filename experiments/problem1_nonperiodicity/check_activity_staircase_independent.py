#!/usr/bin/env python3
"""Independent local-seam check for the activity staircase proof."""
import hashlib
import json
import os
import platform
import signal
import subprocess
import sys
import tempfile
import time

RULE30_LAB = "/home/ryan/rule30-lab"
ADMISSION = "proofs/informal/problem1_activity_staircase_verification_admission.md"
OUT_PATH = "results/problem1/20260906_activity_staircase_independent.json"
REF_PATH = "src/python/rule30_research_reference.py"
CPU_LIMIT_S = 120
WALL_LIMIT_S = 120
AS_LIMIT_B = 1 << 30


def cell(self_b, mid_b, upp_b):
    return upp_b ^ (mid_b | self_b)


def evolve(row):
    return [cell(row[k], row[k + 1], row[k + 2])
            for k in range(len(row) - 2)]


def bits(n, w):
    return [(n >> k) & 1 for k in range(w)]


class WallExpired(Exception):
    pass


def _on_alarm(signum, frame):
    raise WallExpired("wall alarm %ds expired" % WALL_LIMIT_S)


def atomic_write_json(path, record):
    tmp = tempfile.NamedTemporaryFile(
        mode="w", dir=os.path.dirname(path), delete=False)
    try:
        json.dump(record, tmp, indent=2, sort_keys=False)
        tmp.write("\n")
        tmp.flush()
        os.fsync(tmp.fileno())
    finally:
        tmp.close()
    os.replace(tmp.name, path)


def base_meta(extra):
    with open(os.path.join(RULE30_LAB, ADMISSION), "rb") as fh:
        admission_bytes = fh.read()
    with open(os.path.abspath(__file__), "rb") as fh:
        source_bytes = fh.read()
    with open(os.path.join(RULE30_LAB, REF_PATH), "rb") as fh:
        ref_bytes = fh.read()
    ref_clean = subprocess.call(
        ["git", "diff", "--quiet", "--", REF_PATH],
        cwd=RULE30_LAB) == 0
    meta = {
        "experiment_id": "20260906_activity_staircase_independent",
        "timestamp_utc": time.strftime(
            "%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "git_commit": subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=RULE30_LAB,
            text=True).strip(),
        "git_status": subprocess.check_output(
            ["git", "status", "--short"], cwd=RULE30_LAB, text=True),
        "question": "problem1",
        "backend": "cpython-stdlib-direct-bitarray",
        "hardware": {
            "platform": platform.platform(),
            "processor": platform.processor(),
            "cpu_count": os.cpu_count()},
        "software": {
            "python": sys.version.replace("\n", " "),
            "method": "direct bit arrays, stdlib only, no repo imports"},
        "result_hashes": {
            "source_sha256": hashlib.sha256(source_bytes).hexdigest(),
            "admission_sha256": hashlib.sha256(
                admission_bytes).hexdigest(),
            "immutable_reference_sha256": hashlib.sha256(
                ref_bytes).hexdigest(),
            "immutable_reference_git_clean": ref_clean},
        "admission_snapshot": admission_bytes.decode(),
        "source_snapshot": source_bytes.decode(),
    }
    meta.update(extra)
    return meta


def main():
    start_wall = time.perf_counter()
    start_cpu = time.process_time()
    deadline_utc = time.strftime(
        "%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time() + WALL_LIMIT_S))
    enforced = {}
    try:
        import resource
        resource.setrlimit(resource.RLIMIT_AS,
                           (AS_LIMIT_B, AS_LIMIT_B))
        enforced["RLIMIT_AS_1GiB"] = True
        resource.setrlimit(resource.RLIMIT_CPU,
                           (CPU_LIMIT_S, CPU_LIMIT_S))
        enforced["RLIMIT_CPU_120"] = True
    except Exception as exc:
        enforced["resource_error"] = "%r" % (exc,)
    try:
        signal.signal(signal.SIGALRM, _on_alarm)
        signal.alarm(WALL_LIMIT_S)
        enforced["wall_alarm_120"] = True
    except Exception as exc:
        enforced["alarm_error"] = "%r" % (exc,)

    if not (enforced.get("RLIMIT_AS_1GiB")
            and enforced.get("RLIMIT_CPU_120")
            and enforced.get("wall_alarm_120")):
        record = base_meta({
            "run_number": 2,
            "status": "inconclusive",
            "proof_scope": "no cases run: enforcement setup failed",
            "enforcement": enforced,
            "deadline_utc": deadline_utc,
            "interpretation": ("STOPPED inconclusive before any case: "
                               "a required cap not enforced; no cap "
                               "is claimed."),
            "limitations": ["enforcement setup failed; nothing executed"],
        })
        atomic_write_json(os.path.join(RULE30_LAB, OUT_PATH), record)
        print("INCONCLUSIVE: enforcement setup failed: %r" % (enforced,))
        return 2

    prior = None
    prior_abs = os.path.join(RULE30_LAB, OUT_PATH)
    if os.path.exists(prior_abs):
        with open(prior_abs, "r") as fh:
            prior = json.load(fh)

    try:
        local = []
        for n in range(8):
            init = bits(n, 3)
            out = cell(init[0], init[1], init[2])
            premise = (out == 0 and init[2] == 0)
            conclusion = (init[0] == 0 and init[1] == 0)
            local.append({"input": n, "initial": init, "output": out,
                          "premise": premise, "conclusion": conclusion,
                          "passed": ((not premise) or conclusion)})

        rectangle_2 = []
        for n in range(16):
            r0 = bits(n, 4)
            r1 = evolve(r0)
            assert len(r1) == 2
            premise = (r0[0] == 0 and r0[1] == 0
                       and r1[0] == 0 and r1[1] == 0)
            conclusion = (r0[2] == 0 and r0[3] == 0)
            rectangle_2.append({"input": n, "rows": [r0, r1],
                                "premise": premise,
                                "conclusion": conclusion,
                                "passed": ((not premise) or conclusion)})

        rectangle_3 = []
        for n in range(64):
            r0 = bits(n, 6)
            r1 = evolve(r0)
            r2 = evolve(r1)
            assert len(r1) == 4 and len(r2) == 2
            premise = (r0[0] == 0 and r0[1] == 0
                       and r1[0] == 0 and r1[1] == 0
                       and r2[0] == 0 and r2[1] == 0)
            conclusion = (r0[2] == 0 and r0[3] == 0
                          and r1[2] == 0 and r1[3] == 0)
            rectangle_3.append({"input": n, "rows": [r0, r1, r2],
                                "premise": premise,
                                "conclusion": conclusion,
                                "passed": ((not premise) or conclusion)})
    except WallExpired as exc:
        record = base_meta({
            "run_number": 2,
            "status": "inconclusive",
            "proof_scope": "aborted: wall deadline expired mid-run",
            "enforcement": enforced,
            "deadline_utc": deadline_utc,
            "interpretation": "STOPPED inconclusive: %s." % (exc,),
            "limitations": ["wall deadline expired before completion"],
        })
        atomic_write_json(os.path.join(RULE30_LAB, OUT_PATH), record)
        print("INCONCLUSIVE: %s" % (exc,))
        return 2
    finally:
        try:
            signal.alarm(0)
        except Exception:
            pass

    wall_used = time.perf_counter() - start_wall
    cpu_used = time.process_time() - start_cpu
    if wall_used > WALL_LIMIT_S:
        record = base_meta({
            "run_number": 2,
            "status": "inconclusive",
            "proof_scope": "overrun: wall used exceeds deadline",
            "enforcement": enforced,
            "deadline_utc": deadline_utc,
            "runtime_seconds": {"wall": wall_used, "cpu": cpu_used},
            "interpretation": "STOPPED inconclusive: wall overrun.",
            "limitations": ["wall deadline exceeded"],
        })
        atomic_write_json(os.path.join(RULE30_LAB, OUT_PATH), record)
        print("INCONCLUSIVE: wall overrun")
        return 2

    payload = {"local": local, "rectangle_2": rectangle_2,
               "rectangle_3": rectangle_3}

    def counts(rows):
        return {"cases": len(rows),
                "passed": sum(1 for r in rows if r["passed"]),
                "premise_true": sum(1 for r in rows if r["premise"]),
                "conclusion_true": sum(1 for r in rows if r["conclusion"])}

    summary = {"local": counts(local),
               "rectangle_2": counts(rectangle_2),
               "rectangle_3": counts(rectangle_3)}
    ok = all(v["passed"] == v["cases"] for v in summary.values())
    payload_canonical = json.dumps(
        payload, sort_keys=True, separators=(",", ":")).encode()
    record = base_meta({
        "run_number": 2,
        "correction_note": ("run 1 enforced only RLIMIT_AS and omitted "
                            "the immutable reference hash; run 2 enforces "
                            "RLIMIT_AS + RLIMIT_CPU(120) + wall alarm "
                            "(120s) with explicit deadline, records the "
                            "immutable reference hash, and archives the "
                            "full run-1 record below. Same 88 cases."),
        "superseded_prior_record": prior,
        "hypothesis": ("A-cell zero adjacent pair over L times forces "
                       "the next higher adjacent pair zero over the "
                       "first L-1 times (L=2,3); staggered zeros "
                       "force the lower pair zero."),
        "parameters": {
            "local_cases": 8, "rectangle_2_cases": 16,
            "rectangle_3_cases": 64,
            "cone_widths": {"local": [3, 1], "rectangle_2": [4, 2],
                            "rectangle_3": [6, 4, 2]},
            "cell_rule": "out=upper XOR (middle OR self)",
            "work_cpu": "1",
            "limits": "120s CPU (RLIMIT_CPU) + 120s wall (alarm), "
                      "1GiB AS (RLIMIT_AS)"},
        "enforcement": enforced,
        "deadline_utc": deadline_utc,
        "runtime_seconds": {"wall": wall_used, "cpu": cpu_used},
        "result_hashes_extra": {},
        "result_summary": summary,
        "payload": payload,
        "interpretation": (("ALL PASS: 8/8 local, 16/16 L=2, 64/64 L=3. "
                            if ok else
                            "FAILURE PRESENT: see per-case rows. ") +
                           "Finite local seams agree; all-width induction, "
                           "packing and harmonic limit need proof, "
                           "not extrapolation."),
        "status": "finite-exhaustive" if ok else "refuted",
        "proof_scope": ("exact admitted cones only: 8 three-bit "
                        "neighborhoods, 16 four-bit L=2 cones, "
                        "64 six-bit L=3 cones"),
        "limitations": [
            "covers finite local seams only",
            "no whole-row orbit replayed",
            "no survivor, enumeration, sweep, or first-witness claim",
            "R(27)/R(111) cited, not re-executed"],
    })
    record["result_hashes"]["payload_sha256"] = hashlib.sha256(
        payload_canonical).hexdigest()
    if prior is not None:
        record["result_hashes"]["superseded_prior_payload_sha256"] = (
            prior.get("result_hashes", {}).get("payload_sha256"))
    atomic_write_json(os.path.join(RULE30_LAB, OUT_PATH), record)
    print("cases=8/16/64 passed=%d/%d/%d status=%s"
          % (summary["local"]["passed"],
             summary["rectangle_2"]["passed"],
             summary["rectangle_3"]["passed"], record["status"]))
    print("payload_sha256=%s"
          % record["result_hashes"]["payload_sha256"])
    print("enforcement=%r" % (enforced,))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
