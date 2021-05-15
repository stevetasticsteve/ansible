# Brand new raspberry pi
These steps set up a brand new raspberry pi. Pi user is replaced with a new user, ssh keys are added and system is updated.

1. Format SD card (Fat32)
2. Use Rpi imager to flash iso
3. Add a blank file named ssh in the boot partition
4. Add a wpa_supplicant.conf in the boot partition
5. Insert SD card into pi and power on
6. Find the IP address
7. ssh into pi as pi (password raspberry) to establish trusted connection
8. Edit new_pi_hosts to point to the new pi
9.  > ansible-playbook -i new_pi_hosts init_pi.yml
10. Update global hosts and secrets file