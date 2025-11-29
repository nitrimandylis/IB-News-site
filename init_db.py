import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

# This script is now idempotent. It can be run many times without changing the result
# after the first run. It creates the table if it doesn't exist, and only adds
# seed data if the table is empty.

DATABASE_URL = os.environ.get('DATABASE_URL')
if not DATABASE_URL:
    print("FATAL: DATABASE_URL environment variable not set.")
    exit(1)
if DATABASE_URL.startswith("https://"):
    DATABASE_URL = DATABASE_URL.replace('https://', 'postgresql://')

conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

# Create the table if it doesn't exist
with open('schema.sql', 'r') as f:
    cur.execute(f.read())

# Idempotently add the 'image_data' column if it doesn't exist
cur.execute("""
    SELECT column_name 
    FROM information_schema.columns 
    WHERE table_name='articles' AND column_name='image_data';
""")
if cur.fetchone() is None:
    print("Column 'image_data' not found in 'articles' table. Adding it now.")
    cur.execute("ALTER TABLE articles ADD COLUMN image_data BYTEA;")
    print("Column 'image_data' added successfully.")
else:
    print("Column 'image_data' already exists in 'articles' table.")

# Commit the changes and close the connection
conn.commit()
cur.close()
conn.close()

print("Database initialization check complete.")

# Commit the changes and close the connection
conn.commit()
cur.close()
conn.close()

print("Database initialization check complete.")