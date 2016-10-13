from celery import Celery
celery=Celery()
celery.config_from_object('masterconf')
from svmscript import work



result_arr=[]
num_workers=2

for i in range num_workers:
    ###TODO  30 should be an argv (All numbers should be comming from argv)
    result_arr.append(work.delay((30/num_workers)*i,(30/num_workers)*(i+1),10,100,1))

