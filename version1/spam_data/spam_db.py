import os
import sys
import json
import sqlite3

file = "result.json"
db_file = "./spam_messages.db"

# Check if the file exists
if not os.path.exists(file):
    print(f"File '{file}' does not exist.")
    sys.exit(1)

# Read JSON file
with open(file, 'r') as f:
    data = json.load(f)

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

def create():
    # Create table for messages with an auto-incrementing id
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT,
            spam_id INTEGER,
            channel_name TEXT,
            channel_id INTEGER
        )
    ''')



def add(spam_id, data):
    for message in data['messages']:
        if message['type'] == 'message':
            text_content = ""

            # Extract text content
            for part in message['text']:
                if isinstance(part, dict):
                    text_content += part['text'] + " "
                else:
                    text_content += part + " "

            text_content = text_content.strip()  # Remove any trailing whitespace


            # Insert data into the SQLite database
            cursor.execute('''
                INSERT INTO messages (text, spam_id, channel_name , channel_id)
                VALUES (?, ?, ?, ?)
            ''', ( text_content, spam_id,data['name'],data['id']))



def deleate():
    cursor.execute('''
    delete from messages where text = "" 
''')

def update():
    cursor.execute('''
                   update messages set spam_id = 0 where  channel_name = "ACM Uz"
                   ''')
create()
add(spam_id=0, data=data)
deleate()
# update()

conn.commit()
conn.close()

print(f"SQLite database '{db_file}' created and data inserted successfully.")
