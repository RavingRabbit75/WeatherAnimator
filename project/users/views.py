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





