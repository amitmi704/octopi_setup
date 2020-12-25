# octopi_setup
An Ansible setup package to get OctoPrint running on your Raspberry Pi with ease.  Includes a Python WiFi setup script (one for Raspbian and one for Ubuntu) to ensure quick connectivity setup.
*Note: Developed on Raspbian OS 2020-12-02 release*

# Directions:
###### USB File Transfer
1. Format a USB drive using the FAT32 format.
1. Insert the USB drive into the Raspberry Pi (any port will work, we're not dealing with large files)
1. Locate the device name and make note of it: `fdisk -l`
   - E.g. `/dev/sda1`
1. Create a temporary mounting point for the thumb drive, and a directory to copy the files to:
   1. `mkdir ~/tmp_mount`
   1. `mkdir ~/octopi_setup`
1. Mount the drive as a super user: `sudo mount <DEVICE_PATH> ~/tmp_mount`
1. Copy the files to your home directory as a super user: `sudo cp -R ~/tmp_mount ~/octopi_setup`
1. Unmount the thumb drive and clean up the temporary folder:
   1. `sudo umount ~/tmp_mount`
   1. `rm ~/tmp_mount`
1. Update file permissions on the copied files: `sudo chown -R ${LOGNAME}:${LOGNAME} ~/octopi_setup`

###### WiFi Setup
1. Execute the WiFi joining script: `sudo ~/octopi_setup/setup-wifi-ros.py`
2. Follow the prompts to connect.

###### Ansible Install
1. Install Ansible: `sudo apt install ansible`

###### Setup OctoPi
*Note: This step upgrades all application packages and the distribution prior to installing OctoPrint!*
1. Execute the playbook and wait: `ansible-playbook ~/octopi_setup/octoprint_setup.yaml`
2. Obtain the IP address of your system from your NIC: `ip addr show wlan0`
3. Browse to the IP address on port 5000:
   - E.g. `http://192.0.2.1:5000`
4. Finish configuring OctoPrint
