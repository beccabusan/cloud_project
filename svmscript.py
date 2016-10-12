from celery import Celery
import os, sys, subprocess, time 
from os import environment as env
GEODIR = "/geo/"

username = env['CEL_USER_NAME']
userpwd = env['CEL_USER_PWD']
masterip = env['CEL_MASTER_IP']
mastervhost = env['CEL_MASTER_VHOST']

mainurl = "amqp:// " + username + ":" + userpwd + "@" + masterip + "/" + mastervhost

app = Celery('fenicstask', backend=mainurl, broker=mainurl)

@app.task
def work(a_start, a_stop, n_angles, n_nodes, n_levels):
	strcmd = "./runme.sh " + a_start + " " + a_stop + " " + n_angles + " " + n_nodes + " " + n_levels
	meshfiles = subprocess.call(['./runme.sh','a_start','a_stop','n_angles','n_nodes','n_levels'])
	
	while meshfiles==0:
		time.sleep(0.1)
	geofilepath = GEODIR

	for file in geofilepath:
		geofilename = os.path.basename(file))
		xmlfilename = ((geofilename).split('.'))[0] + ".xml"
    	convert = subprocess.call(['./dolphin-convert', geofilename, xmlfilename])
	
    return "worked."



