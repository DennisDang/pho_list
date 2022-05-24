from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import model_user
from flask import flash

DATABASE = 'pho_list_db'

class Restaurant:
    def __init__(self, data):
        self.id = data['id']
        self.restaurant_name = data['restaurant_name']
        self.location = data['location']
        self.topping = data['topping']
        self.noodle = data['noodle']
        self.broth = data['broth']
        self.overall_score = data['overall_score']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


#Create
    @classmethod
    def create(cls, data:dict):
        query = "INSERT INTO restaurants (user_id, restaurant_name, description, location, topping, nnodle, broth, overall_score) VALUES (%(user_id)s, %(restaurant_name)s, %(description)s, %(location)s, %(topping)s, %(noodle)s, %(broth)s, %(overall_score)s);"
        return  connectToMySQL(DATABASE).query_db(query, data)
#Read

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM restaurants;"
        results = connectToMySQL(model_user.DATABASE).query_db(query)

        restaurants = []
        for restaurant in results:
            restaurants.append(cls(restaurant))
        return restaurants

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM restaurants WHERE id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)

        if len(results) < 1:
            return False

        return Restaurant(results[0])
#Update
    @classmethod
    def update(cls, data):
        query = "UPDATE restaurants SET restaurant_name = %(restaurant_name)s, description = %(description)s, location = %(location)s, topping = %(topping)s, noodle = %(noodle)s, broth = %(broth)s, overall_score = %(overall_score)s WHERE id = %(id)s; "
        return  connectToMySQL(DATABASE).query_db(query, data)
#Delete
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM restaurants WHERE id = %(id)s;"
        connectToMySQL(DATABASE).query_db(query, data)
        
#Static Methods

    @staticmethod
    def validate(post_data):
        is_valid = True

        if len(post_data['restaurant_name']) < 2:
            flash("Restaurant name must be at least 2 characters")
            is_valid = False

        if len(post_data['location']) < 2:
            flash("Location must be at least 2 characters")
            is_valid = False
                   
        if int(post_data['topping']) < 0:
            flash("Rating must be 1-5")
            is_valid = False

        if int(post_data['noodle']) < 0:
            flash("Rating must be 1-5")
            is_valid = False

        if int(post_data['broth']) < 0:
            flash("Rating must be 1-5")
            is_valid = False

        if int(post_data['overall_score']) < 0:
            flash("Rating must be 1-5")
            is_valid = False

        if len(post_data['description']) < 2:
            flash("Description must be at least 2 characters")
            is_valid = False

        return is_valid

