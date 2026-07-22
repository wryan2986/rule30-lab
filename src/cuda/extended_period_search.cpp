#include "rule30_cuda/batch_period.hpp"
#include "rule30_cuda/batch_sideways.hpp"

#include <algorithm>
#include <array>
#include <charconv>
#include <chrono>
#include <cstddef>
#include <cstdint>
#include <cstdlib>
#include <iomanip>
#include <iostream>
#include <limits>
#include <optional>
#include <sstream>
#include <span>
#include <stdexcept>
#include <string>
#include <string_view>
#include <utility>
#include <vector>

namespace rule30::cuda::extended_period_search {
namespace {

using Clock = std::chrono::steady_clock;
constexpr std::size_t kMaximumHorizon = 512;
constexpr std::size_t kMaximumTraceWords =
    (kMaximumHorizon + 1U + 63U) / 64U;

[[nodiscard]] std::size_t checked_add(std::size_t left, std::size_t right,
                                      std::string_view description) {
  if (left > std::numeric_limits<std::size_t>::max() - right) {
    throw std::overflow_error(std::string(description) + " overflow");
  }
  return left + right;
}

[[nodiscard]] std::size_t checked_product(std::size_t left, std::size_t right,
                                          std::string_view description) {
  if (right != 0U && left > std::numeric_limits<std::size_t>::max() / right) {
    throw std::overflow_error(std::string(description) + " overflow");
  }
  return left * right;
}

[[nodiscard]] std::uint64_t checked_add_u64(std::uint64_t left,
                                            std::uint64_t right,
                                            std::string_view description) {
  if (left > std::numeric_limits<std::uint64_t>::max() - right) {
    throw std::overflow_error(std::string(description) + " overflow");
  }
  return left + right;
}

[[nodiscard]] double elapsed_milliseconds(Clock::time_point start,
                                           Clock::time_point end) {
  return std::chrono::duration<double, std::milli>(end - start).count();
}

struct PackedTraceRecord {
  std::array<std::uint64_t, kMaximumTraceWords> words{};
  std::uint64_t code{};
  std::uint64_t multiplicity{1};
  std::uint16_t preperiod{};
  std::uint16_t period{};
};

[[nodiscard]] bool same_trace(const PackedTraceRecord& left,
                              const PackedTraceRecord& right) {
  return left.words == right.words;
}

[[nodiscard]] bool record_less(const PackedTraceRecord& left,
                               const PackedTraceRecord& right) {
  if (left.words != right.words) {
    return left.words < right.words;
  }
  if (left.preperiod != right.preperiod) {
    return left.preperiod < right.preperiod;
  }
  if (left.period != right.period) {
    return left.period < right.period;
  }
  return left.code < right.code;
}

[[nodiscard]] std::uint8_t description_bit(std::uint64_t code,
                                           std::size_t preperiod,
                                           std::size_t period,
                                           std::size_t time) {
  const std::size_t index =
      time < preperiod ? time : preperiod + (time - preperiod) % period;
  return static_cast<std::uint8_t>((code >> index) & 1ULL);
}

[[nodiscard]] PackedTraceRecord make_record(std::size_t preperiod,
                                            std::size_t period,
                                            std::size_t horizon,
                                            std::uint64_t code) {
  PackedTraceRecord record{};
  record.preperiod = static_cast<std::uint16_t>(preperiod);
  record.period = static_cast<std::uint16_t>(period);
  record.code = code;
  for (std::size_t time = 0; time <= horizon; ++time) {
    if (description_bit(code, preperiod, period, time) != 0U) {
      record.words[time / 64U] |= 1ULL << (time % 64U);
    }
  }
  return record;
}

void unpack_trace(const PackedTraceRecord& record, std::size_t trace_length,
                  std::span<std::uint8_t> destination) {
  if (destination.size() != trace_length) {
    throw std::logic_error("unpack destination has the wrong length");
  }
  for (std::size_t time = 0; time < trace_length; ++time) {
    destination[time] = static_cast<std::uint8_t>(
        (record.words[time / 64U] >> (time % 64U)) & 1ULL);
  }
}

[[nodiscard]] std::vector<std::uint8_t> reconstruct_cpu(
    std::span<const std::uint8_t> trace) {
  if (trace.empty()) {
    throw std::invalid_argument("CPU oracle trace must be nonempty");
  }
  const std::size_t horizon = trace.size() - 1U;
  std::vector<std::uint8_t> first(horizon + 2U, 0U);
  std::vector<std::uint8_t> second(horizon + 2U, 0U);
  std::vector<std::uint8_t> right_neighbor(horizon + 1U, 0U);

  auto* right_current = &first;
  auto* right_next = &second;
  for (std::size_t time = 0; time <= horizon; ++time) {
    right_neighbor[time] = (*right_current)[1];
    if (time == horizon) {
      break;
    }
    (*right_current)[0] = trace[time];
    for (std::size_t position = 1; position <= horizon; ++position) {
      (*right_next)[position] = static_cast<std::uint8_t>(
          (*right_current)[position - 1U] ^
          ((*right_current)[position] | (*right_current)[position + 1U]));
    }
    (*right_next)[horizon + 1U] = 0U;
    std::swap(right_current, right_next);
  }

  std::vector<std::uint8_t> current(trace.begin(), trace.end());
  std::vector<std::uint8_t> neighbor = std::move(right_neighbor);
  std::vector<std::uint8_t> scratch(horizon + 1U, 0U);
  std::vector<std::uint8_t> reconstructed(horizon, 0U);
  for (std::size_t depth = 1; depth <= horizon; ++depth) {
    const std::size_t length = trace.size() - depth;
    for (std::size_t time = 0; time < length; ++time) {
      scratch[time] = static_cast<std::uint8_t>(
          current[time + 1U] ^ (current[time] | neighbor[time]));
    }
    reconstructed[depth - 1U] = scratch[0];
    neighbor.assign(current.begin(), current.begin() + length);
    current.assign(scratch.begin(), scratch.begin() + length);
  }
  return reconstructed;
}

void verify_period_cpu(std::span<const std::uint8_t> trace,
                       std::size_t preperiod, std::size_t period) {
  for (std::size_t time = preperiod + period; time < trace.size(); ++time) {
    if (trace[time] != trace[time - period]) {
      throw std::logic_error("generated trace violates its own description");
    }
  }
}

[[nodiscard]] std::optional<std::size_t> first_nonzero(
    std::span<const std::uint8_t> reconstructed) {
  const auto found = std::find(reconstructed.begin(), reconstructed.end(), 1U);
  if (found == reconstructed.end()) {
    return std::nullopt;
  }
  return static_cast<std::size_t>(found - reconstructed.begin()) + 1U;
}

[[nodiscard]] std::string json_escape(std::string_view value) {
  std::ostringstream out;
  for (const unsigned char character : value) {
    switch (character) {
      case '\"':
        out << "\\\"";
        break;
      case '\\':
        out << "\\\\";
        break;
      case '\b':
        out << "\\b";
        break;
      case '\f':
        out << "\\f";
        break;
      case '\n':
        out << "\\n";
        break;
      case '\r':
        out << "\\r";
        break;
      case '\t':
        out << "\\t";
        break;
      default:
        if (character < 0x20U) {
          out << "\\u" << std::hex << std::setw(4) << std::setfill('0')
              << static_cast<unsigned int>(character) << std::dec;
        } else {
          out << static_cast<char>(character);
        }
    }
  }
  return out.str();
}

}  // namespace

enum class Backend { kCpu, kCuda };

struct SearchConfig {
  std::size_t minimum_preperiod{0};
  std::size_t maximum_preperiod{4};
  std::size_t minimum_period{1};
  std::size_t maximum_period{8};
  std::size_t horizon{64};
  std::size_t maximum_evaluation_chunk{256};
  std::size_t host_memory_budget_bytes{256ULL * 1024ULL * 1024ULL};
  std::size_t device_memory_budget_bytes{128ULL * 1024ULL * 1024ULL};
  std::size_t maximum_output_bytes{4ULL * 1024ULL * 1024ULL};
  std::size_t maximum_witnesses{32};
  int device_index{0};
  int threads_per_block{128};
  Backend backend{Backend::kCuda};
};

struct Description {
  std::size_t preperiod{};
  std::size_t period{};
  std::uint64_t code{};
};

struct Witness {
  Description canonical_description{};
  std::size_t first_nonzero_left_depth{};
  std::uint64_t represented_descriptions{};
};

struct DepthCount {
  std::size_t depth{};
  std::uint64_t distinct_traces{};
  std::uint64_t descriptions{};
};

struct SearchStats {
  std::uint64_t parameter_pairs{};
  std::uint64_t descriptions_total{};
  std::uint64_t descriptions_rejected_c0{};
  std::uint64_t descriptions_seed_compatible{};
  std::uint64_t distinct_trace_sequences{};
  std::uint64_t duplicate_descriptions{};
  std::uint64_t traces_evaluated{};
  std::uint64_t finite_compatible_traces{};
  std::uint64_t finite_incompatible_traces{};
  std::uint64_t finite_compatible_descriptions{};
  std::uint64_t finite_incompatible_descriptions{};
  std::size_t evaluation_chunks{};
  std::size_t peak_host_bytes_accounted{};
  std::size_t peak_device_bytes{};
  double generation_and_dedup_milliseconds{};
  double period_kernel_milliseconds{};
  double sideways_kernel_milliseconds{};
  double period_end_to_end_milliseconds{};
  double sideways_end_to_end_milliseconds{};
  double search_end_to_end_milliseconds{};
};

struct SearchResult {
  SearchConfig config{};
  SearchStats stats{};
  std::vector<DepthCount> first_nonzero_histogram;
  std::vector<Witness> witnesses;
  std::string cuda_device_name;
  int cuda_compute_major{};
  int cuda_compute_minor{};
};

namespace {

void validate_config(const SearchConfig& config) {
  if (config.minimum_preperiod > config.maximum_preperiod) {
    throw std::invalid_argument(
        "minimum_preperiod cannot exceed maximum_preperiod");
  }
  if (config.minimum_period == 0U ||
      config.minimum_period > config.maximum_period) {
    throw std::invalid_argument("period bounds must be positive and ordered");
  }
  if (config.maximum_preperiod > kMaximumHorizon ||
      config.maximum_period > kMaximumHorizon ||
      config.horizon > kMaximumHorizon) {
    throw std::invalid_argument("preperiod, period, and horizon are capped at 512");
  }
  if (config.maximum_preperiod + config.maximum_period > config.horizon) {
    throw std::invalid_argument(
        "horizon must be at least maximum_preperiod + maximum_period");
  }
  if (config.maximum_preperiod + config.maximum_period > 63U) {
    throw std::invalid_argument(
        "description bit count is capped at 63 for exact enumeration");
  }
  if (config.maximum_evaluation_chunk == 0U) {
    throw std::invalid_argument("maximum_evaluation_chunk must be positive");
  }
  if (config.host_memory_budget_bytes == 0U ||
      config.device_memory_budget_bytes == 0U ||
      config.maximum_output_bytes == 0U) {
    throw std::invalid_argument("memory and output budgets must be positive");
  }
  if (config.device_index < 0 || config.threads_per_block <= 0) {
    throw std::invalid_argument(
        "device index must be nonnegative and threads must be positive");
  }
}

struct CoverageTotals {
  std::uint64_t parameter_pairs{};
  std::uint64_t descriptions_total{};
  std::uint64_t seed_compatible{};
};

[[nodiscard]] CoverageTotals coverage_totals(const SearchConfig& config) {
  CoverageTotals totals{};
  for (std::size_t preperiod = config.minimum_preperiod;
       preperiod <= config.maximum_preperiod; ++preperiod) {
    for (std::size_t period = config.minimum_period;
         period <= config.maximum_period; ++period) {
      const std::size_t width = preperiod + period;
      const std::uint64_t descriptions = 1ULL << width;
      totals.parameter_pairs = checked_add_u64(
          totals.parameter_pairs, 1U, "parameter-pair count");
      totals.descriptions_total = checked_add_u64(
          totals.descriptions_total, descriptions, "description count");
      totals.seed_compatible = checked_add_u64(
          totals.seed_compatible, descriptions / 2U,
          "seed-compatible description count");
    }
  }
  return totals;
}

[[nodiscard]] std::size_t select_chunk_capacity(const SearchConfig& config,
                                                std::size_t fixed_host_bytes) {
  const std::size_t trace_length = config.horizon + 1U;
  const std::size_t per_candidate = checked_add(
      checked_add(trace_length, config.horizon,
                  "chunk trace and reconstruction bytes"),
      sizeof(PeriodCandidate) + sizeof(PeriodResult),
      "chunk period metadata bytes");
  if (fixed_host_bytes >= config.host_memory_budget_bytes ||
      config.host_memory_budget_bytes - fixed_host_bytes < per_candidate) {
    throw std::invalid_argument(
        "host memory budget cannot hold records and one evaluation candidate");
  }
  std::size_t capacity =
      (config.host_memory_budget_bytes - fixed_host_bytes) / per_candidate;
  capacity = std::min(capacity, config.maximum_evaluation_chunk);
  const std::size_t output_item_bytes =
      std::max(config.horizon, sizeof(PeriodResult));
  capacity = std::min(capacity,
                      config.maximum_output_bytes / output_item_bytes);
  if (capacity == 0U) {
    throw std::invalid_argument(
        "output budget cannot hold one compact evaluation result");
  }
  return capacity;
}

[[nodiscard]] std::size_t fixed_host_bytes(const SearchConfig& config,
                                           std::size_t record_bytes) {
  const std::size_t depth_slots = config.horizon + 1U;
  std::size_t report_workspace = checked_product(
      depth_slots, sizeof(DepthCount) + sizeof(std::optional<Witness>),
      "report workspace");
  report_workspace = checked_add(
      report_workspace,
      checked_product(config.horizon, sizeof(DepthCount),
                      "compact histogram storage"),
      "report workspace");
  report_workspace = checked_add(
      report_workspace,
      checked_product(std::min(config.maximum_witnesses, config.horizon),
                      sizeof(Witness), "compact witness storage"),
      "report workspace");

  // The CPU implementation evaluates one trace at a time using seven linear
  // byte buffers. Eight times (horizon+2) is a conservative explicit-buffer
  // bound. CUDA mode does not allocate these CPU oracle buffers.
  const std::size_t cpu_scratch =
      config.backend == Backend::kCpu
          ? checked_product(8U, config.horizon + 2U, "CPU oracle scratch")
          : 0U;
  return checked_add(checked_add(record_bytes, report_workspace,
                                 "fixed host allocation accounting"),
                     cpu_scratch, "fixed host allocation accounting");
}

[[nodiscard]] std::vector<PackedTraceRecord> enumerate_unique_records(
    const SearchConfig& config, const CoverageTotals& totals) {
  if (totals.seed_compatible >
      std::numeric_limits<std::size_t>::max() / sizeof(PackedTraceRecord)) {
    throw std::invalid_argument("description set exceeds addressable memory");
  }
  const std::size_t record_bytes = checked_product(
      static_cast<std::size_t>(totals.seed_compatible),
      sizeof(PackedTraceRecord), "description records");
  if (record_bytes >= config.host_memory_budget_bytes) {
    throw std::invalid_argument(
        "description records exceed the host memory budget");
  }

  std::vector<PackedTraceRecord> records;
  records.reserve(static_cast<std::size_t>(totals.seed_compatible));
  for (std::size_t preperiod = config.minimum_preperiod;
       preperiod <= config.maximum_preperiod; ++preperiod) {
    for (std::size_t period = config.minimum_period;
         period <= config.maximum_period; ++period) {
      const std::uint64_t description_count = 1ULL << (preperiod + period);
      // Bit zero is c_0 for every description convention used here. Enumerate
      // only odd codes while accounting for the rejected even codes exactly.
      for (std::uint64_t code = 1U; code < description_count; code += 2U) {
        records.push_back(make_record(preperiod, period, config.horizon, code));
      }
    }
  }
  if (records.size() != totals.seed_compatible) {
    throw std::logic_error("seed-compatible enumeration coverage mismatch");
  }

  std::sort(records.begin(), records.end(), record_less);
  std::size_t unique_count = 0U;
  for (std::size_t begin = 0; begin < records.size();) {
    std::size_t end = begin + 1U;
    while (end < records.size() && same_trace(records[begin], records[end])) {
      ++end;
    }
    PackedTraceRecord representative = records[begin];
    representative.multiplicity = static_cast<std::uint64_t>(end - begin);
    records[unique_count++] = representative;
    begin = end;
  }
  records.resize(unique_count);
  return records;
}

void account_chunk_results(
    std::span<const PackedTraceRecord> records,
    std::span<const std::uint8_t> reconstructed, std::size_t horizon,
    std::vector<DepthCount>& histogram,
    std::vector<std::optional<Witness>>& witness_by_depth, SearchResult& result) {
  if (reconstructed.size() != records.size() * horizon) {
    throw std::logic_error("reconstruction result size mismatch");
  }
  for (std::size_t index = 0; index < records.size(); ++index) {
    const auto tail = reconstructed.subspan(index * horizon, horizon);
    const auto depth = first_nonzero(tail);
    const auto multiplicity = records[index].multiplicity;
    if (!depth.has_value()) {
      ++result.stats.finite_compatible_traces;
      result.stats.finite_compatible_descriptions = checked_add_u64(
          result.stats.finite_compatible_descriptions, multiplicity,
          "finite-compatible descriptions");
      continue;
    }

    ++result.stats.finite_incompatible_traces;
    result.stats.finite_incompatible_descriptions = checked_add_u64(
        result.stats.finite_incompatible_descriptions, multiplicity,
        "finite-incompatible descriptions");
    auto& bin = histogram.at(*depth);
    ++bin.distinct_traces;
    bin.descriptions = checked_add_u64(bin.descriptions, multiplicity,
                                       "witness histogram descriptions");
    if (!witness_by_depth[*depth].has_value()) {
      witness_by_depth[*depth] = Witness{
          {records[index].preperiod, records[index].period,
           records[index].code},
          *depth, multiplicity};
    }
  }
}

[[nodiscard]] std::vector<std::uint8_t> evaluate_cpu_chunk(
    std::span<const PackedTraceRecord> records, std::size_t trace_length) {
  const std::size_t horizon = trace_length - 1U;
  std::vector<std::uint8_t> traces(records.size() * trace_length);
  std::vector<std::uint8_t> reconstructed(records.size() * horizon);
  for (std::size_t index = 0; index < records.size(); ++index) {
    auto trace = std::span<std::uint8_t>(traces).subspan(index * trace_length,
                                                        trace_length);
    unpack_trace(records[index], trace_length, trace);
    verify_period_cpu(trace, records[index].preperiod, records[index].period);
    const auto one = reconstruct_cpu(trace);
    std::copy(one.begin(), one.end(),
              reconstructed.begin() + static_cast<std::ptrdiff_t>(index * horizon));
  }
  return reconstructed;
}

[[nodiscard]] std::vector<std::uint8_t> evaluate_cuda_chunk(
    std::span<const PackedTraceRecord> records, const SearchConfig& config,
    SearchResult& result) {
  const std::size_t trace_length = config.horizon + 1U;
  std::vector<std::uint8_t> traces(records.size() * trace_length);
  std::vector<PeriodCandidate> candidates;
  candidates.reserve(records.size());
  for (std::size_t index = 0; index < records.size(); ++index) {
    auto trace = std::span<std::uint8_t>(traces).subspan(index * trace_length,
                                                        trace_length);
    unpack_trace(records[index], trace_length, trace);
    const std::size_t base = index * trace_length;
    candidates.push_back(
        {base + records[index].preperiod + records[index].period,
         base + trace_length, records[index].period});
  }

  BatchConfig period_config{};
  period_config.device_index = config.device_index;
  period_config.threads_per_block = config.threads_per_block;
  period_config.device_memory_budget_bytes = config.device_memory_budget_bytes;
  period_config.max_chunk_candidates = config.maximum_evaluation_chunk;
  period_config.max_output_bytes = config.maximum_output_bytes;
  BatchStats period_stats{};
  const auto period_results =
      evaluate_period_candidates(traces, candidates, period_config, &period_stats);
  if (period_results.size() != records.size()) {
    throw std::logic_error("CUDA period validation result size mismatch");
  }
  for (std::size_t index = 0; index < records.size(); ++index) {
    const std::uint64_t expected_comparisons =
        trace_length - records[index].preperiod - records[index].period;
    if (period_results[index].matches == 0U ||
        period_results[index].first_mismatch != kNoMismatch ||
        period_results[index].comparisons_checked != expected_comparisons) {
      throw std::runtime_error(
          "CUDA period kernel rejected a generated description");
    }
  }
  result.stats.period_kernel_milliseconds += period_stats.kernel_milliseconds;
  result.stats.period_end_to_end_milliseconds +=
      period_stats.end_to_end_milliseconds;
  result.stats.peak_device_bytes =
      std::max(result.stats.peak_device_bytes, period_stats.peak_device_bytes);

  SidewaysBatchConfig sideways_config{};
  sideways_config.device_index = config.device_index;
  sideways_config.threads_per_block = config.threads_per_block;
  sideways_config.device_memory_budget_bytes =
      config.device_memory_budget_bytes;
  sideways_config.max_chunk_candidates = config.maximum_evaluation_chunk;
  sideways_config.max_output_bytes = config.maximum_output_bytes;
  sideways_config.max_horizon = config.horizon;
  SidewaysBatchStats sideways_stats{};
  auto reconstructed = reconstruct_left_initial_batch(
      traces, trace_length, sideways_config, &sideways_stats);
  result.stats.sideways_kernel_milliseconds +=
      sideways_stats.kernel_milliseconds;
  result.stats.sideways_end_to_end_milliseconds +=
      sideways_stats.end_to_end_milliseconds;
  result.stats.peak_device_bytes =
      std::max(result.stats.peak_device_bytes, sideways_stats.peak_device_bytes);
  return reconstructed;
}

}  // namespace

[[nodiscard]] SearchResult run_search(const SearchConfig& config) {
  validate_config(config);
  const auto search_start = Clock::now();
  const auto totals = coverage_totals(config);
  const std::size_t record_bytes = checked_product(
      static_cast<std::size_t>(totals.seed_compatible),
      sizeof(PackedTraceRecord), "description records");
  const std::size_t fixed_bytes = fixed_host_bytes(config, record_bytes);
  const std::size_t chunk_capacity =
      select_chunk_capacity(config, fixed_bytes);

  SearchResult result{};
  result.config = config;
  result.stats.parameter_pairs = totals.parameter_pairs;
  result.stats.descriptions_total = totals.descriptions_total;
  result.stats.descriptions_seed_compatible = totals.seed_compatible;
  result.stats.descriptions_rejected_c0 =
      totals.descriptions_total - totals.seed_compatible;

  const auto generation_start = Clock::now();
  auto records = enumerate_unique_records(config, totals);
  result.stats.generation_and_dedup_milliseconds =
      elapsed_milliseconds(generation_start, Clock::now());
  result.stats.distinct_trace_sequences = records.size();
  result.stats.duplicate_descriptions =
      totals.seed_compatible - static_cast<std::uint64_t>(records.size());

  const std::size_t trace_length = config.horizon + 1U;
  const std::size_t per_candidate_bytes = checked_add(
      checked_add(trace_length, config.horizon,
                  "accounted trace and reconstruction bytes"),
      sizeof(PeriodCandidate) + sizeof(PeriodResult),
      "accounted period metadata bytes");
  result.stats.peak_host_bytes_accounted = checked_add(
      fixed_bytes,
      checked_product(chunk_capacity, per_candidate_bytes,
                      "accounted chunk bytes"),
      "accounted peak host bytes");

  if (config.backend == Backend::kCuda) {
    const auto device = probe_device(config.device_index);
    result.cuda_device_name = device.name;
    result.cuda_compute_major = device.compute_major;
    result.cuda_compute_minor = device.compute_minor;
  }

  std::vector<DepthCount> histogram(config.horizon + 1U);
  for (std::size_t depth = 1; depth <= config.horizon; ++depth) {
    histogram[depth].depth = depth;
  }
  std::vector<std::optional<Witness>> witness_by_depth(config.horizon + 1U);

  for (std::size_t offset = 0; offset < records.size();
       offset += chunk_capacity) {
    const std::size_t count = std::min(chunk_capacity, records.size() - offset);
    const auto chunk = std::span<const PackedTraceRecord>(records).subspan(
        offset, count);
    std::vector<std::uint8_t> reconstructed;
    if (config.backend == Backend::kCpu) {
      reconstructed = evaluate_cpu_chunk(chunk, trace_length);
    } else {
      reconstructed = evaluate_cuda_chunk(chunk, config, result);
    }
    account_chunk_results(chunk, reconstructed, config.horizon, histogram,
                          witness_by_depth, result);
    result.stats.traces_evaluated = checked_add_u64(
        result.stats.traces_evaluated, count, "evaluated trace count");
    ++result.stats.evaluation_chunks;
  }

  for (std::size_t depth = 1; depth <= config.horizon; ++depth) {
    if (histogram[depth].distinct_traces != 0U) {
      result.first_nonzero_histogram.push_back(histogram[depth]);
    }
    if (witness_by_depth[depth].has_value() &&
        result.witnesses.size() < config.maximum_witnesses) {
      result.witnesses.push_back(*witness_by_depth[depth]);
    }
  }

  if (result.stats.traces_evaluated !=
          result.stats.distinct_trace_sequences ||
      result.stats.finite_compatible_traces +
              result.stats.finite_incompatible_traces !=
          result.stats.distinct_trace_sequences ||
      result.stats.finite_compatible_descriptions +
              result.stats.finite_incompatible_descriptions !=
          result.stats.descriptions_seed_compatible) {
    throw std::logic_error("final exact coverage accounting mismatch");
  }
  result.stats.search_end_to_end_milliseconds =
      elapsed_milliseconds(search_start, Clock::now());
  return result;
}

[[nodiscard]] std::string result_json(const SearchResult& result) {
  const auto& config = result.config;
  const auto& stats = result.stats;
  std::ostringstream out;
  out << std::setprecision(9);
  out << "{\n"
      << "  \"schema_version\": 1,\n"
      << "  \"status\": \"finite-exhaustive\",\n"
      << "  \"claim_scope\": \"configured descriptions and finite reconstruction horizon only\",\n"
      << "  \"backend\": \""
      << (config.backend == Backend::kCpu ? "cpu-oracle" : "cuda-sm75")
      << "\",\n"
      << "  \"parameters\": {\"minimum_preperiod\": "
      << config.minimum_preperiod << ", \"maximum_preperiod\": "
      << config.maximum_preperiod << ", \"minimum_period\": "
      << config.minimum_period << ", \"maximum_period\": "
      << config.maximum_period << ", \"horizon\": " << config.horizon
      << ", \"maximum_evaluation_chunk\": "
      << config.maximum_evaluation_chunk << ", \"threads_per_block\": "
      << config.threads_per_block << "},\n"
      << "  \"limits\": {\"host_memory_budget_bytes\": "
      << config.host_memory_budget_bytes
      << ", \"device_memory_budget_bytes\": "
      << config.device_memory_budget_bytes
      << ", \"maximum_output_bytes\": " << config.maximum_output_bytes
      << ", \"maximum_witnesses\": " << config.maximum_witnesses << "},\n"
      << "  \"coverage\": {\"parameter_pairs\": " << stats.parameter_pairs
      << ", \"descriptions_total\": " << stats.descriptions_total
      << ", \"descriptions_rejected_c0\": "
      << stats.descriptions_rejected_c0
      << ", \"descriptions_seed_compatible\": "
      << stats.descriptions_seed_compatible
      << ", \"distinct_trace_sequences\": "
      << stats.distinct_trace_sequences << ", \"duplicate_descriptions\": "
      << stats.duplicate_descriptions << ", \"traces_evaluated\": "
      << stats.traces_evaluated << ", \"evaluation_chunks\": "
      << stats.evaluation_chunks << "},\n"
      << "  \"finite_results\": {\"compatible_distinct_traces\": "
      << stats.finite_compatible_traces
      << ", \"incompatible_distinct_traces\": "
      << stats.finite_incompatible_traces
      << ", \"compatible_descriptions\": "
      << stats.finite_compatible_descriptions
      << ", \"incompatible_descriptions\": "
      << stats.finite_incompatible_descriptions << "},\n"
      << "  \"timings_milliseconds\": {\"generation_and_dedup\": "
      << stats.generation_and_dedup_milliseconds
      << ", \"period_kernel\": " << stats.period_kernel_milliseconds
      << ", \"sideways_kernel\": " << stats.sideways_kernel_milliseconds
      << ", \"period_end_to_end\": "
      << stats.period_end_to_end_milliseconds
      << ", \"sideways_end_to_end\": "
      << stats.sideways_end_to_end_milliseconds
      << ", \"search_end_to_end\": "
      << stats.search_end_to_end_milliseconds << "},\n"
      << "  \"resource_accounting\": {\"peak_host_bytes_accounted\": "
      << stats.peak_host_bytes_accounted << ", \"peak_device_bytes\": "
      << stats.peak_device_bytes << "},\n";
  if (config.backend == Backend::kCuda) {
    out << "  \"device\": {\"name\": \""
        << json_escape(result.cuda_device_name) << "\", \"compute_capability\": \""
        << result.cuda_compute_major << '.' << result.cuda_compute_minor
        << "\"},\n";
  } else {
    out << "  \"device\": null,\n";
  }

  out << "  \"first_nonzero_histogram\": [";
  for (std::size_t index = 0; index < result.first_nonzero_histogram.size();
       ++index) {
    const auto& bin = result.first_nonzero_histogram[index];
    if (index != 0U) {
      out << ',';
    }
    out << "{\"depth\":" << bin.depth << ",\"distinct_traces\":"
        << bin.distinct_traces << ",\"descriptions\":" << bin.descriptions
        << '}';
  }
  out << "],\n  \"witnesses\": [";
  for (std::size_t index = 0; index < result.witnesses.size(); ++index) {
    const auto& witness = result.witnesses[index];
    if (index != 0U) {
      out << ',';
    }
    out << "{\"preperiod\":" << witness.canonical_description.preperiod
        << ",\"period\":" << witness.canonical_description.period
        << ",\"description_code_hex\":\"0x" << std::hex
        << witness.canonical_description.code << std::dec
        << "\",\"first_nonzero_left_depth\":"
        << witness.first_nonzero_left_depth
        << ",\"represented_descriptions\":"
        << witness.represented_descriptions << '}';
  }
  out << "],\n"
      << "  \"interpretation\": \"Every listed incompatibility is an exact finite sideways-reconstruction witness. Surviving finite traces and excluded finite traces imply nothing by themselves about all horizons or eventual nonperiodicity.\"\n"
      << "}\n";
  const std::string json = out.str();
  if (json.size() > config.maximum_output_bytes) {
    throw std::invalid_argument("JSON report exceeds maximum_output_bytes");
  }
  return json;
}

#ifndef RULE30_EXTENDED_PERIOD_SEARCH_NO_MAIN
namespace {

[[nodiscard]] std::uint64_t parse_u64(std::string_view text,
                                      std::string_view option) {
  std::uint64_t value{};
  const auto [end, error] =
      std::from_chars(text.data(), text.data() + text.size(), value);
  if (error != std::errc{} || end != text.data() + text.size()) {
    throw std::invalid_argument("invalid value for " + std::string(option));
  }
  return value;
}

[[nodiscard]] std::string_view require_value(int argc, char** argv, int& index,
                                             std::string_view option) {
  if (index + 1 >= argc) {
    throw std::invalid_argument("missing value for " + std::string(option));
  }
  return argv[++index];
}

[[nodiscard]] SearchConfig parse_options(int argc, char** argv) {
  SearchConfig config{};
  for (int index = 1; index < argc; ++index) {
    const std::string_view option(argv[index]);
    if (option == "--help") {
      std::cout
          << "usage: rule30_cuda_extended_period_search [OPTIONS]\n"
          << "  --backend cpu|cuda\n"
          << "  --min-preperiod N --max-preperiod N\n"
          << "  --min-period N --max-period N --horizon N\n"
          << "  --evaluation-chunk N --threads N --device N\n"
          << "  --host-memory-budget-bytes N\n"
          << "  --device-memory-budget-bytes N\n"
          << "  --output-budget-bytes N --maximum-witnesses N\n";
      std::exit(EXIT_SUCCESS);
    }
    const auto value = require_value(argc, argv, index, option);
    const auto number = [&] { return parse_u64(value, option); };
    if (option == "--backend") {
      if (value == "cpu") {
        config.backend = Backend::kCpu;
      } else if (value == "cuda") {
        config.backend = Backend::kCuda;
      } else {
        throw std::invalid_argument("--backend must be cpu or cuda");
      }
    } else if (option == "--min-preperiod") {
      config.minimum_preperiod = number();
    } else if (option == "--max-preperiod") {
      config.maximum_preperiod = number();
    } else if (option == "--min-period") {
      config.minimum_period = number();
    } else if (option == "--max-period") {
      config.maximum_period = number();
    } else if (option == "--horizon") {
      config.horizon = number();
    } else if (option == "--evaluation-chunk") {
      config.maximum_evaluation_chunk = number();
    } else if (option == "--host-memory-budget-bytes") {
      config.host_memory_budget_bytes = number();
    } else if (option == "--device-memory-budget-bytes") {
      config.device_memory_budget_bytes = number();
    } else if (option == "--output-budget-bytes") {
      config.maximum_output_bytes = number();
    } else if (option == "--maximum-witnesses") {
      config.maximum_witnesses = number();
    } else if (option == "--threads") {
      const auto parsed = number();
      if (parsed > static_cast<std::uint64_t>(std::numeric_limits<int>::max())) {
        throw std::invalid_argument("--threads exceeds int range");
      }
      config.threads_per_block = static_cast<int>(parsed);
    } else if (option == "--device") {
      const auto parsed = number();
      if (parsed > static_cast<std::uint64_t>(std::numeric_limits<int>::max())) {
        throw std::invalid_argument("--device exceeds int range");
      }
      config.device_index = static_cast<int>(parsed);
    } else {
      throw std::invalid_argument("unknown option: " + std::string(option));
    }
  }
  return config;
}

}  // namespace
#endif

}  // namespace rule30::cuda::extended_period_search

#ifndef RULE30_EXTENDED_PERIOD_SEARCH_NO_MAIN
int main(int argc, char** argv) {
  try {
    const auto config =
        rule30::cuda::extended_period_search::parse_options(argc, argv);
    const auto result =
        rule30::cuda::extended_period_search::run_search(config);
    std::cout << rule30::cuda::extended_period_search::result_json(result);
    return EXIT_SUCCESS;
  } catch (const std::exception& error) {
    std::cerr << "extended period search failed: " << error.what() << '\n';
    return EXIT_FAILURE;
  }
}
#endif
