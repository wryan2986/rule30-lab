#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <limits>
#include <map>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>

using u64 = std::uint64_t;
constexpr int MAXK = 27;
constexpr int SCHEDULE_CAP = 64;

u64 forward_generator(char generator, u64 state) {
    const u64 stepped = state ^ ((state << 1) | (state << 2));
    if (generator == 't') return stepped;
    if (generator == 'u') return stepped ^ 1;
    if (generator == 'p') return stepped ^ 1 ^ ((state & 1) == 0 ? 2 : 0);
    throw std::runtime_error("unknown generator");
}

std::vector<u64> next_level(const std::vector<u64>& current) {
    std::vector<u64> output;
    output.reserve(current.size() * 3);
    for (u64 state : current) {
        output.push_back(forward_generator('t', state));
        output.push_back(forward_generator('u', state));
        output.push_back(forward_generator('p', state));
    }
    std::sort(output.begin(), output.end());
    output.erase(std::unique(output.begin(), output.end()), output.end());
    return output;
}

std::vector<std::vector<u64>> build_levels(char phase, int maximum_complexity) {
    std::vector<std::vector<u64>> levels(maximum_complexity + 1);
    levels[1] = {phase == 'p' ? 3ULL : 1ULL};
    for (int complexity = 2; complexity <= maximum_complexity; ++complexity) {
        levels[complexity] = next_level(levels[complexity - 1]);
    }
    return levels;
}

bool contains(const std::vector<u64>& values, u64 target) {
    return std::binary_search(values.begin(), values.end(), target);
}

unsigned fiber_mask(
    const std::vector<std::vector<u64>>& levels, int complexity, u64 quotient
) {
    unsigned mask = 0;
    for (int digit = 0; digit < 4; ++digit) {
        if (contains(levels[complexity + 1], 4 * quotient + unsigned(digit))) {
            mask |= 1u << digit;
        }
    }
    return mask;
}

u64 mask_sequence(
    const std::vector<std::vector<u64>>& levels,
    int complexity,
    u64 state,
    int depth
) {
    u64 result = 0;
    for (int step = 0; step < depth; ++step) {
        const u64 quotient = state >> 2;
        const int level = complexity - 1 - step;
        result |= u64(fiber_mask(levels, level, quotient)) << (4 * step);
        state = quotient;
    }
    return result;
}

bool dominates(u64 current, u64 shadow, int depth) {
    for (int step = 0; step < depth; ++step) {
        const unsigned a = (current >> (4 * step)) & 15;
        const unsigned b = (shadow >> (4 * step)) & 15;
        if (a & ~b) return false;
    }
    return true;
}

int defect_count(u64 shadow, int depth) {
    int result = 0;
    for (int step = 0; step < depth; ++step) {
        if (((shadow >> (4 * step)) & 15) != 15) ++result;
    }
    return result;
}

bool synchronized_or_full(u64 current, u64 shadow, int depth) {
    for (int step = 0; step < depth; ++step) {
        const unsigned a = (current >> (4 * step)) & 15;
        const unsigned b = (shadow >> (4 * step)) & 15;
        if (b != 15 && b != a) return false;
    }
    return true;
}

std::string sequence_string(u64 sequence, int depth) {
    std::string result;
    for (int step = 0; step < depth; ++step) {
        if (step) result.push_back(',');
        const unsigned mask = (sequence >> (4 * step)) & 15;
        for (int bit = 3; bit >= 0; --bit) {
            result.push_back(((mask >> bit) & 1) ? '1' : '0');
        }
    }
    return result;
}

std::string forced_zero_schedule(u64 state) {
    std::string word;
    for (int step = 0; step < SCHEDULE_CAP; ++step) {
        const u64 residue = state & 15;
        char branch;
        if (residue == 7) branch = 'u';
        else if (residue == 11) branch = 't';
        else return word;
        state = forward_generator(
            branch, forward_generator('p', (state - 3) >> 2)
        );
        word.push_back(branch);
    }
    throw std::runtime_error("forced schedule reached safety cap");
}

bool admissible(const std::string& word) {
    return word.find("uu") == std::string::npos
        && word.find("ttttt") == std::string::npos
        && word.find("ututtu") == std::string::npos;
}

using WeightedBelief = std::map<u64, int>;

WeightedBelief direct_weighted_belief(
    const std::vector<std::vector<u64>>& levels,
    int complexity,
    u64 current,
    int depth
) {
    const u64 mask = (u64{1} << (2 * depth)) - 1;
    const u64 residue = current & mask;
    const u64 current_sequence = mask_sequence(levels, complexity, current, depth);
    WeightedBelief result;
    for (u64 shadow : levels[complexity - 1]) {
        if ((shadow & mask) != residue) continue;
        const u64 shadow_sequence = mask_sequence(
            levels, complexity - 1, shadow, depth
        );
        if (dominates(current_sequence, shadow_sequence, depth)) {
            result[shadow] = defect_count(shadow_sequence, depth);
        }
    }
    return result;
}

WeightedBelief recursive_weighted_belief(
    const std::vector<std::vector<u64>>& levels,
    int complexity,
    u64 current,
    int depth
) {
    const int digit = current & 3;
    const u64 quotient = current >> 2;
    const unsigned current_mask = fiber_mask(levels, complexity - 1, quotient);
    WeightedBelief result;
    if (depth == 1) {
        for (u64 shadow : levels[complexity - 1]) {
            if ((shadow & 3) != u64(digit)) continue;
            const u64 shadow_quotient = shadow >> 2;
            const unsigned shadow_mask = fiber_mask(
                levels, complexity - 2, shadow_quotient
            );
            if (!(current_mask & ~shadow_mask)) {
                result[shadow] = shadow_mask != 15;
            }
        }
        return result;
    }

    const auto lower = recursive_weighted_belief(
        levels, complexity - 1, quotient, depth - 1
    );
    for (const auto& [shadow_quotient, lower_cost] : lower) {
        const u64 shadow = 4 * shadow_quotient + unsigned(digit);
        if (!contains(levels[complexity - 1], shadow)) continue;
        const unsigned shadow_mask = fiber_mask(
            levels, complexity - 2, shadow_quotient
        );
        if (current_mask & ~shadow_mask) continue;
        result[shadow] = lower_cost + (shadow_mask != 15);
    }
    return result;
}

u64 verify_weighted_recursion() {
    u64 checks = 0;
    for (char phase : {'p', 'u'}) {
        const auto levels = build_levels(phase, 9);
        for (int complexity = 2; complexity <= 9; ++complexity) {
            for (u64 current : levels[complexity]) {
                for (int depth = 1; depth < complexity; ++depth) {
                    if (direct_weighted_belief(levels, complexity, current, depth)
                        != recursive_weighted_belief(
                            levels, complexity, current, depth
                        )) {
                        throw std::runtime_error(
                            "direct and recursive weighted beliefs disagree"
                        );
                    }
                    ++checks;
                }
            }
        }
    }
    return checks;
}

struct Occurrence {
    u64 current;
    u64 residue;
    u64 current_sequence;
    u64 best_shadow = 0;
    u64 best_sequence = 0;
    int cut;
    int depth;
    int best_defects = 999;
};

int main() {
    const u64 recursive_checks = verify_weighted_recursion();
    const auto levels = build_levels('u', MAXK);
    u64 outputs = 0;
    for (int complexity = 1; complexity <= MAXK; ++complexity) {
        outputs += levels[complexity].size();
    }

    u64 total_occurrences = 0;
    u64 dominant_failures = 0;
    u64 synchronized_failures = 0;
    std::map<int, u64> defect_histogram;
    std::vector<Occurrence> exceptions;

    for (int complexity = 2; complexity <= MAXK; ++complexity) {
        std::vector<Occurrence> occurrences;
        int maximum_depth = 0;
        std::vector<std::unordered_map<u64, std::vector<int>>> lookup(20);

        for (u64 current : levels[complexity]) {
            if ((current & 3) != 3) continue;
            const std::string schedule = forced_zero_schedule(current);
            for (int cut = 0; cut <= static_cast<int>(schedule.size()); ++cut) {
                if (schedule.compare(cut, 6, "ututut") != 0) continue;
                if (!admissible(schedule.substr(0, cut) + "utututu")) continue;
                const int depth = cut + 1;
                const u64 mask = (u64{1} << (2 * depth)) - 1;
                const u64 residue = current & mask;
                const int index = occurrences.size();
                occurrences.push_back({
                    current,
                    residue,
                    mask_sequence(levels, complexity, current, depth),
                    0,
                    0,
                    cut,
                    depth,
                    999,
                });
                lookup[depth][residue].push_back(index);
                maximum_depth = std::max(maximum_depth, depth);
            }
        }

        for (u64 shadow : levels[complexity - 1]) {
            u64 state = shadow;
            u64 sequence = 0;
            int defects = 0;
            for (int step = 0; step < maximum_depth; ++step) {
                const u64 quotient = state >> 2;
                const int level = complexity - 2 - step;
                const unsigned shadow_mask = fiber_mask(levels, level, quotient);
                sequence |= u64(shadow_mask) << (4 * step);
                defects += shadow_mask != 15;
                state = quotient;
                const int depth = step + 1;
                const u64 residue = shadow & ((u64{1} << (2 * depth)) - 1);
                const auto found = lookup[depth].find(residue);
                if (found == lookup[depth].end()) continue;
                for (int index : found->second) {
                    auto& occurrence = occurrences[index];
                    if (defects >= occurrence.best_defects) continue;
                    if (!dominates(
                            occurrence.current_sequence, sequence, depth
                        )) {
                        continue;
                    }
                    occurrence.best_defects = defects;
                    occurrence.best_shadow = shadow;
                    occurrence.best_sequence = sequence;
                }
            }
        }

        total_occurrences += occurrences.size();
        for (const auto& occurrence : occurrences) {
            if (occurrence.best_defects == 999) {
                ++dominant_failures;
                continue;
            }
            ++defect_histogram[occurrence.best_defects];
            if (!synchronized_or_full(
                    occurrence.current_sequence,
                    occurrence.best_sequence,
                    occurrence.depth
                )) {
                ++synchronized_failures;
            }
            if (occurrence.best_defects > 0) exceptions.push_back(occurrence);
        }
    }

    std::cout << "maximum_complexity=" << MAXK << '\n';
    std::cout << "phase_u_outputs=" << outputs << '\n';
    std::cout << "weighted_recursion_checks=" << recursive_checks << '\n';
    std::cout << "gap_222_occurrences=" << total_occurrences << '\n';
    std::cout << "dominant_failures=" << dominant_failures << '\n';
    std::cout << "synchronized_failures=" << synchronized_failures << '\n';
    for (const auto& [defects, count] : defect_histogram) {
        std::cout << "minimum_defect_" << defects << '=' << count << '\n';
    }
    std::cout << "exceptions=" << exceptions.size() << '\n';

    for (const auto& occurrence : exceptions) {
        int count_1011 = 0;
        int count_1100 = 0;
        int count_other = 0;
        for (int step = 0; step < occurrence.depth; ++step) {
            const unsigned mask =
                (occurrence.best_sequence >> (4 * step)) & 15;
            if (mask == 15) continue;
            if (mask == 0b1011) ++count_1011;
            else if (mask == 0b1100) ++count_1100;
            else ++count_other;
        }
        std::cout << "exception_complexity="
                  << (occurrence.current == 0x191cf4384dfbULL ? 23
                      : occurrence.current == 0x1bcd3a7b3fdfbULL ? 25
                      : 27)
                  << " cut=" << occurrence.cut
                  << " state=0x" << std::hex << occurrence.current
                  << " shadow=0x" << occurrence.best_shadow << std::dec
                  << " defects=" << occurrence.best_defects
                  << " count_1011=" << count_1011
                  << " count_1100=" << count_1100
                  << " count_other=" << count_other
                  << " current_masks="
                  << sequence_string(
                         occurrence.current_sequence, occurrence.depth
                     )
                  << " shadow_masks="
                  << sequence_string(
                         occurrence.best_sequence, occurrence.depth
                     )
                  << '\n';
        if (count_1011 != 2 || count_1100 != 1 || count_other != 0) {
            throw std::runtime_error("exception defect types changed");
        }
    }

    if (total_occurrences != 2989 || dominant_failures != 0
        || synchronized_failures != 0 || defect_histogram.size() != 2
        || defect_histogram[0] != 2986 || defect_histogram[3] != 3
        || exceptions.size() != 3) {
        throw std::runtime_error("complexity-27 totals changed");
    }
}
