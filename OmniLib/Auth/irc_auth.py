import OmniLib
import OmniLib.debug

authd_users = {}{}
trustd_users = []

def init(self):
    OmniLib.debug("Initializing Authentication module")
    authd_users = {}{}
    trustd_users = []

def keygen(userstring, private_key):
    if(userstring not in trustd_users):
	# log attempt!
	return -1

def auth_request(userstring, private_key, genkey):
    pass
def add_trusted(userstring, priv_level, email_address):
    pass
def del_trusted(userstring):
    pass
