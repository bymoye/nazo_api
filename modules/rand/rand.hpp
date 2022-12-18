#pragma once
#include <algorithm>
#include <cmath>
#include <limits>
#include <random>

namespace Storm
{
    using Integer = long long;

    inline std::mt19937_64 &get_generator()
    {
        static std::mt19937_64 generator{std::random_device{}()};
        return generator;
    }

    inline void seed(unsigned long long seed)
    {
        get_generator().seed(seed);
    }

    inline auto uniform_int_variate(Integer a, Integer b) -> Integer
    {
        std::uniform_int_distribution<Integer> distribution{std::min(a, b), std::max(b, a)};
        return distribution(get_generator());
    }

    inline auto random_below(Integer number) -> Integer
    {
        return uniform_int_variate(0, number - 1);
    }

    inline auto random_range(Integer start, Integer stop, Integer step) -> Integer
    {
        if (start == stop || step == 0)
            return start;

        // Avoid calculating width if step is negative, because it could cause an overflow
        if (step > 0)
        {
            const auto width{std::abs(start - stop) - 1};
            const auto pivot{std::min(start, stop)};
            const auto step_size{std::abs(step)};
            return pivot + step_size * random_below((width + step_size) / step_size);
        }
        else
        {
            const auto width{std::abs(stop - start) - 1};
            const auto pivot{std::max(start, stop)};
            const auto step_size{std::abs(step)};
            return pivot - step_size * random_below((width + step_size) / step_size);
        }
    }
}