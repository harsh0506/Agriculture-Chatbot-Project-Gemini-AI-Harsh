import sqlite3
from datetime import datetime

# Function to create a SQLite database table
def create_table():
    conn = sqlite3.connect('qa_database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS qa_records
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 question TEXT,
                 answer TEXT,
                 user_id TEXT,
                 timestamp DATETIME,
                 image_url TEXT,
                 from_lang TEXT,
                 to_lang TEXT)''')
    conn.commit()
    conn.close()

# Function to retrieve the last 4 records of a given user ID based on timestamp
def retrieve_last_4_records(user_id):
    conn = sqlite3.connect('qa_database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM qa_records WHERE user_id=? ORDER BY timestamp DESC LIMIT 4", (user_id,))
    all_rec = c.fetchall()
    
    records = []
    
    for row in all_rec: 
        
        record = {
                "question": row[1],
                "answer": f"<Answer>: {row[2]}",
                "user_id": row[3],
                "timestamp": row[4]
            }
        records.append(record)
    
    return records


# Function to retrieve all users
def retrieve_all_users():
    conn = sqlite3.connect('qa_database.db')
    c = conn.cursor()
    c.execute('''SELECT DISTINCT user_id FROM qa_records''')
    users = [row[0] for row in c.fetchall()]
    conn.close()
    return users

# Function to retrieve all records for a given user
def retrieve_all_records_for_user(user_id):
    conn = sqlite3.connect('qa_database.db')
    c = conn.cursor()
    c.execute('''SELECT * FROM qa_records WHERE user_id=?''', (user_id,))
    records = []
    for row in c.fetchall():
        record = {
            "question": row[1],
            "answer": f"<Answer>: {row[2]}",
            "user_id": row[3],
            "timestamp": row[4].strftime("%Y-%m-%d %H:%M:%S"),
            "image_url": row[5],
            "from_lang": row[6],
            "to_lang": row[7]
        }
        records.append(record)
    conn.close()
    return records

# Function to add a new record to the table
def add_record(question, answer, user_id, image_url=None, from_lang=None, to_lang=None):
    timestamp = datetime.now()
    conn = sqlite3.connect('qa_database.db')
    c = conn.cursor()
    c.execute('''INSERT INTO qa_records (question, answer, user_id, timestamp, image_url, from_lang, to_lang)
                 VALUES (?, ?, ?, ?, ?, ?, ?)''', (question, answer, user_id, timestamp, image_url, from_lang, to_lang))
    conn.commit()
    conn.close()

# Function to handle errors
def handle_errors(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return {"error": str(e)}
    return wrapper


'''
# Decorate functions with error handling
retrieve_last_4_records = handle_errors(retrieve_last_4_records)
retrieve_all_users = handle_errors(retrieve_all_users)
retrieve_all_records_for_user = handle_errors(retrieve_all_records_for_user)
add_record = handle_errors(add_record)

# Create the table if it doesn't exist
create_table()

'''








