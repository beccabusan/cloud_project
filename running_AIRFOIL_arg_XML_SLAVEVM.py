from celery import Celery
import re
import os, sys, subprocess, time 
from os import environ as env

homepath = '/home/ubuntu/'
geofilepath = homepath + "cloud_project/geo"
mshfilepath = homepath + "cloud_project/msh"
xmlfilepath = homepath + "xml_files/" ###THIS SHOULD BE THE STANDARD FILE PATH, IE ON THE CONTAINER OR SOMETHING##
resultpath= os.getcwd() + "/results/drag_ligt.m"


username = "slavevm1"
userpwd = "slavepwd1"
masterip = "127.0.0.1"
mastervhost = "mastervhost"

mainurl = "amqp://" + username + ":" + userpwd + "@" + masterip + "/" + mastervhost

app = Celery('fenicstask', backend=mainurl, broker=mainurl)

@app.task
def work(xmlfile_to_calculate):
	str_angle = re.search('a(.+?)n', xmlfile_to_calculate)
        if str_angle:
		angle = str_angle.group(1)
               	print "This is the angle: "+ angle
	airfoil_bin_path = "/home/ubuntu/cloud_project/navier_stokes_solver/./airfoil"
	get_airfoil_result = subprocess.call([airfoil_bin_path, '10', '0.0001','10.','1', xmlfilepath + xmlfile_to_calculate])
               
	print 'Starting some calculations on angle: '+ angle
        dlfile = open(resultpath,'r')
        dragsum=liftsum=0
        i=1
        for line in dlfile:
		row = (line).split()
		if(i%10):
			print 'Doing calculations...'
		if i>20:
			liftsum+=float(row[1])
			dragsum+=float(row[2])
		i+=1

	meandrag = (dragsum/(i-2))
	meanlift = (liftsum/(i-2))
	result_angle_dir = {'Angle': int(angle), 'Drag': meandrag, 'Lift': meanlift}
 	return result_angle_dir
        

