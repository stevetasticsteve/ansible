#!/bin/bash

read -p "Set up for (s)teve or (g)erdine?: " user 
sudo apt install ansible curl -y
curl https://github.com/stevetasticsteve/ansible/archive/master.zip -L -o /tmp/ansible.zip
sudo rm -r /tmp/ansible
unzip /tmp/ansible.zip -d /tmp/ansible
cd /tmp/ansible/ansible-master/workstation
if [[ $user == s ]]; then
    ansible-playbook /tmp/ansible/ansible-master/workstation/steve_laptop.yml
elif [[ $user == g ]]; then
    ansible-playbook /tmp/ansible/ansible-master/workstation/gerdine_laptop.yml
else
    echo "Incorrect user, run the playbook yourself." && exit 1
fi
sudo dpkg-reconfigure libdvd-pkg
