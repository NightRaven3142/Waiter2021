from src.methods.db_structures import *
from src.methods.carriers import *
from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)
app.debug = True
app.secret_key = "AUjKj298!$g.?"

DB = SQLDb()

nav_data = navbar_data()

@app.route("/")
def index():
    nav_data.set_left("Order")
    nav_data.set_right_a("Login")
    nav_data.set_right_b("Signup")

    return redirect(url_for("home"))

@app.route("/home", methods= ["GET", "POST"])
def home():
    global nav_data
    return render_template("home.html", navbar_data=nav_data)

@app.route("/order")
def order():
    global nav_data
    return render_template("order.html", navbar_data=nav_data)

@app.route("/login")
def login():
    global nav_data
    return render_template("login.html", navbar_data=nav_data)

@app.route("/signup")
def signup():
    global nav_data
    return render_template("signup.html", navbar_data=nav_data)

@app.route("/account_details")
def account_details():
    global nav_data
    return render_template("account_details.html", navbar_data=nav_data)

if __name__ == '__main__':
    app.run()
