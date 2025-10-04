import os
import psycopg2
from flask import Flask, render_template, g

# --- Basic App Setup ---
app = Flask(__name__)

# --- Database Connection Functions ---

def get_db():
    # Get the database connection URL from the environment variable set in Render
    DATABASE_URL = os.environ['DATABASE_URL']
    if 'db' not in g:
        g.db = psycopg2.connect(DATABASE_URL)
    return g.db

@app.teardown_appcontext
def close_connection(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

# --- Routes ---

@app.route('/')
def index():
    conn = get_db()
    cur = conn.cursor()
    # Fetch all articles, ordered by the newest first
    cur.execute('SELECT * FROM articles ORDER BY created_at DESC;')
    articles = cur.fetchall()
    cur.close()
    
    # Convert list of tuples to list of dictionaries for easier template access
    articles_dict = []
    for article in articles:
        articles_dict.append({
            'id': article[0],
            'title': article[1],
            'author': article[2],
            'content': article[3],
            'created_at': article[4]
        })

    return render_template('index.html', articles=articles_dict)

# --- Main Execution ---

if __name__ == '__main__':
    app.run(port=5001, debug=True)
