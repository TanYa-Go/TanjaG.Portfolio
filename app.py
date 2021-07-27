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


@app.route("/")
def index():
    """
    Renders index page template when going to the main website link
    """
    try:
        skills = list(mongo.db.skills.find())
        user = mongo.db.users.find_one({"username": session.get("user")}) or {}
        username = user.get('username')
        is_admin = user.get('is_admin')
        testimonials = mongo.db.testimonials.find()
    except Exception:
        print("An error occurred loading the index.")

    host = request.host
    if 'gitpod' in host:
        cdn = ''
    else:
        cdn = 'https://dyw7dciygqjtx.cloudfront.net'

    return render_template(
        "pages/index.html", skills=skills, username=username,
        is_admin=is_admin, testimonials=testimonials, cdn=cdn)


@app.route("/register", methods=["GET", "POST"])
def register():
    """
    Register page, allows users to register for an account
    if username doesn't already exist.
    """
    if request.method == "POST":

        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        try:
            mongo.db.users.insert_one(register)
        except Exception:
            flash("An error occurred. Contact site admin.")

        # put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("Registration Successful!")
        return redirect(url_for("dashboard", username=session["user"]))

    return render_template("pages/register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Checks users collection for user and password to allow registered
    users to log in. Redirects to user's dashboard on successful sign in.
    """
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

    return render_template("pages/login.html")


@app.route("/dashboard/<username>", methods=["GET", "POST"])
def dashboard(username):
    """
    If username exists in the database, render dashboard page
    """
    try:
        user = mongo.db.users.find_one({"username": session["user"]})
        username = user.get('username')
        is_admin = user.get('is_admin')

        if session["user"]:
            return render_template(
                "pages/dashboard.html", username=username, is_admin=is_admin)

    except Exception:
        flash("An error occurred. Contact site admin.")

    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    """
    Removes logged in user from session cookie and
    returns them to the log in page.
    """
    flash("You have been logged out")
    try:
        session.pop("user")
    except Exception:
        pass
    return redirect(url_for("login"))


@app.route("/add_skill", methods=["GET", "POST"])
def add_skill():
    """
    Gets values from add skill form and stores values
    into MongoDB collection skills.
    """
    if request.method == "POST":

        user = mongo.db.users.find_one({"username": session["user"]})
        username = user.get('username')

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
            "created_by": username,
        }

        try:
            mongo.db.skills.insert_one(skill)
            flash("Skill Successfully Added")
        except Exception:
            flash("An error occurred. Contact site admin.")

        return redirect(url_for("add_skill"))

    categories = mongo.db.categories.find().sort("category_title", 1)
    return render_template(
        "pages/add_edit_skill.html", categories=categories, edit=False)


@app.route("/edit_skill/<skill_id>", methods=["GET", "POST"])
def edit_skill(skill_id):
    """
    Allows user to edit a skill. If successful, flash message is displayed
    to alert user.
    """
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

        try:
            mongo.db.skills.update_one(skill, new_values)
            flash("Skill Successfully Updated")
        except Exception:
            flash("An error occurred. Contact site admin.")

        return redirect(url_for('edit_skill', skill_id=skill['_id']))

    categories = mongo.db.categories.find().sort("category_name", 1)
    return render_template(
        "pages/add_edit_skill.html", skill=skill, categories=categories,
        edit=True)


@app.route("/delete_skill/<skill_id>")
def delete_skill(skill_id):
    """
    Allows user to delete a skill and redirects user to add skill page.
    Flash message alerts user that delete was successful.
    """
    try:
        mongo.db.skills.remove({"_id": ObjectId(skill_id)})
        flash("Skill Successfully Deleted")
    except Exception:
        flash("An error occurred. Contact site admin.")

    return redirect(url_for("add_skill"))


@app.route("/add_testimonial", methods=["GET", "POST"])
def add_testimonial():
    """
    Gets values from add testimonial form and stores values
    into MongoDB collection testimonials.
    """
    if request.method == "POST":
        files = request.files
        if 'image' not in files:
            return 'no image'
        image = files['image']

        path = f'static/uploads/{image.filename}'
        image.save(path)

        try:
            user = mongo.db.users.find_one(
                {"username": session.get("user")}) or {}
            username = user.get('username')
            is_admin = user.get('is_admin')

            testimonial = {
                "user_name": request.form.get("user_name"),
                "testimonial_description": request.form.get(
                    "testimonial_description"),
                "image_path": path,
                "created_by": username,
            }
            try:
                mongo.db.testimonials.insert_one(testimonial)
                flash("Testimonial Successfully Added")
            except Exception:
                flash("An error occurred. Contact site admin.")

        except Exception:
            print("An error occurred loading the index.")

        return redirect(url_for("add_testimonial"))

    testimonials = mongo.db.testimonials.find()
    return render_template(
        "pages/add_testimonial.html", testimonials=testimonials)


@app.route("/edit_testimonial/<testimonial_id>", methods=["GET", "POST"])
def edit_testimonial(testimonial_id):
    """
    Allows user to edit a testimonial. If successful, flash message is
    displayed to alert user.
    """
    testimonial = mongo.db.testimonials.find_one(
        {"_id": ObjectId(testimonial_id)})
    if request.method == "POST":
        new_values = {
            "user_name": request.form.get("user_name"),
            "testimonial_description": request.form.get(
                "testimonial_description"),
        }
        files = request.files
        image = files['image']
        if image:
            path = f'static/uploads/{image.filename}'
            image.save(path)
            new_values["image_path"] = path

        new_values = {'$set': new_values}
        try:
            mongo.db.testimonials.update_one(testimonial, new_values)
            flash("Testimonial Successfully Updated")
        except Exception:
            flash("An error occurred. Contact site admin.")

        return redirect(url_for(
            'edit_testimonial', testimonial_id=testimonial['_id']))

    return render_template(
        "pages/edit_testimonial.html", testimonial=testimonial)


@app.route("/delete_testimonial/<testimonial_id>")
def delete_testimonial(testimonial_id):
    """
    Allows user to delete a testimonial and redirects
    user to add testimonial page. Flash message alerts user
    that delete was successful.
    """
    try:
        mongo.db.testimonials.remove({"_id": ObjectId(testimonial_id)})
        flash("Testimonial Successfully Deleted")
    except Exception:
        flash("An error occurred. Contact site admin.")

    return redirect(url_for("add_testimonial"))


@app.errorhandler(404)
def not_found_error(error):
    """
    Route to handle 404 error
    """
    return render_template('pages/404.html', error=error), 404


@app.errorhandler(500)
def internal_error(error):
    """
    Route to handle 500 error
    """
    return render_template('pages/500.html', error=error), 500


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
