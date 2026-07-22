#include "rule30/engine.hpp"

#include "detail/update.hpp"

#include <algorithm>
#include <ios>
#include <limits>
#include <ostream>
#include <stdexcept>
#include <utility>

#ifndef RULE30_HAVE_AVX2_IMPL
#define RULE30_HAVE_AVX2_IMPL 0
#endif

namespace rule30 {
namespace {

constexpr std::size_t bits_per_word = 64U;

[[nodiscard]] std::size_t words_for_bits(const std::size_t bit_count) noexcept {
    return (bit_count / bits_per_word) +
           static_cast<std::size_t>((bit_count % bits_per_word) != 0U);
}

[[nodiscard]] std::uint64_t updated_word(
    const std::uint64_t current,
    const std::uint64_t previous) noexcept {
    // At time t, packed index i represents coordinate j = i - t. Thus for
    // output index k, Rule 30 reads old indices k-2, k-1, and k:
    //   next[k] = old[k-2] XOR (old[k-1] OR old[k]).
    const std::uint64_t shifted_one = (current << 1U) | (previous >> 63U);
    const std::uint64_t shifted_two = (current << 2U) | (previous >> 62U);
    return shifted_two ^ (shifted_one | current);
}

void update_words_scalar(
    const std::uint64_t* const current,
    const std::size_t current_word_count,
    std::uint64_t* const next,
    const std::size_t next_word_count) noexcept {
    for (std::size_t index = 0; index < next_word_count; ++index) {
        const std::uint64_t current_word =
            index < current_word_count ? current[index] : 0U;
        const std::uint64_t previous_word =
            index > 0U && (index - 1U) < current_word_count
                ? current[index - 1U]
                : 0U;
        next[index] = updated_word(current_word, previous_word);
    }
}

void mask_unused_high_bits(
    std::vector<std::uint64_t>& words,
    const std::size_t logical_size) noexcept {
    const std::size_t used_in_final_word = logical_size % bits_per_word;
    if (used_in_final_word == 0U) {
        return;
    }

    const std::uint64_t mask =
        (std::uint64_t{1} << used_in_final_word) - std::uint64_t{1};
    words.back() &= mask;
}

[[nodiscard]] std::int64_t discrepancy_for(
    const std::uint64_t ones,
    const std::size_t count) noexcept {
    const std::uint64_t zeros =
        static_cast<std::uint64_t>(count) - ones;
    if (ones >= zeros) {
        return static_cast<std::int64_t>(ones - zeros);
    }
    return -static_cast<std::int64_t>(zeros - ones);
}

}  // namespace

std::string_view backend_name(const Backend backend) noexcept {
    switch (backend) {
        case Backend::scalar:
            return "scalar";
        case Backend::avx2:
            return "avx2";
        case Backend::automatic:
            return "auto";
    }
    return "unknown";
}

bool avx2_compiled() noexcept {
    return RULE30_HAVE_AVX2_IMPL != 0;
}

bool avx2_runtime_supported() noexcept {
#if RULE30_HAVE_AVX2_IMPL && \
    (defined(__x86_64__) || defined(__i386__)) && \
    (defined(__GNUC__) || defined(__clang__))
    static const bool supported = [] {
        __builtin_cpu_init();
        return __builtin_cpu_supports("avx2") != 0;
    }();
    return supported;
#else
    return false;
#endif
}

Backend resolve_backend(const Backend requested) {
    switch (requested) {
        case Backend::scalar:
            return Backend::scalar;
        case Backend::avx2:
            if (!avx2_compiled()) {
                throw std::runtime_error("the AVX2 backend was not compiled");
            }
            if (!avx2_runtime_supported()) {
                throw std::runtime_error(
                    "the AVX2 backend is not supported by this CPU/OS");
            }
            return Backend::avx2;
        case Backend::automatic:
            return avx2_compiled() && avx2_runtime_supported()
                       ? Backend::avx2
                       : Backend::scalar;
    }
    throw std::invalid_argument("unknown Rule 30 backend");
}

PackedRow::PackedRow(
    const std::size_t logical_size,
    std::vector<std::uint64_t> words)
    : logical_size_(logical_size), words_(std::move(words)) {
    if (logical_size_ == 0U) {
        throw std::invalid_argument("a packed row must contain at least one bit");
    }
    if (words_.size() != words_for_bits(logical_size_)) {
        throw std::invalid_argument("packed row word count does not match length");
    }
    mask_unused_high_bits(words_, logical_size_);
}

PackedRow PackedRow::single_seed() {
    return PackedRow(1U, {std::uint64_t{1}});
}

PackedRow PackedRow::from_bits(const std::span<const std::uint8_t> bits) {
    if (bits.empty()) {
        throw std::invalid_argument("a packed row must contain at least one bit");
    }

    std::vector<std::uint64_t> words(words_for_bits(bits.size()), 0U);
    for (std::size_t index = 0; index < bits.size(); ++index) {
        if (bits[index] > 1U) {
            throw std::invalid_argument("row values must be numeric zero or one");
        }
        words[index / bits_per_word] |=
            static_cast<std::uint64_t>(bits[index])
            << (index % bits_per_word);
    }
    return PackedRow(bits.size(), std::move(words));
}

std::size_t PackedRow::logical_size() const noexcept {
    return logical_size_;
}

std::size_t PackedRow::word_count() const noexcept {
    return words_.size();
}

bool PackedRow::bit(const std::size_t index) const {
    if (index >= logical_size_) {
        throw std::out_of_range("packed row bit index is outside logical length");
    }
    return ((words_[index / bits_per_word] >> (index % bits_per_word)) & 1U) !=
           0U;
}

std::span<const std::uint64_t> PackedRow::words() const noexcept {
    return words_;
}

std::vector<std::uint8_t> PackedRow::unpack() const {
    std::vector<std::uint8_t> bits(logical_size_, 0U);
    for (std::size_t index = 0; index < logical_size_; ++index) {
        bits[index] = static_cast<std::uint8_t>(bit(index));
    }
    return bits;
}

void PackedRow::step(const Backend backend) {
    if (logical_size_ > std::numeric_limits<std::size_t>::max() - 2U) {
        throw std::length_error("packed row length overflow");
    }

    const Backend selected = resolve_backend(backend);
    const std::size_t next_logical_size = logical_size_ + 2U;
    std::vector<std::uint64_t> next(words_for_bits(next_logical_size), 0U);

    if (selected == Backend::avx2) {
#if RULE30_HAVE_AVX2_IMPL
        detail::update_words_avx2(
            words_.data(), words_.size(), next.data(), next.size());
#else
        throw std::logic_error("AVX2 backend resolution is inconsistent");
#endif
    } else {
        update_words_scalar(
            words_.data(), words_.size(), next.data(), next.size());
    }

    mask_unused_high_bits(next, next_logical_size);
    words_ = std::move(next);
    logical_size_ = next_logical_size;
}

GenerationSummary stream_center_prefix(
    const std::size_t count,
    const GenerationOptions& options,
    const ByteSink& sink) {
    if (count > static_cast<std::size_t>(
                    std::numeric_limits<std::int64_t>::max())) {
        throw std::length_error(
            "prefix length exceeds the supported discrepancy range");
    }
    if (options.chunk_size == 0U) {
        throw std::invalid_argument("stream chunk size must be positive");
    }

    std::vector<std::size_t> requested = options.checkpoints;
    std::sort(requested.begin(), requested.end());
    requested.erase(std::unique(requested.begin(), requested.end()), requested.end());
    for (const std::size_t checkpoint : requested) {
        if (checkpoint == 0U || checkpoint > count) {
            throw std::invalid_argument(
                "checkpoints must be between one and the prefix length");
        }
    }

    GenerationSummary summary;
    summary.count = count;
    summary.backend = resolve_backend(options.backend);

    if (count == 0U) {
        return summary;
    }

    std::vector<std::uint8_t> chunk;
    if (sink) {
        chunk.reserve(std::min(options.chunk_size, count));
    }

    PackedRow row = PackedRow::single_seed();
    std::size_t next_checkpoint = 0U;

    for (std::size_t index = 0; index < count; ++index) {
        const std::uint8_t center = static_cast<std::uint8_t>(row.bit(index));
        summary.ones += center;

        const std::size_t completed = index + 1U;
        if (next_checkpoint < requested.size() &&
            completed == requested[next_checkpoint]) {
            summary.checkpoints.push_back(BalanceCheckpoint{
                completed,
                summary.ones,
                discrepancy_for(summary.ones, completed),
            });
            ++next_checkpoint;
        }

        if (sink) {
            chunk.push_back(center);
            if (chunk.size() == options.chunk_size) {
                sink(chunk);
                chunk.clear();
            }
        }

        if (completed < count) {
            row.step(summary.backend);
        }
    }

    if (sink && !chunk.empty()) {
        sink(chunk);
    }

    summary.zeros = static_cast<std::uint64_t>(count) - summary.ones;
    summary.discrepancy = discrepancy_for(summary.ones, count);
    return summary;
}

std::vector<std::uint8_t> generate_center_prefix(
    const std::size_t count,
    const Backend backend,
    const std::size_t chunk_size) {
    std::vector<std::uint8_t> result;
    result.reserve(count);

    GenerationOptions options;
    options.backend = backend;
    options.chunk_size = chunk_size;
    static_cast<void>(stream_center_prefix(
        count,
        options,
        [&result](const std::span<const std::uint8_t> values) {
            result.insert(result.end(), values.begin(), values.end());
        }));
    return result;
}

GenerationSummary write_center_prefix_bytes(
    std::ostream& output,
    const std::size_t count,
    const GenerationOptions& options) {
    if (!output) {
        throw std::ios_base::failure("output stream is not writable");
    }

    return stream_center_prefix(
        count,
        options,
        [&output](const std::span<const std::uint8_t> values) {
            if (values.size() > static_cast<std::size_t>(
                                    std::numeric_limits<std::streamsize>::max())) {
                throw std::length_error("output chunk exceeds streamsize range");
            }
            output.write(
                reinterpret_cast<const char*>(values.data()),
                static_cast<std::streamsize>(values.size()));
            if (!output) {
                throw std::ios_base::failure("failed to write center bytes");
            }
        });
}

}  // namespace rule30
