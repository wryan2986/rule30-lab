#include "rule30_cuda/batch_sideways.hpp"

#include "rule30_cuda/batch_period.hpp"

#include <cuda_runtime.h>

#include <algorithm>
#include <chrono>
#include <cstdio>
#include <limits>
#include <stdexcept>
#include <string>
#include <utility>

namespace rule30::cuda {
namespace {

using Clock = std::chrono::steady_clock;

constexpr std::size_t kFreeMemoryReserve = 64ULL * 1024ULL * 1024ULL;

[[noreturn]] void throw_sideways_cuda_error(cudaError_t status,
                                            const char* expression,
                                            const char* file, int line) {
  throw std::runtime_error(std::string("CUDA call failed: ") + expression +
                           " at " + file + ":" + std::to_string(line) +
                           ": " + cudaGetErrorString(status));
}

void check_sideways_cuda(cudaError_t status, const char* expression,
                         const char* file, int line) {
  if (status != cudaSuccess) {
    throw_sideways_cuda_error(status, expression, file, line);
  }
}

#define RULE30_SIDEWAYS_CUDA_CHECK(expression)                    \
  check_sideways_cuda((expression), #expression, __FILE__, __LINE__)

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

void validate_inputs(std::span<const std::uint8_t> traces,
                     std::size_t trace_length,
                     const SidewaysBatchConfig& config) {
  if (config.device_index < 0) {
    throw std::invalid_argument("device_index must be nonnegative");
  }
  if (config.threads_per_block <= 0) {
    throw std::invalid_argument("threads_per_block must be positive");
  }
  if (config.device_memory_budget_bytes == 0) {
    throw std::invalid_argument("device_memory_budget_bytes must be positive");
  }
  if (trace_length == 0) {
    throw std::invalid_argument("trace_length must be positive");
  }
  if (traces.size() % trace_length != 0) {
    throw std::invalid_argument(
        "flattened traces are not divisible by trace_length");
  }
  const std::size_t horizon = trace_length - 1U;
  if (horizon > config.max_horizon) {
    throw std::invalid_argument("trace horizon exceeds max_horizon");
  }
  if (std::any_of(traces.begin(), traces.end(),
                  [](std::uint8_t bit) { return bit > 1U; })) {
    throw std::invalid_argument("center traces must contain only numeric 0/1 bytes");
  }

  const std::size_t candidate_count = traces.size() / trace_length;
  const std::size_t output_bytes =
      checked_product(candidate_count, horizon, "sideways host output");
  if (config.max_output_bytes != 0 &&
      output_bytes > config.max_output_bytes) {
    throw std::invalid_argument("sideways results exceed max_output_bytes");
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
    RULE30_SIDEWAYS_CUDA_CHECK(
        cudaMalloc(reinterpret_cast<void**>(&pointer_), bytes));
  }

  void release() {
    if (pointer_ == nullptr) {
      return;
    }
    T* pointer = std::exchange(pointer_, nullptr);
    RULE30_SIDEWAYS_CUDA_CHECK(cudaFree(pointer));
  }

  [[nodiscard]] T* get() const { return pointer_; }

 private:
  T* pointer_{nullptr};
};

class CudaEvent {
 public:
  CudaEvent() { RULE30_SIDEWAYS_CUDA_CHECK(cudaEventCreate(&event_)); }
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
    RULE30_SIDEWAYS_CUDA_CHECK(cudaEventDestroy(event));
  }

  [[nodiscard]] cudaEvent_t get() const { return event_; }

 private:
  cudaEvent_t event_{nullptr};
};

__global__ void reconstruct_left_initial_kernel(
    const std::uint8_t* traces, std::uint8_t* reconstructed,
    std::uint8_t* workspace, std::uint64_t candidate_count,
    std::uint64_t trace_length, std::uint64_t horizon,
    std::uint64_t workspace_stride) {
  const std::uint64_t candidate_index =
      static_cast<std::uint64_t>(blockIdx.x) * blockDim.x + threadIdx.x;
  if (candidate_index >= candidate_count) {
    return;
  }

  const std::uint8_t* trace = traces + candidate_index * trace_length;
  std::uint8_t* output = reconstructed + candidate_index * horizon;
  std::uint8_t* candidate_workspace =
      workspace + candidate_index * 3U * workspace_stride;
  std::uint8_t* first = candidate_workspace;
  std::uint8_t* second = first + workspace_stride;
  std::uint8_t* third = second + workspace_stride;

  // Build the forced x[1,t] column from the supplied center boundary and the
  // all-zero initial half-line to its right. Three O(horizon) buffers suffice;
  // no quadratic per-candidate storage is retained.
  for (std::uint64_t index = 0; index < workspace_stride; ++index) {
    first[index] = 0U;
    second[index] = 0U;
    third[index] = 0U;
  }
  std::uint8_t* right_current = first;
  std::uint8_t* right_next = second;
  for (std::uint64_t time = 0; time <= horizon; ++time) {
    third[time] = right_current[1];
    if (time == horizon) {
      break;
    }
    right_current[0] = trace[time];
    for (std::uint64_t position = 1; position <= horizon; ++position) {
      right_next[position] = static_cast<std::uint8_t>(
          right_current[position - 1U] ^
          (right_current[position] | right_current[position + 1U]));
    }
    right_next[horizon + 1U] = 0U;
    std::uint8_t* swap = right_current;
    right_current = right_next;
    right_next = swap;
  }

  // Reuse the two row buffers for the sideways columns. At each depth,
  // left = next XOR (center OR right), then rotate all three buffers.
  std::uint8_t* current = first;
  std::uint8_t* neighbor = third;
  std::uint8_t* scratch = second;
  for (std::uint64_t time = 0; time < trace_length; ++time) {
    current[time] = trace[time];
  }
  for (std::uint64_t depth = 1; depth <= horizon; ++depth) {
    const std::uint64_t length = trace_length - depth;
    for (std::uint64_t time = 0; time < length; ++time) {
      scratch[time] = static_cast<std::uint8_t>(
          current[time + 1U] ^ (current[time] | neighbor[time]));
    }
    output[depth - 1U] = scratch[0];
    std::uint8_t* old_neighbor = neighbor;
    neighbor = current;
    current = scratch;
    scratch = old_neighbor;
  }
}

}  // namespace

std::vector<std::uint8_t> reconstruct_left_initial_batch(
    std::span<const std::uint8_t> traces, std::size_t trace_length,
    const SidewaysBatchConfig& config, SidewaysBatchStats* stats) {
  validate_inputs(traces, trace_length, config);
  if (stats != nullptr) {
    *stats = {};
  }

  const std::size_t candidate_count = traces.size() / trace_length;
  const std::size_t horizon = trace_length - 1U;
  const std::size_t output_bytes =
      checked_product(candidate_count, horizon, "sideways host output");
  std::vector<std::uint8_t> results(output_bytes);

  SidewaysBatchStats local_stats{};
  local_stats.candidates_evaluated = candidate_count;
  local_stats.trace_length = trace_length;
  local_stats.horizon = horizon;
  if (candidate_count == 0 || horizon == 0) {
    if (stats != nullptr) {
      *stats = local_stats;
    }
    return results;
  }

  const std::size_t workspace_stride =
      checked_add(horizon, 2U, "sideways workspace stride");
  const std::size_t workspace_bytes_per_candidate =
      checked_product(workspace_stride, 3U, "sideways workspace");
  const std::size_t trace_and_output_bytes =
      checked_add(trace_length, horizon, "sideways trace and output");
  const std::size_t bytes_per_candidate =
      checked_add(trace_and_output_bytes, workspace_bytes_per_candidate,
                  "sideways device buffers");

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
  if (effective_budget < bytes_per_candidate) {
    throw std::invalid_argument(
        "device memory budget cannot hold one sideways candidate");
  }

  std::size_t chunk_capacity = effective_budget / bytes_per_candidate;
  chunk_capacity = std::min(chunk_capacity, candidate_count);
  if (config.max_chunk_candidates != 0) {
    chunk_capacity = std::min(chunk_capacity, config.max_chunk_candidates);
  }
  const std::size_t maximum_grid_candidates = checked_product(
      static_cast<std::size_t>(device.max_grid_size_x),
      static_cast<std::size_t>(config.threads_per_block), "sideways grid");
  chunk_capacity = std::min(chunk_capacity, maximum_grid_candidates);
  if (chunk_capacity == 0) {
    throw std::invalid_argument("configuration produced an empty sideways chunk");
  }

  const std::size_t trace_chunk_bytes =
      checked_product(chunk_capacity, trace_length, "trace chunk");
  const std::size_t output_chunk_bytes =
      checked_product(chunk_capacity, horizon, "sideways output chunk");
  const std::size_t workspace_chunk_bytes = checked_product(
      chunk_capacity, workspace_bytes_per_candidate, "sideways workspace chunk");

  DeviceBuffer<std::uint8_t> device_traces;
  DeviceBuffer<std::uint8_t> device_results;
  DeviceBuffer<std::uint8_t> device_workspace;
  device_traces.allocate(trace_chunk_bytes);
  device_results.allocate(output_chunk_bytes);
  device_workspace.allocate(workspace_chunk_bytes);
  CudaEvent kernel_start;
  CudaEvent kernel_stop;

  local_stats.chunk_capacity = chunk_capacity;
  local_stats.workspace_bytes_per_candidate = workspace_bytes_per_candidate;
  local_stats.peak_device_bytes =
      checked_product(chunk_capacity, bytes_per_candidate,
                      "peak sideways device memory");
  local_stats.effective_device_budget_bytes = effective_budget;

  for (std::size_t offset = 0; offset < candidate_count;
       offset += chunk_capacity) {
    const std::size_t count =
        std::min(chunk_capacity, candidate_count - offset);
    const std::size_t input_bytes =
        checked_product(count, trace_length, "sideways input transfer");
    const std::size_t chunk_output_bytes =
        checked_product(count, horizon, "sideways result transfer");

    auto transfer_start = Clock::now();
    RULE30_SIDEWAYS_CUDA_CHECK(
        cudaMemcpy(device_traces.get(), traces.data() + offset * trace_length,
                   input_bytes, cudaMemcpyHostToDevice));
    local_stats.host_to_device_milliseconds +=
        elapsed_milliseconds(transfer_start, Clock::now());

    const std::size_t threads =
        static_cast<std::size_t>(config.threads_per_block);
    const std::size_t block_count =
        count / threads + static_cast<std::size_t>(count % threads != 0U);
    RULE30_SIDEWAYS_CUDA_CHECK(cudaEventRecord(kernel_start.get()));
    reconstruct_left_initial_kernel<<<static_cast<unsigned int>(block_count),
                                      config.threads_per_block>>>(
        device_traces.get(), device_results.get(), device_workspace.get(), count,
        trace_length, horizon, workspace_stride);
    RULE30_SIDEWAYS_CUDA_CHECK(cudaGetLastError());
    RULE30_SIDEWAYS_CUDA_CHECK(cudaEventRecord(kernel_stop.get()));
    // Report asynchronous launch and execution errors before accepting output.
    RULE30_SIDEWAYS_CUDA_CHECK(cudaEventSynchronize(kernel_stop.get()));
    float kernel_milliseconds = 0.0F;
    RULE30_SIDEWAYS_CUDA_CHECK(cudaEventElapsedTime(
        &kernel_milliseconds, kernel_start.get(), kernel_stop.get()));
    local_stats.kernel_milliseconds += kernel_milliseconds;

    transfer_start = Clock::now();
    RULE30_SIDEWAYS_CUDA_CHECK(cudaMemcpy(
        results.data() + offset * horizon, device_results.get(),
        chunk_output_bytes, cudaMemcpyDeviceToHost));
    local_stats.device_to_host_milliseconds +=
        elapsed_milliseconds(transfer_start, Clock::now());
    ++local_stats.chunks;
  }

  kernel_stop.close();
  kernel_start.close();
  device_workspace.release();
  device_results.release();
  device_traces.release();
  local_stats.end_to_end_milliseconds =
      elapsed_milliseconds(end_to_end_start, Clock::now());

  if (stats != nullptr) {
    *stats = local_stats;
  }
  return results;
}

}  // namespace rule30::cuda
