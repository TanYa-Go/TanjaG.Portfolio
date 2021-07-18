import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)


app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


# @app.route("/skills")
# def skills():
#     skills = list(mongo.db.skills.find())
#     return render_template("index.html/", skills=skills)


@app.route("/")
@app.route("/index")
def index():
    skills = list(mongo.db.skills.find())
    try:
        username = mongo.db.users.find_one(
            {"username": session["user"]}
        )["username"]
    except:
        username = ''
    testimonials = mongo.db.testimonials.find()
    return render_template("index.html", skills=skills, username=username, testimonials=testimonials)


@app.route("/projects")
def projects():
    return render_template("projects.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if username already exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("Registration Successful!")
        return redirect(url_for("dashboard", username=session["user"]))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if username exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                flash("Welcome, {}".format(
                            request.form.get("username")))
                return redirect(url_for(
                            "dashboard", username=session["user"]))
            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/dashboard/<username>", methods=["GET", "POST"])
def dashboard(username):
    # grab the session user's username from db
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]

    if session["user"]:
        return render_template("dashboard.html", username=username)

    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    # remove user from session cookie
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


@app.route("/add_skill", methods=["GET", "POST"])
def add_skill():
    if request.method == "POST":
        files = request.files
        if 'image' not in files:
            return 'no image'
        image = files['image']
        path = f'static/uploads/{image.filename}'
        image.save(path)

        skill = {
            "category_title": request.form.get("category_title"),
            "skill_title": request.form.get("skill_title"),
            "image_path": path,
        }
        mongo.db.skills.insert_one(skill)
        flash("Skill Successfully Added")
        return redirect(url_for("add_skill"))

    categories = mongo.db.categories.find().sort("category_title", 1)
    return render_template("add_skill.html", categories=categories)


@app.route("/edit_skill/<skill_id>", methods=["GET", "POST"])
def edit_skill(skill_id):
    skill = mongo.db.skills.find_one({"_id": ObjectId(skill_id)})
    if request.method == "POST":
        new_values = {
            "category_title": request.form.get("category_title"),
            "skill_title": request.form.get("skill_title"),
        }
        files = request.files
        image = files['image']
        if image:
            path = f'static/uploads/{image.filename}'
            image.save(path)
            new_values["image_path"] = path

        new_values = {'$set': new_values}

        mongo.db.skills.update_one(skill, new_values)
        flash("Skill Successfully Updated")

        return redirect( url_for('edit_skill', skill_id=skill['_id']) )

    
    categories = mongo.db.categories.find().sort("category_name", 1)
    return render_template(
        "edit_skill.html", skill=skill, categories=categories)


@app.route("/delete_skill/<skill_id>")
def delete_skill(skill_id):
    mongo.db.skills.remove({"_id": ObjectId(skill_id)})
    flash("Skill Successfully Deleted")
    return redirect(url_for("add_skill"))



@app.route("/add_testimonial", methods=["GET", "POST"])
def add_testimonial():
    if request.method == "POST":
        files = request.files
        if 'image' not in files:
            return 'no image'
        image = files['image']
        path = f'static/uploads/{image.filename}'
        image.save(path)

        testimonial = {
            "user_name": request.form.get("user_name"),
            "testimonial_description": request.form.get(
                "testimonial_description"),
            "image_path": path,
        }
        mongo.db.testimonials.insert_one(testimonial)
        flash("Testimonial Successfully Added")
        return redirect(url_for("add_testimonial"))

    testimonials = mongo.db.testimonials.find()
    return render_template("add_testimonial.html", testimonials=testimonials)


@app.route("/edit_testimonial/<testimonial_id>", methods=["GET", "POST"])
def edit_testimonial(testimonial_id):
    testimonial = mongo.db.testimonials.find_one({"_id": ObjectId(testimonial_id)})
    if request.method == "POST":
        new_values = {
            "user_name": request.form.get("user_name"),
            "testimonial_description": request.form.get("testimonial_description"),
        }
        files = request.files
        image = files['image']
        if image:
            path = f'static/uploads/{image.filename}'
            image.save(path)
            new_values["image_path"] = path

        new_values = {'$set': new_values}

        mongo.db.testimonials.update_one(testimonial, new_values)
        flash("Testimonial Successfully Updated")

        return redirect(url_for('edit_testimonial', testimonial_id=testimonial['_id']) )

    
    return render_template(
        "edit_testimonial.html", testimonial=testimonial)


@app.route("/delete_testimonial/<testimonial_id>")
def delete_testimonial(testimonial_id):
    mongo.db.testimonials.remove({"_id": ObjectId(testimonial_id)})
    flash("Testimonial Successfully Deleted")
    return redirect(url_for("add_testimonial"))


@app.errorhandler(404)
def not_found_error(error):
    """
    Route to handle 404 error
    """
    return render_template('404.html', error=error), 404


@app.errorhandler(500)
def internal_error(error):
    """
    Route to handle 500 error
    """
    return render_template('500.html', error=error), 500


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
