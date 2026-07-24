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

namespace {

constexpr std::array<char, 3> LETTERS{'t', 'p', 'u'};
constexpr std::array<int, 23> KAPPA_P{
    0, 1, 3, 7, 8, 8, 12, 13, 17, 17, 17, 21, 28, 30, 33, 34, 36, 40,
    40, 42, 47, 49, 51,
};
constexpr std::array<int, 23> KAPPA_U{
    0, 2, 2, 2, 7, 12, 14, 14, 14, 18, 19, 26, 27, 30, 30, 30, 30, 40,
    42, 42, 49, 52, 52,
};

uint64_t width_mask(int width) {
    if (width < 0 || width > 62) {
        throw std::invalid_argument("width must lie between zero and 62");
    }
    return width == 0 ? 0 : ((uint64_t{1} << width) - 1);
}

uint64_t forward_generator(char letter, uint64_t state, int width) {
    const uint64_t stepped =
        (state ^ ((state << 1) | (state << 2))) & width_mask(width);
    if (letter == 't') return stepped;
    if (letter == 'u') return stepped ^ 1;
    if (letter == 'p') {
        return stepped ^ 1 ^ ((state & 1) == 0 ? 2 : 0);
    }
    throw std::invalid_argument("unknown generator");
}

uint64_t inverse_t_mod(uint64_t output, int width) {
    output &= width_mask(width);
    uint64_t state = 0;
    for (int position = 0; position < width; ++position) {
        uint64_t previous = 0;
        if (position >= 1) previous |= (state >> (position - 1)) & 1;
        if (position >= 2) previous |= (state >> (position - 2)) & 1;
        const uint64_t bit = ((output >> position) & 1) ^ previous;
        state |= bit << position;
    }
    return state;
}

uint64_t inverse_generator_mod(char letter, uint64_t output, int width) {
    output &= width_mask(width);
    if (letter == 't') return inverse_t_mod(output, width);
    if (letter == 'u') return inverse_t_mod(output ^ 1, width);
    if (letter == 'p') {
        const uint64_t recovered_low_bit = (output & 1) ^ 1;
        const uint64_t adjusted =
            output ^ 1 ^ (recovered_low_bit == 0 ? 2 : 0);
        return inverse_t_mod(adjusted, width);
    }
    throw std::invalid_argument("unknown generator");
}

uint64_t fringe_step(uint64_t state) {
    const uint64_t packed = 1 + 2 * state;
    const uint64_t odd = packed ^ ((packed >> 1) | (packed >> 2));
    return (odd << 1) ^ (odd | (odd >> 1));
}

std::vector<char> actual_driver(int length) {
    uint64_t state = 0;
    std::vector<char> result;
    result.reserve(length);
    for (int index = 0; index < length; ++index) {
        result.push_back((state & 3) == 0 ? 'u' : 't');
        state = fringe_step(state);
    }
    return result;
}

uint64_t backward_zero_branch(char branch, uint64_t successor, int width) {
    const int inner_width = width - 2;
    uint64_t state = inverse_generator_mod(branch, successor, inner_width);
    state = inverse_generator_mod('p', state, inner_width);
    return ((state << 2) | 3) & width_mask(width);
}

uint64_t actual_survivor_residue(int depth) {
    const auto driver = actual_driver(depth);
    uint64_t state = 0;
    int precision = 0;
    for (auto iterator = driver.rbegin(); iterator != driver.rend(); ++iterator) {
        precision += 2;
        state = backward_zero_branch(*iterator, state, precision);
    }
    return state;
}

std::vector<std::pair<int, int>> actual_u_return_intervals(int count) {
    std::vector<int> positions;
    uint64_t state = 0;
    int position = 0;
    while (static_cast<int>(positions.size()) < count + 1) {
        if ((state & 3) == 0) positions.push_back(position);
        state = fringe_step(state);
        ++position;
    }
    std::vector<std::pair<int, int>> result;
    for (int index = 0; index < count; ++index) {
        const int gap = positions[index + 1] - positions[index];
        if (gap < 2 || gap > 5) {
            throw std::runtime_error("actual return gap escaped 2..5");
        }
        result.emplace_back(positions[index], positions[index + 1]);
    }
    return result;
}

uint64_t actual_block_code(int base_depth, int span) {
    const uint64_t lower = actual_survivor_residue(base_depth);
    const uint64_t upper = actual_survivor_residue(base_depth + span);
    if ((upper & width_mask(2 * base_depth)) != lower) {
        throw std::runtime_error("survivor residues failed to project");
    }
    return (upper - lower) >> (2 * base_depth);
}

uint64_t fnv1a64(const std::vector<uint8_t>& values) {
    uint64_t hash = 1469598103934665603ULL;
    for (uint8_t value : values) {
        hash ^= value;
        hash *= 1099511628211ULL;
    }
    return hash;
}

struct ProfileSummary {
    int minimum;
    int actual_length;
    int penalty;
    int minimizer_count;
    int maximum;
    uint64_t digest;
    std::map<int, int> histogram;
};

ProfileSummary return_lift_profile(
    int base_depth,
    int span,
    char phase,
    uint64_t actual_code
) {
    const int final_depth = base_depth + span;
    if (final_depth > 12) {
        throw std::invalid_argument("controlled final depth exceeds twelve");
    }
    const int width = 2 * final_depth;
    const uint32_t state_count = uint32_t{1} << width;
    const uint32_t block_count = uint32_t{1} << (2 * span);
    const uint64_t base = actual_survivor_residue(base_depth);

    std::vector<int32_t> target_code(state_count, -1);
    for (uint32_t code = 0; code < block_count; ++code) {
        const uint32_t target = static_cast<uint32_t>(
            base + (static_cast<uint64_t>(code) << (2 * base_depth))
        );
        target_code[target] = static_cast<int32_t>(code);
    }

    const uint32_t start = static_cast<uint32_t>(
        forward_generator(phase, 0, width)
    );
    std::vector<uint8_t> distance(state_count, 255);
    std::vector<uint32_t> queue;
    queue.reserve(state_count);
    std::vector<uint8_t> profile(block_count, 255);
    distance[start] = 0;
    queue.push_back(start);
    uint32_t remaining = block_count;
    if (target_code[start] >= 0) {
        profile[target_code[start]] = 1;
        --remaining;
    }

    for (std::size_t head = 0; head < queue.size() && remaining; ++head) {
        const uint32_t state = queue[head];
        const uint8_t next_distance = distance[state] + 1;
        for (char letter : LETTERS) {
            const uint32_t image = static_cast<uint32_t>(
                forward_generator(letter, state, width)
            );
            if (distance[image] != 255) continue;
            distance[image] = next_distance;
            queue.push_back(image);
            const int32_t code = target_code[image];
            if (code >= 0 && profile[code] == 255) {
                profile[code] = next_distance + 1;
                --remaining;
            }
        }
    }
    if (remaining) throw std::runtime_error("unreached block-lift target");

    const auto [minimum_it, maximum_it] =
        std::minmax_element(profile.begin(), profile.end());
    ProfileSummary summary{};
    summary.minimum = *minimum_it;
    summary.maximum = *maximum_it;
    summary.actual_length = profile.at(actual_code);
    summary.penalty = summary.actual_length - summary.minimum;
    summary.minimizer_count = std::count(
        profile.begin(), profile.end(), static_cast<uint8_t>(summary.minimum)
    );
    summary.digest = fnv1a64(profile);
    for (uint8_t value : profile) ++summary.histogram[value];
    return summary;
}

void print_histogram(const std::map<int, int>& histogram) {
    bool first = true;
    std::cout << '{';
    for (const auto& [distance, count] : histogram) {
        if (!first) std::cout << ',';
        first = false;
        std::cout << distance << ':' << count;
    }
    std::cout << '}';
}

}  // namespace

int main(int argc, char** argv) {
    int maximum_returns = 3;
    if (argc >= 2) maximum_returns = std::stoi(argv[1]);
    if (maximum_returns < 1 || maximum_returns > 3) {
        throw std::invalid_argument("maximum returns must lie in 1..3");
    }

    const auto intervals = actual_u_return_intervals(maximum_returns);
    std::array<int, 2> cumulative{0, 0};
    std::cout << "status finite-exhaustive\n";
    std::cout << "maximum_returns " << maximum_returns << '\n';

    for (int index = 0; index < maximum_returns; ++index) {
        const int left = intervals[index].first;
        const int right = intervals[index].second;
        const int gap = right - left;
        const int base_depth = left + 1;
        const int final_depth = right + 1;
        const uint64_t code = actual_block_code(base_depth, gap);

        std::cout << "return " << index
                  << " driver=" << left << ".." << right
                  << " gap=" << gap
                  << " depth=" << base_depth << ".." << final_depth
                  << " code=" << code << " digits=";
        for (int digit = 0; digit < gap; ++digit) {
            if (digit) std::cout << ',';
            std::cout << ((code >> (2 * digit)) & 3);
        }
        std::cout << '\n';

        for (int phase_index = 0; phase_index < 2; ++phase_index) {
            const char phase = phase_index == 0 ? 'p' : 'u';
            const auto summary =
                return_lift_profile(base_depth, gap, phase, code);
            const auto& kappa = phase == 'p' ? KAPPA_P : KAPPA_U;
            if (summary.minimum != kappa[base_depth]
                || summary.actual_length != kappa[final_depth]
                || summary.penalty != kappa[final_depth] - kappa[base_depth]) {
                throw std::runtime_error("profile theorem check failed");
            }
            cumulative[phase_index] += summary.penalty;
            std::cout << "phase " << phase
                      << " minimum=" << summary.minimum
                      << " actual=" << summary.actual_length
                      << " penalty=" << summary.penalty
                      << " minimizers=" << summary.minimizer_count
                      << " maximum=" << summary.maximum
                      << " fnv1a64=" << std::hex << std::setw(16)
                      << std::setfill('0') << summary.digest << std::dec
                      << std::setfill(' ') << " histogram=";
            print_histogram(summary.histogram);
            std::cout << '\n';
        }
    }

    const int first_depth = intervals.front().first + 1;
    const int final_depth = intervals.back().second + 1;
    if (cumulative[0] != KAPPA_P[final_depth] - KAPPA_P[first_depth]
        || cumulative[1] != KAPPA_U[final_depth] - KAPPA_U[first_depth]) {
        throw std::runtime_error("return penalties failed to telescope");
    }
    std::cout << "cumulative p=" << cumulative[0]
              << " u=" << cumulative[1] << '\n';
    std::cout << "scope no_infinite_penalty_recurrence_theorem\n";
    return 0;
}
