import sys
from celery import Celery 
celery = Celery()
celery.config_from_object('settings')

def main():
        filelist = (sys.argv[1]).split()
        tasks = []
        for line in filelist:
                tasks.append(running_AIRFOIL_arg_XML_SLAVEVM.work.delay(line))
        return tasks		
if __name__=="__main__":  
        main()
