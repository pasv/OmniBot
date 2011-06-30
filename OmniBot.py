#!/usr/bin/python

#
# OmniBot main source file
# parse options to edit the Config object, start the threads for each
# protocol and logging thread


# OmniBot is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# OmniBot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with OmniBot.  If not, see <http://www.gnu.org/licenses/>.

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
OmniLib.plugs = {}
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

#add more as we go along, extras should be plugins read from the command line args
def load_plugins(extras):
    # for extra in extras
    OmniLib.plugs['main'] = OmniLib.plugins.PluginManager.LoadPlugins("Main")
    OmniLib.plugs['irc'] = OmniLib.plugins.PluginManager.LoadPlugins("IRC")
    
if __name__ == "__main__":
    # And so begins the main
    OmniLib.editme="mooface"
    # global OmniLib.plugs
    OmniLib.debug.debug("[+] Initializing OmniBot!")
    parse_args(sys.argv)
    if (OmniLib.testing):
	## SIMPLE TESTS - ignore   && damn this is a crappy way to do this... Clean up this hackiness
	print "Entering TEST mode"
    
    load_plugins([])

    if(OmniLib.plugs['main'].__len__()> 0):
	try:
	    for plugin in OmniLib.plugs['main']:
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
