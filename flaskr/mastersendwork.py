import sys
from celery import Celery 
celery = Celery()
celery.config_from_object('settings')


def send_task(filelist):
        tasks = []
        for line in filelist:
                tasks.append(celery.send_task('running_AIRFOIL_arg_XML_SLAVEVM.work', (line,)))
        return tasks		
