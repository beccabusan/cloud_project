from celery import Celery
celery=Celery()
celery.config_from_object('masterconf')
from svmscript import work
work.delay(15,30,5,5,0)

