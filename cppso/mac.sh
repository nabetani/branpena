set -eu
g++-12 -O2 -Wall -std=c++17 main.cpp && ./a.out 10000000 > mac_gcc.txt
clang++ -O2 -Wall -std=c++17 main.cpp && ./a.out 10000000 > mac_clang.txt