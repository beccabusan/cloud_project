#!/bin/bash
rm -rf /home/ubuntu/xml_files
mkdir /home/ubuntu/xml_files

rm -rf /home/ubuntu/cloud_project/msh
rm -rf /home/ubuntu/cloud_project/geo

mkdir /home/ubuntu/cloud_project/msh
mkdir /home/ubuntu/cloud_project/geo

rm -rf /home/ubuntu/cloud_project/results


python /home/ubuntu/cloud_project/test_worker.py
