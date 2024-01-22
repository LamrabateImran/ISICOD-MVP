# Import necessary PyQt5 modules and other dependencies
import json
import sqlite3

db = sqlite3.connect("local_database.db")
cursor = db.cursor()


def execute_query(query, fetch=False):
    cursor.execute(query)
    if fetch:
        return cursor.fetchall()
    db.commit()


def create_labels_table():
    cursor.execute("CREATE TABLE IF NOT EXISTS labels ( id INT AUTO_INCREMENT PRIMARY KEY, label TEXT, value JSON)")
    db.commit()


def create_users_table():
    # Assuming you have a statement like this in your code
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT, email TEXT);")

    db.commit()


create_users_table()


def fetch_data_from_database():
    cursor.execute("SELECT * FROM labels")
    data = cursor.fetchall()
    labels_data = {label: value for _, label, value in data}
    return labels_data


def add_labels(label, value):
    cursor.execute("SELECT COUNT(*) FROM labels")
    row_count = cursor.fetchone()[0]
    if row_count < 4:
        json_value = json.dumps(value)
        cursor.execute("INSERT INTO labels (label, value) VALUES (?, ?)", (label, json_value))
        db.commit()


def add_users(email_, password_):
    cursor.execute("SELECT COUNT(*) FROM users")
    row_count = cursor.fetchone()[0]
    db.commit()
    print(row_count)
    if row_count == 0:
        cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email_, password_))
        db.commit()


create_labels_table()

add_users('imran', 'qqqq')

add_labels('Step 1', {
     '1': 'Extracted first row, first Value in Label table',
     '2': 'Extracted first row, second Value in Label table'})

add_labels('Step 2', {
     '1': 'Extracted second row, first Value in Label table',
     '2': 'Extracted second row, second Value in Label table'})

add_labels('Step 3', {
     '1': 'Extracted third row, first Value in Label table',
     '2': 'Extracted third row, second Value in Label table'})


