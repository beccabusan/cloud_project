from celery import Celery
import re
import os, sys, subprocess, time 
from os import environ as env

homepath = '/home/ubuntu/'
geofilepath = homepath + "cloud_project/geo"
mshfilepath = homepath + "cloud_project/msh"
xmldir = homepath + "xml_files/" 
resultpath= os.getcwd() + "/results/drag_ligt.m"


username = "slavevm1"
userpwd = "slavepwd1"
masterip = "127.0.0.1"
mastervhost = "mastervhost"

mainurl = "amqp://" + username + ":" + userpwd + "@" + masterip + "/" + mastervhost

app = Celery('fenicstask', backend=mainurl, broker=mainurl)

@app.task
def work(xmlfilename, samples=10, viscosity=0.0001, speed=10., time=1):
			
	swift_con = swiftclient.client.Connection(authurl='http://130.238.29.253:5000/v3',
                                               user='albins',
                                               key='grupp6',
                                               tenant_name='g2015034',
                                               auth_version='3',
                                               os_options={'tenant_id':'74833650f49e4227b868610684b155f2' , 'region_name': 'UPPMAX'})

	container_name = 'Grupp6'
	xmlfile = swift_con.get_object(container_name, xmlfilename)

	with open(xmldir + xmlfilename, 'w') as xmltoDL:
        	xmltoDL.write(obj_tuple[1])
		
		
	###Find the angle 
	str_angle = re.search('a(.+?)n', xmlfilename)
        if str_angle:
		angle = str_angle.group(1)
               	print "This is the angle: "+ angle

	airfoil_bin_path = "/home/ubuntu/cloud_project/navier_stokes_solver/./airfoil"
	get_airfoil_result = subprocess.call([airfoil_bin_path, str(samples), str(viscosity), str(speed), str(time), xmldir + xmlfilename)
               
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
        

