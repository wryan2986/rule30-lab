# Environment report

Initial inspection began 2026-07-21T23:19:11Z. Toolchain preparation was
verified at 2026-07-21T23:30:26Z. Commands were run in the existing default
`Ubuntu` WSL2 distribution.

## Windows host and WSL

- OS: Microsoft Windows 11 Home, 64-bit
- Windows kernel/version: `10.0.26200.8655` (build 26200)
- WSL package: `2.7.3.0`
- WSL kernel: `6.6.114.1-1`, reported by Linux as
  `6.6.114.1-microsoft-standard-WSL2`
- WSLg: `1.0.73`
- Default distribution: `Ubuntu`, WSL version 2, running
- Other registered distribution: `docker-desktop`, WSL version 2, stopped
- `/etc/wsl.conf`: systemd enabled; Windows PATH appending disabled
- Windows `.wslconfig`: absent
- Host system: Micro-Star International `MS-7C96`

## Linux distribution

- Ubuntu 26.04 LTS (Resolute Raccoon), x86-64
- glibc 2.43
- Root filesystem: ext4, 1007 GiB total, 926 GiB available at inspection
- Repository: `/home/wryan/rule30-lab` on the ext4 filesystem

## CPU and memory

- CPU: AMD Ryzen 5 3600 6-Core Processor
- Topology exposed to WSL: 6 physical cores, 12 logical CPUs, one NUMA node
- Cache: 192 KiB L1d, 192 KiB L1i, 3 MiB L2, 16 MiB L3
- Relevant ISA flags: SSE through SSE4.2, AVX, AVX2, FMA, BMI1, BMI2, POPCNT,
  AES, SHA-NI, ADX, and RDSEED
- Windows physical RAM: 34,282,160,128 bytes (31.92 GiB)
- RAM visible to WSL: approximately 15 GiB total, 14 GiB available at initial
  inspection
- WSL swap: 4.0 GiB, unused at initial inspection

Full initial CPU flags reported by `lscpu`:

```text
fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36
clflush mmx fxsr sse sse2 ht syscall nx mmxext fxsr_opt pdpe1gb rdtscp lm
constant_tsc rep_good nopl tsc_reliable nonstop_tsc cpuid extd_apicid
tsc_known_freq pni pclmulqdq ssse3 fma cx16 sse4_1 sse4_2 movbe popcnt aes
xsave avx f16c rdrand hypervisor lahf_lm cmp_legacy svm cr8_legacy abm sse4a
misalignsse 3dnowprefetch osvw topoext perfctr_core ssbd ibpb stibp vmmcall
fsgsbase bmi1 avx2 smep bmi2 rdseed adx smap clflushopt clwb sha_ni xsaveopt
xsavec xgetbv1 clzero xsaveerptr arat npt nrip_save tsc_scale vmcb_clean
flushbyasid decodeassists pausefilter pfthreshold v_vmsave_vmload umip rdpid
```

## NVIDIA GPU and CUDA

- GPU: NVIDIA GeForce RTX 2060 SUPER
- GPU UUID: `GPU-361d77d2-f8ae-91e7-e7bd-d59dea9879f9`
- Compute capability: 7.5
- Detected framebuffer memory: 8192 MiB
- Windows NVIDIA driver: 591.86
- Maximum CUDA version advertised by the driver: 13.1
- Driver stub visible in WSL: `/usr/lib/wsl/lib/libcuda.so.1`
- Initial temperature: 39 C
- Default/current power limit: 175 W; no project setting changed it
- NVIDIA-reported thermal values: target 83 C, maximum operating 89 C,
  slowdown 93 C, shutdown 96 C
- Initial toolkit state: `nvcc` absent
- First attempted toolkit: Ubuntu CUDA 13.1.115; compiler-ID failed against
  glibc 2.43 before project code compilation
- Selected prepared toolkit: nvcc 13.3.73, CUDA runtime 13.3.29, Compute
  Sanitizer 13.3.75; `/usr/local/cuda` points to `/usr/local/cuda-13.3`
- Compatibility mode: explicit `sm_75` SASS under NVIDIA's CUDA 13.x minor
  compatibility rule for drivers `>= 580`

Initial standard `nvidia-smi` output:

```text
Tue Jul 21 19:19:11 2026
+-----------------------------------------------------------------------------------------+
| NVIDIA-SMI 590.57                 Driver Version: 591.86         CUDA Version: 13.1     |
+-----------------------------------------+------------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id          Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |           Memory-Usage | GPU-Util  Compute M. |
|=========================================+========================+======================|
|   0  NVIDIA GeForce RTX 2060 ...    On  |   00000000:23:00.0  On |                  N/A |
|  0%   39C    P8             14W /  175W |    1758MiB /   8192MiB |      4%      Default |
+-----------------------------------------+------------------------+----------------------+
```

The full model name and memory values above come from the corresponding CSV
query because the standard table truncates the model name.

## Development tools

| Tool | Initial inspection | Prepared state |
|---|---:|---:|
| Git | 2.53.0 | unchanged |
| Python | 3.14.4 | project `.venv` created |
| pip | 25.1.1 | project-local |
| CMake/CTest | 4.2.3 | unchanged |
| GCC/G++ | 15.2.0 | unchanged |
| Clang | absent | 21.1.8 |
| Ninja | 1.13.2 | unchanged |
| GNU Make | 4.4.1 | unchanged |
| Rust/Cargo | absent | project-local 1.97.1 |
| CUDA nvcc | absent | 13.3.73 selected; 13.1 retained but unusable with glibc 2.43 |
| Docker CLI | absent | absent; not required |
| Lean/Lake | absent | project-local Lean 4.30.0 / Lake 5.0.0 |

## Interpretation

The GPU is available to unsandboxed WSL processes. The initial sandboxed
`nvidia-smi` probe returned an operating-system access error; rerunning the
same read-only command with GPU-device access succeeded. This was an execution
sandbox restriction, not a WSL/CUDA configuration failure.
