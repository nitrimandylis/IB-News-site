import os
import psycopg2

# Get the database connection URL from the environment variable
DATABASE_URL = os.environ['DATABASE_URL']

# Connect to the database
conn = psycopg2.connect(DATABASE_URL)

# Open a cursor to perform database operations
cur = conn.cursor()

# Execute the schema.sql file to create the tables and insert data
with open('schema.sql', 'r') as f:
    cur.execute(f.read())

# Make the changes to the database persistent
conn.commit()

# Close the cursor and connection
cur.close()
conn.close()

print("Database initialized successfully using PostgreSQL.")