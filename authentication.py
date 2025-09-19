#Handling imports
import sqlite3
import bcrypt
import re

def is_strong_password(password):
    # Checks if the password meets the criteria for being strong
    if len(password) < 8:  # Checks if the password is at least 8 characters long
        return False
    if not re.search("[a-z]", password):  # Checks for at least one lowercase letter
        return False
    if not re.search("[A-Z]", password):  # Checks for at least one uppercase letter
        return False
    if not re.search("[0-9]", password):  # Checks for at least one digit
        return False
    return True  # Returns True if all criteria are met


def create_username_old(username):
    # Creates a new username in the database
    conn = sqlite3.connect('user_data.db')  # Connects to the SQLite database
    cursor = conn.cursor()
    # Checks if the username already exists in the database
    cursor.execute("SELECT username FROM users WHERE username=?", (username,))
    existing_user = cursor.fetchone()
    conn.close()  # Closes the database connection

    if existing_user:
        return "F"  # Returns "F" if the username already exists
    else:
        return username  # Returns the username if it is unique

def create_username(username):
    # Creates a new username in the database
    conn = sqlite3.connect('user_data.db')  # Connects to the SQLite database
    cursor = conn.cursor()

    # Checks if the username already exists in the database
    cursor.execute("SELECT username FROM users WHERE username=?", (username,))
    existing_user = cursor.fetchone()

    if existing_user:
        conn.close()  # Close the database connection if username exists
        return "F"  # Returns "F" if the username already exists
    else:
        # Check if the username contains only letters and a space after the first name
        if re.match("^[A-Za-z]+ [A-Za-z]+$", username):
            conn.close()  # Close the database connection if username is valid
            return username  # Returns the username if it is unique and valid
        else:
            conn.close()  # Close the database connection if username is invalid
            return "F"  # Returns message for an invalid username format


def create_password(password):
    # Creates a hashed password if the provided password is strong
    if is_strong_password(password):  # Checks if the password is strong
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        return hashed_password  # Returns the hashed password
    else:
        return "F"  # Returns "F" if the password is not strong


def create_account(username, password):
    # Creates a new user account in the database
    conn = sqlite3.connect('user_data.db')  # Connects to the SQLite database
    cursor = conn.cursor()
    # Inserts the new username and password into the database
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()  # Commits the transaction
    conn.close()  # Closes the database connection


def login(username, password):
    # Logs in a user by verifying their password
    conn = sqlite3.connect('user_data.db')  # Connects to the SQLite database
    cursor = conn.cursor()
    # Retrieves the hashed password for the given username
    cursor.execute("SELECT password FROM users WHERE username=?", (username,))
    stored_password = cursor.fetchone()
    conn.close()  # Closes the database connection

    if stored_password:
        stored_password = stored_password[0]  # Extracts the hashed password

        # Verifies the provided password against the stored hash
        if bcrypt.checkpw(password.encode('utf-8'), stored_password):
            print("Login successful.")
            return True  # Returns True if the password is correct
        else:
            print("Login failed. Please check your password.")
            return False  # Returns False if the password is incorrect
    else:
        print("Login failed. User does not exist.")
        return False  # Returns False if the username does not exist


print(create_username("hb n]"))
