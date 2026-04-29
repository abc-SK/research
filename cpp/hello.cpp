#include <iostream>
#include <vector>

int main() {
    std::vector<int> a{0,1,2,3,4};
    for (auto x : a) std::cout << x << " ";
    std::cout << "\nHello C++!\n";
    return 0;
}