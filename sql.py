import sqlite3

# Create connection to database
with sqlite3.connect('users.db') as connection:
    c = connection.cursor()
    # Create table with usernames and passwords
    c.execute('''DROP TABLE users''')
    c.execute('''CREATE TABLE users(user_id TEXT, password TEXT)''')
    c.execute('INSERT INTO users VALUES("admin", "admin")')
    c.execute('INSERT INTO users VALUES("test", "test")')