import socket
import sys
from thread import *

HOST = '' #Symbolic name, all available interfaces
PORT = 5733 #Arbitrary non-privileged port
connList = []

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'

try:
	s.bind((HOST, PORT))
except socket.error, msg:
	print 'Bind failed. Error:' + str(msg[0]) + ' ' + msg[1]
	sys.exit()

print 'Socket Bind Complete'

wall = [] # List of OP, Post
accounts = []	# List of tuple accounts
# Adding accounts
## [0]User   [1]Pass [2]New Msgs, [3] Messages, [4]New Friend Requests, [5] Name, Friend Status
acct1 = ["Bill", "1111", 1, [], 0, []]
accounts.append(acct1)

acct2 = ["Joe", "2222", 2, [], 0, []]
accounts.append(acct2)
accounts[1][3].append(["MiniNet","Welcome!"])
accounts[1][3].append(["MiniNet","How To Message Someone:\nType 4, Type Recipient, Send Message"])


acct3 = ["Bob", "3333", 0, [], 0, []]
accounts.append(acct3)
accounts[2][3].append(["MiniNet","Welcome!"])
# End Of accounts


s.listen(10) #10 is max waitlisted
print 'Socket Now Listening'

def findUser(user):
	i = 0;
	for acc in accounts:
		#print acc[0]
		if user == acc[0]: 
			return i
		else: 
			i = i + 1
	return 0

def isFriends(userIndex, user): # index of OP, username of potential friend
	for acc in accounts[userIndex][5]:
		if acc[0] == user and acc[1] == 1:
			return 1
	return 0
	
def printUnread(userIndex):
	reply = "mesge" 
	numToRead = accounts[userIndex][2]
	for msg in accounts[userIndex][3][-numToRead:]:
		reply = reply + msg[0] + "\n" + msg[1] + "\n\n"
		

	return reply
	
def printFriends(userIndex):
	reply = "frndl" 
	for friends in accounts[userIndex][6]:
		reply = reply + friends[0] + "\n"
	return reply
	
def findInList(name, requestee):
	i = 0
	print name + " " + str(requestee)
	for acct in accounts[requestee][5]:
		print "Account" + requests[0]
		print "Pending: " + look[0]
		if acct[0] == name:
			return i
		i = i + 1	
	return -1
	
def clientthread(conn):
	userIndex = 0 ## Index for User/Pass tuple
	while 1:
		user = ""
		while user != accounts[userIndex][0]:	
			reply = "usrin" + "Username: " # Tell client to send user
			conn.send(reply)
			user = conn.recv(1024)
			userIndex = findUser(user)
		# Get Password for user above	
		passWord = ""
		while passWord != accounts[userIndex][1]:	
			reply = "psswd" + "Password: "  # Tell client to send password
			conn.send(reply)
			passWord = conn.recv(1024)
				
		print user + " Logged In"
			
		options = "\n1) Logout 2)Change Password 3)Show Unread Messages 4)Send Message \n5) Accept Friend Requests 6) Write a Post 7) News Feed 8) Send A Request 9) Timeline\nDo:"
		menu = "choos" + "New Messages:" + str(accounts[userIndex][2]) + "\nFriend Requests:" + str(accounts[userIndex][4]) + options # Output possible menu	
		conn.send(menu)
		while 1: #Loop in menu while not logging out
			#print "Waiting for Data"
			
			data = conn.recv(1024)
			
			### Log Out
			if data == '1': 
				reply = "lgout" + "Logging out" + user
				conn.send(reply)
				print user + "Logged Out"
				break;
			### Change Password
			elif data == '2': 
				passWord = ""
				while passWord != accounts[userIndex][1]:	
					reply = "psswd" + "Old Password: "  # Tell client to send old password
					conn.send(reply)
					passWord = conn.recv(1024)
				passWord = ""
				reply = "psswd" + "New Password: "  # Tell client to send New password
				conn.send(reply)
				passWord = conn.recv(1024)
				print "New Pass" + passWord
				accounts[userIndex][1] = passWord
				reply = "choos" + menu  # Tell client to send New password
				conn.send(reply)
			### Print New Messages
			elif data == '3': 
				if accounts[userIndex][2] != 0:
					reply = printUnread(userIndex)
					accounts[userIndex][2] = 0 # Reset Unread Messages number
					conn.send(reply)
				else: # If no new message, tell user
					reply = "mesge" + "\nNo Unread Messages\n"
					conn.send(reply)
			### Send Message
			elif data == '4':
				reply = "choos" + "Recipient:" # Ask for recipient
				conn.send(reply)
				rcvd= conn.recv(1024)
				recipient = findUser(rcvd) # Get Recipient
				print "Rcpnt:" + accounts[userIndex][0] + " Sender:" + user
				reply = "choos" + "Message:"   # Ask for Message
				conn.send(reply)
				rcvd= conn.recv(2048)
				print "Msg:" + rcvd
				msg = []
				msg.append(str(user))			#Attach Sender Name
				msg.append(str(rcvd))			#Attach Message

				accounts[recipient][3].append(msg) # Add Message
				accounts[recipient][2] = accounts[recipient][2] + 1 # Add Message
				reply = "choos" + "New Messages:" + str(accounts[userIndex][2]) + "\nFriend Requests:" + str(accounts[userIndex][4]) + options # Output possible menu	
				conn.send(reply)
			# Accept Friends
			elif data == '5':
				if accounts[userIndex][4] != 0: # Check if there are new ones
					adding = ""
					for requests in accounts[userIndex][5]:
						if requests[1] == 0: #If not friends Yet Output
							reply = "frndr" + requests[0]
							conn.sendall(reply)
							response = conn.recv(1024)
							if response == '1': # If yes, change the flag as friends
								accounts[userIndex][4] = accounts[userIndex][4] - 1 # Reduce Waiting Requests
								requests[1] = 1	
								adding = requests[0]
								break;
							else:
								print "Request Rejected"
					
			
					adding = findUser(adding) #Finds the user being added
					for acct in accounts[adding][5]:
						if acct[0] == user:
							acct[1] = 1	
							break	
								
					reply = "choos" + "New Messages:" + str(accounts[userIndex][2]) + "\nFriend Requests:" + str(accounts[userIndex][4]) + options # Output possible menu	
					conn.send(reply)			
				else: # If no new request, tell user
					reply = "mesge" + "\nNo New Friend Requests\n"
					conn.send(reply)
			
			# Write A Post
			elif data == '6':
				reply = "choos" + "Post:\n" # Ask for recipient
				conn.send(reply)
				rcvd= conn.recv(1024)
				post = (user, "\n" + rcvd) # Include OP and his Post
				wall.append(post)			# Add post to wall
				reply = "choos" + "New Messages:" + str(accounts[userIndex][2]) + "\nFriend Requests:" + str(accounts[userIndex][4]) + options # Output possible menu	
				conn.send(reply)
			
			# Print Wall
			elif data == '7':
				reply = "walll"
				for posts in wall:
					if isFriends(userIndex, posts[0]) == 1:
						reply = reply + posts[0]  + posts[1] + "\n\n"
				conn.send(reply)
			
			# Sending Friend Request	
			elif data == '8':
				reply = "choos" + "Name: " # ask for user to add
				conn.send(reply)
				rcvd = conn.recv(1024)
				userToAdd = findUser(rcvd)	# Look for that user's index
				req = []
				req.append(user)			# Put name, and non friendship flag
				req.append(0)
				accounts[userToAdd][5].append(req)	# Add that to list
				accounts[userToAdd][4] = accounts[userToAdd][4] + 1 # Increase number of requests
				req1 = []
				req1.append(rcvd)
				req1.append(0)
				accounts[userIndex][5].append(req1)  # Add pending request to itself
				
				
				reply = "choos" + "New Messages:" + str(accounts[userIndex][2]) + "\nFriend Requests:" + str(accounts[userIndex][4]) + options # Output possible menu	
				conn.send(reply)
			
			# Print Timeline
			elif data == '9':
				reply = "timel"
				for posts in wall:
					if posts[0] == user:
						reply = reply + posts[1] + "\n\n"
				conn.send(reply)
				
			# Print Menu
			else:
				reply = "choos" + "New Messages:" + str(accounts[userIndex][2]) + "\nFriend Requests:" + str(accounts[userIndex][4]) + options # Output possible menu	
				conn.send(reply)
		break;
	conn.close
		
while 1:
	#wait to accept a connection - blocking call
	conn, addr = s.accept()
	connList.append(conn)
	#display client info
	print 'Connected with ' + addr[0] + ':' + str(addr[1])

	start_new_thread(clientthread ,(conn,))
	
s.close()

