#pragma once

#include <cstddef>
#include <cstdint>
#include <span>
#include <string>
#include <vector>

namespace rule30::cuda {

inline constexpr std::uint64_t kNoMismatch = UINT64_MAX;

// Check bits[t] == bits[t - period] for every t in [start, end).
// The host validates all ranges before launching a kernel.
struct PeriodCandidate {
  std::uint64_t start{};
  std::uint64_t end{};
  std::uint64_t period{};

  friend bool operator==(const PeriodCandidate&, const PeriodCandidate&) = default;
};

struct PeriodResult {
  std::uint64_t first_mismatch{kNoMismatch};
  std::uint64_t comparisons_checked{};
  std::uint32_t matches{};
  std::uint32_t reserved{};

  friend bool operator==(const PeriodResult&, const PeriodResult&) = default;
};

struct BatchConfig {
  int device_index{0};
  int threads_per_block{256};

  // This is a hard cap for the sequence, candidate, and result device buffers.
  // The implementation may use less to preserve free-memory headroom.
  std::size_t device_memory_budget_bytes{256ULL * 1024ULL * 1024ULL};

  // Zero means no additional chunk-size cap.
  std::size_t max_chunk_candidates{0};

  // Prevent accidental creation of enormous host result vectors. Zero disables
  // this guard explicitly.
  std::size_t max_output_bytes{64ULL * 1024ULL * 1024ULL};
};

struct BatchStats {
  std::size_t candidates_evaluated{};
  std::size_t chunks{};
  std::size_t chunk_capacity{};
  std::size_t peak_device_bytes{};
  std::size_t effective_device_budget_bytes{};
  double host_to_device_milliseconds{};
  double kernel_milliseconds{};
  double device_to_host_milliseconds{};
  double end_to_end_milliseconds{};
};

struct DeviceInfo {
  int device_index{};
  std::string name;
  int compute_major{};
  int compute_minor{};
  int multiprocessor_count{};
  int max_threads_per_block{};
  int max_grid_size_x{};
  std::size_t total_global_memory_bytes{};
  std::size_t free_global_memory_bytes{};
  int driver_version{};
  int runtime_version{};
};

[[nodiscard]] int device_count();
[[nodiscard]] DeviceInfo probe_device(int device_index = 0);

// Returns one compact result per candidate. This is an exact finite check, not
// evidence that a sequence is eventually periodic beyond the supplied range.
[[nodiscard]] std::vector<PeriodResult> evaluate_period_candidates(
    std::span<const std::uint8_t> bits,
    std::span<const PeriodCandidate> candidates,
    const BatchConfig& config = {},
    BatchStats* stats = nullptr);

}  // namespace rule30::cuda
