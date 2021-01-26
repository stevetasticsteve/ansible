#!/bin/bash

sudo apt install git ansible
cd ~Documents/post_install
git clone https://github.com/stevetasticsteve/ansible
ansible-playbook ./workstation/steve_laptop.yml -K --ask-vault-pass