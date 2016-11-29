from project import db
from datetime import datetime

class Notification(db.Model):
	__tablename__ = "notifications"

	id=db.Column(db.Integer, primary_key=True)
	weather_type=db.Column(db.Text)
	user_id=db.Column(db.Integer, db.ForeignKey("users.id"))

	def __init__(self, weather_type, user_id):
		self.weather_type = weather_type
		self.user_id = user_id

	def __repr__(self):
		return "{} notification for user {}.".format(self.weather_type, self.user_id)