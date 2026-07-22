# Publication Validation Report

**Date:** 2026-07-22
**Repository:** /home/wryan/rule30-lab

## Test Results

| Component | Command | Result |
|-----------|---------|--------|
| Python (311 tests) | `.venv/bin/python -m pytest tests/python/ -v --timeout=60` | **PASSED** |
| Rust (11 tests) | `cargo test --offline --locked --release --workspace` | **PASSED** |
| C++ unit + contract (2 tests) | `ctest --test-dir /tmp/rule30-lab-release` | **PASSED** |
| Lean 4 (lake build) | `lake build` in `proofs/lean/` | **PASSED** |
| CUDA | Skipped (CUDA disabled for CPU-only validation) | **SKIPPED** |

## Summary

- **Passed:** Python, Rust, C++, Lean 4
- **Failed:** None
- **Skipped:** CUDA (requires NVIDIA GPU; tested separately with `RULE30_ENABLE_CUDA=ON`)

All CPU-compatible components pass their test suites. The repository is ready for public release.
