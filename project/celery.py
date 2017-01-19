from __future__ import absolute_import, unicode_literals
from celery import Celery
from celery.schedules import crontab
import os

celery_config={}
if os.environ.get("ENV") == "production":
	celery_config["CELERY_BROKER"] = os.environ.get("CELERY_BROKER")
	celery_config['CELERY_BACKEND'] = os.environ.get("CELERY_BACKEND")

else:
	celery_config["CELERY_BROKER"] = 'redis://localhost:6379/0'
	celery_config['CELERY_BACKEND'] = 'redis://localhost:6379/0'


celery = Celery('proj',
             broker=celery_config["CELERY_BROKER"],
             backend=celery_config['CELERY_BACKEND'],
             include=['project.tasks'])

celery.conf.beat_schedule={
	'my_periodic_task': {
		'task': 'project.tasks.check_notifications',
		'schedule': crontab(minute=17, hour='4,16') # checks and sends notifs at 4am and 4pm GMT (or 8am & 8pm Pacific time)
	}

}

celery.conf.timezone = 'UTC'

# Optional configuration, see the application user guide.
celery.conf.update(
	result_expires=3600
)


if __name__ == '__main__':
    celery.start()


