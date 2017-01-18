from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators

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

	# requried format (U.S. numbers only so far): ###-###-####
	phone_number = StringField('Phone Number', [validators.Optional(),
												validators.Regexp('\d{3}-\d{3}-\d{4}', message="Entry must a valid U.S. phone number")])


class LoginUser(FlaskForm):
	email = StringField("Email", [validators.DataRequired(),
								  validators.Length(min=3),
								  validators.Email("Must be a valid email")])
	password = PasswordField("Password", [validators.DataRequired()])

