#import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import model_restaurant
from flask_bcrypt import Bcrypt
from flask_app import app
import re


bcrypt= Bcrypt(app)

DATABASE = 'pho_list_db'
#model the class after the table from our database

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        # self.restaurants = []



# Create
    @classmethod
    def create(cls, data:dict):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return  connectToMySQL(DATABASE).query_db(query, data)

# Read
    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)

        if len(results) < 1:
            return False

        return User(results[0])

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)

        if len(results) < 1:
            return False

        return User(results[0])


# Update
# Delete

#Static Methods

    @staticmethod
    def register_validator(post_data):
        is_valid = True

        if len(post_data["first_name"]) < 2:
            flash("First Name must be at least 2 characters", "err_reg_first_name")
            is_valid = False

        if len(post_data["last_name"]) < 2:
            flash("Last Name must be at least 2 characters", "err_reg_last_name")
            is_valid = False

        if len(post_data["email"]) < 2:
            flash("Email cannot be blank", "err_reg_email")
            is_valid = False


        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
        if not EMAIL_REGEX.match(post_data['email']): 
            flash("Invalid email address!", "err_reg_email")
            is_valid = False

        if len(post_data["password"]) < 8:
            flash("Password must be at least 8 characters", "err_reg_password")
            is_valid = False
            
        if post_data["password"] != post_data["confirm_password"]:
            flash("Passwords DO NOT match", "err_reg_confirm_password")
            is_valid = False
            
        return is_valid

    @staticmethod
    def login_validator(post_data):
        user = User.get_by_email({"email": post_data['email']})

        if not user:
            flash("Invalid Credentials", "err_reg_user")
            return False

        if not bcrypt.check_password_hash(user.password, post_data["password"]):
            flash("Invalid Password", "err_reg_wrong")
            return False

        return True

