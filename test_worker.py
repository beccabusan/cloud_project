from celery import Celery
celery=Celery()
celery.config_from_object('masterconf')
from svmscript import work
work.delay(0,180,18,5,0)

