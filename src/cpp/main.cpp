#include "rule30/engine.hpp"

#include <algorithm>
#include <charconv>
#include <chrono>
#include <cmath>
#include <cstddef>
#include <cstdint>
#include <cstdlib>
#include <iomanip>
#include <iostream>
#include <limits>
#include <stdexcept>
#include <string>
#include <string_view>
#include <vector>

namespace {

enum class OutputFormat {
    json,
    raw,
};

struct CliOptions {
    std::string_view command;
    std::size_t count{};
    bool count_was_set{false};
    rule30::Backend backend{rule30::Backend::automatic};
    OutputFormat format{OutputFormat::json};
    std::size_t chunk_size{64U * 1024U};
    std::vector<std::size_t> checkpoints;
    std::size_t warmups{1U};
    std::size_t repetitions{5U};
};

[[nodiscard]] std::size_t parse_size(
    const std::string_view text,
    const std::string_view option_name) {
    std::uint64_t value = 0U;
    const char* const begin = text.data();
    const char* const end = begin + text.size();
    const auto [position, error] = std::from_chars(begin, end, value);
    if (error != std::errc{} || position != end || text.empty()) {
        throw std::invalid_argument(
            std::string(option_name) + " requires a nonnegative integer");
    }
    if (value > std::numeric_limits<std::size_t>::max()) {
        throw std::out_of_range(std::string(option_name) + " is too large");
    }
    return static_cast<std::size_t>(value);
}

[[nodiscard]] rule30::Backend parse_backend(const std::string_view value) {
    if (value == "scalar") {
        return rule30::Backend::scalar;
    }
    if (value == "avx2") {
        return rule30::Backend::avx2;
    }
    if (value == "auto") {
        return rule30::Backend::automatic;
    }
    throw std::invalid_argument("--backend must be scalar, avx2, or auto");
}

[[nodiscard]] OutputFormat parse_format(const std::string_view value) {
    if (value == "json") {
        return OutputFormat::json;
    }
    if (value == "raw") {
        return OutputFormat::raw;
    }
    throw std::invalid_argument("--format must be json or raw");
}

[[nodiscard]] std::string_view require_value(
    const int argc,
    char** const argv,
    int& index,
    const std::string_view option_name) {
    if (index + 1 >= argc) {
        throw std::invalid_argument(
            std::string(option_name) + " requires a value");
    }
    ++index;
    return argv[index];
}

void print_usage(std::ostream& output) {
    output
        << "Usage:\n"
        << "  rule30_cpp generate --count N [--backend auto|scalar|avx2] "
           "[--format json|raw]\n"
        << "                      [--chunk-size N] [--checkpoint N ...]\n"
        << "  rule30_cpp benchmark --count N [--backend auto|scalar|avx2] "
           "[--warmup N] [--repetitions N]\n\n"
        << "Raw generation writes exactly N binary bytes, each numeric 0 or 1, "
           "to stdout.\n";
}

[[nodiscard]] CliOptions parse_arguments(const int argc, char** const argv) {
    if (argc < 2) {
        throw std::invalid_argument("a command is required (generate or benchmark)");
    }

    CliOptions options;
    options.command = argv[1];
    if (options.command != "generate" && options.command != "benchmark") {
        throw std::invalid_argument("unknown command; expected generate or benchmark");
    }

    for (int index = 2; index < argc; ++index) {
        const std::string_view argument = argv[index];
        if (argument == "--count") {
            options.count = parse_size(
                require_value(argc, argv, index, argument), argument);
            options.count_was_set = true;
        } else if (argument == "--backend") {
            options.backend = parse_backend(
                require_value(argc, argv, index, argument));
        } else if (argument == "--format") {
            options.format = parse_format(
                require_value(argc, argv, index, argument));
        } else if (argument == "--chunk-size") {
            options.chunk_size = parse_size(
                require_value(argc, argv, index, argument), argument);
        } else if (argument == "--checkpoint") {
            options.checkpoints.push_back(parse_size(
                require_value(argc, argv, index, argument), argument));
        } else if (argument == "--warmup") {
            options.warmups = parse_size(
                require_value(argc, argv, index, argument), argument);
        } else if (argument == "--repetitions") {
            options.repetitions = parse_size(
                require_value(argc, argv, index, argument), argument);
        } else if (argument == "--help" || argument == "-h") {
            print_usage(std::cout);
            std::exit(0);
        } else {
            throw std::invalid_argument("unknown option: " + std::string(argument));
        }
    }

    if (!options.count_was_set) {
        throw std::invalid_argument("--count is required");
    }
    if (options.chunk_size == 0U) {
        throw std::invalid_argument("--chunk-size must be positive");
    }
    if (options.command == "benchmark" && options.repetitions == 0U) {
        throw std::invalid_argument("--repetitions must be positive");
    }
    if (options.command == "benchmark" && !options.checkpoints.empty()) {
        throw std::invalid_argument(
            "--checkpoint is only available for the generate command");
    }
    if (options.command == "benchmark" && options.format == OutputFormat::raw) {
        throw std::invalid_argument(
            "raw output is only available for the generate command");
    }
    return options;
}

void print_summary_json(const rule30::GenerationSummary& summary) {
    std::cout << '{'
              << "\"count\":" << summary.count << ','
              << "\"ones\":" << summary.ones << ','
              << "\"zeros\":" << summary.zeros << ','
              << "\"discrepancy\":" << summary.discrepancy << ','
              << "\"backend\":\"" << rule30::backend_name(summary.backend)
              << "\",\"checkpoints\":[";

    for (std::size_t index = 0; index < summary.checkpoints.size(); ++index) {
        if (index != 0U) {
            std::cout << ',';
        }
        const auto& checkpoint = summary.checkpoints[index];
        std::cout << '{'
                  << "\"count\":" << checkpoint.count << ','
                  << "\"ones\":" << checkpoint.ones << ','
                  << "\"discrepancy\":" << checkpoint.discrepancy
                  << '}';
    }
    std::cout << "]}\n";
}

[[nodiscard]] bool same_result(
    const rule30::GenerationSummary& left,
    const rule30::GenerationSummary& right) noexcept {
    return left.count == right.count && left.ones == right.ones &&
           left.zeros == right.zeros &&
           left.discrepancy == right.discrepancy &&
           left.backend == right.backend;
}

void run_benchmark(const CliOptions& cli) {
    rule30::GenerationOptions generation;
    generation.backend = cli.backend;
    generation.chunk_size = cli.chunk_size;

    rule30::GenerationSummary reference;
    bool have_reference = false;

    for (std::size_t warmup = 0; warmup < cli.warmups; ++warmup) {
        const auto result =
            rule30::stream_center_prefix(cli.count, generation);
        if (!have_reference) {
            reference = result;
            have_reference = true;
        } else if (!same_result(reference, result)) {
            throw std::runtime_error("benchmark warm-up results were inconsistent");
        }
    }

    std::vector<double> seconds;
    seconds.reserve(cli.repetitions);
    for (std::size_t repetition = 0; repetition < cli.repetitions; ++repetition) {
        const auto start = std::chrono::steady_clock::now();
        const auto result =
            rule30::stream_center_prefix(cli.count, generation);
        const auto stop = std::chrono::steady_clock::now();

        if (!have_reference) {
            reference = result;
            have_reference = true;
        } else if (!same_result(reference, result)) {
            throw std::runtime_error("benchmark results were inconsistent");
        }

        seconds.push_back(std::chrono::duration<double>(stop - start).count());
    }

    const auto [minimum, maximum] =
        std::minmax_element(seconds.begin(), seconds.end());
    double sum = 0.0;
    for (const double value : seconds) {
        sum += value;
    }
    const double mean = sum / static_cast<double>(seconds.size());

    double squared_deviation = 0.0;
    for (const double value : seconds) {
        const double difference = value - mean;
        squared_deviation += difference * difference;
    }
    const double standard_deviation =
        std::sqrt(squared_deviation / static_cast<double>(seconds.size()));

    std::vector<double> sorted = seconds;
    std::sort(sorted.begin(), sorted.end());
    const std::size_t middle = sorted.size() / 2U;
    const double median = sorted.size() % 2U != 0U
                              ? sorted[middle]
                              : (sorted[middle - 1U] + sorted[middle]) / 2.0;

    std::cout << std::setprecision(12) << '{'
              << "\"count\":" << reference.count << ','
              << "\"backend\":\"" << rule30::backend_name(reference.backend)
              << "\",\"warmups\":" << cli.warmups << ','
              << "\"repetitions\":" << cli.repetitions << ','
              << "\"ones\":" << reference.ones << ','
              << "\"discrepancy\":" << reference.discrepancy << ','
              << "\"seconds\":{"
              << "\"minimum\":" << *minimum << ','
              << "\"median\":" << median << ','
              << "\"maximum\":" << *maximum << ','
              << "\"mean\":" << mean << ','
              << "\"standard_deviation\":" << standard_deviation
              << "}}\n";
}

}  // namespace

int main(const int argc, char** const argv) {
    try {
        std::ios::sync_with_stdio(false);
        const CliOptions options = parse_arguments(argc, argv);

        if (options.command == "benchmark") {
            run_benchmark(options);
            return 0;
        }

        rule30::GenerationOptions generation;
        generation.backend = options.backend;
        generation.chunk_size = options.chunk_size;
        generation.checkpoints = options.checkpoints;

        if (options.format == OutputFormat::raw) {
            static_cast<void>(rule30::write_center_prefix_bytes(
                std::cout, options.count, generation));
        } else {
            const auto summary =
                rule30::stream_center_prefix(options.count, generation);
            print_summary_json(summary);
        }
        return 0;
    } catch (const std::exception& error) {
        std::cerr << "rule30_cpp: " << error.what() << '\n';
        print_usage(std::cerr);
        return 2;
    }
}
