import sqlite3
import pandas as pd

# Connect to the SQLite database
conn = sqlite3.connect('spam_messages.db')

# Query to extract data
query = "SELECT id, text, spam_id FROM messages"

# Load data into a pandas DataFrame
df = pd.read_sql_query(query, conn)

# Save the DataFrame to a CSV file
df.to_csv('spam.csv', index=False)

# Close the connection
conn.close()
