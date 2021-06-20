from src.methods.cookie_management import *
from src.methods.carriers import *
from flask import render_template, redirect, url_for, session, request, flash
from werkzeug.utils import secure_filename
from src.accounts.flask_structures import *
from src.methods.structures import *
from src.accounts.validation import *
import os

UPLOAD_FOLDER = 'src/static/order_images'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', "JPG"}

app = Flask(__name__)
app.debug = True
app.secret_key = "AUjKj298!$g.?"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

DB = SQLDb()

nav_data = navbar_data()

current_dishes = []

@app.before_request
def make_session_permanent():
    session.permanent = True

def set_navbar():
    u_name = session.get("waiter_username_01A", None)
    print(f"Username is {u_name}")

    if u_name is None:
        nav_data.populate_no_user()
    else:
        nav_data.populate_logged_in_user()
        session["waiter_is_logged_in"] = True
        #
        # if session.get("waiter_current_user") is None:
        #     session["waiter_current_user"] = User(DB.get_username(u_name))


def get_dishes():
    global current_dishes

    dishes_db = DB.get_all_dishes()
    print(dishes_db)
    dishes_converted = []
    for d in dishes_db:
        dishes_converted.append(Dish(d))

    current_dishes = dishes_converted

@app.route("/")
def index():
    set_navbar()
    DB.initialise_tables()
    get_dishes()

    return redirect(url_for("home"))

@app.route("/home", methods= ["GET", "POST"])
def home():
    global nav_data
    set_navbar()

    return render_template("home.html", navbar_data=nav_data)

@app.route("/order")
def order():
    global nav_data
    global current_dishes

    set_navbar()

    return render_template("order.html", navbar_data=nav_data, dishes=current_dishes)

@app.route("/login", methods=["GET", "POST"])
def login():
    global nav_data
    set_navbar()

    form = LoginForm()
    output = ""

    if form.is_submitted():
        username = form.username.data
        password = form.password.data

        if username == "" or username is None:
            return render_template("login.html", navbar_data=nav_data, output=output)

        user_info = User(DB.get_username(username))

        if user_info.is_empty():
            output = "Username not found"
            return render_template("login.html", navbar_data=nav_data, output=output)
        elif password != user_info.get_password_hash():
            output = "Invalid password"
            return render_template("login.html", navbar_data=nav_data, output=output)
        else:
            session["waiter_username_01A"] = username
            set_is_logged_in_cookie(True)
            set_current_user_id_cookie(user_info.get_user_id())

            return redirect(url_for("account_details"))
    else:
        output = "Login Failed"
        return render_template("login.html", navbar_data=nav_data, output=output)

    return render_template("login.html", navbar_data=nav_data, output=output)

@app.route("/signup")
def signup():
    global nav_data
    set_navbar()

    return render_template("signup.html", navbar_data=nav_data)

@app.route("/signup_cook", methods=["GET", "POST"])
def signup_cook():
    global nav_data
    set_navbar()

    form = RegisterForm()
    output = ""
    print("In signup")

    if form.is_submitted():
        print("Is submitted")
        cook_data = (form.first_name.data, form.last_name.data, form.email_address.data, form.username.data,
                     form.date_of_birth.data, form.home_address.data, form.password.data, form.repeat_password.data)

        validation = validate_register_input(cook_data)
        if not validation[0]:
            output = validation[1]
            return render_template("signup_cook.html", navbar_data=nav_data, output=output, form=form)

        DB.insert_new_cook((cook_data[0], cook_data[1], cook_data[2], cook_data[-2], cook_data[4], cook_data[3]))

    return render_template("signup_cook.html", navbar_data=nav_data, output=output, form=form)


@app.route("/signup_customer", methods=["GET", "POST"])
def signup_customer():
    global nav_data
    set_navbar()

    form = RegisterForm()
    output = ""
    print("In customer signup")

    if form.is_submitted():
        print("Is customer submitted")
        customer_data = (form.first_name.data, form.last_name.data, form.email_address.data, form.username.data,
                     form.date_of_birth.data, form.home_address.data, form.password.data, form.repeat_password.data)

        validation = validate_register_input(customer_data)
        if not validation[0]:
            output = validation[1]
            return render_template("signup_customer.html", navbar_data=nav_data, output=output, form=form)

        DB.insert_new_customer((customer_data[0], customer_data[1], customer_data[2], customer_data[-2], customer_data[4], customer_data[3]))

    return render_template("signup_customer.html", navbar_data=nav_data, output=output, form=form)

@app.route("/logout")
def logout():
    set_is_logged_in_cookie(False)
    set_is_cook_cookie(False)

    session["waiter_username_01A"] = None
    session["waiter_basket"] = None

    return redirect(url_for("home"))

@app.route("/purchase_confirm")
def purchase_confirm():
    global nav_data
    set_navbar()

    return render_template("purchase_confirm.html", navbar_data=nav_data, basket=session.get("waiter_basket", None))

@app.route("/account_details")
def account_details():
    global nav_data
    set_navbar()

    if get_is_logged_in_cookie():
        current_user_obj = User(DB.get_username(session.get("waiter_username_01A", None)))
        if DB.is_user_in_cook_table(current_user_obj.get_user_id()):
            current_user_obj = Cook(current_user_obj.get_data_as_tuple(), current_user_obj.get_user_id())
            set_is_cook_cookie(True)
            return render_template("account_details_cook.html", navbar_data=nav_data, user=current_user_obj)
        elif DB.is_user_in_customer_table(current_user_obj.get_user_id()):
            current_user_obj = Customer(current_user_obj.get_data_as_tuple(), current_user_obj.get_user_id())
            set_is_cook_cookie(False)
            return render_template("account_details_customer.html", navbar_data=nav_data, user=current_user_obj)
    else:
        return redirect(url_for("home"))

@app.route("/reroute_purchase_confirm")
def reroute_purchase_confirm():
    global nav_data
    set_navbar()

    print("Purchase rerouted")

    return redirect(url_for("purchase_confirm"))

@app.route("/reroute_cook")
def reroute_cook():
    global nav_data
    set_navbar()

    return redirect(url_for("signup_cook"))

@app.route("/reroute_customer")
def reroute_customer():
    global nav_data
    set_navbar()

    return redirect(url_for("signup_customer"))

# @app.route("/reroute_purchase")
# def reroute_purchase():
#     global nav_data
#     set_navbar()
#
#     print("Reroute")
#
#     return redirect(url_for("purchase_confirm"))

@app.route("/reroute_new_dish")
def reroute_new_dish():
    global nav_data
    set_navbar()

    return redirect(url_for("new_dish"))

@app.route("/order_completed")
def order_completed():
    global nav_data
    set_navbar()

    return render_template("order_completed.html", navbar_data=nav_data)

@app.route("/complete_order")
def complete_order():
    global nav_data
    set_navbar()

    print("Purchased")
    return redirect(url_for("order_completed"))

@app.route("/reroute_nav_a")
def reroute_nav_a():
    if get_is_logged_in_cookie():
        return redirect(url_for("account_details"))
    else:
        return redirect(url_for("login"))

@app.route("/reroute_nav_b")
def reroute_nav_b():
    if get_is_logged_in_cookie():
        return redirect(url_for("logout"))
    else:
        return redirect(url_for("signup"))

@app.route("/add_dish_to_basket", methods=["GET", "POST"])
def add_dish_to_basket():
    global current_dishes

    if request.method == "POST":
        dish_js_id = request.form["d_id"]
        print(f"Dish id is {dish_js_id}")
        basket = session.get("waiter_basket", None)
        if basket is None or len(basket) == 0:
            session["waiter_basket"] = [x.dish_id for x in current_dishes if x.dish_id == int(dish_js_id)]
        else:
            print(f"Basket is {session['waiter_basket']}")

        print(f"Basket is {session.get('waiter_basket', None)}")
        return dish_js_id


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/new_dish', methods=['GET', 'POST'])
def new_dish():
    if not get_is_cook_cookie():
        return redirect(url_for("home"))

    form = DishForm()
    output = ""
    print("In dish form")

    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']

        if form.is_submitted():
            dish_data = (form.dish_name.data, form.dish_cuisine.data, get_current_user_id_cookie(),
                         form.dish_description.data, file.filename, form.dish_price.data)

            validation = validate_dish_input(dish_data)
            if not validation[0]:
                output = validation[1]
                return render_template("new_dish.html", navbar_data=nav_data, output=output)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        print(f"Dish data is {dish_data}")
        DB.insert_new_dish(dish_data)
        get_dishes()

    return render_template("new_dish.html", navbar_data=nav_data, output=output)


if __name__ == '__main__':
    app.run()
