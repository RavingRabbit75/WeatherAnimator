from project import db, bcrypt
from flask_login import UserMixin

class User(db.Model, UserMixin):
	__tablename__ = "users"

	id=db.Column(db.Integer, primary_key=True)
	email=db.Column(db.Text, unique=True)
	password=db.Column(db.Text)
	first_name=db.Column(db.Text)
	last_name=db.Column(db.Text)
	locations=db.relationship("Location", backref="user", lazy="dynamic")

	def __init__(self, email, password, first_name, last_name):
		self.email = email
		self.password = bcrypt.generate_password_hash(password).decode("UTF-8")
		self.first_name = first_name
		self.last_name = last_name


	def __repr__(self):
		return "User {} is {} {}.".format(self.email, self.first_name, self.last_name)


	def update_password(self, password):
		self.password=bcrypt.generate_password_hash(password).decode("UTF-8")


	