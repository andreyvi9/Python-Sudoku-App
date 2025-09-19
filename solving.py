import random
import copy

class SudokuSolver:
    def __init__(self, size):
        self.size = size  # Sets the size of the Sudoku grid (e.g., 9 for a standard Sudoku)
        self.grid = [[0 for _ in range(size)] for _ in range(size)]  # Initialises an empty grid

    def is_safe(self, row, col, num):
        # Checks if 'num' can be placed at (row, col) without breaking Sudoku rules
        for i in range(self.size):
            # Checks the row and column for 'num'
            if self.grid[row][i] == num or self.grid[i][col] == num:
                return False

        # Checks the corresponding box
        box_size = int(self.size ** 0.5)
        start_row, start_col = box_size * (row // box_size), box_size * (col // box_size)
        for i in range(box_size):
            for j in range(box_size):
                if self.grid[start_row + i][start_col + j] == num:
                    return False

        return True  # Returns True if 'num' can be safely placed

    def solve_sudoku(self):
        # Solves the Sudoku puzzle using backtracking
        for row in range(self.size):
            for col in range(self.size):
                if self.grid[row][col] == 0:  # Looks for an empty cell
                    for num in range(1, self.size + 1):  # Tries all possible numbers
                        if self.is_safe(row, col, num):  # Checks if the number is safe to place
                            self.grid[row][col] = num  # Places the number
                            if self.solve_sudoku():  # Continues to solve the rest of the grid
                                return True
                            self.grid[row][col] = 0  # Backtracks if placing num didn't lead to a solution
                    return False
        return True  # Returns True if the entire grid is filled without conflicts

    def count_solutions(self):
        # Counts the number of unique solutions for the current grid state
        original_grid = copy.deepcopy(self.grid)  # Makes a deep copy of the grid
        solution_count = [0]  # Initializes solution count

        def solve_unique_sudoku(row, col):
            # Helper function to count solutions using backtracking
            if row == self.size:
                solution_count[0] += 1  # Increments solution count
                return

            # Skips filled cells
            if self.grid[row][col] != 0:
                if col == self.size - 1:
                    solve_unique_sudoku(row + 1, 0)
                else:
                    solve_unique_sudoku(row, col + 1)
                return

            # Tries placing each number and counts solutions
            for num in range(1, self.size + 1):
                if self.is_safe(row, col, num):
                    self.grid[row][col] = num
                    if col == self.size - 1:
                        solve_unique_sudoku(row + 1, 0)
                    else:
                        solve_unique_sudoku(row, col + 1)
                    self.grid[row][col] = 0  # Backtracks

        solve_unique_sudoku(0, 0)
        self.grid = original_grid  # Restores the original grid
        return solution_count[0]  # Returns the count of unique solutions

    def solve(self, input_grid):
        # Function to solve the Sudoku puzzle based on user input
        if len(input_grid) != self.size or any(len(row) != self.size for row in input_grid):
            return "Error: Invalid grid size"

        self.grid = input_grid

        if self.count_solutions() == 1:
            self.solve_sudoku()
            return self.grid
        else:
            return "Error: No unique solution or multiple solutions exist"
    

# Helper function to display the grid
def display_grid(grid):
    for row in grid:
        print(" ".join(str(num) for num in row))

# Taking user input for grid and size
def get_user_input():
    try:
        size = int(input("Enter the size of the Sudoku grid: "))
        grid =  [
    [ 6,  0,  0,  0,  0,  6,  0,  0,  0, 15,  0,  0,  0,  0,  0,  0],
    [ 0,  0,  0,  4,  0,  0,  0, 14,  0,  0,  0,  0,  0,  0,  0,  0],
    [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
    [ 0,  0,  0,  0,  0,  0,  4,  0, 13,  0,  0,  0,  0,  0,  0,  0],
    [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
    [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
    [ 0,  0,  3,  0,  0,  0,  0,  0,  0,  0,  0,  6,  0,  0,  0,  0],
    [ 0,  0,  0,  0,  0,  0,  0,  0,  5,  0,  0,  0,  0,  0,  0,  0],
    [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
    [ 0,  0,  0,  0,  2,  0,  0,  0,  0,  0,  0,  0,  0,  3,  0,  0],
    [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  6,  0],
    [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
    [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  4,  0,  0,  0,  0,  0,  0],
    [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
    [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
    [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  6,  0,  0,  0,  0,  0,  0]
]
        
        return size, grid
    except ValueError as e:
        print(f"Error: {e}")
        return None, None
    
##################################################################################
# Option B
def optionb():
    print("Welcome to the Sudoku Solver!")
    size, input_grid = get_user_input()
    if size and input_grid:
        solver = SudokuSolver(size)
        solution = solver.solve(input_grid)
        if isinstance(solution, list):
            print("\nSolution:")
            display_grid(solution)
        else:
            print(solution)

    
#################TESTING##################################
# Example Sudoku puzzle (9x9)
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

initial_grid_toomany = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 0],
    [4, 0, 0, 0, 0, 3, 0, 0, 0],
    [7, 0, 0, 0, 2, 0, 0, 0, 0],
    [0, 6, 0, 0, 0, 0, 2, 0, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 0],
    [0, 0, 0, 0, 8, 0, 0, 7, 0]
]
# extra 5 top right
initial_grid_none = [
    [5, 3, 0, 0, 7, 0, 0, 0, 5],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]
# Example Sudoku puzzle (4x4)
initial_grid_4x4 = [
    [1, 2, 3, 4],
    [3, 4, 2, 1],
    [2, 1, 0, 0],
    [4, 3, 0, 0]
]

initial_grid_4x4_toomany = [
    [1, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 3]
]

#extra 1 right of top left
initial_grid_4x4_none = [
    [1, 1, 0, 4],
    [0, 3, 0, 0],
    [0, 0, 2, 0],
    [4, 0, 0, 3]
]

# Example Sudoku puzzle (16x16)
initial_grid_16x16 = [
    [0, 9, 13, 0, 4, 0, 7, 11, 1, 10, 5, 0, 2, 0, 3, 12],
    [4, 0, 0, 11, 16, 0, 13, 0, 2, 8, 3, 0, 1, 0, 0, 0],
    [1, 0, 5, 0, 2, 8, 0, 0, 0, 9, 13, 15, 4, 6, 0, 0],
    [0, 0, 3, 12, 0, 10, 5, 0, 4, 0, 0, 11, 16, 0, 13, 15],
    [9, 16, 0, 0, 6, 4, 11, 7, 10, 1, 0, 0, 0, 2, 12, 3],
    [0, 4, 0, 7, 9, 16, 15, 0, 8, 0, 12, 0, 10, 0, 14, 0],
    [10, 0, 14, 5, 0, 2, 12, 3, 9, 0, 0, 13, 6, 0, 11, 0],
    [0, 2, 12, 0, 0, 0, 14, 5, 0, 4, 0, 0, 9, 0, 15, 0],
    [13, 0, 16, 9, 7, 11, 4, 6, 0, 0, 0, 10, 3, 0, 2, 0],
    [0, 11, 0, 0, 13, 15, 0, 0, 0, 12, 0, 0, 5, 0, 1, 10],
    [5, 14, 0, 0, 3, 12, 2, 8, 13, 15, 16, 0, 7, 11, 0, 0],
    [3, 0, 2, 0, 5, 14, 1, 0, 7, 0, 4, 6, 13, 15, 16, 0],
    [0, 0, 9, 16, 11, 0, 0, 4, 14, 5, 10, 0, 0, 3, 8, 0],
    [0, 0, 6, 0, 15, 13, 9, 0, 0, 3, 0, 2, 0, 5, 10, 1],
    [14, 5, 10, 0, 0, 3, 8, 0, 15, 0, 0, 16, 11, 7, 6, 0],
    [12, 3, 8, 0, 14, 5, 10, 1, 11, 0, 6, 4, 0, 13, 9, 16]
]


initial_grid_16x16_toomany = [
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]


#extra 6 top left
initial_grid_16x16_none = [
    [ 6,  0,  0,  0,  0,  6,  0,  0,  0, 15,  0,  0,  0,  0,  0,  0],
    [ 0,  0,  0,  4,  0,  0,  0, 14,  0,  0,  0,  0,  0,  0,  0,  0],
    [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
    [ 0,  0,  0,  0,  0,  0,  4,  0, 13,  0,  0,  0,  0,  0,  0,  0],
    [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
    [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
    [ 0,  0,  3,  0,  0,  0,  0,  0,  0,  0,  0,  6,  0,  0,  0,  0],
    [ 0,  0,  0,  0,  0,  0,  0,  0,  5,  0,  0,  0,  0,  0,  0,  0],
    [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
    [ 0,  0,  0,  0,  2,  0,  0,  0,  0,  0,  0,  0,  0,  3,  0,  0],
    [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  6,  0],
    [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
    [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  4,  0,  0,  0,  0,  0,  0],
    [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
    [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
    [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  6,  0,  0,  0,  0,  0,  0]
]




def main():
    choice = input("Choose to either enter data (A) or solve existing puzzle (B).")
    # Initialize the SudokuSolver with a 9x9 grid
    if choice == "B":
        optionb()
    
    if choice == "A":
        size = int(input("Size:"))
        initial_grid = [ [ 0 for i in range(size) ] for j in range(size) ]
        def enter():
            solver = SudokuSolver(size)
            flag = False
            while flag == False:
                col = input(f"Pick column 1-{size}")
                row = input(f"Pick row 1-{size}")
                digit = input("Enter Digit")
                if not row.isdigit()or not col.isdigit()or not digit.isdigit():
                    print("Enter Integers please")
                    enter()
                if int(col)-1 >= size or int(row)-1 >= size or int(digit) > size or int(col)-1 < 0 or int(row)-1 < 0 or int(digit) < 0:
                    print("Out of range")
                    enter()
                col=int(col)-1
                row=int(row)-1
                initial_grid[row][col] = digit
                cont = input("Continue Y/N")
                print (initial_grid)
                if cont == "Y":
                    enter()
                if cont == "N":
                    flag = True
                    solver.grid = initial_grid
                    # Solve the puzzle
                    if solver.solve():
                        print("Solved Sudoku:")
                        solver.print_grid()
                    else:
                        print("No solution exists for the given Sudoku.")
                        main()
        enter()

