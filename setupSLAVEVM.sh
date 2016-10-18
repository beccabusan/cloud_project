#!/bin/bash

FLOATING_IP=`cat /home/ubuntu/floating_ip.txt`
while ! ping -c1 $FLOATING_IP &>/dev/null; do echo $FLOATING_IP; done


echo innan update
ssh -i -t /home/ubuntu/albins2.key ubuntu@$FLOATING_IP <<- "endssh"
sudo apt-get update
cd cloud_project/
git pull
export USER_NAME = slavevm1
export USER_PWD = slavepwd1
export MASTER_IP = $(curl ipecho.net/plain)
export MASTER_HOST = mastervhost

cd flaskr/
screen -d -m celery -A running_AIRFOIL_arg_XML_SLAVEVM worker --loglevel=info


endssh


