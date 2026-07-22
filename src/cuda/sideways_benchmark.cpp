#include "rule30_cuda/batch_period.hpp"
#include "rule30_cuda/batch_sideways.hpp"

#include <algorithm>
#include <chrono>
#include <cmath>
#include <cstddef>
#include <cstdint>
#include <cstdlib>
#include <exception>
#include <iomanip>
#include <iostream>
#include <limits>
#include <numeric>
#include <stdexcept>
#include <string>
#include <vector>

namespace {

using Clock = std::chrono::steady_clock;

constexpr std::uint64_t kFnvOffsetBasis = 0xcbf29ce484222325ULL;
constexpr std::uint64_t kFnvPrime = 1099511628211ULL;

struct Options {
  std::size_t candidate_count{4099};
  std::size_t horizon{63};
  std::size_t memory_budget_mib{64};
  std::size_t max_chunk_candidates{0};
  int repetitions{5};
  int threads_per_block{128};
  int device_index{0};
};

std::size_t parse_size(const char* value, const char* name) {
  const std::string text(value);
  if (text.empty() || text.front() == '-') {
    throw std::invalid_argument(std::string("invalid value for ") + name);
  }
  std::size_t consumed = 0;
  const unsigned long long parsed = std::stoull(text, &consumed);
  if (consumed != text.size() ||
      parsed > std::numeric_limits<std::size_t>::max()) {
    throw std::invalid_argument(std::string("invalid value for ") + name);
  }
  return static_cast<std::size_t>(parsed);
}

int parse_int(const char* value, const char* name) {
  const std::string text(value);
  std::size_t consumed = 0;
  const long parsed = std::stol(text, &consumed);
  if (consumed != text.size() || parsed < std::numeric_limits<int>::min() ||
      parsed > std::numeric_limits<int>::max()) {
    throw std::invalid_argument(std::string("invalid value for ") + name);
  }
  return static_cast<int>(parsed);
}

std::size_t mebibytes_to_bytes(std::size_t value) {
  constexpr std::size_t kBytesPerMebibyte = 1024ULL * 1024ULL;
  if (value > std::numeric_limits<std::size_t>::max() / kBytesPerMebibyte) {
    throw std::invalid_argument("--memory-budget-mib is too large");
  }
  return value * kBytesPerMebibyte;
}

Options parse_options(int argc, char** argv) {
  Options options;
  for (int index = 1; index < argc; index += 2) {
    if (index + 1 >= argc) {
      throw std::invalid_argument("every option requires a value");
    }
    const std::string option(argv[index]);
    if (option == "--candidates") {
      options.candidate_count =
          parse_size(argv[index + 1], "--candidates");
    } else if (option == "--horizon") {
      options.horizon = parse_size(argv[index + 1], "--horizon");
    } else if (option == "--memory-budget-mib") {
      options.memory_budget_mib =
          parse_size(argv[index + 1], "--memory-budget-mib");
    } else if (option == "--max-chunk-candidates") {
      options.max_chunk_candidates =
          parse_size(argv[index + 1], "--max-chunk-candidates");
    } else if (option == "--repetitions") {
      options.repetitions = parse_int(argv[index + 1], "--repetitions");
    } else if (option == "--threads") {
      options.threads_per_block = parse_int(argv[index + 1], "--threads");
    } else if (option == "--device") {
      options.device_index = parse_int(argv[index + 1], "--device");
    } else {
      throw std::invalid_argument("unknown option: " + option);
    }
  }
  if (options.candidate_count == 0 || options.horizon == 0 ||
      options.memory_budget_mib == 0 || options.repetitions <= 0 ||
      options.threads_per_block <= 0 || options.device_index < 0) {
    throw std::invalid_argument(
        "candidates, horizon, memory, repetitions, and threads must be positive");
  }
  if (options.horizon == std::numeric_limits<std::size_t>::max()) {
    throw std::invalid_argument("--horizon is too large");
  }
  return options;
}

std::uint64_t next_random(std::uint64_t& state) {
  state ^= state << 13U;
  state ^= state >> 7U;
  state ^= state << 17U;
  return state;
}

std::vector<std::uint8_t> make_traces(std::size_t candidate_count,
                                      std::size_t trace_length) {
  if (trace_length != 0 &&
      candidate_count >
          std::numeric_limits<std::size_t>::max() / trace_length) {
    throw std::invalid_argument("trace input size overflow");
  }
  std::uint64_t state = 0x4d595df4d0f33173ULL;
  std::vector<std::uint8_t> traces(candidate_count * trace_length);
  for (auto& bit : traces) {
    bit = static_cast<std::uint8_t>(next_random(state) & 1U);
  }
  return traces;
}

// Independent O(horizon)-workspace host oracle for the same finite mapping.
std::vector<std::uint8_t> reconstruct_cpu(
    const std::vector<std::uint8_t>& traces, std::size_t trace_length) {
  const std::size_t horizon = trace_length - 1U;
  const std::size_t candidate_count = traces.size() / trace_length;
  std::vector<std::uint8_t> output(candidate_count * horizon);
  const std::size_t stride = horizon + 2U;
  std::vector<std::uint8_t> first(stride);
  std::vector<std::uint8_t> second(stride);
  std::vector<std::uint8_t> third(stride);

  for (std::size_t candidate = 0; candidate < candidate_count; ++candidate) {
    std::fill(first.begin(), first.end(), 0U);
    std::fill(second.begin(), second.end(), 0U);
    std::fill(third.begin(), third.end(), 0U);
    const std::uint8_t* trace = traces.data() + candidate * trace_length;

    std::uint8_t* right_current = first.data();
    std::uint8_t* right_next = second.data();
    for (std::size_t time = 0; time <= horizon; ++time) {
      third[time] = right_current[1];
      if (time == horizon) {
        break;
      }
      right_current[0] = trace[time];
      for (std::size_t position = 1; position <= horizon; ++position) {
        right_next[position] = static_cast<std::uint8_t>(
            right_current[position - 1U] ^
            (right_current[position] | right_current[position + 1U]));
      }
      right_next[horizon + 1U] = 0U;
      std::swap(right_current, right_next);
    }

    std::copy_n(trace, trace_length, first.data());
    std::uint8_t* current = first.data();
    std::uint8_t* neighbor = third.data();
    std::uint8_t* scratch = second.data();
    for (std::size_t depth = 1; depth <= horizon; ++depth) {
      const std::size_t length = trace_length - depth;
      for (std::size_t time = 0; time < length; ++time) {
        scratch[time] = static_cast<std::uint8_t>(
            current[time + 1U] ^ (current[time] | neighbor[time]));
      }
      output[candidate * horizon + depth - 1U] = scratch[0];
      std::uint8_t* old_neighbor = neighbor;
      neighbor = current;
      current = scratch;
      scratch = old_neighbor;
    }
  }
  return output;
}

std::uint64_t hash_bytes(const std::vector<std::uint8_t>& values) {
  std::uint64_t hash = kFnvOffsetBasis;
  for (const std::uint8_t value : values) {
    hash ^= value;
    hash *= kFnvPrime;
  }
  return hash;
}

struct TimingSummary {
  double minimum{};
  double median{};
  double maximum{};
  double mean{};
  double standard_deviation{};
};

TimingSummary summarize_timings(std::vector<double> values) {
  std::sort(values.begin(), values.end());
  const std::size_t middle = values.size() / 2U;
  const double median =
      values.size() % 2U == 0U
          ? (values[middle - 1U] + values[middle]) / 2.0
          : values[middle];
  const double mean =
      std::accumulate(values.begin(), values.end(), 0.0) / values.size();
  const double squared_deviation =
      std::accumulate(values.begin(), values.end(), 0.0,
                      [mean](double sum, double value) {
                        const double difference = value - mean;
                        return sum + difference * difference;
                      });
  return {values.front(), median, values.back(), mean,
          std::sqrt(squared_deviation / values.size())};
}

void print_timing_summary(const char* name, const TimingSummary& summary,
                          bool trailing_comma) {
  std::cout << "  \"" << name << "\": {"
            << "\"minimum\": " << summary.minimum << ", "
            << "\"median\": " << summary.median << ", "
            << "\"maximum\": " << summary.maximum << ", "
            << "\"mean\": " << summary.mean << ", "
            << "\"standard_deviation\": " << summary.standard_deviation
            << '}' << (trailing_comma ? ",\n" : "\n");
}

std::string json_escape(const std::string& input) {
  std::string output;
  for (const char character : input) {
    if (character == '\\' || character == '"') {
      output.push_back('\\');
    }
    output.push_back(character);
  }
  return output;
}

}  // namespace

int main(int argc, char** argv) {
  try {
    const Options options = parse_options(argc, argv);
    const std::size_t trace_length = options.horizon + 1U;
    const auto traces = make_traces(options.candidate_count, trace_length);
    const auto device = rule30::cuda::probe_device(options.device_index);

    const auto cpu_warmup = reconstruct_cpu(traces, trace_length);
    rule30::cuda::SidewaysBatchConfig config{};
    config.device_index = options.device_index;
    config.threads_per_block = options.threads_per_block;
    config.device_memory_budget_bytes =
        mebibytes_to_bytes(options.memory_budget_mib);
    config.max_chunk_candidates = options.max_chunk_candidates;
    config.max_horizon = options.horizon;
    const auto gpu_warmup = rule30::cuda::reconstruct_left_initial_batch(
        traces, trace_length, config);
    if (gpu_warmup != cpu_warmup) {
      throw std::runtime_error(
          "GPU warm-up result disagrees with the independent CPU oracle");
    }

    std::vector<double> cpu_times;
    std::vector<double> host_to_device_times;
    std::vector<double> kernel_times;
    std::vector<double> device_to_host_times;
    std::vector<double> transfer_times;
    std::vector<double> end_to_end_times;
    for (int repetition = 0; repetition < options.repetitions; ++repetition) {
      const auto start = Clock::now();
      const auto measured = reconstruct_cpu(traces, trace_length);
      cpu_times.push_back(
          std::chrono::duration<double, std::milli>(Clock::now() - start)
              .count());
      if (measured != cpu_warmup) {
        throw std::runtime_error("CPU sideways oracle was nondeterministic");
      }
    }

    rule30::cuda::SidewaysBatchStats final_stats{};
    for (int repetition = 0; repetition < options.repetitions; ++repetition) {
      const auto measured = rule30::cuda::reconstruct_left_initial_batch(
          traces, trace_length, config, &final_stats);
      if (measured != cpu_warmup) {
        throw std::runtime_error(
            "measured GPU result disagrees with the independent CPU oracle");
      }
      host_to_device_times.push_back(
          final_stats.host_to_device_milliseconds);
      kernel_times.push_back(final_stats.kernel_milliseconds);
      device_to_host_times.push_back(
          final_stats.device_to_host_milliseconds);
      transfer_times.push_back(final_stats.host_to_device_milliseconds +
                               final_stats.device_to_host_milliseconds);
      end_to_end_times.push_back(final_stats.end_to_end_milliseconds);
    }

    const auto cpu_timing = summarize_timings(cpu_times);
    const auto host_to_device_timing =
        summarize_timings(host_to_device_times);
    const auto kernel_timing = summarize_timings(kernel_times);
    const auto device_to_host_timing =
        summarize_timings(device_to_host_times);
    const auto transfer_timing = summarize_timings(transfer_times);
    const auto end_to_end_timing = summarize_timings(end_to_end_times);
    const double ratio = cpu_timing.median / end_to_end_timing.median;
    const std::size_t ones = static_cast<std::size_t>(
        std::count(cpu_warmup.begin(), cpu_warmup.end(), 1U));

    std::cout << std::fixed << std::setprecision(6)
              << "{\n"
              << "  \"workload\": \"bounded-batch-sideways-reconstruction\",\n"
              << "  \"interpretation\": \"exact finite reconstruction; no "
                 "eventual-periodicity inference\",\n"
              << "  \"device\": \"" << json_escape(device.name) << "\",\n"
              << "  \"compute_capability\": \"" << device.compute_major << '.'
              << device.compute_minor << "\",\n"
              << "  \"sass_architecture\": \"sm_75\",\n"
              << "  \"candidate_count\": " << options.candidate_count
              << ",\n"
              << "  \"trace_length\": " << trace_length << ",\n"
              << "  \"horizon\": " << options.horizon << ",\n"
              << "  \"result_bytes\": " << cpu_warmup.size() << ",\n"
              << "  \"result_ones\": " << ones << ",\n"
              << "  \"result_zeros\": " << cpu_warmup.size() - ones
              << ",\n"
              << "  \"result_hash_fnv1a64\": \"" << std::hex
              << std::setw(16) << std::setfill('0') << hash_bytes(cpu_warmup)
              << std::dec << std::setfill(' ') << "\",\n"
              << "  \"cpu_gpu_exact_match\": true,\n"
              << "  \"chunks_per_run\": " << final_stats.chunks << ",\n"
              << "  \"chunk_capacity\": " << final_stats.chunk_capacity
              << ",\n"
              << "  \"workspace_bytes_per_candidate\": "
              << final_stats.workspace_bytes_per_candidate << ",\n"
              << "  \"peak_device_bytes\": "
              << final_stats.peak_device_bytes << ",\n"
              << "  \"cpu_warmup_runs\": 1,\n"
              << "  \"gpu_warmup_runs\": 1,\n"
              << "  \"measured_repetitions\": " << options.repetitions
              << ",\n"
              << "  \"median_cpu_to_cuda_end_to_end_ratio\": " << ratio
              << ",\n"
              << "  \"cuda_end_to_end_median_is_lower\": "
              << (end_to_end_timing.median < cpu_timing.median ? "true" : "false")
              << ",\n";
    print_timing_summary("cpu_oracle_milliseconds", cpu_timing, true);
    print_timing_summary("host_to_device_milliseconds",
                         host_to_device_timing, true);
    print_timing_summary("kernel_milliseconds", kernel_timing, true);
    print_timing_summary("device_to_host_milliseconds",
                         device_to_host_timing, true);
    print_timing_summary("total_transfer_milliseconds", transfer_timing, true);
    print_timing_summary("cuda_end_to_end_milliseconds", end_to_end_timing,
                         false);
    std::cout << "}\n";
    return EXIT_SUCCESS;
  } catch (const std::exception& error) {
    std::cerr << "CUDA sideways benchmark failed: " << error.what() << '\n';
    return EXIT_FAILURE;
  }
}
