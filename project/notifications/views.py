from flask import Flask, render_template, redirect, request, url_for, Blueprint, session, g
from flask_modus import Modus
from flask_sqlalchemy import SQLAlchemy

from flask_login import login_user, logout_user, login_required
from functools import wraps

from project import db
from project.locations.models import Location
from project.locations.forms import NewLocation
from project.users.models import User
from project.notifications.models import Notification


notifications_blueprint = Blueprint("notifications", __name__,template_folder="templates")


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


@notifications_blueprint.route("/", methods=["GET","POST"])
@ensure_loggied_in
@ensure_correct_user
def index(id,loc_id):
	found_notifications=Notification.query.all()
	found_location=Location.query.get_or_404(loc_id)
	found_user=User.query.get(id)
	return render_template("notifications/index.html", notifications=found_notifications, 
													   location=found_location, 
													   user=found_user)


@ensure_loggied_in
@ensure_correct_user
@notifications_blueprint.route("/new")
def notifications_new(id):
	return "new notification"



@notifications_blueprint.route("/<int:location_id>", methods=["GET", "PATCH", "DELETE"])
@ensure_loggied_in
@ensure_correct_user
def notificatons_show(id, location_id):
	return "show notification"



@notifications_blueprint.route("/<int:notif_id>/edit")
@login_required
@ensure_correct_user
def edit(id, loc_id, notif_id):
	print(id, loc_id)
	# found_user=User.query.get(id)
	# form=EditUser(request.form)
	return render_template("notifications/edit.html")





