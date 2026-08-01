#include <algorithm>
#include <cstdint>
#include <iomanip>
#include <iostream>
#include <map>
#include <set>
#include <stdexcept>
#include <string>
#include <tuple>
#include <unordered_map>
#include <utility>
#include <vector>

using u64 = std::uint64_t;

constexpr int MAXIMUM_COMPLEXITY = 27;
constexpr int PROFILE_CENSUS_MAXIMUM_COMPLEXITY = 22;
constexpr int SCHEDULE_CAP = 64;

constexpr u64 WITNESS_CURRENT = 0x1bcd3a1c36ULL;
constexpr u64 WITNESS_GOOD_SHADOW = 0x642e240c2ULL;
constexpr u64 WITNESS_BAD_SHADOW = 0x642e27436ULL;

u64 forward_generator(char generator, u64 state) {
    const u64 stepped = state ^ ((state << 1) | (state << 2));
    if (generator == 't') return stepped;
    if (generator == 'u') return stepped ^ 1;
    if (generator == 'p') {
        return stepped ^ 1 ^ ((state & 1) == 0 ? 2 : 0);
    }
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

bool contains(const std::vector<u64>& values, u64 target) {
    return std::binary_search(values.begin(), values.end(), target);
}

unsigned fiber_mask(
    const std::vector<std::vector<u64>>& levels,
    int complexity,
    u64 state
) {
    unsigned mask = 0;
    for (int digit = 0; digit < 4; ++digit) {
        if (contains(levels[complexity + 1], 4 * state + unsigned(digit))) {
            mask |= 1u << digit;
        }
    }
    return mask;
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

u64 mask_sequence(
    const std::vector<std::vector<u64>>& levels,
    int complexity,
    u64 state,
    int depth
) {
    u64 result = 0;
    for (int step = 0; step < depth; ++step) {
        const u64 quotient = state >> 2;
        const unsigned mask = fiber_mask(
            levels, complexity - 1 - step, quotient
        );
        result |= u64(mask) << (4 * step);
        state = quotient;
    }
    return result;
}

bool dominates(u64 current, u64 shadow, int depth) {
    for (int step = 0; step < depth; ++step) {
        const unsigned current_mask = (current >> (4 * step)) & 15;
        const unsigned shadow_mask = (shadow >> (4 * step)) & 15;
        if (current_mask & ~shadow_mask) return false;
    }
    return true;
}

bool synchronized_or_full(u64 current, u64 shadow, int depth) {
    for (int step = 0; step < depth; ++step) {
        const unsigned current_mask = (current >> (4 * step)) & 15;
        const unsigned shadow_mask = (shadow >> (4 * step)) & 15;
        if (shadow_mask != 15 && shadow_mask != current_mask) return false;
    }
    return true;
}

int defect_count(u64 shadow, int depth) {
    int result = 0;
    for (int step = 0; step < depth; ++step) {
        result += ((shadow >> (4 * step)) & 15) != 15;
    }
    return result;
}

// Own fiber occupies four bits. Each child occupies five bits: zero means
// absent; 0b1xxxx means present with four-bit fiber xxxx. This distinguishes
// an absent child from a present child with fiber 0000.
u64 endpoint_profile(
    const std::vector<std::vector<u64>>& levels,
    int complexity,
    u64 state
) {
    u64 result = fiber_mask(levels, complexity, state);
    for (int digit = 0; digit < 4; ++digit) {
        const u64 child = 4 * state + unsigned(digit);
        unsigned code = 0;
        if (contains(levels[complexity + 1], child)) {
            code = 16u | fiber_mask(levels, complexity + 1, child);
        }
        result |= u64(code) << (4 + 5 * digit);
    }
    return result;
}

bool synchronized_pair(
    const std::vector<std::vector<u64>>& levels,
    int complexity,
    u64 current,
    u64 shadow
) {
    if (!contains(levels[complexity], current)) return false;
    if (!contains(levels[complexity - 1], shadow)) return false;
    if ((current & 3) != (shadow & 3)) return false;
    const unsigned current_mask = fiber_mask(levels, complexity, current);
    const unsigned shadow_mask = fiber_mask(levels, complexity - 1, shadow);
    return !(current_mask & ~shadow_mask)
        && (shadow_mask == 15 || shadow_mask == current_mask);
}

bool follows_two_digits(
    const std::vector<std::vector<u64>>& levels,
    int complexity,
    u64 current,
    u64 shadow,
    int first,
    int second
) {
    for (int digit : {first, second}) {
        current = 4 * current + unsigned(digit);
        shadow = 4 * shadow + unsigned(digit);
        ++complexity;
        if (!synchronized_pair(levels, complexity, current, shadow)) {
            return false;
        }
    }
    return true;
}

struct Occurrence {
    u64 current;
    u64 residue;
    u64 current_sequence;
    u64 best_shadow = 0;
    u64 best_sequence = 0;
    int complexity;
    int cut;
    int depth;
    int best_defects = 999;
};

using PairNode = std::tuple<int, u64, u64>;
using Provenance = std::tuple<int, u64, int, u64>;

int main() {
    std::vector<std::vector<u64>> levels(MAXIMUM_COMPLEXITY + 1);
    levels[1] = {1};
    u64 outputs = 1;
    for (int complexity = 2; complexity <= MAXIMUM_COMPLEXITY; ++complexity) {
        levels[complexity] = next_level(levels[complexity - 1]);
        outputs += levels[complexity].size();
    }

    u64 occurrences = 0;
    u64 dominant_failures = 0;
    std::map<int, u64> defect_histogram;
    std::set<PairNode> selected_nodes;
    std::map<PairNode, Provenance> provenance;

    for (int complexity = 2; complexity <= MAXIMUM_COMPLEXITY; ++complexity) {
        std::vector<Occurrence> rows;
        int maximum_depth = 0;
        std::vector<std::unordered_map<u64, std::vector<int>>> lookup(20);

        for (u64 current : levels[complexity]) {
            if ((current & 3) != 3) continue;
            const std::string schedule = forced_zero_schedule(current);
            for (int cut = 0; cut <= static_cast<int>(schedule.size()); ++cut) {
                if (schedule.compare(cut, 6, "ututut") != 0) continue;
                if (!admissible(schedule.substr(0, cut) + "utututu")) continue;
                const int depth = cut + 1;
                const u64 residue_mask = (u64{1} << (2 * depth)) - 1;
                const int index = rows.size();
                rows.push_back({
                    current,
                    current & residue_mask,
                    mask_sequence(levels, complexity, current, depth),
                    0,
                    0,
                    complexity,
                    cut,
                    depth,
                    999,
                });
                lookup[depth][current & residue_mask].push_back(index);
                maximum_depth = std::max(maximum_depth, depth);
            }
        }

        for (u64 shadow : levels[complexity - 1]) {
            u64 state = shadow;
            u64 shadow_sequence = 0;
            int defects = 0;
            for (int step = 0; step < maximum_depth; ++step) {
                const u64 quotient = state >> 2;
                const unsigned mask = fiber_mask(
                    levels, complexity - 2 - step, quotient
                );
                shadow_sequence |= u64(mask) << (4 * step);
                defects += mask != 15;
                state = quotient;

                const int depth = step + 1;
                const u64 residue = shadow & ((u64{1} << (2 * depth)) - 1);
                const auto found = lookup[depth].find(residue);
                if (found == lookup[depth].end()) continue;
                for (int index : found->second) {
                    auto& row = rows[index];
                    if (defects > row.best_defects) continue;
                    if (!dominates(row.current_sequence, shadow_sequence, depth)) {
                        continue;
                    }
                    if (!synchronized_or_full(
                            row.current_sequence, shadow_sequence, depth
                        )) {
                        continue;
                    }
                    if (defects < row.best_defects || shadow < row.best_shadow) {
                        row.best_defects = defects;
                        row.best_shadow = shadow;
                        row.best_sequence = shadow_sequence;
                    }
                }
            }
        }

        occurrences += rows.size();
        for (const auto& row : rows) {
            if (row.best_defects == 999) {
                ++dominant_failures;
                continue;
            }
            ++defect_histogram[row.best_defects];
            u64 current = row.current;
            u64 shadow = row.best_shadow;
            for (int step = 0; step < row.depth; ++step) {
                const PairNode node{complexity - step, current, shadow};
                selected_nodes.insert(node);
                provenance.emplace(
                    node,
                    Provenance{
                        complexity,
                        row.current,
                        row.cut,
                        row.best_shadow,
                    }
                );
                current >>= 2;
                shadow >>= 2;
            }
        }
    }

    std::map<std::tuple<int, u64, u64>, std::vector<PairNode>> classes;
    std::set<std::pair<u64, u64>> unlevelled_classes;
    int profile_nodes_analyzed = 0;
    for (const auto& node : selected_nodes) {
        const auto [complexity, current, shadow] = node;
        if (complexity > PROFILE_CENSUS_MAXIMUM_COMPLEXITY) continue;
        ++profile_nodes_analyzed;
        const u64 current_profile = endpoint_profile(
            levels, complexity, current
        );
        const u64 shadow_profile = endpoint_profile(
            levels, complexity - 1, shadow
        );
        classes[{complexity, current_profile, shadow_profile}].push_back(node);
        unlevelled_classes.insert({current_profile, shadow_profile});
    }

    int collision_classes = 0;
    int divergent_classes = 0;
    int maximum_class_size = 0;
    for (const auto& [key, nodes] : classes) {
        static_cast<void>(key);
        maximum_class_size = std::max(
            maximum_class_size, static_cast<int>(nodes.size())
        );
        if (nodes.size() < 2) continue;
        ++collision_classes;
        bool divergent = false;
        for (int first = 0; first < 4 && !divergent; ++first) {
            for (int second = 0; second < 4 && !divergent; ++second) {
                const auto [base_complexity, base_current, base_shadow] = nodes[0];
                const bool base = follows_two_digits(
                    levels,
                    base_complexity,
                    base_current,
                    base_shadow,
                    first,
                    second
                );
                for (std::size_t index = 1; index < nodes.size(); ++index) {
                    const auto [complexity, current, shadow] = nodes[index];
                    const bool value = follows_two_digits(
                        levels,
                        complexity,
                        current,
                        shadow,
                        first,
                        second
                    );
                    if (value != base) {
                        divergent = true;
                        break;
                    }
                }
            }
        }
        if (divergent) ++divergent_classes;
    }

    const u64 current_profile = endpoint_profile(
        levels, 19, WITNESS_CURRENT
    );
    const u64 good_profile = endpoint_profile(
        levels, 18, WITNESS_GOOD_SHADOW
    );
    const u64 bad_profile = endpoint_profile(
        levels, 18, WITNESS_BAD_SHADOW
    );
    const bool profiles_equal = good_profile == bad_profile;
    const bool good_word_30 = follows_two_digits(
        levels, 19, WITNESS_CURRENT, WITNESS_GOOD_SHADOW, 3, 0
    );
    const bool bad_word_30 = follows_two_digits(
        levels, 19, WITNESS_CURRENT, WITNESS_BAD_SHADOW, 3, 0
    );

    const u64 first_current = 4 * WITNESS_CURRENT + 3;
    const u64 first_good_shadow = 4 * WITNESS_GOOD_SHADOW + 3;
    const u64 first_bad_shadow = 4 * WITNESS_BAD_SHADOW + 3;
    const u64 second_current = 4 * first_current;
    const u64 second_good_shadow = 4 * first_good_shadow;
    const u64 second_bad_shadow = 4 * first_bad_shadow;

    std::cout << "maximum_complexity=" << MAXIMUM_COMPLEXITY << '\n';
    std::cout << "phase_u_outputs=" << outputs << '\n';
    std::cout << "gap_222_occurrences=" << occurrences << '\n';
    std::cout << "dominant_failures=" << dominant_failures << '\n';
    std::cout << "minimum_defect_0=" << defect_histogram[0] << '\n';
    std::cout << "minimum_defect_3=" << defect_histogram[3] << '\n';
    std::cout << "selected_endpoint_pairs=" << selected_nodes.size() << '\n';
    std::cout << "profile_census_maximum_complexity="
              << PROFILE_CENSUS_MAXIMUM_COMPLEXITY << '\n';
    std::cout << "profile_nodes_analyzed=" << profile_nodes_analyzed << '\n';
    std::cout << "level_specific_profile_classes=" << classes.size() << '\n';
    std::cout << "unlevelled_profile_classes="
              << unlevelled_classes.size() << '\n';
    std::cout << "collision_profile_classes=" << collision_classes << '\n';
    std::cout << "two_digit_language_divergent_classes="
              << divergent_classes << '\n';
    std::cout << "maximum_profile_class_size=" << maximum_class_size << '\n';

    std::cout << std::hex;
    std::cout << "witness_current=0x" << WITNESS_CURRENT << '\n';
    std::cout << "witness_good_shadow=0x" << WITNESS_GOOD_SHADOW << '\n';
    std::cout << "witness_bad_shadow=0x" << WITNESS_BAD_SHADOW << '\n';
    std::cout << "witness_current_profile=0x" << current_profile << '\n';
    std::cout << "witness_shadow_profile=0x" << good_profile << '\n';
    std::cout << "first_current=0x" << first_current << '\n';
    std::cout << "first_good_shadow=0x" << first_good_shadow << '\n';
    std::cout << "first_bad_shadow=0x" << first_bad_shadow << '\n';
    std::cout << "second_current=0x" << second_current << '\n';
    std::cout << "second_good_shadow=0x" << second_good_shadow << '\n';
    std::cout << "second_bad_shadow=0x" << second_bad_shadow << '\n';
    std::cout << std::dec;

    std::cout << "profiles_equal=" << profiles_equal << '\n';
    std::cout << "good_word_30=" << good_word_30 << '\n';
    std::cout << "bad_word_30=" << bad_word_30 << '\n';
    std::cout << "second_good_masks="
              << fiber_mask(levels, 21, second_current) << ','
              << fiber_mask(levels, 20, second_good_shadow) << '\n';
    std::cout << "second_bad_masks="
              << fiber_mask(levels, 21, second_current) << ','
              << fiber_mask(levels, 20, second_bad_shadow) << '\n';

    for (const auto& [shadow, expected_cut] : std::vector<std::pair<u64, int>>{
             {WITNESS_GOOD_SHADOW, 2},
             {WITNESS_BAD_SHADOW, 4},
         }) {
        const auto found = provenance.find({19, WITNESS_CURRENT, shadow});
        if (found == provenance.end()) {
            throw std::runtime_error("witness pair missing from selected certificates");
        }
        const auto [complexity, occurrence_state, cut, occurrence_shadow] =
            found->second;
        std::cout << std::hex;
        std::cout << "provenance_shadow=0x" << shadow
                  << " occurrence_state=0x" << occurrence_state
                  << " occurrence_shadow=0x" << occurrence_shadow;
        std::cout << std::dec
                  << " occurrence_complexity=" << complexity
                  << " occurrence_cut=" << cut << '\n';
        if (complexity != 21 || occurrence_state != 0x1bcd3a1c36bULL
            || cut != expected_cut) {
            throw std::runtime_error("witness provenance changed");
        }
    }

    if (outputs != 23270776 || occurrences != 2989
        || dominant_failures != 0 || defect_histogram.size() != 2
        || defect_histogram[0] != 2986 || defect_histogram[3] != 3
        || selected_nodes.size() != 4323 || profile_nodes_analyzed != 456
        || classes.size() != 241 || unlevelled_classes.size() != 148
        || collision_classes != 62 || divergent_classes != 19
        || maximum_class_size != 53 || !profiles_equal
        || !good_word_30 || bad_word_30
        || fiber_mask(levels, 21, second_current) != 0
        || fiber_mask(levels, 20, second_good_shadow) != 0
        || fiber_mask(levels, 20, second_bad_shadow) != 11) {
        throw std::runtime_error("endpoint profile no-go totals changed");
    }
}
