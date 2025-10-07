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
        "INSERT INTO articles (title, author, content, image_url) VALUES (%s, %s, %s, %s)",
        (
            'Welcome to the New Gazette!', 
            'The Editors', 
            'This is the very first article on our new, dynamic website platform. More content to come!',
            'https://images.unsplash.com/photo-1585241936939-be4099591252?q=80&w=3540&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'
        )
    )
    cur.execute(
        "INSERT INTO articles (title, author, content, image_url) VALUES (%s, %s, %s, %s)",
        (
            'A Guide to the Extended Essay', 
            'Jane Doe', 
            'The Extended Essay can be a daunting task, but with the right approach, it can be a rewarding experience. Here are our top tips for success.',
            'https://images.unsplash.com/photo-1456406644174-8ddd4cd52a06?q=80&w=3540&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'
        )
    )
else:
    print("Table 'articles' already contains data. Skipping initial data insertion.")

# Commit the changes and close the connection
conn.commit()
cur.close()
conn.close()

print("Database initialization check complete.")
