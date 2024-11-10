import sqlite3

conn = sqlite3.connect("./spam_messages.db")
cursor = conn.cursor()

def deleate():
    cursor.execute('''
    delete from messages where text = "" 
''')


deleate()

conn.commit()
conn.close()