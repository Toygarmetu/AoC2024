def parse_map(input_map):
    lines = [list(line.strip()) for line in input_map.strip().splitlines()]
    return lines

def find_start(grid):
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] in '^v<>':
                return (x, y), grid[y][x]
    return None, None

def get_next_pos(pos, direction):
    x, y = pos
    if direction == '^': return (x, y-1)
    if direction == 'v': return (x, y+1)
    if direction == '<': return (x-1, y)
    if direction == '>': return (x+1, y)
    return pos

def turn_right(direction):
    return {'^': '>', '>': 'v', 'v': '<', '<': '^'}[direction]

def is_valid_move(grid, pos):
    x, y = pos
    if y < 0 or y >= len(grid) or x < 0 or x >= len(grid[0]):
        return False
    return grid[y][x] != '#'

def simulate_path(grid, start_pos, start_dir, obstacle_pos=None):
    visited = set()
    pos = start_pos
    direction = start_dir
    steps = 0
    max_steps = len(grid) * len(grid[0]) * 4  # Maximum possible unique states
    
    while steps < max_steps:
        if pos == obstacle_pos:
            return None, None  # Hit the obstacle
            
        state = (pos, direction)
        if state in visited:
            # Found a loop - return visited positions and True for loop
            return visited, True
        
        visited.add(state)
        next_pos = get_next_pos(pos, direction)
        
        # Check if we're about to leave the grid
        if not (0 <= next_pos[0] < len(grid[0]) and 0 <= next_pos[1] < len(grid)):
            return visited, False  # No loop found, guard exits map
            
        # Try moving forward if not blocked
        if is_valid_move(grid, next_pos) and next_pos != obstacle_pos:
            pos = next_pos
        else:
            direction = turn_right(direction)
            
        steps += 1
        
    return visited, False # No loop found, guard stuck in loop

def find_loop_positions(input_map):
    grid = parse_map(input_map)
    start_pos, start_dir = find_start(grid)
    loop_positions = set()
    
    
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            # Skip if position is already occupied or is start position
            if grid[y][x] != '.' or (x, y) == start_pos:
                continue
                
            # Simulate path with obstacle at (x, y)
            visited, found_loop = simulate_path(grid, start_pos, start_dir, (x, y))
            
            # If a loop was found, this is a valid obstacle position
            if found_loop:
                loop_positions.add((x, y))
    
    return len(loop_positions)

example_map = """ Give your map here""".strip()

result = find_loop_positions(example_map)
print(f"Found {result} possible positions for creating a loop")