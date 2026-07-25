#include <algorithm>
#include <array>
#include <cstdint>
#include <iomanip>
#include <iostream>
#include <map>
#include <stdexcept>
#include <utility>
#include <vector>

namespace {
constexpr int MAX_BITS = 20;
constexpr int SEMICONJUGACY_BITS = 14;
constexpr int MAX_BLOCKS = 10;
constexpr int RETURN_COUNT = 4;

std::uint64_t advance_fringe(std::uint64_t state) {
    const std::uint64_t row = 1 | (state << 1);
    const std::uint64_t odd = row ^ ((row >> 1) | (row >> 2));
    return (odd << 1) ^ (odd | (odd >> 1));
}

std::uint64_t renormalized_front(std::uint64_t value) {
    return advance_fringe(value) >> 2;
}

int bit_length(std::uint64_t value) {
    int result = 0;
    while (value) {
        ++result;
        value >>= 1;
    }
    return result;
}

unsigned bit(std::uint64_t value, int index) {
    if (index < 0 || index >= 64) return 0;
    return static_cast<unsigned>((value >> index) & 1);
}

std::uint64_t formula_front(std::uint64_t value) {
    std::uint64_t result = 0;
    const int length = bit_length(value);
    for (int index = 0; index < length; ++index) {
        const unsigned odd0 = bit(value, index)
            ^ (bit(value, index + 1) | bit(value, index + 2));
        const unsigned odd1 = bit(value, index + 1)
            ^ (bit(value, index + 2) | bit(value, index + 3));
        const unsigned odd2 = bit(value, index + 2)
            ^ (bit(value, index + 3) | bit(value, index + 4));
        const unsigned output = odd0 ^ (odd1 | odd2);
        result |= static_cast<std::uint64_t>(output) << index;
    }
    return result;
}

std::uint64_t inverse_front(std::uint64_t value) {
    std::uint64_t result = 0;
    for (int index = bit_length(value) - 1; index >= 0; --index) {
        const unsigned bit1 = bit(result, index + 1);
        const unsigned bit2 = bit(result, index + 2);
        const unsigned bit3 = bit(result, index + 3);
        const unsigned bit4 = bit(result, index + 4);
        const unsigned odd0_without = bit1 | bit2;
        const unsigned odd1 = bit1 ^ (bit2 | bit3);
        const unsigned odd2 = bit2 ^ (bit3 | bit4);
        const unsigned correction = odd0_without ^ (odd1 | odd2);
        const unsigned source = bit(value, index) ^ correction;
        result |= static_cast<std::uint64_t>(source) << index;
    }
    return result;
}

std::uint64_t iterate_front(std::uint64_t value, int blocks) {
    for (int step = 0; step < blocks; ++step) value = renormalized_front(value);
    return value;
}

std::uint64_t iterate_fringe(std::uint64_t state, int blocks) {
    for (int step = 0; step < blocks; ++step) state = advance_fringe(state);
    return state;
}

std::pair<int, std::uint64_t> first_return(std::uint64_t z) {
    std::uint64_t state = 4 * z;
    for (int gap = 1; gap <= 5; ++gap) {
        state = advance_fringe(state);
        if ((state & 3) == 0) return {gap, state >> 2};
    }
    throw std::runtime_error("five-block return bound failed");
}

struct ReturnReplay {
    std::vector<int> word;
    int span = 0;
    std::uint64_t final = 0;
};

ReturnReplay follow_returns(std::uint64_t z, int count) {
    ReturnReplay replay;
    replay.final = z;
    for (int index = 0; index < count; ++index) {
        auto [gap, successor] = first_return(replay.final);
        replay.word.push_back(gap);
        replay.span += gap;
        replay.final = successor;
    }
    return replay;
}

bool power_of_two(std::uint64_t value) {
    return value != 0 && (value & (value - 1)) == 0;
}
}  // namespace

int main() {
    std::uint64_t formula_checks = 0;
    std::uint64_t inverse_checks = 0;
    for (std::uint64_t value = 1; value < (std::uint64_t{1} << MAX_BITS); ++value) {
        const std::uint64_t front = renormalized_front(value);
        if (front != formula_front(value)) throw std::runtime_error("formula mismatch");
        if (bit_length(front) != bit_length(value)) throw std::runtime_error("length mismatch");
        if (inverse_front(front) != value) throw std::runtime_error("left inverse failed");
        if (renormalized_front(inverse_front(value)) != value) {
            throw std::runtime_error("right inverse failed");
        }
        ++formula_checks;
        inverse_checks += 2;
    }

    std::uint64_t truncation_checks = 0;
    std::uint64_t semiconjugacy_checks = 0;
    std::uint64_t return_bridge_checks = 0;
    for (std::uint64_t value = 1; value < (std::uint64_t{1} << SEMICONJUGACY_BITS); ++value) {
        for (int shift = 0; shift <= SEMICONJUGACY_BITS; ++shift) {
            if ((advance_fringe(value) >> (shift + 2))
                != renormalized_front(value >> shift)) {
                throw std::runtime_error("truncation commutation failed");
            }
            ++truncation_checks;
        }
        for (int blocks = 0; blocks <= MAX_BLOCKS; ++blocks) {
            const std::uint64_t left = iterate_fringe(4 * value, blocks) >> (2 * blocks + 2);
            const std::uint64_t right = iterate_front(value, blocks);
            if (left != right) throw std::runtime_error("semiconjugacy failed");
            ++semiconjugacy_checks;
        }
        const ReturnReplay replay = follow_returns(value, RETURN_COUNT);
        if ((replay.final >> (2 * replay.span)) != iterate_front(value, replay.span)) {
            throw std::runtime_error("return bridge failed");
        }
        std::uint64_t recovered = replay.final >> (2 * replay.span);
        for (int step = 0; step < replay.span; ++step) recovered = inverse_front(recovered);
        if (recovered != value) throw std::runtime_error("return recovery failed");
        const ReturnReplay second = follow_returns(recovered, RETURN_COUNT);
        if (second.word != replay.word || second.span != replay.span || second.final != replay.final) {
            throw std::runtime_error("history replay failed");
        }
        ++return_bridge_checks;
    }

    std::uint64_t cycle_states = 0;
    std::uint64_t checksum = 1469598103934665603ULL;
    for (int bits_count = 1; bits_count <= MAX_BITS; ++bits_count) {
        const std::uint64_t lower = std::uint64_t{1} << (bits_count - 1);
        const std::uint64_t upper = std::uint64_t{1} << bits_count;
        std::vector<unsigned char> seen(upper - lower, 0);
        std::map<std::uint64_t, std::uint64_t> counts;
        for (std::uint64_t start = lower; start < upper; ++start) {
            if (seen[start - lower]) continue;
            std::uint64_t current = start;
            std::uint64_t length = 0;
            while (!seen[current - lower]) {
                seen[current - lower] = 1;
                current = renormalized_front(current);
                ++length;
            }
            if (current != start) throw std::runtime_error("cycles merged");
            if (!power_of_two(length)) throw std::runtime_error("non-dyadic cycle");
            ++counts[length];
        }
        cycle_states += upper - lower;
        const std::uint64_t maximum = counts.rbegin()->first;
        std::cout << "shell bits=" << bits_count
                  << " states=" << (upper - lower)
                  << " max_cycle=" << maximum
                  << " cycles=";
        bool first = true;
        for (const auto& [length, count] : counts) {
            if (!first) std::cout << ',';
            first = false;
            std::cout << length << ':' << count;
            checksum ^= length + (count << 20) + static_cast<std::uint64_t>(bits_count);
            checksum *= 1099511628211ULL;
        }
        std::cout << '\n';
    }

    std::cout << "formula_checks=" << formula_checks << '\n';
    std::cout << "inverse_checks=" << inverse_checks << '\n';
    std::cout << "truncation_checks=" << truncation_checks << '\n';
    std::cout << "semiconjugacy_checks=" << semiconjugacy_checks << '\n';
    std::cout << "return_bridge_checks=" << return_bridge_checks << '\n';
    std::cout << "cycle_states=" << cycle_states << '\n';
    std::cout << "checksum=0x" << std::hex << std::setw(16) << std::setfill('0')
              << checksum << std::dec << '\n';
    std::cout << "lossless_return_high_front=true\n";
    return 0;
}
