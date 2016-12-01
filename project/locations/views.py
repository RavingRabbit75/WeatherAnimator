from flask import Flask, render_template, redirect, request, url_for, Blueprint
from flask_modus import Modus
from flask_sqlalchemy import SQLAlchemy

from project import db
from project.locations.models import Location
from project.locations.forms import NewLocation
from project.users.models import User


locations_blueprint = Blueprint("locations", __name__,template_folder="templates")


@locations_blueprint.route("/", methods=["GET","POST"])
def index(id):
	found_locations=User.query.get_or_404(id).locations.all()
	found_user=User.query.get(id)

	if request.method=="POST":
		new_location=Location(request.form["new_location"],id)
		db.session.add(new_location)
		db.session.commit()
		return redirect(url_for("locations.index", id=id))

	return render_template("locations/index.html", locations=found_locations, user=found_user)



@locations_blueprint.route("/new")
def locations_new(id):
	found_user=User.query.get(id)
	form=NewLocation()

	return render_template("locations/new.html", user=found_user, form=form, errors="")


@locations_blueprint.route("/<int:location_id>", methods=["GET", "PATCH", "DELETE"])
def locations_show(id, location_id):
	found_location=Location.query.get_or_404(location_id)

	if request.method == b"DELETE":
		db.session.delete(found_location)
		db.session.commit()
		return redirect(url_for('locations.index', id=id))

	if request.method == "GET":
		location_current=Location.get_current_weather(found_location.location)
		location_forecast=Location.get_5day_forecast(found_location.location)
		found_user=User.query.get_or_404(id)

		current_temp=str(Location.kelvin_to_fahrenheit(location_current["main"]["temp"]))+"°F"
		current_condition=location_current["weather"][0]["description"]
		icon_bitmap= Location.get_icon_type(location_current["weather"][0]["icon"])

	return render_template("locations/show.html", location=found_location,
												  current=location_current,
												  forecast=location_forecast,
												  current_temp=current_temp,
												  current_condition=current_condition,
												  icon_bitmap=icon_bitmap,
												  user=found_user)








