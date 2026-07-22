#pragma once

#include <cstddef>
#include <cstdint>
#include <functional>
#include <iosfwd>
#include <span>
#include <string_view>
#include <vector>

namespace rule30 {

enum class Backend {
    scalar,
    avx2,
    automatic,
};

[[nodiscard]] std::string_view backend_name(Backend backend) noexcept;
[[nodiscard]] bool avx2_compiled() noexcept;
[[nodiscard]] bool avx2_runtime_supported() noexcept;
[[nodiscard]] Backend resolve_backend(Backend requested);

class PackedRow {
public:
    [[nodiscard]] static PackedRow single_seed();
    [[nodiscard]] static PackedRow from_bits(std::span<const std::uint8_t> bits);

    [[nodiscard]] std::size_t logical_size() const noexcept;
    [[nodiscard]] std::size_t word_count() const noexcept;
    [[nodiscard]] bool bit(std::size_t index) const;
    [[nodiscard]] std::span<const std::uint64_t> words() const noexcept;
    [[nodiscard]] std::vector<std::uint8_t> unpack() const;

    void step(Backend backend = Backend::automatic);

private:
    PackedRow(std::size_t logical_size, std::vector<std::uint64_t> words);

    std::size_t logical_size_{};
    std::vector<std::uint64_t> words_;
};

struct BalanceCheckpoint {
    std::size_t count{};
    std::uint64_t ones{};
    std::int64_t discrepancy{};

    friend bool operator==(const BalanceCheckpoint&, const BalanceCheckpoint&) = default;
};

struct GenerationSummary {
    std::size_t count{};
    std::uint64_t ones{};
    std::uint64_t zeros{};
    std::int64_t discrepancy{};
    Backend backend{Backend::scalar};
    std::vector<BalanceCheckpoint> checkpoints;
};

struct GenerationOptions {
    Backend backend{Backend::automatic};
    std::size_t chunk_size{64U * 1024U};
    std::vector<std::size_t> checkpoints;
};

using ByteSink = std::function<void(std::span<const std::uint8_t>)>;

// Generate exactly count bits: c_0, ..., c_(count-1). The sink, when present,
// receives nonempty chunks whose bytes are the numeric values 0 and 1.
[[nodiscard]] GenerationSummary stream_center_prefix(
    std::size_t count,
    const GenerationOptions& options,
    const ByteSink& sink = {});

[[nodiscard]] std::vector<std::uint8_t> generate_center_prefix(
    std::size_t count,
    Backend backend = Backend::automatic,
    std::size_t chunk_size = 64U * 1024U);

[[nodiscard]] GenerationSummary write_center_prefix_bytes(
    std::ostream& output,
    std::size_t count,
    const GenerationOptions& options = {});

}  // namespace rule30
