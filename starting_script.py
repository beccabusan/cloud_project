# -*- coding: utf-8 -*-
# http://docs.openstack.org/developer/python-novaclient/ref/v2/servers.html
import time, os, sys
import inspect
from os import environ as env

from  novaclient import client
import keystoneclient.v3.client as ksclient
from keystoneauth1 import loading
from keystoneauth1 import session

flavor = "c1.small" 
private_net = 'g2015034-net_2'
floating_ip_pool_name = 'public'
floating_ip = None
slave_number = str(sys.argv[1])
slavename = "slavevm"+str(slave_number)
slavepwd = "slavepwd"+str(slave_number)
master_ip = str(sys.argv[2])
master_host = "mastervhost"

loader = loading.get_plugin_loader('password')
auth = loader.load_from_options(auth_url=env['OS_AUTH_URL'],username=env['OS_USERNAME'],password=env['OS_PASSWORD'],project_name=env['OS_PROJECT_NAME'],user_domain_name=env['OS_USER_DOMAIN_NAME'],project_domain_name=env['OS_PROJECT_DOMAIN_NAME'])

#how to create custom userdata - export the variables inside each slave vm
userdata='Content-Type: test/cloud-config\nwrite_files:\n - path: /tmp/slave_attr.txt\n   content: | \n     '+slavename+'\n     '+slavepwd+'\n     '+master_ip+'\n     '+master_host+'\n - path: /tmp/userscript.sh\n   content: | \n     mkdir /tmp/cproj\n     cd /tmp/cproj\n     git clone https://github.com/beccabusan/cloud_project.git\n     mkdir xml_files\n     cd cloud_project\n      mkdir geo\n      mkdir msh\n     celery --purge -A worker running_AIRFOIL_arg_XML_SLAVEVM -l info --autoscale=1,1\n\nruncmd:\n - sh /tmp/userscript.sh'

sess = session.Session(auth=auth)
nova = client.Client('2.1', session=sess)
print "user authorization completed."

image = nova.images.find(name="Grupp6_real_real")
flavor = nova.flavors.find(name=flavor)

if private_net != None:
    net = nova.networks.find(label=private_net)
    nics = [{'net-id': net.id}]
else:
    sys.exit("private-net not defined.")

#print("Path at terminal when executing this file")
#print(os.getcwd() + "\n")
#cfg_file_path =  '/home/albin/labb3-cfg.txt'
#if os.path.isfile(cfg_file_path):
#    userdata = open(cfg_file_path)
#else:
#    sys.exit("cloud-cfg.txt is not in current working directory")
    
secgroup = nova.security_groups.find(name="default")
secgroups = [secgroup.id]

#floating_ip = nova.floating_ips.create(nova.floating_ip_pools.list()[0].name)


###DONT NEED Floating IP
if floating_ip_pool_name != None: 
    floating_ip = nova.floating_ips.create(floating_ip_pool_name)
else: 
    sys.exit("public ip pool name not defined.")

print "Creating instance ... "

instance = nova.servers.create(name="grupp6-"+slavename, image=image, flavor=flavor, nics=nics,security_groups=secgroups, userdata=userdata, key_name='albins2')
inst_status = instance.status

print "waiting for 10 seconds.. "
time.sleep(10)

while inst_status == 'BUILD':
    print "Instance: "+instance.name+" is in "+inst_status+" state, sleeping for 5 seconds more..."
    time.sleep(5)
    instance = nova.servers.get(instance.id)
    inst_status = instance.status

print "Instance: "+ instance.name +" is in " + inst_status + "state"

if floating_ip.ip != None: 
   instance.add_floating_ip(floating_ip)
   with open("/home/ubuntu/floating_ip.txt","w") as f:
   	f.write(floating_ip.ip)
print "Instance booted! Name: " + instance.name + " Status: " +instance.status+ ", no floating IP attached " + floating_ip.ip

#else:
#    print "Instance booted! Name: " + instance.name + " Status: " +instance.status+ ", floating IP missing"
