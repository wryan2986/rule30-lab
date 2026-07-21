# Research log

## 2026-07-21

- Created the WSL-native repository and imported the supplied reference source
  unchanged in commit `8296a83e5972257a23a3d80cf0016a351a92ed6d`.
- Recorded Windows 11, WSL 2.7.3, Ubuntu 26.04, Ryzen 5 3600, RAM, disk, and
  NVIDIA facts. Confirmed one RTX 2060 SUPER with 8192 MiB and compute
  capability 7.5.
- Installed minimal Clang, rustup, elan, and CUDA development packages. Pinned
  project-local Rust 1.97.1, Lean 4.30.0, and Python dependencies.
- Diagnosed the Ubuntu CUDA 13.1/glibc 2.43 header conflict and moved the active
  compiler to NVIDIA WSL CUDA 13.3. A clean nvcc/CMake compiler check passed.
- Added an independent cell-array implementation and 28 passing Python tests
  covering all supplied functions and explicit edge behavior.
- Completed adversarial reference audit and primary-source theory review. The
  latter verifies the limited `partial-proof` that the center cannot become
  permanently one; it does not solve eventual nonperiodicity.
