#!/usr/bin/python

#
# OmniBot main source file
# parse options to edit the Config object, start the threads for each
# protocol and logging thread

import os
import sys
import re

sys.path.append(os.curdir + os.sep)
import OmniLib
import OmniLib.debug
import OmniLib.plugins
import OmniLib.plugins.PluginManager
#import OmniLib.Config as Conf

NO_CONTINUE = 1

if __name__ == "__main__":
    # And so begins the main
    OmniLib.editme="mooface"
    global PLUGINS_OMNIBOT_MAIN
    OmniLib.debug.debug("[+] Initializing OmniBot!")
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




if __name__ == "TEST":
    ## SIMPLE TESTS - ignore
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
