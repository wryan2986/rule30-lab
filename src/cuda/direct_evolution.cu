#include "rule30_cuda/direct_evolution.hpp"

#include "rule30_cuda/batch_period.hpp"

#include <cuda_runtime.h>

#include <algorithm>
#include <chrono>
#include <cstdio>
#include <limits>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

namespace rule30::cuda {
namespace {

using Clock = std::chrono::steady_clock;

constexpr std::uint64_t kFnvOffsetBasis = 0xcbf29ce484222325ULL;
constexpr std::uint64_t kFnvPrime = 1099511628211ULL;
constexpr std::size_t kFreeMemoryReserve = 64ULL * 1024ULL * 1024ULL;

[[noreturn]] void throw_direct_cuda_error(cudaError_t status,
                                          const char* expression,
                                          const char* file, int line) {
  throw std::runtime_error(std::string("CUDA call failed: ") + expression +
                           " at " + file + ":" + std::to_string(line) +
                           ": " + cudaGetErrorString(status));
}

void check_direct_cuda(cudaError_t status, const char* expression,
                       const char* file, int line) {
  if (status != cudaSuccess) {
    throw_direct_cuda_error(status, expression, file, line);
  }
}

#define RULE30_DIRECT_CUDA_CHECK(expression)                    \
  check_direct_cuda((expression), #expression, __FILE__, __LINE__)

double elapsed_milliseconds(Clock::time_point start, Clock::time_point end) {
  return std::chrono::duration<double, std::milli>(end - start).count();
}

std::size_t checked_add(std::size_t left, std::size_t right,
                        const char* description) {
  if (left > std::numeric_limits<std::size_t>::max() - right) {
    throw std::overflow_error(std::string(description) + " size overflow");
  }
  return left + right;
}

std::size_t checked_product(std::size_t count, std::size_t item_size,
                            const char* description) {
  if (item_size != 0 &&
      count > std::numeric_limits<std::size_t>::max() / item_size) {
    throw std::overflow_error(std::string(description) + " size overflow");
  }
  return count * item_size;
}

std::size_t row_bit_count_for(std::size_t center_bit_count) {
  if (center_bit_count == 0) {
    return 0;
  }
  if (center_bit_count >
      std::numeric_limits<std::size_t>::max() / 2U + 1U) {
    throw std::overflow_error("final row bit count overflow");
  }
  return center_bit_count * 2U - 1U;
}

std::size_t word_count_for(std::size_t bit_count) {
  return bit_count / 64U + static_cast<std::size_t>(bit_count % 64U != 0U);
}

void validate_config(const DirectEvolutionConfig& config) {
  if (config.device_index < 0) {
    throw std::invalid_argument("device_index must be nonnegative");
  }
  if (config.threads_per_block <= 0) {
    throw std::invalid_argument("threads_per_block must be positive");
  }
  if (config.device_memory_budget_bytes == 0) {
    throw std::invalid_argument("device_memory_budget_bytes must be positive");
  }
}

template <typename T>
class DeviceBuffer {
 public:
  DeviceBuffer() = default;
  DeviceBuffer(const DeviceBuffer&) = delete;
  DeviceBuffer& operator=(const DeviceBuffer&) = delete;

  ~DeviceBuffer() {
    if (pointer_ != nullptr) {
      const cudaError_t status = cudaFree(pointer_);
      if (status != cudaSuccess) {
        std::fprintf(stderr, "CUDA cleanup failed in cudaFree: %s\n",
                     cudaGetErrorString(status));
      }
    }
  }

  void allocate(std::size_t count) {
    if (count == 0) {
      return;
    }
    const std::size_t bytes =
        checked_product(count, sizeof(T), "device allocation");
    RULE30_DIRECT_CUDA_CHECK(
        cudaMalloc(reinterpret_cast<void**>(&pointer_), bytes));
  }

  void release() {
    if (pointer_ == nullptr) {
      return;
    }
    T* pointer = std::exchange(pointer_, nullptr);
    RULE30_DIRECT_CUDA_CHECK(cudaFree(pointer));
  }

  [[nodiscard]] T* get() const { return pointer_; }

 private:
  T* pointer_{nullptr};
};

class CudaEvent {
 public:
  CudaEvent() { RULE30_DIRECT_CUDA_CHECK(cudaEventCreate(&event_)); }
  CudaEvent(const CudaEvent&) = delete;
  CudaEvent& operator=(const CudaEvent&) = delete;

  ~CudaEvent() {
    if (event_ != nullptr) {
      const cudaError_t status = cudaEventDestroy(event_);
      if (status != cudaSuccess) {
        std::fprintf(stderr, "CUDA cleanup failed in cudaEventDestroy: %s\n",
                     cudaGetErrorString(status));
      }
    }
  }

  void close() {
    if (event_ == nullptr) {
      return;
    }
    cudaEvent_t event = std::exchange(event_, nullptr);
    RULE30_DIRECT_CUDA_CHECK(cudaEventDestroy(event));
  }

  [[nodiscard]] cudaEvent_t get() const { return event_; }

 private:
  cudaEvent_t event_{nullptr};
};

__device__ __forceinline__ std::uint64_t load_active_word(
    const std::uint64_t* row, std::uint64_t word_index,
    std::uint64_t active_low_word, std::uint64_t active_high_word) {
  if (word_index < active_low_word || word_index > active_high_word) {
    return 0;
  }
  return row[word_index];
}

__global__ void evolve_row_kernel(
    const std::uint64_t* current_row, std::uint64_t* next_row,
    std::uint8_t* center_bits, std::uint64_t total_word_count,
    std::uint64_t source_low_word, std::uint64_t source_high_word,
    std::uint64_t output_low_word, std::uint64_t output_word_count,
    std::uint64_t output_low_bit, std::uint64_t output_high_bit,
    std::uint64_t center_word, unsigned int center_offset,
    std::uint64_t center_output_index) {
  const std::uint64_t first =
      static_cast<std::uint64_t>(blockIdx.x) * blockDim.x + threadIdx.x;
  const std::uint64_t stride =
      static_cast<std::uint64_t>(gridDim.x) * blockDim.x;
  const std::uint64_t output_high_word =
      output_low_word + output_word_count - 1U;

  for (std::uint64_t local_index = first;
       local_index < output_word_count; local_index += stride) {
    const std::uint64_t word_index = output_low_word + local_index;
    const std::uint64_t current = load_active_word(
        current_row, word_index, source_low_word, source_high_word);
    const std::uint64_t previous =
        word_index == 0U
            ? 0U
            : load_active_word(current_row, word_index - 1U,
                               source_low_word, source_high_word);
    const std::uint64_t following =
        word_index + 1U >= total_word_count
            ? 0U
            : load_active_word(current_row, word_index + 1U,
                               source_low_word, source_high_word);

    // Bit i represents a coordinate increasing from left to right. Thus the
    // Rule 30 neighbors of output bit i are old bits i-1, i, and i+1.
    const std::uint64_t left = (current << 1U) | (previous >> 63U);
    const std::uint64_t right = (current >> 1U) | (following << 63U);
    std::uint64_t output = left ^ (current | right);

    if (word_index == output_low_word) {
      const unsigned int low_offset =
          static_cast<unsigned int>(output_low_bit & 63U);
      output &= ~std::uint64_t{0} << low_offset;
    }
    if (word_index == output_high_word) {
      const unsigned int high_offset =
          static_cast<unsigned int>(output_high_bit & 63U);
      if (high_offset != 63U) {
        output &= (std::uint64_t{1} << (high_offset + 1U)) - 1U;
      }
    }

    next_row[word_index] = output;
    if (word_index == center_word) {
      center_bits[center_output_index] =
          static_cast<std::uint8_t>((output >> center_offset) & 1U);
    }
  }
}

std::uint64_t fnv1a_bytes(const std::vector<std::uint8_t>& values) {
  std::uint64_t hash = kFnvOffsetBasis;
  for (const std::uint8_t value : values) {
    hash ^= value;
    hash *= kFnvPrime;
  }
  return hash;
}

std::uint64_t fnv1a_words(const std::vector<std::uint64_t>& values) {
  std::uint64_t hash = kFnvOffsetBasis;
  for (const std::uint64_t value : values) {
    for (unsigned int byte = 0; byte < 8U; ++byte) {
      hash ^= (value >> (byte * 8U)) & 0xffU;
      hash *= kFnvPrime;
    }
  }
  return hash;
}

}  // namespace

DirectEvolutionResult evolve_single_history(
    std::size_t center_bit_count, const DirectEvolutionConfig& config,
    DirectEvolutionStats* stats) {
  validate_config(config);
  if (stats != nullptr) {
    *stats = {};
  }

  const std::size_t row_bit_count = row_bit_count_for(center_bit_count);
  const std::size_t row_word_count = word_count_for(row_bit_count);
  const std::size_t row_bytes =
      checked_product(row_word_count, sizeof(std::uint64_t), "packed row");
  const std::size_t output_bytes =
      checked_add(center_bit_count, row_bytes, "host output");
  if (config.max_output_bytes != 0 &&
      output_bytes > config.max_output_bytes) {
    throw std::invalid_argument("direct evolution output exceeds max_output_bytes");
  }

  DirectEvolutionResult result{};
  result.center_hash_fnv1a64 = kFnvOffsetBasis;
  result.final_row_hash_fnv1a64 = kFnvOffsetBasis;
  if (center_bit_count == 0) {
    return result;
  }

  const std::size_t two_row_bytes =
      checked_product(row_bytes, 2U, "two packed rows");
  const std::size_t peak_device_bytes =
      checked_add(two_row_bytes, center_bit_count, "direct device buffers");

  const auto end_to_end_start = Clock::now();
  const DeviceInfo device = probe_device(config.device_index);
  if (config.threads_per_block > device.max_threads_per_block) {
    throw std::invalid_argument("threads_per_block exceeds the device limit");
  }
  if (device.max_grid_size_x <= 0) {
    throw std::runtime_error("CUDA device reported an invalid x-grid limit");
  }

  const std::size_t safe_free_memory =
      device.free_global_memory_bytes > kFreeMemoryReserve
          ? device.free_global_memory_bytes - kFreeMemoryReserve
          : device.free_global_memory_bytes / 2U;
  const std::size_t effective_budget =
      std::min(config.device_memory_budget_bytes, safe_free_memory);
  if (peak_device_bytes > effective_budget) {
    throw std::invalid_argument(
        "device memory budget cannot hold two rows and the center output");
  }

  result.center_bits.assign(center_bit_count, 0U);
  result.center_bits[0] = 1U;
  result.final_row_words.assign(row_word_count, 0U);
  const std::size_t center_position = center_bit_count - 1U;
  result.final_row_words[center_position / 64U] |=
      std::uint64_t{1} << (center_position & 63U);

  DeviceBuffer<std::uint64_t> row_a;
  DeviceBuffer<std::uint64_t> row_b;
  DeviceBuffer<std::uint8_t> device_center_bits;
  row_a.allocate(row_word_count);
  row_b.allocate(row_word_count);
  device_center_bits.allocate(center_bit_count);
  CudaEvent kernel_start;
  CudaEvent kernel_stop;

  DirectEvolutionStats local_stats{};
  local_stats.center_bit_count = center_bit_count;
  local_stats.final_row_bit_count = row_bit_count;
  local_stats.final_row_word_count = row_word_count;
  local_stats.peak_device_bytes = peak_device_bytes;
  local_stats.effective_device_budget_bytes = effective_budget;

  auto transfer_start = Clock::now();
  RULE30_DIRECT_CUDA_CHECK(cudaMemcpy(row_a.get(), result.final_row_words.data(),
                                      row_bytes, cudaMemcpyHostToDevice));
  RULE30_DIRECT_CUDA_CHECK(
      cudaMemcpy(device_center_bits.get(), result.center_bits.data(),
                 center_bit_count, cudaMemcpyHostToDevice));
  local_stats.host_to_device_milliseconds =
      elapsed_milliseconds(transfer_start, Clock::now());

  std::uint64_t* current_row = row_a.get();
  std::uint64_t* next_row = row_b.get();
  if (center_bit_count > 1U) {
    RULE30_DIRECT_CUDA_CHECK(cudaEventRecord(kernel_start.get()));
    for (std::size_t step = 1; step < center_bit_count; ++step) {
      const std::size_t source_radius = step - 1U;
      const std::size_t source_low_bit = center_position - source_radius;
      const std::size_t source_high_bit = center_position + source_radius;
      const std::size_t output_low_bit = center_position - step;
      const std::size_t output_high_bit = center_position + step;
      const std::size_t source_low_word = source_low_bit / 64U;
      const std::size_t source_high_word = source_high_bit / 64U;
      const std::size_t output_low_word = output_low_bit / 64U;
      const std::size_t output_high_word = output_high_bit / 64U;
      const std::size_t active_word_count =
          output_high_word - output_low_word + 1U;

      local_stats.row_word_updates = checked_add(
          local_stats.row_word_updates, active_word_count,
          "direct evolution word-update count");

      const std::size_t threads =
          static_cast<std::size_t>(config.threads_per_block);
      const std::size_t blocks_needed =
          active_word_count / threads +
          static_cast<std::size_t>(active_word_count % threads != 0U);
      const std::size_t block_count = std::min(
          blocks_needed, static_cast<std::size_t>(device.max_grid_size_x));

      evolve_row_kernel<<<static_cast<unsigned int>(block_count),
                          config.threads_per_block>>>(
          current_row, next_row, device_center_bits.get(), row_word_count,
          source_low_word, source_high_word, output_low_word,
          active_word_count, output_low_bit, output_high_bit,
          center_position / 64U,
          static_cast<unsigned int>(center_position & 63U), step);
      RULE30_DIRECT_CUDA_CHECK(cudaGetLastError());
      ++local_stats.kernel_launches;
      std::swap(current_row, next_row);
    }
    RULE30_DIRECT_CUDA_CHECK(cudaEventRecord(kernel_stop.get()));
    // This synchronization reports asynchronous launch or execution failures.
    RULE30_DIRECT_CUDA_CHECK(cudaEventSynchronize(kernel_stop.get()));
    float kernel_milliseconds = 0.0F;
    RULE30_DIRECT_CUDA_CHECK(cudaEventElapsedTime(
        &kernel_milliseconds, kernel_start.get(), kernel_stop.get()));
    local_stats.kernel_milliseconds = kernel_milliseconds;
  }

  transfer_start = Clock::now();
  RULE30_DIRECT_CUDA_CHECK(
      cudaMemcpy(result.center_bits.data(), device_center_bits.get(),
                 center_bit_count, cudaMemcpyDeviceToHost));
  RULE30_DIRECT_CUDA_CHECK(cudaMemcpy(result.final_row_words.data(), current_row,
                                      row_bytes, cudaMemcpyDeviceToHost));
  local_stats.device_to_host_milliseconds =
      elapsed_milliseconds(transfer_start, Clock::now());

  result.center_ones = static_cast<std::uint64_t>(
      std::count(result.center_bits.begin(), result.center_bits.end(), 1U));
  if (std::any_of(result.center_bits.begin(), result.center_bits.end(),
                  [](std::uint8_t bit) { return bit > 1U; })) {
    throw std::runtime_error("CUDA evolution produced a non-binary center byte");
  }
  result.center_zeros =
      static_cast<std::uint64_t>(center_bit_count) - result.center_ones;
  result.center_hash_fnv1a64 = fnv1a_bytes(result.center_bits);
  result.final_row_hash_fnv1a64 = fnv1a_words(result.final_row_words);

  kernel_stop.close();
  kernel_start.close();
  device_center_bits.release();
  row_b.release();
  row_a.release();
  local_stats.end_to_end_milliseconds =
      elapsed_milliseconds(end_to_end_start, Clock::now());

  if (stats != nullptr) {
    *stats = local_stats;
  }
  return result;
}

}  // namespace rule30::cuda
