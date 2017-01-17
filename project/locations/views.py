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


locations_blueprint = Blueprint("locations", __name__,template_folder="templates")


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


@locations_blueprint.route("/", methods=["GET","POST"])
@ensure_loggied_in
@ensure_correct_user
def index(id):
	found_locations=User.query.get_or_404(id).locations.all()
	found_user=User.query.get(id)
	if request.method=="POST":
		new_location=Location(request.form["new_location"],id)
		db.session.add(new_location)
		db.session.commit()
		return redirect(url_for("locations.index", id=id))

	return render_template("locations/index.html", locations=found_locations, user=found_user)


@ensure_loggied_in
@ensure_correct_user
@locations_blueprint.route("/new")
def locations_new(id):
	found_user=User.query.get(id)
	form=NewLocation()

	return render_template("locations/new.html", user=found_user, form=form, errors="")



@locations_blueprint.route("/<int:location_id>", methods=["GET", "PATCH", "DELETE"])
@ensure_loggied_in
@ensure_correct_user
def locations_show(id, location_id):
	found_location=Location.query.get_or_404(location_id)

	if request.method == b"DELETE":
		found_notifications=Notification.query.filter_by(location_id=location_id).all()
		for notification in found_notifications:
			db.session.delete(notification)

		db.session.commit()
	
		db.session.delete(found_location)
		db.session.commit()
		return redirect(url_for('locations.index', id=id))

	if request.method == "GET":
		location_current=Location.get_current_weather(found_location.location)
		location_forecast=Location.get_5day_forecast(found_location.location)
		found_user=User.query.get_or_404(id)

		current_temp=str(Location.kelvin_to_fahrenheit(location_current["main"]["temp"]))+"°F"
		current_condition=location_current["weather"][0]["description"].title()
		icon_bitmap= Location.get_icon_type(location_current["weather"][0]["icon"])

		humidity=location_current["main"]["humidity"]
		pressure=location_current["main"]["pressure"]
		wind_speed=location_current["wind"]["speed"]
		if "deg" in location_current["wind"]:
			wind_dir=location_current["wind"]["deg"]
		else:
			wind_dir="0"
		
		
		tz_id=Location.get_timezone(location_current["coord"]["lat"],location_current["coord"]["lon"])
		sunrise_time = Location.utc_unix_to_readable(location_current["sys"]["sunrise"], tz_id)
		sunset_time = Location.utc_unix_to_readable(location_current["sys"]["sunset"], tz_id)
		wdata = Location.day_or_night(location_current["sys"]["sunrise"], location_current["sys"]["sunset"], tz_id)
		w_code = location_current["weather"][0]["id"] 


	return render_template("locations/show.html", location=found_location,
												  current=location_current,
												  forecast=location_forecast,
												  current_temp=current_temp,
												  current_condition=current_condition,
												  icon_bitmap=icon_bitmap,
												  humidity=humidity,
												  pressure=pressure,
												  wind_speed=wind_speed,
												  wind_dir=wind_dir,
												  sunrise_time=sunrise_time,
												  sunset_time=sunset_time,
												  user=found_user,
												  wdata=wdata,
												  w_code=w_code)








