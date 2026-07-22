#pragma once

#include <cstddef>
#include <cstdint>
#include <span>
#include <vector>

namespace rule30::cuda {

struct SidewaysBatchConfig {
  int device_index{0};
  int threads_per_block{128};

  // Hard cap for trace, output, and workspace device buffers.
  std::size_t device_memory_budget_bytes{256ULL * 1024ULL * 1024ULL};

  // Zero means no additional candidate-count cap per chunk.
  std::size_t max_chunk_candidates{0};

  // Prevent accidental materialization of enormous reconstructed tails. Zero
  // disables this output guard explicitly.
  std::size_t max_output_bytes{64ULL * 1024ULL * 1024ULL};

  // Each trace has horizon trace_length-1. The explicit bound keeps per-thread
  // quadratic work controlled even when memory would permit a larger request.
  std::size_t max_horizon{512};
};

struct SidewaysBatchStats {
  std::size_t candidates_evaluated{};
  std::size_t trace_length{};
  std::size_t horizon{};
  std::size_t chunks{};
  std::size_t chunk_capacity{};
  std::size_t workspace_bytes_per_candidate{};
  std::size_t peak_device_bytes{};
  std::size_t effective_device_budget_bytes{};
  double host_to_device_milliseconds{};
  double kernel_milliseconds{};
  double device_to_host_milliseconds{};
  double end_to_end_milliseconds{};
};

// Reconstruct x[-1,0] through x[-horizon,0] for each supplied center trace,
// assuming the initial half-line x[j,0]=0 for j>0. Traces and results are flat,
// candidate-major numeric-byte arrays. The result has candidate_count*horizon
// bytes. This is an exact finite reconstruction, not an infinite compatibility
// claim.
[[nodiscard]] std::vector<std::uint8_t> reconstruct_left_initial_batch(
    std::span<const std::uint8_t> traces, std::size_t trace_length,
    const SidewaysBatchConfig& config = {},
    SidewaysBatchStats* stats = nullptr);

}  // namespace rule30::cuda
