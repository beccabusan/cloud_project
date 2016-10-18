#!/usr/bin/python
import os, subprocess
import sys

def start(numvms):
	masterip = subprocess.check_output("ip route get 8.8.8.8 | awk '{print $NF; exit}'",shell=True)
	number_of_vmslaves = numvms
	i=1
	while i <= number_of_vmslaves:
		print "Iniated slave number: "+ str(i)
		vm = subprocess.Popen('python /home/ubuntu/cloud_project/starting_script.py ' + str(i) + " " + str(masterip), shell=True)				
		vm.wait()
		os.system('/home/ubuntu/cloud_project/./setupSLAVEVM.sh')
		i += 1
	



















