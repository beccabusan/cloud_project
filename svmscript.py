from celery import Celery
import re
import os, sys, subprocess, time 
from os import environ as env

homepath = '/home/ubuntu/'
geofilepath = homepath+"cloud_project/geo"
mshfilepath = homepath+"cloud_project/msh"
xmlfilepath = homepath+"xml_files/" 
resultpath= homepath+"cloud_project/results/drag_ligt.m"


username = "slavevm1"
userpwd = "slavepwd1"
masterip = "127.0.0.1"
mastervhost = "mastervhost"

mainurl = "amqp://" + username + ":" + userpwd + "@" + masterip + "/" + mastervhost

app = Celery('fenicstask', backend=mainurl, broker=mainurl)

@app.task
def work(a_start, a_stop, n_angles, n_nodes, n_levels):
        
	meshfiles = subprocess.call(['./run.sh',str(a_start),str(a_stop),str(n_angles),str(n_nodes),str(n_levels)])
	
	print "Starting to convert msh files"
	for file in os.listdir(mshfilepath):		
	
		mshfilename =  "/home/ubuntu/cloud_project/msh/"+file
		
		xmlfilename = xmlfilepath+((file).split('.'))[0] + ".xml"
		print "Converting "+ mshfilename +" into "+ xmlfilename
              	convert = subprocess.call(['dolfin-convert', mshfilename, xmlfilename])

	result_all_angles = []
	for file in os.listdir(xmlfilepath):
		str_angle = re.search('a(.+?)n', file)
                if str_angle:
                        angle = str_angle.group(1)
                print "This is the angle: "+ angle

		airfoil_bin_path = "/home/ubuntu/cloud_project/navier_stokes_solver/./airfoil"
		get_airfoil_result = subprocess.call([airfoil_bin_path, '10', '0.0001','10.','0.2', homepath+"/xml_files/"+file])
                
                print 'Starting some calculations on angle: '+ angle
                dlfile = open(resultpath,'r')
                dragsum=liftsum=0
                i=1
                for line in dlfile:
                        row = (line).split()
                        if(i%10):
                                print 'Doing calculations...'
                        if i>20:
                                dragsum+=float(row[1])
                                liftsum+=float(row[2])
                        i+=1
                meandrag = (dragsum/(i-2))
                meanlift = (liftsum/(i-2))
                print 'Meandrag: ' + str(meandrag)
                print 'Meanlift: ' + str(meanlift)
                result_angle_dir = {'Angle': int(angle), 'Drag': meandrag, 'Lift': meanlift}
                result_all_angles.append(result_angle_dir)
        
        result_all_angles_sorted = sorted(result_all_angles, key=lambda k: k['Lift'], reverse=True)
        
        for line in result_all_angles_sorted:
                print line

        return result_all_angles_sorted
