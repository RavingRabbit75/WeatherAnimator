from project import db
from datetime import datetime

class Notification(db.Model):
	__tablename__ = "notifications"

	id=db.Column(db.Integer, primary_key=True)
	location=db.Column(db.Text)
	weather_type=db.Column(db.Text)
	days_notice=db.Column(db.Integer) # Max 5 days
	location_id=db.Column(db.Integer, db.ForeignKey("locations.id"))
	user_id=db.Column(db.Integer, db.ForeignKey("users.id"))


	def __init__(self, location, weather_type, days_notice, user_id):
		self.location = location
		self.weather_type = weather_type
		self.days_notice = days_notice
		self.user_id = user_id


	def __repr__(self):
		return "{} notification for user {}.".format(self.location, 
													 self.weather_type, 
													 self.days_notice, 
													 self.user_id)