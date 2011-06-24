
import OmniLib
import OmniLib.debug

def e_PRIVMSG(irc_o, userstring, action, target, content):
    if(content[0] == "!ping"):
	OmniLib.debug.debug("!ping command issued from plugin")
	irc_o.send("PRIVMSG " + target + " :pong!")
