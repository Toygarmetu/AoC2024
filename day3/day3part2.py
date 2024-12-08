import re

# Open the file containing the input
with open("input.txt", "r") as input_file:
    corrupted_memory = input_file.read()


do_pattern = re.compile(r"do\(\)")
dont_pattern = re.compile(r"don't\(\)")
mul_pattern = re.compile(r"mul\((\d+),(\d+)\)")


search_start = 0

total_sum = 0
mul_enabled = True  # Multiplications are enabled by default


while search_start < len(corrupted_memory):
    do_match = do_pattern.search(corrupted_memory, search_start)
    dont_match = dont_pattern.search(corrupted_memory, search_start)
    mul_match = mul_pattern.search(corrupted_memory, search_start)

    # Check for `do()` instruction (enable mul)
    if do_match and (not dont_match or do_match.start() < dont_match.start()) and (not mul_match or do_match.start() < mul_match.start()):
        mul_enabled = True  # Enable `mul()` instructions
        search_start = do_match.end()  # Move past the `do()` instruction
    # Check for `don't()` instruction (disable mul)
    elif dont_match and (not mul_match or dont_match.start() < mul_match.start()):
        mul_enabled = False  # Disable `mul()` instructions
        search_start = dont_match.end()  # Move past the `don't()` instruction
    # Check for valid `mul(X,Y)` instructions
    elif mul_match:
        if mul_enabled:
            # Extract numbers X and Y
            x = int(mul_match.group(1))
            y = int(mul_match.group(2))

            
            total_sum += x * y
        search_start = mul_match.end()  # Move past the `mul()` instruction
    
    else:
        break

# Output the result
print("Sum of valid multiplications:", total_sum)