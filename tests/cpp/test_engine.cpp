#include "rule30/engine.hpp"

#include <array>
#include <cstddef>
#include <cstdint>
#include <exception>
#include <fstream>
#include <functional>
#include <iostream>
#include <iterator>
#include <sstream>
#include <stdexcept>
#include <string>
#include <string_view>
#include <vector>

namespace {

#ifndef RULE30_SOURCE_DIR
#error "RULE30_SOURCE_DIR must identify the repository root"
#endif

[[noreturn]] void fail(const std::string& message) {
    throw std::runtime_error(message);
}

void expect(const bool condition, const std::string& message) {
    if (!condition) {
        fail(message);
    }
}

template <typename Exception, typename Function>
void expect_throws(Function&& function, const std::string& message) {
    try {
        std::forward<Function>(function)();
    } catch (const Exception&) {
        return;
    } catch (const std::exception& error) {
        fail(message + ": wrong exception: " + error.what());
    }
    fail(message + ": no exception");
}

[[nodiscard]] std::vector<std::uint8_t> bits_from_text(
    const std::string_view text) {
    std::vector<std::uint8_t> bits;
    bits.reserve(text.size());
    for (const char value : text) {
        if (value != '0' && value != '1') {
            fail("test vector contains a non-binary character");
        }
        bits.push_back(static_cast<std::uint8_t>(value - '0'));
    }
    return bits;
}

[[nodiscard]] std::string bits_to_text(
    const std::vector<std::uint8_t>& bits) {
    std::string text;
    text.reserve(bits.size());
    for (const std::uint8_t bit : bits) {
        text.push_back(static_cast<char>('0' + bit));
    }
    return text;
}

// Independent coordinate-oriented cell-array update. Index i at time t is
// coordinate i-t. Out-of-range cells are zero.
[[nodiscard]] std::vector<std::uint8_t> naive_step(
    const std::vector<std::uint8_t>& current) {
    std::vector<std::uint8_t> next(current.size() + 2U, 0U);
    const auto old = [&current](const std::ptrdiff_t index) -> std::uint8_t {
        if (index < 0 ||
            static_cast<std::size_t>(index) >= current.size()) {
            return 0U;
        }
        return current[static_cast<std::size_t>(index)];
    };

    for (std::size_t index = 0; index < next.size(); ++index) {
        const auto signed_index = static_cast<std::ptrdiff_t>(index);
        next[index] = static_cast<std::uint8_t>(
            old(signed_index - 2) ^
            (old(signed_index - 1) | old(signed_index)));
    }
    return next;
}

[[nodiscard]] std::vector<std::uint8_t> naive_center_prefix(
    const std::size_t count) {
    std::vector<std::uint8_t> output;
    output.reserve(count);
    std::vector<std::uint8_t> row{1U};
    for (std::size_t time = 0; time < count; ++time) {
        output.push_back(row[time]);
        if (time + 1U < count) {
            row = naive_step(row);
        }
    }
    return output;
}

void test_hand_derived_rows() {
    // Listed left-to-right for coordinates -t through t.
    const std::array<std::string_view, 6> expected{
        "1",
        "111",
        "11001",
        "1101111",
        "110010001",
        "11011110111",
    };

    rule30::PackedRow row = rule30::PackedRow::single_seed();
    for (std::size_t time = 0; time < expected.size(); ++time) {
        expect(
            bits_to_text(row.unpack()) == expected[time],
            "hand-derived row mismatch at time " + std::to_string(time));
        expect(
            row.logical_size() == 2U * time + 1U,
            "logical row length mismatch");
        if (time + 1U < expected.size()) {
            row.step(rule30::Backend::scalar);
        }
    }
}

void test_prefix_convention_and_small_values() {
    expect(
        rule30::generate_center_prefix(0U, rule30::Backend::scalar).empty(),
        "N=0 must produce no center bytes");
    expect(
        rule30::generate_center_prefix(1U, rule30::Backend::scalar) ==
            bits_from_text("1"),
        "N=1 must contain c_0 only");
    expect(
        rule30::generate_center_prefix(9U, rule30::Backend::scalar) ==
            bits_from_text("110111001"),
        "first nine center bits mismatch");
}

void test_requested_prefix_boundaries() {
    for (const std::size_t count : {64U, 65U, 127U, 128U, 129U}) {
        const auto expected = naive_center_prefix(count);
        const auto actual = rule30::generate_center_prefix(
            count, rule30::Backend::scalar, 7U);
        expect(
            actual == expected,
            "center prefix mismatch at N=" + std::to_string(count));
    }
}

void test_arbitrary_row_word_boundaries() {
    for (const std::size_t length : {1U, 63U, 64U, 65U, 127U, 128U, 129U}) {
        std::vector<std::uint8_t> bits(length, 0U);
        for (std::size_t index = 0; index < length; ++index) {
            bits[index] = static_cast<std::uint8_t>(
                ((index * 17U + 3U) % 11U) < 5U);
        }
        bits.front() = 1U;
        bits.back() = 1U;
        if (length > 64U) {
            bits[63U] = 1U;
            bits[64U] = 0U;
        }

        const auto expected = naive_step(bits);
        auto packed = rule30::PackedRow::from_bits(bits);
        packed.step(rule30::Backend::scalar);
        expect(
            packed.unpack() == expected,
            "packed scalar update mismatch at row length " +
                std::to_string(length));
        expect(
            packed.logical_size() == length + 2U,
            "packed row did not grow by two cells");

        const std::size_t final_bits = packed.logical_size() % 64U;
        if (final_bits != 0U) {
            expect(
                (packed.words().back() >> final_bits) == 0U,
                "unused final-word bits were not cleared");
        }
    }

    const auto sixty_five_ones = bits_from_text(std::string(65U, '1'));
    const auto partial = rule30::PackedRow::from_bits(sixty_five_ones);
    expect(partial.word_count() == 2U, "65 bits must occupy two words");
    expect(partial.words()[1] == 1U, "partial final word contains stray bits");
}

void test_streaming_chunks_and_checkpoints() {
    const auto expected = bits_from_text("110111001");
    for (const std::size_t chunk_size : {1U, 2U, 7U, 8U, 9U, 64U, 65U}) {
        rule30::GenerationOptions options;
        options.backend = rule30::Backend::scalar;
        options.chunk_size = chunk_size;
        options.checkpoints = {9U, 1U, 5U, 2U, 5U};

        std::vector<std::uint8_t> streamed;
        std::size_t calls = 0U;
        const auto summary = rule30::stream_center_prefix(
            expected.size(),
            options,
            [&](const std::span<const std::uint8_t> chunk) {
                expect(!chunk.empty(), "sink received an empty chunk");
                expect(
                    chunk.size() <= chunk_size,
                    "sink chunk exceeds configured size");
                streamed.insert(streamed.end(), chunk.begin(), chunk.end());
                ++calls;
            });

        expect(calls > 0U, "nonempty stream never invoked sink");
        expect(streamed == expected, "streamed output changed with chunk size");
        expect(summary.count == 9U, "summary count mismatch");
        expect(summary.ones == 6U, "summary ones mismatch");
        expect(summary.zeros == 3U, "summary zeros mismatch");
        expect(summary.discrepancy == 3, "summary discrepancy mismatch");
        const std::vector<rule30::BalanceCheckpoint> checkpoints{
            {1U, 1U, 1},
            {2U, 2U, 2},
            {5U, 4U, 3},
            {9U, 6U, 3},
        };
        expect(
            summary.checkpoints == checkpoints,
            "checkpoint summaries mismatch");
    }

    rule30::GenerationOptions empty_options;
    empty_options.backend = rule30::Backend::scalar;
    bool called = false;
    const auto empty_summary = rule30::stream_center_prefix(
        0U,
        empty_options,
        [&called](std::span<const std::uint8_t>) { called = true; });
    expect(!called, "N=0 invoked the streaming sink");
    expect(
        empty_summary.ones == 0U && empty_summary.zeros == 0U &&
            empty_summary.discrepancy == 0,
        "N=0 summary mismatch");
}

void test_byte_stream_contract() {
    std::ostringstream output(std::ios::out | std::ios::binary);
    rule30::GenerationOptions options;
    options.backend = rule30::Backend::scalar;
    options.chunk_size = 3U;
    const auto summary =
        rule30::write_center_prefix_bytes(output, 9U, options);
    const std::string bytes = output.str();
    const auto expected = bits_from_text("110111001");

    expect(bytes.size() == expected.size(), "byte stream length mismatch");
    for (std::size_t index = 0; index < bytes.size(); ++index) {
        expect(
            static_cast<std::uint8_t>(bytes[index]) == expected[index],
            "byte stream contains a nonmatching value");
    }
    expect(summary.ones == 6U, "byte stream summary mismatch");
}

void test_scalar_avx2_and_auto_equality() {
    const auto scalar = rule30::generate_center_prefix(
        513U, rule30::Backend::scalar, 31U);
    const auto automatic = rule30::generate_center_prefix(
        513U, rule30::Backend::automatic, 64U);
    expect(automatic == scalar, "automatic backend differs from scalar");

    if (rule30::avx2_compiled() && rule30::avx2_runtime_supported()) {
        const auto avx2 = rule30::generate_center_prefix(
            513U, rule30::Backend::avx2, 127U);
        expect(avx2 == scalar, "AVX2 center sequence differs from scalar");

        std::vector<std::uint8_t> bits(129U, 0U);
        for (std::size_t index = 0; index < bits.size(); ++index) {
            bits[index] = static_cast<std::uint8_t>((index % 5U) == 1U);
        }
        auto scalar_row = rule30::PackedRow::from_bits(bits);
        auto avx2_row = rule30::PackedRow::from_bits(bits);
        for (std::size_t iteration = 0; iteration < 20U; ++iteration) {
            scalar_row.step(rule30::Backend::scalar);
            avx2_row.step(rule30::Backend::avx2);
            expect(
                scalar_row.unpack() == avx2_row.unpack(),
                "AVX2 row differs from scalar after iteration " +
                    std::to_string(iteration + 1U));
        }
    } else {
        expect(
            rule30::resolve_backend(rule30::Backend::automatic) ==
                rule30::Backend::scalar,
            "automatic backend did not fall back to scalar");
        expect_throws<std::runtime_error>(
            [] { static_cast<void>(rule30::resolve_backend(rule30::Backend::avx2)); },
            "unavailable AVX2 backend must be rejected");
    }
}

void test_shared_reference_vectors() {
    const std::string repository = RULE30_SOURCE_DIR;
    const std::string center_path =
        repository +
        "/tests/reference_vectors/center_c00000000_c00009999.u8";
    std::ifstream center_file(center_path, std::ios::binary);
    expect(center_file.is_open(), "could not open shared center vector");
    const std::vector<char> raw_center{
        std::istreambuf_iterator<char>(center_file),
        std::istreambuf_iterator<char>()};
    expect(raw_center.size() == 10'000U, "shared center vector size mismatch");

    std::vector<std::uint8_t> expected_center;
    expected_center.reserve(raw_center.size());
    for (const char value : raw_center) {
        const auto bit = static_cast<std::uint8_t>(value);
        expect(bit <= 1U, "shared center vector contains a non-binary byte");
        expected_center.push_back(bit);
    }

    const auto scalar = rule30::generate_center_prefix(
        expected_center.size(), rule30::Backend::scalar, 73U);
    expect(scalar == expected_center, "scalar engine differs from shared center vector");

    if (rule30::avx2_compiled() && rule30::avx2_runtime_supported()) {
        const auto avx2 = rule30::generate_center_prefix(
            expected_center.size(), rule30::Backend::avx2, 127U);
        expect(avx2 == expected_center, "AVX2 engine differs from shared center vector");
    }

    const std::string rows_path =
        repository + "/tests/reference_vectors/rows_t0000_t0255.txt";
    std::ifstream rows_file(rows_path);
    expect(rows_file.is_open(), "could not open shared complete-row vector");

    rule30::PackedRow row = rule30::PackedRow::single_seed();
    std::string line;
    std::size_t time = 0U;
    while (std::getline(rows_file, line)) {
        expect(time < 256U, "shared row vector contains extra rows");
        expect(line.size() >= 6U && line[4] == '\t', "malformed shared row line");
        const auto expected_label =
            std::to_string(10'000U + time).substr(1U);
        expect(
            line.substr(0U, 4U) == expected_label,
            "shared row time label mismatch at row " + std::to_string(time));
        expect(
            bits_to_text(row.unpack()) == line.substr(5U),
            "packed row differs from shared vector at time " +
                std::to_string(time));
        ++time;
        if (time < 256U) {
            row.step(rule30::Backend::scalar);
        }
    }
    expect(time == 256U, "shared row vector is incomplete");
}

void test_invalid_inputs() {
    expect_throws<std::invalid_argument>(
        [] {
            const std::vector<std::uint8_t> empty;
            static_cast<void>(rule30::PackedRow::from_bits(empty));
        },
        "empty row must be rejected");
    expect_throws<std::invalid_argument>(
        [] {
            const std::vector<std::uint8_t> invalid{0U, 2U, 1U};
            static_cast<void>(rule30::PackedRow::from_bits(invalid));
        },
        "non-binary row value must be rejected");
    expect_throws<std::out_of_range>(
        [] {
            const auto row = rule30::PackedRow::single_seed();
            static_cast<void>(row.bit(1U));
        },
        "logical out-of-range bit must be rejected");
    expect_throws<std::invalid_argument>(
        [] {
            rule30::GenerationOptions options;
            options.backend = rule30::Backend::scalar;
            options.chunk_size = 0U;
            static_cast<void>(rule30::stream_center_prefix(1U, options));
        },
        "zero stream chunk must be rejected");
    expect_throws<std::invalid_argument>(
        [] {
            rule30::GenerationOptions options;
            options.backend = rule30::Backend::scalar;
            options.checkpoints = {0U};
            static_cast<void>(rule30::stream_center_prefix(1U, options));
        },
        "zero checkpoint must be rejected");
    expect_throws<std::invalid_argument>(
        [] {
            rule30::GenerationOptions options;
            options.backend = rule30::Backend::scalar;
            options.checkpoints = {2U};
            static_cast<void>(rule30::stream_center_prefix(1U, options));
        },
        "checkpoint beyond prefix must be rejected");
}

}  // namespace

int main() {
    try {
        const std::array<std::pair<std::string_view, std::function<void()>>, 9>
            tests{{
                {"hand-derived rows", test_hand_derived_rows},
                {"prefix convention", test_prefix_convention_and_small_values},
                {"prefix boundaries", test_requested_prefix_boundaries},
                {"row boundaries", test_arbitrary_row_word_boundaries},
                {"streaming and checkpoints", test_streaming_chunks_and_checkpoints},
                {"byte stream", test_byte_stream_contract},
                {"scalar/AVX2 equality", test_scalar_avx2_and_auto_equality},
                {"shared reference vectors", test_shared_reference_vectors},
                {"invalid inputs", test_invalid_inputs},
            }};

        for (const auto& [name, test] : tests) {
            test();
            std::cout << "PASS: " << name << '\n';
        }
        return 0;
    } catch (const std::exception& error) {
        std::cerr << "FAIL: " << error.what() << '\n';
        return 1;
    }
}
