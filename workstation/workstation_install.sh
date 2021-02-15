#!/bin/bash

read -p "Set up for (s)teve or (g)erdine?: " user 
sudo apt install ansible -y
curl https://github.com/stevetasticsteve/ansible/archive/master.zip -L -o /tmp/ansible.zip
unzip /tmp/ansible.zip -d /tmp/ansible
if [[ $user == s ]]; then
    ansible-playbook /tmp/ansible/ansible-master/workstation/steve_laptop.yml -K 
elif [[ $user == g ]]; then
    ansible-playbook /tmp/ansible/ansible-master/workstation/gerdine_laptop.yml -K 
else
    echo "Incorrect user, run the playbook yourself." && exit 1
fi
sudo dpkg-reconfigure libdvd-pkg
