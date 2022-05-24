from flask import render_template, redirect, request, session

from flask_app import app
from flask_app.models.model_user import User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)


@app.route("/")
def index():
    if "uuid" in session:
        return redirect("/home")

    return render_template("login.html")

@app.route("/user/create", methods = ["post"])
def register():
    if not User.register_validator(request.form):
        return redirect("/")

    hash_pass = bcrypt.generate_password_hash(request.form['password'])
    data ={
        **request.form,
        "password": hash_pass
    }

    user_id = User.create(data)
    
    session["uuid"] = user_id

    return redirect("/home")



@app.route("/login", methods = ["post"])
def login():
    if not User.login_validator(request.form):
        return redirect("/")

    user = User.get_by_email({"email": request.form["email"]})
    session["uuid"] = user.id
    return redirect("/home")


@app.route("/logout")
def logout():
    del session["uuid"]

    return redirect("/")

