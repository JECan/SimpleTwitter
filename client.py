#Socket client example in python
 
import socket   #for sockets
import sys  #for exit
import getpass
 
#create an INET, STREAMing socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
    print 'Failed to create socket'
    sys.exit()
     
print 'Socket Created'
 
#HOST = 'localhost';
HOST = '10.0.0.4';
PORT = 5733;
 
try:
    remote_ip = socket.gethostbyname(HOST)
 
except socket.gaierror:
    #could not resolve
    print 'Hostname could not be resolved. Exiting'
    sys.exit()
 
#Connect to remote server
s.connect((remote_ip , PORT))
 
#print 'Socket Connected to ' + HOST + ' on ip ' + remote_ip

while 1:
	try :
		##
		#print "1 Loop"
		d = s.recv(2048)
		#print "Post Recv"
		opt = d[0:5]
		reply = d[5:]
		
		#print "OPT:" + opt	# For Debugging Purposes
		# Print from server
		if opt == "usrin" or opt == "choos":
			userIn = raw_input(reply)
			s.sendall(userIn)
		elif opt == "psswd" or reply == "chngp":
			pwd = getpass.getpass(reply)
			s.sendall(pwd)
		elif opt == "lgout":
			print "Loggint out"
			break
		elif opt == "mesge":
			print reply
			s.sendall("0")
		elif opt == "frndr": #Friend Request
			print reply
			userIn = raw_input("Add(1 for Yes): ")
			s.sendall(userIn)
		elif opt == "walll":
			print reply
			s.sendall("0")
		elif opt == "timel":
			print reply
			s.sendall("0")
		else:
			#print "IN ELSE\n"
			print d
	except socket.error:
		#Send failed
		print 'Send failed'
		sys.exit()
 
#print 'Message send successfully'
 
#Now receive data
#reply = s.recv(4096)
s.close()
