from celery import Celery
celery=Celery()
celery.config_from_object('masterconf')
from svmscript import work
work.delay(0,30,10,100,1)

