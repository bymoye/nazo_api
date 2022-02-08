#pragma once
#include <algorithm>
#include <cmath>
#include <limits>
#include <random>


namespace Storm { // Storm 3.2.2 Custom
    using Integer = long long;
    
    namespace Engine {
        struct Cyclone {
            using MT64_SCRAM = std::shuffle_order_engine<std::discard_block_engine<std::mt19937_64, 12, 8>, 256>;
            std::random_device hardware_seed;
            MT64_SCRAM hurricane { hardware_seed() };
            template <typename D>
            auto operator()(D distribution) {
                return distribution(hurricane);
            }
            auto seed(unsigned long long seed) -> void {
                MT64_SCRAM seeded_storm { seed == 0 ? hardware_seed() : seed };
                hurricane = seeded_storm;
            }
        } cyclone;
    }

    auto uniform_int_variate(Storm::Integer a, Storm::Integer b) -> Storm::Integer {
        std::uniform_int_distribution<Storm::Integer> distribution { std::min(a, b), std::max(b, a) };
        return Engine::cyclone(distribution);
    }

    auto random_below(Storm::Integer number) -> Storm::Integer {
        return Storm::uniform_int_variate(0, std::nextafter(number, 0));
    }

    auto random_range(Storm::Integer start, Storm::Integer stop, Storm::Integer step) -> Storm::Integer {
        if (start == stop or step == 0) return start;
        const auto width { std::abs(start - stop) - 1 };
        const auto pivot { step > 0 ? std::min(start, stop) : std::max(start, stop) };
        const auto step_size { std::abs(step) };
        return pivot + step_size * Storm::random_below((width + step_size) / step);
    }
    
} // end namespace