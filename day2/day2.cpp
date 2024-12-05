#include <iostream>
#include <sstream>
#include <string>
#include <vector>

using namespace std;

bool is_safe_sequence(const vector<int>& levels) {
    if (levels.size() < 2) return true;
    
    // Check first difference to determine if sequence should be increasing or decreasing
    bool should_increase = levels[1] > levels[0];
    
    for (size_t i = 1; i < levels.size(); i++) {
        int diff = levels[i] - levels[i-1];
        
        // Check if difference is between 1 and 3 (inclusive)
        if (abs(diff) < 1 || abs(diff) > 3) {
            return false;
        }
        
        // Check if direction matches the initial direction
        if (should_increase && diff <= 0) {
            return false;
        }
        if (!should_increase && diff >= 0) {
            return false;
        }
    }
    
    return true;
}

bool can_be_safe_with_removal(const vector<int>& levels) {
    // Try removing each level one at a time
    for (size_t skip_idx = 0; skip_idx < levels.size(); skip_idx++) {
        std::vector<int> modified_levels;
        // Create new sequence without the current index
        for (size_t i = 0; i < levels.size(); i++) {
            if (i != skip_idx) {
                modified_levels.push_back(levels[i]);
            }
        }
        
        // Check if this modified sequence is safe
        if (is_safe_sequence(modified_levels)) {
            return true;
        }
    }
    return false;
}

int count_safe_reports(istream& input) {
    string line;
    int safe_count = 0;
    
    while (getline(input, line)) {
        if (line.empty()) continue;  // Skip empty lines
        
        vector<int> levels;
        istringstream iss(line);
        int level;
        
        // Parse numbers from the line
        while (iss >> level) {
            levels.push_back(level);
        }
        
        if (is_safe_sequence(levels) || can_be_safe_with_removal(levels)) {
            safe_count++;
        }
    }
    
    return safe_count;
}

int main() {
    cout << "Enter the reactor level reports (press Ctrl+D on Unix or Ctrl+Z on Windows when done):\n";
    int result = count_safe_reports(cin);
    cout << "Number of safe reports: " << result << endl;
    return 0;
}