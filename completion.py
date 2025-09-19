import copy
hints = 0
strikes = 0
def is_safe(grid, size, row, col, num):
    # Checks if 'num' can be placed at (row, col) without breaking Sudoku rules
    for i in range(size):
        # Checks the row and column for 'num'
        if grid[row][i] == num or grid[i][col] == num:
            return False

    # Checks the corresponding box
    box_size = int(size ** 0.5)
    start_row, start_col = box_size * (row // box_size), box_size * (col // box_size)
    for i in range(box_size):
        for j in range(box_size):
            if grid[start_row + i][start_col + j] == num:
                return False

    return True  # Returns True if 'num' can be safely placed

def solve_sudoku(grid):
    size = len(grid)
    for row in range(size):
        for col in range(size):
            if grid[row][col] == 0:  # Looks for an empty cell
                for num in range(1, size + 1):  # Tries all possible numbers
                    if is_safe(grid, size, row, col, num):  # Checks if the number is safe to place
                        grid[row][col] = num  # Places the number
                        if solve_sudoku(grid):  # Continues to solve the rest of the grid
                            return True
                        grid[row][col] = 0  # Backtracks if placing num didn't lead to a solution
                return False
    return True  # Returns True if the entire grid is filled without conflicts

def count_solutions(grid):
    size = len(grid)
    original_grid = copy.deepcopy(grid)  # Makes a deep copy of the grid
    solution_count = [0]  # Initializes solution count

    def solve_unique_sudoku(row, col):
        nonlocal solution_count
        # Helper function to count solutions using backtracking
        if row == size:
            solution_count[0] += 1  # Increments solution count
            return

        # Skips filled cells
        if grid[row][col] != 0:
            if col == size - 1:
                solve_unique_sudoku(row + 1, 0)
            else:
                solve_unique_sudoku(row, col + 1)
            return

        # Tries placing each number and counts solutions
        for num in range(1, size + 1):
            if is_safe(grid, size, row, col, num):
                grid[row][col] = num
                if col == size - 1:
                    solve_unique_sudoku(row + 1, 0)
                else:
                    solve_unique_sudoku(row, col + 1)
                grid[row][col] = 0  # Backtracks

    solve_unique_sudoku(0, 0)
    grid = original_grid  # Restores the original grid
    return solution_count[0]  # Returns the count of unique solutions

def solve_comp(input_grid):
    size = len(input_grid)
    if any(len(row) != size for row in input_grid):
        return "Error: Invalid grid size"

    if count_solutions(input_grid) == 1:
        solve_sudoku(input_grid)
        return input_grid
    else:
        return "Error: No unique solution or multiple solutions exist"

# Helper function to display the grid
def display_grid(grid):
    for row in grid:
        print(" ".join(str(num) for num in row))


        
initial_grid = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

initial_grid_solve = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

#solved_grid = solve(initial_grid_solve)
#print(solved_grid)

#on_screen = display_grid(initial_grid)
#hint(initial_grid,0,2)
#display_grid(initial_grid)
