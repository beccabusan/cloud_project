from celery import Celery
celery=Celery()
celery.config_from_object('masterconf')
from svmscript import work
work.delay(10,150,5,5,0)

