import sqlite3

# This script will initialize our database

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

connection.commit()
connection.close()

print("Database 'database.db' initialized successfully.")
