from flask import Flask, render_template, request, redirect, flash, session
from flask_session import Session
from cs50 import SQL
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

# Flask instance configuration
app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

app.secret_key = "super secret key"

# Database started
db = SQL("sqlite:///database.db")


# Homepage / Purchase documentation
@app.route("/")
def index():

    # Check if user is logged in
    try:
        # Get id from current user
        user_value = session["user_id"]

        # Get data from database users
        log_name = db.execute("SELECT user_name FROM users WHERE user_id = :user_id", user_id=user_value)
        log_cash = db.execute("SELECT user_cash FROM users WHERE user_id = :user_id", user_id=user_value)

        # Get data from database transactions
        transactions_db = db.execute("SELECT * FROM transactions WHERE user_id = :user_id", user_id=user_value)

        # List of prices times amount
        total_price = []


        for item in transactions_db:
            if user_value==int(item["user_id"]):
                total_price.append((int(item["items_amount"])) * int(item["items_price"]))

        # Render homepage with purchasing documentation for logged in user
        return render_template("index.html", transactions_db=transactions_db, log_name=log_name[0]["user_name"], log_cash=log_cash[0]["user_cash"], total_price=total_price)

    except:
        # Render homepage for user which not logged in
        redirect("/")

    # Render homepage without user data
    return render_template("index.html")


# Registration
@app.route("/registration", methods=["GET", "POST"])
def registration():

    if request.method=="POST":
        # Get data from registration.html
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        password_confirmation = request.form.get("password_confirmation")

        # Check if data is empty or false
        if not username:
            flash("Please enter a username")
            return render_template("registration.html")

        if not email:
            flash("Please enter a E-Mail adress")
            return render_template("registration.html")

        if not password or not password_confirmation or password != password_confirmation:
            flash("Please enter a password and the same confirmation")
            return render_template("registration.html")

        # Database query
        username_test = db.execute("SELECT COUNT(*) FROM users WHERE user_name = :user_name", user_name=username)
        email_test = db.execute("SELECT COUNT(*) FROM users WHERE user_email = :user_email", user_email=email)

        # Check if username is in database
        if username_test[0]["COUNT(*)"] != 0:
            flash("Username is already used please enter other username")
            return render_template("registration.html")

        # Check if email is in database
        if email_test[0]["COUNT(*)"] != 0:
            flash("E-Mail adress is already used please enter other E-Mail adress")
            return render_template("registration.html")

        # Insert new user to databse (Registration)
        db.execute("INSERT INTO users(user_name, user_email, user_password) VALUES (?, ?, ?)", username, email, generate_password_hash(password))

        flash("You are registered, please log in")

        # Bring user to login
        return render_template("login.html")
    else:
        return render_template("registration.html")

# Login
@app.route("/login", methods=["GET", "POST"])
def login():
    # Clear other session
    session.clear()

    if request.method=="POST":

        # Check if username was entered
        if not request.form.get("username"):
            flash("Please enter your username")
            return render_template("login.html")

        # Check if password was entered
        if not request.form.get("password"):
            flash("Please enter your password")
            return render_template("login.html")

        # Query database for data
        data = db.execute("SELECT * FROM users WHERE user_name = ?", request.form.get("username"))

        # Check if username and password is correct
        if len(data) != 1 or not check_password_hash(data[0]["user_password"], request.form.get("password")):
            flash("Entered data does not match, please try again")
            return render_template("login.html")

        # Log in process
        session["user_id"] = data[0]["user_id"]

        # Render homepage with current user purchase documentation
        return redirect("/")
    else:
        # Render login page
        return render_template("login.html")

# Logout
@app.route("/logout")
def logout():

    # Logout user
    session.clear()

    # Return to homepage without user data
    return redirect("/")

# E-Market
@app.route("/emarket", methods=["GET", "POST"])
def emarket():

    # Dictionary with items
    items_db = db.execute("SELECT * FROM items")

    try:
        user_value = session["user_id"]

        # Get global data from database
        log_name = db.execute("SELECT user_name FROM users WHERE user_id = :user_id", user_id=session["user_id"])
        log_cash = db.execute("SELECT user_cash FROM users WHERE user_id = :user_id", user_id=session["user_id"])

        if request.method == "GET":

            # Render emarket for logged in users
            return render_template("emarket.html", items_db=items_db, log_name=log_name[0]["user_name"], log_cash=log_cash[0]["user_cash"])
        else:
            # No use only for the function of the application
            return render_template("emarket.html")
    except:
        # Render emarket for not logged in users
        return render_template("emarket.html", items_db=items_db)

# Bought
@app.route("/bought", methods=["GET", "POST"])
def bought():

    # Get data from items database
    items_db = db.execute("SELECT * FROM items")

    if request.method=="POST":

        try:
            user_value = session["user_id"]

            # Get data from emarket.html
            amount = request.form.get("amount")
            item_buy_id = request.form.get("item_buy_id")

            # Get data from users and items db
            log_name = db.execute("SELECT user_name FROM users WHERE user_id = :user_id", user_id=user_value)
            log_cash = db.execute("SELECT user_cash FROM users WHERE user_id = :user_id", user_id=user_value)
            item_price = db.execute("SELECT price FROM items WHERE item_id = :item_id", item_id=item_buy_id)
            item_name = db.execute("SELECT name FROM items WHERE item_id = :item_id", item_id=item_buy_id)

            # Check the amount
            if  int(amount) <= 0:
                flash("Please enter a amount greater than zero")
                return render_template("emarket.html", items_db=items_db, log_name=log_name[0]["user_name"], log_cash=log_cash[0]["user_cash"])


            # Check if user has enough cash
            if (int(item_price[0]["price"]) * int(amount)) > int(log_cash[0]["user_cash"]):
                flash("Sorry you have not enough money")
                return render_template("emarket.html", items_db=items_db, log_name=log_name[0]["user_name"], log_cash=log_cash[0]["user_cash"])


            # Buy item and update db
            current_cash = int(log_cash[0]["user_cash"]) - (int(item_price[0]["price"]) * int(amount))

            db.execute("UPDATE users SET user_cash = ? WHERE user_id = ?", current_cash, session["user_id"])

            transactions_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            db.execute("INSERT INTO transactions (user_id, items_id, items_amount, items_price, items_name, transactions_date) VALUES (:user_id, :items_id, :items_amount, :items_price, :items_name, :transactions_date)", user_id=session["user_id"], items_id=item_buy_id, items_amount=int(amount), items_price=int(item_price[0]["price"]), items_name=str(item_name[0]["name"]), transactions_date=transactions_date)

            # Update users db the transactions_count value
            transactions_db = db.execute("SELECT * FROM transactions WHERE user_id = :user_id", user_id=user_value)

            count = 0

            for counter in transactions_db:
                count+=1

            db.execute("UPDATE transactions SET transactions_count = ? WHERE transactions_date = ?", count, transactions_date)

        except:
            # Render login page when the user does something that requires login
            return render_template("login.html")

        # Return to the purchasing documentation with updated values
        return redirect("/")
    else:
        # Render emarket page for not logged in users
        return render_template("emarket.html", items_db=items_db)

# Error 404 handling
@app.errorhandler(404)
def error_404(e):
    return render_template("404.html"), 404

# Error 500 handling
@app.errorhandler(500)
def error_500(e):
    return render_template("500.html"), 500