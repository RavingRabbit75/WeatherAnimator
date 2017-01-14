from flask_wtf import FlaskForm
from wtforms import SelectField

class NotificationForm(FlaskForm):
	condition = SelectField("Weather Condition", 
							 choices=[("rain", "Rain"), 
							 ("snow", "Snow"),
							 ("clear", "Clear Skies")])

	days_notice = SelectField("Days Notice",
							   choices=[("1", "1 Day"),
							   ("2", "2 Days"),
							   ("3", "3 Days"),
							   ("4", "4 Days"),
							   ("5", "5 Days")])


# class EditNotification(FlaskForm):
# 	location = StringField("Location", [validators.Length(min=1, max=100)])

