# Error handling: 0 is accepted, 1 is name too long
from validate_email import validate_email
from src.methods.db_structures import SQLDb


class ValidationError(Exception):
    def __init__(self, message="Invalid input"):
        super().__init__(message)

    def name_too_long(self):
        raise ValidationError("Name is too long")

    def name_does_not_exist(self):
        raise ValidationError("No name entered")

    def username_already_exists(self):
        raise ValidationError("Username does exist")


def validate_name(name):
    if len(name) > 64:
        return False
    elif len(name.rstrip())<= 0:
        return False

    return True


def validate_username(username):
    db_test = SQLDb()
    output = db_test.get_username(username)

    if len(output) <= 0:
        return True

    return False


def validate_register_input(c_data):
    print(f"User entered data is {c_data}")

    if not validate_name(c_data[0]):
        print("Name")
        return (0, "Invalid First Name")
    if not validate_name(c_data[1]):
        print("Name 2")
        return (0, "Invalid Last Name")

    if not validate_email(c_data[2]):
        print("Email")
        return (0, "Invalid Email")
    if not validate_username(c_data[3]):
        print("Username")
        return (0, "Invalid Username")
    #
    # if c_data[-1] != c_data[-2]:
    #     print("Repeats")
    #     return False

    return (1, None)

def validate_dish_input(d_data):
    if not validate_name(d_data[0]):
        return (0, "Invalid Name")
    if not validate_name(d_data[1]):
        return (0, "Invalid Cuisine")

    if not validate_dish_description(d_data[3]):
        return (0, "Invalid Description")
    if d_data[4] == "":
        return (0, "Invalid Filenmae")
    if not validate_price(d_data[-1]):
        print(f"Price is {d_data[-1]}")
        return (0, "Invalid Price")

    return (1, None)

def validate_dish_description(description):
    if len(description) > 200:
        return False

    return True

def validate_price(price):
    try:
        price = float(price)
    except Exception as e:
        return False

    return round(int(price * 100), 2)

