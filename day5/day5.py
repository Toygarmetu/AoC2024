from collections import defaultdict, deque

def parse_input(text):
    rules_text, sequences_text = text.strip().split('\n\n')
    
    # Parse rules into a graph
    rules = defaultdict(set)
    in_degree = defaultdict(int)
    for line in rules_text.strip().split('\n'):
        before, after = map(int, line.split('|'))
        rules[before].add(after)
    
    # Parse sequences
    sequences = []
    for line in sequences_text.strip().split('\n'):
        sequences.append([int(x) for x in line.strip().split(',')])
    
    return rules, sequences

def is_valid_sequence(sequence, rules):
    positions = {num: i for i, num in enumerate(sequence)}
    
    for page in sequence:
        if page in rules:
            for must_come_after in rules[page]:
                if must_come_after in positions:
                    if positions[page] >= positions[must_come_after]:
                        return False
    return True

def topological_sort(numbers, rules):
    # Create a graph only including the numbers we care about
    graph = defaultdict(set)
    in_degree = defaultdict(int)
    numbers_set = set(numbers)
    
    # Only include rules that involve our numbers
    for before in rules:
        if before in numbers_set:
            for after in rules[before]:
                if after in numbers_set:
                    graph[before].add(after)
                    in_degree[after] += 1
    
    # Initialize queue with all nodes that have no incoming edges
    queue = deque([n for n in numbers_set if in_degree[n] == 0])
    result = []
    
    while queue:
        current = queue.popleft()
        result.append(current)
        
        # Process neighbors
        for neighbor in graph[current]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    # Check if we used all numbers
    if len(result) != len(numbers):
        remaining = numbers_set - set(result)
        result.extend(sorted(remaining))
    
    return result

def get_middle_number(sequence):
    return sequence[len(sequence) // 2]

def solve_page_ordering_part2(input_text):
    rules, sequences = parse_input(input_text)
    
    # Find and fix incorrect sequences
    incorrect_middles = []
    for sequence in sequences:
        if not is_valid_sequence(sequence, rules):
            # This is an incorrect sequence - sort it properly
            corrected = topological_sort(sequence, rules)
            middle = get_middle_number(corrected)
            incorrect_middles.append(middle)
            print(f"Fixed sequence: {sequence} -> {corrected} (middle: {middle})")
    
    total = sum(incorrect_middles)
    print(f"Found {len(incorrect_middles)} incorrect sequences")
    return total


with open('input.txt', 'r') as file:
    input_text = file.read()

result = solve_page_ordering_part2(input_text)
print(f"Sum of middle numbers from fixed sequences: {result}")