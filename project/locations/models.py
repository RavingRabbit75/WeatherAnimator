from project import db
from datetime import datetime
import moment
import arrow
import requests
import time
from project import app

class Location(db.Model):
	__tablename__ = "locations"

	id=db.Column(db.Integer, primary_key=True)
	location=db.Column(db.Text)
	last_updated=db.Column(db.DateTime, default=datetime.utcnow)
	user_id=db.Column(db.Integer, db.ForeignKey("users.id"))

	def __init__(self, location, user_id):
		self.location = location
		self.user_id = user_id


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
		path = "/static/images/weather_icons/"
		return path+icon_value+".png"


	def get_timezone(_lat, _lon):
		timestamp = str(time.time())
		lat = str(_lat)
		lon = str(_lon)
		r = requests.get("https://maps.googleapis.com/maps/api/timezone/json?location="+lat+","+lon+"&timestamp="+timestamp+"&key="+app.config['GOOGLETIMEZONE_KEY'])
		return r.json()["timeZoneId"]


	def get_dayOfWeek(utc_time, tz_id):
		momentObj= moment.unix(utc_time, utc=True).timezone(tz_id)
		return momentObj.format('dddd')

	def get_hour(utc_time, tz_id):
		momentObj= moment.unix(utc_time, utc=True).timezone(tz_id)
		return momentObj.format('HH')

	def utc_unix_to_readable(utc_time, tz_id):
		momentObj= moment.unix(utc_time, utc=True).timezone(tz_id)
		time_string = momentObj.format("h:mm A")
		return time_string


	def day_or_night(ts_sunrise, ts_sunset, tz_id):
		ts_current = arrow.utcnow()
		if ts_current.timestamp > ts_sunrise and ts_current.timestamp < ts_sunset:
			return "day"

		return "night"


	





