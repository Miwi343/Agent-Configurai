#include <iostream>
#include <cstdio>
#include <cstdlib>
#include <string>
#include <stdexcept>
#include <array>

std::string exec(const char* cmd) {
    std::array<char, 128> buffer;
    std::string result;
    FILE* pipe = popen(cmd, "r");
    if (!pipe) {
        throw std::runtime_error("popen() failed!");
    }
    while (fgets(buffer.data(), buffer.size(), pipe) != nullptr) {
        result += buffer.data();
    }
    auto rc = pclose(pipe);
    if (rc == -1) {
        throw std::runtime_error("pclose() failed!");
    }
    return result;
}

int main(int argc, char *argv[]) {
    if (argc < 3) {
        std::cerr << "Usage: " << argv[0] << " <terminal_id> <command>" << std::endl;
        return 1;
    }

    std::string terminal_id = argv[1];
    std::string command = argv[2];

    // Construct the full command to run in the specified terminal
    std::string full_command = "osascript -e 'tell application \"Terminal\" to do script \"" + command + "\" in window id " + terminal_id + "'";

    // Execute the command and capture the output
    std::string output = exec(full_command.c_str());

    // Print the output
    std::cout << output << std::endl;

    return 0;
}
