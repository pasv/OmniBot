
import OmniLib
import OmniLib.debug
import OmniLib.Auth
import OmniLib.Auth.irc_auth
# this is the basic OmniLib.Auth hook/tie in module

def e_PRIVMSG(irc_o, userstring, action, target, content):
    if(content[0] == "!auth"):
	user = userstring[:userstring.find("!")].replace(":", "")
	if(target != irc_o.nick):
	    irc_o.privmsg(user, "!auth: not supported for non PM communications, use this PM instead")
	if(content[0] == "-keygen"):
	    if(OmniLib.Auth.irc_auth.keygen(userstring) == -1):
		irc_o.privmsg(user, "!auth: your nick/host isn't on our list for keygen-capable users, this attempt has been logged")
	    else:
		irc_o.privmsg(user, "!auth: key sent to your out of band account")
	if(content[0] == "-key"):  #user should send !auth -key [private_key] [generated key]
	    if(OmniLib.Auth.irc_auth.auth_request(userstring, content[1:]) == -1):
		irc_o.privmsg(user, "!auth: you have been authenticated, timeout in " + OmniLib.Auth.irc_auth.authd_users[userstring]["timeleft"]*60 + "minutes"
	    else:
		irc_o.privmsg(user, "!auth: your nick/host didn't match a key, this attempt has been logged")
	if(content[0] == "-admin"):
	    if(OmniLib.Auth.irc_auth.authd_users[userstring]["priv_level"] != "admin"): #consider changing this to irc_auth.is_admin(userstring) for in obj logging purposes
		irc_o.privmsg(user, "!auth: your nick/host isnt authenticated to admin level, this attempt has been logged")
	    else:
		# admin commands: show [timeouts,authd_users,etc], add [userstring] [email address], remove [userstring]
		if(content[1] == "show"):
		    if(content[2] == "authd_users"):
			irc_o.privmsg(user, "!auth: userstring # priv_level # email # timeleft")
			for u in OmniLib.Auth.irc_auth.authd_users.keys():
			    irc_o.privmsg(user, "!auth: " + OmniLib.Auth.irc_auth.authd_users[u]["userstring"] + " # " OmniLib.Auth.irc_auth.authd_users[u]["priv_level"] + " # " + OmniLib.Auth.irc_auth.authd_users[u]["email"] + " # " + OmniLib.Auth.irc_auth.authd_users[u]["timeleft"]
		if(content[1] == "add"): #!auth add [userstring] [priv_level] [email address]
		    if(OmniLib.Auth.irc_auth.add_trusted(content[2], content[3], content[4]) == -1):
			irc_o.privmsg(user, "!auth: failed to add " + content[2])
		    else:
			irc_o.privmsg(user, "!auth: " + content[2] + " successfully added to trusted list at level " + content[3])
		if(content[1] == "del"): #!auth del [userstring]
			if(OmniLib.Auth.irc_auth.del_trusted(content[2]) == -1):
			    irc_o.privmsg(user, "!auth: failed to delete " + content[2])
			else:
			    irc_o.privmsg(user, "!auth: " + content[2] + " successfully deleted from trusted list at level " + content[3])
		

		
