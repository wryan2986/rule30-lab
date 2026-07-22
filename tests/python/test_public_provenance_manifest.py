from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MANIFEST = (
    ROOT
    / "docs"
    / "public_provenance"
    / "20260722_controlled_run_manifest.json"
)
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


def test_public_provenance_manifest_is_path_neutral_and_complete() -> None:
    payload = json.loads(MANIFEST.read_text(encoding="utf-8"))

    assert payload["schema_version"] == 1
    records = payload["records"]
    assert len(records) == 7
    assert len({record["id"] for record in records}) == len(records)

    serialized = MANIFEST.read_text(encoding="utf-8")
    assert "/home/" not in serialized
    assert "C:\\Users\\" not in serialized

    for record in records:
        assert record["status"] == "finite-exhaustive"
        assert SHA256_RE.fullmatch(record["scientific_certificate_sha256"])
        assert record["original_local_record"].startswith("results/runs/")
        assert record["reproduction_command"]

        for key in ("controlled_stdout_sha256", "arithmetic_certificate_sha256"):
            if key in record:
                assert SHA256_RE.fullmatch(record[key])

        for path_group in (
            "public_result_paths",
            "source_paths",
            "documentation_paths",
        ):
            for relative_path in record[path_group]:
                assert (ROOT / relative_path).is_file(), relative_path
