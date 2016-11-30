from flask import Flask, render_template, redirect, url_for
from flask_modus import Modus
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os
from flask_wtf.csrf import CsrfProtect
from flask_restful import Api, Resource, fields, marshal_with
from flask_jwt import JWT, jwt_required, current_identity

app = Flask(__name__)
bcrypt = Bcrypt(app)

login_manager=LoginManager()
login_manager.init_app(app)

if os.environ.get("ENV") == "production":
	debug=False
	app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
	app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL')

else:
	debug=True
	app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
	app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://localhost/weather_animator'
	app.config['APP_KEY'] = os.environ.get('APP_KEY')


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)
modus=Modus(app)
CsrfProtect(app)

login_manager.login_view = "users.login"


from project.users.models import User
from project.locations.models import Location
from project.notifications.models import Notification
from project.users.views import users_blueprint
from project.locations.views import locations_blueprint


app.register_blueprint(users_blueprint, url_prefix="/users")
app.register_blueprint(locations_blueprint, url_prefix="/users/<int:id>/locations")

@app.route("/")
def root():
	weather_data = Location.get_data("Denver")
	print(weather_data.)
	return render_template("index.html", data=weather_data)


@app.errorhandler(404)
def page_not_found(e):
	return render_template("404.html"), 404


@login_manager.user_loader
def load_user(user_id):
	return User.query.get(user_id)

