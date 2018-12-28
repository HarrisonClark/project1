import os

from flask import Flask, session, render_template, request, redirect
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return redirect("/login")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/process-login", methods=["POST"])
def process_login():
    """Log into the Webpage"""

    # Get form information.
    email = request.form.get("email")
    password = request.form.get("password")

    # Make sure flight exists.
    if db.execute("SELECT id FROM users WHERE email = :em AND password = :ps", {"em": email, "ps": password}).rowcount == 0:
        return "Incorrect Email or Password."
    else:
        return redirect("/database")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/process-registration", methods=["POST"])
def process_registration():
    """Registers new account with Webpage"""

    # Get form information.
    email = request.form.get("email")
    password = request.form.get("password")
    # Make sure flight exists.
    db.execute("INSERT INTO users (email, password) VALUES (:email, :password)", {"email": email, "password": password})
    db.commit()
    return redirect("/database")

@app.route("/database")
def database():
    users = db.execute("SELECT * FROM users").fetchall()
    text = ""
    for user in users:
        text += str(user[0]) +": "+ user[1] +" "+ user[2] + "<br>"
    return 'database' + "<br>" + text

@app.route("/user/<string:user_name>")
def user(user_name):
    return render_template("user-page.html", username=user_name)

@app.route("/search")
def serach():
    return render_template("search.html")

@app.route("/search-isbn", methods=["POST"])
def search_isbn():
    """Searches through book database using isbn"""
    # Get form information.
    isbn = request.form.get("isbn")
    # Make sure flight exists.
    results = db.execute("SELECT title, author FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchall()
    if results is None:
        return "<h3>There were no matching books</h1>"
    text = "<br>"
    for result in results:
        text += result.title + " by " + result.author + "<br>"
    return text

@app.route("/search-title", methods=["POST"])
def search_title():
    """Searches through book database using title"""
    # Get form information.
    title = request.form.get("title")
    # Make sure flight exists.
    results = db.execute("SELECT title, author FROM books WHERE title = :title", {"title": title}).fetchall()
    if results is None:
        return "<h3>There were no matching books</h1>"
    text = "<br>"
    for result in results:
        text += result.title + " by " + result.author + "<br>"
    return text

@app.route("/search-author", methods=["POST"])
def search_author():
    """Searches through book database using author"""
    # Get form information.
    author = request.form.get("author")
    # Make sure flight exists.
    results = db.execute("SELECT title, author FROM books WHERE author = :author", {"author": author}).fetchall()
    if results is None:
        return "<h3>There were no matching books</h1>"
    text = "<br>"
    for result in results:
        text += result.title + " by " + result.author + "<br>"
    return text

@app.route("/isbn/<string:isbn>")
def book_isbn(isbn):
    book = db.execute("SELECT title, author FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()
    if book is None:
        return "ERROR! Book doesn't exisit"
    text = "<br>" + isbn + " is " + book.title + " by " + book.author + ".<br>"
    return text
