from __future__ import annotations

import json

import pytest

from rule30lab.cli import main


def test_generate_text(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(("generate", "--count", "5")) == 0
    assert capsys.readouterr().out == "11011\n"


def test_generate_json(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(("generate", "--count", "5", "--json")) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["bits"] == "11011"
    assert payload["count"] == 5
    assert len(payload["sha256_u8"]) == 64
