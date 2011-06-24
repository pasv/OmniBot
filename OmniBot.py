#!/usr/bin/python

#
# OmniBot main source file
# parse options to edit the Config object, start the threads for each
# protocol and logging thread

import os
import sys
import re,time
import threading
import getopt
#import queue
sys.path.append(os.curdir + os.sep)
import OmniLib
import OmniLib.debug
import OmniLib.plugins
import OmniLib.plugins.PluginManager
import OmniLib.Auth
import OmniLib.Comm
import OmniLib.Comm.IRC.irc
import OmniLib.Config

VERSION = "v0.1"
NO_CONTINUE = 1
debug = False
OmniLib.testing = False #obviously this is for the devel branch only! take it out for master
def parse_args(argv):
    try:
	options, therest = getopt.getopt(argv[1:], 'c:dvht', ['config=','debug', 'version', 'help', 'testing'])
    
	for opt, arg in options:
	    if opt in ('-c', '--config'):
		config_file = arg
	    elif opt in ('-d', '--debug'):
		debug = True
	    elif opt in ('-v', '--version'):
		print VERSION
	    elif opt in ('-h', '--help'):
		usage(argv[0])
	    elif opt in ('-t', '--testing'):
		OmniLib.testing=True
    except getopt.GetoptError:
	usage(argv[0])

def usage(path):
    print "Usage:"
    print path + " [-v] [-c file] [-d]"
    print "\t-v\t\t--version"
    print "\t-c file\t\t--config file"
    print "\t-d\t\t--debug"
    print "\t-h\t\t--help"
    sys.exit(-1)



if __name__ == "__main__":
    # And so begins the main
    OmniLib.editme="mooface"
    global PLUGINS_OMNIBOT_MAIN
    OmniLib.debug.debug("[+] Initializing OmniBot!")
    parse_args(sys.argv)
    if (OmniLib.testing):
	## SIMPLE TESTS - ignore   && damn this is a crappy way to do this... Clean up this hackiness
	print "Entering TEST mode"
    PLUGINS_OMNIBOT_MAIN = OmniLib.plugins.PluginManager.LoadPlugins("Main")
    OmniLib.debug.debug(PLUGINS_OMNIBOT_MAIN.__len__())
    if(PLUGINS_OMNIBOT_MAIN.__len__()> 0):
	try:
	    for plugin in PLUGINS_OMNIBOT_MAIN:
		try:
		    plugin.main()
		except:
		    print plugin.__name__ + " didnt work for main()"
	except NO_CONTINUE:
	    pass
    
    # here goes nothing...
    global_queue = 'addme' # queue.Queue()
    IRC_thread=OmniLib.Comm.IRC.irc.IRC(global_queue)
    IRC_thread.start()
    print "entering forever loop" #testonly
    IRC_thread.join()


if (OmniLib.testing):
    ## SIMPLE TESTS - ignore   && damn this is a crappy way to do this... Clean up this hackiness
    OmniLib.debug.debug("Entering TEST mode")
    CA=OmniLib.Auth.CentralAuth()
    class Omni:
	def funky(self):
	    self.moof='moo'
    m=Omni()
    m.funky()
    OmniLib.plugins.PluginManager.PluginSync(Omni, plugin)
    print m.moof
   # m.funky()
    m2=Omni()
    m2.funky()
    print OmniLib.editme
