from __future__ import absolute_import, unicode_literals
from project.celery import celery
from celery.schedules import crontab
import time
from flask_sqlalchemy import SQLAlchemy
from project import db
from project.locations.models import Location
from project.notifications.models import Notification
from project.users.models import User
from datetime import datetime
import os
from twilio.rest import TwilioRestClient 

celery_config={}
celery_config["TWILIO_ACCOUNT_SID"] = os.environ.get("TWILIO_ACCOUNT_SID")
celery_config['TWILIO_AUTH_TOKEN'] = os.environ.get('TWILIO_AUTH_TOKEN')
celery_config['TWILIO_PHONE_NUMBER'] = os.environ.get('TWILIO_PHONE_NUMBER')

client = TwilioRestClient(celery_config["TWILIO_ACCOUNT_SID"], celery_config['TWILIO_AUTH_TOKEN'])

@celery.task
def add(x, y):
	return x + y


@celery.task
def mul(x, y):
	# time.sleep(10)
	print(x*y)
	return x * y


@celery.task
def xsum(numbers):
	return sum(numbers)


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
	# Calls test('hello') every 10 seconds.
	# sender.add_periodic_task(10.0, test.s('hello'), name='add every 10')

	# Calls test('world') every 30 seconds
	# sender.add_periodic_task(30.0, test.s('world'), expires=10)
	# sender.add_periodic_task(30.0, test.s('world'), expires=10)

	# Executes every Monday morning at 7:30 a.m.
	# sender.add_periodic_task(
	# 	crontab(hour=7, minute=30, day_of_week=1),
	# 	test.s('Happy Mondays!'),
	# )
	pass


@celery.task
def test():

	found_locations=db.session.query(Notification.location.distinct().label("location"))
	notif_locations=[row.location for row in found_locations]
	locations_5day_forcast=[]
	for location in notif_locations:
		locations_5day_forcast.append(Location.get_5day_forecast(location))

	# print(notif_locations[0])
	# print(locations_5day_forcast[0]["city"]["name"])

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
			message=client.messages.create(
			    to=celery_config['TEMP_PHONE_NUMBER'],
			    from_=celery_config['TWILIO_PHONE_NUMBER'], 
			    body="This is your weather notification for {}. There will be {} in about {} day(s).".format(notif.location, notif.weather_type, notif.days_notice)
			)
			print(message)
			print("Notification is True")

		else:
			print("Notification is False")


	return notif_locations





