# System change log

All timestamps are UTC. Project-local virtual environments/toolchains are
listed separately from operating-system packages.

## 2026-07-21T23:27Z — Ubuntu package metadata

Command, executed in the existing `Ubuntu` WSL distribution as root:

```bash
apt-get update
```

No repository was added or removed. Existing Ubuntu 26.04 and NodeSource
metadata was refreshed.

## 2026-07-21T23:28Z — minimal development packages

Command:

```bash
apt-get install -y --no-install-recommends \
  clang-21 rustup elan cuda-nvcc-13-1 cuda-cudart-dev-13-1 \
  cuda-sanitizer-13-1
```

Result: 23 new packages, 138 MB downloaded, 608 MB installed. No package was
upgraded or removed. Notable installed versions:

- Clang `21.1.8-6ubuntu1`
- rustup `1.27.1-8`
- elan `4.1.2-3.1ubuntu1`
- nvcc `13.1.115`
- CUDA runtime/development files `13.1.80`
- Compute Sanitizer `13.1.118`

No NVIDIA Linux display driver package was installed. `cuda-driver-dev-13-1`
is a toolkit development-stub dependency, not a display/kernel driver.

## Project-local installations

- `.venv`: Python 3.14 virtual environment.
- `.toolchains/rustup`: Rust 1.97.1 minimal toolchain with Clippy and rustfmt.
- `.toolchains/elan`: Lean 4.30.0 and Lake 5.0.0.

These paths are ignored by Git and can be recreated from pinned project files.
No global shell profile was modified.

## 2026-07-21T23:39Z — CUDA compiler compatibility diagnosis

The Ubuntu 26.04 CUDA 13.1 package installed above failed a minimal CMake
compiler-identification build. Its `math_functions.h` declarations for
`rsqrt`/`rsqrtf` have exception specifications incompatible with glibc 2.43.
No project source was compiled and no unsupported-compiler override or header
patch was applied.

NVIDIA's current installation guide validates Ubuntu 26.04 with CUDA 13.3, and
its compatibility guide permits CUDA 13.x applications on drivers `>= 580`
when explicit SASS is generated for the target architecture. The installed
591.86 driver meets that requirement.

## 2026-07-21T23:42Z — official NVIDIA WSL package repository

Downloaded NVIDIA's `cuda-keyring_1.1-1_all.deb` from the official WSL-Ubuntu
repository. SHA-256:
`eea6cc5f0eaeb99082d054b8c05ae206a378e31e88048df0310d59f651dceed2`.
Installed it with `dpkg -i` and refreshed package metadata. This enrolled key
`3BF863CC` and added only NVIDIA's WSL CUDA repository.

## 2026-07-21T23:44Z — CUDA 13.3 development components

Command:

```bash
apt-get install -y --no-install-recommends \
  cuda-nvcc-13-3 cuda-cudart-dev-13-3 cuda-sanitizer-13-3
```

Result: 11 new packages, two shared CUDA config packages upgraded, 106 MB
downloaded, and 436 MB installed. No Linux display or kernel driver was
installed. `/usr/local/cuda` now selects `/usr/local/cuda-13.3`. A clean CMake
compiler-ID build succeeded with nvcc 13.3.73, GCC 15.2, and architecture 75.
The earlier 13.1 packages remain side-by-side temporarily for an auditable
setup history; they are not selected by the CUDA alternative.
