from __future__ import absolute_import, unicode_literals
from project.celery import celery
from project import db
from project.locations.models import Location
from project.notifications.models import Notification
from project.users.models import User
from datetime import datetime
import os
from twilio.rest import TwilioRestClient 

twilio_config={}
twilio_config["TWILIO_ACCOUNT_SID"] = os.environ.get("TWILIO_ACCOUNT_SID")
twilio_config['TWILIO_AUTH_TOKEN'] = os.environ.get('TWILIO_AUTH_TOKEN')
twilio_config['TWILIO_PHONE_NUMBER'] = os.environ.get('TWILIO_PHONE_NUMBER')

client = TwilioRestClient(twilio_config["TWILIO_ACCOUNT_SID"], twilio_config['TWILIO_AUTH_TOKEN'])


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
	pass


@celery.task
def check_notifications():

	found_locations=db.session.query(Notification.location.distinct().label("location"))
	notif_locations=[row.location for row in found_locations]
	locations_5day_forcast=[]
	for location in notif_locations:
		locations_5day_forcast.append(Location.get_5day_forecast(location))


	notifs_to_check=Notification.query.all()
	# 10800 seconds = 3 hours
	# 1 day = 86400 seconds
	current_utc=datetime.utcnow().timestamp()
	
	def check_notification(location, weather_type, days_notice):
		idx=notif_locations.index(location)
		utc_to_check=current_utc+(days_notice*86400)

		for forecast_3hour_slot in locations_5day_forcast[idx]["list"]:
			if utc_to_check>=forecast_3hour_slot["dt"]:
				found_forecast_3hour_slot=forecast_3hour_slot
				break

		print(found_forecast_3hour_slot["weather"][0]["main"].lower(), weather_type.lower())
		if found_forecast_3hour_slot["weather"][0]["main"].lower()==weather_type.lower():
			return True

		return False


	for notif in notifs_to_check:

		if check_notification(notif.location, notif.weather_type, notif.days_notice):
			found_user=User.query.get(notif.user_id)
			if found_user.phone_number:
				message=client.messages.create(
				    to="+1"+found_user.phone_number,
				    from_=twilio_config['TWILIO_PHONE_NUMBER'], 
				    body="Hello {}. This is your weather notification for {}. There will be {} in about {} day(s).".format(found_user.first_name,
				    																									   notif.location, 
				    																									   notif.weather_type, 
				    																									   notif.days_notice)
				)
				print(message)
			else:
				print("No phone number for {}".format(found_user.first_name))

		else:
			print("Notification is False")


	return notif_locations





