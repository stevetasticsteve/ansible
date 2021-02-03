#!/bin/bash

sudo apt install git ansible -y
cd ~/Documents
git clone https://github.com/stevetasticsteve/ansible
cd ~/Documents/ansible/
ansible-playbook ./workstation/steve_laptop.yml -K 
