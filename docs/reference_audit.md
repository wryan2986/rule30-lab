# Adversarial audit of `rule30_research_reference.py`

Date: 2026-07-21
Audited commit: `8296a83e5972257a23a3d80cf0016a351a92ed6d`
Audited file SHA-256: `358bdc07904e77080eb78b67bdd8da25822d6b51f1a91b58b5313dfe461c1d01`

## Scope and method

This audit covers every function in `src/python/rule30_research_reference.py`, including `main`, without modifying that file. It focuses on indexing conventions, empty and insufficient inputs, spatial orientation, resource growth, sideways-reconstruction assumptions, and the boundary between finite computation and infinite mathematical claims.

Checks were independent of the implementation where that distinction matters:

- A cell-array Rule 30 implementation, indexed directly by spatial coordinate `j`, was written independently and compared with `center_column` through time 256.
- Complete small rows were derived from the local rule, not from the packed-integer update.
- A brute-force oracle enumerated all binary recurrence coefficients to obtain the finite GF(2) linear complexity of every nonempty binary word of lengths 1 through 8 (510 words total).
- For every binary center trace through horizons 0 through 4, all possible finite initial-left vectors were enumerated, evolved by an ordinary forward cellular automaton, and compared with `reconstruct_left_initial`.
- Boundary and malformed-input behavior was exercised directly and through the command line with Python bytecode writing disabled.

The central valid-input algorithms passed these checks. The confirmed defects below concern contracts, edge cases, and the interpretation of reported values. No finite check in this audit is offered as proof of an infinite Rule 30 claim.

## Independently derived small examples and conventions

Rows below are written from spatial position `j=-t` on the left to `j=t` on the right. The center is the character at zero-based index `t`.

| `t` | Complete row | `c_t` |
|---:|:---|---:|
| 0 | `1` | 1 |
| 1 | `111` | 1 |
| 2 | `11001` | 0 |
| 3 | `1101111` | 1 |
| 4 | `110010001` | 1 |
| 5 | `11011110111` | 1 |
| 6 | `1100100001001` | 0 |
| 7 | `110111100111111` | 0 |
| 8 | `11001000111000001` | 1 |

Thus `c_0...c_8 = 110111001`. The independently evolved first 100 bits contain 52 ones, so `D(100) = 2(52)-100 = 4`.

The file uses two conventions that need to remain explicit:

1. `center_column(steps)` returns `steps + 1` bits, namely `c_0` through `c_steps`. Here `steps` counts updates, not output bits.
2. A center trace of length `h + 1`, covering times 0 through `h`, determines exactly `h` initial-left cells, `x_{-1}(0)` through `x_{-h}(0)`.

## Confirmed bugs

### C1. Empty Berlekamp-Massey input crashes, and the CLI exposes the crash

At lines 97--100, lists of length `n` are allocated and index zero is assigned unconditionally. Therefore:

```text
berlekamp_massey_binary([]) -> IndexError
```

The conventional linear complexity of the empty finite word is 0. Explicit rejection with `ValueError` would also be coherent, but the current accidental `IndexError` is not. This is reachable through the advertised CLI: `--linear-prefix 0` passes an empty slice and terminates with `IndexError`.

Negative `--linear-prefix` values are worse: Python interprets them as negative slice endpoints. For example, with four generated bits, `--linear-prefix -1` analyzes three bits and prints `N=-1`. The reported input length is then false.

Required correction: define empty-prefix behavior, reject negative lengths at argument parsing, and ensure the printed `N` equals the actual analyzed length.

### C2. `longest_matching_suffix_for_period` does not return the documented suffix length

The loop at lines 135--139 counts final recurrence equalities, not bits in the maximal periodic suffix. If `r` equalities are counted for period `p`, the corresponding bit suffix has length `r + p` (bounded here automatically by the input length).

Concrete examples:

```text
longest_matching_suffix_for_period([0,1,0,1], 2)       -> 2
actual maximal period-2 suffix length                  -> 4

longest_matching_suffix_for_period([1,0,0,1,0,1], 2)   -> 2
actual maximal period-2 suffix is [0,1,0,1], length    -> 4
```

For a wholly period-`p` word of length `n`, the function returns `n-p`, not `n`. The computation is valid if the intended metric is “number of trailing recurrence constraints satisfied,” but the function name, docstring, and CLI label “matching suffix” do not say that. Either return `matched + period` or rename and document the metric. Historical outputs must state which convention they used.

### C3. The 2-kernel function silently compares truncated and empty prefixes

For level `k`, let `m = 2^k` and requested prefix length be `q`. Every residue-class subsequence has `q` available terms only when `len(bits) >= m*q`. The function does not check this. It silently inserts shorter byte strings for late residues, so missing data can itself make two “prefixes” appear distinct.

The smallest counterexample is decisive:

```text
two_kernel_distinct_prefixes([0], level=1, prefix_length=1) -> 2
```

It appears to report `2/2` distinct one-bit prefixes, although residue 1 has no bit at all; the compared byte strings are `b'\x00'` and `b''`.

A negative `prefix_length` is also accepted as Python's “drop trailing items” slice convention instead of being rejected. A negative `level` fails with a low-level negative-shift exception. The function should validate `level >= 0`, define whether a zero-length diagnostic is permitted, require `prefix_length >= 1` for research use, and reject insufficient source data.

The current `main` loop does guard its fixed 64-bit call with `modulus * 64 <= len(bits)`, so this specific defect does not invalidate 2-kernel values produced through that loop. It does invalidate unrestricted direct use of the function.

### C4. Negative size arguments can produce plausible but meaningless output

Input-domain checks are inconsistent:

- `periodic_trace("10", -1)` silently returns an empty trace because `range(-1)` is empty.
- A negative `--max-period` produces an empty ranking headed by a range such as `periods 1..-1` and exits successfully.
- Negative `--linear-prefix` has the mislabeled-slice behavior described in C1.

These values are outside the mathematical domains described by the interfaces and should be rejected at the boundary. `periodic_trace(..., 0)` may reasonably return an empty trace if explicitly documented; negative length should not.

## Questionable behavior and research hazards

### Q1. “Bit” inputs are trusted rather than validated

All analytical functions assume values in `{0,1}`, but this precondition is not enforced or consistently implied by Python failures.

- `balance_report` sums arbitrary integers as ones.
- `autocorrelation` maps every nonzero value to `+1` by truthiness, which is not the documented transformation `2*bit-1` outside `{0,1}`.
- `block_counts` can create keys outside `0...(2^width-1)` because the initial window is not masked after incorporating a non-bit.
- `berlekamp_massey_binary` no longer computes over GF(2) for arbitrary integers.
- `two_kernel_distinct_prefixes` accepts byte values 0 through 255, not just bits.
- `reconstruct_left_initial` accepts byte values above 1 and applies integer XOR/OR rather than Boolean Rule 30.

Internal use with `center_column` is safe, but public research APIs should either validate once at a trusted boundary or state and test a strict binary precondition.

### Q2. `reconstruct_left_initial` can make vacuous compatibility look positive

An empty trace returns `[]`; a one-element trace also returns `[]`. Moreover, the function does not enforce the single-cell condition `center[0] == 1`. For example, an all-zero center trace reconstructs an all-zero left prefix, but it is already incompatible with the seed at time zero.

This is not an inversion error: the function is useful for arbitrary boundary traces. It is a caller-level hazard. A “compatible with the single-cell seed” predicate must separately require all of the following:

- a nonempty trace;
- `center[0] == 1`;
- binary values;
- the reconstructed finite left prefix is zero.

Even all four establish only compatibility over the finite reconstructed triangle.

### Q3. Resource growth is unsafe for unrestricted parameters

| Function | Time | Peak memory | Main hazard |
|:---|:---|:---|:---|
| `center_column(n)` | quadratic bit-work in `n` | `O(n)` bits plus output | Repeated growing big-integer operations become expensive at large `n`. |
| `balance_report` | `O(n + q log q)` | `O(q)` | Prints only; silently discards invalid/out-of-range checkpoints. |
| `autocorrelation` | `O(n)` per lag | `O(1)` | Repeated lag sweeps reread the sequence. |
| `block_counts(n,w)` | `O(n + 2^w)` | `O(2^w)` | Explicitly creates every absent block; moderate `w` can exhaust memory/time. |
| `berlekamp_massey_binary(n)` | `O(n^2)` | `O(n)` peak | Copies the full connection vector at every nonzero discrepancy, causing substantial allocation traffic. |
| suffix test | `O(n)` per period worst case | `O(1)` | Testing many periods is `O(Pn)` in the worst case. |
| 2-kernel test | `O(2^k q)` when fully supplied | `O(2^k q)` | Exponential growth in level and no direct resource bound. |
| `reconstruct_left_initial(h+1)` | `O(h^2)` | `O(h^2)` | Allocates an `(h+1) x (h+2)` byte matrix; large horizons can exhaust RAM. |
| `periodic_trace(length)` | `O(length)` | `O(length)` | No output-size guard in this reference function. |

The default main-program horizon of 500 keeps sideways reconstruction modest, and block widths are capped at 8 there. Direct calls are not similarly protected.

### Q4. Several reporting choices can obscure the exact sample

- `--steps n` creates `n+1` center bits. This is mathematically coherent because the initial state is time zero, but users asking for “one million bits” need `steps=999999`, whereas the historical invocation may use one million updates and then select the first million bits at checkpoints.
- Balance checkpoints count `bits[0:N]`, hence `c_0` through `c_{N-1}`. This is the correct convention for the stated discrepancy, but it must be included in result metadata.
- Autocorrelation and block statistics consume all generated `steps+1` bits, while fixed balance checkpoints can consume fewer. A single CLI run can therefore report statistics for different sample sizes without printing every size.
- `balance_report` silently removes duplicate, nonpositive, and out-of-range checkpoints. Silent omission can hide a requested result.
- The banner `First 80 center bits` prints fewer than 80 when fewer are available.

### Q5. The autocorrelation is an uncentered spin product

The implementation computes exactly the documented quantity

`(1/(N-lag)) * sum s_t s_(t+lag)`, with `s_t = 2c_t-1`.

It does not subtract the finite-sample mean and is therefore not a Pearson correlation coefficient or covariance. This is not a code defect because the docstring is explicit, but reports should preserve the definition.

## Verified facts

### `center_column`

Let packed bit `k` at time `t` encode spatial cell `x_(t-k)(t)`. At time `t+1`, packed bit `k` must be

`old[k] XOR (old[k-1] OR old[k-2])`.

The expression `row ^ ((row << 1) | (row << 2))` implements exactly this relation, and the original center is at packed position `t`. Parentheses and Python operator semantics are correct; no negative shifts or fixed-width overflow occur. The result matched an independently indexed cell-array evolution at every time through 256, including the rows listed above. `center_column(0) == bytearray([1])` is correct.

### `balance_report`

For valid binary input, checkpoint `N` includes exactly the first `N` sequence values and computes `D(N) = 2*ones-N`. Sorting and deduplication of valid checkpoints are correct. The independent first-100 calculation reproduced 52 ones and `D(100)=4`.

### `autocorrelation`

The lag bounds exclude empty products and division by zero. For `[1,1,0]`, the spin sequence is `[+1,+1,-1]`; lag 1 gives `(1-1)/2 = 0`, and lag 2 gives `-1`. The function returns those values.

### `block_counts`

For valid bits and practical width, the rolling mask and big-endian block orientation are correct. For bits `[1,0,1,1]` and width 2, the windows are `10`, `01`, and `11`, giving `{0:0, 1:1, 2:1, 3:1}`. There are exactly `len(bits)-width+1` counted windows, and absent valid blocks are represented with zero counts.

### `berlekamp_massey_binary`

For nonempty binary inputs, the update is a standard finite Berlekamp-Massey computation over GF(2). It agreed with exhaustive coefficient enumeration for all 510 nonempty binary words of lengths 1 through 8. Examples include complexity 0 for `[0]`, 1 for `[1,1,1,1]`, 2 for `[1,0,1,0]`, and 2 for `[0,1]`. This verification does not remove the empty-input bug or the quadratic cost.

### Period matching

The loop correctly counts consecutive equalities `bits[i] == bits[i-period]` while scanning backward from the final element. The defect is the interpretation of that count as a bit-suffix length, not the equality checks themselves.

### 2-kernel extraction

When `level >= 0`, the input is binary, `prefix_length >= 1`, and `len(bits) >= 2^level * prefix_length`, the slice `bits[residue::modulus][:prefix_length]` extracts the intended sequence `c_(2^level*n+residue)` in increasing `n`. Distinct byte strings then count distinct observed prefixes correctly. The guard in `main` establishes the required length for its 64-bit prefixes.

### `reconstruct_left_initial`

The spatial orientation and inversion are correct. The right-side table evolves `x_j(t+1)` for `j>0` using the supplied `x_0(t)` boundary and the initial condition `x_j(0)=0` for `j>0`. Its far-right zero boundary is valid for the finite horizon by the radius-one light cone.

For a current column `x_j(t)` and known right-neighbor column `x_(j+1)(t)`, lines 211--214 implement

`x_(j-1)(t) = x_j(t+1) XOR (x_j(t) OR x_(j+1)(t))`.

After each depth, assigning the old current column as the new right neighbor is the correct orientation. Exhaustive forward evolution found exactly the returned initial-left vector for every binary center trace through horizons 0, 1, 2, 3, and 4. Small examples are:

```text
reconstruct_left_initial([1])       == []
reconstruct_left_initial([1,1])     == [0]
reconstruct_left_initial([1,1,0])   == [0,0]
reconstruct_left_initial([1,1,1])   == [0,1]
reconstruct_left_initial([1,0,0])   == [1,0]
```

The independently generated true center prefixes reconstructed all-zero initial-left vectors through horizon 12.

### `periodic_trace`

For nonempty binary words and nonnegative lengths, phase and orientation are straightforward and correct: `periodic_trace("10", 5) == bytearray([1,0,1,0,1])`. Nonminimal period words are intentionally accepted.

### `main`

For default positive arguments, the calls are internally compatible. Its 2-kernel guard is sufficient, its sideways horizon uses `steps` rather than `steps+1`, and the true center slice has the required `horizon+1` values. The module-level warning correctly says the tool is experimental and not a proof.

## Finite-versus-infinite inference boundaries

The following conclusions are justified by these functions, and only at the stated scope:

- A disagreement between a generated bit and a proposed purely periodic trace is a finite refutation of that particular trace alignment. No finite prefix can rule out eventual periodicity whose preperiod starts beyond the observed range.
- Pairwise different finite prefixes prove that those particular residue-class subsequences are different as infinite sequences, assuming the generated bits are correct. Finitely many tested levels provide only a finite lower bound on 2-kernel size; they do not prove nonautomaticity.
- A reconstructed `1` at some initial-left position is a finite incompatibility certificate for that proposed center prefix under the zero-right-half assumption. An all-zero reconstructed finite prefix is only finite compatibility and does not prove that the infinite left tail is zero.
- Balance, block counts, autocorrelation, and finite linear complexity are empirical properties of the sampled prefix. They imply neither limiting balance nor randomness.
- Failure to find a period, recurrence, automaton, or compatible trace is not a nonexistence proof outside the explicitly exhausted finite search space.

## Concrete regression tests to add

The following tests are minimal. Tests marked “after contract fix” encode the recommended behavior rather than the current behavior.

```python
def test_center_column_small_rows():
    assert center_column(0) == bytearray([1])
    assert center_column(8) == bytearray([1, 1, 0, 1, 1, 1, 0, 0, 1])


def test_center_column_against_independent_cell_array_to_256():
    assert center_column(256) == direct_cell_array_centers(256)


def test_balance_counts_c0_through_c_n_minus_1(capsys):
    balance_report([1, 1, 0, 1], [4])
    out = capsys.readouterr().out
    assert "ones=        3" in out
    assert "D=      2" in out


def test_autocorrelation_small_exact_values():
    assert autocorrelation([1, 1, 0], 1) == 0.0
    assert autocorrelation([1, 1, 0], 2) == -1.0


def test_autocorrelation_rejects_empty_product():
    with pytest.raises(ValueError):
        autocorrelation([1], 1)


def test_block_counts_orientation_and_absent_blocks():
    counts = block_counts([1, 0, 1, 1], 2)
    assert counts == Counter({1: 1, 2: 1, 3: 1, 0: 0})
    assert set(counts) == {0, 1, 2, 3}


def test_berlekamp_massey_empty_is_zero_after_contract_fix():
    assert berlekamp_massey_binary([]) == 0


@pytest.mark.parametrize(
    ("bits", "expected"),
    [([0], 0), ([1], 1), ([1, 1, 1, 1], 1), ([1, 0, 1, 0], 2), ([0, 1], 2)],
)
def test_berlekamp_massey_examples(bits, expected):
    assert berlekamp_massey_binary(bits) == expected


def test_berlekamp_massey_against_exhaustive_oracle():
    for n in range(1, 9):
        for bits in itertools.product((0, 1), repeat=n):
            assert berlekamp_massey_binary(bits) == brute_force_linear_complexity(bits)


def test_periodic_suffix_contract_after_fix():
    assert longest_matching_suffix_for_period([0, 1, 0, 1], 2) == 4
    assert longest_matching_suffix_for_period([1, 0, 0, 1, 0, 1], 2) == 4


def test_kernel_prefixes_with_full_data():
    assert two_kernel_distinct_prefixes([0, 1, 1, 0], 1, 2) == 2


def test_kernel_rejects_insufficient_data_after_contract_fix():
    with pytest.raises(ValueError):
        two_kernel_distinct_prefixes([0], 1, 1)


@pytest.mark.parametrize(("level", "prefix"), [(-1, 1), (1, -1)])
def test_kernel_rejects_negative_parameters(level, prefix):
    with pytest.raises(ValueError):
        two_kernel_distinct_prefixes([0, 1, 1, 0], level, prefix)


@pytest.mark.parametrize(
    ("center", "left"),
    [([1], []), ([1, 1], [0]), ([1, 1, 0], [0, 0]), ([1, 1, 1], [0, 1]), ([1, 0, 0], [1, 0])],
)
def test_sideways_small_examples(center, left):
    assert reconstruct_left_initial(center) == left


def test_sideways_against_exhaustive_forward_oracle():
    for horizon in range(5):
        for center in itertools.product((0, 1), repeat=horizon + 1):
            assert reconstruct_left_initial(center) == unique_left_vector_by_forward_search(center)


def test_true_trace_reconstructs_zero_finite_tail():
    for horizon in range(13):
        assert reconstruct_left_initial(center_column(horizon)) == [0] * horizon


def test_periodic_trace_and_negative_length():
    assert periodic_trace("10", 5) == bytearray([1, 0, 1, 0, 1])
    with pytest.raises(ValueError):
        periodic_trace("10", -1)


def test_cli_rejects_negative_analysis_sizes():
    # Use subprocess.run and assert a documented nonzero exit with a concise argparse error.
    for args in (["--linear-prefix", "-1"], ["--max-period", "-1"]):
        completed = run_reference_cli(*args)
        assert completed.returncode != 0
```

Add a shared binary-input validation test for each public analytical function if validation is adopted. Add resource-limit tests around block width, 2-kernel level, and reconstruction horizon in the production wrapper rather than attempting dangerous allocations in unit tests.

## Bottom line

No valid-domain error was found in packed center evolution, finite GF(2) linear complexity for nonempty words, right-half evolution, or sideways inversion orientation. The most research-significant defect is the 2-kernel function's silent underlength behavior; the current `main` guard avoids it, but reusable code must not. The period routine's output is also systematically off by `period` if read according to its documented suffix-length contract. Empty and negative lengths need consistent rejection or explicit semantics before the reference implementation is treated as a trusted API.
