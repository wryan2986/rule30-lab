#include <algorithm>
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
using u64 = std::uint64_t;
constexpr int MAXK = 25;
constexpr int CAP = 64;
constexpr std::array<int, 4> GAPS{2, 3, 4, 5};

u64 forward(char generator, u64 state) {
    const u64 stepped = state ^ ((state << 1) | (state << 2));
    if (generator == 't') return stepped;
    if (generator == 'u') return stepped ^ 1;
    if (generator == 'p') return stepped ^ 1 ^ ((state & 1) == 0 ? 2 : 0);
    throw std::runtime_error("unknown generator");
}

std::vector<u64> children(u64 state) {
    std::array<u64, 3> values{
        forward('t', state), forward('u', state), forward('p', state)
    };
    std::sort(values.begin(), values.end());
    return {values.begin(), std::unique(values.begin(), values.end())};
}

int bit_length(u64 value) {
    return value == 0 ? 0 : 64 - __builtin_clzll(value);
}

struct Schedule {
    u64 bits = 0;
    int length = 0;
};

Schedule forced_schedule(u64 state) {
    Schedule result;
    for (int step = 0; step < CAP; ++step) {
        const unsigned residue = state & 15;
        char branch;
        if (residue == 7) branch = 'u';
        else if (residue == 11) branch = 't';
        else return result;
        state = forward(branch, forward('p', (state - 3) >> 2));
        result.bits = (result.bits << 1) | (branch == 'u');
        ++result.length;
    }
    throw std::runtime_error("forced schedule reached cap");
}

struct PrefixKey {
    u64 bits;
    int length;
    bool operator==(const PrefixKey& other) const {
        return bits == other.bits && length == other.length;
    }
};

struct PrefixHash {
    std::size_t operator()(const PrefixKey& key) const noexcept {
        u64 value = key.bits ^ (u64(key.length) << 57);
        value ^= value >> 30;
        value *= 0xbf58476d1ce4e5b9ULL;
        value ^= value >> 27;
        value *= 0x94d049bb133111ebULL;
        value ^= value >> 31;
        return static_cast<std::size_t>(value);
    }
};

PrefixKey prefix(const Schedule& schedule, int length) {
    return {schedule.bits >> (schedule.length - length), length};
}

std::string decode(PrefixKey key) {
    std::string word;
    for (int bit = key.length - 1; bit >= 0; --bit) {
        word.push_back(((key.bits >> bit) & 1) ? 'u' : 't');
    }
    return word;
}

bool admissible(const std::string& word) {
    return word.find("uu") == std::string::npos
        && word.find("ttttt") == std::string::npos
        && word.find("ututtu") == std::string::npos;
}

std::string extension(const std::array<int, 3>& gaps, bool include_final_u) {
    std::string word = "u";
    for (int index = 0; index < 3; ++index) {
        word += std::string(gaps[index] - 1, 't');
        if (index < 2 || include_final_u) word += 'u';
    }
    return word;
}

struct Pattern {
    std::array<int, 3> gaps;
    std::string target;
    std::string complete;
};

std::vector<Pattern> patterns() {
    std::vector<Pattern> output;
    for (int first : GAPS) {
        for (int second : GAPS) {
            for (int third : GAPS) {
                std::array<int, 3> gaps{first, second, third};
                const std::string target = extension(gaps, false);
                const std::string complete = extension(gaps, true);
                if (admissible(complete)) {
                    output.push_back({gaps, target, complete});
                }
            }
        }
    }
    return output;
}

bool schedule_has_at(const Schedule& schedule, int cut, const std::string& target) {
    if (cut + static_cast<int>(target.size()) > schedule.length) return false;
    for (int index = 0; index < static_cast<int>(target.size()); ++index) {
        const int shift = schedule.length - 1 - (cut + index);
        const char observed = ((schedule.bits >> shift) & 1) ? 'u' : 't';
        if (observed != target[index]) return false;
    }
    return true;
}

bool contains(const std::vector<u64>& values, u64 target) {
    return std::binary_search(values.begin(), values.end(), target);
}

unsigned fiber(const std::vector<u64>& next_level, u64 quotient) {
    unsigned mask = 0;
    for (int digit = 0; digit < 4; ++digit) {
        if (contains(next_level, 4 * quotient + digit)) mask |= 1U << digit;
    }
    return mask;
}

struct Totals {
    u64 outputs = 0;
    u64 eligible = 0;
    u64 occurrences = 0;
    u64 positive = 0;
    u64 shadowed = 0;
    u64 violations = 0;
    u64 states = 0;
    int maximum_cut = 0;
    std::map<std::pair<unsigned, unsigned>, u64> pairs;
    std::map<std::tuple<unsigned, unsigned, int>, u64> transitions;
};

bool dominant(
    const std::vector<std::vector<u64>>& levels,
    int complexity,
    u64 current,
    u64 shadow,
    int depth,
    std::vector<std::tuple<unsigned, unsigned, int>>& path
) {
    path.clear();
    for (int step = 0; step < depth; ++step) {
        const int digit = current & 3;
        if (static_cast<int>(shadow & 3) != digit) return false;
        const u64 current_quotient = current >> 2;
        const u64 shadow_quotient = shadow >> 2;
        const int current_level = complexity - 1 - step;
        if (current_level < 2) return false;
        const unsigned current_mask = fiber(
            levels[current_level + 1], current_quotient
        );
        const unsigned shadow_mask = fiber(
            levels[current_level], shadow_quotient
        );
        path.emplace_back(current_mask, shadow_mask, digit);
        if (current_mask & ~shadow_mask) return false;
        current = current_quotient;
        shadow = shadow_quotient;
    }
    return true;
}

Totals run_phase(
    char phase,
    const std::vector<std::vector<u64>>& levels,
    const std::vector<Pattern>& pattern_rows
) {
    Totals totals;
    totals.outputs = 1;
    totals.eligible = phase == 'p' ? 1 : 0;

    for (int complexity = 2; complexity <= MAXK; ++complexity) {
        const auto& current_level = levels[complexity];
        const auto& previous_level = levels[complexity - 1];
        std::unordered_map<PrefixKey, std::vector<u64>, PrefixHash> prefix_map;
        prefix_map.reserve(previous_level.size());
        for (u64 shadow : previous_level) {
            if ((shadow & 3) != 3) continue;
            const Schedule schedule = forced_schedule(shadow);
            for (int length = 0; length <= schedule.length; ++length) {
                prefix_map[prefix(schedule, length)].push_back(shadow);
            }
        }

        u64 level_occurrences = 0;
        u64 level_violations = 0;
        for (u64 current : current_level) {
            const int expected = phase == 'p' ? 2 * complexity : 2 * complexity - 1;
            if (bit_length(current) != expected) {
                throw std::runtime_error("frontier bit-length law failed");
            }
            if ((current & 3) != 3) continue;
            ++totals.eligible;
            const Schedule schedule = forced_schedule(current);
            bool state_has_occurrence = false;

            for (int cut = 0; cut <= schedule.length; ++cut) {
                const PrefixKey key = prefix(schedule, cut);
                const std::string base = decode(key);
                int matches = 0;
                for (const Pattern& pattern : pattern_rows) {
                    if (schedule_has_at(schedule, cut, pattern.target)
                        && admissible(base + pattern.complete)) {
                        ++matches;
                    }
                }
                if (!matches) continue;
                state_has_occurrence = true;

                bool found = false;
                std::vector<std::tuple<unsigned, unsigned, int>> chosen_path;
                const auto found_prefix = prefix_map.find(key);
                if (found_prefix != prefix_map.end()) {
                    for (u64 shadow : found_prefix->second) {
                        std::vector<std::tuple<unsigned, unsigned, int>> path;
                        if (dominant(
                                levels, complexity, current, shadow, cut + 1, path
                            )) {
                            found = true;
                            chosen_path = std::move(path);
                            break;
                        }
                    }
                }

                for (int match = 0; match < matches; ++match) {
                    ++totals.occurrences;
                    ++level_occurrences;
                    if (cut > 0) ++totals.positive;
                    totals.maximum_cut = std::max(totals.maximum_cut, cut);
                    if (found) {
                        ++totals.shadowed;
                        for (const auto& [current_mask, shadow_mask, digit] : chosen_path) {
                            ++totals.pairs[{current_mask, shadow_mask}];
                            ++totals.transitions[{current_mask, shadow_mask, digit}];
                        }
                    } else {
                        ++totals.violations;
                        ++level_violations;
                    }
                }
            }
            if (state_has_occurrence) ++totals.states;
        }
        totals.outputs += current_level.size();
        if (level_occurrences || level_violations) {
            std::cout << "phase=" << phase
                      << " k=" << complexity
                      << " occ=" << level_occurrences
                      << " viol=" << level_violations
                      << " prefix_keys=" << prefix_map.size() << '\n';
        }
    }
    return totals;
}
}  // namespace

int main() {
    const std::vector<Pattern> pattern_rows = patterns();
    std::cout << "patterns=" << pattern_rows.size() << '\n';
    Totals total;

    for (char phase : {'p', 'u'}) {
        std::vector<std::vector<u64>> levels(MAXK + 1);
        levels[1] = {phase == 'p' ? 3ULL : 1ULL};
        for (int complexity = 2; complexity <= MAXK; ++complexity) {
            std::vector<u64> next;
            next.reserve(levels[complexity - 1].size() * 3);
            for (u64 state : levels[complexity - 1]) {
                const std::vector<u64> values = children(state);
                next.insert(next.end(), values.begin(), values.end());
            }
            std::sort(next.begin(), next.end());
            next.erase(std::unique(next.begin(), next.end()), next.end());
            levels[complexity] = std::move(next);
        }

        const Totals phase_totals = run_phase(phase, levels, pattern_rows);
        std::cout << "summary phase=" << phase
                  << " outputs=" << phase_totals.outputs
                  << " eligible=" << phase_totals.eligible
                  << " occ=" << phase_totals.occurrences
                  << " positive=" << phase_totals.positive
                  << " shadowed=" << phase_totals.shadowed
                  << " viol=" << phase_totals.violations
                  << " states=" << phase_totals.states
                  << " maxcut=" << phase_totals.maximum_cut << '\n';
        for (const auto& [pair, count] : phase_totals.pairs) {
            std::cout << "pair phase=" << phase
                      << " current=" << pair.first
                      << " shadow=" << pair.second
                      << " count=" << count << '\n';
        }

        total.outputs += phase_totals.outputs;
        total.eligible += phase_totals.eligible;
        total.occurrences += phase_totals.occurrences;
        total.positive += phase_totals.positive;
        total.shadowed += phase_totals.shadowed;
        total.violations += phase_totals.violations;
        total.states += phase_totals.states;
        total.maximum_cut = std::max(total.maximum_cut, phase_totals.maximum_cut);
        for (const auto& [pair, count] : phase_totals.pairs) {
            total.pairs[pair] += count;
        }
        for (const auto& [transition, count] : phase_totals.transitions) {
            total.transitions[transition] += count;
        }
    }

    std::cout << "total outputs=" << total.outputs
              << " eligible=" << total.eligible
              << " occ=" << total.occurrences
              << " positive=" << total.positive
              << " shadowed=" << total.shadowed
              << " viol=" << total.violations
              << " states=" << total.states
              << " maxcut=" << total.maximum_cut << '\n';
    for (const auto& [pair, count] : total.pairs) {
        std::cout << "pair current=" << pair.first
                  << " shadow=" << pair.second
                  << " count=" << count << '\n';
    }
    for (const auto& [transition, count] : total.transitions) {
        std::cout << "triple current=" << std::get<0>(transition)
                  << " shadow=" << std::get<1>(transition)
                  << " digit=" << std::get<2>(transition)
                  << " count=" << count << '\n';
    }
    return total.violations == 0 ? 0 : 2;
}
