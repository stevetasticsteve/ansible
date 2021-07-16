#!/bin/bash
# wget https://raw.githubusercontent.com/stevetasticsteve/ansible/master/workstation/workstation_install.sh; bash workstation_install.sh

read -p "Set up for (s)teve or (g)erdine?: " user 
sudo apt install ansible curl -y
curl https://github.com/stevetasticsteve/ansible/archive/master.zip -L -o /tmp/ansible.zip
sudo rm -r /tmp/ansible
unzip /tmp/ansible.zip -d /tmp/ansible
cd /tmp/ansible/ansible-master/workstation
if [[ $user == s ]]; then
    ansible-playbook --ask-vault-pass steve_laptop.yml -K
elif [[ $user == g ]]; then
    ansible-playbook --ask-vault-pass gerdine_laptop.yml -K
else
    echo "Incorrect user, run the playbook yourself." && exit 1
fi
sudo dpkg-reconfigure libdvd-pkg
