import OmniLib
import OmniLib.debug
import OmniLib.Auth.smtp
import OmniLib.Auth.users
import OmniLib.Auth.pastebin

authd_users = {}
trustd_users = []

def init():
    OmniLib.debug.debug("Initializing Authentication module")

    #ahem some default test options anyone?
    OmniLib.Auth.irc_auth.trustd_users.append(":pasv!~l@sa-9AC43B12.socal.res.rr.com")
    OmniLib.Auth.user_db["pasv"] = OmniLib.Auth.users.user(['irc'])
    OmniLib.Auth.user_db["pasv"].priv_level = "admin" # privlevels admin - user
    OmniLib.Auth.user_db["pasv"].timeleft = 9999999 # when timeleft =< 0 authflag sets to false
    OmniLib.Auth.user_db["pasv"].email = "pasvninja@gmail.com" # email to send genkey to
    OmniLib.Auth.user_db["pasv"].authflag = True # determines if the user is genkeyed or not
    OmniLib.Auth.user_db["pasv"].genkey = "z85qZo!skdq"
    OmniLib.Auth.user_db["pasv"].private_key = "priv8"
    
def keygen(user,userstring, private_key):
    if(userstring not in trustd_users):
	# log attempt!
	return -1
    key=OmniLib.Auth.user_db[user].keygen(private_key)
    if(key == -1):
	return -1
    msg = "OmniBot generated genkey " + key + " for user: " + user + "\n authenticate with: !auth -key [private_key] " + key
    if(OmniLib.Auth.user_db[user].email == "pastebin"):
	url=OmniLib.Auth.pastebin.post_it(msg) #yes that is insecure but some people dont have gmail..
	return url
    else:
	OmniLib.Auth.smtp.send_email(OmniLib.Auth.user_db[user].email, msg)
	return 0

def auth_request(userstring, private_key, genkey):
    if(not authd_users.has_key(userstring)):
	return -1
    return OmniLib.Auth.user_db[user].authenticate(private_key, genkey)

# we should really hash/encrypt the genkey/authkey with DES or something..
def add_trusted(userstring, priv_level, email):
    (nick, username, host) = OmniLib.Comm.IRC.irc.parse_userstring(userstring)
    OmniLib.Auth.irc_auth.trusted_users.append(userstring)
    if(not OmniLib.Auth.user_db.has_key(nick)):
	OmniLib.Auth.user_db[nick] = OmniLib.Auth.users.user(['irc'])
	OmniLib.Auth.user_db[nick].nick = nick
	OmniLib.Auth.user_db[nick].username = username
	OmniLib.Auth.user_db[nick].host = host
	OmniLib.Auth.user_db[nick].priv_level = priv_level
	OmniLib.Auth.user_db[nick].email = email
    else:
	return -1 # user exists! use mod_users()
	
def del_trusted(userstring): #note this is for the trusted list not the authd_users
    if(userstring in trustd_users):
	del trustd_users[userstring]
	#del authd_users[userstring]
    else:
	return -1
