from __future__ import absolute_import, unicode_literals
from celery import Celery
from celery.schedules import crontab
import os

celery = Celery('proj',
             broker='redis://localhost:6379/0',
             backend='redis://localhost:6379/0',
             include=['project.tasks'])


celery.conf.beat_schedule={
	'my_periodic_task': {
		'task': 'project.tasks.test',
		'schedule': 10
	}

}

celery.conf.timezone = 'UTC'

# Optional configuration, see the application user guide.
celery.conf.update(
	result_expires=3600
)


if __name__ == '__main__':
    celery.start()


