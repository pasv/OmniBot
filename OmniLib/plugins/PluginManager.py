import OmniLib
import OmniLib.debug
import os,sys

# HTTP_PLUGINS.append(__import__("libmiddler.plugins.http.%s"%filename[:-3], None, None, "libmiddler.plugins.http"))

def LoadPlugins(category):
    ret_plugins = []
    plugins_dir = os.curdir + "/" + "OmniLib" + "/" + "plugins" + "/" + category + "/"
    #plugin_files = os.listdir(plugins_dir)
    plugins_dir=plugins_dir[2:]
    OmniLib.debug.debug("DEBUG: plugins dir=" + plugins_dir)

    for plugin in os.listdir(plugins_dir):
	if(plugin[-3:] == ".py" and plugin[1] != "_"):
	    OmniLib.debug.debug("DEBUG: loading " + ("OmniLib.plugins." + category + "." + plugin[:-3]))
	    ret_plugins.append(__import__(("OmniLib.plugins." + category + "." + plugin[:-3]), None, None, ("OmniLib.plugins." + category)))
	    
    return ret_plugins