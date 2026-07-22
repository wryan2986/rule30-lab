from __future__ import annotations

import json
import subprocess
from pathlib import Path

from rule30lab.records import validate_record


REPOSITORY = Path(__file__).resolve().parents[2]
RESULTS = REPOSITORY / "results"


def test_all_machine_readable_results_follow_the_record_contract() -> None:
    paths = sorted(RESULTS.glob("**/*.json"))
    assert paths, "at least one structured result record is required"

    experiment_ids: set[str] = set()
    for path in paths:
        record = json.loads(path.read_text(encoding="utf-8"))
        validate_record(record)
        assert record["experiment_id"] not in experiment_ids, path
        experiment_ids.add(record["experiment_id"])


def test_every_record_names_an_existing_local_commit() -> None:
    for path in sorted(RESULTS.glob("**/*.json")):
        record = json.loads(path.read_text(encoding="utf-8"))
        subprocess.run(
            ("git", "cat-file", "-e", f"{record['git_commit']}^{{commit}}"),
            cwd=REPOSITORY,
            check=True,
            capture_output=True,
        )
