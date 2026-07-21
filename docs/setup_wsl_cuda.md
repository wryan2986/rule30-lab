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

Python:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -e '.[dev,analysis]'
```

Rust and Lean downloads are stored below ignored `.toolchains/` directories.
The pinned versions are in `rust-toolchain.toml` and
`proofs/lean/lean-toolchain`.

## WSL administrative note

This distribution requires an interactive password for `sudo`. The initial
automated setup used the equivalent Windows command
`wsl.exe -d Ubuntu -u root -- apt-get ...` for the explicitly approved package
operations. No distro, driver, kernel, WSL setting, or hardware setting was
changed.
