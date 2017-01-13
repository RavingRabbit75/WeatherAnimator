from __future__ import absolute_import, unicode_literals
from project.celery import celery
from celery.schedules import crontab
import time
from flask_sqlalchemy import SQLAlchemy
from project import db
from project.locations.models import Location


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
	found_location=Location.query.get_or_404(6)
	location_current=Location.get_current_weather(found_location.location)

	return location_current