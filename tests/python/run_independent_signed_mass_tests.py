#!/usr/bin/env python3
"""Minimal local test runner (no pytest available in this worktree)."""
import sys
import traceback
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_three_return_signed_mass_independent as t

names = sorted(n for n in dir(t) if n.startswith("test_"))
failed = 0
for n in names:
    try:
        getattr(t, n)()
        print(f"PASS {n}")
    except Exception:
        failed += 1
        print(f"FAIL {n}")
        traceback.print_exc()
print(f"{len(names) - failed}/{len(names)} passed")
sys.exit(1 if failed else 0)
