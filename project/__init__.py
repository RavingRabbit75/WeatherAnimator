from flask import Flask, render_template, redirect, url_for, request, json
from flask_modus import Modus
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os
from flask_wtf.csrf import CsrfProtect
from flask_restful import Api, Resource, fields, marshal_with
from flask_jwt import JWT, jwt_required, current_identity

from celery import Celery
from flask_mail import Mail, Message

app = Flask(__name__)
bcrypt = Bcrypt(app)

login_manager=LoginManager()
login_manager.init_app(app)

if os.environ.get("ENV") == "production":
	debug=False
	app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
	app.config['APP_KEY'] = os.environ.get('APP_KEY')
	app.config['GOOGLETIMEZONE_KEY'] = os.environ.get('GOOGLETIMEZONE_KEY')
	app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL')

else:
	debug=True
	app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
	app.config['APP_KEY'] = os.environ.get('APP_KEY')
	app.config['GOOGLETIMEZONE_KEY'] = os.environ.get('GOOGLETIMEZONE_KEY')
	app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://localhost/weather_animator'
	app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
	app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
	app.config['MAIL_SERVER']='smtp.gmail.com'
	app.config['MAIL_PORT'] = 465
	app.config['MAIL_USE_SSL'] = True
	app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
	app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)
modus=Modus(app)
CsrfProtect(app)

mail= Mail(app)
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

login_manager.login_view = "users.login"


from project.users.models import User
from project.locations.models import Location
from project.notifications.models import Notification
from project.users.views import users_blueprint
from project.locations.views import locations_blueprint
from project.locations.forms import SearchLocationPublic


app.register_blueprint(users_blueprint, url_prefix="/users")
app.register_blueprint(locations_blueprint, url_prefix="/users/<int:id>/locations")

@app.route("/")
def root():
	# msg = Message('Get Rich Quick Scheme', 
	# 	sender='mightyturtle75@gmail.com',
	# 	recipients=['me@raychow.com'])
	# msg.body="Click this link to get rich quick!"
	# msg.html = '<b>HTML</b> body'
	# mail.send(msg)
	return render_template("index.html")


@app.route("/demo")
def demo():
	# found_locations=User.query.get_or_404(id).locations.all()
	# found_user=User.query.get(id)
	found_locations=["Light Snow", 
					 "Heavy Snow", 
					 "Light Rain", 
					 "Heavy Rain", 
					 "Thunder with Light Rain",
					 "Thunder with Heavy Rain",
					 "Clouds"]
	print(found_locations[0])
	return render_template("locations/demo.html", locations=found_locations)


@app.route("/demo/<int:location_id>", methods=["GET"])
def demo_show(location_id):
	SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
	if location_id == 1:
		json_url = os.path.join(SITE_ROOT, "static/demo_json", "snow_light.json")
		
	if location_id == 2:
		json_url = os.path.join(SITE_ROOT, "static/demo_json", "snow_heavy.json")

	if location_id == 3:
		json_url = os.path.join(SITE_ROOT, "static/demo_json", "rain_light.json")

	if location_id == 4:
		json_url = os.path.join(SITE_ROOT, "static/demo_json", "rain_heavy.json")

	if location_id == 5:
		json_url = os.path.join(SITE_ROOT, "static/demo_json", "thunderRain_light.json")

	if location_id == 6:
		json_url = os.path.join(SITE_ROOT, "static/demo_json", "thunderRain_heavy.json")

	if location_id == 7:
		json_url = os.path.join(SITE_ROOT, "static/demo_json", "clouds.json")


	found_location=json.load(open(json_url))

	if request.method == "GET":
		location_current=found_location
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


	return render_template("locations/demo_show.html", location=found_location,
												  current=location_current,
												  current_temp=current_temp,
												  current_condition=current_condition,
												  icon_bitmap=icon_bitmap,
												  humidity=humidity,
												  pressure=pressure,
												  wind_speed=wind_speed,
												  wind_dir=wind_dir,
												  sunrise_time=sunrise_time,
												  sunset_time=sunset_time,
												  wdata=wdata,
												  w_code=w_code)



@app.errorhandler(404)
def page_not_found(e):
	return render_template("404.html"), 404


@login_manager.user_loader
def load_user(user_id):
	return User.query.get(user_id)











