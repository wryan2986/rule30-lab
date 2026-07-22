#pragma once

#include <cstddef>
#include <cstdint>
#include <vector>

namespace rule30::cuda {

// Resource controls for direct evolution of one Rule 30 history. The default
// budgets are intentionally conservative for an interactive workstation.
struct DirectEvolutionConfig {
  int device_index{0};
  int threads_per_block{256};

  // Hard cap for both packed row buffers and the center-bit device buffer.
  std::size_t device_memory_budget_bytes{256ULL * 1024ULL * 1024ULL};

  // Hard cap for the returned center bytes and packed final row. Zero disables
  // this guard explicitly.
  std::size_t max_output_bytes{64ULL * 1024ULL * 1024ULL};
};

struct DirectEvolutionStats {
  std::size_t center_bit_count{};
  std::size_t final_row_bit_count{};
  std::size_t final_row_word_count{};
  std::size_t row_word_updates{};
  std::size_t kernel_launches{};
  std::size_t peak_device_bytes{};
  std::size_t effective_device_budget_bytes{};
  double host_to_device_milliseconds{};
  double kernel_milliseconds{};
  double device_to_host_milliseconds{};
  double end_to_end_milliseconds{};
};

struct DirectEvolutionResult {
  // Exactly center_bit_count bytes, one numeric byte (0 or 1) per bit, for
  // c_0 through c_(center_bit_count-1).
  std::vector<std::uint8_t> center_bits;

  // Final row in little-endian packed-bit order. For N center bits, bit i is
  // x_(i-(N-1))(N-1). Bits beyond the final row width are always zero.
  std::vector<std::uint64_t> final_row_words;

  std::uint64_t center_ones{};
  std::uint64_t center_zeros{};
  std::uint64_t center_hash_fnv1a64{};
  std::uint64_t final_row_hash_fnv1a64{};

  friend bool operator==(const DirectEvolutionResult&,
                         const DirectEvolutionResult&) = default;
};

// Evolve Rule 30 from the single-black-cell seed and return exactly N center
// bits. This is direct sequential evolution: one CUDA kernel launch computes
// each new row, because row t+1 depends on row t.
[[nodiscard]] DirectEvolutionResult evolve_single_history(
    std::size_t center_bit_count,
    const DirectEvolutionConfig& config = {},
    DirectEvolutionStats* stats = nullptr);

}  // namespace rule30::cuda
