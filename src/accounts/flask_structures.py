from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField


class LoginForm(FlaskForm):
    username = StringField("username")
    password = PasswordField("password")
    submit = SubmitField("login")


class RegisterForm(FlaskForm):
    first_name = StringField("first_name")
    last_name = StringField("last_name")

    email_address = StringField("email_address")
    username = StringField("username")
    date_of_birth = StringField("dob")

    home_address = StringField("home_address")

    password = PasswordField("password")
    repeat_password = PasswordField("password2")

    submit = SubmitField("signup")

class DishForm(FlaskForm):
    dish_name = StringField("dish_name")
    dish_cuisine = StringField("dish_cuisine")
    dish_description = StringField("dish_description")
    dish_price = StringField("dish_price")