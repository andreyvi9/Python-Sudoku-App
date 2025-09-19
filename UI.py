#Handling Tkinter imports
import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
from tkinter import messagebox

#Handling other library imports
from PIL import Image, ImageTk #Imported to achieve button image functionality
import sqlite3 #Imported to achieve database functionality
import bcrypt #Imported to achieve encryption functionality
import re #Imported to achieve password testing functionality
import os #Imported to achieve file finding functionality
import time #Imported to track time taken to complete puzzles
from datetime import date

#Handling imports from my other components
from datarep import create_graph
from generationfinal import SudokuGenerator, display_sudoku, save_to_text_file
from loginfinal import is_strong_password, create_username, create_password, create_account, login
from solving3 import SudokuSolver
from sharingnew import share, save
from c import is_safe, solve_sudoku, count_solutions, solve_comp

#Function to add the CSGS logo to all relevant screens
def logo_add(new_window):
    #Adding CSGS logo
    imageMain = Image.open("csgs-logo.jpg")
    photoMain = ImageTk.PhotoImage(imageMain)
    logoMain = tk.Label(new_window, image=photoMain)
    logoMain.image = photoMain  # Keep a reference to the PhotoImage
    logoMain.place(x=900, y=0)
    
def button_click_sign():
    def back():
        new_window.destroy() #Closes new window
        root.deiconify() #Reopens the main window

    def get_input_username(entry, label, label_text):
        user_input = entry.get()#tests inputs
        print(user_input)
        label.config(text=f"{label_text}: {user_input}")

    def get_input_password(entry, label, label_text):
        user_input = entry.get()#tests inputs
        print(user_input)
        label.config(text=f"{label_text}: {user_input}")

    def create_user():
        global current_username
        username_input = username.get()
        current_username = username_input
        password_input = password.get()

        if create_username(username_input) != "F" and create_password(password_input) != "F":
            create_account(username_input, create_password(password_input))
            result_label.config(text="Account created successfully.")
        else:
            result_label.config(text="Username or password is invalid.")

    new_window = tk.Toplevel(root)
    new_window.title("Sign Up")
    new_window.configure(bg="#47206e")
    new_window.geometry("1100x900")

    logo_add(new_window)
    
    username = tk.Entry(new_window)
    username.pack()
    get_username = tk.Button(new_window, text="Enter Username", command=lambda: get_input_username(username, result_label, "Your username"))
    get_username.pack()

    password = tk.Entry(new_window)
    password.pack()
    get_password = tk.Button(new_window, text="Enter Password", command=lambda: get_input_password(password, result_label, "Your password"))
    get_password.pack()

    create_button = tk.Button(new_window, text="Create Account", command=create_user)
    create_button.pack()

    result_label = tk.Label(new_window, text="")
    result_label.pack()

    new_button = tk.Button(new_window, text="Back", command=back)
    new_button.pack()

    root.withdraw()  # Hide the main window

def button_click_log():
    def back():
        new_window.destroy()
        root.deiconify()

    def get_input(entry, label, label_text):
        user_input = entry.get()
        label.config(text=f"{label_text}: {user_input}")

    def perform_login():
        global current_username
        username_input = username.get()
        current_username = username_input
        password_input = password.get()
        login(username_input, password_input)
        if login(username_input, password_input)== True:
            enterButton.place(x=475, y=725)

    new_window = tk.Toplevel(root)
    new_window.title("Log In")
    new_window.configure(bg="#47206e")
    new_window.geometry("1100x900")
    
    logo_add(new_window)

    username = tk.Entry(new_window)
    username.pack()
    get_username = tk.Button(new_window, text="Enter Username", command=lambda: get_input(username, result_label, "Your username"))
    get_username.pack()

    password = tk.Entry(new_window)
    password.pack()
    get_password = tk.Button(new_window, text="Enter Password", command=lambda: get_input(password, result_label, "Your password"))
    get_password.pack()

    login_button = tk.Button(new_window, text="Login", command=perform_login)
    login_button.pack()

    result_label = tk.Label(new_window, text="")
    result_label.pack()

    new_button = tk.Button(new_window, text="Back", command=back)
    new_button.pack()

    root.withdraw()

def button_click_enter():
    #Following functions will open call the relevant procedures based on the user input
    def solve_pressed():
        solving()

    def gen_pressed():
        generation()

    def comp_pressed():
        completion()

    def hist_pressed():
        data_representation()

    def share_pressed():
        sharing()

    def settings_pressed():
        settings()

    #Here will be the user's unique result database
    global db_name    
    db_name = current_username + '.db'

    connection = sqlite3.connect(db_name)

    cursor = connection.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS puzzle_results 
                  (difficulty TEXT, date DATE, time_taken INTEGER)''')

    # Commit the changes and close the cursor and connection
    connection.commit()
    cursor.close()
    connection.close()

    admin_state = is_user_admin(current_username)
    
    
    #Making new window
    new_window = tk.Toplevel(root)
    new_window.title("Main Menu")
    new_window.configure(bg="#47206e")
    new_window.geometry("1100x900")
    
    #Making main buttons
    buttonSolve = tk.Button(new_window, text="Solve", command=solve_pressed, bg="yellow", font=("",32), padx=1, pady=1)
    buttonGenerate = tk.Button(new_window, text="Generate", command=gen_pressed, bg="yellow", font=("",32), padx=1, pady=1)
    buttonComplete = tk.Button(new_window, text="Complete", command=comp_pressed, bg="yellow", font=("",32), padx=1, pady=1)
    
    #Making message, split into 2 such that presented nicely
    wlc_msg = tk.Label(new_window, text="Welcome to Chronicle Sudoku", bg="#47206e", fg="yellow", font=("",32))
    wlc_msg2 = tk.Label(new_window, text="Application", bg="#47206e", fg="yellow", font=("",32))
    
    #Adding CSGS logo
    logo_add(new_window)


    if admin_state == True:
        #Adding settings image
        imageMainCog = Image.open("cog.png")
        photoMainCog = ImageTk.PhotoImage(imageMainCog)
        cogMain = tk.Label(new_window, image=photoMainCog)
        cogMain.image = photoMainCog  # Keep a reference to the PhotoImage
        cogMain.place(x=850, y=600)
        buttonSettings = tk.Button(new_window, image=photoMainCog, command=settings_pressed)
        buttonSettings.place(x=850, y=600)
    
    #Adding history image
    imageMainHist = Image.open("history.png")
    photoMainHist = ImageTk.PhotoImage(imageMainHist)
    histMain = tk.Label(new_window, image=photoMainHist)
    histMain.image = photoMainHist  # Keep a reference to the PhotoImage
    
    #Adding share image
    imageMainShareIcon = Image.open("share_icon.png")
    photoMainShareIcon = ImageTk.PhotoImage(imageMainShareIcon)
    shareIconMain = tk.Label(new_window, image=photoMainShareIcon)
    shareIconMain.image = photoMainShareIcon  # Keep a reference to the PhotoImage
    
    #Making the image buttons
    buttonHist = tk.Button(new_window, image=photoMainHist, command=hist_pressed)
    buttonHist.place(x=50, y=200)
    buttonShare = tk.Button(new_window, image=photoMainShareIcon, command=share_pressed)
    buttonShare.place(x=50, y=600)
    
    
    #Placing widgets
    wlc_msg.place(x=250, y=50)
    wlc_msg2.place(x=440, y=100)
    buttonSolve.place(x=480, y=180)
    buttonGenerate.place(x=445, y=280), buttonComplete.place(x=442, y=380)
    
    #Hiding Log-in screen
    root.withdraw()

# Create or connect to the SQLite database (this will create a new file named 'user_data.db' if it doesn't exist)
conn = sqlite3.connect('user_data.db')
cursor = conn.cursor()

# Create a table to store user details
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        admin INTEGER DEFAULT 0 -- 0 for non-admin, 1 for admin
    )
''')
# Commit changes and close the database connection
conn.commit()
conn.close()

# Statement to check if a given user is an admin
def is_user_admin(username):
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT admin FROM users
        WHERE username = ?
    ''', (username,))

    result = cursor.fetchone()

    conn.commit()
    conn.close()
    
    if result is not None:
        return bool(result[0])  # Convert the value to a boolean
    else:
        return False  # User not found

# Example usage
username_to_check = 'Michael Truong'
if is_user_admin(username_to_check):
    print(f"{username_to_check} is an admin.")
else:
    print(f"{username_to_check} is not an admin.")

#Making the initial window
root = tk.Tk()
root.title("CSGS Sudoku App")
# Set the background color of the main window to correct shade of purple
root.configure(bg="#47206e")
root.geometry("1100x900")
#Title and button widgets
name = tk.Label(root, text="Chronicle Sudoku", bg="#47206e", fg="#85e346", font=("",32))
buttonSign = tk.Button(root, text="Sign Up", command=button_click_sign, bg="yellow", font=("",32), padx=1, pady=1)
buttonLog = tk.Button(root, text="Log In", command=button_click_log, bg="yellow", font=("",32), padx=1, pady=1)
#Logo image widget
image1 = Image.open("csgs-logo.jpg")
photo1 = ImageTk.PhotoImage(image1)
logo = tk.Label(root, image=photo1)
#Puzzle image widget
image2 = Image.open("puz.png")
photo2 = ImageTk.PhotoImage(image2)
puz = tk.Label(root, image=photo2)
#Making the enter button
enterButton = tk.Button(root, text="Enter", command=button_click_enter, bg="yellow", font=("",32), padx=1, pady=1)
#Placing everything
name.place(x=400, y=50)
buttonSign.place(x=455, y=450)
buttonLog.place(x=475, y=550)
logo.place(x=900, y=0)
puz.place(x=400, y=140)
enterButton.place_forget() #Keeps enter button hidden until successful login



################################################################################################################################################################################################
######## HERE BEGIN THE FUNCTIONS THAT WILL GOVERN WHAT HAPPENS WHEN ON THE MAIN MENU###########################################################################################################
######## HERE BEGIN THE FUNCTIONS THAT WILL GOVERN WHAT HAPPENS WHEN ON THE MAIN MENU###########################################################################################################
################################################################################################################################################################################################
################################################################################################################################################################################################
def get_all_usernames():
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT username FROM users
    ''')
    usernames = [row[0] for row in cursor.fetchall()]
    conn.close()
    return usernames

def settings():
    def back():
        new_window.destroy()

    # Create window
    new_window = tk.Toplevel(root)
    new_window.title("Settings")
    new_window.configure(bg="#47206e")
    new_window.geometry("1100x900")
    logo_add(new_window)

    # Create and populate the GUI components
    frame = ttk.Frame(new_window)
    frame.pack(padx=10, pady=10)


    # Fetch all usernames
    all_usernames = get_all_usernames()
    
    # Difficulty selection
    ttk.Label(frame, text="Select Difficulty:").grid(row=0, column=0)
    difficulty_combobox = ttk.Combobox(frame, values=["Beginner","Easy", "Medium", "Hard", "Expert"])
    difficulty_combobox.grid(row=0, column=1)
    difficulty_combobox.set("Easy")

    ttk.Label(frame, text="Select User:").grid(row=1, column=0)
    user_combobox = ttk.Combobox(frame, values=all_usernames)
    user_combobox.grid(row=1, column=1)
    user_combobox.set("")

    # Graph type selection
    ttk.Label(frame, text="Select Graph Type:").grid(row=2, column=0)
    graph_type = tk.StringVar()
    graph_type.set("Bar Graph")
    bar_radio = ttk.Radiobutton(frame, text="Bar Graph", variable=graph_type, value="Bar Graph")
    line_radio = ttk.Radiobutton(frame, text="Line Graph", variable=graph_type, value="Line Graph")
    bar_radio.grid(row=2, column=1)
    line_radio.grid(row=2, column=2)

    
    # Create graph button
    def create_graph_button():
        new_db = user_combobox.get()+'.db'
        print(new_db)
        selected_difficulty = difficulty_combobox.get()
        selected_graph_type = graph_type.get()
        create_graph(selected_difficulty, selected_graph_type, new_db)

    create_button = ttk.Button(frame, text="Create Graph", command=create_graph_button)
    create_button.grid(row=3, column=0, columnspan=3)

    new_button = tk.Button(new_window, text="Back", command=back, bg="yellow", font=32, padx=1, pady=1)
    new_button.place(x=50, y=650)

            
def data_representation(): #Making new function to avoid nesting too many functions
    def back():
        new_window.destroy()

    # Create window
    new_window = tk.Toplevel(root)
    new_window.title("Puzzle Results Graph")
    new_window.configure(bg="#47206e")
    new_window.geometry("1100x900")

    logo_add(new_window)
    
    # Create and populate the GUI components
    frame = ttk.Frame(new_window)
    frame.pack(padx=10, pady=10)

    # Difficulty selection
    ttk.Label(frame, text="Select Difficulty:").grid(row=0, column=0)
    difficulty_combobox = ttk.Combobox(frame, values=["Beginner","Easy", "Medium", "Hard", "Expert"])
    difficulty_combobox.grid(row=0, column=1)
    difficulty_combobox.set("Easy")

    # Graph type selection
    ttk.Label(frame, text="Select Graph Type:").grid(row=1, column=0)
    graph_type = tk.StringVar()
    graph_type.set("Bar Graph")
    bar_radio = ttk.Radiobutton(frame, text="Bar Graph", variable=graph_type, value="Bar Graph")
    line_radio = ttk.Radiobutton(frame, text="Line Graph", variable=graph_type, value="Line Graph")
    bar_radio.grid(row=1, column=1)
    line_radio.grid(row=1, column=2)

    # Create graph button
    def create_graph_button():
        selected_difficulty = difficulty_combobox.get()
        selected_graph_type = graph_type.get()
        print(db_name)
        create_graph(selected_difficulty, selected_graph_type, db_name)

    create_button = ttk.Button(frame, text="Create Graph", command=create_graph_button)
    create_button.grid(row=2, column=0, columnspan=3)

    new_button = tk.Button(new_window, text="Back", command=back, bg="yellow", font=32, padx=1, pady=1)
    new_button.place(x=50, y=650)

def sharing():
    def back():
        new_window.destroy()
        
    def perform_share():
        def back():
            share_window.destroy()
            
        share_window = tk.Toplevel(root)
        share_window.title("Sharing")
        share_window.configure(bg="#47206e")
        share_window.geometry("1100x900")
        logo_add(share_window)

        # Share and puzzle variables
        app_var = tk.StringVar()
        puzzle_var = tk.StringVar()
        app_var.set("Outlook")  # Default app
        puzzle_var.set("")  # Default puzzle

        # Getting directory of my puzzles
        directory = 'C:\\Users\\User\\AppData\\Local\\Programs\\Python\\Python311\\sudoku'

        # Create an empty list to store the filenames
        text_files = []

        # List all files in the directory and add text files to the list
        for filename in os.listdir(directory):
            if filename.endswith(".txt"):
                text_files.append(filename)

        # Share drop-down
        app_label = ttk.Label(share_window, text='Select App:', font=16, background="#47206e", foreground="yellow")
        app_label.pack(pady=10)
        app_choices = ["Outlook", "Gmail"]
        app_dropdown = ttk.Combobox(share_window, textvariable=app_var, values=app_choices)
        app_dropdown.pack()

        # Puzzle drop-down
        puzzle_label = ttk.Label(share_window, text='Select Puzzle:', font=('Helvetica', 16), background="#47206e", foreground="yellow")
        puzzle_label.pack(pady=10)
        puzzle_choices = text_files
        puzzle_dropdown = ttk.Combobox(share_window, textvariable=puzzle_var, values=puzzle_choices)
        puzzle_dropdown.pack()

        # Share button
        def share_puzzle():
            app_choice = app_var.get()
            puzzle_choice = puzzle_var.get()
            share(app_choice,puzzle_choice)
            
        share_button = tk.Button(share_window, text='Share', command=share_puzzle, bg="yellow")
        share_button.pack(pady=20)

        back_button = tk.Button(share_window, text="Back", command=back, bg="yellow", font=32, padx=1, pady=1)
        back_button.place(x=50, y=650)

    def perform_import():
        def back():
            import_window.destroy()
            
        import_window = tk.Toplevel(root)
        import_window.title("Import")
        import_window.configure(bg="#47206e")
        import_window.geometry("1100x900")
        logo_add(import_window)

        def get_input(entry, label, label_text):
            user_input = entry.get()
            label.config(text=f"{label_text}: {user_input}")
            
        #Creating the entry box for which the user can enter the puzzle they want to import from an email    
        import_box = tk.Entry(import_window, bg="yellow")
        import_box.pack()

        #Button to retrieve the puzzle
        get_puzzle = tk.Button(import_window, text="Paste Puzzle", command=lambda: get_input(import_box, result_label, "Your Puzzle"), bg="yellow")
        get_puzzle.pack()

        #Label to display input
        result_label = tk.Label(import_window, text="", bg="yellow")
        result_label.pack()

        save_puzzle_button = tk.Button(import_window, text="Save To File", command=lambda: save(import_box.get()), bg="yellow")
        save_puzzle_button.pack()

        back_button = tk.Button(import_window, text="Back", command=back, bg="yellow", font=32, padx=1, pady=1)
        back_button.place(x=50, y=650)
        
    # Create overarching window
    new_window = tk.Toplevel(root)
    new_window.title("Sharing")
    new_window.configure(bg="#47206e")
    new_window.geometry("1100x900")

    logo_add(new_window)

    share_puzzle_button = tk.Button(new_window, text="Share", command=perform_share, bg="yellow", font=("",32), padx=1, pady=1)
    share_puzzle_button.pack()

    import_puzzle_button = tk.Button(new_window, text="Import", command=perform_import, bg="yellow", font=("",32), padx=1, pady=1)
    import_puzzle_button.pack()

    back_button = tk.Button(new_window, text="Back", command=back, bg="yellow", font=("",32), padx=1, pady=1)
    back_button.place(x=50, y=650)
    
def solving():
    def back():
        choose_size_window.destroy()
        
    def solve_puzzle(input_grid):  # Updated to accept input_grid
        solver = SudokuSolver(int(size_var.get()))
        solver.solve(input_grid)  # Pass input_grid to the solve method

        if solver.count_solutions() == 1:  # Check for unique solution
            for i in range(solver.size):
                for j in range(solver.size):
                    entries[i][j].delete(0, tk.END)
                    entries[i][j].insert(tk.END, str(solver.grid[i][j]))
        else:
            messagebox.showinfo("Result", "No unique solution found for this Sudoku puzzle.")

    def reset_grid():
        for i in range(solver.size):
            for j in range(solver.size):
                entries[i][j].delete(0, tk.END)
                
    choose_size_window = tk.Toplevel(root)
    choose_size_window.title("Solving")
    choose_size_window.configure(bg="#47206e")
    choose_size_window.geometry("1100x900")

    logo_add(choose_size_window)

    size_var = tk.StringVar()
    size_var.set("9")  # Default size

    # Solve drop-down
    size_label = ttk.Label(choose_size_window, text='Select Size:', font=('Helvetica', 16), background="#47206e", foreground="yellow")
    size_label.pack(pady=10)
    size_choices = ["4", "9", "16"]
    size_dropdown = ttk.Combobox(choose_size_window, textvariable=size_var, values=size_choices)
    size_dropdown.pack()

    def solve_window():
        def back():
            new_window.destroy()
        # Create main application window
        new_window = tk.Toplevel(root)
        new_window.title("Solving")
        new_window.configure(bg="#47206e")
        new_window.geometry("1100x900")
        logo_add(new_window)
        
        solve_size = int(size_var.get())
        global solver
        global entries
        solver = SudokuSolver(solve_size)
        entries = [[tk.Entry(new_window, width=2, font=('Arial', 14)) for j in range(solver.size)] for i in range(solver.size)]

        for i in range(solver.size):
            for j in range(solver.size):
                entries[i][j].grid(row=i, column=j, padx=5, pady=5)

        solve_button = tk.Button(new_window, bg="yellow", text="Solve", command=lambda: solve_puzzle(get_input_grid()))  # Pass input grid
        solve_button.grid(row=solver.size, column=0, columnspan=solver.size // 2)

        reset_button = tk.Button(new_window, text="Reset Grid", command=reset_grid, bg="yellow")
        reset_button.grid(row=solver.size, column=solver.size // 2, columnspan=solver.size // 2)

        new_button = tk.Button(new_window, text="Back", command=back, bg="yellow", font=("",32), padx=1, pady=1)
        new_button.place(x=50, y=650)

    def get_input_grid():  # Helper function to get input grid
        input_grid = []
        for i in range(solver.size):
            row = []
            for j in range(solver.size):
                try:
                    value = int(entries[i][j].get())
                    if value not in range(1, solver.size + 1):
                        raise ValueError
                    row.append(value)
                except ValueError:
                    row.append(0)
            input_grid.append(row)
        return input_grid
    
    size_btn = tk.Button(choose_size_window, text='Select Size', command=int(size_var.get()), bg="yellow")
    size_btn.pack(pady=20)

    solve_btn = tk.Button(choose_size_window, text='Solve', command=solve_window, bg="yellow")
    solve_btn.pack(pady=20)

    new_button = tk.Button(choose_size_window, text="Back", command=back, bg="yellow", font=("",32), padx=1, pady=1)
    new_button.place(x=50, y=650)

def generation():
    def back():
        new_window.destroy()
        
    new_window = tk.Toplevel(root)
    new_window.title("Generation")
    new_window.configure(bg="#47206e")
    new_window.geometry("1100x900")

    logo_add(new_window)

    # Difficulty and Size variables
    difficulty_var = tk.StringVar()
    size_var = tk.StringVar()
    difficulty_var.set("Easy")  # Default difficulty
    size_var.set("9")  # Default size

    # Difficulty drop-down
    difficulty_label = ttk.Label(new_window, text='Select Difficulty:', font=('Helvetica', 16), background="#47206e", foreground="yellow")
    difficulty_label.pack(pady=10)
    difficulty_choices = ["Beginner", "Easy", "Moderate", "Hard", "Expert"]
    difficulty_dropdown = ttk.Combobox(new_window, textvariable=difficulty_var, values=difficulty_choices)
    difficulty_dropdown.pack()

    # Size drop-down
    size_label = ttk.Label(new_window, text='Select Size:', font=('Helvetica', 16), background="#47206e", foreground="yellow")
    size_label.pack(pady=10)
    size_choices = ["4", "9", "16"]
    size_dropdown = ttk.Combobox(new_window, textvariable=size_var, values=size_choices)
    size_dropdown.pack()

    # Generate button
    def generate_puzzle():
        size_choice = int(size_var.get())
        difficulty_choice = difficulty_var.get()

        sudoku_generator = SudokuGenerator(size_choice)
        sudoku_grid = sudoku_generator.generate_sudoku(difficulty_choice)
        display_str = display_sudoku(sudoku_grid)

        generated_puzzle_label.config(text="\nGenerated Sudoku Puzzle:\n" + display_str)

    generate_btn = tk.Button(new_window, text='Generate', command=generate_puzzle, bg="yellow")
    generate_btn.pack(pady=20)

    # Generated puzzle label
    generated_puzzle_label = tk.Label(new_window, foreground="white", text="", font=('Courier', 14), background="#47206e")
    generated_puzzle_label.pack(pady=20)

    # Save button
    def save_puzzle():
        size_choice = int(size_var.get())
        difficulty_choice = difficulty_var.get()

        sudoku_generator = SudokuGenerator(size_choice)
        sudoku_grid = sudoku_generator.generate_sudoku(difficulty_choice)
        filename = f"sudoku_{size_choice}x{size_choice}_{difficulty_choice}.txt"
        save_to_text_file(sudoku_grid, filename)
        print(f"Sudoku puzzle has been saved to '{filename}'.")

    save_btn = tk.Button(new_window, text='Save Puzzle', command=save_puzzle, bg="yellow")
    save_btn.pack(pady=20)

    new_button = tk.Button(new_window, text="Back", command=back, bg="yellow", font=("",32), padx=1, pady=1)
    new_button.place(x=50, y=650)

def completion():
    
    def back():
        new_window.destroy()

    def start():
        def back():
            complete_window.destroy()
            
        def read_grid_from_file(filename):
            with open(filename, 'r') as file:
                lines = file.readlines()

            # Extract numbers from lines and create a 2D list
            grid = [[int(num) if num.isdigit() else 0 for num in line.split()] for line in lines]
            
            return grid

        def fill_entries_from_grid(entries, grid):
            for i in range(len(grid)):
                for j in range(len(grid[i])):
                    if grid[i][j] != 0:
                        entries[i][j].insert(0, str(grid[i][j]))


        
        selected_puzzle = puzzle_var.get()
        print("Selected Puzzle:", selected_puzzle)  # Making sure puzzle is selected
        
        # Record the start time
        start_time = time.time()

        parts = selected_puzzle.split('_')

        # Access the second element
        sub_string = parts[1]

        # Use a loop to extract digits until a non-digit character is encountered
        desired_number = ''
        for char in sub_string:
            if char.isdigit():
                desired_number += char
            else:
                break

        diff = parts[2][:-4]
        diff = diff.capitalize()
        size = int(desired_number)
        
        hints = 0
        
        complete_window = tk.Toplevel(root)        
        complete_window.title("Complete Puzzle")
        complete_window.configure(bg="#47206e")
        complete_window.geometry("1100x900")
        logo_add(complete_window)
        
        entries = [[tk.Entry(complete_window, width=2, font=('Arial', 14)) for j in range(size)] for i in range(size)]


        for i in range(size):
            for j in range(size):
                entries[i][j].grid(row=i, column=j, padx=5, pady=5)


        # Read the grid from the file
        grid = read_grid_from_file(selected_puzzle)

        # Fill the grid with the values from the file
        fill_entries_from_grid(entries, grid)

        solved = solve_comp(read_grid_from_file(selected_puzzle))
        print(solved)
        
        def check_solution():
            nonlocal incorrect_guesses
            user_grid = [[int(entry.get()) if entry.get().isdigit() else 0 for entry in row] for row in entries]
            
            flag = False
            
            # Check for incorrect entries
            for i in range(size):
                for j in range(size):
                    if user_grid[i][j] > size or user_grid[i][j] < 0:
                        messagebox.showinfo("Error", "Enter a number within the correct range")
                        flag = True
                        
                    if user_grid[i][j] != 0 and solved[i][j] != user_grid[i][j] and flag == False:
                        entries[i][j].configure({"background": "red"})
                        incorrect_guesses += 1
                        

                    if user_grid[i][j] != 0 and solved[i][j] == user_grid[i][j] and user_grid[i][j] != grid[i][j]:
                        entries[i][j].configure({"background": "green"})

            if incorrect_guesses >= 3:
                messagebox.showinfo("Game Over", "You've made three incorrect guesses. Better luck next time!")
                complete_window.destroy()
            

        
        incorrect_guesses = 0  # Counter for incorrect guesses


        def hint():
            nonlocal hints_used
            if hints_used >= 3:
                messagebox.showinfo("Sorry", "You've used the maximum amout of hints")
            else:
                    
                user_grid = [
                    [int(entry.get()) if entry.get().isdigit() else 0 if entry.get() != 'h' else 'h' for entry in row]
                    for row in entries
                ]

                for i in range(size):
                    for j in range(size):
                        if user_grid[i][j] == 'h':
                            entries[i][j].configure(background="yellow")
                            entries[i][j].delete(0, "end")  # Clear existing text
                            entries[i][j].insert("end", str(solved[i][j]))
                            hints_used += 1

        hints_used = 0                        

        def end_puzzle():
            user_grid = [[int(entry.get()) if entry.get().isdigit() else 0 for entry in row] for row in entries]
            if user_grid == solved:
                end_time = time.time()
                time_elapsed = end_time - start_time

                # Extract the current date
                current_date = date.today()
                # Connect to the database
                conn = sqlite3.connect(db_name)
                cursor = conn.cursor()
                cursor.execute("INSERT INTO puzzle_results VALUES (?, ?, ?)", (diff, current_date, time_elapsed))

                conn.commit()
                conn.close()

                end_window = tk.Toplevel(root)        
                end_window.title("Congratulations!")
                end_window.configure(bg="#47206e")
                end_window.geometry("1100x900")
                logo_add(end_window)

                diff_str = "Difficulty: " + diff
                time_str = "Time taken: " + str((time_elapsed // 60)) + " minutes " + str(round((time_elapsed % 60),0)) + " seconds"

                congratulations = tk.Label(end_window, text="Congratulations", bg="#47206e", fg="yellow", font=("",32))
                difficulty_message = tk.Label(end_window, text=diff_str, bg="#47206e", fg="yellow", font=("",32))
                time_message = tk.Label(end_window, text=time_str, bg="#47206e", fg="yellow", font=("",32))
                
                congratulations.pack()
                difficulty_message.pack()
                time_message.pack()

                def proceed():
                    end_window.destroy()
                    complete_window.destroy()
                    new_window.destroy()

                proceed_button = tk.Button(end_window, text="Proceed", command=proceed, bg="yellow", font=32, padx=1, pady=1)
                proceed_button.place(x=900, y=650)

        hint_button = tk.Button(complete_window, text="Hint- Enter h into desired cell", command=hint, bg="yellow")
        hint_button.grid(row=size+1, columnspan=size, pady=10)
            
        check_button = tk.Button(complete_window, text="Check", command=check_solution, bg="yellow")
        check_button.grid(row=size, columnspan=size, pady=10)

        submit_button = tk.Button(complete_window, text="Submit", command=end_puzzle, bg="yellow")
        submit_button.grid(row=size+2, columnspan=size, pady=10)

        new_button = tk.Button(complete_window, text="Back", command=back, bg="yellow", font=("",32), padx=1, pady=1)
        new_button.place(x=50, y=650)
        
    new_window = tk.Toplevel(root)
    new_window.title("Select Puzzle")
    new_window.configure(bg="#47206e")
    new_window.geometry("1100x900")

    logo_add(new_window)

    # Getting directory of my puzzles
    directory = 'C:\\Users\\User\\AppData\\Local\\Programs\\Python\\Python311\\sudoku'

    # Create an empty list to store the filenames
    text_files = []

    # List all files in the directory and add text files to the list
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            text_files.append(filename)
            
    puzzle_var = tk.StringVar()
    puzzle_var.set("")  # Default puzzle

    # Puzzle drop-down
    puzzle_label = ttk.Label(new_window, text='Select Puzzle:', font=('Helvetica', 16), background="#47206e", foreground="yellow")
    puzzle_label.pack(pady=10)
    puzzle_choices = text_files
    puzzle_dropdown = ttk.Combobox(new_window, textvariable=puzzle_var, values=puzzle_choices, state="readonly")
    puzzle_dropdown.pack()
    
    store_button = tk.Button(new_window, text="Start!", command=start, bg="yellow")
    store_button.pack(pady=10)

    new_button = tk.Button(new_window, text="Back", command=back, bg="yellow", font=("",32), padx=1, pady=1)
    new_button.place(x=50, y=650)

root.mainloop()
