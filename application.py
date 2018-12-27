import os

from flask import Flask, session, render_template, request
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
    return render_template("book-reviews.html")

@app.route("/login", methods=["POST"])
def login():
    """Log into the Webpage"""

    # Get form information.
    user = request.form.get("username")
    password = request.form.get("password")

    # Make sure flight exists.
    db.execute("INSERT INTO users (username, password) VALUES (:username, :password)",
            {"username": user, "password": password})
    db.commit()
    return "successful login"

@app.route("/database")
def database():
    users = db.execute("SELECT * FROM users").fetchall()
    text = ""
    for user in users:
        text += str(user[0]) +": "+ user[1] +" "+ user[2] + "<br>"
    return 'database' + "<br>" + text