import socket
import os, sys
#import OmniLib.Config
import OmniLib.debug
import threading
import socket
import re
import OmniLib
import OmniLib.debug
import OmniLib.Auth
OmniLib.debug.debug ("Entered " + __name__)

# TODO: clean this entire file up
# TODO: code against more exceptions/faults/server errors/nick collisions/etc

class IRC(threading.Thread):
    def __init__(self,global_queue):
	self.global_queue = global_queue
	#all this is just for testing...
	self.channels = ['#testing', '#omnibot'] # change later! also add key support
	self.nick = "OmniBot"
	self.server="irc2.serenia.net"
	self.port = 6667
	self.legal_events = ['PRIVMSG', 'MODE', 'TOPIC'] # add more later?
	
	threading.Thread.__init__(self)
    def run(self):
	# This is where the IRC session starts
	# TODO: add the plugin handler here
	self.init_connect()
	
    def init_connect(self):
	# The socket portion starts here..
	self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	self.sock.connect((self.server, self.port))
	self.send("NICK " + self.nick)
	self.send("USER m mo moo :Moof moo ") # obviously this should be changed for each value
	for chan in self.channels:
	    self.send("JOIN " + chan)
	try:
	    self.event_loop()
	except KeyboardInterrupt:
	    sys.exit(1)
	
    # this will be the main event loop for the IRC bot
    def event_loop(self):
	while (True):
	    # There is likely a more efficient way to recv TODO
	    r=''
	    recvd=""
	    while(1):
		recvd=recvd+str(r)
		if(r == '\n'):
		    OmniLib.debug.debug( "RECV: " + str(recvd) )#for a test
		    self.parse_recvd(recvd)
		    recvd=""
		r=self.sock.recv(1)
		if not r:
		    break
	    print "Socket closed! Lets get out"
	    sys.exit(-1)
	    return
    # TODO: find better ways to handle all this memory it is a LOT of copy operations, perhaps
    # work by reference?
    #Design consideration: Im sending both the parsed data and recvd because recvd will contain
    # the full contents (whitespaces included) and I dont want to resplit it.., perhaps there
    # is a better way? perhaps splitting the array better... will revise in future TODO!
    def event_PRIVMSG(self, data, recvd):
	userstring = str(data[0])
	action = str(data[1])
	target = str(data[2])
	data[3]=data[3][1:] # strip out pesky ':'
	content = data[3:]
	for plugin in OmniLib.plugs['irc']:  #consider redo?
	    plugin.e_PRIVMSG(self, userstring, action, target, content)
	    
	if(content[0] == "!quit"): #cuz it's annoying for now
	    self.send("QUIT")
	if(OmniLib.testing):
	    if(content[0] == "!eval"):
		cmd = ""
		for i in range(content.__len__()-1):
		    cmd = cmd + content[i+1] + " "
		OmniLib.debug.debug ("EVAL: " + cmd)
		try:
		    eval(cmd)
		except:
		    OmniLib.debug.debug ("incorrect syntax or some other exception")
	
    def event_MODE(self, data, recvd):
	pass
    def event_TOPIC(self, data, recvd):
	pass
    def event_PART(self, data, recvd):
	pass
    def event_JOIN(self, data, recvd):
	pass
    def event_KICK(self, data, recvd):
	pass
    
    # hook this later for encryption/logging
    def privmsg(self, target, msg):
	self.send("PRIVMSG " + target + " :"+msg)
	
    #obviously not the best way of doing things, index out of bounds can happen quite easily, fix me
    def parse_recvd(self, recvd):
	#insert plugin handling here
	#[userstring, action, target, content] = 
	data=recvd.split()
	userstring = str(data[0])
	action = str(data[1])
	if(userstring == 'PING'): #TODO: make this a little prettier
	    self.send("PONG " + action)
	    return
	target = str(data[2])
	content = data[3:]
	
	if(action in self.legal_events): #here is our dispatch
	    exec("self.event_" + action + "(data, recvd)")
	#else    #unknown case...
	#    return
	#testing...
	#print "userstring: " + userstring + " content: " + str(content[0][1:]+str(content[1:])) #pesky ';'
	return
	
    # TODO: add better sending handler, check sentlen against msglen
    def send(self, msg):
	msg = msg + "\r\n"
	try:
	    self.sock.send(msg)
	except:
	    pass #for now....
	