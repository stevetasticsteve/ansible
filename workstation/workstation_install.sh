#!/bin/bash

sudo apt install git ansible -y
git clone https://github.com/stevetasticsteve/ansible
cd ~Documents/ansible/
ansible-playbook ./workstation/steve_laptop.yml -K 
