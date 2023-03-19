#include <chrono>
#include <cstdio>
#include <cstdlib>
#include <cstdint>
#include <vector>
#include <random>
#include <algorithm>

using namespace std;
using uint = uint32_t;

std::vector<uint> //
makeData(size_t size)
{
    std::vector<uint> v(size);
    for (size_t i = 0; i < v.size(); ++i)
    {
        v[i] = uint(i & 0xff);
    }
    return v;
}

size_t getSize(int argc, char const *argv[])
{
    if (argc < 2)
    {
        return 100;
    }
    return size_t(std::atoll(argv[1]));
}

int64_t simple(std::vector<uint> const &data)
{
    int64_t sum = 0;
    for (size_t i = 0, size = data.size(); i < size; ++i)
    {
        if (128 <= data[i])
        {
            sum += data[i];
        }
    }
    return sum;
}
int64_t opt_simple(std::vector<uint> const &data)
{
    int64_t sum = 0;
    for (size_t i = 0, size = data.size(); i < size; ++i)
    {
        auto v = data[i];
        sum += ((v < 128) - 1) & v;
    }
    return sum;
}

int64_t foreach (std::vector<uint> const &data)
{
    int64_t sum = 0;
    for (auto const &v : data)
    {
        if (128 <= v)
        {
            sum += v;
        }
    }
    return sum;
}
int64_t opt_foreach(std::vector<uint> const &data)
{
    int64_t sum = 0;
    for (auto const &v : data)
    {
        sum += ((v < 128) - 1) & v;
    }
    return sum;
}

template <typename proc_t> //
void measure(char const *name, std::vector<uint> const &data, proc_t const &proc)
{
    using clock = chrono::high_resolution_clock;
    using namespace std::chrono_literals;
    int64_t sum = 0;
    auto t0 = clock::now();
    for (int i = 0; i < 1000; ++i)
    {
        sum += proc(data);
    }
    auto dur = clock::now() - t0;
    auto durSec = (dur / 1ns) * 1e-9;
    printf("  %11s: duration=%5.2fs  sum=%lld\n", name, durSec, (long long)sum);
}

int main(int argc, char const *argv[])
{
    auto data = makeData(getSize(argc, argv));
    std::mt19937 rng{1234};
    for (int i = 0; i < 2; ++i)
    {
        std::shuffle(data.begin(), data.end(), rng);
        puts("shuffled");
        measure("simple", data, simple);
        measure("foreach", data, foreach);
        measure("opt-simple", data, opt_simple);
        measure("opt-foreach", data, opt_foreach);
        std::sort(data.begin(), data.end());
        puts("sorted");
        measure("simple", data, simple);
        measure("foreach", data, foreach);
        measure("opt-simple", data, opt_simple);
        measure("opt-foreach", data, opt_foreach);
    }
}