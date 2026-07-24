#include <boost/multiprecision/cpp_int.hpp>
#include <array>
#include <cstdint>
#include <iostream>
#include <map>
#include <stdexcept>
#include <string>
#include <vector>

using boost::multiprecision::cpp_int;

namespace {
constexpr int BLOCKS = 200000;
constexpr std::array<unsigned, 3> BAD{28, 44, 60};

cpp_int advance_fringe(const cpp_int& state) {
    const cpp_int row = 1 | (state << 1);
    const cpp_int odd = row ^ ((row >> 1) | (row >> 2));
    return (odd << 1) ^ (odd | (odd >> 1));
}

char branch_letter(const cpp_int& state) {
    return static_cast<unsigned>(state & 3) == 0 ? 'u' : 't';
}

std::string branch_word_from_z(unsigned z, int length) {
    cpp_int state = cpp_int{4} * z;
    std::string word;
    for (int index = 0; index < length; ++index) {
        word.push_back(branch_letter(state));
        state = advance_fringe(state);
    }
    return word;
}

bool bad_residue(unsigned residue) {
    for (unsigned value : BAD) if (residue == value) return true;
    return false;
}
}  // namespace

int main() {
    std::vector<unsigned> witnesses;
    for (unsigned z = 0; z < 256; ++z) {
        const bool pair = branch_word_from_z(z, 5) == "ututu";
        const bool predicted = bad_residue(z & 63);
        if (pair != predicted) {
            throw std::runtime_error("mod-64 cylinder classification failed");
        }
        if (pair) witnesses.push_back(z);
    }

    cpp_int state = 0;
    std::map<unsigned, std::uint64_t> residue_counts;
    std::map<int, std::uint64_t> gap_counts;
    std::uint64_t returns = 0;
    std::uint64_t bad_visits = 0;
    std::uint64_t pair_22 = 0;
    int previous_position = -1;
    int previous_gap = -1;
    int last_gap_two_start = -1;

    for (int block = 0; block < BLOCKS; ++block) {
        if (branch_letter(state) == 'u') {
            const unsigned residue = static_cast<unsigned>((state >> 2) & 63);
            ++residue_counts[residue];
            ++returns;
            if (bad_residue(residue)) ++bad_visits;
            if (previous_position >= 0) {
                const int gap = block - previous_position;
                ++gap_counts[gap];
                if (previous_gap == 2 && gap == 2) ++pair_22;
                if (gap == 2) last_gap_two_start = previous_position;
                previous_gap = gap;
            }
            previous_position = block;
        }
        state = advance_fringe(state);
    }

    std::cout << "blocks=" << BLOCKS << '\n';
    std::cout << "cylinder_witnesses_mod_256=";
    for (std::size_t index = 0; index < witnesses.size(); ++index) {
        if (index) std::cout << ',';
        std::cout << witnesses[index];
    }
    std::cout << '\n';
    std::cout << "cylinder_residues_mod_64=28,44,60\n";
    std::cout << "return_count=" << returns << '\n';
    std::cout << "gap_counts=";
    bool first = true;
    for (const auto& [gap, count] : gap_counts) {
        if (!first) std::cout << ',';
        first = false;
        std::cout << gap << ':' << count;
    }
    std::cout << '\n';
    std::cout << "return_residue_counts_mod_64=";
    first = true;
    for (const auto& [residue, count] : residue_counts) {
        if (!first) std::cout << ',';
        first = false;
        std::cout << residue << ':' << count;
    }
    std::cout << '\n';
    std::cout << "bad_cylinder_visits=" << bad_visits << '\n';
    std::cout << "consecutive_gap_two_count=" << pair_22 << '\n';
    std::cout << "last_gap_two_start=" << last_gap_two_start << '\n';
    return 0;
}
