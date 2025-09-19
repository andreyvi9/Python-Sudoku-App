import sqlite3 #Imported to achieve database functionality


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

# Function to make a user an admin
def make_user_admin(username):
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    
    # Check if the user exists
    cursor.execute('''
        SELECT id FROM users
        WHERE username = ?
    ''', (username,))

    user_id = cursor.fetchone()

    if user_id is not None:
        # Update the 'admin' status for the user
        cursor.execute('''
            UPDATE users
            SET admin = 1
            WHERE id = ?
        ''', (user_id[0],))

        conn.commit()
        conn.close()
        return True  # User is now an admin
    else:
        conn.close()
        return False  # User not found

# Example usage to make 'Michael Truong' an admin
username_to_make_admin = 'Michael Truong'
if make_user_admin(username_to_make_admin):
    print(f"{username_to_make_admin} is now an admin.")
else:
    print(f"Failed to make {username_to_make_admin} an admin. User not found.")
