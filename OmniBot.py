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
#import OmniLib.Config as Conf


if __name__ == "__main__":
    # And so begins the main
    global PLUGINS_OMNIBOT_MAIN
    OmniLib.debug.debug("[+] Initializing OmniBot!")
    PLUGINS_OMNIBOT_MAIN = OmniLib.plugins.LoadPlugins("Main")
    if(PLUGINS_OMNIBOT_MAIN.len() > 0):
	try:
	    for plugin in PLUGINS_OMNIBOT_MAIN:
		plugin.main()
	except NO_CONTINUE:
	    pass
    