
import OmniLib
import threading

#TODO: find a good way to sync up config objects
# what kind of a mutex to use here? hmm
class config:
	def __init__(self):
		self.mutex = threading.Lock()
		self.irc_server = "irc2.serenia.net"
		self.irc_nick = "OmniBot" #obvious
		# insert a load of default values here!
	def mutex_unlock(self):
		self.mutex.Release()
	def mutex_lock(self):
		self.mutex.Lock()
