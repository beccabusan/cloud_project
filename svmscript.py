from celery import Celery
import os, sys, subprocess, time 
from os import environ as env
geofilepath = "/home/ubuntu/cloud_project/geo"
mshfilepath = "/home/ubuntu/cloud_project/msh"
xmlfilepath = "/home/ubuntu/xml_files/"


username = "slavevm1"
userpwd = "slavepwd1"
masterip = "127.0.0.1"
mastervhost = "mastervhost"

mainurl = "amqp://" + username + ":" + userpwd + "@" + masterip + "/" + mastervhost

app = Celery('fenicstask', backend=mainurl, broker=mainurl)

@app.task
def work(a_start, a_stop, n_angles, n_nodes, n_levels):
#	strcmd = "./run.sh " + a_start + " " + a_stop + " " + n_angles + " " + n_nodes + " " + n_levels
	meshfiles = subprocess.call(['./run.sh',str(a_start),str(a_stop),str(n_angles),str(n_nodes),str(n_levels)])
	
	print "Starting to convert msh files"
	for file in os.listdir(mshfilepath):		
	
		mshfilename =  "/home/ubuntu/cloud_project/msh/"+file
		
		xmlfilename = xmlfilepath+((file).split('.'))[0] + ".xml"
		print "Converting "+ mshfilename +" into "+ xmlfilename
              	convert = subprocess.call(['dolfin-convert', mshfilename, xmlfilename])
	
	
	for file in os.listdir(xmlfilepath):
		
		airfoil_bin_path = "/home/ubuntu/cloud_project/navier_stokes_solver/./airfoil"
		get_airfoil_result = subprocess.call([airfoil_bin_path, '10', '0.0001','10.','1', file])
	
		
	
