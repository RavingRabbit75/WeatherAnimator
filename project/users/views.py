from flask import Flask, render_template, redirect, request, url_for, Blueprint, session, flash, g
from flask_modus import Modus
from flask_sqlalchemy import SQLAlchemy

from project import db,bcrypt

from sqlalchemy.exc import IntegrityError
from flask_login import login_user, logout_user, login_required
from functools import wraps

from project.users.models import User
from project.locations.models import Location
from project.notifications.models import Notification
from project.users.forms import NewUser, EditUser, LoginUser

users_blueprint = Blueprint("users", __name__, template_folder="templates")


def ensure_correct_user(fn):
	@wraps(fn)
	def wrapper(*args, **kwargs):
		if kwargs.get("id") != int(session.get("user_id")):
			return redirect(url_for("users.show", id=g.current_user.id))

		return fn(*args, **kwargs)

	return wrapper

def ensure_loggied_in(fn):
	@wraps(fn)
	def wrapper(*args, **kwargs):
		if not session.get("user_id"):
			return redirect(url_for("users.login"))
		return fn(*args, **kwargs)
	return wrapper


@users_blueprint.route("/", methods=["GET", "POST"])
def index():
	form = NewUser(request.form)
	if request.method=="POST" and form.validate():
		new_user=User(request.form["email"],
					  request.form["password"],
					  request.form["first_name"],
					  request.form["last_name"])
		db.session.add(new_user)
		db.session.commit()
	elif request.method=="POST":
		error_found=next(iter(form.errors.values()))[0]
		return render_template("users/signup.html", form=form, error=error_found)


	return redirect("/")


@users_blueprint.route("/<int:id>", methods=["GET", "PATCH", "DELETE"])
@ensure_loggied_in
@ensure_correct_user
def show(id):
	found_user=User.query.get_or_404(id)
	form=EditUser(request.form)

	if found_user==None:
		return render_template("404.html"), 404

	if request.method==b"PATCH" and form.validate():
		found_user.email=request.form["email"]
		found_user.password=bcrypt.generate_password_hash(request.form["password"]).decode("UTF-8")
		found_user.first_name=request.form["first_name"];
		found_user.last_name=request.form["last_name"];
		db.session.add(found_user)
		db.session.commit()
		return redirect(url_for("users.index"))

	if request.method==b"PATCH":
		error_found=next(iter(form.errors.values()))[0]
		return render_template("users/edit.html", user=found_user, form=form, error=error_found)

	if request.method==b"DELETE":
		found_locations=Location.query.filter_by(user_id=id).all()
		found_notifications=Notification.query.filter_by(user_id=id).all()
		for notification in found_notifications:
			db.session.delete(notification)

		db.session.commit()
		for location in found_locations:
			db.session.delete(location)

		db.session.commit()
		db.session.delete(found_user)
		db.session.commit()
		return redirect("/")

	return redirect(url_for("locations.index", id=found_user.id))


@users_blueprint.route("/<int:id>/edit")
@login_required
@ensure_correct_user
def edit(id):
	found_user=User.query.get(id)
	form=EditUser(request.form)
	return render_template("users/edit.html", user=found_user, form=form)


@users_blueprint.route("/signup", methods=["GET", "POST"])
def signup():
	form=NewUser()

	if request.method=="POST":
		if form.validate_on_submit():
			try:
				new_user=User(request.form["email"],
							  request.form["password"],
							  request.form["first_name"],
							  request.form["last_name"])
				db.session.add(new_user)
				db.session.commit()
				login_user(new_user)
			except IntegrityError as e:
				error_found="Email alreadyin use."
				return render_template("users/signup.html", form=form, error=error_found)

			return redirect(url_for("locations.index", id=new_user.id))

		return render_template("users/signup.html", form=form)

	return render_template("users/signup.html", form=form)


@users_blueprint.route("/login", methods=["GET","POST"])
def login():
    form = LoginUser()
    if request.method=="POST" and form.validate():
        found_user = User.query.filter_by(email = form.email.data).first()
        if found_user:
            authenticated_user = bcrypt.check_password_hash(found_user.password, request.form['password'])
            if authenticated_user:
                login_user(found_user)
                return redirect(url_for("locations.index", id=found_user.id))
            else:
                error_found="Incorrect Password"
                return render_template("users/login.html", form=form, error=error_found)

        else:
            error_found="No Such User"
            return render_template("users/login.html", form=form, error=error_found)


    if request.method=="POST":
        error_found=next(iter(form.errors.values()))[0]
        return render_template("users/login.html", form=form, error=error_found)

    if request.method=="GET":
        return render_template("users/login.html", form=form, error="")




@users_blueprint.route("/logout")
def logout():
    session.pop("user_id", None)
    flash("You have been signed out.")
    return redirect(url_for("users.login"))


@users_blueprint.before_request
def current_user():
    if session.get("user_id"):
        g.current_user=User.query.get(session["user_id"])
    else:
        g.current_user = None





