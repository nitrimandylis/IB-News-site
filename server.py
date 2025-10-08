import os
import psycopg2
from flask import Flask, render_template, g, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

# --- Basic App Setup ---
app = Flask(__name__)
app.secret_key = os.urandom(24)

# --- User Authentication ---
# In a real app, you'd store this in a database or a more secure config.
users = {
    "admin": generate_password_hash("password")
}

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
    cur.execute('SELECT id, title, author, content, image_url, created_at FROM articles ORDER BY created_at DESC;')
    articles = cur.fetchall()
    cur.close()
    
    articles_dict = []
    for article in articles:
        articles_dict.append({
            'id': article[0],
            'title': article[1],
            'author': article[2],
            'content': article[3],
            'image_url': article[4],
            'created_at': article[5]
        })

    return render_template('index.html', articles=articles_dict)

@app.route('/article/<int:article_id>')
def article(article_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT id, title, author, content, image_url, created_at FROM articles WHERE id = %s', (article_id,))
    article_data = cur.fetchone()
    cur.close()

    if article_data is None:
        return "Article not found", 404

    article_dict = {
        'id': article_data[0],
        'title': article_data[1],
        'author': article_data[2],
        'content': article_data[3],
        'image_url': article_data[4],
        'created_at': article_data[5]
    }

    return render_template('article.html', article=article_dict)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

# --- Admin Routes ---

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and check_password_hash(users.get(username), password):
            session['user'] = username
            return redirect(url_for('admin'))
        else:
            return "Invalid credentials", 401
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

@app.route('/admin')
def admin():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('admin.html')

@app.route('/admin/add', methods=['POST'])
def add_article():
    if 'user' not in session:
        return redirect(url_for('login'))
    title = request.form['title']
    author = request.form['author']
    content = request.form['content']
    image_url = request.form['image_url']
    
    conn = get_db()
    cur = conn.cursor()
    # Use parameterized query to prevent SQL injection
    cur.execute(
        'INSERT INTO articles (title, author, content, image_url) VALUES (%s, %s, %s, %s)',
        (title, author, content, image_url)
    )
    conn.commit()
    cur.close()
    
    return redirect(url_for('index'))

# --- Main Execution ---

if __name__ == '__main__':
    app.run(port=5001, debug=True)