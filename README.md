junos-multi-command
===================
junos-multi-command enables you to run a console command simultaneously on many network devices
running the Juniper Junos operating system. The ability to group network devices in the config.yaml file
gives the operator the ability to pick and choose the type of device or logical grouping for the 
selected command.

What is really nifty is that it is involked at the command prompt giving the operator the ability to execute
commands on many routers in seconds from a terminal window. 

Functions
=========
* Run a single command on a few or even hundreds of network devices with results returned.
* Uses a config.yaml file to define your hosts in zones allowing you to group like network devices.
* Very rapid execution of commands on multiple routers.
* Secure transfer of commands and results via Netconf (SSH)

Installation
============
Download from github and install dependencies, or type "easy_install junos-multi-command" and have
the dependencies and python script installed automatically.

Platform
========
Should work on any platform, UNIX, Windows, etc

Dependencies
============
* ncclient - Netconf interface to Juniper devices. 
* PyYaml - YAML parsers for python.
* getpass - used to obsecure password prompt.


Configuration
=============
Ensure you have a proper config.yaml file in your current directory as the script looks for it 
realitive to your current directory.

Configuration file is in YAML format and is divided into zones, below is an example.

Sample config.yaml
[root@localhost junos-multi-command]# more config.yaml 
firewalls:
 - 172.16.50.200
 - 172.16.50.201

routers:
 - 172.16.50.200

Usage
=====
	[root@localhost junos-multi-command]# ./junos-multi-command.py -h
	usage: junos-multi-command.py [-h] -z ZONE -c COMMAND [-o OUTPUT]
	
	Run a command on many Juniper Junos OS devices via Netconf.
	
	optional arguments:
	  -h, --help            show this help message and exit
	  -z ZONE, --zone ZONE  category of network devices to run command against.
	  -c COMMAND, --command COMMAND
	                        command in quotes.
	  -o OUTPUT, --output OUTPUT
	                        file to output results.

i.e. junos-multi-command.py --zone firewalls --command "show chassis hardware"

Example of Command
==================
	[root@localhost junos-multi-command]# ./junos-multi-command.py -z firewalls -c "show chassis hardware"
	
	Using YAML Key: firewalls
	Executing Command: show chassis hardware
	
	Enter your network username: root
	Password: 
	
	
	
	>>>>>>>>>> 172.16.50.200 Start <<<<<<<<<
	Hardware inventory:
	Item             Version  Part number  Serial number     Description
	Chassis                                9c28b76d076d      JUNOSV-FIREFLY
	Midplane        
	System IO       
	Routing Engine                                           JUNOSV-FIREFLY RE
	FPC 0                                                    Virtual FPC
	  PIC 0                                                  Virtual GE
	Power Supply 0  
	>>>>>>>>>> 172.16.50.200 End <<<<<<<<<
	
	>>>>>>>>>> 172.16.50.201 Start <<<<<<<<<
	Hardware inventory:
	Item             Version  Part number  Serial number     Description
	Chassis                                2bdc25efad71      JUNOSV-FIREFLY
	Midplane        
	System IO       
	Routing Engine                                           JUNOSV-FIREFLY RE
	FPC 0                                                    Virtual FPC
	  PIC 0                                                  Virtual GE
	Power Supply 0  
	>>>>>>>>>> 172.16.50.201 End <<<<<<<<<

