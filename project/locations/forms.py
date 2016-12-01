from flask_wtf import FlaskForm
from wtforms import StringField, validators

class NewLocation(FlaskForm):
	new_location = StringField("Location", [validators.Length(min=1, max=100)])


class EditLocation(FlaskForm):
	location = StringField("Location", [validators.Length(min=1, max=100)])


class SearchLocationPublic(FlaskForm):
	location = StringField("Location", [validators.DataRequired(),
										validators.Length(min=1, max=50)])