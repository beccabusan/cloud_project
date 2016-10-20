#!/usr/bin/python
import os, subprocess
import swiftclient
homepath = '/home/ubuntu/'
geofilepath = homepath+"cloud_project/geo"
mshfilepath = homepath+"cloud_project/msh"
xmlfilepath = homepath+"xml_files/" 

##############################
##Setting the defualt values##
##############################
def generate_convert(a_start="0", a_stop='30', n_angles='5', n_nodes='5', n_levels='0'):
	
	swift_con = swiftclient.client.Connection(authurl='http://130.238.29.253:5000/v3',
                                               user='',
                                               key='',
                                               tenant_name='g2015034',
                                               auth_version='3',
                                               os_options={'tenant_id':'74833650f49e4227b868610684b155f2', 'region_name': 'UPPMAX'})

	container_name = 'Grupp6_test'		

	for data in swift_con.get_container(container_name)[1]:
		swift_con.delete_object(container_name, data['name'])
	
	
	##Generating the .msh and .geo files
	meshfiles = subprocess.call(['/home/ubuntu/cloud_project/./run.sh',str(a_start),str(a_stop),str(n_angles),str(n_nodes),str(n_levels)])

	all_xml_filename = []

	###Converting the .msh to .xml
	print "Starting to convert msh files"		
	for file in os.listdir(mshfilepath):		
		mshfilename =  mshfilepath + "/" + file
		xmlname = ((file).split('.'))[0] + ".xml"
		xmlfilename = xmlfilepath+((file).split('.'))[0] + ".xml"	
		print "Converting "+ mshfilename +" into "+ xmlfilename
        	convert = subprocess.call(['dolfin-convert', mshfilename, xmlfilename])

		###Maybe wrong here, might want to use xmlname instead of xmlfilename under here
		with open(xmlfilename, 'r') as xmlfiletoUpload:
        		swift_con.put_object(container_name, xmlname,
                                        contents= xmlfiletoUpload.read(),
                                        content_type='text/plain')

		all_xml_filename.append(xmlname)				

			
	return all_xml_filename
	
generate_convert()
