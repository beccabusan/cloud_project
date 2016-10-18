import sys
from celery import Celery 
celery = Celery()
celery.conf.update('settings')
from running_AIRFOIL_arg_XML_SLAVEVM import work

if __name__=="__main__":
	filelist = (sys.argv[1]).split()
	tasks = []
		for line in filelist:
			tasks.append(work.delay(line))
	return tasks		