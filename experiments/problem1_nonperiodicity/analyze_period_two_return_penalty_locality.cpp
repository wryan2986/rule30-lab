#include <array>
#include <cstdint>
#include <iostream>
#include <map>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>

namespace {

constexpr std::array<char, 3> LETTERS{'t', 'p', 'u'};
constexpr std::array<char, 2> PHASES{'p', 'u'};
constexpr std::array<int, 4> GAPS{2, 3, 4, 5};
constexpr int MAXIMUM_FINAL_DEPTH = 12;

constexpr std::array<int, 23> KAPPA_P{
    0, 1, 3, 7, 8, 8, 12, 13, 17, 17, 17, 21, 28, 30, 33, 34, 36, 40,
    40, 42, 47, 49, 51,
};
constexpr std::array<int, 23> KAPPA_U{
    0, 2, 2, 2, 7, 12, 14, 14, 14, 18, 19, 26, 27, 30, 30, 30, 30, 40,
    42, 42, 49, 52, 52,
};

uint32_t width_mask(int width) {
    if (width < 0 || width > 30) {
        throw std::invalid_argument("controlled width outside 0..30");
    }
    return width == 0 ? 0 : ((uint32_t{1} << width) - 1);
}

uint32_t forward_generator(char letter, uint32_t state, int width) {
    const uint32_t stepped =
        (state ^ ((state << 1) | (state << 2))) & width_mask(width);
    if (letter == 't') return stepped;
    if (letter == 'u') return stepped ^ 1;
    if (letter == 'p') {
        return stepped ^ 1 ^ ((state & 1) == 0 ? 2 : 0);
    }
    throw std::invalid_argument("unknown generator");
}

uint32_t inverse_t_mod(uint32_t output, int width) {
    output &= width_mask(width);
    uint32_t state = 0;
    for (int position = 0; position < width; ++position) {
        uint32_t previous = 0;
        if (position >= 1) previous |= (state >> (position - 1)) & 1;
        if (position >= 2) previous |= (state >> (position - 2)) & 1;
        const uint32_t bit = ((output >> position) & 1) ^ previous;
        state |= bit << position;
    }
    return state;
}

uint32_t inverse_generator_mod(char letter, uint32_t output, int width) {
    output &= width_mask(width);
    if (letter == 't') return inverse_t_mod(output, width);
    if (letter == 'u') return inverse_t_mod(output ^ 1, width);
    if (letter == 'p') {
        const uint32_t recovered_low_bit = (output & 1) ^ 1;
        const uint32_t adjusted =
            output ^ 1 ^ (recovered_low_bit == 0 ? 2 : 0);
        return inverse_t_mod(adjusted, width);
    }
    throw std::invalid_argument("unknown inverse generator");
}

uint32_t backward_zero_branch(char branch, uint32_t successor, int width) {
    const int inner_width = width - 2;
    uint32_t state = inverse_generator_mod(branch, successor, inner_width);
    state = inverse_generator_mod('p', state, inner_width);
    return ((state << 2) | 3) & width_mask(width);
}

uint32_t survivor_for_prefix(const std::string& prefix) {
    uint32_t state = 0;
    int precision = 0;
    for (auto iterator = prefix.rbegin(); iterator != prefix.rend(); ++iterator) {
        precision += 2;
        state = backward_zero_branch(*iterator, state, precision);
    }
    return state;
}

bool locally_admissible(const std::string& word) {
    return word.find("uu") == std::string::npos
        && word.find("ttttt") == std::string::npos
        && word.find("ututtu") == std::string::npos;
}

void generate_prefixes(
    int length,
    std::string& prefix,
    std::vector<std::string>& output
) {
    if (static_cast<int>(prefix.size()) == length) {
        if (!prefix.empty() && prefix.back() == 'u') output.push_back(prefix);
        return;
    }
    for (char letter : {'t', 'u'}) {
        prefix.push_back(letter);
        if (locally_admissible(prefix)) {
            generate_prefixes(length, prefix, output);
        }
        prefix.pop_back();
    }
}

std::vector<uint8_t> phase_distances(int depth, char phase) {
    const int width = 2 * depth;
    const uint32_t state_count = uint32_t{1} << width;
    const uint32_t start = forward_generator(phase, 0, width);
    std::vector<uint8_t> distance(state_count, 255);
    std::vector<uint32_t> queue;
    queue.reserve(state_count);
    distance[start] = 0;
    queue.push_back(start);
    for (std::size_t head = 0; head < queue.size(); ++head) {
        const uint32_t state = queue[head];
        const uint8_t next_distance = distance[state] + 1;
        for (char letter : LETTERS) {
            const uint32_t image = forward_generator(letter, state, width);
            if (distance[image] == 255) {
                distance[image] = next_distance;
                queue.push_back(image);
            }
        }
    }
    return distance;
}

struct Summary {
    int candidates = 0;
    int zero = 0;
    int positive = 0;
    int minimum = 255;
    int maximum = -1;
    std::map<int, int> histogram;
    std::string first_zero_prefix;
    std::string first_positive_prefix;
    int first_zero_depth = -1;
    int first_positive_depth = -1;
};

void print_string(const std::string& value) {
    std::cout << '"' << value << '"';
}

void print_summary(const Summary& summary) {
    std::cout << "{\"candidates\":" << summary.candidates
              << ",\"zero_penalty_count\":" << summary.zero
              << ",\"positive_penalty_count\":" << summary.positive
              << ",\"minimum_penalty\":" << summary.minimum
              << ",\"maximum_penalty\":" << summary.maximum
              << ",\"histogram\":{";
    bool first = true;
    for (const auto& [penalty, count] : summary.histogram) {
        if (!first) std::cout << ',';
        first = false;
        std::cout << '"' << penalty << "\":" << count;
    }
    std::cout << "},\"first_zero_example\":";
    if (summary.first_zero_depth < 0) {
        std::cout << "null";
    } else {
        std::cout << "{\"base_depth\":" << summary.first_zero_depth
                  << ",\"prefix\":";
        print_string(summary.first_zero_prefix);
        std::cout << '}';
    }
    std::cout << ",\"first_positive_example\":";
    if (summary.first_positive_depth < 0) {
        std::cout << "null";
    } else {
        std::cout << "{\"base_depth\":" << summary.first_positive_depth
                  << ",\"prefix\":";
        print_string(summary.first_positive_prefix);
        std::cout << '}';
    }
    std::cout << '}';
}

}  // namespace

int main() {
    std::unordered_map<int, std::vector<uint8_t>> p_distance;
    std::unordered_map<int, std::vector<uint8_t>> u_distance;
    for (int depth = 1; depth <= MAXIMUM_FINAL_DEPTH; ++depth) {
        p_distance.emplace(depth, phase_distances(depth, 'p'));
        u_distance.emplace(depth, phase_distances(depth, 'u'));
    }

    std::cout << "{\"maximum_final_depth\":" << MAXIMUM_FINAL_DEPTH
              << ",\"known_forbidden_factors\":[\"uu\",\"ttttt\",\"ututtu\"]"
              << ",\"return_gap_rows\":{";
    bool first_gap = true;
    for (int gap : GAPS) {
        if (!first_gap) std::cout << ',';
        first_gap = false;
        std::cout << '"' << gap << "\":{";
        bool first_phase = true;
        const std::string extension(gap - 1, 't');
        for (char phase : PHASES) {
            if (!first_phase) std::cout << ',';
            first_phase = false;
            Summary summary;
            for (int base_depth = 1;
                 base_depth + gap <= MAXIMUM_FINAL_DEPTH;
                 ++base_depth) {
                std::vector<std::string> prefixes;
                std::string prefix;
                generate_prefixes(base_depth, prefix, prefixes);
                for (const std::string& candidate : prefixes) {
                    const std::string extended = candidate + extension + 'u';
                    if (!locally_admissible(extended)) continue;
                    const uint32_t current_target = survivor_for_prefix(candidate);
                    const uint32_t following_target = survivor_for_prefix(extended);
                    const int current = 1 + (
                        phase == 'p'
                            ? p_distance.at(base_depth)[current_target]
                            : u_distance.at(base_depth)[current_target]
                    );
                    const int final_depth = base_depth + gap;
                    const int following = 1 + (
                        phase == 'p'
                            ? p_distance.at(final_depth)[following_target]
                            : u_distance.at(final_depth)[following_target]
                    );
                    const int penalty = following - current;
                    if (penalty < 0) {
                        throw std::runtime_error("projection monotonicity failed");
                    }
                    ++summary.candidates;
                    ++summary.histogram[penalty];
                    summary.minimum = std::min(summary.minimum, penalty);
                    summary.maximum = std::max(summary.maximum, penalty);
                    if (penalty == 0) {
                        ++summary.zero;
                        if (summary.first_zero_depth < 0) {
                            summary.first_zero_depth = base_depth;
                            summary.first_zero_prefix = candidate;
                        }
                    } else {
                        ++summary.positive;
                        if (summary.first_positive_depth < 0) {
                            summary.first_positive_depth = base_depth;
                            summary.first_positive_prefix = candidate;
                        }
                    }
                }
            }
            std::cout << '"' << phase << "\":";
            print_summary(summary);
        }
        std::cout << '}';
    }
    std::cout << "},\"actual_exact_returns_through_depth_21\":[";
    constexpr std::array<int, 7> POSITIONS{0, 4, 6, 11, 13, 18, 20};
    for (std::size_t index = 0; index + 1 < POSITIONS.size(); ++index) {
        if (index) std::cout << ',';
        const int base_depth = POSITIONS[index] + 1;
        const int final_depth = POSITIONS[index + 1] + 1;
        std::cout << "{\"return_index\":" << index
                  << ",\"gap\":" << POSITIONS[index + 1] - POSITIONS[index]
                  << ",\"base_depth\":" << base_depth
                  << ",\"final_depth\":" << final_depth
                  << ",\"p_penalty\":" << KAPPA_P[final_depth] - KAPPA_P[base_depth]
                  << ",\"u_penalty\":" << KAPPA_U[final_depth] - KAPPA_U[base_depth]
                  << '}';
    }
    std::cout << "]}\n";
    return 0;
}
