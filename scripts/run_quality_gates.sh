#!/usr/bin/env bash
set -euo pipefail

repository_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
build_root="${RULE30_BUILD_ROOT:-/tmp/rule30-lab-quality-gates}"
build_jobs="${RULE30_BUILD_JOBS:-2}"

if [[ ! -x "${repository_root}/.venv/bin/python" ]]; then
  echo "Missing project virtual environment: ${repository_root}/.venv" >&2
  exit 2
fi

cd "${repository_root}"

PYTHONDONTWRITEBYTECODE=1 \
  .venv/bin/python -m pytest -p no:cacheprovider

cmake --fresh -S . -B "${build_root}/release" -G Ninja \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_CUDA_COMPILER=/usr/local/cuda/bin/nvcc \
  -DRULE30_ENABLE_CUDA=ON
nice -n 10 cmake --build "${build_root}/release" --parallel "${build_jobs}"
nice -n 10 ctest --test-dir "${build_root}/release" --output-on-failure

# CTest's SKIP_RETURN_CODE=77 is useful on machines without CUDA, but this
# repository's canonical workstation has a known RTX 2060 SUPER.  Run every
# GPU contract directly as well so a missing/inaccessible device is a hard
# failure here rather than a successful skip.
cuda_build="${build_root}/release/src/cuda"
nice -n 10 "${cuda_build}/rule30_cuda_probe"
nice -n 10 "${cuda_build}/tests/rule30_cuda_tests"
nice -n 10 "${cuda_build}/tests/rule30_cuda_evolution_tests"
nice -n 10 "${cuda_build}/tests/rule30_cuda_sideways_tests"
nice -n 10 "${cuda_build}/tests/rule30_cuda_generate_contract_tests" \
  gpu \
  "${cuda_build}/rule30_cuda_generate" \
  "${repository_root}/tests/reference_vectors/center_c00000000_c00009999.u8"
nice -n 10 \
  "${cuda_build}/tests/rule30_cuda_extended_period_search_tests" gpu

cmake --fresh -S . -B "${build_root}/sanitized" -G Ninja \
  -DCMAKE_BUILD_TYPE=Debug \
  -DRULE30_ENABLE_AVX2=ON \
  -DRULE30_ENABLE_CUDA=OFF \
  -DRULE30_ENABLE_SANITIZERS=ON
nice -n 10 cmake --build "${build_root}/sanitized" --parallel "${build_jobs}"
ASAN_OPTIONS=detect_leaks=0 UBSAN_OPTIONS=print_stacktrace=1 \
  ctest --test-dir "${build_root}/sanitized" --output-on-failure

env \
  RUSTUP_HOME="${repository_root}/.toolchains/rustup" \
  CARGO_HOME="${repository_root}/.toolchains/cargo" \
  CARGO_TARGET_DIR="${build_root}/rust" \
  cargo fmt --all -- --check
env \
  RUSTUP_HOME="${repository_root}/.toolchains/rustup" \
  CARGO_HOME="${repository_root}/.toolchains/cargo" \
  CARGO_TARGET_DIR="${build_root}/rust" \
  nice -n 10 cargo clippy --offline --locked -p rule30-core --all-targets -- -D warnings
env \
  RUSTUP_HOME="${repository_root}/.toolchains/rustup" \
  CARGO_HOME="${repository_root}/.toolchains/cargo" \
  CARGO_TARGET_DIR="${build_root}/rust" \
  nice -n 10 cargo test --offline --locked -p rule30-core

(
  cd proofs/lean
  env \
    ELAN_HOME="${repository_root}/.toolchains/elan" \
    PATH="${repository_root}/.toolchains/elan/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin" \
    lake build
)

echo "All available Rule 30 quality gates passed."
