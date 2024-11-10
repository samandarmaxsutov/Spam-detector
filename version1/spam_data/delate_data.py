import sqlite3

conn = sqlite3.connect("./spam_messages.db")
cursor = conn.cursor()

def update():
    cursor.execute('''
                   update messages set spam_id = 0 where  channel_name = "ACM Uz"
                   ''')

conn.commit()
conn.close()