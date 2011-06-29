
import OmniLib
import OmniLib.debug
import OmniLib.Auth
import OmniLib.Auth.irc_auth
# this is the basic OmniLib.Auth hook/tie in module
def init(irc_o):
    OmniLib.Auth.irc_auth.init() # initializes defaults
    
def e_PRIVMSG(irc_o, userstring, action, target, content):
    if(content[0] == "!auth"):
	user = userstring[:userstring.find("!")].replace(":", "")
	if(target != irc_o.nick):
	    irc_o.privmsg(user, "!auth: not supported for non PM communications, use this PM instead")
	if(content[1] == "-keygen"):
	    url=OmniLib.Auth.irc_auth.keygen(userstring)
	    if(url == -1):
		irc_o.privmsg(user, "!auth: your nick/host isn't on our list for keygen-capable users, this attempt has been logged")
	    else:
		if(url):
		    irc_o.privmsg(user, "!auth: the key is temporarily stored at " + url + " :get it quick")
		else:
		    irc_o.privmsg(user, "!auth: key sent to your out of band account")
	if(content[1] == "-key"):  #user should send !auth -key [private_key] [generated key]
	    if(OmniLib.Auth.irc_auth.auth_request(userstring, content[1:]) == -1):
		irc_o.privmsg(user, "!auth: you have been authenticated, timeout in " + OmniLib.Auth.irc_auth.authd_users[userstring]["timeleft"]*60 + "minutes")
	    else:
		irc_o.privmsg(user, "!auth: your nick/host didn't match a key, this attempt has been logged")
	if(content[1] == "-admin"):
	    if(content.__len__() < 4):
		irc_o.privmsg(user, show_admin_help())
		return -1
	    if(not OmniLib.Auth.irc_auth.authd_users.has_key(userstring)):
		irc_o.privmsg(user, "!auth: your nick/host isnt authenticated to admin level, this attempt has been logged")
		return -1
	    if(OmniLib.Auth.irc_auth.authd_users[userstring]["priv_level"] != "admin"): #consider changing this to irc_auth.is_admin(userstring) for in obj logging purposes
		irc_o.privmsg(user, "!auth: your nick/host isnt authenticated to admin level, this attempt has been logged")
		return -1
	    else:
		# admin commands: show [timeouts,authd_users,etc], add [userstring] [email address], remove [userstring]
		if(content[2] == "show"):
		    if(content[3] == "authd_users"):
			irc_o.privmsg(user, "!auth: userstring # priv_level # email # timeleft")
			for u in OmniLib.Auth.irc_auth.authd_users.keys():
			    irc_o.privmsg(user, "!auth: " + u + " # " + OmniLib.Auth.irc_auth.authd_users[u]["priv_level"] + " # " + OmniLib.Auth.irc_auth.authd_users[u]["email"] + " # " + str(OmniLib.Auth.irc_auth.authd_users[u]["timeleft"]))
		if(content[2] == "add"): #!auth add [userstring] [priv_level] [email address]
		    if(content.__len__() != 6):
			irc_o.privmsg(user, show_admin_help())
			return -1
		    if(OmniLib.Auth.irc_auth.add_trusted(content[3], content[4], content[5]) == -1):
			irc_o.privmsg(user, "!auth: failed to add " + content[2])
		    else:
			irc_o.privmsg(user, "!auth: " + content[2] + " successfully added to trusted list at level " + content[3])
		if(content[2] == "del"): #!auth del [userstring]
			if(OmniLib.Auth.irc_auth.del_trusted(content[3]) == -1):
			    irc_o.privmsg(user, "!auth: failed to delete " + content[3])
			else:
			    irc_o.privmsg(user, "!auth: " + content[3] + " successfully deleted from trusted list at level " + content[4])
		
def show_admin_help():
    return """!auth -admin [show [authd_users]] [del [userstring]] [add [userstring] [priv_level] [email]] [help]"""


