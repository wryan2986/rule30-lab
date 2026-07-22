# Controlled local experiment runner

`rule30lab.controlled_runner` is the production envelope for long or
nontrivial repository experiments. It executes one audited experiment on this
WSL2 instance, applies conservative limits before scientific code starts,
streams bounded output, emits progress, and writes an atomic strict experiment
record.

The runner never accepts a child script path and never invokes a shell. Its
only scientific child entry points are:

| Runner name | Repository script | Question |
|---|---|---|
| `problem1-sideways` | `experiments/problem1_nonperiodicity/run_sideways_search.py` | Problem 1 |
| `problem2-finite-prefix` | `experiments/problem2_balance/run_finite_prefix.py` | Problem 2 |
| `problem2-scaling` | `experiments/problem2_balance/run_scaling_analysis.py` | Problem 2 |
| `problem2-conservation` | `experiments/problem2_balance/search_local_conservation.py` | Problem 2 |
| `problem3-exact-searches` | `experiments/problem3_complexity/run_exact_searches.py` | Problem 3 |

An allowlisted path must be repository-relative, remain inside the repository
after resolution, be a regular `.py` file, and contain no symlink component.
The child is launched as an explicit argument vector using the current virtual
environment's Python with isolated mode (`-I`), `stdin` attached to
`/dev/null`, and `shell=False`. The runner itself makes no network request.
The fixed experiment scripts perform local computation; arbitrary executable
or script selection is not available. Fixed read-only metadata probes are
limited to `git rev-parse HEAD` and, when explicitly enabled, `nvidia-smi`.
The runner also requires a clean tracked and untracked Git worktree before
launch, excluding its explicitly ignored transient run artifacts. Read-path
options must resolve inside the repository; abbreviated path-bearing options
are rejected rather than delegated to argparse abbreviation.
Generic child side-output options such as `--export-graphs-dir` are rejected
because those files would bypass the parent's streamed-output budget.
The child receives a small explicit environment without `LD_PRELOAD`; fixed
tool probes use absolute paths. This is an audited execution envelope, not a
kernel network namespace or hostile-code sandbox.

## Basic use

Put runner options before the experiment name and experiment-specific options
after `--`:

```bash
cd /home/wryan/rule30-lab
rule30 experiment controlled -- \
  --profile interactive \
  --run-directory results/runs \
  --experiment-id p2-conservation-widths-1-5 \
  problem2-conservation -- \
  --minimum-width 1 --maximum-width 5
```

For a finite-prefix run:

```bash
rule30 experiment controlled -- \
  --profile interactive \
  --experiment-id p2-trusted-10000 \
  problem2-finite-prefix -- \
  --input tests/reference_vectors/center_c00000000_c00009999.u8
```

The parent prints compact progress JSON lines to its stderr. Child stderr is
not mixed into those lines; it is captured in its own bounded artifact. A
terminal summary is printed to parent stdout.

## Profiles and overrides

Profiles come directly from `rule30lab.resources.ResourceLimits.conservative`.
They are ceilings, not targets.

| Limit | `interactive` | `idle` |
|---|---:|---:|
| Wall time | 1 hour | 6 hours |
| Child Linux address space | 8 GiB | 13 GiB |
| GPU-memory policy budget | 4 GiB | 6 GiB |
| Overall planned-output budget | 1 GiB | 4 GiB |
| Free-disk reserve | 10 GiB | 10 GiB |
| Progress interval | 10 seconds | 15 seconds |
| GPU pause threshold | 78 C | 82 C |
| GPU abort threshold | 84 C | 86 C |
| Child worker environment | logical CPUs minus two | all logical CPUs |
| Default child stdout cap | 16 MiB | 64 MiB |
| Default child stderr cap | 4 MiB | 16 MiB |

The interactive profile is the default and leaves CPU, RAM, GPU-memory, and
thermal headroom while the machine may be in use. The idle profile permits
more local work but remains bounded and retains thermal and disk safeguards.
Neither profile changes clocks, voltage, power limits, fan policy, driver
settings, or any Windows/NVIDIA safety control.

Useful explicit overrides include:

```text
--wall-seconds SECONDS
--ram-mib MIB
--gpu-memory-mib MIB
--output-budget-mib MIB
--disk-reserve-mib MIB
--progress-seconds SECONDS
--cpu-workers COUNT
--stdout-cap-mib MIB
--stderr-cap-mib MIB
--gpu-pause-temperature-c C
--gpu-abort-temperature-c C
```

The stdout and stderr caps each have an additional hard runner ceiling of
64 MiB. The planned disk/output total is:

```text
stdout cap + stderr cap + 2 MiB record reserve + 512 KiB checkpoint reserve
```

That total must fit the selected profile's output budget. Before creating a
run, the shared disk preflight verifies that the destination filesystem can
hold the planned total while preserving the configured free-space reserve.
The run directory must resolve below `results/runs`; arbitrary output
directories and symlink escapes are refused.

## Enforced controls

### Child memory and CPU headroom

Immediately before `exec`, the child applies Linux `RLIMIT_AS` through
`rule30lab.resources.apply_address_space_limit`. Descendants inherit this
address-space ceiling. Address space is not the same as resident RAM: mapped
libraries, allocators, and device mappings count, so a process may receive
`MemoryError` before its RSS reaches the configured byte value.
The limit applies separately to each process, not to aggregate process-tree
RSS. The fixed allowlist and wall/output limits reduce this risk, but the
runner is not a cgroup-based aggregate memory sandbox.

The runner also sets `OMP_NUM_THREADS`, `OPENBLAS_NUM_THREADS`,
`MKL_NUM_THREADS`, `NUMEXPR_NUM_THREADS`, and `RAYON_NUM_THREADS` to the
profile's worker count. This bounds cooperative libraries; it is not a kernel
CPU quota for code that deliberately ignores those variables.

### Wall time and streamed output

Wall time is measured by the parent with a monotonic clock and includes time
spent thermally paused. Stdout and stderr are nonblocking pipes drained with a
selector. Each chunk is written directly to a same-directory temporary file
and incorporated into an incremental SHA-256. The runner never performs an
unbounded `capture_output`.

If a stream produces one byte beyond its cap, only bytes through the cap are
persisted, the artifact is marked `truncated_by_cap`, and the child process
group is terminated. Records separately state whether EOF was observed; a
finalized truncated artifact is never called a complete child stream.

### Interruption and termination

The shared `GracefulInterruption` handler converts `SIGINT` and `SIGTERM` into
a polled request. The runner then:

1. sends `SIGTERM` to the isolated child process group and atomically
   checkpoints current argv, state, byte counts, and incremental output
   hashes;
2. continues draining bounded output;
3. sends `SIGKILL` only if the configurable grace interval expires;
4. atomically publishes the captured artifacts, terminal checkpoint, and an
   `inconclusive` strict record.

The same graceful termination sequence is used for wall, output, and telemetry
limits. An unexpected internal runner exception uses a fail-safe process-group
kill and writes terminal artifacts when possible. Exit code 130/143 identifies
intercepted SIGINT or SIGTERM, 124 identifies wall timeout, and 125 identifies
an output or GPU policy abort. A successful child and valid JSON return zero.
The wall deadline remains active until both child pipes reach EOF, even if the
direct child exits first; surviving pipe-inheriting descendants are terminated
through the original process group. After `SIGKILL`, a final 250-millisecond
pipe-drain interval prevents an escaped or detached descriptor holder from
blocking the parent indefinitely; EOF is not claimed when that fallback closes
a pipe.

## Optional read-only NVIDIA telemetry

GPU telemetry is disabled unless `--gpu-telemetry` is supplied. Enabling it
runs the existing fixed `nvidia-smi` CSV query at `--telemetry-seconds`
intervals. The query reads temperature, utilization, memory use, total memory,
and power draw. It never passes a setter option.

Policy responses affect only the child process group:

- below all thresholds: continue;
- at the pause temperature: send `SIGSTOP`, keep checking, then send `SIGCONT`
  after cooling;
- at the abort temperature: terminate and checkpoint;
- above the GPU-memory policy budget: terminate and checkpoint, because a
  generic running child cannot safely change its chunk size;
- telemetry-command failure: fail closed, terminate, and checkpoint.

Telemetry is device-global. Memory or temperature can include unrelated local
applications and is not attributed exclusively to the experiment. Records
therefore preserve samples as operational evidence only. No telemetry reading
is a mathematical result.

## Artifacts and hashes

For experiment ID `example`, one run directory contains:

```text
example.stdout.data
example.stderr.log
example.checkpoint.state
example.record.json
```

Stdout and stderr are first written to same-directory temporary files, flushed
and `fsync`ed, then atomically replaced. The checkpoint uses
`atomic_write_checkpoint`; the final record uses the validating
`atomic_write_json` primitive. Existing artifacts are not replaced unless
`--overwrite` is explicit or the run is a validated restart of its own
checkpoint.

Raw stdout, stderr, checkpoints, and run records beneath `results/runs` are
Git-ignored so an incomplete attempt can be resumed immediately. A reviewed
strict record can be promoted deliberately with `git add -f`; ignored JSON is
still checked by the repository-wide result-schema tests while present.

Each file replacement is atomic and its temporary file is flushed and
`fsync`ed. The four files are not one transactional unit, and directory
`fsync` is not claimed; after abrupt power loss, inspect the terminal
checkpoint and hashes before trusting an artifact set.

The strict record includes:

- a full Git commit, clean-worktree checks before and after execution,
  runner-module SHA-256 before and after, and child-script SHA-256 before and
  after;
- logical child-argv SHA-256;
- exact captured stdout/stderr SHA-256 and byte counts;
- canonical parsed-child-JSON SHA-256 when output validation succeeds;
- local kernel, CPU, memory, Python, profile, and optional GPU telemetry;
- explicit `remote_compute_used: false` and
  `hardware_settings_changed: false` fields;
- finite scientific scope, status, interpretation, and limitations.

Hashes identify exact bytes. They do not upgrade empirical evidence into a
proof.

## Honest checkpoint and restart semantics

The five current child scripts emit a final JSON payload but do not expose a
generic durable mid-script continuation protocol. Every checkpoint therefore
states:

```json
{
  "child_continuation_supported": false,
  "resume": {
    "mid_script_continuation_supported": false,
    "mode": "restart-child-from-beginning"
  }
}
```

A checkpoint stores parent runner state, exact child argv, logical argv hash,
captured byte counts and hashes, attempt number, outcome, and artifact paths.
`--resume-from` validates the experiment name, experiment ID, argv hash,
full argv, schema version, positive attempt, incomplete state, and stdout/stderr
destinations. The checkpoint must be the exact checkpoint path derived from
the selected run directory and experiment ID. It then starts a new child at
its first instruction and increments the attempt number. It does not append
old output, skip completed child work, or claim that a finite-search loop
resumes where it stopped.

Use the same explicit ID when restarting:

```bash
rule30 experiment controlled -- \
  --experiment-id p2-conservation-widths-1-5 \
  --resume-from results/runs/p2-conservation-widths-1-5.checkpoint.state \
  problem2-conservation -- \
  --minimum-width 1 --maximum-width 5
```

Some scientific scripts expose manual partition parameters, such as starting
model IDs. Those can support researcher-designed separate runs, but they are
not automatic continuation and are not represented as such by this runner.

## Verification

The focused suite uses only tiny temporary Python children; it does not query
the GPU or run an expensive experiment:

```bash
cd /home/wryan/rule30-lab
.venv/bin/python -m pytest -q tests/python/test_controlled_runner.py
```

It covers successful strict records, deterministic hashes, wall timeout
(including a pipe-inheriting descendant), streamed stdout/stderr caps, child
address-space setup, interruption and atomic checkpointing,
exact-artifact-bound restart-only resume, run/read path and symlink escape
rejection, child side-output refusal, shell exclusion, fail-closed JSON
validation, atomic record writing, optional telemetry, pause/resume decisions,
combined memory/temperature precedence, and thermal abort behavior.
