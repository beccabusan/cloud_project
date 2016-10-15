#!/usr/bin/python
import os, subprocess

homepath = '/home/ubuntu/'
geofilepath = homepath+"cloud_project/geo"
mshfilepath = homepath+"cloud_project/msh"
xmlfilepath = homepath+"xml_files/" 

##############################
##Setting the defualt values##
##############################
def generate_convert(a_start="0", a_stop='30', n_angles='5', n_nodes='5', n_levels='0'):
	##Generating the .msh and .geo files
	meshfiles = subprocess.call(['./run.sh',str(a_start),str(a_stop),str(n_angles),str(n_nodes),str(n_levels)])

	###Converting the .msh to .xml
	print "Starting to convert msh files"		
	for file in os.listdir(mshfilepath):		
		mshfilename =  mshfilepath + "/" + file
		xmlfilename = xmlfilepath+((file).split('.'))[0] + ".xml"	
		print "Converting "+ mshfilename +" into "+ xmlfilename
        	convert = subprocess.call(['dolfin-convert', mshfilename, xmlfilename])

