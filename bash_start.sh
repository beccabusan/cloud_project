#!/bin/bash
source ~/source_this.sh
python ~/cloud_project/starting_script.py
FLOATING_IP=`cat ~/cloud_project/floating_ip.txt`
while ! ping -c1 $FLOATING_IP &>/dev/null; do echo $FLOATING_IP; done
echo "Ping successful!"
echo "resting for my master"
sleep 10
echo "Sleep done mothafucka"
scp -o "StrictHostKeyChecking no" -i ~/albins2.key ~/cloud_project/run.sh ubuntu@$FLOATING_IP:/home/ubuntu/
scp -o "StrictHostKeyChecking no" -i ~/albins2.key ~/cloud_project/naca2gmsh_geo.py ubuntu@$FLOATING_IP:/home/ubuntu/



echo innan update
ssh -i ~/albins2.key ubuntu@$FLOATING_IP sudo apt-get update
echo efter update

ssh -i ~/albins2.key ubuntu@$FLOATING_IP sudo apt-get install rabbitmq-server

ssh -i ~/albins2.key ubuntu@$FLOATING_IP sudo -H pip install Celery 

echo efter rabbit
#ssh -i ~/albins2.key ubuntu@$FLOATING_IP screen -d -m celery -A readTweets worker --loglevel=info 
echo started worker
#ssh -i ~/albins2.key ubuntu@$FLOATING_IP screen -d -m python init_flask.py 
echo start flask shit

