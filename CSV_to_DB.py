import sqlite3
import pandas as pd

# Paths
DB_PATH = '/Users/emmet/Documents/PythonLX/Website/LXDatabase.db'  # SQLite database file
CSV_PATH = '/Users/emmet/Desktop/allfixtures.csv'  # Path to your CSV file
TABLE_NAME = 'fixturesv2'  # Name of the table to create

try:
    # Load the CSV file into a pandas DataFrame
    df = pd.read_csv(CSV_PATH)
    print(f"Loaded CSV file with {len(df)} rows and {len(df.columns)} columns.")

    # Connect to the SQLite database
    conn = sqlite3.connect(DB_PATH)
    print(f"Connected to the database at {DB_PATH}")

    # Write the DataFrame to a table
    df.to_sql(TABLE_NAME, conn, index=False, if_exists='replace')
    print(f"Table '{TABLE_NAME}' created and data inserted successfully.")

    # Verify the table creation
    cursor = conn.cursor()
    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Tables in the database:", [table[0] for table in tables])

    # Close the connection
    conn.close()
    print("Database connection closed.")

except Exception as e:
    print(f"Error: {e}")
