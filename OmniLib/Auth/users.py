# this is the user object's file
# essentially we're moving away from the dictionary approach and moving to something
# a LOT more OOP, and perhaps easier to handle for multiple protocols
# import Lock from thread
import os
import base64
from threading import Lock
import threading
from Crypto.Cipher import AES

class user:
    def __init__(self, protocols):
	#self.lock = threading.Lock.acquire()
	self.gen_timeout = 0
	self.timeout = 0
	self.private_key = ""
	self.genkey = ""
	self.encryption_key = ""
	self.encryption_enabled = False
	self.is_authd = False
	self.priv_level = ""
	self.email = ""
	self.userstring = ""
	self.username = "" # for irc
	self.nick = "" # for irc
	self.screen_name = "" # for AIM
	self.host = "" # multiple
	self.protocols = protocols # IRC, aim, http?
	#self.lock=Lock.release()
	
    def lock(self): # this is a waiting acquire.. perhaps a nonblocking conditional would be better?
	self.lock = Lock.acquire()
    def unlock(self):
	self.lock = Lock.release()
	
    def decrypt(self, msg):
	msg=base64.b64decode(msg)
	enc = AES.new(self.encryption_key, AES.MODE_CBC)
	msg=enc.decrypt(msg)
	msg=base64.b64decode(msg)
	return msg
	
	
    def encrypt(self, msg):
	enc = AES.new(self.encryption_key, AES.MODE_CBC)
	msg = base64.b64encode(msg)

	if((msg.__len__() % 16) != 0):
	    msg = msg + "="*(16-msg.__len__() % 16) # padding

	msg=enc.encrypt(msg)
	msg=base64.b64encode(msg)
	return msg    

    def keygen(self, private_key): #creates genkey and encryption_key
	if(self.private_key != private_key):
	    return -1
	self.genkey=os.urandom(32) # 256 bit keys
	self.encryption_key = os.urandom(32) # 256 bit key, base64 it when u print it in the email..
	self.genkey=base64.b64encode(self.genkey) #gotta make it printable
	
    # these keys may be decrypted first before entering the object, the host should be checked too
    # optionally but again this is outside of the object
    def authenticate(self, genkey, private_key):
	if(self.genkey != genkey or self.private_key != private_key or self.gen_timeout > 0):
	    return False
	else:
	    self.genkey = ""
	    self.gen_timeout = 0
	    self.is_authd = True
	    self.timeout = 60*60 # start timer
	    return True
	