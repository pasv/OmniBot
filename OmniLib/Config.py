
import OmniLib
import threading

# what kind of a mutex to use here? hmm
class config:
	def __init__(self):
		self.mutex = threading.Lock()
		self.irc_server = "irc2.serenia.net"
		self.default_irc_nick = 
		# insert a load of default values here!
	def mutex_unlock(self):
		self.mutex.Release()
	def mutex_lock(self):
		self.mutex.Lock()
