def find_x_mas(grid):
    # Convert input to list of lists becuase it's string
    if isinstance(grid, str):
        grid = [list(line.strip()) for line in grid.strip().split('\n')]
    
    rows = len(grid)
    cols = len(grid[0])
    count = 0
    
    def check_mas(row, col, dr, dc):
        for i in range(3):  # MAS is 3 letters
            new_row = row + i*dr
            new_col = col + i*dc
            if not (0 <= new_row < rows and 0 <= new_col < cols):
                return False
        
        
        forwards = (grid[row][col] == 'M' and
                   grid[row + dr][col + dc] == 'A' and
                   grid[row + 2*dr][col + 2*dc] == 'S')
                   
        
        backwards = (grid[row][col] == 'S' and
                    grid[row + dr][col + dc] == 'A' and
                    grid[row + 2*dr][col + 2*dc] == 'M')
                    
        return forwards or backwards
    
    
    for row in range(1, rows-1):  # Skip edges since we need room for the X
        for col in range(1, cols-1):
            # Check upper-left to lower-right diagonal
            ul_lr = check_mas(row-1, col-1, 1, 1)
            # Check upper-right to lower-left diagonal
            ur_ll = check_mas(row-1, col+1, 1, -1)
            
            # If both diagonals contain MAS, we found an X-MAS
            if ul_lr and ur_ll:
                count += 1
    
    return count

test_grid = """Input was too long
""".strip()

result = find_x_mas(test_grid)
print(f"Number of X-MAS: {result}")  