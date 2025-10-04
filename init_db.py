import os
import psycopg2

# This script is now idempotent. It can be run many times without changing the result
# after the first run. It creates the table if it doesn't exist, and only adds
# seed data if the table is empty.

DATABASE_URL = os.environ['DATABASE_URL']

conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

# Create the table if it doesn't exist
with open('schema.sql', 'r') as f:
    cur.execute(f.read())

# Check if the table is empty
cur.execute("SELECT COUNT(id) FROM articles")
# fetchone() returns a tuple, e.g., (0,)
empty = cur.fetchone()[0] == 0

# If it's empty, insert the initial seed data
if empty:
    print("Table 'articles' was empty, inserting initial data.")
    cur.execute(
        "INSERT INTO articles (title, author, content) VALUES (%s, %s, %s)",
        (
            'Welcome to the New Gazette!', 
            'The Editors', 
            'This is the very first article on our new, dynamic website platform. More content to come!'
        )
    )
    cur.execute(
        "INSERT INTO articles (title, author, content) VALUES (%s, %s, %s)",
        (
            'A Guide to the Extended Essay', 
            'Jane Doe', 
            'The Extended Essay can be a daunting task, but with the right approach, it can be a rewarding experience. Here are our top tips for success.'
        )
    )
else:
    print("Table 'articles' already contains data. Skipping initial data insertion.")

# Commit the changes and close the connection
conn.commit()
cur.close()
conn.close()

print("Database initialization check complete.")
