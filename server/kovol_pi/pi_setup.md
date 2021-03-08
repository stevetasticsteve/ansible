# Steps to setup a new headless Rpi
1. Format SD card with FAT
2. Use Rpi imager to image the card
3. Drop a file called ssh in the boot partition
4. Add a wpa_supplicant.conf file into the boot partition
5. ssh into pi as pi (password raspberry) to establish trusted connection
6. enable ssh with sudo raspi-config
7. Adjust hosts file
8. Run "ansible-playbook init_pi.yml -i new_pi_hosts" to install new user
9. Adjust /etc/ansible/hosts
10. Run "ansible-playbook delete_pi_user.yml -K" with new host settings to finish