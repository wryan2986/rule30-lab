#pragma once

#include <cstddef>
#include <cstdint>

namespace rule30::detail {

void update_words_avx2(
    const std::uint64_t* current,
    std::size_t current_word_count,
    std::uint64_t* next,
    std::size_t next_word_count) noexcept;

}  // namespace rule30::detail
