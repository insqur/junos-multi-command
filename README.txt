junos-multi-command
===================
junos-multi-command enables you to run console commands on a few to hundreds of your network devices
running the Juniper Junos operating system.

Functions
=========
* Can run a command on a few or hundreds of network devices with result returned.
* Uses a config.yaml file to define your hosts in zones.
* Zones allow you to run commands on groups of select network devices.
* Secure transfer of commands and results via Netconf (SSH)

Installation
============
Download from github and install dependencies, or type "easy_install junos-multi-command" and have
the dependencies and python script installed automatically.


Dependencies
============
* ncclient - Netconf interface to Juniper devices. 
* PyYaml - YAML parsers for python.
* getpass - used to obsecure password prompt.


Configuration
=============
Ensure you have a proper config.yaml file in your current directory as the script looks for relative location.

Configuration file is in YAML format and is divided into zones.

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
usage: junos-multi-command.py [-h] -z ZONE -c COMMAND

Run a command on many Juniper Junos OS devices via Netconf.

optional arguments:
  -h, --help            show this help message and exit
  -z ZONE, --zone ZONE  category of network devices to run command against.
  -c COMMAND, --command COMMAND
                        command to run in quotes.

i.e. junos-multi-command.py --zone firewalls --command "show chassis hardware"
