from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, validators

class NewUser(FlaskForm):
	email=StringField("Email", [validators.DataRequired(),
								validators.Length(min=3),
								validators.Email("Must be a valid email")])
	password=PasswordField("Password", [validators.DataRequired(),
										validators.Length(min=3),
										validators.EqualTo("confirm_password", message="Passwords must match")])
	confirm_password=PasswordField("Repeat Password")
	first_name = StringField("First Name", [validators.DataRequired(),
											validators.Length(min=1)])
	last_name = StringField("Last Name", [validators.DataRequired(),
										  validators.Length(min=1)])


class EditUser(FlaskForm):
	email=StringField("Email", [validators.DataRequired(),
								validators.Length(min=3),
								validators.Email("Must be a valid email")])
	password=PasswordField("Password", [validators.DataRequired(),
										validators.Length(min=3),
										validators.EqualTo("confirm_password", message="Passwords must match")])
	confirm_password = PasswordField("Repeat Password")
	first_name = StringField("First Name", [validators.DataRequired(),
											validators.Length(min=1)])
	last_name = StringField("Last Name", [validators.DataRequired(),
										  validators.Length(min=1)])
	phone_number = IntegerField('Number', [validators.Optional(),
										   validators.Length(min=10,max=10)])


class LoginUser(FlaskForm):
	email = StringField("Email", [validators.DataRequired(),
								  validators.Length(min=3),
								  validators.Email("Must be a valid email")])
	password = PasswordField("Password", [validators.DataRequired()])

