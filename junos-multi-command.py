#!/usr/bin/env python

from ncclient import manager
import sys, getpass, yaml

def welcomemsg(yamlkey, commandline):
	#Print banner and ask for username and password.
	global username
	global password
        print '\nUsing YAML Key: ' + yamlkey
        print 'Executing Command: '+  str(sys.argv[2]) + '\n'
        username = raw_input("Enter your network username: ")
        password = getpass.getpass(prompt='Password: ', stream=None)
	print "\n\n"

def yamlread(yamlkey, commandline):
        headerleftchar = '>>>>>>>>>> '
        headerrightchar = ' <<<<<<<<<'

	#Open the yaml file and bring in hosts for the specified zone.
	try:
		stream = open("config.yaml", 'r')
        except IOError:
		print 'config.yaml is missing, this file contains the list of network devices.\n\nSample Format:\n\nrouters\n - 192.168.0.1\n - 192.168.1.2\n\nfirewalls\n - 172.16.1.1\n - 172.16.1.2'
		sys.exit()
	hostlist = yaml.load(stream)

        for x in hostlist[yamlkey]:
		print headerleftchar + x + ' Start' + headerrightchar
		connect(x, '22', commandline, username, password)
		#connect(x, '22', commandline, 'root', 'Cole44!!')	
		print headerleftchar + x + ' End' + headerrightchar + '\n'
	stream.close()

def connect(host, port, cmdline, user, password):
	conn = manager.connect(host=host,
	port=port,
	username=user,	
	password=password,
	timeout=10,
	hostkey_verify=False)
	
	result = conn.command(command=cmdline, format='text')
	resultstr = result.tostring
	resultstr = resultstr.splitlines() 
	#Remove first and last two lines of display. Makes it look more like a standard network device output.
	for a in range(0, 2):
		resultstr.pop(0)
		resultstr.pop(-1)
	for line in resultstr: print line    

  
if __name__ == '__main__':
	#Show welcome message.
	welcomemsg(sys.argv[1], sys.argv[2])
	
	#Pass the yaml key and command from system argumemt to yamlread and loop through each host.
	yamlread(sys.argv[1], sys.argv[2])

		#print headerleftchar + str.strip(line) + ' Start' + headerrightchar
		#connect(str.strip(line), '22', str(sys.argv[2]), username, password)
		#print headerleftchar + str.strip(line) + ' End' + headerrightchar + '\n'
		
		
