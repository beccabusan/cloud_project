from celery import Celery
celery=Celery()
celery.config_from_object('masterconf')
from svmscript import work
work.delay(0,90,30,5,0)

