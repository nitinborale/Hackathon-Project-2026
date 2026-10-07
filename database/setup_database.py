import sqlite3

# Connect to SQLite database
connection = sqlite3.connect("lunch.db")

# Create cursor
cursor = connection.cursor()

# Create orders table
cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    food_item TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    price REAL NOT NULL,
    total REAL NOT NULL
)
""")

# Save changes
connection.commit()

# Close connection
connection.close()

print("Database created successfully!")