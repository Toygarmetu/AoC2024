#include <iostream>
#include <fstream>
#include <regex>
#include <string>

int main() {
    // Open the file containing the input
    std::ifstream input_file("input.txt");
    if (!input_file) {
        std::cerr << "Error: Unable to open input file!" << std::endl;
        return 1;
    }

    // Read the entire file content into a single string
    std::string corrupted_memory((std::istreambuf_iterator<char>(input_file)),
                                 std::istreambuf_iterator<char>());
    input_file.close();

    // Regular expressions for `do()`, `don't()`, and `mul(X,Y)` instructions
    std::regex do_pattern(R"(do\(\))");
    std::regex dont_pattern(R"(don't\(\))");
    std::regex mul_pattern(R"(mul\((\d+),(\d+)\))");

    // Iterator to traverse the string
    auto search_start = corrupted_memory.cbegin();

    int total_sum = 0;
    bool mul_enabled = true; // Multiplications are enabled by default

    // Process the file content
    while (search_start != corrupted_memory.cend()) {
        std::smatch match;

        // Check for `do()` instruction (enable mul)
        if (std::regex_search(search_start, corrupted_memory.cend(), match, do_pattern)) {
            mul_enabled = true;  // Enable `mul()` instructions
            search_start = match.suffix().first; // Move past the `do()` instruction
        } 
        // Check for `don't()` instruction (disable mul)
        else if (std::regex_search(search_start, corrupted_memory.cend(), match, dont_pattern)) {
            mul_enabled = false; // Disable `mul()` instructions
            search_start = match.suffix().first; // Move past the `don't()` instruction
        }
        // Check for valid `mul(X,Y)` instructions
        else if (std::regex_search(search_start, corrupted_memory.cend(), match, mul_pattern)) {
            if (mul_enabled) {
                // Extract numbers X and Y
                int x = std::stoi(match[1].str());
                int y = std::stoi(match[2].str());

                // Calculate the product and add to the total sum
                total_sum += x * y;
            }
            search_start = match.suffix().first; // Move past the `mul()` instruction
        } 
        // If none of the patterns match, break the loop
        else {
            break;
        }
    }

    // Output the result
    std::cout << "Sum of valid multiplications: " << total_sum << std::endl;

    return 0;
}