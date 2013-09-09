#!/usr/bin/env python
#*
#* Author : Lance Le Roux
#* Program : junos-multi-command.py
#* Platform : Python Any platform
#* Description :
#* junos-multi-command enables you to run a console command simultaneously on many network devices
#* running the Juniper Junos operating system. The ability to group network devices in the config.yaml file
#* gives the operator the ability to pick and choose the type of device or logical grouping for the
#* selected command.
#*
#* What is really nifty is that it is involked at the command prompt giving the operator the ability to execute
#* commands on many routers in seconds from a terminal window.
#*
#* Copyright (c) 2012 Juniper Networks. All Rights Reserved.
#*
#* YOU MUST ACCEPT THE TERMS OF THIS DISCLAIMER TO USE THIS SOFTWARE,
#* IN ADDITION TO ANY OTHER LICENSES AND TERMS REQUIRED BY JUNIPER NETWORKS.
#*
#* JUNIPER IS WILLING TO MAKE THE INCLUDED SCRIPTING SOFTWARE AVAILABLE TO YOU
#* ONLY UPON THE CONDITION THAT YOU ACCEPT ALL OF THE TERMS CONTAINED IN THIS
#* DISCLAIMER. PLEASE READ THE TERMS AND CONDITIONS OF THIS DISCLAIMER
#* CAREFULLY.
#*
#* THE SOFTWARE CONTAINED IN THIS FILE IS PROVIDED "AS IS." JUNIPER MAKES NO
#* WARRANTIES OF ANY KIND WHATSOEVER WITH RESPECT TO SOFTWARE. ALL EXPRESS OR
#* IMPLIED CONDITIONS, REPRESENTATIONS AND WARRANTIES, INCLUDING ANY WARRANTY
#* OF NON-INFRINGEMENT OR WARRANTY OF MERCHANTABILITY OR FITNESS FOR A
#* PARTICULAR PURPOSE, ARE HEREBY DISCLAIMED AND EXCLUDED TO THE EXTENT
#* ALLOWED BY APPLICABLE LAW.
#*
#* IN NO EVENT WILL JUNIPER BE LIABLE FOR ANY DIRECT OR INDIRECT DAMAGES,
#* INCLUDING BUT NOT LIMITED TO LOST REVENUE, PROFIT OR DATA, OR
#* FOR DIRECT, SPECIAL, INDIRECT, CONSEQUENTIAL, INCIDENTAL OR PUNITIVE DAMAGES
#* HOWEVER CAUSED AND REGARDLESS OF THE THEORY OF LIABILITY ARISING OUT OF THE
#* USE OF OR INABILITY TO USE THE SOFTWARE, EVEN IF JUNIPER HAS BEEN ADVISED OF
#* THE POSSIBILITY OF SUCH DAMAGES.
#*

from ncclient import manager
import sys, getpass, yaml, argparse

def commandlineparser():
	global args
	parser = argparse.ArgumentParser(description='Run a command on many Juniper Junos OS devices via Netconf.', epilog='i.e. junos-multi-command.py --zone firewalls --command "show chassis hardware"')
	parser.add_argument('-z', '--zone', required=True, help='category of network devices to run command against.')
	parser.add_argument('-c', '--command', required=True, help='command in quotes.')
	parser.add_argument('-o', '--output', required=False, help='file to output results.')
	args = parser.parse_args()

def welcomemsg(yamlkey, commandline, output):
	#Print banner and ask for username and password.
	global username
	global password
        print '\nUsing YAML Key: ' + yamlkey
        print 'Executing Command: '+  commandline
	if output is not None:
		print 'Outputing results to: ' + output
        username = raw_input("\nNetwork device username: ")
        password = getpass.getpass(prompt='Password: ', stream=None)
	print "\n\n"

def yamlread(yamlkey, commandline, outputfile):
        headerleftchar = '>>>>>>>>>> '
        headerrightchar = ' <<<<<<<<<'
	try:
                #Open output file if selected
                if outputfile is not None: f = open(outputfile, 'w')
	except IOError:
		print 'Error opening %s for writing output', outputfile

	try:
	        #Open the yaml file and bring in hosts for the specified zone.
		stream = open("config.yaml", 'r')
        except IOError:
		print 'config.yaml is missing, this file contains the list of network devices.\n\nSample Format:\n\nrouters\n - 192.168.0.1\n - 192.168.1.2\n\nfirewalls\n - 172.16.1.1\n - 172.16.1.2'
		createconfig = query_yes_no("Would you like to create a template config.yaml?")		
		if createconfig == True:
			print "\nCreating template config.yaml in your current directory."
			try:
				y = open('config.yaml','w')
				y.write('routers:\n - a.b.c.d\n - a.b.c.d\n\nfirewalls:\n - a.b.c.d\n - a.b.c.d')
				y.close()
				print '\n\nconfig.yaml has been created, please modify it to include your network devices.'
				sys.exit()
			except IOError:
				print 'Could not create config.yaml, there could be a permissions issue'
		else:
			print "Exiting."
			if outputfile is not None: f.close()
			sys.exit()
	hostlist = yaml.load(stream)

	try:
        	for x in hostlist[yamlkey.lower()]:
			topline = headerleftchar + x + ' Start' + headerrightchar
			print topline
			try:
				cmdresult = connect(x, '22', commandline, username, password)
				print cmdresult
        		except Exception, e:
               			 print e			
			bottomline =  headerleftchar + x + ' End' + headerrightchar + '\n'
			print bottomline
			if outputfile is not None:
				f.write(topline + '\n')
				f.write(cmdresult)
				f.write('\n' + bottomline + '\n')
			stream.close()
	except KeyError:
		print 'Check your config.yaml file as your zone does not exist.'
		if outputfile is not None: f.close()
		sys.exit()
	if outputfile is not None: f.close()

def query_yes_no(question, default="no"):
    """Ask a yes/no question via raw_input() and return their answer.
    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).
    The "answer" return value is one of "yes" or "no".
    """
    valid = {"yes":True,   "y":True,  "ye":True,
             "no":False,     "n":False}
    if default == None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
	raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "\
                             "(or 'y' or 'n').\n")

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
#	for line in resultstr: 
#		outputresult += line
	outputresult = '\n'.join(resultstr)
	return outputresult
  
if __name__ == '__main__':
	#Get command line arguments
	commandlineparser()

	#Show welcome message.
	welcomemsg(args.zone, args.command, args.output)
	
	#Pass the yaml key and command from system argumemt to yamlread and loop through each host.
	yamlread(args.zone.lower(), args.command, args.output)

		
		
