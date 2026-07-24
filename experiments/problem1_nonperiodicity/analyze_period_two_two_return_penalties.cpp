#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <map>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>

namespace {
constexpr std::array<char, 3> LETTERS{'t', 'p', 'u'};
constexpr std::array<char, 2> PHASES{'p', 'u'};
constexpr std::array<int, 4> GAPS{2, 3, 4, 5};
constexpr int MAXIMUM_FINAL_DEPTH = 14;

uint32_t width_mask(int width) {
    return width == 0 ? 0 : ((uint32_t{1} << width) - 1);
}

uint32_t forward_generator(char letter, uint32_t state, int width) {
    const uint32_t stepped =
        (state ^ ((state << 1) | (state << 2))) & width_mask(width);
    if (letter == 't') return stepped;
    if (letter == 'u') return stepped ^ 1;
    if (letter == 'p') return stepped ^ 1 ^ ((state & 1) == 0 ? 2 : 0);
    throw std::invalid_argument("unknown generator");
}

uint32_t inverse_t_mod(uint32_t output, int width) {
    output &= width_mask(width);
    uint32_t state = 0;
    for (int position = 0; position < width; ++position) {
        uint32_t previous = 0;
        if (position >= 1) previous |= (state >> (position - 1)) & 1;
        if (position >= 2) previous |= (state >> (position - 2)) & 1;
        state |= ((((output >> position) & 1) ^ previous) << position);
    }
    return state;
}

uint32_t inverse_generator_mod(char letter, uint32_t output, int width) {
    output &= width_mask(width);
    if (letter == 't') return inverse_t_mod(output, width);
    if (letter == 'u') return inverse_t_mod(output ^ 1, width);
    if (letter == 'p') {
        const uint32_t recovered_low_bit = (output & 1) ^ 1;
        return inverse_t_mod(
            output ^ 1 ^ (recovered_low_bit == 0 ? 2 : 0), width
        );
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
    int length, std::string& prefix, std::vector<std::string>& output
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
    std::vector<uint8_t> distance(state_count, 255);
    std::vector<uint32_t> queue;
    queue.reserve(state_count);
    const uint32_t start = forward_generator(phase, 0, width);
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
    long candidates = 0;
    long zero = 0;
    int minimum = 255;
    int maximum = -1;
    std::map<int, long> histogram;
    int minimum_depth = -1;
    std::string minimum_prefix;
};

std::string return_extension(int gap) {
    return std::string(gap - 1, 't') + 'u';
}

using PairKey = std::pair<int, int>;
using SummaryMap = std::map<PairKey, Summary>;

SummaryMap classify_phase(char phase) {
    std::unordered_map<int, std::vector<uint8_t>> distances;
    for (int depth = 1; depth <= MAXIMUM_FINAL_DEPTH; ++depth) {
        distances.emplace(depth, phase_distances(depth, phase));
    }

    SummaryMap summaries;
    for (int first_gap : GAPS) {
        for (int second_gap : GAPS) {
            Summary summary;
            const std::string extension =
                return_extension(first_gap) + return_extension(second_gap);
            for (int base_depth = 1;
                 base_depth + first_gap + second_gap <= MAXIMUM_FINAL_DEPTH;
                 ++base_depth) {
                std::vector<std::string> prefixes;
                std::string prefix;
                generate_prefixes(base_depth, prefix, prefixes);
                for (const std::string& candidate : prefixes) {
                    const std::string final_prefix = candidate + extension;
                    if (!locally_admissible(final_prefix)) continue;
                    const int final_depth =
                        base_depth + first_gap + second_gap;
                    const int initial = 1 + distances.at(base_depth).at(
                        survivor_for_prefix(candidate)
                    );
                    const int final = 1 + distances.at(final_depth).at(
                        survivor_for_prefix(final_prefix)
                    );
                    const int penalty = final - initial;
                    if (penalty < 0) {
                        throw std::runtime_error("projection monotonicity failed");
                    }
                    ++summary.candidates;
                    ++summary.histogram[penalty];
                    if (penalty == 0) ++summary.zero;
                    if (penalty < summary.minimum) {
                        summary.minimum = penalty;
                        summary.minimum_depth = base_depth;
                        summary.minimum_prefix = candidate;
                    }
                    summary.maximum = std::max(summary.maximum, penalty);
                }
            }
            summaries[{first_gap, second_gap}] = summary;
        }
    }
    return summaries;
}

void print_summary(char phase, int first_gap, int second_gap, const Summary& row) {
    std::cout << "pair=" << first_gap << ',' << second_gap
              << " phase=" << phase
              << " candidates=" << row.candidates
              << " zero=" << row.zero;
    if (row.candidates == 0) {
        std::cout << " minimum=null maximum=null histogram={}\n";
        return;
    }
    std::cout << " minimum=" << row.minimum
              << " maximum=" << row.maximum
              << " minimum_example=" << row.minimum_depth << ':'
              << row.minimum_prefix << " histogram={";
    bool first = true;
    for (const auto& [penalty, count] : row.histogram) {
        if (!first) std::cout << ',';
        first = false;
        std::cout << penalty << ':' << count;
    }
    std::cout << "}\n";
}
}  // namespace

int main() {
    long total_cases = 0;
    long total_zero = 0;
    std::cout << "maximum_final_depth=" << MAXIMUM_FINAL_DEPTH << '\n';
    std::cout << "forbidden=uu,ttttt,ututtu\n";
    for (char phase : PHASES) {
        const SummaryMap summaries = classify_phase(phase);
        for (int first_gap : GAPS) {
            for (int second_gap : GAPS) {
                const Summary& row = summaries.at({first_gap, second_gap});
                print_summary(phase, first_gap, second_gap, row);
                total_cases += row.candidates;
                total_zero += row.zero;
            }
        }
    }
    std::cout << "total_phase_gap_pair_cases=" << total_cases << '\n';
    std::cout << "total_zero_two_return_penalties=" << total_zero << '\n';
    return 0;
}
