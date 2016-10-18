#!/usr/bin/python
import os, subprocess
import sys

#def start_x_slavevms():
if sys.argv[1:]:
	masterip = subprocess.check_output("ip route get 8.8.8.8 | awk '{print $NF; exit}'",shell=True)
	number_of_vmslaves = int(sys.argv[1])
	i=1
	while i <= number_of_vmslaves:
		print "Iniated slave number: "+ str(i)
		###TODO ADD USER DATA FOR EACH WORKER- CELERY SETUP
		subprocess.call('python /home/ubuntu/cloud_project/starting_script.py ' + str(i) + " " + str(masterip), shell=True)				
		i += 1
	



















