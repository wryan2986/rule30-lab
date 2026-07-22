# WSL2 and CUDA setup

The canonical repository is `/home/wryan/rule30-lab` in the Ubuntu WSL2 ext4
filesystem. The current machine facts are in
`results/environment/environment_report.md`.

## GPU model

The Windows NVIDIA driver is the only display driver. WSL exposes it through
`/usr/lib/wsl/lib/libcuda.so.1`. Do not install a Linux NVIDIA display driver.

The project uses narrowly scoped CUDA 13.3 development packages from NVIDIA's
official WSL-Ubuntu repository:

```bash
apt-get install --no-install-recommends \
  cuda-nvcc-13-3 cuda-cudart-dev-13-3 cuda-sanitizer-13-3
```

These provide `nvcc`, runtime headers/libraries, and Compute Sanitizer. CUDA
13.3 is the first installed release validated for Ubuntu 26.04 and glibc 2.43.
The Ubuntu-packaged 13.1 compiler was tried first but failed its compiler-ID
test because its math declarations conflict with glibc 2.43; no project code
was involved in that failure. The
project does not install the `cuda`, `cuda-drivers`, or Linux display-driver
meta-packages. This follows NVIDIA's WSL guidance that the Windows driver is
stubbed into WSL and must not be overwritten:
<https://docs.nvidia.com/cuda/wsl-user-guide/>.

Verify without changing GPU state:

```bash
nvidia-smi
/usr/local/cuda/bin/nvcc --version
```

The detected RTX 2060 SUPER has compute capability 7.5, so release CUDA targets
must compile SASS for `sm_75`. No PTX-only deployment is accepted. The R590
driver is older than CUDA 13.3's paired driver but is within NVIDIA's documented
CUDA 13.x minor-version compatibility range (`>= 580`); compiling explicit
`sm_75` SASS is required by that compatibility mode.

## Project-local toolchains

Run every command below from `/home/wryan/rule30-lab`. The operating-system
build prerequisites used by this checkout are Git, Python 3 with `venv`, GCC
and G++, CMake, Ninja, GNU Make, Clang 21, `rustup`, and `elan`. Their detected
versions are recorded in `results/environment/environment_report.md`.

Create the pinned Python environment from the lock file:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -e . --no-deps
.venv/bin/python -m pip install -r requirements-dev.lock
```

Bootstrap the pinned Rust toolchain without changing a global shell profile:

```bash
export RUSTUP_HOME="$PWD/.toolchains/rustup"
export CARGO_HOME="$PWD/.toolchains/cargo"
rustup toolchain install 1.97.1 --profile minimal \
  --component clippy --component rustfmt
cargo --version
```

Bootstrap Lean 4 and Lake in a project-local `ELAN_HOME`:

```bash
export ELAN_HOME="$PWD/.toolchains/elan"
export PATH="$ELAN_HOME/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
elan toolchain install leanprover/lean4:v4.30.0
cd proofs/lean
lake build
cd ../..
```

The pinned versions are also declared by `rust-toolchain.toml` and
`proofs/lean/lean-toolchain`. `.venv/` and `.toolchains/` are ignored and can
be recreated from the tracked files.

## Build commands

C++ and CUDA release build targeting the detected Turing GPU:

```bash
cmake --fresh -S . -B /tmp/rule30-lab-release -G Ninja \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_CUDA_COMPILER=/usr/local/cuda/bin/nvcc \
  -DCMAKE_CUDA_ARCHITECTURES=75 \
  -DRULE30_ENABLE_CUDA=ON
nice -n 10 cmake --build /tmp/rule30-lab-release --parallel 2
ctest --test-dir /tmp/rule30-lab-release --output-on-failure
cuda_build=/tmp/rule30-lab-release/src/cuda
nice -n 10 "$cuda_build/rule30_cuda_probe"
nice -n 10 "$cuda_build/tests/rule30_cuda_tests"
nice -n 10 "$cuda_build/tests/rule30_cuda_evolution_tests"
nice -n 10 "$cuda_build/tests/rule30_cuda_sideways_tests"
nice -n 10 "$cuda_build/tests/rule30_cuda_generate_contract_tests" \
  gpu "$cuda_build/rule30_cuda_generate" \
  "$PWD/tests/reference_vectors/center_c00000000_c00009999.u8"
```

CTest deliberately skips CUDA cases with return code 77 when no device is
available. Therefore CTest success alone is not proof that the GPU ran. The
direct invocations above, and the consolidated quality-gate script below,
treat device unavailability as a failure on this canonical workstation.

Rust release binaries:

```bash
env RUSTUP_HOME="$PWD/.toolchains/rustup" \
  CARGO_HOME="$PWD/.toolchains/cargo" \
  CARGO_TARGET_DIR=/tmp/rule30-lab-rust \
  cargo build --offline --locked --release -p rule30-core --bins
```

The consolidated command `nice -n 10 scripts/run_quality_gates.sh` rebuilds
and tests Python, release C++/CUDA, sanitizer-enabled C++, Rust, and Lean. On
this canonical workstation it deliberately fails if CUDA tests are skipped.

## Official references

- Microsoft: [Install WSL](https://learn.microsoft.com/en-us/windows/wsl/install)
  and [basic WSL commands](https://learn.microsoft.com/en-us/windows/wsl/basic-commands).
- NVIDIA: [CUDA on WSL](https://docs.nvidia.com/cuda/wsl-user-guide/index.html),
  the [CUDA 13.3 Linux installation guide](https://docs.nvidia.com/cuda/cuda-installation-guide-linux/index.html),
  and [minor-version compatibility](https://docs.nvidia.com/deploy/cuda-compatibility/minor-version-compatibility.html).
- Python: [`venv`](https://docs.python.org/3/library/venv.html).
- CMake: [`cmake(1)`](https://cmake.org/cmake/help/latest/manual/cmake.1.html).
- Rust: [Install Rust](https://rust-lang.org/install.html) and the
  [Cargo installation guide](https://doc.rust-lang.org/stable/cargo/getting-started/installation.html).
- Lean: [official Lean installation manual](https://lean-lang.org/install/manual/).

## WSL administrative note

This distribution requires an interactive password for `sudo`. The initial
automated setup used the equivalent Windows command
`wsl.exe -d Ubuntu -u root -- apt-get ...` for the explicitly approved package
operations. No distro, driver, kernel, WSL setting, or hardware setting was
changed.
