import sqlite3
import pandas as pd

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect("Lighting_Database.db")

# Create a cursor to execute SQL commands
cursor = conn.cursor()

# Create the table (if it doesn't already exist)
cursor.execute("""
CREATE TABLE IF NOT EXISTS fixturesv1 (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    manufacturer TEXT NOT NULL,
    fixture TEXT NOT NULL
)
""")

# Data to be inserted
data = [
    ("Robe", "ColorSpot 250 AT")  # Tuple with manufacturer and fixture_name
]

# Insert data into the database
cursor.executemany("""
INSERT INTO fixturesv1 (manufacturer, fixture) 
VALUES (?, ?)
""", data)

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Data inserted successfully!")
