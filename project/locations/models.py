from project import db
from datetime import datetime
import requests
from project import app

class Location(db.Model):
	__name__ = "locations"

	id=db.Column(db.Integer, primary_key=True)
	location=db.Column(db.Text)
	last_updated=db.Column(db.DateTime, default=datetime.utcnow)
	user_id=db.Column(db.Integer, db.ForeignKey("users.id"))

	def __init__(self, location, user_id):
		self.location = location
		self.user_id


	def __repr__(self):
		return "Location: {} was last updated {}.".format(self.location, self.last_updated)


	def get_current_weather(city):
		searchText = city
		r = requests.get("http://api.openweathermap.org/data/2.5/weather?q="+searchText+"&APPID="+app.config['APP_KEY'])
		return r.json()


	def get_5day_forecast(city):
		searchText = city
		r = requests.get("http://api.openweathermap.org/data/2.5/forecast?q="+searchText+"&APPID="+app.config['APP_KEY'])
		return r.json()
		

	def kelvin_to_fahrenheit(temp_in_K):
		temp_in_F = (9/5)*(temp_in_K-273)+32
		return round(temp_in_F)


	def get_icon_type(icon_value):
		path = "static/images/weather_icons/"
		return path+icon_value+".png"