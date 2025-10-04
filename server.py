import sqlite3
from flask import Flask, render_template, g

# --- Basic App Setup ---
app = Flask(__name__)
DATABASE = 'database.db'

# --- Database Connection Functions ---
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# --- Routes ---

@app.route('/')
def index():
    db = get_db()
    # Fetch all articles, ordered by the newest first
    articles = db.execute('SELECT * FROM articles ORDER BY created_at DESC').fetchall()
    # Pass the articles to the template
    return render_template('index.html', articles=articles)

# --- Main Execution ---

if __name__ == '__main__':
    app.run(port=5001, debug=True)