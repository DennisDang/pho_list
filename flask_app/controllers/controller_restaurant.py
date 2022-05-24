from flask import render_template, redirect, request, session

from flask_app import app
from flask_app.models.model_user import User
from flask_app.models.model_restaurant import Restaurant

@app.route("/home")
def home():
    if "uuid" not in session:
        return redirect("/")


    return render_template(
        "home.html", user = User.get_by_id({"id": session['uuid']}),
        all_restaurants = Restaurant.get_all()
    )

@app.route("/restaurants/new")
def new_restaurant():
    return render_template("new_restaurant.html")

@app.route("/restaurants/create", methods = ["POST"])
def create_restaurant():
    if not Restaurant.validate(request.form):
        return redirect("/restaurants/new")

    data = {
        **request.form,
        "user_id": session["uuid"]
    }

    Restaurant.create(data)

    return redirect("/home")

@app.route("/restaurants/<int:id>")
def show_restaurant(id):
    return render_template("show_restaurant.html",
    user = User.get_by_id({"id": session['uuid']}),
    restaurant = Restaurant.get_one({"id": id})
    )

@app.route("/restaurants/<int:id>/edit")
def edit_restaurant(id):
    return render_template("edit_restaurant.html",
    restaurant = Restaurant.get_one({"id": id})
    )

@app.route("/restaurants/<int:id>/update", methods = ["POST"])
def update_restaurant(id):
    if not Restaurant.validate(request.form):
        return redirect(f"/restaurants/{id}/edit")

    data = {
    **request.form,
    "id": id
    }

    Restaurant.update(data)

    return redirect("/home")


@app.route("/restaurants/<int:id>/delete")
def delete_restaurant(id):
    Restaurant.delete({"id": id})

    return redirect("/home")