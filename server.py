import datetime
import mimetypes
import os
import re # Import re for email validation
from math import ceil # Add this import at the top

import psycopg2
from dotenv import load_dotenv
from flask import (
    Flask,
    flash,
    g,
    make_response,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash

load_dotenv()

# --- Basic App Setup ---
app = Flask(__name__)
app.secret_key = os.urandom(24)


@app.context_processor
def inject_now():
    return {"now": datetime.datetime.utcnow()}


@app.context_processor
def inject_current_user():
    user = session.get("user")
    if user:
        return {"current_user": {"is_authenticated": True, "username": user}}
    return {"current_user": {"is_authenticated": False}}


@app.context_processor
def inject_all_tags():
    conn = get_db()
    if conn is None:
        return {"all_tags_for_nav": [], "tag_icons": {}}
    cur = conn.cursor()
    cur.execute("SELECT name FROM tags WHERE name != '#ad' ORDER BY name")
    all_tags = [row[0] for row in cur.fetchall()]
    cur.close()

    # Font Awesome icon mappings (lowercase keys)
    tag_icons = {
        "ad": "fa-solid fa-money-bill-wave",
        "business": "fa-solid fa-briefcase",
        "for-the-student": "fa-solid fa-graduation-cap",
        "arts": "fa-solid fa-paint-brush",
        "opinion": "fa-solid fa-comments",
        "sports": "fa-solid fa-futbol",
        "student-life": "fa-solid fa-users",
        "student-projects": "fa-solid fa-laptop-code",
        "volunteering-cas": "fa-solid fa-hand-holding-heart",
    }
    # Provide a default icon for tags not explicitly mapped
    default_icon = "fa-solid fa-tag"

    final_tag_icons = {}
    for tag in all_tags:
        # Normalize the tag name for lookup: lowercase and replace spaces with hyphens
        normalized_tag = tag.lower().replace(' ', '-')
        app.logger.debug(f"Processing tag: '{tag}' -> Normalized: '{normalized_tag}'") # Diagnostic log
        final_tag_icons[tag] = tag_icons.get(normalized_tag, default_icon)

    return {'all_tags_for_nav': all_tags, 'tag_icons': final_tag_icons}


from templatetags.tag_helpers import get_tag_class

# Register custom Jinja2 filters
app.jinja_env.filters["get_tag_class"] = get_tag_class

# --- Image Upload Settings ---
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# --- User Authentication ---
# In a real app, you'd store this in a database or a more secure config.
users = {"admin": generate_password_hash("password")}


# --- Database Connection Functions ---
def get_db():
    if "db" not in g:
        try:
            DATABASE_URL = os.environ.get("DATABASE_URL")
            if not DATABASE_URL:
                app.logger.error("DATABASE_URL is not set.")
                return None
            if DATABASE_URL.startswith("https://"):
                DATABASE_URL = DATABASE_URL.replace("https://", "postgresql://")
            g.db = psycopg2.connect(DATABASE_URL)
        except psycopg2.OperationalError as e:
            app.logger.error(f"Failed to connect to the database: {e}")
            return None
    return g.db


@app.teardown_appcontext
def close_connection(exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()


# --- Public Routes ---

ITEMS_PER_PAGE = 9 # Define constant

@app.route("/")
def index():
    conn = get_db()
    if conn is None:
        return render_template("index.html", articles=[], tags=[])

    cur = conn.cursor()

    # Fetch all tags except '#ad'
    cur.execute("SELECT name FROM tags WHERE name != '#ad' ORDER BY name")
    all_tags = [row[0] for row in cur.fetchall()]

    selected_tag = request.args.get("tag")
    page = request.args.get("page", 1, type=int) # Get current page, default to 1

    # Base query for all articles (before pagination limits)
    count_sql = """
        SELECT COUNT(DISTINCT a.id)
        FROM articles a
        LEFT JOIN article_tags at ON a.id = at.article_id
        LEFT JOIN tags t ON at.tag_id = t.id
    """
    
    # Base query for articles
    sql = """
        SELECT a.id, a.title, a.author, a.content, a.image_url, a.created_at, a.image_data IS NOT NULL,
               COALESCE(ARRAY_AGG(t.name), ARRAY[]::VARCHAR[])
        FROM articles a
        LEFT JOIN article_tags at ON a.id = at.article_id
        LEFT JOIN tags t ON at.tag_id = t.id
    """
    where_clauses = []
    params = []

    if selected_tag:
        where_clauses.append("a.id IN (SELECT article_id FROM article_tags WHERE tag_id IN (SELECT id FROM tags WHERE name = %s))")
        params.append(selected_tag)

    if where_clauses:
        sql += " WHERE " + " AND ".join(where_clauses)
        count_sql += " WHERE " + " AND ".join(where_clauses)

    sql += " GROUP BY a.id ORDER BY a.created_at DESC"
    
    # Get total articles count for pagination
    cur.execute(count_sql, tuple(params))
    total_articles = cur.fetchone()[0]
    total_pages = ceil(total_articles / ITEMS_PER_PAGE)

    # Apply pagination limits
    sql += " LIMIT %s OFFSET %s"
    params.extend([ITEMS_PER_PAGE, (page - 1) * ITEMS_PER_PAGE])


    cur.execute(sql, tuple(params))
    articles = cur.fetchall()

    articles_dict = []
    for article in articles:
        articles_dict.append(
            {
                "id": article[0],
                "title": article[1],
                "author": article[2],
                "content": article[3],
                "image_url": article[4],
                "created_at": article[5],
                "has_image": article[6],
                "tags": article[7] if article[7] else [],
            }
        )

    hero_article = articles_dict[0] if articles_dict else None
    # top_articles_dict = articles_dict[1:5] if len(articles_dict) > 1 else [] # top_articles will not be paginated

    cur.execute("SELECT COUNT(*) FROM articles") # This is for author_count, not for pagination
    article_count = cur.fetchone()[0] # This is for author_count, not for pagination
    author_count = 11

    cur.close()

    return render_template(
        "index.html",
        hero_article=hero_article,
        # top_articles=top_articles_dict, 
        articles=articles_dict, # This now contains only the paginated articles
        tags=all_tags,
        selected_tag=selected_tag,
        article_count=article_count,
        author_count=author_count,
        page=page,
        total_pages=total_pages,
        items_per_page=ITEMS_PER_PAGE,
        total_articles=total_articles
    )


@app.route("/article/<int:article_id>")
def article(article_id):
    conn = get_db()
    if conn is None:
        return "Database not available", 503
    cur = conn.cursor()
    cur.execute(
        """
        SELECT a.id, a.title, a.author, a.content, a.image_url, a.created_at, a.image_data IS NOT NULL,
               COALESCE(ARRAY_AGG(t.name), ARRAY[]::VARCHAR[])
        FROM articles a
        LEFT JOIN article_tags at ON a.id = at.article_id
        LEFT JOIN tags t ON at.tag_id = t.id
        WHERE a.id = %s
        GROUP BY a.id;
    """,
        (article_id,),
    )
    article_data = cur.fetchone()
    cur.close()

    if article_data is None:
        return "Article not found", 404

    article_dict = {
        "id": article_data[0],
        "title": article_data[1],
        "author": article_data[2],
        "content": article_data[3],
        "image_url": article_data[4],
        "created_at": article_data[5],
        "has_image": article_data[6],
        "tags": article_data[7] if article_data[7] else [],
    }

    return render_template("article.html", article=article_dict)


@app.route("/image/<int:article_id>")
def get_image(article_id):
    conn = get_db()
    if conn is None:
        return "Image not found", 404
    cur = conn.cursor()
    cur.execute(
        "SELECT image_data, image_mime_type FROM articles WHERE id = %s", (article_id,)
    )
    row = cur.fetchone()
    cur.close()

    if row is None or row[0] is None:
        app.logger.error(f"Image not found for article {article_id}")
        return "Image not found", 404

    image_data, image_mime_type = row

    app.logger.info(f"Image found for article {article_id}, length: {len(image_data)}")

    response = make_response(bytes(image_data))
    response.headers.set("Content-Type", image_mime_type or "application/octet-stream")
    return response


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/search")
def search():
    query = request.args.get("query", "")
    selected_tags_str = request.args.get("tags", "")
    selected_tags = selected_tags_str.split(",") if selected_tags_str else []
    selected_authors = request.args.getlist("authors")
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    conn = get_db()
    if conn is None:
        return render_template(
            "search.html", articles=[], query=query, tags=[], authors=[]
        )

    cur = conn.cursor()

    # Fetch all tags and authors for filter dropdowns
    cur.execute("SELECT DISTINCT name FROM tags ORDER BY name")
    all_tags = [row[0] for row in cur.fetchall()]
    cur.execute("SELECT DISTINCT author FROM articles ORDER BY author")
    all_authors = [row[0] for row in cur.fetchall()]

    # Base query
    sql = """
        SELECT a.id, a.title, a.author, a.content, a.image_url, a.created_at, a.image_data IS NOT NULL,
               COALESCE(ARRAY_AGG(t.name), ARRAY[]::VARCHAR[])
        FROM articles a
        LEFT JOIN article_tags at ON a.id = at.article_id
        LEFT JOIN tags t ON at.tag_id = t.id
    """
    where_clauses = []
    params = []

    if query:
        where_clauses.append(
            "(a.title ILIKE %s OR a.author ILIKE %s OR a.content ILIKE %s)"
        )
        search_term = f"%{query}%"
        params.extend([search_term, search_term, search_term])

    if selected_tags:
        where_clauses.append(
            "a.id IN (SELECT article_id FROM article_tags WHERE tag_id IN (SELECT id FROM tags WHERE name = ANY(%s)))"
        )
        params.append(selected_tags)

    if selected_authors:
        where_clauses.append("a.author = ANY(%s)")
        params.append(selected_authors)

    if start_date:
        where_clauses.append("a.created_at >= %s")
        params.append(start_date)

    if end_date:
        where_clauses.append("a.created_at <= %s")
        params.append(end_date)

    if where_clauses:
        sql += " WHERE " + " AND ".join(where_clauses)

    sql += " GROUP BY a.id ORDER BY a.created_at DESC"

    cur.execute(sql, tuple(params))
    articles = cur.fetchall()
    cur.close()

    articles_dict = []
    for article in articles:
        articles_dict.append(
            {
                "id": article[0],
                "title": article[1],
                "author": article[2],
                "content": article[3],
                "image_url": article[4],
                "created_at": article[5],
                "has_image": article[6],
                "tags": article[7] if article[7] else [],
            }
        )

    return render_template(
        "search.html",
        articles=articles_dict,
        query=query,
        all_tags=all_tags,
        all_authors=all_authors,
        selected_tags=selected_tags,
        selected_authors=selected_authors,
        start_date=start_date,
        end_date=end_date,
    )


@app.route("/tag/<tag_name>")
def tag_page(tag_name):
    conn = get_db()
    if conn is None:
        return "Database not available", 503
    cur = conn.cursor()

    page = request.args.get("page", 1, type=int) # Get current page, default to 1

    # Base query for all articles (before pagination limits) for this tag
    count_sql = """
        SELECT COUNT(DISTINCT a.id)
        FROM articles a
        LEFT JOIN article_tags at ON a.id = at.article_id
        LEFT JOIN tags t ON at.tag_id = t.id
        WHERE a.id IN (SELECT article_id FROM article_tags WHERE tag_id IN (SELECT id FROM tags WHERE name = %s))
    """
    
    # Base query for articles for this tag
    sql = """
        SELECT a.id, a.title, a.author, a.content, a.image_url, a.created_at, a.image_data IS NOT NULL,
               COALESCE(ARRAY_AGG(t.name), ARRAY[]::VARCHAR[])
        FROM articles a
        LEFT JOIN article_tags at ON a.id = at.article_id
        LEFT JOIN tags t ON at.tag_id = t.id
        WHERE a.id IN (SELECT article_id FROM article_tags WHERE tag_id IN (SELECT id FROM tags WHERE name = %s))
        GROUP BY a.id
        ORDER BY a.created_at DESC
    """
    
    # Get total articles count for pagination for this tag
    cur.execute(count_sql, (tag_name,))
    total_articles = cur.fetchone()[0]
    total_pages = ceil(total_articles / ITEMS_PER_PAGE)

    # Apply pagination limits
    sql += " LIMIT %s OFFSET %s"
    params = [tag_name, ITEMS_PER_PAGE, (page - 1) * ITEMS_PER_PAGE]


    cur.execute(sql, tuple(params))
    articles = cur.fetchall()
    cur.close()

    articles_dict = []
    for article in articles:
        articles_dict.append(
            {
                "id": article[0],
                "title": article[1],
                "author": article[2],
                "content": article[3],
                "image_url": article[4],
                "created_at": article[5],
                "has_image": article[6],
                "tags": article[7] if article[7] else [],
            }
        )

    return render_template("tag_page.html", 
                           articles=articles_dict, 
                           tag_name=tag_name,
                           page=page,
                           total_pages=total_pages,
                           items_per_page=ITEMS_PER_PAGE,
                           total_articles=total_articles)


@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        submission_type = request.form.get('submission_type')
        content = request.form.get('content')
        file = request.files.get('file') # For file uploads

        app.logger.info(f"New Submission:")
        app.logger.info(f"  Name: {name}")
        app.logger.info(f"  Email: {email}")
        app.logger.info(f"  Type: {submission_type}")
        app.logger.info(f"  Content: {content[:100]}...") # Log first 100 chars
        if file and file.filename:
            # In a real app, save the file to disk or cloud storage
            app.logger.info(f"  File: {file.filename} ({file.content_type})")
        else:
            app.logger.info(f"  File: None")
        
        # Here you would typically save to a database, send an email, etc.
        # For now, we just flash a success message.
        flash('Your submission has been received! Thank you.', 'success')
        return redirect(url_for('submit')) # Redirect to GET to prevent form resubmission

    return render_template('submit.html')

import re # Import re for email validation

@app.route('/subscribe_newsletter', methods=['POST'])
def subscribe_newsletter():
    email = request.form.get('email')

    if not email:
        flash('Email is required for subscription.', 'error')
        return redirect(url_for('index'))

    # Basic email validation regex
    if not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email):
        flash('Please enter a valid email address.', 'error')
        return redirect(url_for('index'))

    conn = get_db()
    if conn is None:
        flash('Database not available. Please try again later.', 'error')
        return redirect(url_for('index'))

    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO subscribers (email) VALUES (%s)",
            (email,)
        )
        conn.commit()
        flash('Thank you for subscribing to our newsletter!', 'success')
    except psycopg2.errors.UniqueViolation:
        conn.rollback() # Rollback the transaction on unique violation
        flash('This email address is already subscribed.', 'error')
    except Exception as e:
        conn.rollback() # Rollback on any other error
        app.logger.error(f"Error subscribing email {email}: {e}")
        flash('An unexpected error occurred. Please try again later.', 'error')
    finally:
        cur.close()

    return redirect(url_for('index'))


# --- Admin Routes ---


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username in users and check_password_hash(users.get(username), password):
            session["user"] = username
            return redirect(url_for("admin"))
        else:
            return "Invalid credentials", 401
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("index"))


@app.route("/admin")
def admin():
    if "user" not in session:
        return redirect(url_for("login"))
    conn = get_db()
    if conn is None:
        return render_template("admin.html", articles=[], tags=[])
    cur = conn.cursor()
    cur.execute("SELECT id, title FROM articles ORDER BY created_at DESC;")
    articles = cur.fetchall()

    cur.execute("SELECT id, name FROM tags ORDER BY name")
    tags = cur.fetchall()
    cur.close()

    articles_dict = []
    for article in articles:
        articles_dict.append(
            {
                "id": article[0],
                "title": article[1],
            }
        )

    tags_dict = []
    for tag in tags:
        tags_dict.append({"id": tag[0], "name": tag[1]})

    return render_template("admin.html", articles=articles_dict, tags=tags_dict)


@app.route("/admin/add", methods=["POST"])
def add_article():
    if "user" not in session:
        return redirect(url_for("login"))

    conn = get_db()
    if conn is None:
        return "Database not available", 503
    cur = conn.cursor()

    title = request.form["title"]
    author = request.form["author"]
    content = request.form["content"]
    image_url = request.form["image_url"]
    tag_ids = request.form.getlist("tags")

    image_file = request.files.get("image")
    image_data = None
    image_mime_type = None

    if image_file and image_file.filename != "":
        if allowed_file(image_file.filename):
            image_data = image_file.read()
            image_mime_type = image_file.mimetype
        else:
            flash(
                "Invalid image file type. Allowed types are png, jpg, jpeg, gif.",
                "error",
            )
            return redirect(url_for("admin"))

    cur.execute(
        "INSERT INTO articles (title, author, content, image_url, image_data, image_mime_type) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id",
        (title, author, content, image_url, image_data, image_mime_type),
    )
    article_id = cur.fetchone()[0]

    for tag_id in tag_ids:
        cur.execute(
            "INSERT INTO article_tags (article_id, tag_id) VALUES (%s, %s)",
            (article_id, tag_id),
        )

    conn.commit()
    cur.close()

    return redirect(url_for("admin"))


@app.route("/admin/delete/<int:article_id>", methods=["POST"])
def delete_article(article_id):
    if "user" not in session:
        return redirect(url_for("login"))

    conn = get_db()
    if conn is None:
        return "Database not available", 503
    cur = conn.cursor()
    cur.execute("DELETE FROM articles WHERE id = %s", (article_id,))
    conn.commit()
    cur.close()
    return redirect(url_for("admin"))


@app.route("/admin/edit/<int:article_id>", methods=["GET", "POST"])
def edit_article(article_id):
    if "user" not in session:
        return redirect(url_for("login"))

    conn = get_db()
    if conn is None:
        return "Database not available", 503
    cur = conn.cursor()

    if request.method == "POST":
        title = request.form["title"]
        author = request.form["author"]
        content = request.form["content"]
        image_url = request.form["image_url"]
        tag_ids = request.form.getlist("tags")
        image_file = request.files.get("image")

        if image_file and image_file.filename != "":
            if allowed_file(image_file.filename):
                image_data = image_file.read()
                image_mime_type = image_file.mimetype
                cur.execute(
                    "UPDATE articles SET title = %s, author = %s, content = %s, image_url = NULL, image_data = %s, image_mime_type = %s, created_at = CURRENT_TIMESTAMP WHERE id = %s",
                    (title, author, content, image_data, image_mime_type, article_id),
                )
            else:
                flash(
                    "Invalid image file type. Allowed types are png, jpg, jpeg, gif.",
                    "error",
                )
                return redirect(url_for("edit_article", article_id=article_id))
        elif image_url:
            # New image URL provided
            cur.execute(
                "UPDATE articles SET title = %s, author = %s, content = %s, image_url = %s, image_data = NULL, image_mime_type = NULL, created_at = CURRENT_TIMESTAMP WHERE id = %s",
                (title, author, content, image_url, article_id),
            )
        else:
            # No new image, keep existing
            cur.execute(
                "UPDATE articles SET title = %s, author = %s, content = %s, created_at = CURRENT_TIMESTAMP WHERE id = %s",
                (title, author, content, article_id),
            )

        # Update tags
        cur.execute("DELETE FROM article_tags WHERE article_id = %s", (article_id,))
        for tag_id in tag_ids:
            cur.execute(
                "INSERT INTO article_tags (article_id, tag_id) VALUES (%s, %s)",
                (article_id, tag_id),
            )

        conn.commit()
        cur.close()
        return redirect(url_for("admin"))

    # GET request
    cur.execute(
        "SELECT id, title, author, content, image_url FROM articles WHERE id = %s",
        (article_id,),
    )
    article = cur.fetchone()

    if article is None:
        cur.close()
        return "Article not found", 404

    cur.execute("SELECT id, name FROM tags ORDER BY name")
    all_tags = cur.fetchall()

    cur.execute("SELECT tag_id FROM article_tags WHERE article_id = %s", (article_id,))
    article_tags = [row[0] for row in cur.fetchall()]

    cur.close()

    article_dict = {
        "id": article[0],
        "title": article[1],
        "author": article[2],
        "content": article[3],
        "image_url": article[4],
        "tags": article_tags,
    }

    all_tags_dict = []
    for tag in all_tags:
        all_tags_dict.append({"id": tag[0], "name": tag[1]})

    return render_template(
        "edit_article.html", article=article_dict, tags=all_tags_dict
    )


# --- Main Execution ---

if __name__ == "__main__":
    app.run(port=5001, debug=True)
