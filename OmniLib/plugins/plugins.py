import OmniLib
import os,sys

def LoadPlugins(category):
    ret_plugins = []
    plugins_dir = os.curdir + os.sep + "OmniLib" + os.sep + "plugins" + os.sep + category + os.sep
    plugin_files = os.listdir(plugins_dir)
    for plugin in plugin_files:
	ret_plugins.append(__import__(plugins_dir + os.sep + plugin))
	
    return ret_plugins