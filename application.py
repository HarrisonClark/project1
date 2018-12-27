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
    username = request.form.get("username")
    password = request.form.get("password")

    # Make sure flight exists.
    if db.execute("SELECT userId FROM users WHERE username = :us AND password = :ps", {"us": username, "ps": password}).rowcount == 0:
        return "Incorrect Username or Password."
    else:
        return redirect("/database")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/process-registration", methods=["POST"])
def process_registration():
    """Registers new account with Webpage"""

    # Get form information.
    usern = request.form.get("username")
    passw = request.form.get("password")
    print('----------------------------------------------------------')
    print(usern, passw)
    print('----------------------------------------------------------')
    # Make sure flight exists.
    db.execute("INSERT INTO users (username, password) VALUES (:username, :password)", {"username": usern, "password": passw})
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
