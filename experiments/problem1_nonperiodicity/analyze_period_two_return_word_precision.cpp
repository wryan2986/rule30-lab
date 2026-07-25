#include <boost/multiprecision/cpp_int.hpp>
#include <algorithm>
#include <array>
#include <cstdint>
#include <iomanip>
#include <iostream>
#include <map>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

using boost::multiprecision::cpp_int;

namespace {
constexpr int SPAN_CAP = 10;
constexpr int WIDTH_SAMPLES = 5;

std::uint64_t advance64(std::uint64_t state) {
    const std::uint64_t row = 1 | (state << 1);
    const std::uint64_t odd = row ^ ((row >> 1) | (row >> 2));
    return (odd << 1) ^ (odd | (odd >> 1));
}

cpp_int advance_big(const cpp_int& state) {
    const cpp_int row = 1 | (state << 1);
    const cpp_int odd = row ^ ((row >> 1) | (row >> 2));
    return (odd << 1) ^ (odd | (odd >> 1));
}

std::pair<int, std::uint64_t> first_return64(std::uint64_t z) {
    std::uint64_t state = 4 * z;
    for (int gap = 1; gap <= 5; ++gap) {
        state = advance64(state);
        if ((state & 3) == 0) return {gap, state >> 2};
    }
    throw std::runtime_error("five-block return bound failed");
}

std::pair<int, cpp_int> first_return_big(const cpp_int& z) {
    cpp_int state = 4 * z;
    for (int gap = 1; gap <= 5; ++gap) {
        state = advance_big(state);
        if (static_cast<unsigned>(state & 3) == 0) return {gap, state >> 2};
    }
    throw std::runtime_error("five-block return bound failed");
}

std::pair<std::vector<int>, cpp_int> follow_big(cpp_int z, std::size_t count) {
    std::vector<int> word;
    word.reserve(count);
    for (std::size_t index = 0; index < count; ++index) {
        auto [gap, successor] = first_return_big(z);
        word.push_back(gap);
        z = successor;
    }
    return {word, z};
}

int span(const std::vector<int>& word) {
    int total = 0;
    for (int gap : word) total += gap;
    return total;
}

std::string word_string(const std::vector<int>& word) {
    std::string result;
    for (std::size_t index = 0; index < word.size(); ++index) {
        if (index) result.push_back(',');
        result += std::to_string(word[index]);
    }
    return result;
}

void verify_witness(const std::vector<int>& word, std::uint64_t representative, int k) {
    const int total = span(word);
    if (k < 4 * total + 5) throw std::runtime_error("target below threshold");
    if (representative >= (std::uint64_t{1} << (2 * total))) {
        throw std::runtime_error("representative outside canonical cylinder");
    }

    auto [left_word, left] = follow_big(cpp_int{representative}, word.size());
    if (left_word != word) throw std::runtime_error("representative replay failed");

    const int source_bit = k + 2 * total - 1;
    const cpp_int lifted = cpp_int{representative} + (cpp_int{1} << source_bit);
    auto [right_word, right] = follow_big(lifted, word.size());
    if (right_word != word) throw std::runtime_error("lift changed return word");

    const cpp_int mask = (cpp_int{1} << k) - 1;
    const cpp_int difference = (left ^ right) & mask;
    if (difference != (cpp_int{1} << (k - 1))) {
        throw std::runtime_error("top target bit did not flip exactly");
    }
}
}  // namespace

int main() {
    std::map<std::vector<int>, std::uint64_t> representatives;
    const std::uint64_t states = std::uint64_t{1} << (2 * SPAN_CAP);
    for (std::uint64_t start = 0; start < states; ++start) {
        std::uint64_t z = start;
        std::vector<int> word;
        int total = 0;
        while (true) {
            auto [gap, successor] = first_return64(z);
            if (total + gap > SPAN_CAP) break;
            total += gap;
            word.push_back(gap);
            auto [it, inserted] = representatives.emplace(word, start);
            if (!inserted && start < it->second) it->second = start;
            z = successor;
        }
    }

    std::map<int, int> span_counts;
    std::map<int, int> length_counts;
    std::uint64_t checksum = 1469598103934665603ULL;
    std::uint64_t checks = 0;
    for (const auto& [word, representative] : representatives) {
        const int total = span(word);
        ++span_counts[total];
        ++length_counts[static_cast<int>(word.size())];
        const int threshold = 4 * total + 5;
        for (int offset = 0; offset < WIDTH_SAMPLES; ++offset) {
            verify_witness(word, representative, threshold + offset);
            ++checks;
        }
        checksum ^= representative + (static_cast<std::uint64_t>(total) << 32)
            + static_cast<std::uint64_t>(word.size());
        checksum *= 1099511628211ULL;
        for (int gap : word) {
            checksum ^= static_cast<std::uint64_t>(gap);
            checksum *= 1099511628211ULL;
        }
        std::cout << "word=" << word_string(word)
                  << " span=" << total
                  << " representative=" << representative
                  << " threshold=" << threshold
                  << " checks=" << WIDTH_SAMPLES << '\n';
    }

    std::cout << "span_cap=" << SPAN_CAP << '\n';
    std::cout << "source_coordinates_exhausted=" << states << '\n';
    std::cout << "realized_return_words=" << representatives.size() << '\n';
    std::cout << "word_counts_by_span=";
    bool first = true;
    for (const auto& [key, value] : span_counts) {
        if (!first) std::cout << ',';
        first = false;
        std::cout << key << ':' << value;
    }
    std::cout << '\n';
    std::cout << "word_counts_by_length=";
    first = true;
    for (const auto& [key, value] : length_counts) {
        if (!first) std::cout << ',';
        first = false;
        std::cout << key << ':' << value;
    }
    std::cout << '\n';
    std::cout << "witness_checks=" << checks << '\n';
    std::cout << "checksum=0x" << std::hex << std::setw(16) << std::setfill('0')
              << checksum << std::dec << '\n';
    std::cout << "exact_eventual_precision=k+2B_for_k_at_least_4B_plus_5\n";
    return 0;
}
