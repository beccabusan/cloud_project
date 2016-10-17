import sys
from celery import Celery 
from running_AIRFOIL_arg_XML_SLAVEVM import work

if __name__=="__main__":
	filelist = sys.argv[1]
	tasks = []
	celery = Celery()
	celery.conf.update('settings')
		for line in filelist:
			tasks.append(work.delay(line))
	return tasks		