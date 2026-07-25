#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <utility>
#include <vector>

namespace {
using u128 = unsigned __int128;
constexpr int MAXIMUM_COMPLEXITY = 25;
constexpr int SCHEDULE_CAP = 64;
constexpr std::array<int, 4> GAPS{2, 3, 4, 5};
constexpr std::uint64_t KNOWN_STATE = 0x1bcd3a7b3fdfbULL;

u128 forward_generator(char name, u128 state) {
    const u128 stepped = state ^ ((state << 1) | (state << 2));
    if (name == 't') return stepped;
    if (name == 'u') return stepped ^ 1;
    if (name == 'p') return stepped ^ 1 ^ ((state & 1) == 0 ? 2 : 0);
    throw std::invalid_argument("unknown generator");
}

int bit_length(std::uint64_t value) {
    return value == 0 ? 0 : 64 - __builtin_clzll(value);
}

struct Schedule {
    std::uint64_t bits = 0;
    std::uint8_t length = 0;
};

Schedule forced_zero_schedule(std::uint64_t initial) {
    u128 state = initial;
    Schedule schedule;
    for (int step = 0; step < SCHEDULE_CAP; ++step) {
        const unsigned residue = static_cast<unsigned>(state & 15);
        char branch;
        if (residue == 7) branch = 'u';
        else if (residue == 11) branch = 't';
        else return schedule;
        const u128 tail = (state - 3) >> 2;
        state = forward_generator(branch, forward_generator('p', tail));
        schedule.bits = (schedule.bits << 1) | (branch == 'u' ? 1 : 0);
        ++schedule.length;
    }
    throw std::runtime_error("forced zero schedule reached cap");
}

struct PrefixKey {
    std::uint64_t bits;
    std::uint8_t length;
    bool operator==(const PrefixKey& other) const {
        return bits == other.bits && length == other.length;
    }
};

struct PrefixHash {
    std::size_t operator()(const PrefixKey& key) const noexcept {
        std::uint64_t value = key.bits ^ (std::uint64_t{key.length} << 57);
        value ^= value >> 30;
        value *= 0xbf58476d1ce4e5b9ULL;
        value ^= value >> 27;
        value *= 0x94d049bb133111ebULL;
        value ^= value >> 31;
        return static_cast<std::size_t>(value);
    }
};

PrefixKey prefix_key(const Schedule& schedule, int end) {
    return {
        schedule.bits >> (schedule.length - end),
        static_cast<std::uint8_t>(end),
    };
}

std::string decode(std::uint64_t bits, int length) {
    std::string word;
    word.reserve(length);
    for (int index = length - 1; index >= 0; --index) {
        word.push_back(((bits >> index) & 1) ? 'u' : 't');
    }
    return word;
}

bool admissible(const std::string& word) {
    return word.find("uu") == std::string::npos
        && word.find("ttttt") == std::string::npos
        && word.find("ututtu") == std::string::npos;
}

std::string extension(const std::vector<int>& gaps, bool include_final_u) {
    std::string word = "u";
    for (std::size_t index = 0; index < gaps.size(); ++index) {
        word += std::string(gaps[index] - 1, 't');
        if (index + 1 < gaps.size() || include_final_u) word += 'u';
    }
    return word;
}

bool schedule_has_at(
    const Schedule& schedule,
    int cut,
    const std::string& target
) {
    if (cut + static_cast<int>(target.size()) > schedule.length) return false;
    for (int index = 0; index < static_cast<int>(target.size()); ++index) {
        const int shift = schedule.length - 1 - (cut + index);
        const char observed = ((schedule.bits >> shift) & 1) ? 'u' : 't';
        if (observed != target[index]) return false;
    }
    return true;
}

struct Pattern {
    std::vector<int> gaps;
    std::string target;
    std::string complete;
};

void build_patterns_recursive(
    int return_count,
    std::vector<int>& current,
    std::vector<Pattern>& output
) {
    if (static_cast<int>(current.size()) == return_count) {
        const std::string target = extension(current, false);
        const std::string complete = extension(current, true);
        if (admissible(complete)) output.push_back({current, target, complete});
        return;
    }
    for (int gap : GAPS) {
        current.push_back(gap);
        build_patterns_recursive(return_count, current, output);
        current.pop_back();
    }
}

std::vector<Pattern> patterns(int return_count) {
    std::vector<Pattern> output;
    std::vector<int> current;
    build_patterns_recursive(return_count, current, output);
    return output;
}

struct Example {
    int complexity;
    std::uint64_t state;
    int cut;
    std::string base;
    std::vector<int> gaps;
    std::string schedule;
};

struct Summary {
    std::uint64_t outputs = 0;
    std::uint64_t eligible = 0;
    std::uint64_t two = 0;
    std::uint64_t three = 0;
    int maximum_schedule = 0;
    std::vector<Example> two_examples;
    std::vector<Example> three_examples;
};

Summary run_phase(
    char phase,
    const std::vector<Pattern>& two_patterns,
    const std::vector<Pattern>& three_patterns
) {
    std::unordered_set<std::uint64_t> states{phase == 'p' ? 3ULL : 1ULL};
    std::unordered_map<PrefixKey, std::uint8_t, PrefixHash> minimum;
    Summary summary;
    std::cout << "phase=" << phase << '\n';

    for (int complexity = 1; complexity <= MAXIMUM_COMPLEXITY; ++complexity) {
        std::vector<std::pair<std::uint64_t, Schedule>> rows;
        rows.reserve(states.size());
        const int expected = phase == 'p' ? 2 * complexity : 2 * complexity - 1;
        for (std::uint64_t state : states) {
            if (bit_length(state) != expected) {
                throw std::runtime_error("frontier bit-length law failed");
            }
            if ((state & 3) != 3) continue;
            const Schedule schedule = forced_zero_schedule(state);
            rows.emplace_back(state, schedule);
            summary.maximum_schedule = std::max(
                summary.maximum_schedule, static_cast<int>(schedule.length)
            );
            for (int end = 0; end <= schedule.length; ++end) {
                minimum.emplace(prefix_key(schedule, end), complexity);
            }
        }

        std::uint64_t level_two = 0;
        std::uint64_t level_three = 0;
        for (const auto& [state, schedule] : rows) {
            for (int cut = 0; cut <= schedule.length; ++cut) {
                const PrefixKey key = prefix_key(schedule, cut);
                if (minimum.at(key) != complexity) continue;
                const std::string base = decode(key.bits, cut);
                auto scan = [&] (
                    const std::vector<Pattern>& candidates,
                    std::uint64_t& level_count,
                    std::uint64_t& total_count,
                    std::vector<Example>& examples
                ) {
                    for (const Pattern& candidate : candidates) {
                        if (!schedule_has_at(schedule, cut, candidate.target)) continue;
                        if (!admissible(base + candidate.complete)) continue;
                        ++level_count;
                        ++total_count;
                        if (examples.size() < 4) {
                            examples.push_back({
                                complexity,
                                state,
                                cut,
                                base,
                                candidate.gaps,
                                decode(schedule.bits, schedule.length),
                            });
                        }
                    }
                };
                scan(
                    two_patterns,
                    level_two,
                    summary.two,
                    summary.two_examples
                );
                scan(
                    three_patterns,
                    level_three,
                    summary.three,
                    summary.three_examples
                );
            }
        }

        summary.outputs += states.size();
        summary.eligible += rows.size();
        if (level_two || level_three) {
            std::cout << "candidate_level=" << complexity
                      << " two=" << level_two
                      << " three=" << level_three << '\n';
        }

        if (complexity != MAXIMUM_COMPLEXITY) {
            std::unordered_set<std::uint64_t> next;
            next.reserve(states.size() * 3);
            for (std::uint64_t state : states) {
                const std::uint64_t stepped =
                    state ^ ((state << 1) | (state << 2));
                next.insert(stepped);
                next.insert(stepped ^ 1);
                if ((state & 1) == 0) next.insert(stepped ^ 3);
            }
            states.swap(next);
        }
    }

    std::cout << "phase_outputs_checked=" << summary.outputs << '\n';
    std::cout << "phase_eligible_outputs=" << summary.eligible << '\n';
    std::cout << "phase_max_schedule=" << summary.maximum_schedule << '\n';
    std::cout << "phase_two_return_candidates=" << summary.two << '\n';
    std::cout << "phase_three_return_candidates=" << summary.three << '\n';
    for (const Example& example : summary.two_examples) {
        std::cout << "two_example complexity=" << example.complexity
                  << " state=0x" << std::hex << example.state << std::dec
                  << " cut=" << example.cut
                  << " base=" << example.base
                  << " gaps=";
        for (std::size_t index = 0; index < example.gaps.size(); ++index) {
            if (index) std::cout << ',';
            std::cout << example.gaps[index];
        }
        std::cout << " schedule=" << example.schedule << '\n';
    }
    return summary;
}
}  // namespace

int main() {
    const std::vector<Pattern> two_patterns = patterns(2);
    const std::vector<Pattern> three_patterns = patterns(3);
    std::cout << "maximum_complexity=" << MAXIMUM_COMPLEXITY << '\n';
    std::cout << "two_patterns=" << two_patterns.size() << '\n';
    std::cout << "three_patterns=" << three_patterns.size() << '\n';

    const Summary p = run_phase('p', two_patterns, three_patterns);
    const Summary u = run_phase('u', two_patterns, three_patterns);
    std::cout << "total_outputs_checked=" << p.outputs + u.outputs << '\n';
    std::cout << "total_eligible_outputs=" << p.eligible + u.eligible << '\n';
    std::cout << "total_two_return_candidates=" << p.two + u.two << '\n';
    std::cout << "total_three_return_candidates=" << p.three + u.three << '\n';

    if (p.two != 0 || u.two != 1 || p.three != 0 || u.three != 0) {
        throw std::runtime_error("unexpected plateau-candidate totals");
    }
    if (u.two_examples.empty() || u.two_examples.front().state != KNOWN_STATE) {
        throw std::runtime_error("known complexity-25 candidate was not recovered");
    }

    const Schedule schedule = forced_zero_schedule(KNOWN_STATE);
    const std::string word = decode(schedule.bits, schedule.length);
    std::cout << "known_forced_schedule=" << word << '\n';
    if (word != "tutututttutututt") {
        throw std::runtime_error("known forced schedule changed");
    }
    std::cout << "known_third_required_branch=u\n";
    std::cout << "known_observed_branch=t\n";
    return 0;
}
