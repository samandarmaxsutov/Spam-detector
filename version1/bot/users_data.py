import sqlite3

db_path = "./users_data.db"
# Database Initialization
def initialize_database():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id INTEGER UNIQUE,
        save_message BOOLEAN
    )
    ''')

    # Create user_messages table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT,
        spam BOOLEAN,
        user_id INTEGER,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    ''')
    # Create user_feedbacks table
    cursor.execute('''
       CREATE TABLE IF NOT EXISTS user_feedbacks (
           id INTEGER PRIMARY KEY AUTOINCREMENT,
           user_id INTEGER,
           is_positive BOOLEAN,
           text TEXT,
           FOREIGN KEY(user_id) REFERENCES users(id)
       )
       ''')
    conn.commit()
    conn.close()


# Initialize the database
initialize_database()


# User Class
class User:
    def __init__(self, telegram_id, save_message=False):
        self.telegram_id = telegram_id
        self.save_message = save_message

    def update(self):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET save_message=? WHERE telegram_id=?",
                       (int(self.save_message), self.telegram_id))
        conn.commit()
        conn.close()

    def add_user(self):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute('''
        INSERT OR IGNORE INTO users (telegram_id, save_message)
        VALUES (?, ?)
        ''', (self.telegram_id, self.save_message))

        conn.commit()
        conn.close()

    @staticmethod
    def get_user_by_telegram_id(telegram_id):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM users WHERE telegram_id = ?', (telegram_id,))
        user_data = cursor.fetchone()

        conn.close()

        if user_data:
            return User(telegram_id=user_data[1], save_message=user_data[2])
        return None

    @staticmethod
    def get_all():
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM users')
        users = cursor.fetchall()

        conn.close()
        return users


# UserMessages Class
class UserMessages:
    def __init__(self, text, spam, user_id):
        self.text = text
        self.spam = spam
        self.user_id = user_id

    def add_message(self):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute('''
        INSERT INTO user_messages (text, spam, user_id)
        VALUES (?, ?, ?)
        ''', (self.text, self.spam, self.user_id))

        conn.commit()
        conn.close()

    @staticmethod
    def get_messages_by_user_id(user_id):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM user_messages WHERE user_id = ?', (user_id,))
        messages = cursor.fetchall()

        conn.close()
        return messages


class UserFeedbacks:
    def __init__(self, user_id, is_positive, text):
        self.user_id = user_id
        self.is_positive = is_positive
        self.text = text

    def add_feedback(self):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute('''
        INSERT INTO user_feedbacks (user_id, is_positive,text)
        VALUES (?, ?, ?)
        ''', (self.user_id, self.is_positive,self.text))

        conn.commit()
        conn.close()

    @staticmethod
    def get_feedback_by_user_id(user_id):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM user_feedbacks WHERE user_id = ?', (user_id,))
        feedbacks = cursor.fetchall()

        conn.close()
        return feedbacks


# Example Usage
if __name__ == "__main__":
    print(User.get_all())
    print(UserFeedbacks.get_feedback_by_user_id(5504052371))
# Creating a new user
# new_user = User(telegram_id=123456789, save_message=True)
# new_user.save()
#
# # Saving a message for the user
# user = User.get_user_by_telegram_id(123456789)
# if user:
#     message = UserMessages(text="This is a test message", spam=False, user_id=user.telegram_id)
#     message.save()
#
# # Retrieving messages for a user
# messages = UserMessages.get_messages_by_user_id(user.telegram_id)
# for msg in messages:
#     print(msg)
