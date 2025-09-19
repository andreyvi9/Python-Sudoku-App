import sqlite3

# Connect to the SQLite database (change 'mydb.db' to your database file)
conn = sqlite3.connect('user_data.db')

# Create a cursor
cursor = conn.cursor()

# Execute a SELECT query
cursor.execute('SELECT * FROM users')

# Fetch all rows
rows = cursor.fetchall()

# Print the data
for row in rows:
    print(row)

# Close the cursor and the database connection
cursor.close()
conn.close()
