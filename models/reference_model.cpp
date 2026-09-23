#include <cstdlib>
#include <iomanip>
#include <iostream>

int main(int argc, char* argv[]) {
    if (argc != 4) {
        std::cerr << "Usage: " << argv[0]
                  << " <req> <data0_hex> <data1_hex>\n";
        return 1;
    }

    int req = std::strtol(argv[1], nullptr, 0);
    int data0 = std::strtol(argv[2], nullptr, 16);
    int data1 = std::strtol(argv[3], nullptr, 16);

    int gnt = 0;
    int bus = 0;

    // Match the RTL/scoreboard priority:
    // request 0 has priority over request 1.
    if (req & 0b01) {
        gnt = 1;
        bus = data0;
    } else if (req & 0b10) {
        gnt = 2;
        bus = data1;
    }

    std::cout << "gnt=" << gnt
              << " bus=0x"
              << std::uppercase
              << std::hex
              << std::setw(2)
              << std::setfill('0')
              << bus
              << '\n';

    return 0;
}
