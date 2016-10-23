from celery import Celery
import swiftclient
import re
import os, sys, subprocess, time 
from os import environ as env

homepath = '/tmp/cproj/'
geofilepath = homepath + "cloud_project/geo"
mshfilepath = homepath + "cloud_project/msh"
xmldir = homepath + "xml_files/" 
resultpath= os.getcwd() + "/results/drag_ligt.m"
attr_filename = "/tmp/slave_attr.txt"
attributes = []

#slave vms gets their values themselves from the file
if os.path.isfile(attr_filename):
	for line in open(attr_filename)
		attributes.append(line)

	username = attributes[0]
	userpwd = attributes[1]
	masterip = attributes[2]
	mastervhost = attributes[3]

mainurl = "amqp://" + username + ":" + userpwd + "@" + masterip + "/" + mastervhost

app = Celery('fenicstask', backend=mainurl, broker=mainurl)

@app.task
def work(xmlfilename, samples=10, viscosity=0.0001, speed=10., time=1):
			
	swift_con = swiftclient.client.Connection(authurl='http://130.238.29.253:5000/v3',
                                               user='',
                                               key='',
                                               tenant_name='g2015034',
                                               auth_version='3',
                                               os_options={'tenant_id':'74833650f49e4227b868610684b155f2' , 'region_name': 'UPPMAX'})

	container_name = 'Grupp6_test'
	obj_tuple = swift_con.get_object(container_name, xmlfilename)

	with open(xmldir + xmlfilename, 'w') as xmltoDL:
        	xmltoDL.write(obj_tuple[1])
		
		
	
	
	###Find the angle 
	str_angle = re.search('a(.+?)n', xmlfilename)
        if str_angle:
		angle = str_angle.group(1)
               	print "This is the angle: "+ angle

	airfoil_bin_path = "/home/ubuntu/cloud_project/navier_stokes_solver/./airfoil"
	get_airfoil_result = subprocess.call([airfoil_bin_path, str(samples), str(viscosity), str(speed), str(time), xmldir+xmlfilename])
               
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
	result_angle_dict = {'Angle': int(angle), 'Drag': meandrag, 'Lift': meanlift}
	print result_angle_dict
 	return result_angle_dict
        

