import os
import psycopg2
from flask import Flask, render_template, g, request, redirect, url_for
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

# --- Basic App Setup ---
app = Flask(__name__)
auth = HTTPBasicAuth()

# --- User Authentication ---
# In a real app, you'd store this in a database or a more secure config.
users = {
    "admin": generate_password_hash("password")
}

@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username

# --- Database Connection Functions ---
def get_db():
    DATABASE_URL = os.environ['DATABASE_URL']
    if 'db' not in g:
        g.db = psycopg2.connect(DATABASE_URL)
    return g.db

@app.teardown_appcontext
def close_connection(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

# --- Public Routes ---

@app.route('/')
def index():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM articles ORDER BY created_at DESC;')
    articles = cur.fetchall()
    cur.close()
    
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

# --- Admin Routes ---

@app.route('/admin')
@auth.login_required
def admin():
    return render_template('admin.html')

@app.route('/admin/add', methods=['POST'])
@auth.login_required
def add_article():
    title = request.form['title']
    author = request.form['author']
    content = request.form['content']
    
    conn = get_db()
    cur = conn.cursor()
    # Use parameterized query to prevent SQL injection
    cur.execute(
        'INSERT INTO articles (title, author, content) VALUES (%s, %s, %s)',
        (title, author, content)
    )
    conn.commit()
    cur.close()
    
    return redirect(url_for('index'))

# --- Main Execution ---

if __name__ == '__main__':
    app.run(port=5001, debug=True)