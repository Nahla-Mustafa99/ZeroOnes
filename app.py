import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps



# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///ourdb.db")

# Check that te user is logged in
def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure main page
@app.route("/")
def index():
    # Grab all the posts from the database
    posts = db.execute("SElECT * FROM posts ORDER BY date_posted Desc")
    return render_template("index.html", posts=posts)

# Register Form
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # 1- get response of form
    if request.method == "POST":
        name = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        isExist = db.execute("SELECT EXISTS (SELECT * FROM users WHERE email = ?) AS exist", email)  # 1exists2Keyerror
        isUsed = True if isExist[0]["exist"] >= 1 else False
        if not name or not email or not password or not confirmation:
            #return apology("User’s input is blank", 400)
            #return "<h1>You Probably did not enter one of the required inputs, please try again...<h1>"
            flash("Failed to register")
            message= "You Probably did not enter one of the required inputs, please try again..."
            link = "/register"
            return render_template("apology.html", message=message, link=link)
        if isUsed:
            #return apology("Username already exists", 400)
            #return "<h1>This email already exists</h1>"
            flash("Failed to register")
            message= "This email already exists, please try another one..."
            link = "/register"
            return render_template("apology.html", message=message, link=link)
        if password != confirmation:
            flash("Failed to register")
            message= "You Password don't match, Please try again..."
            link = "/register"
            return render_template("apology.html", message=message, link=link)
        hash = generate_password_hash(password)
        db.execute("INSERT INTO users(name, email, hash, date_joined) VALUES(?, ?, ?, DATETIME())", name, email, hash)
        return redirect("/login")
    else:
        return render_template("register.html")

# Create Search Function
@app.route('/search')
def search():
    word = request.args.get("q")
	# Query the Database
    posts = db.execute("SELECT * FROM posts WHERE title LIKE ? or tag LIKE ? or content like ? ORDER BY title", f'%{word}%', f'%{word}%', f'%{word}%')
    print(posts)
    return render_template("search.html", word=word, posts=posts)


# Create Login Page
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    # Forget any user_id
    session.clear()
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("email"):
            flash("Failed to login")
            message= "You must provide an email, Please try again..."
            link = "/login"
            return render_template("apology.html", message=message, link=link)

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("Failed to login")
            message= "You must provide a password, please try again..."
            link = "/login"
            return render_template("apology.html", message=message, link=link)


        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE email = ?", request.form.get("email"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            flash("Failed to login")
            message= "Invalid email or password, please try again..."
            link = "/login"
            return render_template("apology.html", message=message, link=link)
        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

# User Profile
@app.route("/user")
def user():
   rows = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
   user = rows[0]
   posts = db.execute("SELECT * FROM posts WHERE author_id = ? ORDER BY date_posted DESC", session["user_id"])
   if len(posts) >=1:
    return render_template("user.html",user=user, posts=posts)
   else:
    return render_template("user.html", user=user)



# Add Post Form
@app.route('/addpost', methods=['GET', 'POST'])
@login_required
def add_post():
    # 1- get response of form
    if request.method == "POST":
        title = request.form.get("title")
        tag = request.form.get("tag")
        content = request.form.get("content")

        if not title or not tag or not content:
            flash("Failed to add the post")
            message= "You Probably left one of the required inputs empty, please try again..."
            link = "/addpost"
            return render_template("apology.html", message=message, link=link)
        name_row = db.execute("SELECT name FROM users WHERE id = ?", session["user_id"])
        author = name_row[0]["name"]
        db.execute("INSERT INTO posts(title, tag, content, date_posted, author_id, author) VALUES(?, ?, ?,  DATETIME(), ?, ?)", title, tag, content, session["user_id"], author)
        # Return a Message
        flash("Blog Post Submitted Successfully!")
        return redirect("/")

# Redirect to the webpage
    else:
        return render_template("addpost.html")

# Idividual POST page
@app.route('/posts/<int:id>')
def post(id):
    post = db.execute("SELECT * FROM posts WHERE post_id = ?", id)
    print(post[0])
    return render_template('post.html', post=post[0])

# Edit Post Form
@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    if request.method == "POST":
        title = request.form.get("title")
        tag = request.form.get("tag")
        content = request.form.get("content")
        if not title or not tag or not content:
            flash("Failed to edit the post")
            message= "You Probably left one of the required inputs empty, please try again..."
            link = f"/posts/edit/{id}"
            return render_template("apology.html", message=message, link=link)

        # Update Database
        db.execute("UPDATE posts SET title = ?, tag = ?, content = ?  WHERE post_id = ?", title, tag, content, id)
        flash("Post Has Been Updated!")
        return redirect(url_for('post', id=id))
    author_id = db.execute("SELECT author_id FROM posts WHERE post_id = ?", id)
    if session["user_id"] == author_id[0]["author_id"]: #or current_user.id == 14:
        data = db.execute("SELECT * FROM posts WHERE post_id = ?", id)
        print (data[0])
        return render_template('editpost.html', data=data[0])
    else:
        flash("You Aren't Authorized To Edit This Post...")
        posts = db.execute("SELECT * FROM posts ORDER BY date_posted DESC ")
        return render_template("index.html", posts=posts)

# Delete pots
@app.route('/posts/delete/<int:id>')
@login_required
def delete_post(id):
    rows = db.execute("SELECT author_id FROM posts WHERE post_id = ?", id)
    print(rows)
    author_id = rows[0]["author_id"]
    user_id = session["user_id"]
    if user_id == author_id: # or id == 14:
        try:
            db.execute("DELETE FROM posts WHERE post_id = ?", id)
            # Return a message
            flash("Post Was Deleted!")
            # Grab all the posts from the database
            posts = db.execute("SELECT * FROM posts Order by date_posted desc")
            return render_template("index.html", posts=posts)

        except:
            # Return an error message
            flash("There was a problem deleting post, try again...")
            # Grab all the posts from the database
            posts =  db.execute("SELECT * FROM posts order by date_posted desc")
            return render_template("index.html", posts=posts)
    else:
        # Return a message
        flash("You Aren't Authorized To Delete That Post!")

        # Grab all the posts from the database
        posts =  db.execute("SELECT * FROM posts order by date_posted desc")
        return render_template("index.html", posts=posts)

# Logout
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")