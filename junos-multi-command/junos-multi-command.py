#!/usr/bin/env python

from ncclient import manager
import sys, getpass, yaml, argparse

def commandlineparser():
	global args
	parser = argparse.ArgumentParser(description='Run a command on many Juniper Junos OS devices via Netconf.', epilog='i.e. junos-multi-command.py --zone firewalls --command "show chassis hardware"')
	parser.add_argument('-z', '--zone', required=True, help='category of network devices to run command against.')
	parser.add_argument('-c', '--command', required=True, help='command to run in quotes.')
	args = parser.parse_args()

def welcomemsg(yamlkey, commandline):
	#Print banner and ask for username and password.
	global username
	global password
        print '\nUsing YAML Key: ' + yamlkey
        print 'Executing Command: '+  commandline + '\n'
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

	try:
        	for x in hostlist[yamlkey]:
			print headerleftchar + x + ' Start' + headerrightchar
			try:
				connect(x, '22', commandline, username, password)
        		except Exception, e:
               			 print e			
			print headerleftchar + x + ' End' + headerrightchar + '\n'
		stream.close()
	except KeyError:
		print 'Check your config.yaml file as your zone does not exist'
		sys.exit()

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
	#Get command line arguments
	commandlineparser()

	#Show welcome message.
	#welcomemsg(sys.argv[], sys.argv[2])
	welcomemsg(args.zone, args.command)
	
	#Pass the yaml key and command from system argumemt to yamlread and loop through each host.
	yamlread(args.zone, args.command)

		
		
