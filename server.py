import os
import psycopg2
from flask import Flask, render_template, g, request, redirect, url_for, session, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv

load_dotenv()

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
    if 'db' not in g:
        try:
            DATABASE_URL = os.environ['DATABASE_URL']
            if DATABASE_URL.startswith("https://"):
                DATABASE_URL = DATABASE_URL.replace('https://', 'postgresql://')
            g.db = psycopg2.connect(DATABASE_URL)
        except psycopg2.OperationalError:
            return None
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
    if conn is None:
        return render_template('index.html', articles=[])
    cur = conn.cursor()
    cur.execute('SELECT id, title, author, content, image_url, created_at, image_data IS NOT NULL FROM articles ORDER BY created_at DESC;')
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
            'created_at': article[5],
            'has_image': article[6]
        })

    return render_template('index.html', articles=articles_dict)

@app.route('/article/<int:article_id>')
def article(article_id):
    conn = get_db()
    if conn is None:
        return "Database not available", 503
    cur = conn.cursor()
    cur.execute('SELECT id, title, author, content, image_url, created_at, image_data IS NOT NULL FROM articles WHERE id = %s', (article_id,))
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
        'created_at': article_data[5],
        'has_image': article_data[6]
    }

    return render_template('article.html', article=article_dict)

@app.route('/image/<int:article_id>')
def get_image(article_id):
    conn = get_db()
    if conn is None:
        return "Image not found", 404
    cur = conn.cursor()
    cur.execute('SELECT image_data FROM articles WHERE id = %s', (article_id,))
    image_data = cur.fetchone()[0]
    cur.close()

    if image_data is None:
        app.logger.error(f"Image not found for article {article_id}")
        return "Image not found", 404
    else:
        app.logger.info(f"Image found for article {article_id}, length: {len(image_data)}")

    response = make_response(bytes(image_data))
    response.headers.set('Content-Type', 'image/jpeg')
    return response

@app.route('/about')
def about():
    return render_template('about.html')

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
    conn = get_db()
    if conn is None:
        return render_template('admin.html', articles=[])
    cur = conn.cursor()
    cur.execute('SELECT id, title FROM articles ORDER BY created_at DESC;')
    articles = cur.fetchall()
    cur.close()
    
    articles_dict = []
    for article in articles:
        articles_dict.append({
            'id': article[0],
            'title': article[1],
        })

    return render_template('admin.html', articles=articles_dict)

@app.route('/admin/add', methods=['POST'])
def add_article():
    if 'user' not in session:
        return redirect(url_for('login'))
    title = request.form['title']
    author = request.form['author']
    content = request.form['content']
    image_url = request.form['image_url']
    
    image_file = request.files['image']
    image_data = image_file.read() if image_file else None

    conn = get_db()
    if conn is None:
        return "Database not available", 503
    cur = conn.cursor()
    # Use parameterized query to prevent SQL injection
    cur.execute(
        'INSERT INTO articles (title, author, content, image_url, image_data) VALUES (%s, %s, %s, %s, %s)',
        (title, author, content, image_url, image_data)
    )
    conn.commit()
    cur.close()
    
    return redirect(url_for('index'))

@app.route('/admin/delete/<int:article_id>', methods=['POST'])
def delete_article(article_id):
    if 'user' not in session:
        return redirect(url_for('login'))
    
    conn = get_db()
    if conn is None:
        return "Database not available", 503
    cur = conn.cursor()
    cur.execute('DELETE FROM articles WHERE id = %s', (article_id,))
    conn.commit()
    cur.close()
    return redirect(url_for('admin'))

@app.route('/admin/edit/<int:article_id>', methods=['GET', 'POST'])
def edit_article(article_id):
    if 'user' not in session:
        return redirect(url_for('login'))

    conn = get_db()
    if conn is None:
        return "Database not available", 503
    cur = conn.cursor()

    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        content = request.form['content']
        image_url = request.form['image_url']
        image_file = request.files.get('image')

        if image_file and image_file.filename != '':
            # New image uploaded
            image_data = image_file.read()
            cur.execute(
                'UPDATE articles SET title = %s, author = %s, content = %s, image_url = NULL, image_data = %s, created_at = CURRENT_TIMESTAMP WHERE id = %s',
                (title, author, content, image_data, article_id)
            )
        elif image_url:
            # New image URL provided
            cur.execute(
                'UPDATE articles SET title = %s, author = %s, content = %s, image_url = %s, image_data = NULL, created_at = CURRENT_TIMESTAMP WHERE id = %s',
                (title, author, content, image_url, article_id)
            )
        else:
            # No new image, keep existing
            cur.execute(
                'UPDATE articles SET title = %s, author = %s, content = %s, created_at = CURRENT_TIMESTAMP WHERE id = %s',
                (title, author, content, article_id)
            )
        
        conn.commit()
        cur.close()
        return redirect(url_for('admin'))

    cur.execute('SELECT id, title, author, content, image_url FROM articles WHERE id = %s', (article_id,))
    article = cur.fetchone()
    cur.close()

    if article is None:
        return "Article not found", 404

    article_dict = {
        'id': article[0],
        'title': article[1],
        'author': article[2],
        'content': article[3],
        'image_url': article[4]
    }

    return render_template('edit_article.html', article=article_dict)

# --- Main Execution ---

if __name__ == '__main__':
    app.run(port=5001, debug=True)