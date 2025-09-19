#Handling library imports
import sqlite3 #Imported to achieve database functionality 
import matplotlib.pyplot as plt #Imported to achieve graphing functionality
from datetime import datetime #Imported to ensure date and time are present functionality 

# Function to retrieve data from the database
def fetch_data(difficulty, database):
    # Checks if the difficulty level is valid
    if difficulty in ['Beginner', 'Easy', 'Medium', 'Hard', 'Expert']:
        # Establishes a connection to the SQLite database
        conn = sqlite3.connect(database)
        # Creates a cursor object to interact with the database
        cursor = conn.cursor()
        # Executes a SQL query to select date and time taken for puzzles of the given difficulty
        cursor.execute("SELECT date, time_taken FROM puzzle_results WHERE difficulty=?", (difficulty,))
        # Fetches all rows of the query result
        data = cursor.fetchall()
        # Closes the database connection
        conn.close()

        # Sorts the data by date in ascending order
        data.sort(key=lambda x: datetime.strptime(x[0], "%Y-%m-%d")) 
    
        return data
    else:
        # Returns False if the difficulty level is not valid
        return False


# Function to generate a graph
def create_graph(difficulty, graph_type, db):
    # Fetches data for the specified difficulty
    data = fetch_data(difficulty, db)
    # Checks if data retrieval was unsuccessful
    if data == False:
        return False
    
    # Creates a Bar Graph if specified
    if graph_type == "Bar Graph": 
        plt.figure(figsize=(8, 4))  # Sets the figure size
        plt.bar([d[0] for d in data], [d[1] for d in data])  # Plots a bar graph
        plt.xlabel("Date")  # Sets the x-axis label
        plt.ylabel("Time Taken (seconds)")  # Sets the y-axis label
        plt.title(f"{difficulty} Puzzle Results (Bar Graph)")  # Sets the title of the graph
    
    # Creates a Line Graph if specified
    elif graph_type == "Line Graph":
        plt.figure(figsize=(8, 4))  # Sets the figure size
        plt.plot([d[0] for d in data], [d[1] for d in data], marker='o', linestyle='-')  # Plots a line graph
        plt.xlabel("Date")  # Sets the x-axis label
        plt.ylabel("Time Taken (seconds)")  # Sets the y-axis label
        plt.title(f"{difficulty} Puzzle Results (Line Graph)")  # Sets the title of the graph
    
    else:
        # Returns False if the graph type is not valid and displays an error message
        print("Invalid option")
        return False
    
    plt.xticks(rotation=90, ha='center')  # Rotates x-axis labels for better readability
    plt.show()  # Displays the graph


def main():
    difficulty = input("Select difficulty")
    graph_type = input("Select graph type")
    create_graph(difficulty, graph_type)
    if create_graph(difficulty, graph_type) == False:
        print("Invalid option, try again")
        main()

