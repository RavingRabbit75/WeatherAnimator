from flask import Flask, render_template, redirect, request, url_for, Blueprint, session, g
from flask_modus import Modus
from flask_sqlalchemy import SQLAlchemy

from flask_login import login_user, logout_user, login_required
from functools import wraps

from project import db
from project.locations.models import Location
from project.users.models import User
from project.notifications.models import Notification
from project.notifications.forms import NotificationForm


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
def index(id, loc_id):
	found_notifications=Notification.query.all()
	found_location=Location.query.get_or_404(loc_id)
	found_user=User.query.get(id)

	if request.method=="POST":
		new_notification=Notification(found_location.location, 
									  request.form["condition"], 
									  request.form["days_notice"],
									  loc_id, id)
		db.session.add(new_notification)
		db.session.commit()
		return redirect(url_for("notifications.index", id=id, loc_id=loc_id))


	return render_template("notifications/index.html", notifications=found_notifications, 
													   location=found_location, 
													   user=found_user)


@ensure_loggied_in
@ensure_correct_user
@notifications_blueprint.route("/new")
def new(id, loc_id):
	form=NotificationForm()
	found_location=Location.query.get_or_404(loc_id)
	found_user=User.query.get(id)
	return render_template("notifications/new.html", form=form, 
													 user=found_user, 
													 location=found_location)



@notifications_blueprint.route("/<int:notif_id>", methods=["GET", "PATCH", "DELETE"])
@ensure_loggied_in
@ensure_correct_user
def show(id, loc_id, notif_id):
	found_notification=Notification.query.get_or_404(notif_id)
	found_location=Location.query.get_or_404(loc_id)
	found_user=User.query.get_or_404(id)
	form=NotificationForm(request.form)

	if found_user==None:
		return render_template("404.html"), 404

	if request.method==b"PATCH":
		found_notification.weather_type=request.form["condition"];
		found_notification.days_notice=request.form["days_notice"];
		db.session.add(found_notification)
		db.session.commit()
		return redirect(url_for("notifications.index", id=found_user.id, loc_id=found_location.id))

	# if request.method==b"DELETE":
	# 	db.session.delete(found_notification)
	# 	db.session.commit()
	# 	return redirect("/")

	return redirect(url_for("notifications.index", id=found_user.id, loc_id=found_location.id))



@notifications_blueprint.route("/<int:notif_id>/edit")
@login_required
@ensure_correct_user
def edit(id, loc_id, notif_id):
	found_user=User.query.get(id)
	found_location=Location.query.get_or_404(loc_id)
	found_notification=Notification.query.get_or_404(notif_id)

	form=NotificationForm(condition=found_notification.weather_type, 
						  days_notice=found_notification.days_notice)
	
	return render_template("notifications/edit.html", form=form,
													  user=found_user,
													  location=found_location,
													  notification=found_notification)





