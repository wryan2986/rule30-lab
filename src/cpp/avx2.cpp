#include "detail/update.hpp"

#include <immintrin.h>

namespace rule30::detail {
namespace {

[[nodiscard]] std::uint64_t updated_word(
    const std::uint64_t current,
    const std::uint64_t previous) noexcept {
    const std::uint64_t shifted_one = (current << 1U) | (previous >> 63U);
    const std::uint64_t shifted_two = (current << 2U) | (previous >> 62U);
    return shifted_two ^ (shifted_one | current);
}

}  // namespace

void update_words_avx2(
    const std::uint64_t* const current,
    const std::size_t current_word_count,
    std::uint64_t* const next,
    const std::size_t next_word_count) noexcept {
    std::size_t index = 0U;

    // Word zero has an implicit all-zero predecessor.
    if (next_word_count != 0U) {
        const std::uint64_t current_word =
            current_word_count != 0U ? current[0] : 0U;
        next[0] = updated_word(current_word, 0U);
        index = 1U;
    }

    // Each vector lane uses an explicitly loaded preceding word for carries,
    // so no shift crosses an AVX2 lane boundary implicitly.
    for (; index + 4U <= current_word_count; index += 4U) {
        const auto* const current_address =
            reinterpret_cast<const __m256i*>(current + index);
        const auto* const previous_address =
            reinterpret_cast<const __m256i*>(current + index - 1U);

        const __m256i current_words = _mm256_loadu_si256(current_address);
        const __m256i previous_words = _mm256_loadu_si256(previous_address);
        const __m256i shifted_one = _mm256_or_si256(
            _mm256_slli_epi64(current_words, 1),
            _mm256_srli_epi64(previous_words, 63));
        const __m256i shifted_two = _mm256_or_si256(
            _mm256_slli_epi64(current_words, 2),
            _mm256_srli_epi64(previous_words, 62));
        const __m256i result = _mm256_xor_si256(
            shifted_two,
            _mm256_or_si256(shifted_one, current_words));

        auto* const output_address = reinterpret_cast<__m256i*>(next + index);
        _mm256_storeu_si256(output_address, result);
    }

    for (; index < next_word_count; ++index) {
        const std::uint64_t current_word =
            index < current_word_count ? current[index] : 0U;
        const std::uint64_t previous_word =
            index > 0U && (index - 1U) < current_word_count
                ? current[index - 1U]
                : 0U;
        next[index] = updated_word(current_word, previous_word);
    }
}

}  // namespace rule30::detail
