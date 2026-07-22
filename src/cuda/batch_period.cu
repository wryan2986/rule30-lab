#include "rule30_cuda/batch_period.hpp"

#include <cuda_runtime.h>

#include <algorithm>
#include <chrono>
#include <cstdio>
#include <limits>
#include <stdexcept>
#include <string>
#include <type_traits>
#include <utility>

namespace rule30::cuda {
namespace {

using Clock = std::chrono::steady_clock;

static_assert(std::is_trivially_copyable_v<PeriodCandidate>);
static_assert(std::is_trivially_copyable_v<PeriodResult>);
static_assert(sizeof(PeriodCandidate) == 24);
static_assert(sizeof(PeriodResult) == 24);

[[noreturn]] void throw_cuda_error(cudaError_t status, const char* expression,
                                   const char* file, int line) {
  throw std::runtime_error(std::string("CUDA call failed: ") + expression +
                           " at " + file + ":" + std::to_string(line) +
                           ": " + cudaGetErrorString(status));
}

void check_cuda(cudaError_t status, const char* expression, const char* file,
                int line) {
  if (status != cudaSuccess) {
    throw_cuda_error(status, expression, file, line);
  }
}

#define RULE30_CUDA_CHECK(expression) \
  ::rule30::cuda::check_cuda((expression), #expression, __FILE__, __LINE__)

double elapsed_milliseconds(Clock::time_point start, Clock::time_point end) {
  return std::chrono::duration<double, std::milli>(end - start).count();
}

std::size_t checked_product(std::size_t count, std::size_t item_size,
                            const char* description) {
  if (item_size != 0 && count > std::numeric_limits<std::size_t>::max() / item_size) {
    throw std::overflow_error(std::string(description) + " size overflow");
  }
  return count * item_size;
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
    const std::size_t bytes = checked_product(count, sizeof(T), "device allocation");
    RULE30_CUDA_CHECK(cudaMalloc(reinterpret_cast<void**>(&pointer_), bytes));
  }

  void release() {
    if (pointer_ == nullptr) {
      return;
    }
    T* pointer = std::exchange(pointer_, nullptr);
    RULE30_CUDA_CHECK(cudaFree(pointer));
  }

  [[nodiscard]] T* get() const { return pointer_; }

 private:
  T* pointer_{nullptr};
};

class CudaEvent {
 public:
  CudaEvent() { RULE30_CUDA_CHECK(cudaEventCreate(&event_)); }
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
    RULE30_CUDA_CHECK(cudaEventDestroy(event));
  }

  [[nodiscard]] cudaEvent_t get() const { return event_; }

 private:
  cudaEvent_t event_{nullptr};
};

__global__ void evaluate_period_candidates_kernel(
    const std::uint8_t* bits, const PeriodCandidate* candidates,
    PeriodResult* results, std::uint64_t candidate_count) {
  const std::uint64_t candidate_index =
      static_cast<std::uint64_t>(blockIdx.x) * blockDim.x + threadIdx.x;
  if (candidate_index >= candidate_count) {
    return;
  }

  const PeriodCandidate candidate = candidates[candidate_index];
  std::uint64_t first_mismatch = kNoMismatch;
  std::uint64_t comparisons_checked = 0;

  for (std::uint64_t t = candidate.start; t < candidate.end; ++t) {
    ++comparisons_checked;
    if (bits[t] != bits[t - candidate.period]) {
      first_mismatch = t;
      break;
    }
  }

  PeriodResult result{};
  result.first_mismatch = first_mismatch;
  result.comparisons_checked = comparisons_checked;
  result.matches = first_mismatch == kNoMismatch ? 1U : 0U;
  results[candidate_index] = result;
}

void validate_inputs(std::span<const std::uint8_t> bits,
                     std::span<const PeriodCandidate> candidates,
                     const BatchConfig& config) {
  if (config.device_index < 0) {
    throw std::invalid_argument("device_index must be nonnegative");
  }
  if (config.threads_per_block <= 0) {
    throw std::invalid_argument("threads_per_block must be positive");
  }
  if (config.device_memory_budget_bytes == 0) {
    throw std::invalid_argument("device_memory_budget_bytes must be positive");
  }

  const std::size_t output_bytes =
      checked_product(candidates.size(), sizeof(PeriodResult), "host output");
  if (config.max_output_bytes != 0 && output_bytes > config.max_output_bytes) {
    throw std::invalid_argument("candidate results exceed max_output_bytes");
  }

  for (std::size_t index = 0; index < candidates.size(); ++index) {
    const PeriodCandidate& candidate = candidates[index];
    if (candidate.period == 0) {
      throw std::invalid_argument("candidate " + std::to_string(index) +
                                  " has period zero");
    }
    if (candidate.start > candidate.end) {
      throw std::invalid_argument("candidate " + std::to_string(index) +
                                  " has start greater than end");
    }
    if (candidate.start < candidate.period) {
      throw std::invalid_argument("candidate " + std::to_string(index) +
                                  " starts before its period");
    }
    if (candidate.end > static_cast<std::uint64_t>(bits.size())) {
      throw std::invalid_argument("candidate " + std::to_string(index) +
                                  " extends beyond the bit sequence");
    }
  }
}

}  // namespace

int device_count() {
  int count = 0;
  RULE30_CUDA_CHECK(cudaGetDeviceCount(&count));
  return count;
}

DeviceInfo probe_device(int device_index) {
  if (device_index < 0) {
    throw std::invalid_argument("device_index must be nonnegative");
  }

  const int count = device_count();
  if (device_index >= count) {
    throw std::invalid_argument("device_index is outside the available CUDA devices");
  }

  RULE30_CUDA_CHECK(cudaSetDevice(device_index));

  cudaDeviceProp properties{};
  RULE30_CUDA_CHECK(cudaGetDeviceProperties(&properties, device_index));

  int driver_version = 0;
  int runtime_version = 0;
  RULE30_CUDA_CHECK(cudaDriverGetVersion(&driver_version));
  RULE30_CUDA_CHECK(cudaRuntimeGetVersion(&runtime_version));

  std::size_t free_memory = 0;
  std::size_t total_memory = 0;
  RULE30_CUDA_CHECK(cudaMemGetInfo(&free_memory, &total_memory));

  DeviceInfo info{};
  info.device_index = device_index;
  info.name = properties.name;
  info.compute_major = properties.major;
  info.compute_minor = properties.minor;
  info.multiprocessor_count = properties.multiProcessorCount;
  info.max_threads_per_block = properties.maxThreadsPerBlock;
  info.max_grid_size_x = properties.maxGridSize[0];
  info.total_global_memory_bytes = total_memory;
  info.free_global_memory_bytes = free_memory;
  info.driver_version = driver_version;
  info.runtime_version = runtime_version;
  return info;
}

std::vector<PeriodResult> evaluate_period_candidates(
    std::span<const std::uint8_t> bits,
    std::span<const PeriodCandidate> candidates, const BatchConfig& config,
    BatchStats* stats) {
  validate_inputs(bits, candidates, config);
  if (stats != nullptr) {
    *stats = {};
  }
  if (candidates.empty()) {
    return {};
  }

  const auto end_to_end_start = Clock::now();
  const DeviceInfo device = probe_device(config.device_index);
  if (config.threads_per_block > device.max_threads_per_block) {
    throw std::invalid_argument("threads_per_block exceeds the device limit");
  }

  constexpr std::size_t kFreeMemoryReserve = 64ULL * 1024ULL * 1024ULL;
  const std::size_t safe_free_memory =
      device.free_global_memory_bytes > kFreeMemoryReserve
          ? device.free_global_memory_bytes - kFreeMemoryReserve
          : device.free_global_memory_bytes / 2;
  const std::size_t effective_budget =
      std::min(config.device_memory_budget_bytes, safe_free_memory);
  const std::size_t sequence_bytes = bits.size_bytes();
  const std::size_t bytes_per_candidate =
      sizeof(PeriodCandidate) + sizeof(PeriodResult);

  if (sequence_bytes > effective_budget ||
      effective_budget - sequence_bytes < bytes_per_candidate) {
    throw std::invalid_argument(
        "device memory budget cannot hold the sequence and one candidate");
  }

  std::size_t chunk_capacity =
      (effective_budget - sequence_bytes) / bytes_per_candidate;
  chunk_capacity = std::min(chunk_capacity, candidates.size());
  if (config.max_chunk_candidates != 0) {
    chunk_capacity = std::min(chunk_capacity, config.max_chunk_candidates);
  }

  if (device.max_grid_size_x <= 0) {
    throw std::runtime_error("CUDA device reported an invalid x-grid limit");
  }
  const std::size_t maximum_grid_candidates = checked_product(
      static_cast<std::size_t>(device.max_grid_size_x),
      static_cast<std::size_t>(config.threads_per_block), "kernel grid");
  chunk_capacity = std::min(chunk_capacity, maximum_grid_candidates);
  if (chunk_capacity == 0) {
    throw std::invalid_argument("configuration produced an empty GPU chunk");
  }

  DeviceBuffer<std::uint8_t> device_bits;
  DeviceBuffer<PeriodCandidate> device_candidates;
  DeviceBuffer<PeriodResult> device_results;
  device_bits.allocate(bits.size());
  device_candidates.allocate(chunk_capacity);
  device_results.allocate(chunk_capacity);
  CudaEvent kernel_start;
  CudaEvent kernel_stop;

  BatchStats local_stats{};
  local_stats.candidates_evaluated = candidates.size();
  local_stats.chunk_capacity = chunk_capacity;
  local_stats.peak_device_bytes =
      sequence_bytes + chunk_capacity * bytes_per_candidate;
  local_stats.effective_device_budget_bytes = effective_budget;

  auto transfer_start = Clock::now();
  RULE30_CUDA_CHECK(cudaMemcpy(device_bits.get(), bits.data(), sequence_bytes,
                               cudaMemcpyHostToDevice));
  local_stats.host_to_device_milliseconds +=
      elapsed_milliseconds(transfer_start, Clock::now());

  std::vector<PeriodResult> results(candidates.size());
  for (std::size_t offset = 0; offset < candidates.size();
       offset += chunk_capacity) {
    const std::size_t count =
        std::min(chunk_capacity, candidates.size() - offset);
    const std::size_t candidate_bytes =
        checked_product(count, sizeof(PeriodCandidate), "candidate transfer");
    const std::size_t result_bytes =
        checked_product(count, sizeof(PeriodResult), "result transfer");

    transfer_start = Clock::now();
    RULE30_CUDA_CHECK(cudaMemcpy(device_candidates.get(), candidates.data() + offset,
                                 candidate_bytes, cudaMemcpyHostToDevice));
    local_stats.host_to_device_milliseconds +=
        elapsed_milliseconds(transfer_start, Clock::now());

    const std::size_t threads =
        static_cast<std::size_t>(config.threads_per_block);
    const unsigned int block_count = static_cast<unsigned int>(
        count / threads + static_cast<std::size_t>(count % threads != 0));
    RULE30_CUDA_CHECK(cudaEventRecord(kernel_start.get()));
    evaluate_period_candidates_kernel<<<block_count, config.threads_per_block>>>(
        device_bits.get(), device_candidates.get(), device_results.get(), count);
    RULE30_CUDA_CHECK(cudaGetLastError());
    RULE30_CUDA_CHECK(cudaEventRecord(kernel_stop.get()));
    RULE30_CUDA_CHECK(cudaEventSynchronize(kernel_stop.get()));
    float kernel_milliseconds = 0.0F;
    RULE30_CUDA_CHECK(cudaEventElapsedTime(&kernel_milliseconds, kernel_start.get(),
                                          kernel_stop.get()));
    local_stats.kernel_milliseconds += kernel_milliseconds;

    transfer_start = Clock::now();
    RULE30_CUDA_CHECK(cudaMemcpy(results.data() + offset, device_results.get(),
                                 result_bytes, cudaMemcpyDeviceToHost));
    local_stats.device_to_host_milliseconds +=
        elapsed_milliseconds(transfer_start, Clock::now());
    ++local_stats.chunks;
  }

  kernel_stop.close();
  kernel_start.close();
  device_results.release();
  device_candidates.release();
  device_bits.release();
  local_stats.end_to_end_milliseconds =
      elapsed_milliseconds(end_to_end_start, Clock::now());

  if (stats != nullptr) {
    *stats = local_stats;
  }
  return results;
}

}  // namespace rule30::cuda
