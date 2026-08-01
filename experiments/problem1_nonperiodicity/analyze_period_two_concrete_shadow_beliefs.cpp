#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <limits>
#include <map>
#include <set>
#include <stdexcept>
#include <string>
#include <tuple>
#include <unordered_map>
#include <utility>
#include <vector>

using u64 = std::uint64_t;
constexpr int MAXK = 25;
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
    for (int k = 2; k <= maximum_complexity; ++k) {
        levels[k] = next_level(levels[k - 1]);
    }
    return levels;
}

bool contains(const std::vector<u64>& values, u64 target) {
    return std::binary_search(values.begin(), values.end(), target);
}

int bit_length(u64 value) {
    return value ? 64 - __builtin_clzll(value) : 0;
}

int expected_bits(char phase, int complexity) {
    return phase == 'p' ? 2 * complexity : 2 * complexity - 1;
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
    static const std::array<std::string, 3> forbidden{"uu", "ttttt", "ututtu"};
    for (const auto& factor : forbidden) {
        if (word.find(factor) != std::string::npos) return false;
    }
    return true;
}

std::string return_extension(const std::array<int, 3>& gaps, bool final_u) {
    std::string word = "u";
    for (int index = 0; index < 3; ++index) {
        word.append(gaps[index] - 1, 't');
        if (index < 2 || final_u) word.push_back('u');
    }
    return word;
}

struct Pattern {
    std::array<int, 3> gaps;
    std::string target;
    std::string complete;
};

std::vector<Pattern> three_return_patterns() {
    std::vector<Pattern> result;
    for (int a = 2; a <= 5; ++a) {
        for (int b = 2; b <= 5; ++b) {
            for (int c = 2; c <= 5; ++c) {
                std::array<int, 3> gaps{a, b, c};
                const std::string target = return_extension(gaps, false);
                const std::string complete = return_extension(gaps, true);
                if (admissible(complete)) result.push_back({gaps, target, complete});
            }
        }
    }
    return result;
}

std::vector<u64> direct_belief(
    const std::vector<std::vector<u64>>& levels,
    int complexity,
    u64 current,
    int depth
) {
    const u64 mask = (u64{1} << (2 * depth)) - 1;
    const u64 residue = current & mask;
    std::vector<u64> result;
    for (u64 state : levels[complexity - 1]) {
        if ((state & mask) == residue) result.push_back(state);
    }
    return result;
}

std::vector<u64> recursive_belief(
    const std::vector<std::vector<u64>>& levels,
    int complexity,
    u64 current,
    int depth
) {
    const int digit = current & 3;
    if (depth == 1) {
        std::vector<u64> result;
        for (u64 state : levels[complexity - 1]) {
            if ((state & 3) == u64(digit)) result.push_back(state);
        }
        return result;
    }
    auto parent = recursive_belief(levels, complexity - 1, current >> 2, depth - 1);
    std::vector<u64> result;
    result.reserve(parent.size());
    for (u64 state : parent) {
        const u64 child = 4 * state + unsigned(digit);
        if (contains(levels[complexity - 1], child)) result.push_back(child);
    }
    return result;
}

void verify_recursive_theorem() {
    for (char phase : {'p', 'u'}) {
        const auto levels = build_levels(phase, 9);
        for (int complexity = 2; complexity <= 9; ++complexity) {
            for (u64 current : levels[complexity]) {
                for (int depth = 1; depth < complexity; ++depth) {
                    if (direct_belief(levels, complexity, current, depth)
                        != recursive_belief(levels, complexity, current, depth)) {
                        throw std::runtime_error("direct/recursive belief mismatch");
                    }
                }
            }
        }
    }
}

struct Occurrence {
    u64 current;
    int cut;
    int depth;
    int weight;
};

struct Stats {
    u64 outputs = 0;
    u64 eligible_outputs = 0;
    u64 occurrences = 0;
    u64 positive_cut_occurrences = 0;
    u64 shadowed_occurrences = 0;
    u64 empty_beliefs = 0;
    u64 total_shadow_realizations = 0;
    u64 levels_with_occurrences = 0;
    u64 distinct_occurrence_cylinders = 0;
    int maximum_cut = 0;
    int maximum_depth = 0;
    u64 minimum_final_belief = std::numeric_limits<u64>::max();
    u64 maximum_final_belief = 0;
    int minimum_example_complexity = 0;
    int minimum_example_cut = 0;
    int minimum_example_depth = 0;
    u64 minimum_example_current = 0;
    u64 minimum_example_residue = 0;
    std::vector<u64> minimum_example_shadows;
};

Stats campaign(char phase, const std::vector<Pattern>& patterns) {
    const auto levels = build_levels(phase, MAXK);
    Stats stats;
    std::set<std::tuple<int, int, u64>> distinct;
    for (int k = 1; k <= MAXK; ++k) stats.outputs += levels[k].size();

    for (int complexity = 2; complexity <= MAXK; ++complexity) {
        std::vector<Occurrence> occurrences;
        std::set<int> needed_depths;
        for (u64 current : levels[complexity]) {
            if (bit_length(current) != expected_bits(phase, complexity)) {
                throw std::runtime_error("frontier bit-length law failed");
            }
            if ((current & 3) != 3) continue;
            ++stats.eligible_outputs;
            const std::string schedule = forced_zero_schedule(current);
            for (int cut = 0; cut <= static_cast<int>(schedule.size()); ++cut) {
                const std::string base = schedule.substr(0, cut);
                int weight = 0;
                for (const auto& pattern : patterns) {
                    if (schedule.compare(cut, pattern.target.size(), pattern.target) == 0
                        && admissible(base + pattern.complete)) {
                        ++weight;
                    }
                }
                if (!weight) continue;
                const int depth = cut + 1;
                if (depth >= complexity) {
                    throw std::runtime_error("occurrence consumed entire frontier");
                }
                occurrences.push_back({current, cut, depth, weight});
                needed_depths.insert(depth);
            }
        }
        if (occurrences.empty()) continue;
        ++stats.levels_with_occurrences;

        std::map<int, std::unordered_map<u64, u64>> counts;
        for (int depth : needed_depths) {
            const u64 mask = (u64{1} << (2 * depth)) - 1;
            auto& index = counts[depth];
            index.reserve(levels[complexity - 1].size() * 2);
            for (u64 state : levels[complexity - 1]) ++index[state & mask];
        }

        for (const auto& occurrence : occurrences) {
            const u64 mask = (u64{1} << (2 * occurrence.depth)) - 1;
            const u64 residue = occurrence.current & mask;
            const u64 belief_size = counts[occurrence.depth][residue];
            const u64 weight = occurrence.weight;
            stats.occurrences += weight;
            if (occurrence.cut > 0) stats.positive_cut_occurrences += weight;
            stats.maximum_cut = std::max(stats.maximum_cut, occurrence.cut);
            stats.maximum_depth = std::max(stats.maximum_depth, occurrence.depth);
            if (belief_size) stats.shadowed_occurrences += weight;
            else stats.empty_beliefs += weight;
            stats.total_shadow_realizations += weight * belief_size;
            if (belief_size < stats.minimum_final_belief) {
                stats.minimum_final_belief = belief_size;
                stats.minimum_example_complexity = complexity;
                stats.minimum_example_cut = occurrence.cut;
                stats.minimum_example_depth = occurrence.depth;
                stats.minimum_example_current = occurrence.current;
                stats.minimum_example_residue = residue;
                stats.minimum_example_shadows.clear();
                for (u64 state : levels[complexity - 1]) {
                    if ((state & mask) == residue) {
                        stats.minimum_example_shadows.push_back(state);
                    }
                }
                if (stats.minimum_example_shadows.size() != belief_size) {
                    throw std::runtime_error("minimum belief recount mismatch");
                }
            }
            stats.maximum_final_belief = std::max(stats.maximum_final_belief, belief_size);
            distinct.insert({complexity, occurrence.depth, residue});
        }
    }
    // Complexity one is eligible only for phase p and cannot contain a three-return occurrence.
    for (u64 state : levels[1]) if ((state & 3) == 3) ++stats.eligible_outputs;
    stats.distinct_occurrence_cylinders = distinct.size();
    return stats;
}

void print_stats(const std::string& prefix, const Stats& stats) {
    std::cout << prefix << "_outputs=" << stats.outputs << '\n';
    std::cout << prefix << "_eligible_outputs=" << stats.eligible_outputs << '\n';
    std::cout << prefix << "_occurrences=" << stats.occurrences << '\n';
    std::cout << prefix << "_positive_cut_occurrences=" << stats.positive_cut_occurrences << '\n';
    std::cout << prefix << "_shadowed_occurrences=" << stats.shadowed_occurrences << '\n';
    std::cout << prefix << "_empty_beliefs=" << stats.empty_beliefs << '\n';
    std::cout << prefix << "_total_shadow_realizations=" << stats.total_shadow_realizations << '\n';
    std::cout << prefix << "_levels_with_occurrences=" << stats.levels_with_occurrences << '\n';
    std::cout << prefix << "_distinct_occurrence_cylinders=" << stats.distinct_occurrence_cylinders << '\n';
    std::cout << prefix << "_maximum_cut=" << stats.maximum_cut << '\n';
    std::cout << prefix << "_maximum_depth=" << stats.maximum_depth << '\n';
    std::cout << prefix << "_minimum_final_belief=" << stats.minimum_final_belief << '\n';
    std::cout << prefix << "_maximum_final_belief=" << stats.maximum_final_belief << '\n';
    std::cout << prefix << "_minimum_example_complexity=" << stats.minimum_example_complexity << '\n';
    std::cout << prefix << "_minimum_example_cut=" << stats.minimum_example_cut << '\n';
    std::cout << prefix << "_minimum_example_depth=" << stats.minimum_example_depth << '\n';
    std::cout << prefix << "_minimum_example_current=0x" << std::hex << stats.minimum_example_current << std::dec << '\n';
    std::cout << prefix << "_minimum_example_residue=0x" << std::hex << stats.minimum_example_residue << std::dec << '\n';
    std::cout << prefix << "_minimum_example_shadows=";
    const std::size_t shown = std::min<std::size_t>(8, stats.minimum_example_shadows.size());
    for (std::size_t index = 0; index < shown; ++index) {
        if (index) std::cout << ',';
        std::cout << "0x" << std::hex << stats.minimum_example_shadows[index] << std::dec;
    }
    if (shown < stats.minimum_example_shadows.size()) std::cout << ",...";
    std::cout << '\n';
}

int main() {
    verify_recursive_theorem();
    const auto patterns = three_return_patterns();
    if (patterns.size() != 56) throw std::runtime_error("pattern count changed");
    const Stats phase_p = campaign('p', patterns);
    const Stats phase_u = campaign('u', patterns);

    std::cout << "maximum_complexity=" << MAXK << '\n';
    std::cout << "admissible_three_return_patterns=" << patterns.size() << '\n';
    std::cout << "recursive_theorem_small_exhaustive=1\n";
    print_stats("phase_p", phase_p);
    print_stats("phase_u", phase_u);
    std::cout << "total_outputs=" << phase_p.outputs + phase_u.outputs << '\n';
    std::cout << "total_eligible_outputs=" << phase_p.eligible_outputs + phase_u.eligible_outputs << '\n';
    std::cout << "total_occurrences=" << phase_p.occurrences + phase_u.occurrences << '\n';
    std::cout << "total_positive_cut_occurrences="
              << phase_p.positive_cut_occurrences + phase_u.positive_cut_occurrences << '\n';
    std::cout << "total_shadowed_occurrences="
              << phase_p.shadowed_occurrences + phase_u.shadowed_occurrences << '\n';
    std::cout << "total_empty_beliefs=" << phase_p.empty_beliefs + phase_u.empty_beliefs << '\n';
    std::cout << "total_shadow_realizations="
              << phase_p.total_shadow_realizations + phase_u.total_shadow_realizations << '\n';
    std::cout << "minimum_final_belief="
              << std::min(phase_p.minimum_final_belief, phase_u.minimum_final_belief) << '\n';
    std::cout << "maximum_final_belief="
              << std::max(phase_p.maximum_final_belief, phase_u.maximum_final_belief) << '\n';

    if (phase_p.outputs != 9118715 || phase_u.outputs != 7745997
        || phase_p.occurrences + phase_u.occurrences != 3395
        || phase_p.empty_beliefs + phase_u.empty_beliefs != 0) {
        throw std::runtime_error("complexity-25 totals changed");
    }
}
