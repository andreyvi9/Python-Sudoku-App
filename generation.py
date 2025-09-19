import random
import copy

class SudokuGenerator:
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


    def remove_cells(self, difficulty):
        # Removes a number of cells from the completed grid based on the difficulty
        target_empty_cells = self.size * self.size  # Sets a base number of empty cells

        # Adjusts the number of empty cells based on difficulty
        if difficulty == "Beginner":
            target_empty_cells = int(target_empty_cells * 0.4)
        # ... similar adjustments for other difficulty levels ...
        elif difficulty == "Easy":
            target_empty_cells = int(target_empty_cells * 0.48)
        elif difficulty == "Moderate":
            target_empty_cells = int(target_empty_cells * 0.55)
        elif difficulty == "Hard":
            target_empty_cells = int(target_empty_cells * 0.63)
        elif difficulty == "Expert":
            target_empty_cells = int(target_empty_cells * 0.7)

        empty_cells = 0
        while empty_cells < target_empty_cells:
            row, col = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
            if self.grid[row][col] != 0:
                original_value = self.grid[row][col]
                self.grid[row][col] = 0

                # Checks if the puzzle still has a unique solution
                solutions = self.count_solutions()
                if solutions != 1:
                    self.grid[row][col] = original_value  # Restores the cell if multiple solutions exist
                else:
                    empty_cells += 1

    def shuffle_numbers(self):
        # Create a list of numbers from 1 to size
        numbers = list(range(1, self.size + 1))

        # Shuffle the numbers randomly
        random.shuffle(numbers)

        # Map the shuffled numbers to the original numbers in the grid
        number_mapping = {i + 1: numbers[i] for i in range(self.size)}

        # Update the grid with shuffled numbers
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j] != 0:
                    self.grid[i][j] = number_mapping[self.grid[i][j]]

    def generate_sudoku(self, difficulty):
        # Generates a new Sudoku puzzle of a given difficulty
        self.solve_sudoku()  # Solves a blank grid to get a complete solution
        self.shuffle_numbers()  # Shuffles numbers to vary the puzzle
        self.remove_cells(difficulty)  # Removes cells according to the difficulty
        return self.grid



def display_sudoku(grid):
    # Displays the Sudoku grid in a readable format
    size = len(grid)
    box_size = int(size ** 0.5)
    max_value_length = len(str(max(max(row) for row in grid)))  # Get the maximum value length

    result = ""
    for i in range(size):
        if i % box_size == 0 and i != 0:
            if box_size == 2:
                result += "----—".ljust(max_value_length + 2) * (size // box_size) + "\n"  # Add 2 to adjust for the extra space
            if box_size == 3:
                result += "-------".ljust(max_value_length + 2) * (size // box_size) + "\n"  # Add 2 to adjust for the extra space
            if box_size == 4:
                result += "------------—".ljust(max_value_length + 2) * (size // box_size) + "\n"  # Add 2 to adjust for the extra space
        for j in range(size):
            if j % box_size == 0 and j != 0:
                result += "| "
            cell_value = grid[i][j]
            cell_str = " " * (max_value_length - len(str(cell_value))) + str(cell_value)
            result += cell_str + " "
        result += "\n"
    print(result)
    return result

def save_to_text_file(grid, filename):
    with open(filename, "w") as file:
        for row in grid:
            file.write(" ".join(str(num) for num in row) + "\n")


if __name__ == "__main__":
    print("Welcome to Sudoku Generator!")
    size_options = [4, 9, 16]
    difficulty_options = ["Beginner", " Easy", "Moderate", "Hard", "Expert"]

    try:
        size_choice = int(input("Choose grid size (4, 9, or 16): "))
        if size_choice not in size_options:
            print("Invalid size choice. Please choose from 4, 9, or 16.")
        else:
            difficulty_choice = input("Choose difficulty level (beginner, easy, moderate, hard, or expert): ")
            if difficulty_choice not in difficulty_options:
                print("Invalid difficulty choice. Please choose from beginner, easy, moderate, hard, or expert.")
            else:
                sudoku_generator = SudokuGenerator(size_choice)
                sudoku_grid = sudoku_generator.generate_sudoku(difficulty_choice)
                print("\nGenerated Sudoku Puzzle:")
                display_sudoku(sudoku_grid)

                filename = f"sudoku_{size_choice}x{size_choice}_{difficulty_choice}.txt"
                save_to_text_file(sudoku_grid, filename)
                print(f"\nSudoku puzzle has been saved to '{filename}'.")

    except ValueError:
        print("Invalid input. Please enter a valid choice.")
